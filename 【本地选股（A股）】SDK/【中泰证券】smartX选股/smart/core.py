from . import smartc
from . import logging_config
from .event import *
from .emitter import *
from .account import *
from .account_manager import *
from . import utils
from .utils import *
from .type import *
from .cache import *
from .strategy_manager import *
from .book_manager import *
import os
import math
import time
import json
import uuid
from datetime import datetime
import logging
logger = logging.getLogger()


from . import bt_core
from .bt_core import *


smart = None
'''
smart模块的api入口  对于策略开发者来说，smart模块是作为顶层“对象”使用
smartc支持接口及说明:
        .init() #只调用一次
        .init_end() #只调用一次
        .request(string redisCmd , string json ,Function cb) #redisCmd:"insertOrder"
        .get(string key) #key为redis的key name
        .on(string eventName) #eventName为约定的事件名称
'''




class Smart(Emitter):
    def __init__(self) -> None:
        if smart is not None:
            return smart  # 确保单例
        super().__init__()
        self.Event = Event
        self.initCallback = None
        self.showCallback = None
        self.hideCallback = None
        self.closeCallback = None
        self.resetCallback = None
        # self.version = version
        self.Event = Event
        self.Type = Type
        self.utils = utils
        utils.smart = self
        bt_core.smart = self
        self.cache:Cache = Cache()
        # self.logger = logger
        # 账号
        self.account_map = {}  # 当前客户端已经登录的账号map key为资金账号 value为Account对象
        self.current_account:Account = None  # 当前登录账号的引用
        # plugin 提供的实时数据
        self.instrument_map_by_type = {}  # 按照类型分类的证券列表  #todo： 命名需要有含义
        self.instrument_list = []  # 所有证券列表
        self.instrument_map = {}  # key为证券代码_市场  方便查找证券
        self.etf_map = {}  # etf可交易map集合，key为证券代码  value为etf配方表ETF对象
        self.etf_profit_map = {}  # etf预期利润，key为证券代码，value为利润对象
        self.reverse_repo_list = []  # 国债逆回购列表
        self.index_map = {}  # 指数集合，key为指数代码，value为instrument对象
        # self.alphax_td_list = []  #
        # self.alphax_md_list = []
        self.ipo_map = {}  # IPO的map集合，key为证券代码_exchangeId value为IPO对象
        self.isReady = False
        self.__positionList = []
        self.__instrumentMap = {}  # 所有证券的map集合，内部使用 方便快速查找 key为"证券代码_交易所id"  value为instrument
        self.__subMap = {}  # 订阅关系表
        self.__quoteMap = {}  # 行情缓存
        self.__subIndicatorMap = {}  # 指标订阅关系表
        self.__quoteIndicatorMap = {}  # 指标行情缓存
        self._etfProfitSubCount = 0  # etf折溢价预期利润订阅计数器
        self._etfProfitSubCBList = [] # etf订阅缓存回调列表
        self.accountManager:AccountManager = AccountManager(self)
        self.strategyManager:StrategyManager = StrategyManager(self)
        self.strategyManager.accountManager = self.accountManager
        self.strategy_map = {}
        self._timerMap:dict = {}
        self.dataType = {}

        # 格式为整型，如 20220920093005000  年月日时分秒毫秒
        self.current_time = 0
        self.is_back_test = False

        self.bt_static_quote_size = 0
        self.quote_share_mem = bytearray(1024)
        self.order_share_mem = bytearray(1024)
        self.trade_share_mem = bytearray(1024)
        self.bar_share_mem = bytearray(1024)
        self.static_quote_share_mem = bytearray(1024 * 1024 * 8)

        self.bt_time_map:dict = {}
        
        self.book = None
        self.bookManager = BookManager(self)
        self.pluginName = ""
        self.systemset = {}

        self.on_bar = None # bar行情订阅后，bar行情推送的回调函数
        self.on_indicator = None # 通用指标订阅后，指标数据推送的回调函数 
        
        self.current_date = None

    def init(self,config:dict):
        logger.debug("初始化用户数据")
        defaultConfig = {
            "iName":"",
            "iNameReqRep":"",
            "configPath":"",
            "logPath":"",
            "plugin_id":"",
            "isBacktest":False,
            "btconfig":None,
            "enginConfig":None,
            "btId":""
        }
        self.config = config or defaultConfig
        # logger.debug("config is  :%s",str(self.config))
        p = config.get("logPath","")

        self.pluginName =  config.get("plugin_id","")
        clogPath = os.path.join(p,self.pluginName)+"py_c.log"
        if self.config.get("isBacktest"):
            self.is_back_test = True
            btconfig = self.config.get("btconfig")
            clogPath = os.path.join(p,self.pluginName)+"py_c_bt.log"
            if not btconfig:
                logger.error("init error,no btconfig")
                return
            code = smartc.init(self.config.get("iName"),self.config.get("iNameReqRep"),clogPath,btconfig.get("btId"),json.dumps(self.config.get("enginConfig")),btconfig.get("enginLogConfig"),btconfig.get("enginInitConfig"),btconfig.get("enginOutput"))
        else:
            code = smartc.init(self.config.get("iName"),self.config.get("iNameReqRep"),clogPath,"","","","","")
        if code and code != 0:
            logger.error("init smartc error :%s",str(code))

        if self.is_back_test :
            smartc.set_quote_addr(self.quote_share_mem)
            smartc.set_order_addr(self.order_share_mem)
            smartc.set_trade_addr(self.trade_share_mem)
            smartc.set_bar_addr(self.bar_share_mem)
            self.bt_static_quote_size = smartc.set_static_quote_addr(self.static_quote_share_mem)

            logger.debug("quote_share_mem address :%s",str(hex(id(self.quote_share_mem))))

        logger.debug("init ended")

    def init_end(self):
        self.initEvent()
        etfSystem = None
        def account_callback():
            logger.debug("用户数据初始化完成")
            self.isReady = True
            smartc.change_comm_mod(0,1)
            if not self.is_back_test :
                #初始化book数据
                self.bookManager.init_books(etfSystem)
                self.initCallback()
            

        #读取用户本地cache数据
        def cacheSyncCallback(rsp:str):
            try:
                dataCache = decodeRsp(rsp)
                self.cache.update(dataCache.get("cache",{}))
                self.systemset = dataCache.get("systemset",{})
                nonlocal etfSystem
                etfSystem = dataCache.get("etfSystem",{})
                #初始account用户数据
                self.accountManager.initUserData(self.config.get("configPath"),None, account_callback)
            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
            
        smartc.request("cacheSync", "{}",cacheSyncCallback)
        status = {
            "btId": self.config.get("btId"),
            "moduleId": self.config.get("plugin_id"),
            "status":1
        }
        smartc.request("btStartRsp", json.dumps(status),None)
        smartc.init_end()

    # 初始化完成回调
    def on_init(self, cb):
        self.initCallback = cb

    # 显示完成回调
    def on_show(self, cb):
        self.showCallback = cb

    # 隐藏完成回调
    def on_hide(self, cb):
        self.hideCallback = cb

    # 关闭回调
    def on_close(self, cb):
        self.closeCallback = cb

    # 用户退出清空插件
    def on_reset(self, cb):
        self.resetCallback = cb

    def get_submap(self) :
        return self.__subMap

    def get_quoteMap(self) :
        return self.__quoteMap

    def get_quoteIndicatorMap(self) :
        return self.__quoteIndicatorMap

    def get_subIndicatorMap(self) :
        return self.__subIndicatorMap

    def initEvent(self):
        
        def nextDayHandler(data):
            logger.debug("nextDayHandler:"+data)
            try:
                self.current_date = data
                self.current_time = int(data) * 100000
                self.etf_map = {}
                self.removeEventListener(None, None)
                self.current_account.removeEventListener(None, None)
                self.initCallback and self.initCallback()
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on("CHANGE_DAY",nextDayHandler)

        def closeHandler(data):
            #book数据持久化存储到本地
            try:
                if not self.is_back_test :
                    self.bookManager.dump()
                self.closeCallback and self.closeCallback()
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on(Event.ON_CLOSE,closeHandler)

        def hideHandler(data):
            try:
                self.hideCallback and self.hideCallback()
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on(Event.ON_HIDE,hideHandler)

        def showHandler(data):
            try:
                self.showCallback and self.showCallback()
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on(Event.ON_SHOW,showHandler)

        def resetHandler(data):
            try:
                self.resetCallback and self.resetCallback()
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on(Event.ON_RESET,resetHandler)

 
        #行情
        def quoteHandler(data:str):
            # logger.debug("quoteHandler data: %s", data)
            quote = Quote()
            if self.is_back_test :
                bt_core.back_test_quote_handler()
                return

            else :
                try:
                    quote_json = json.loads(data)
                    quote = convertQuoteFromSmartToPlugin(quote_json)
                except Exception as err:
                    logger.error(err,exc_info=True, stack_info=True)
            
            try :
                key = quote.instrument_id + "_" + quote.exchange_id
                if not (key in self.__subMap) :
                    logger.debug("not find key: %s", key)
                    return #未订阅终止派发

                self.__quoteMap[key] = quote #缓存更新行情数据
                subList = self.__subMap.get(key)
                for subObj in subList:
                    subObj["emitter"].emit(Event.ON_QUOTE,quote)
                
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)

        if self.is_back_test :
            smartc.on(Event.QUOTE,back_test_quote_handler)
        else:
            smartc.on(Event.QUOTE,quoteHandler)


        # 指标行情(bar、macd等行情)
        def quoteBarHandler(data: str):
            if self.is_back_test :
                # 回测时 data 为 ""
                bt_core.back_test_bar_handler(data)
                return

            try:
                quoteData = json.loads(data)
                # logger.debug("quoteIndicatorHandler:%s", quoteData)
                quote = quoteData["data"]
                key = quoteData["type"] + '_' + quote["code"]

                if not (key in self.__subIndicatorMap):
                    return  # 未订阅终止派发

                quote = convertQuoteIndicatorFromSmartToPlugin(quoteData["type"], quote)
                self.__quoteIndicatorMap[key] = quote  # 缓存更新行情数据
                subList = self.__subIndicatorMap.get(key)
                for subObj in subList:
                    subObj["emitter"].emit(Event.ON_BAR, quote)
            except Exception as err:
                logger.error(err, exc_info=True, stack_info=True)
        smartc.on(Event.QUOTEBAR, quoteBarHandler)

        # 通用指标行情
        def quoteIndicatorHandler(data: str):
            try:
                quoteData = json.loads(data)
                # logger.debug("quoteIndicatorHandler:%s", quoteData)
                quote = quoteData["data"]
                key = quoteData["type"] + '_' + quote["code"]

                if not (key in self.__subIndicatorMap):
                    return  # 未订阅终止派发

                # quote = convertQuoteIndicatorFromSmartToPlugin(quoteData["type"], quote)
                # self.__quoteIndicatorMap[key] = quote  # 缓存更新行情数据
                subList = self.__subIndicatorMap.get(key)
                for subObj in subList:
                    subObj["emitter"].emit(Event.ON_INDICATOR, quoteData["type"], quote)
            except Exception as err:
                logger.error(err, exc_info=True, stack_info=True)
        smartc.on(Event.QUOTEINDICATOR, quoteIndicatorHandler)

        
        #读取所有的静态行情信息
        def initAllTickers(allTickers:str):
            if self.is_back_test :
                return bt_core.init_all_static_tickers_from_bt(allTickers)
            try:
                allTickerList = json.loads(allTickers)

                _instrumentList = []
                _instrumentMap = {}
                _instrumentTypeMap = {
                    InstrumentType.Unknown: [], #未知 xtp:5 XTP_TICKER_TYPE_UNKNOWN
                    InstrumentType.Stock: [], #股票 xtp:0 XTP_TICKER_TYPE_STOCK普通股票
                    InstrumentType.Future: [], #期货
                    InstrumentType.Bond: [], #债券 xtp:3 XTP_TICKER_TYPE_BOND债券
                    InstrumentType.StockOption: [], #股票期权 xtp:4 XTP_TICKER_TYPE_OPTION期权
                    InstrumentType.Index: [], #指数 xtp:1 XTP_TICKER_TYPE_INDEX指数
                    InstrumentType.Fund: [], #基金 xtp:2 XTP_TICKER_TYPE_FUND基金
                }
                _reverseRepoList = []
                _indexMap = {}

                def initInstrument(it):
                    instrument = Instrument()
                    try:
                        instrument.instrument_id = it.get("ticker") #合约ID(证券代码)
                        instrument.instrument_name = it.get("tickerName") or "" #证券名称
                        securityType = it.get("securityType","XTP_TICKER_TYPE_UNKNOWN")
                        instrument.instrument_type = convertInstrumentTypeFromXtpSecurityType(securityType) #证券类型 InstrumentType枚举值  对应smart的securityType
                        instrument.instrument_type_ext = securityType

                        instrument.exchange_id = convertExchangeIdFromxtpExchangeId(it.get("exchangeId"))
                        instrument.exchange_id_name = dataTypeToName(instrument.exchange_id, "ALPHAX_EXCHANGE_TYPE") #交易所名称
                        instrument.xtp_market_type = getXtpMarketTypeFromExchange(Exchange.__dict__[instrument.exchange_id]) #xtp_market_type标示
                        instrument.name_py = it.get("tickerNamePy") or "" #名称拼音首字母 namePy

                        instrument.price_tick = it.get("priceTick") if it.get("priceTick") else 0.001 #最小价格变动单位 priceTick 如0.01 没有值默认按照0.001处理
                        instrument.precision = -math.floor(math.log10(instrument.price_tick)) if instrument.price_tick < 1 else 0 #最小价格变动单位小数点后位数
                        instrument.buy_volume_unit = it.get("bidQtyUnit") # 弃用 最小买入数量 bidQtyUnit 100
                        instrument.sell_volume_unit = it.get("askQtyUnit") #弃用 最小卖出数量 askQtyUnit

                        instrument.bid_volume_unit = it.get("bidQtyUnit") # 限价买单位 bidQtyUnit
                        instrument.ask_volume_unit = it.get("askQtyUnit") # 限价卖单位 askQtyUnit
                        instrument.bid_upper_limit_volume = it.get("bidQtyUpperLimit") #限价买上限 bidQtyUpperLimit
                        instrument.bid_lower_limit_volume = it.get("bidQtyLowerLimit") #限价买下限 bidQtyLowerLimit
                        instrument.ask_upper_limit_volume = it.get("askQtyUpperLimit") #限价卖上限 askQtyUpperLimit
                        instrument.ask_lower_limit_volume = it.get("askQtyLowerLimit") #限价卖下限 askQtyLowerLimit

                        instrument.market_bid_volume_unit = it.get("marketBidQtyUnit") # 市价买单位 marketBidQtyUnit
                        instrument.market_ask_volume_unit = it.get("marketAskQtyUnit") # 市价卖单位 marketAskQtyUnit
                        instrument.market_bid_upper_limit_volume = it.get("marketBidQtyUpperLimit") #市价买上限 marketBidQtyUpperLimit
                        instrument.market_bid_lower_limit_volume = it.get("marketBidQtyLowerLimit") #市价买下限 marketBidQtyLowerLimit
                        instrument.market_ask_upper_limit_volume = it.get("marketAskQtyUpperLimit") #市价卖上限 marketAskQtyUpperLimit
                        instrument.market_ask_lower_limit_volume = it.get("marketAskQtyLowerLimit") #市价卖下限 marketAskQtyLowerLimit

                        instrument.pre_close_price = it.get("preClosePrice") #昨收价 preClosePrice
                        instrument.upper_limit_price = it.get("upperLimitPrice") #涨停价 upperLimitPrice
                        instrument.lower_limit_price = it.get("lowerLimitPrice") #跌停价 lowerLimitPrice

                        instrument.is_registration = it.get("isRegistration") # 是否注册制 isRegistration

                        instrument.kw = toCDB(trimAll(it.get("tickerName") or "")) # 删除股票名称中的空格，替换全角都替换为半角

                        exchange_str = getExchangeStrFromExchangeId(instrument.exchange_id)
                        if (exchange_str):
                            instrument.code = instrument.instrument_id + "." + exchange_str
                    except Exception as err:
                        instrument = None
                        logger.warning("%s,%s",err,it)
                    return  instrument

                def initNQInstrument(it):
                    instrument = NQInstrument()
                    try:
                        instrument.instrument_id = it.get("ticker") #合约ID(证券代码)
                        instrument.instrument_name = it.get("tickerName") or "" #证券名称
                        securityType = it.get("securityType","XTP_TICKER_TYPE_UNKNOWN")
                        instrument.instrument_type = convertInstrumentTypeFromXtpSecurityType(securityType) #证券类型 InstrumentType枚举值  对应smart的securityType
                        instrument.instrument_type_ext = securityType

                        instrument.exchange_id = convertExchangeIdFromxtpExchangeId(it.get("exchangeId"))
                        instrument.exchange_id_name = dataTypeToName(instrument.exchange_id, "ALPHAX_EXCHANGE_TYPE") #交易所名称
                        instrument.xtp_market_type = getXtpMarketTypeFromExchange(Exchange.__dict__[instrument.exchange_id]) #xtp_market_type标示
                        instrument.name_py = it.get("tickerNamePy") or "" #名称拼音首字母 namePy

                        instrument.price_tick = it.get("priceGear") if it.get("priceGear") else 0.001 #最小价格变动单位 priceTick 如0.01 没有值默认按照0.001处理
                        instrument.precision = -math.floor(math.log10(instrument.price_tick)) if instrument.price_tick < 1 else 0 #最小价格变动单位小数点后位数
                        instrument.buy_volume_unit = it.get("buyVolUnit") # 弃用 最小买入数量 100
                        instrument.sell_volume_unit = it.get("sellVolUnit") #弃用 最小卖出数量

                        instrument.bid_volume_unit = it.get("buyVolUnit") # 限价买单位
                        instrument.ask_volume_unit = it.get("sellVolUnit") # 限价卖单位
                        instrument.bid_upper_limit_volume = it.get("perLimitVol") #限价买上限 
                        instrument.bid_lower_limit_volume = it.get("miniDeclaredVol") #限价买下限 
                        instrument.ask_upper_limit_volume = it.get("perLimitVol") #限价卖上限 
                        instrument.ask_lower_limit_volume = it.get("miniDeclaredVol") #限价卖下限 

                        instrument.market_bid_volume_unit = it.get("buyVolUnit") # 市价买单位 
                        instrument.market_ask_volume_unit = it.get("sellVolUnit") # 市价卖单位 
                        instrument.market_bid_upper_limit_volume = it.get("perLimitVol") #市价买上限 
                        instrument.market_bid_lower_limit_volume = it.get("miniDeclaredVol") #市价买下限 
                        instrument.market_ask_upper_limit_volume = it.get("perLimitVol") #市价卖上限 
                        instrument.market_ask_lower_limit_volume = it.get("miniDeclaredVol") #市价卖下限 

                        instrument.pre_close_price = 0 #昨收价 preClosePrice
                        instrument.upper_limit_price = it.get("limitUpperPrice") #涨停价 
                        instrument.lower_limit_price = it.get("limitLowerPrice") #跌停价 

                        instrument.is_registration = True # 是否注册制 isRegistration

                        instrument.kw = toCDB(trimAll(it.get("tickerName") or "")) # 删除股票名称中的空格，替换全角都替换为半角

                        exchange_str = getExchangeStrFromExchangeId(instrument.exchange_id)
                        if (exchange_str):
                            instrument.code = instrument.instrument_id + "." + exchange_str
                    except Exception as err:
                        instrument = None
                        logger.warning("%s,%s",err,it)
                    return  instrument
                
                if not allTickerList or len(allTickerList)<1:
                    return
                for it in  allTickerList:
                    exchange_id = convertExchangeIdFromxtpExchangeId(it["exchangeId"])
                    instrumentID = it["ticker"] + "_" + exchange_id
                    if instrumentID in _instrumentMap:
                        continue #已经存在，结束当前证券数据处理
                    
                    instrument = None
                    if (exchange_id == Exchange.BSE) :
                        instrument = initNQInstrument(it)
                    else:
                        instrument = initInstrument(it)
                    
                    if not instrument:
                        continue #本条数据不合格跳过

                    _instrumentList.append(instrument)
                    _instrumentMap[instrument.instrument_id + "_" + instrument.exchange_id] = instrument
                    _instrumentTypeMap[instrument.instrument_type].append(instrument)
                    if (instrument.instrument_type_ext == "XTP_SECURITY_NATIONAL_BOND_REVERSE_REPO"):
                        _reverseRepoList.append(instrument)
                    if (instrument.instrument_type_ext == "XTP_SECURITY_INDEX"):
                        _indexMap[instrument.instrument_id] = instrument
                
                self.instrument_map_by_type = _instrumentTypeMap # TODO: 为何要暴露ticker？
                self.instrument_list = _instrumentList
                self.instrument_map = _instrumentMap
                self.reverse_repo_list = _reverseRepoList
                self.index_map = _indexMap
                self.emit("_INIT_ALL_TICKERS_DONE")
            except Exception as err0:
                logger.error("allTickerList:%s",allTickers)
                logger.error(err0,exc_info=True, stack_info=True)

        smartc.on(Event.INIT_ALL_TICKERS,initAllTickers)

        def initDataType(dataTypeStr:str):
            try:
                logger.debug("======================enter initDataType=====================")
                dataType = json.loads(dataTypeStr)
                smart.dataType = dataType
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on(Event.INIT_DATA_TYPE,initDataType)


        #委托数据
        def entrustHandler(data:str):
            try:
                if ( not self.current_account or not self.current_account.account_id): return #用户未初始化完，暂不接受数据推送，数据不会丢
                
                if self.is_back_test :
                    bt_core.back_test_entrust_handler()
                    return

                list = json.loads(data)
                for item in list:
                    orderObj = item.get("data")
                    orderInfo = convertOrderFromSmartToPlugin(orderObj)
                    if(orderInfo.traffic_sub_id == self.pluginName):
                        self.bookManager.on_order(orderInfo)

                    accountId = orderInfo.account_id
                    account = self.account_map.get(accountId)
                    if account:
                        account._addOrderInfo(orderInfo)
                        #如果为算法单单独分发母单的子单
                        if orderInfo.business_type == "algo" and orderInfo.parent_order_id :
                            strategie = smart.strategy_map.get(orderInfo.parent_order_id + "_algo")
                            if (strategie):strategie._addOrderInfo(orderInfo)
                        
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)

        smartc.on(Event.UPDATE_ENTRUST, entrustHandler)

        #接受smart框架的 账户级别的【成交回报】 向插件提供【on_trade】事件派发
        def tradeReportHandler(data:str):
            try:
                if ( not self.current_account or not self.current_account.account_id): return #用户未初始化完，暂不接受数据推送，数据不会丢

                if self.is_back_test :
                    bt_core.back_test_trade_report_handler()
                    return

                list = json.loads(data)
                for report in list:
                    report = convertTradeFromSmartToPlugin(report)

                    if(report.traffic_sub_id == self.pluginName):
                        self.bookManager.on_trade(report)

                    accountId = report.account_id
                    account = self.account_map.get(accountId)
                    if account:
                        account._addTradeReport(report)
                        #如果为算法单单独分发母单的子单
                        if report.business_type == "algo" and report.parent_order_id:
                            strategie = smart.strategy_map.get(report.parent_order_id + "_algo")
                            if (strategie):strategie._addTradeReport(report)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on(Event.UPDATE_TRADE_REPORT, tradeReportHandler)

        #接受smart框架的 账户级别的【撤单失败】 向插件提供【on_cancel_fail】事件派发
        def cancelFailHandler(data:str):#todo: order需要转型
            try:
                if ( not self.current_account or not self.current_account.account_id): return #用户未初始化完，暂不接受数据推送，数据不会丢
                order = json.loads(data)
                # accountId = order.get("account_id")
                account = self.account_map.get(self.current_account.account_id)
                account and account.emit(Event.ON_CANCEL_FAIL, order)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)

        smartc.on(Event.CANCEL_ORDER_FAIL_RSP, cancelFailHandler)

        #接受smart框架的 账户级别的【资产变更】 向插件提供【on_assets】事件派发
        def assetsHandler(data:str) :
            try:
                if ( not self.current_account or not self.current_account.account_id): return #用户未初始化完，暂不接受数据推送，数据不会丢
                data = json.loads(data)
                account = self.account_map.get(self.current_account.account_id) #todo:应该smart server的资产变更消息中加入资金账号字段  绍光 万佳  这里先用当前账号了
                assets = convertAssetsFromSmartToPlugin(data)
                utils.assign(account.assets, assets)
                account and account.emit(Event.ON_ASSETS, assets)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)

        smartc.on(Event.UPDATE_ASSETS, assetsHandler)

        #接受smart框架的 账户级别的【持仓变更 仅含发生变更的数据行（增量）】 向插件提供【on_position_changed】事件派发
        def updatePositionHandler(data:str) :
            try:
                if ( not self.current_account or not self.current_account.account_id): return #用户未初始化完，暂不接受数据推送，数据不会丢
                list = json.loads(data)
                account = self.account_map[self.current_account.account_id] #todo: 账号需要细化  绍光
                for row in list:
                    position = convertPositionFromSmartToPlugin(row)
                    key = "{}_{}_{}".format(position.instrument_id,position.exchange_id,position.direction)
                    oldRow = account.positionMap.get(key,None)
                    if (oldRow) :
                        utils.assign(oldRow, position)
                    else:
                        account.position_list.append(position)
                        account.positionMap[key] = position
                    account and account.emit(Event.ON_POSITION, position)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on(Event.UPDATE_POSITION, updatePositionHandler)

        #接受smart框架的 账户级别的【持仓刷新 全量的持仓数据行】 向插件提供【on_position_refresh_all】事件派发
        def refreshPositionHandler(data:str):
            try:
                if ( not self.current_account or not self.current_account.account_id): return #用户未初始化完，暂不接受数据推送，数据不会丢
                list = json.loads(data)
                account = self.account_map.get(self.current_account.account_id) #todo: 账号需要细化  绍光
                positionList = []
                for row in list:
                    position = convertPositionFromSmartToPlugin(row)
                    positionList.append(position)
                account.refreshPositionList(positionList)#更新全部持仓信息
                account and account.emit(Event.ON_POSITION_REFRESH_ALL, positionList)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on(Event.REFRESH_POSITION, refreshPositionHandler)
        
        #更新信用可融券头寸信息,处理信用可融券头寸更新
        def tickerAssignHandler(data:str):
            try:
                if ( not self.current_account or not self.current_account.account_id): return #用户未初始化完，暂不接受数据推送，数据不会丢
                account = smart.account_map[smart.current_account.account_id] #todo: 账号需要细化  绍光
                list = json.loads(data)
                for item in list:
                    temp = convertCreditTickerAssignInfoFromSmartToPlugin(item)
                    oldRow = account.credit_ticker_assign_map.get(temp.instrument_id + "_" + temp.exchange_id)
                    # for it in account.credit_ticker_assign_list:
                    #     if it.instrument_id == temp.instrument_id and it.exchange_id == temp.exchange_id:
                    #         oldRow = it
                    #         break
                    if (oldRow) :
                        utils.assign(oldRow, temp)
                    else:
                        account.credit_ticker_assign_map[temp.instrument_id + "_" + temp.exchange_id] = temp
                        account.credit_ticker_assign_list.append(temp)
                    account and account.emit(Event.ON_CREDIT_TICKER_ASSIGN, temp)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)

        smartc.on(Event.UPDATE_CREDIT_TICKER_ASSIGN_INFO, tickerAssignHandler)

        #更新信用可融券头寸信息,融资负债合约更新
        def creditDebtFinanceHandler(data:str):
            try:
                if ( not self.current_account or not self.current_account.account_id): return #用户未初始化完，暂不接受数据推送，数据不会丢
                account = smart.account_map[smart.current_account.account_id] #todo: 账号需要细化  绍光
                list = json.loads(data)
                temp = convertCreditDebtFinanceFromSmartToPlugin(list)
                oldRow = account.credit_debt_finance_map.get(temp.debt_id)
                if (oldRow) :
                        utils.assign(oldRow, temp)
                else:
                    account.credit_debt_finance_map[temp.debt_id] = temp
                    account.credit_debt_finance_list.append(temp)
                account and account.emit(Event.ON_CREDIT_DEBT_FINANCE, temp)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)

        smartc.on(Event.UPDATE_CREDITDEBTINFO_CASH, creditDebtFinanceHandler)
        

    	#更新信用可融券头寸信息,融券负债合约更新
        def creditDebtSecurityHandler(data:str):
            try:
                if ( not self.current_account or not self.current_account.account_id): return #用户未初始化完，暂不接受数据推送，数据不会丢
                account = smart.account_map[smart.current_account.account_id] #todo: 账号需要细化  绍光
                list = json.loads(data)
                temp = convertCreditDebtSecurityFromSmartToPlugin(list)
                oldRow = account.credit_debt_security_map.get(temp.debt_id)
                if (oldRow) :
                    utils.assign(oldRow, temp)
                else:
                    account.credit_debt_security_map[temp.debt_id] = temp
                    account.credit_debt_security_list.append(temp)
                account and account.emit(Event.ON_CREDIT_DEBT_SECURITY, temp)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)

        smartc.on(Event.UPDATE_CREDITDEBTINFO_SECURITY, creditDebtSecurityHandler)

        # 接受smart框架的 【ETF套利/交易费用设置通知】 向插件提供事件派发
        def etfRateHandler(data:str):
            try:
                if (not data): return
                etfSystem = json.loads(data)
                self.emit(Event.ON_ETF_RATE_UPDATE, etfSystem)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on(Event.ETF_RATE_UPDATE, etfRateHandler)

        # 更新系统全局常用设置项通知
        def systemSetUpHandler(data:str):
            try:
                if (not data): return
                sys = json.loads(data)
                self.systemsetting = sys
                self.emit(Event.ON_SYSTEM_SET_UPDATE, sys)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
            
        smartc.on(Event.SYSTEM_SET_UPDATE, systemSetUpHandler)

        # ETF折溢价利润更新
        def etfProfitHandler(data:str):
            try:
                data = json.loads(data)
                etfProfit = ETFProfit()
                etfProfit.instrument_id = data.get("etf")
                etfProfit.iopv = data.get("iopv")
                etfProfit.iopv_buy = data.get("iopvBuy")
                etfProfit.iopv_sale = data.get("iopvSale")
                etfProfit.diopv = data.get("diopv")
                etfProfit.dis_profit = data.get("disProfit")
                etfProfit.pre_profit = data.get("preProfit")
                self.emit(Event.ON_ETF_PROFIT, etfProfit)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
            return 1
        smartc.on(Event.UPDATE_ETF_PROFIT, etfProfitHandler)

        # 缓存同步数据机制
        def cacheHandler(data:str):
            try:
                data = json.loads(data)
                self.cache.__processCMD(data)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on("cacheSet", cacheHandler)
        smartc.on("cacheDel", cacheHandler)
        smartc.on("cachePush", cacheHandler)

        self.strategyManager.initEvent()
        


    '''
     *    全局insert_order 下委托单 account_id选填  strategy_platform_type和strategy_id选填 order_client_id和parent_order_id选填
     *    说明：通过该接口下单，不会记在任何策略上
     *    入参：
     * @param    account_id str 选填 交易账号（资金账号），默认为当前账号id
     * @param    strategy_platform_type StrategyPlatformType枚举 选填 策略平台类型，默认为FrontPy
     * @param    strategy_id str 选填  策略id，可选参数，默认为None，如果传该参数，则下单会影响该策略的资金和持仓，即使策略不启动，只要策略存在，也能下单，是逻辑上的影响策略
     * @param    instrument_id  str 必填 合约ID，如证券代码 "600000"(该参数与code参数必填其一)
     * @param    exchange_id    str 必填 交易所ID 参考Exchange对象 如"SSE"(该参数与code参数必填其一)
     * @param    limit_price    float 必填 价格 如10.32
     * @param    volume int 必填 数量 如100
     * @param    price_type PriceType枚举 选填 报单类型，默认为Limit
     * @param    side   Side枚举  选填 买卖方向，默认为Buy
     * @param    offset Offset枚举    选填 开平方向，默认为Init
     * @param    order_client_id str 选填 客户自定义id，默认为0
     * @param    parent_order_id str 选填 母单编号，默认为"" startStrategy会得到一个母单编号，不传默认使用这个母单编号，如果客户需要自定义的母单编号可以传入
     * @param    business_type str 选填 BusinessType下枚举值，默认为CASH
     * @param    autoSplit boolean 选填 自动拆单，默认为False
     * @param    code str 必填 证券代码.交易所标识,600000.SH,000001.SZ(若该参数与instrument_id、exchange_id同时存在,以该参数为准)
     *   返回：
     *   order_id   long    订单ID
    '''
    def insert_order(self,
                     account_id:str=None,
                     strategy_platform_type:str=None,
                     strategy_id:str=None,
                     instrument_id:str=None,
                     exchange_id:str=Exchange.SSE,
                     limit_price:float=0,
                     volume:int=0,
                     price_type:int=PriceType.Limit,
                     side:int=Side.Buy,
                     offset:int=Offset.Init,
                     order_client_id:int=0,
                     parent_order_id:str="",
                     business_type:int= BusinessType.CASH,
                     callback = None,
                     autoSplit = False,
                     code:str=None):
        strategy_platform_type = StrategyPlatformType.FrontPy
        cb = callback
        try:
            if not account_id:
                account_id = self.current_account.account_id
            if not strategy_id:
                # 资金账号级别的下单
                # todo: 目前smart只支持单账户登录，account_id不论传什么都是当前资金账号，后期扩展到多账号时需要支持
                runtime_id = uuid.uuid1().hex
                if strategy_platform_type and strategy_id:
                    account = self.account_map[account_id]
                    if account:
                        strategy = account.account_map[strategy_platform_type + "" + strategy_id]
                        if strategy:
                            runtime_id = strategy["runtime_id"]
                    # todo: 这里下单都是走的smart server，需要后续补充根据strategy_platform_type为AlphaX，实现到alphax的手工下单和撤单的路由以及spec等其他路由
                        #计算priceType
                if(code):
                    instrument_id, exchange_id = getInstrumentIdAndExchangeIdFromCode(code)

                priceType = ""
                
                if (isinstance(price_type,str)):
                    priceType = getXtpPriceTypeFromPriceTypeWithExchange(PriceType[price_type], Exchange.__dict__[exchange_id])
                else:
                    priceType = getXtpPriceTypeFromPriceTypeWithExchange(price_type, Exchange.__dict__[exchange_id])
                
                #计算side
                _side = ""
                if (isinstance(side,str)):
                    _side = getXtpSideTypeFromSide(Side.__dict__[side])
                else:
                    _side = getXtpSideTypeFromSide(side)

                #计算xtpBusinessType
                if (_side == "XTP_SIDE_REDEMPTION" or _side == "XTP_SIDE_PURCHASE"):
                    business_type = BusinessType.ETF

                xtpBusinessType = ""
                if (isinstance(business_type,str)):
                    xtpBusinessType = getXtpBusinessTypeFromBusinessType(BusinessType.__dict__[business_type])
                else:
                    xtpBusinessType = getXtpBusinessTypeFromBusinessType(business_type)

                # 拆单处理
                volumeList = [volume]
                if autoSplit:
                    volumeList = splitOrder(instrument_id,exchange_id,volume,side,price_type,business_type)
                
                orders = []
                for v in volumeList:
                    rowId = uuid.uuid1().int>>64
                    order = {
                    'ticker': instrument_id,
                    'xtpMarketType': self.dataType['XTP_MARKET_TYPE'][getXtpMarketTypeFromExchange(Exchange.__dict__[exchange_id])]['i'],
                    'xtpPriceType': self.dataType['XTP_PRICE_TYPE'][priceType]['i'],
                    'quantity': v,
                    'price': limit_price,
                    'xtpSideType': self.dataType['XTP_SIDE_TYPE'][_side]['i'],
                    'xtpBusinessType': self.dataType['XTP_BUSINESS_TYPE'][xtpBusinessType]['i'],
                    'offset': self.dataType['XTP_POSITION_EFFECT_TYPE'][getXtpOffsetTypeFromOffset(offset)]['i'],
                    'userName': account_id,
                    'strategyId': strategy_id,
                    'orderClientId': order_client_id,
                    'parentOrderId': parent_order_id,
                    'strategyPlatformType': strategy_platform_type,
                    'autoSplit':autoSplit,
                    'rowId': str(rowId) #客户端生成唯一编号
                    }
                    orders.append(order)
                    if not self.is_back_test :
                        self.bookManager.on_order_input(order)


                def list_callback(rsp):
                    if not cb:return
                    try:
                        orderList = decodeRsp(rsp)
                        if autoSplit:
                            for i in range(len(orderList)):
                                orderList[i] = convertOrderFromSmartToPlugin(orderList[i])
                            cb(orderList,None)
                        else:
                            item = orderList[0]
                            orderInfo = convertOrderFromSmartToPlugin(item)
                            cb(orderInfo,None)
                    except RspError as rspError:
                        logger.error(rspError,exc_info=True, stack_info=True)
                        cb(None,rspError)

                if self.is_back_test :
                    orders[0]["quantity"] = volume #重新赋值原始数量，不用拆单数量
                    bt_core.bt_insert_order(orders[0], list_callback)
                    order_info = bt_core.get_share_order()
                    cb(order_info, None)

                else :
                    smartc.request("insertOrder", json.dumps({"orders":orders}), list_callback)
                
                #######################################################################################################################################
            else:
                # 策略级别的下单  # todo：魏义
                pass
        except Exception as e:
            logger.error(e,exc_info=True, stack_info=True)
            cb and cb(None,RspError({"code":RspError.RUNTIME_ERROR,"message":e}))

    '''
     * 撤单
     * @param order_id
     * @param account_id
    '''
    def cancel_order(self, account_id:str=None, order_id:str=None, cb=None):
        # 资金账号级别的撤单，如果该委托是从策略中下的，策略也会收到
        if not account_id:
            account_id = self.current_account.account_id 
        if not order_id:
            raise Exception("order_id required!")   
        def cancel_callback(data:str):
            try:
                data = json.loads(data)
                if data.get("code")== "0000":
                    data = data["data"]
                cb and cb(data,None)
            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
                cb and cb(None,rspError)
        
        if self.is_back_test :
            bt_core.bt_cancel_order(order_id)
            order_info = bt_core.get_share_order()
            cb(order_info, None)
            return
        
        smartc.request("cancelOrder", json.dumps({
                'orderXtpId': order_id,
                'userName': account_id,
            }),cancel_callback)

    '''
     * 订阅行情
     * @param account_id 选填 账号id，默认为当前账号id  这里区别alphax后台的subscribe函数是后台第一个参数是source
     * @param instruments 必填 订阅的股票列表 数组 如['600000'](该参数与codes参数必填其一)
     * @param exchange_id 必填 交易所id 如Exchange.SSE(该参数与codes参数必填其一)
     * @param is_level2 选填 是否level2，默认为False bool类型 True or False 目前暂不支持level2
     * @param emitter 选填 注册行情派发事件对象,默认为全局smart对象
     * @param callback 选填 订阅后的数据或错误返回信息参数(quoteList,err)
     * @param codes 必填 订阅股票的证券代码.交易所标识列表 数组 如['600000.SH','300001.SZ'](若该参数与instruments、exchange_id同时存在,以该参数为准)
    '''
    def subscribe(self, account_id:str=None, instruments:list[str]=None, exchange_id:str=None, is_level2:bool = False, emitter:Emitter= None, callback=None, codes:list[str]=None):
        
        # for instrument in instruments :
        #     logger.debug("subscribe for instrument : %s", instrument)

        try:
            account_type = None
            if not account_id:
                account_id = self.current_account.account_id
                account_type = self.current_account.account_type
            else:
                account = self.account_map[account_id]
                account_type = account.account_type

            if not emitter:
                emitter = self
            quoteList = []
            instrumentsMap = {}
            rspErrorAll = None
            count = 0
            if(codes):
                for code in codes:
                    instrument_id, exchange_id = getInstrumentIdAndExchangeIdFromCode(code)
                    instruments = instrumentsMap.get(exchange_id)
                    if not instruments:
                        instruments = []
                        instrumentsMap[exchange_id] = instruments
                    instruments.append(instrument_id)
            else:
                instrumentsMap[exchange_id] = instruments
            # logger.debug("subscribe map:%s",instrumentsMap)
            # 订阅行情管理器处理订阅关系
            for exchange_id, instruments in instrumentsMap.items():
                instrumentList = []
                for instrument in instruments:
                    subList = None
                    key = instrument + "_" + exchange_id
                    if key in self.__subMap:
                        subList = self.__subMap[key]
                    subObj = None
                    if not subList:
                        subList = []
                        self.__subMap[key] = subList
                    else:
                        for it in subList:
                            if it['emitter'] is emitter:
                                subObj = it
                                break
                        
                    # 之前未订阅过, 加入订阅列表
                    if len(subList) <= 0:
                        instrumentList.append(instrument)

                    if not subObj:
                        subObj = {
                            "emitter": emitter,
                            "times": 0
                        }
                        subList.append(subObj)
                    else:  # 行情已经存在，直接内存派发
                        cacheQuote = self.__quoteMap.get(key)
                        if cacheQuote:
                            emitter.emit(Event.ON_QUOTE, cacheQuote)
                            quoteList.append(cacheQuote)
                        
                    subObj['times'] = subObj['times'] + 1
                    
                if len(instrumentList)> 0:
                    count += 1
                    # logger.debug("subscribe send list:%s",instrumentList)
                    def subscribeCallback(rsp:str):
                        nonlocal count
                        count -= 1
                        try:
                            tempList = decodeRsp(rsp)
                            for quoteObj in tempList:
                                quoteList.append(convertQuoteFromSmartToPlugin(quoteObj))
                            
                        except RspError as rspError:
                            nonlocal rspErrorAll
                            rspErrorAll = rspError
                            logger.error(rspError,exc_info=True, stack_info=True)

                        if count <= 0:
                            # logger.debug("subscribe has quotes:%d",len(quoteList))
                            callback and callback(quoteList,rspErrorAll)
                    if self.is_back_test :
                        # WT 的订阅接口返回的数据为 {"command":7,"datatype":1,"data":{"code":0,"msg":"success"}}, 没有行情信息，所以这里调用回调函数没有意义
                        # 立即回调空数组
                        # TODO 增加检查是否有数据的判断，并更改smartc里for循环的执行流程，等待前端发回的nng消息。
                        bt_core.checkBTData(instrumentList, exchange_id,"ticks")
                        bt_core.bt_subscribe_tick(instrumentList, exchange_id, None)
                        callback and callback(quoteList,rspErrorAll)
                    else :
                        smartc.request("subscribe", json.dumps({
                            'userName': account_id,
                            'accountType': account_type,
                            'tickers': instrumentList,
                            'exchangeId': exchange_id,
                            'is_level2': is_level2
                        }),subscribeCallback)
                    
            if count <= 0:
                callback and callback(quoteList,None)
        except Exception as e:
            logger.error(e,exc_info=True, stack_info=True)
            callback and callback(None, e)

    '''
     * 取消订阅
     * @param account_id 选填 账号id，默认为当前账号id  这里区别alphax后台的unsubscribe函数是后台第一个参数是source
     * @param instruments 必填 订阅的股票列表 数组 如['600000'](该参数与codes参数必填其一)
     * @param exchange_id 必填 交易所id 如Exchange.SSE(该参数与codes参数必填其一)
     * @param is_level2 选填 是否level2，默认为False bool类型 True or False 目前暂不支持level2
     * @param emitter 选填 注册行情派发事件对象,默认为全局smart对象
     * @param codes 必填 订阅股票的证券代码.交易所标识列表 数组 如['600000.SH','300001.SZ'](若该参数与instruments、exchange_id同时存在,以该参数为准)
    '''
    def unsubscribe(self, account_id:str=None, instruments:list[str]=None, exchange_id:str=None, is_level2:bool = False, emitter:Emitter = None, codes:list[str]=None):
        try:
            if not emitter:
                emitter = self
            instrumentsMap = {}
            if(codes):
                for code in codes:
                    instrument_id, exchange_id = getInstrumentIdAndExchangeIdFromCode(code)
                    instruments = instrumentsMap.get(exchange_id)
                    if not instruments:
                        instruments = []
                        instrumentsMap[exchange_id] = instruments
                    instruments.append(instrument_id)
            else:
                instrumentsMap[exchange_id] = instruments
            # 订阅管理器处理订阅关系
            for exchange_id, instruments in instrumentsMap.items():
                unsubList = []
                for instrument in instruments:
                    subList = None
                    key = instrument + "_" + exchange_id
                    if key in self.__subMap:
                        subList = self.__subMap[key]
                        for subObj in subList:
                            if subObj['emitter'] is emitter:
                                subObj['times'] = subObj['times'] - 1
                                if (subObj['times'] <= 0):
                                    subList.remove(subObj)
                                    if (len(subList) <= 0):
                                        unsubList.append(instrument)
                                        self.__subMap.pop(key,"")
                                        self.__quoteMap.pop(key,"")
                                break
                
                if(len(unsubList)>0):
                    if self.is_back_test :
                        bt_core.bt_unsubscribe_tick(unsubList, exchange_id)
                        return

                    smartc.request("unsubscribe", json.dumps({
                        'userName': account_id,
                        'tickers': unsubList,
                        'exchangeId': exchange_id,
                        'is_level2': is_level2
                    }),None)
        except Exception as e:
            logger.error(e,exc_info=True, stack_info=True)
    
    '''
     * 订阅指数行情
     * @param account_id 选填 账号id，默认为当前账号id
     * @param instruments 必填 订阅的指数列表 数组 如["000001", "CESCPD", "931646"]
     * @param is_level2 选填 是否level2，默认为False bool类型 True or False 目前暂不支持level2
     * @param emitter 选填 注册行情派发事件对象,默认为全局smart对象
     * @param callback 选填 订阅后的数据或错误返回信息参数(quoteList,err)
    '''
    def subscribe_index(self, account_id:str=None, instruments:list[str]=None, is_level2:bool = False, emitter:Emitter= None, callback=None):
        try:
            codes = []
            for instrument_id in instruments:
                if instrument_id not in self.index_map:
                    continue
                exchange_id = self.index_map[instrument_id].exchange_id
                exchange_str = getExchangeStrFromExchangeId(exchange_id)
                code = instrument_id + "." + exchange_str
                codes.append(code)
            self.subscribe(account_id=account_id, is_level2=is_level2, emitter=emitter, codes=codes, callback=callback)
        except Exception as e:
            logger.error(e,exc_info=True, stack_info=True)
            callback and callback(None, e)

    '''
     * 取消订阅指数行情
     * @param account_id 选填 账号id，默认为当前账号id
     * @param instruments 必填 订阅的指数列表 数组 如["000001", "CESCPD", "931646"]
     * @param is_level2 选填 是否level2，默认为False bool类型 True or False 目前暂不支持level2
     * @param emitter 选填 注册行情派发事件对象,默认为全局smart对象
    '''
    def unsubscribe_index(self, account_id:str=None, instruments:list[str]=None, is_level2:bool = False, emitter:Emitter = None):
        try:
            codes = []
            for instrument_id in instruments:
                if instrument_id not in self.index_map:
                    continue
                exchange_id = self.index_map[instrument_id].exchange_id
                exchange_str = getExchangeStrFromExchangeId(exchange_id)
                code = instrument_id + "." + exchange_str
                codes.append(code)
            self.unsubscribe(account_id=account_id, is_level2=is_level2, emitter=emitter, codes=codes)
        except Exception as e:
            logger.error(e,exc_info=True, stack_info=True)

    '''
     * 订阅通用指标
     * @param type 必填 指标参数，例如'etf'等字符串，该参数识别大小写
     * @param codes 选填 订阅的股票列表 数组 如['600000.SH','000001.SZ']
     * @param on_indicator_callback 选填 接收行情推送的回调函数，支持三种定义，且优先级为：on_indicator > smart.on()> 默认
     * @param emitter 选填 注册数据派发事件对象, 默认为全局smart对象
    '''
    def subscribe_indicator(self, type: str = None, codes: list[str] = None, on_indicator_callback=None, emitter: Emitter = None):
        try:
            if not emitter:
                emitter = self
            # quoteList = [] #行情数组

            if not type:
                msg = f"订阅的指标类型参数type必填，不允许为空"
                params = {
                    "level": "error",
                    "title": "订阅的指标参数错误",
                    "msg": msg,
                }
                smart.notice(params)
                raise Exception(msg)
            if type.find("bar") > -1:
                msg = f"不支持bar行情订阅"
                params = {
                    "level": "error",
                    "title": "订阅的指标参数错误",
                    "msg": msg,
                }
                smart.notice(params)
                raise Exception(msg)

            logger.debug("subscribe_%s codes:%s", type, codes)
            # 订阅行情管理器处理订阅关系
            instrumentCodeList = [] # 新订阅行情的股票数组
            for code in codes:
                code = code.upper() #默认转大写
                getInstrumentIdAndExchangeIdFromCode(code)
                # instrument_id, exchange_id = getInstrumentIdAndExchangeIdFromCode(code) # 校验股票列表 数组格式 如['600000.SH','000001.SZ']
                # if ( not isStock(instrument_id, exchange_id)) :
                #     msg = f"证券{instrument_id}非股票，只能订阅股票的行情"
                #     params = {
                #         "level": "error",
                #         "title": "订阅证券的类型错误",
                #         "msg": msg,
                #     }
                #     smart.notice(params)
                #     raise Exception(msg)
                subList = None
                key = type + '_' + code
                if key in self.__subIndicatorMap:
                    subList = self.__subIndicatorMap[key]
                subObj = None
                if not subList:
                    subList = []  # 数组第一位为总计数
                    self.__subIndicatorMap[key] = subList
                else:
                    for it in subList:
                        if it['emitter'] is emitter:
                            subObj = it
                            break

                # 之前未订阅过, 加入订阅列表
                if len(subList) <= 0:
                    instrumentCodeList.append(code)

                if not subObj:
                    subObj = {
                        "emitter": emitter,
                        "times": 0
                    }
                    subList.append(subObj)
                else:  # 行情已经存在，直接内存派发
                    cacheQuote = self.__quoteIndicatorMap.get(key)
                    if cacheQuote:
                        emitter.emit(Event.ON_INDICATOR, type, cacheQuote)
                        # quoteList.append(cacheQuote)
                subObj['times'] = subObj['times'] + 1

            if len(instrumentCodeList) > 0:
                logger.debug("subscribe_%s send list:%s", type, instrumentCodeList)
                # def subscribeCallback(rsp: str):
                #     try:
                #         tempList = decodeRsp(rsp)
                #         # for quoteObj in tempList:
                #             # quoteList.append(quoteObj)
                #         subscribe_callback and subscribe_callback(tempList, None)     
                #     except RspError as rspError:
                #         for code in instrumentCodeList:
                #             key =  type+ code
                #             self.__subIndicatorMap.pop(key, "")
                #         logger.error(rspError, exc_info=True, stack_info=True)
                #         subscribe_callback and subscribe_callback(None, rspError)
                failed = smartc.request_reply("subscribe_indicator", 
                                        json.dumps({
                                            'type': type,
                                            'codes':instrumentCodeList,
                                        })
                                    )
                if failed:
                    failed = json.loads(failed)
                    if not isinstance(failed, list):
                        failed = None
                    else:
                        for code in failed:
                            code = code.upper() #默认转大写
                            subList = None
                            key = type + '_' + code
                            if key in self.__subIndicatorMap:
                                subList = self.__subIndicatorMap[key]
                                for subObj in subList:
                                    if subObj['emitter'] is emitter:
                                        subObj['times'] = subObj['times'] - 1
                                        if (subObj['times'] <= 0):
                                            subList.remove(subObj)
                                            if (len(subList) <= 0):
                                                self.__subIndicatorMap.pop(key, "")
                                                self.__quoteIndicatorMap.pop(key, "")
                                        break
                addListener(smart.Event.ON_INDICATOR, on_indicator_callback)
                return failed
            else:
                # logger.debug("subscribe has quotes:%d",len(quoteList))
                # subscribe_callback and subscribe_callback(None, None)
                addListener(smart.Event.ON_INDICATOR, on_indicator_callback)
                return None
        except Exception as e:
            logger.error(e,exc_info=True, stack_info=True)
            return None
            # subscribe_callback and subscribe_callback(None, e)


    '''
     * 订阅指标bar行情
     * 当全部是首次订阅或是已订阅无行情时，返回空数组；若存在已订阅的股票且有最新行情，则返回订阅股票的最新行情数组。
     * 订阅失败时抛出异常信息
     * @param codes 必填 订阅的股票列表 数组 如['600000.SH','000001.SZ']
     * @param period 选填 周期 默认1m，最大60m（m代表分钟）
     * @param on_bar_callback 选填 接收行情推送的回调函数，支持三种定义，且优先级为：on_bar > smart.on()> 默认
     * @param emitter 选填 注册行情派发事件对象, 默认为全局smart对象
    '''
    def subscribe_bar(self, codes: list[str] = None, period: str = "1m", on_bar_callback=None, emitter: Emitter = None):
        try:
            if not emitter:
                emitter = self
            # quoteList = [] #行情数组
            if not codes:
                msg = f"订阅的股票列表codes必填，不允许为空"
                params = {
                    "level": "error",
                    "title": "订阅证券的股票列表错误",
                    "msg": msg,
                }
                smart.notice(params)
                raise Exception(msg)

            logger.debug("subscribe_bar codes:%s period:%s", codes, period)
            if not isFormatPeriod(period,"m"):
                msg = f"bar行情订阅的周期格式错误，例如1m"
                params = {
                    "level": "error",
                    "title": "订阅周期错误",
                    "msg": msg,
                }
                smart.notice(params)
                raise Exception(msg)

            # time_interval = int(period.split("m")[0])
            # 订阅行情管理器处理订阅关系
            instrumentCodeList = [] # 新订阅行情的股票数组
            for code in codes:
                code = code.upper() #默认转大写
                getInstrumentIdAndExchangeIdFromCode(code) # 校验股票列表 数组格式 如['600000.SH','000001.SZ']
                # if ( not isStock(instrument_id, exchange_id)) :
                #     msg = f"证券{instrument_id}非股票，只能订阅股票的行情"
                #     params = {
                #         "level": "error",
                #         "title": "订阅证券的类型错误",
                #         "msg": msg,
                #     }
                #     smart.notice(params)
                #     raise Exception(msg)
                # if (time_interval > 60):
                #     msg = f"bar行情订阅的时间间隔不能大于60"
                #     params = {
                #         "level": "error",
                #         "title": "时间间隔错误",
                #         "msg": msg,
                #     }
                #     smart.notice(params)
                #     raise Exception(msg)
                subList = None
                key = 'bar_' + period +"_"+ code
                if key in self.__subIndicatorMap:
                    subList = self.__subIndicatorMap[key]
                subObj = None
                if not subList:
                    subList = []  # 数组第一位为总计数
                    self.__subIndicatorMap[key] = subList
                else:
                    for it in subList:
                        if it['emitter'] is emitter:
                            subObj = it
                            break

                # 之前未订阅过, 加入订阅列表
                if len(subList) <= 0:
                    instrumentCodeList.append(code)

                if not subObj:
                    subObj = {
                        "emitter": emitter,
                        "times": 0
                    }
                    subList.append(subObj)
                else:  # 行情已经存在，直接内存派发
                    cacheQuote = self.__quoteIndicatorMap.get(key)
                    if cacheQuote:
                        emitter.emit(Event.ON_BAR, cacheQuote)
                        # quoteList.append(cacheQuote)
                subObj['times'] = subObj['times'] + 1

            if len(instrumentCodeList) > 0:
                logger.debug("subscribe_bar send list:%s", instrumentCodeList)
                # def subscribeCallback(rsp: str):
                #     try:
                #         tempList = decodeRsp(rsp)
                #         # for quoteObj in tempList:
                #             # quoteList.append(convertQuoteIndicatorFromSmartToPlugin(subscribe_type + '_' + str(param.time_interval) + 'm',quoteObj))
                #         subscribe_callback and subscribe_callback(tempList, None)
                #     except RspError as rspError:
                #         for code in instrumentCodeList:
                #             key = subscribe_type + '_' + str(param.time_interval) + 'min_' + code
                #             self.__subIndicatorMap.pop(key, "")
                #         logger.error(rspError, exc_info=True, stack_info=True)
                #         subscribe_callback and subscribe_callback(None, rspError)

                failed = None

                if self.is_back_test :
                    bt_core.checkBTData(instrumentCodeList, None, period)
                    bt_core.bt_subscribe_bar(instrumentCodeList, period)
                else :
                    failed = smartc.request_reply("subscribe_bar", json.dumps({
                        'codes':instrumentCodeList,
                        'period':period
                    }))
                    
                if failed:
                    failed = json.loads(failed)
                    if not isinstance(failed, list):
                        failed = None
                    else:
                        for code in failed:
                            code = code.upper() #默认转大写
                            subList = None
                            key = 'bar_' + period +"_"+ code
                            if key in self.__subIndicatorMap:
                                subList = self.__subIndicatorMap[key]
                                for subObj in subList:
                                    if subObj['emitter'] is emitter:
                                        subObj['times'] = subObj['times'] - 1
                                        if (subObj['times'] <= 0):
                                            subList.remove(subObj)
                                            if (len(subList) <= 0):
                                                self.__subIndicatorMap.pop(key, "")
                                                self.__quoteIndicatorMap.pop(key, "")
                                        break
                addListener(smart.Event.ON_BAR, on_bar_callback)
                return failed
            else:
                # logger.debug("subscribe has quotes:%d",len(quoteList))
                # subscribe_callback and subscribe_callback(None, None)
                addListener(smart.Event.ON_BAR, on_bar_callback)
                return None
        except Exception as e:
            logger.error(e,exc_info=True, stack_info=True)
            # subscribe_callback and subscribe_callback(None, e)
            return None
    
    '''
     * 取消订阅通用指标
     * @param type 必填 指标类型参数，例如'etf'等字符串，该参数识别大小写
     * @param codes 选填 订阅的股票列表 数组 如['600000.SH','000001.SZ']
     * @param emitter 选填 注册数据派发事件对象, 默认为全局smart对象
    '''
    def unsubscribe_indicator(self, type: str = None, codes: list[str] = None, emitter: Emitter = None):
        if not emitter:
            emitter = self
        if not type:
                msg = f"取消订阅的指标类型参数type必填，不允许为空"
                params = {
                    "level": "error",
                    "title": "订阅的指标参数错误",
                    "msg": msg,
                }
                smart.notice(params)
                raise Exception(msg)
        if type.find("bar") > -1:
            msg = f"不支持bar行情订阅"
            params = {
                "level": "error",
                "title": "取消订阅的指标参数错误",
                "msg": msg,
            }
            smart.notice(params)
            raise Exception(msg)
        if type.find("_") > -1:
            msg = f"指标类型参数不能含特殊字符_"
            params = {
                "level": "error",
                "title": "取消订阅的指标参数错误",
                "msg": msg,
            }
            smart.notice(params)
            raise Exception(msg)

        unsubList = []
        for code in codes:
            getInstrumentIdAndExchangeIdFromCode(code) # 校验股票列表 数组格式 如['600000.SH','000001.SZ']
    
        # 订阅管理器处理订阅关系
        for code in codes:
            code = code.upper() #默认转大写
            subList = None
            key = type + '_' + code
            if key in self.__subIndicatorMap:
                subList = self.__subIndicatorMap[key]
                for subObj in subList:
                    if subObj['emitter'] is emitter:
                        subObj['times'] = subObj['times'] - 1
                        if (subObj['times'] <= 0):
                            subList.remove(subObj)
                            if (len(subList) <= 0):
                                unsubList.append(code)
                                self.__subIndicatorMap.pop(key, "")
                                self.__quoteIndicatorMap.pop(key, "")
                        break

        if (len(unsubList) > 0):
            failed = smartc.request_reply("unsubscribe_indicator", json.dumps({
                'type': type,
                'codes':unsubList,
            }))
            if failed:
                    failed = json.loads(failed)
                    if not isinstance(failed, list):
                        failed = None
            return failed
        else:
            return None

    '''
     * 取消订阅指标行情（bar、macd行情）
     * @param codes 必填 订阅的股票列表 数组 如['600000.SH','000001.SZ']
     * @param period 选填 周期 默认1m，最大60m（m代表分钟）
     * @param emitter 选填 注册行情派发事件对象, 默认为全局smart对象
    '''
    def unsubscribe_bar(self, codes: list[str] = None, period: str = "1m", emitter: Emitter = None):
        if not emitter:
            emitter = self
        if not codes:
                msg = f"取消订阅的股票列表codes必填，不允许为空"
                params = {
                    "level": "error",
                    "title": "取消订阅证券的股票列表错误",
                    "msg": msg,
                }
                smart.notice(params)
                raise Exception(msg)

        unsubList = []
        for code in codes:
            getInstrumentIdAndExchangeIdFromCode(code) # 校验股票列表 数组格式 如['600000.SH','000001.SZ']
    
        # 订阅管理器处理订阅关系
        for code in codes:
            code = code.upper() #默认转大写
            subList = None
            key = 'bar_' + period + '_' + code
            if key in self.__subIndicatorMap:
                subList = self.__subIndicatorMap[key]
                for subObj in subList:
                    if subObj['emitter'] is emitter:
                        subObj['times'] = subObj['times'] - 1
                        if (subObj['times'] <= 0):
                            subList.remove(subObj)
                            if (len(subList) <= 0):
                                unsubList.append(code)
                                self.__subIndicatorMap.pop(key, "")
                                self.__quoteIndicatorMap.pop(key, "")
                        break

        if (len(unsubList) > 0):
            if self.is_back_test :
                bt_core.bt_unsubscribe_bar(codes, period)
                return
            failed = smartc.request_reply("unsubscribe_bar", json.dumps({
                'codes':unsubList,
                'period':period,
            }))
            if failed:
                    failed = json.loads(failed)
                    if not isinstance(failed, list):
                        failed = None
            return failed
        else:
            return None

    '''/**
    * 根据证券代码和交易所查找一个instrument
    * @param instrumentId 必填 证券代码(该参数与code参数必填其一)
    * @param exchangeId 必填 交易所 如'SSE'(该参数与code参数必填其一)
    * @param code 必填 证券代码.交易所标识,600000.SH,000001.SZ(若该参数与instrument_id、exchange_id同时存在,以该参数为准)
    */'''
    def getInstrument(self, instrumentId:str=None, exchangeId:str=None, code:str=None)->Instrument:
        try:
            if (code):
                instrumentId, exchangeId = getInstrumentIdAndExchangeIdFromCode(code)
            instrument_name = instrumentId + "_" + exchangeId
            return self.instrument_map.get(instrument_name,None)
        except Exception as e:
            logger.error(e,exc_info=True, stack_info=True)
            return None

    '''/**
    * 获取可交易的ETF列表
    * @param cb:function return list[ETF]
    */'''
    def getETFList(self,cb=None):
        if not cb:
            raise Exception("cb required!")
        if (len(self.etf_map) <= 0):
            def getETFListBT(cb=None):
                try:
                    if(len(self.current_date)!=8):
                        raise Exception("current_date len error!"+self.current_date)
                    dateStr = datetime.strptime(self.current_date, '%Y%m%d').strftime('%Y-%m-%d')
                    inParams = { "date": dateStr }
                    #logger.info("inParams:%s",json.dumps(inParams))
                    rsp = smartc.request_reply("getETFList",json.dumps(inParams))
                    etfList = decodeRsp(rsp)
                    for etfItem in etfList :
                        key = etfItem["etf"] + "_" + etfItem["exchange_id"]
                        instrument = self.instrument_map.get(key,{})
                        etfObj = ETF()
                        utils.assign(etfObj, instrument)
                        etfObj.cash_component = etfItem["cash_component"]
                        etfObj.estimate_amount = etfItem["estimate_amount"]
                        etfObj.max_cash_ratio = etfItem["max_cash_ratio"]
                        etfObj.net_value = etfItem["net_value"]
                        etfObj.redemption_status = etfItem["redemption_status"]
                        etfObj.total_amount = etfItem["total_amount"]
                        etfObj.unit = etfItem["unit"]
                        #候补属性
                        etfObj.instrument_id = etfItem["etf"]
                        etfObj.instrument_name = etfItem["etf_name"] or "" #证券名称
                        etfObj.xtp_market_type = getXtpMarketTypeFromExchange(etfItem["exchange_id"])
                        etfObj.code = etfObj.instrument_id + "." + getExchangeStrFromExchangeId(etfItem["exchange_id"])
                        self.etf_map[etfObj.instrument_id] = etfObj
                    cb(list(self.etf_map.values()),None)
                except RspError as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)
                    
            def getETFListCB(rsp:str):
                try:
                    etfList = decodeRsp(rsp)
                    for etfItem in etfList :
                        key = etfItem["etf"] + "_" + convertExchangeIdFromxtpMarketType(etfItem["marketType"])
                        instrument = self.instrument_map.get(key,{})
                        etfObj = ETF()
                        utils.assign(etfObj, instrument)
                        etfObj.cash_component = etfItem["cashComponent"]
                        etfObj.estimate_amount = etfItem["estimateAmount"]
                        etfObj.max_cash_ratio = etfItem["maxCashRatio"]
                        etfObj.net_value = etfItem["netValue"]
                        etfObj.redemption_status = etfItem["redemptionStatus"]
                        etfObj.total_amount = etfItem["totalAmount"]
                        etfObj.unit = etfItem["unit"]
                        #候补属性
                        etfObj.instrument_id = etfItem["etf"]
                        etfObj.instrument_name = etfItem["etfName"] or "" #证券名称
                        etfObj.xtp_market_type = etfItem["marketType"]
                        etfObj.code = etfObj.instrument_id + "." + getExchangeStrFromExchangeId(convertExchangeIdFromxtpMarketType(etfObj.xtp_market_type))
                        self.etf_map[etfObj.instrument_id] = etfObj
                    cb(list(self.etf_map.values()),None)
                except RspError as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)    
            if self.is_back_test :
                getETFListBT(cb)
            else:
                smartc.request("getETFList","{}",getETFListCB)
                pass
        else:
            cb(list(self.etf_map.values()),None)
    '''/**
    * 获取可转债正股信息
    * @param code 可转债code
    * @param cb:function return ConvertableBond
    */'''
    def getConvertableBond(self, code:str=None, cb=None)->ConvertableBond:
        if not code:
            raise Exception("code required!")
        if not cb:
            raise Exception("cb required!")
        instrument_id, exchange_id = getInstrumentIdAndExchangeIdFromCode(code)
        marketType = getXtpMarketTypeFromExchange(exchange_id)
        params = { "ticker": instrument_id, "marketType": marketType }
        def getConvertableBondCB(rsp:str):
            try:
                tempBond = decodeRsp(rsp)
                exchangeId = convertExchangeIdFromxtpMarketType(tempBond.get("marketType"))
                key = tempBond.get("ticker") + "_" + exchangeId
                instrument = self.instrument_map.get(key)
                convertableBond = ConvertableBond()
                utils.assign(convertableBond, instrument)
                convertableBond.qtyMax = tempBond.get("qtyMax")
                convertableBond.qtyMin = tempBond.get("qtyMin")
                convertableBond.swapFlag = tempBond.get("swapFlag")
                convertableBond.swapPrice = tempBond.get("swapPrice")
                convertableBond.underlyingTicker = tempBond.get("underlyingTicker")
                convertableBond.unit = tempBond.get("unit")
                cb(convertableBond, None)
            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
                cb(None,rspError)
        smartc.request("getConvertableBond",json.dumps(params),getConvertableBondCB)




    '''/**
    * 获取ETF成分股列表
    * @param instrument_id ETF代码
    * @param cb:function return list[ETFCompoment]
    */'''
    def getETFBasket(self,instrument_id:str=None, cb=None):
        if not instrument_id:
            raise Exception("instrument_id required!")
        if not cb:
            raise Exception("cb required!")
        etfObj = self.etf_map.get(instrument_id)
        if (etfObj and len(etfObj.basket) > 0) :
            return cb(list(etfObj.basket),None)
        else:
            marketType = None
            if (etfObj):
                marketType = etfObj.xtp_market_type
            else:
                #按照ETF，15或者51开头决定市场类型
                marketType =  "XTP_MKT_SZ_A"  if instrument_id.startswith("15") else "XTP_MKT_SH_A"
                
                '''/**
            * 回测模式下获取ETF成分股列表
            * @param instrument_id ETF代码
            * @param cb:function return list[ETFCompoment]
            */'''
            def getETFBasketBT(instrument_id:str=None, cb=None):
                
                if "XTP_MKT_SZ_A" == marketType:
                    code = instrument_id+".SZ"
                else:
                    code = instrument_id+".SH"
                
                try:
                    if(len(self.current_date)!=8):
                        raise Exception("current_date len error!"+self.current_date)
                    dateStr = datetime.strptime(self.current_date, '%Y%m%d').strftime('%Y-%m-%d')
                    inParams = { "date": dateStr, "code": code }
                    #logger.info("getETFBasket inParams: %s",json.dumps(inParams))
                    rsp = smartc.request_reply("getETFBasket",json.dumps(inParams))
                    tempBasket = decodeRsp(rsp)
                    basket = []
                    for basketItem in tempBasket:
                        exchangeId = basketItem.get("exchange_id")
                        key = basketItem.get("ticker") + "_" + exchangeId
                        instrument = self.instrument_map.get(key)
                        etfComp = ETFCompoment()
                        if instrument:
                            utils.assign(etfComp, instrument)
                        etfComp.amount = basketItem.get("amount")
                        etfComp.creation_amount = basketItem.get("creation_amount")
                        etfComp.creation_premium_ratio = basketItem.get("creation_premium_ratio")
                        etfComp.premium_ratio = basketItem.get("premium_ratio")
                        etfComp.quantity = basketItem.get("quantity")
                        etfComp.redemption_amount = basketItem.get("redemption_amount")
                        etfComp.redemption_discount_ratio = basketItem.get("redemption_discount_ratio")
                        etfComp.replace_type = basketItem.get("replace_type")
                        etfComp.ticker = basketItem.get("ticker")
                        etfComp.instrument_id = basketItem.get("instrument_id")
                        etfComp.instrument_name = basketItem.get("instrument_name")
                        etfComp.xtp_market_type = basketItem.get("instrument_market_type")
                        basket.append(etfComp)
                    if (etfObj) :
                        etfObj.basket = basket
                        cb(list(etfObj.basket),None)
                        
                except Exception as rspError:
                    raise rspError

            def getETFBasketCB(rsp:str):
                try:
                    tempBasket = decodeRsp(rsp)
                    basket = []
                    for basketItem in tempBasket:
                        exchangeId = convertExchangeIdFromxtpMarketType(basketItem.get("componentMarketType"))
                        key = basketItem.get("componentTicker") + "_" + exchangeId
                        instrument = self.instrument_map.get(key)
                        etfComp = ETFCompoment()
                        if instrument:
                            utils.assign(etfComp, instrument)
                        etfComp.amount = basketItem.get("amount")
                        etfComp.creation_amount = basketItem.get("creationAmount")
                        etfComp.creation_premium_ratio = basketItem.get("creationPremiumRatio")
                        etfComp.premium_ratio = basketItem.get("premiumRatio")
                        etfComp.quantity = basketItem.get("quantity")
                        etfComp.redemption_amount = basketItem.get("redemptionAmount")
                        etfComp.redemption_discount_ratio = basketItem.get("redemptionDiscountRatio")
                        etfComp.replace_type = basketItem.get("replaceType")
                        etfComp.ticker = basketItem.get("ticker")
                        etfComp.creation_amount = basketItem.get("creationAmount")
                        etfComp.redemption_amount = basketItem.get("redemptionAmount")
                        etfComp.instrument_id = basketItem.get("componentTicker")
                        etfComp.instrument_name = basketItem.get("componentName")
                        etfComp.xtp_market_type = basketItem.get("componentMarketType")
                        basket.append(etfComp)
                    if (etfObj) :
                        etfObj.basket = basket
                    cb(list(basket),None)
                except RspError as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError) 
            if self.is_back_test :
                getETFBasketBT(instrument_id,cb)
            else:
                params = { "ticker": instrument_id, "marketType": marketType }
                smartc.request("getETFBasket",json.dumps(params),getETFBasketCB)


    
    '''/**
    * 取得IPO列表
    * @param cb:function return list[IPO]
    */'''
    def getIPOList(self,cb=None):
        if not cb:
            raise Exception("cb required!")
        ipolist = self.ipo_map.values()
        if (len(ipolist) > 0) :
            cb(list(ipolist),None)
            return
        def getIPOInfoCB(rsp:str):
            try:
                ipolist = decodeRsp(rsp)
                for ipoItem in ipolist:
                    ipoObj = IPO()
                    instrumentType = convertInstrumentTypeFromXtpSecurityType(ipoItem.get("tickerType","XTP_TICKER_TYPE_UNKNOWN"))
                    ipoObj.xtp_market_type = ipoItem.get("marketType")
                    ipoObj.price = ipoItem.get("price") # 价格
                    ipoObj.qty_upper_limit = ipoItem.get("qtyUpperLimit") # 持仓数量
                    ipoObj.instrument_id = ipoItem.get("ticker") # 股票代码
                    ipoObj.instrument_name = ipoItem.get("tickerName") # 股票名称
                    ipoObj.instrument_type = instrumentType # 证券类型 InstrumentType枚举值  对应smart的securityType
                    ipoObj.instrument_type_ext = ipoItem.get("tickerType") # 用于标识具体的证券类型
                    ipoObj.unit = ipoItem.get("unit") # 最小申购赎回单位
                    ipoObj.exchange_id = convertExchangeIdFromxtpMarketType(ipoObj.xtp_market_type) # 交易所ID
                    ipoObj.exchange_id_name = dataTypeToName(ipoObj.exchange_id, "ALPHAX_EXCHANGE_TYPE") # 交易所名称
                    ipoObj.code = ipoObj.instrument_id + "." + getExchangeStrFromExchangeId(ipoObj.exchange_id) # code
                    self.ipo_map[ipoObj.instrument_id] = ipoObj
                ipolist = self.ipo_map.values()
                cb(list(ipolist),None)
            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
                cb(None,rspError)

        smartc.request("getIPOInfo","{}",getIPOInfoCB)

    '''/**
    * 获取国债逆回购列表
    * @param cb:function return list[IPO]
    */'''
    def getBondReverseRepoList(self,cb=None):
        if not cb:
            raise Exception("cb required!")
        def initReverseRepoList():
            cb(smart.reverse_repo_list,None)
        
        if len(smart.reverse_repo_list) > 0:
            cb(smart.reverse_repo_list,None)
        else:
            smart.on("_INIT_ALL_TICKERS_DONE", initReverseRepoList)           
    
    '''/**
    * 订阅ETF折溢价预期利润
    * @param cb:function return list[ETFProfit]
    */'''
    def subscribeETFProfit(self,cb=None):
        if not cb:
            raise Exception("cb required!")
        if (self._etfProfitSubCount <= 0) :
            def subscribeETFProfitCB(rsp:str):
                try:
                    profitList = decodeRsp(rsp)
                    for profit in profitList :
                        etf = profit.get("etf")
                        etfProfit = ETFProfit()
                        etfProfit.instrument_id = profit.get("etf")
                        etfProfit.dis_profit = profit.get("disProfit")
                        etfProfit.pre_profit = profit.get("preProfit")
                        etfProfit.iopv = profit.get("iopv")
                        etfProfit.iopv_sale = profit.get("iopvSale")
                        etfProfit.iopv_buy = profit.get("iopvBuy")
                        etfProfit.diopv = profit.get("diopv")
                        self.etf_profit_map[etf] = etfProfit
                    results = list(self.etf_profit_map.values())
                    cb(results,None)
                    for subCB in self._etfProfitSubCBList :
                        subCB(results,None)
                    self._etfProfitSubCBList = []
                except RspError as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)
                    for subCB in self._etfProfitSubCBList :
                        subCB(None,rspError)
                    self._etfProfitSubCBList = []
            smartc.request("subscribeETFProfit","{}",subscribeETFProfitCB)
        else:
            subCacheList = list(self.etf_profit_map.values())
            if(len(subCacheList)>0):
                cb(subCacheList,None)
            else:
                self._etfProfitSubCBList.append(cb)
        self._etfProfitSubCount += 1

    '''/**
    * 取消订阅ETF折溢价预期利润
    */'''
    def unsubscribeETFProfit(self):
        self._etfProfitSubCount-=1
        if (self._etfProfitSubCount <= 0) :
            smartc.request("unsubscribeETFProfit","{}",None)
            self.etf_profit_map = {}

    
    ''' 读取设置中的设置项 '''
    def getSystemSet(self,cb=None):
        if not cb:
            raise Exception("cb required!")
        #// 读取用户信息
        def systCallback(rsp:str):
            try:
                data = decodeRsp(rsp)
                cb(data,None)
            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
                cb(None,rspError)
        smartc.request("getSystemSet","{}", systCallback)

    '''/**
    * 全局消息通知弹窗（目前专供给股票价格异动提醒功能）
    * @param {*} type 提醒级别
    * @param {*} title 提醒主题
    * @param {*} msg 提醒信息
    * @param {*} msgType 消息类型
    * @param {*} boxPosition 消息位置rightTop右上，rightBottom右下，leftTop左上,leftBottom左下
    * @param {*} autoClose 弹框是否自动关闭
    * @param {*} duration 弹框关闭时间  毫秒
    */'''
    def msgRemind(self,kwargs:dict):
        smartc.request("getMsgRemind", json.dumps(kwargs), None)

    '''/**
    * 全局消息弹窗
    * @param {*} level 消息状态
    * @param {*} title 头部标题
    * @param {*} msg 需要推送的消息内容
    * @param duration 消息显示时间
    * @param timestamp 时间戳
    * */'''
    def notice(self,kwargs:dict):
        if not kwargs.get('duration'): kwargs['duration'] = 4.5
        if not kwargs.get('timestamp'): kwargs['timestamp'] = time.time()
        smartc.request("getNotice", json.dumps(kwargs), None)
    
    '''/**
    * 获取最新的信用资产信息
    *
    */'''
    #2022-4-18 新增信用函数
    def queryCreditAssets(self, account_id:str=None, cb=None):
        if not account_id:
            account_id = self.current_account.account_id
        if not cb:
            raise Exception("cb required!")
        account = self.account_map[account_id]
        if (account and account.account_type == AccountType.Credit):
            def creditAssetscb(data):
                try:
                    creditAssets = decodeRsp(data)
                    utils.assign(account.assets, convertCreditAssetsFromSmartToPlugin(creditAssets))
                    cb(account.assets,None)
                except RspError as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)
            smartc.request("queryCreditAssets","{}", creditAssetscb)
        else:
            cb(None,RspError({"code":"1001","message":"当前账号类型暂不支持"}))

    #2022-5-7 新增获取自选股列表
    def querySelfSelectStockList(self, groupName:str=None, source:str=None , account_id:str=None, cb=None):
        if not groupName:
            raise Exception("groupName required!")
        if not account_id:
            account_id = self.current_account.account_id
        if not source:
            source  = "xtp"
        if not cb:
            raise Exception("cb required!")
        
        def querySelfSelectStockListCB(rsp:str):
            try:
                stockList = decodeRsp(rsp)
                cb(stockList,None)
            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
                cb(None,rspError)

        params = { "boardName": groupName, "source": source , "account_id":account_id }
        smartc.request("getSelfSelectStocksService", json.dumps(params) ,querySelfSelectStockListCB)

    def createStrategy(self,account_id:str=None, strategy_platform_type:str=None, strategy_id:str=None, config:dict=None,cb=None):
        self.strategyManager.createInstance(account_id, strategy_platform_type, strategy_id, config,cb)
    
    def startStrategy(self,account_id:str=None, strategy_platform_type:str=None, clent_id:str=None,cb=None):
        self.strategyManager.startStrategy(account_id, strategy_platform_type, clent_id,cb)
    
    def insertAlgoOrder(self,account_id:str=None, strategy_id:str=None, config:dict=None,cb=None):
        manager = self.strategyManager.managers[StrategyPlatformType.Algo]
        manager.insertAlgoOrder(account_id, strategy_id, config,cb)

    def registCallableFunction(self,functionName:str=None,func=None):
        if not functionName:
            raise Exception("functionName required!")
        if not func:
            raise Exception("func required!")
        def callbackHandler(data):
            try:
                data = json.loads(data)
                reqID = data.get("reqID")
                if reqID:
                    result = func(data)
                    self.callJSFunction(reqID,result,None)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on(functionName,callbackHandler)
    
    def callJSFunction(self,functionName:str=None,params:dict=None,callback=None):
        if not functionName:
            raise Exception("functionName required!")
        if(not params):params = {}
        params["reqtype"] = 1 #1 内部js和py双向通信类型
        smartc.request(functionName, json.dumps(params),callback)
        
    #通过ipc跨进程通知插件js：python调试准备完成
    def isDebugReady(self,kwargs:dict):
        logger.debug("isDebugReady %s",json.dumps(kwargs))
        smartc.request("isDebugReady", json.dumps(kwargs), None)


    #  单次定时
    def add_timer(self,msec:int=0,callback=None):
        if(msec<=0):
            raise Exception("时间设置超出范围，必须大于0的整数")
        if not callback:
            raise Exception("callback required!")

        if self.is_back_test :
            return bt_core.add_timer_bt(msec, callback)

        sid = f'TIME_{uuid.uuid1()}'
        self._timerMap[sid] = 1

        def timeHandler(rsp:str):
            try:
                if not (sid in self._timerMap):return
                callback()
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.request("setTimeout", json.dumps({"during":msec}) ,timeHandler)
        return sid

    def clear_timer(self,sid:str):
        if self.is_back_test :
            bt_core.clear_timer_bt(sid)
            return

        if(sid in self._timerMap):
            del self._timerMap[sid]

        
    #  轮询定时
    def add_time_interval(self,msec:int=0,callback=None):
        
        if(msec<=0):
            raise Exception("时间设置超出范围，必须大于0的整数")
        if not callback:
            raise Exception("callback required!")

        if self.is_back_test :
            return bt_core.add_timer_interval_bt(msec, callback)

        sid = f'TIME_INTERVAL_{uuid.uuid1()}'
        self._timerMap[sid] = 1
        def timeHandler(rsp:str):
            try:
                if not (sid in self._timerMap):return
                callback()
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        smartc.on(sid,timeHandler)
        smartc.request("setInterval", json.dumps({"during":msec,"sid":sid}) ,None)
        return sid
    # 清除轮询定时
    def clear_time_interval(self,sid:str=None):
        logger.debug("enter clear_time_interval, sid: " + str(sid))
        if self.is_back_test :
            bt_core.clear_time_interval_bt(sid)
            return

        if not sid:
            raise Exception("sid required!")
        if(sid in self._timerMap):
            del self._timerMap[sid]
            smartc.request("clearInterval", json.dumps({"sid":sid}) ,None)


    '''/**
    * 券源行情查询
    * @param 必填 cb  查询券源行情列表的回调
    * */'''
    def query_source_quote_list(self, queryCallback= None):
        if not queryCallback:
            raise Exception("queryCallback required!")
        logger.debug("query_source_quote_list")
        cb = queryCallback
        def query_source_quote_list_CB(rsp:str):
                try:
                    sourceList = decodeRsp(rsp)
                    # logger.debug("query_source_quote_list_CB:%d",len(sourceList))
                    results =[]
                    for item in sourceList:
                        sourceQuoteInfo = SourceQuoteInfo()
                        sourceQuoteInfo.sno = item.get('sno')
                        sourceQuoteInfo.stk_code = item.get('stkCode')
                        sourceQuoteInfo.stk_name = item.get('stkName')
                        sourceQuoteInfo.quotation_type = item.get('quotationType')
                        sourceQuoteInfo.end_date = item.get('endDate')
                        sourceQuoteInfo.term_rate = 0 if not item.get('termRate') or item.get('termRate') == '0' else float(item.get('termRate'))
                        sourceQuoteInfo.lend_qty = 0 if not item.get('lendQty') or item.get('lendQty') == '0' else int(item.get('lendQty'))
                        sourceQuoteInfo.reallend_qty = 0 if not item.get('reallendQty') or item.get('reallendQty') == '0' else int(item.get('reallendQty'))
                        sourceQuoteInfo.match_qty = item.get('matchQty')
                        sourceQuoteInfo.market = item.get('market')
                        sourceQuoteInfo.term_code = 0 if not item.get('termCode') or item.get('termCode') == '0' else int(item.get('termCode'))
                        sourceQuoteInfo.lend_qty_des = item.get('lendQtyDes')
                        sourceQuoteInfo.remark = item.get('remark')
                        # sourceQuoteInfo.canlend_qty = item.get('canlendQty')  暂不开放给客户
                        # sourceQuoteInfo.posstr = item.get('posstr')
                        # sourceQuoteInfo.reqrate = item.get('reqrate')
                        # sourceQuoteInfo.serverid = item.get('serverid')
                        # sourceQuoteInfo.status = item.get('status')
                        sourceQuoteInfo.sys_date = item.get('sysDate')
                        # sourceQuoteInfo.tar_seat = item.get('tarSeat')
                        # sourceQuoteInfo.tar_secu_id = item.get('tarSecuId')
                        results.append(sourceQuoteInfo)
                    cb(results,None)
                except Exception as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)
        logger.debug("query_source_quote_list send")
        smartc.request("querySourceQuoteList","{}",query_source_quote_list_CB)

    '''/**
    * 券源申请
    * @param 必填 account_id 资金账号id
    * @param 必填 applySources 券源行情申请列表
    * @param 必填 cb  券源申请提交的回调
    * */'''
    def submit_source_apply(self,account_id:str=None,applySources:list[SourceQuoteInfo]=None, cb=None):
        logger.debug("submit_source_apply")
        if not account_id:
            account_id = self.current_account.account_id
        if not applySources:
            raise Exception("applySources required!")
        if not cb:
            raise Exception("cb required!")
        sendList = []
        applySourcesMap ={}
        for item in applySources:
            item.req_qty = 0 if not hasattr(item,'req_qty') else scienceNum2numstr(item.req_qty) #数量
            # item.req_qty = '0' if not hasattr(item,'req_qty') else str(item.req_qty) #数量
            # item.termCode = '' if not hasattr(item,'termCode') else str(item.termCode) #期限
            # item.termRate = '' if not hasattr(item,'termRate') else str(item.termRate) #费率
            now=datetime.now()
            item.sys_date= now.strftime("%Y%m%d") if not hasattr(item,'sys_date') else item.sys_date #系统日期
            
            if not hasattr(item,'prepare_date') or not item.prepare_date:
                item.prepare_date=item.sys_date
            if not hasattr(item,'prepare_date_end') or not item.prepare_date_end:
                item.prepare_date_end=item.sys_date
            
            item.term_rate = scienceNum2numstr(item.term_rate)
            # item.lend_qty = str(item.lend_qty)
            # item.term_code = str(item.term_code)
            sendItem = {}
            sendItem["rowId"] = str(uuid.uuid1())
            sendItem["userName"] = account_id
            sendItem["market"] = item.market
            sendItem["stkCode"] = item.stk_code
            sendItem["prepareDate"] = item.prepare_date
            sendItem["prepareDateEnd"] = item.prepare_date_end
            sendItem["termCode"] = item.term_code
            sendItem["reqQty"] = item.req_qty
            sendItem["termRate"] = item.term_rate
            sendItem["sno"] = item.sno
            sendItem["quotationType"] = item.quotation_type
            sendItem["errorMsg"] = "" if not hasattr(item,'error_msg') else item.error_msg
            sendList.append(sendItem)
            applySourcesMap[sendItem["rowId"]] = item
        #组织券源申请数据
        def submitSourceApplyCB(rspInfo:str):
            try:
                rsp = None
                try:
                    rsp = json.loads(rspInfo)
                except Exception as err:
                    rsp = {
                        "code":"9999",
                        "message":err
                    }
                    raise RspError(rsp)
                sourceList = rsp.get("data")
                if(rsp["code"] == "0000"):#全部成功
                    successList = []
                    for it in sourceList:
                        applyItem = applySourcesMap[it["rowId"]]
                        applyItem.account_id = it["userName"]
                        successList.append(applyItem)
                    # rsp["message"] = "券源申请推送成功"
                    # rspInfo = smart.utils.toString(rsp)
                    cb(successList,None)
                elif(rsp["code"] == "0001"):#数据校验出问题或券源申请推送存在失败的
                    #过滤出成功、失败的数据集合
                    successList = []
                    errList = []
                    for it in sourceList:
                        applyItem = applySourcesMap[it["rowId"]]
                        applyItem.account_id = it["userName"]
                        if not 'errorMsg'in it.keys() or not it['errorMsg']:
                            successList.append(applyItem)
                        else:
                            applyItem.error_msg = it['errorMsg']
                            errList.append(applyItem)
                    rsp = {
                        "code":"0001",
                        "message":"失败",
                        "value":errList
                    }
                    cb(successList,rsp)
                else:
                    cb(None,rspInfo)
            except Exception as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
                cb(None,rspError)
        logger.debug("submit_source_apply send")
        smartc.request("submitSourceApply",json.dumps({"submitSourceApplys":sendList}),submitSourceApplyCB)

    '''/**
    * 回测 获取行情数据--同步
    * @param 必填 method 方法
    * @param 必填 inParams 请求参数
    * @param 选填 outFormat 返回类型：List、DataFrame、Ndarray
    * */'''
    def query_data(self,method,inParams = None,outFormat=OutFormat.List):
        try:
            if method == "current_next_trading_day" and not inParams:
                inParams = {}

            rsp = smartc.request_reply("query_data_async",json.dumps({ 'method':method,'inParams': inParams,'from':'frontpy','sdk_ver':'' }))
            marketDataList = decodeRsp(rsp)
            if outFormat ==OutFormat.List: #将返回数据进行转化为客户指定的类型数据
                marketDataList= marketDataList
            elif outFormat ==OutFormat.DataFrame:
                import pandas as pd
                marketDataList = pd.DataFrame(marketDataList)
            elif outFormat ==OutFormat.Ndarray:
                import numpy as np
                marketDataList = np.array(marketDataList)
        except Exception as rspError:
            raise rspError
        return marketDataList
    
    '''/**
    * 回测 获取行情数据--异步
    * @param 必填 method 方法
    * @param 必填 inParams 请求参数
    * @param 必填 query_data_callback 查询结果的回调函数
    * @param 选填 outFormat 返回类型：List、DataFrame、Ndarray
    * */'''
    def query_data_async(self,method, inParams = None, query_data_callback= None, outFormat=OutFormat.List):
        logger.debug("query_data_async start")

        if method == "current_next_trading_day" and not inParams:
            inParams = {}

        if not query_data_callback:
            logger.debug("回调函数query_callback必填")
            return
            # raise Exception("queryCallback required!")

        cb = query_data_callback
        def query_data_async_CB(rsp:str):
                try:
                    marketDataList = decodeRsp(rsp)
                    if outFormat ==OutFormat.List: #将返回数据进行转化为客户指定的类型数据
                        marketDataList= marketDataList
                    elif outFormat ==OutFormat.DataFrame:
                        import pandas as pd
                        marketDataList = pd.DataFrame(marketDataList)
                    elif outFormat ==OutFormat.Ndarray:
                        import numpy as np
                        marketDataList = np.array(marketDataList)
                    # logger.debug("get_data_async_CB:%d",len(marketDataList))
                    cb(marketDataList,None)
                except Exception as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)
        logger.debug("query_data_async send")
        smartc.request("query_data_async",json.dumps({ 'method':method,'inParams': inParams,'from':'frontpy','sdk_ver':'' }), query_data_async_CB)
    

    '''/**
    * 回测 获取bar行情数据--同步
    * @param 必填 inParams 请求参数
    * */'''
    def query_bar(self,inParams):
        try:
            method = "bar"
            rsp = smartc.request_reply("query_data_async",json.dumps({ 'method':method,'inParams': inParams,'from':'frontpy','sdk_ver':'' }))
            tempList = decodeRsp(rsp)
            barDataList = []
            for item in tempList:
                barDataList.append(convertQuoteIndicatorFromSmartToPlugin(None,item))
        except Exception as rspError:
            raise rspError
        return barDataList  
  
    '''/**
    * 回测 获取bar行情数据--异步
    * @param 必填 inParams 请求参数
    * @param 必填 query_bar_callback 查询结果的回调函数
    * */'''
    def query_bar_async(self,inParams, query_bar_callback= None):
        if not query_bar_callback:
            logger.debug("回调函数query_bar_callback必填")
            return
            # raise Exception("queryCallback required!")

        cb = query_bar_callback
        def query_data_async_CB(rsp:str):
                try:
                    tempList = decodeRsp(rsp)
                    barDataList = []
                    for item in tempList:
                        barDataList.append(convertQuoteIndicatorFromSmartToPlugin(None,item))
                    cb(barDataList, None)
                    return True
                except Exception as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)
        method = "bar"
        smartc.request("query_data_async",json.dumps({ 'method':method,'inParams': inParams,'from':'frontpy','sdk_ver':'' }), query_data_async_CB)

    '''/**
    * 回测 获取ticker行情数据--同步
    * @param 必填 inParams 请求参数
    * */'''
    def query_market_data(self,inParams):
        try:
            method = "market_data"
            rsp = smartc.request_reply("query_data_async",json.dumps({ 'method':method,'inParams': inParams,'from':'frontpy','sdk_ver':'' }))
            tempList= decodeRsp(rsp)
            marketDataList = []
            for item in tempList:
                marketDataList.append(convertQuoteFromServerToPlugin(item))
        except Exception as rspError:
            raise rspError
        return marketDataList 

    '''/**
    * 回测 获取ticker行情数据--异步
    * @param 必填 inParams 请求参数
    * @param 必填 query_market_data_callback 查询结果的回调函数
    * */'''
    def query_market_data_async(self,inParams, query_market_data_callback= None):
        if not query_market_data_callback:
            logger.debug("回调函数query_market_data_callback必填")
            return
            # raise Exception("queryCallback required!")
        cb = query_market_data_callback
        def query_data_async_CB(rsp:str):
                try:
                    tempList= decodeRsp(rsp)
                    marketDataList = []
                    for item in tempList:
                        marketDataList.append(convertQuoteFromServerToPlugin(item))
                    cb(marketDataList, None)
                    return True
                except Exception as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)
        method = "market_data"
        smartc.request("query_data_async",json.dumps({ 'method':method,'inParams': inParams,'from':'frontpy','sdk_ver':'' }), query_data_async_CB)

    '''/**
    * 回测 获取行情数据--分页同步
    * @param 必填 method 方法
    * @param 必填 inParams 请求参数
    * @param 选填 outFormat 返回类型：List、DataFrame、Ndarray
    * */'''
    def query_data_page(self, method, inParams, outFormat=OutFormat.List):
        try:
            rsp = smartc.request_reply("query_data_page_async",json.dumps({ 'method':method,'inParams': inParams,'from':'frontpy','sdk_ver':'' }))
            result = decodeRsp(rsp)
            resultInfo = DataPageInfo()
            resultInfo.currentPage = result.get('currentPage')   
            resultInfo.pageSize = result.get('pageSize')
            resultInfo.totalCount = result.get('totalCount')
            resultInfo.totalPage = result.get('totalPage')
            dataList = result.get('data')
            if outFormat ==OutFormat.List: #将返回数据进行转化为客户指定的类型数据
                dataList= dataList
            elif outFormat ==OutFormat.DataFrame:
                import pandas as pd
                dataList = pd.DataFrame(dataList)
            elif outFormat ==OutFormat.Ndarray:
                import numpy as np
                dataList = np.array(dataList)
            resultInfo.data = dataList
        except Exception as rspError:
            raise rspError
        return resultInfo
    
    
    '''/**
    * 回测 获取行情数据--分页异步
    * @param 必填 method 方法
    * @param 必填 inParams 请求参数
    * @param 必填 query_data_page_callback 查询结果的回调函数
    * @param 选填 outFormat 返回类型：List、DataFrame、Ndarray
    * */'''
    def query_data_page_async(self,method, inParams, query_data_page_callback= None, outFormat=OutFormat.List):
        logger.debug("query_data_page_async start")
        
        if not query_data_page_callback:
            logger.debug("回调函数query_callback必填")
            return
            # raise Exception("queryCallback required!")

        cb = query_data_page_callback
        def query_data_page_async_CB(rsp:str):
                try:
                    result = decodeRsp(rsp)
                    resultInfo = DataPageInfo()
                    resultInfo.currentPage = result.get('currentPage')   
                    resultInfo.pageSize = result.get('pageSize')
                    resultInfo.totalCount = result.get('totalCount')
                    resultInfo.totalPage = result.get('totalPage')

                    dataList = result.get('data')
                    if outFormat ==OutFormat.List: #将返回数据进行转化为客户指定的类型数据
                        dataList= dataList
                    elif outFormat ==OutFormat.DataFrame:
                        import pandas as pd
                        dataList = pd.DataFrame(dataList)
                    elif outFormat ==OutFormat.Ndarray:
                        import numpy as np
                        dataList = np.array(dataList)
                    resultInfo.data = dataList
                    cb(resultInfo,None)
                except Exception as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)
        logger.debug("query_data_page_async send")
        smartc.request("query_data_page_async",json.dumps({ 'method':method,'inParams': inParams,'from':'frontpy','sdk_ver':'' }), query_data_page_async_CB)
    
    
    #信用现金还款
    def credit_cash_repay(self,account_id,amount, callback=None):
        if not account_id:
            account_id = self.current_account.account_id    
        def repay_callback(data:str):
            try:
                data = json.loads(data)
                if data.get("code")== "0000":
                    data = data["data"]
                else:
                    data = None
                callback and callback(data,None)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
                callback and callback(None,err)
        smartc.request("creditCashRepay", json.dumps({
                'amount': amount,
            }),repay_callback)
    

        
    '''/**
    * 获取当天任意分钟的行情数据--异步接口
    * @param codes 必填 股票列表 数组 如['600000.SH','000001.SZ']
    * @param query_bar_today_callback 必填 查询结果的回调函数 
    * @param period 选填 周期 默认1m（m代表分钟）
    * */'''
    def query_bar_today_async(self, codes, query_bar_today_callback= None, period="1m"):
        #读取用户信息
        if codes:
            newCodes =[]
            for code in codes:
                code = code.upper()
                newCodes.append(code)
            codes = newCodes

        if not query_bar_today_callback:
            logger.debug("回调函数query_callback必填")
            return
            # raise Exception("queryCallback required!")

        logger.debug("query_bar_today_async")
        cb = query_bar_today_callback
        def query_current_bar_list_CB(rsp:str):
                try:
                    currentBarMap = decodeRsp(rsp)
                    logger.debug("query_bar_today_CB:%d",len(currentBarMap))
                    # 将查询结果进行处理，把bar行情信息转成bar实体
                    if currentBarMap:
                        for k, v in currentBarMap.items():
                            if v:
                                results =[]
                                for item in v:
                                    barInfo = convertQuoteIndicatorFromSmartToPlugin(None,item)
                                    results.append(barInfo)
                                currentBarMap[k] = results
                    cb(currentBarMap, None)
                    return True
                except Exception as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)
        logger.debug("query_bar_today_async send")
        inParams = { 'code': codes, 'period': period }
        smartc.request("query_bar_today_async", json.dumps({'inParams': inParams}), query_current_bar_list_CB)
    
    '''/**
    * 获取当天任意分钟的行情数据--同步接口
    * @param codes 必填 股票列表 数组 如['600000.SH','000001.SZ']
    * @param period 选填 周期 默认1m（m代表分钟）
    * */'''
    def query_bar_today(self, codes, period="1m"):
        try:
            #读取用户信息
            if codes:
                newCodes =[]
                for code in codes:
                    code = code.upper()
                    newCodes.append(code)
                codes = newCodes

            logger.debug("query_bar_today send")
            inParams = { 'code': codes, 'period': period }
            rsp = smartc.request_reply("query_bar_today_async", json.dumps({'inParams': inParams}))
            currentBarMap = decodeRsp(rsp)
            if currentBarMap:
                for k, v in currentBarMap.items():
                    if v:
                        results =[]
                        for item in v:
                            barInfo = convertQuoteIndicatorFromSmartToPlugin(None,item)
                            results.append(barInfo)
                        currentBarMap[k] = results
            logger.debug("query_bar_today rsp:%d",len(currentBarMap))
        except Exception as rspError:
            raise rspError
        return currentBarMap
    
    '''/**
    * 获取当前交易日及下一交易日。当前日期不是交易日时，则当前交易日为空  --异步接口
    * @param get_trading_day_async_callback 必填 查询结果的回调函数 
    * */'''
    def get_trading_day_async(self, get_trading_day_async_callback= None):
    
        if not get_trading_day_async_callback:
            logger.debug("回调函数get_trading_day_async_callback必填")
            return
            # raise Exception("queryCallback required!")

        logger.debug("get_trading_day_async_callback")
        cb = get_trading_day_async_callback
        def get_trading_day_async_CB(rsp:str):
                try:
                    tradingDayMap = {}
                    tradingDayList = decodeRsp(rsp)
                    if tradingDayList and len(tradingDayList)>0:
                        tradingDayMap = tradingDayList[0]
                    logger.debug("get_trading_day_async_CB:%d",len(tradingDayList))
                    cb(tradingDayMap, None)
                    return True
                except Exception as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)
        logger.debug("get_trading_day_async send")
        inParams = {}
        method = "current_next_trading_day"
        smartc.request("query_data_async",json.dumps({ 'method':method,'inParams': inParams,'from':'frontpy','sdk_ver':'' }), get_trading_day_async_CB)

    '''/**
    * 获取当前交易日及下一交易日。当前日期不是交易日时，则当前交易日为空  ---同步接口
    * */'''
    def get_trading_day(self):
        try:
            #读取用户信息
            logger.debug("get_trading_day send")
            inParams = {}
            method = "current_next_trading_day"
            rsp = smartc.request_reply("query_data_async",json.dumps({ 'method':method,'inParams': inParams,'from':'frontpy','sdk_ver':'' }))
            tradingDayMap = {}
            tradingDayList = decodeRsp(rsp)
            if tradingDayList and len(tradingDayList)>0:
                tradingDayMap = tradingDayList[0]
            logger.debug("get_trading_day rsp:%d",len(tradingDayList))
        except Exception as rspError:
            raise rspError
        return tradingDayMap
smart = Smart()