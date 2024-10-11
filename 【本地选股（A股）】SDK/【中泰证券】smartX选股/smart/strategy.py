from .emitter import *
from .type import *
from . import smartc
from . import utils
from .utils import *
from .event import *
import json
import logging
logger = logging.getLogger()


class Strategy(Emitter):
    # 策略对象  strategy_platform_type为smart.Type.StrategyPlatformType的某一种  返回一个Strategy对象  然后调用strategy.startStrategy()等方法
    def __init__(self,context,strategyPlatformType:str, strategyId:str):
        super().__init__()
        self.smart = context
        self.strategy_platform_type = strategyPlatformType # StrategyPlatformType枚举 分AlphaX/Algo/ProgramTrade
        self.strategy_id = strategyId
        self.status = StrategyStatus.Unknown
        self.isPrivate = False # 是否是私有策略
        self.status_name = "未知"
        self.round_list = [] # 当天策略启动的轮次信息   一个策略对象，alphax同时只能start一次，形成一个round对象，round_list是该策略当天历次启动的列表；对algo一个策略对象可同时start多次，形成多个round对象，round_list也是当天历次启动的列表，每个round_id对algo就是parent_order_id
        self.last_round = None # 最后执行的轮次对象
        self.book = {
            "avail": 0, # 可用资金
            "margin": 0, # 保证金
            "market_value": 0, # 市值
            "initial_equity": 0, # 初始权益
            "dynamic_equity": 0, # 动态权益
            "static_equity": 0, # 静态权益
            "realized_pnl": 0, # 已实现盈亏
            "unrealized_pnl": 0, # 未实现盈亏
        } # 该策略的账簿信息  目前仅对AlphaX有效
        self.strategy_position_list = [] # 该策略的实时持仓 StrategyPosition对象集合
        # self.strategyPositionMap = {}#策略实时持仓的map集合
        self.strategy_order_list = [] # 该策略实时委托列表 Order对象集合
        # self.strategyOrderMap = {}#策略实时委托的map集合
        self.strategy_trade_list = [] # 该策略的实时成交回报 Trade对象集合
        # self.strategyTradeMap = {}#策略实时成交回报map集合
        self.relation_account_map = {} # 该策略涉及的资金账号
        self.data = {} # 策略的详细数据
        self.runtime_id = ""

    # 需要从初始化中拆分一个加载数据的方法，减轻初始化时的工作量
    def loadData(self):
        raise RspError({"code":RspError.NOT_SUPPORTED})

    # 上传策略文件
    def uploadFile(self,cb):
        cb(None,RspError({"code":RspError.NOT_SUPPORTED}))

# 启动策略  成功返回母单编号parent_order_id（字符串）  失败：返回'fail'
# todo: 还需要在start中判断有无权限、是否签协议  签协议全局弹出由smart进行签署
    def startStrategy(self,cb):
        if (self.strategy_platform_type == StrategyPlatformType.Algo):
            cb(self.runtime_id,None)
        else:
            cb(None,RspError({"code":RspError.NOT_SUPPORTED}))
            
    # 停止策略
    def stopStrategy(self,cb):
        if (self.strategy_platform_type == StrategyPlatformType.Algo):
            # 调stopStrategy
            def stop_callback(rsp):
                try:
                    data = decodeRsp(rsp)
                    cb(data,None)
                except RspError as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)
            smartc.request("algostopStrategy", json.dumps({"strategy_id":self.strategy_id}), stop_callback)
        else:
            # todo: 绍光
            cb(None,RspError({"code":RspError.NOT_SUPPORTED}))

    # 强制停止策略 直接退出，不做收尾动作  类似kill
    def forceStopStrategy(self) :
        if (self.strategy_platform_type == StrategyPlatformType.Algo) :
            # todo: 永震  调destroyStrategy
            smartc.request("algoforceStopStrategy", json.dumps({"strategy_id":self.strategy_id}), None)
        else:
            raise RspError({"code":RspError.NOT_SUPPORTED})
        
    # 策略启动前传参  strParms为字符串参数  filePath为策略平台落地的参数文件的相对本策略根目录的相对路径
    def postStrategyParamsBeforeStart(self,strParms, filePath):
        raise RspError({"code":RspError.NOT_SUPPORTED})
        
    # 策略运行期间向策略透传通用参数 strParms为字符串参数
    def postStrategyParams(self,strarms) :
        raise RspError({"code":RspError.NOT_SUPPORTED})
    # 修改某策略的book账簿数据
    def modifyStrategyBook(self,book) :
        raise RspError({"code":RspError.NOT_SUPPORTED})

    # 修改某策略的持仓数据 positionList为全量持仓数据
    def modifyStrategyPosition(self,positionList) :
        raise RspError({"code":RspError.NOT_SUPPORTED})
    # 设置费率 todo：是实现在策略级别还是账户级别？ 与smart客户端设置的费率是否打通一并修改？
    def setCommission(self,commission) :
        # todo: 魏义 优先级低 仅alphax
        raise RspError({"code":RspError.NOT_SUPPORTED})
    # 订阅策略日志并接受实时变动  对AlphaX为特定的logType（'STRATEGY'、'TD_'+资金账号、'MD'） 对ProgramTrade为注册策略时提供的logPath（需要做校验）
    def subscribeStrategyLog(self,logTypeOrPath) :
        raise RspError({"code":RspError.NOT_SUPPORTED})
    # 取消订阅策略日志并取消实时变动
    def unsubscribeStrategyLog(self,logTypeOrPath) :
        raise RspError({"code":RspError.NOT_SUPPORTED})
    # 取的日志N行内容  考虑到翻页 还需要行号参数
    def getStrategyLogContent(self) :
        raise RspError({"code":RspError.NOT_SUPPORTED})
    # 抛出异常通知 on_strategy_exception会被触发  仅Front前台策略使用 其他后台策略如果需要前台捕获异常信息需要实现后台的该方法
    def throwStrategyException(self) :
        raise RspError({"code":RspError.NOT_SUPPORTED})
        
    '''
    为策略添加资金账号 添加后策略就能收到这个账号的订阅、order、trade 该账号也被同步加入smart.accountMap中 AlphaX和ProgramTrade、Front使用   todo:魏义
    @param account_id 资金账号
    @param account_pwd 资金账号密码 可选 当不传密码时，界面自动弹窗与客户交互输入密码
    '''
    def addAccount(self,account_id, account_pwd) :
        raise RspError({"code":RspError.NOT_SUPPORTED})

    '''
    解除策略与账户的关系
    解除策略与资金账号绑定关系，策略无法收到该账户的订阅、order、trade 该账号从smart.accountMap删除
    并不是真的删除了物理资金账号，只是解除了与策略的关系，也解除了与当前账号的关系
    @param account_id 账号id
    '''
    def removeAccount(self,account_id) :
        # todo:魏义
        raise RspError({"code":RspError.NOT_SUPPORTED})

    '''
     启动td 仅对AlphaX有效
 * @param account_id  必填 账号id
 * @param pwd 选填 资金账号密码 如果当前登录账号为smart.accountMap中已经登录本客户端的，pwd可传可不传  如果是非登录用户必传
    '''
    def startTD(account_id, pwd) :
        raise RspError({"code":RspError.NOT_SUPPORTED})

    '''
    启动md 仅对AlphaX有效
    @param account_id 选填 当不填时走普通账户的订阅，对期货行情需要必传
    @param pwd 选填 资金账号密码 如果当前登录账号为smart.accountMap中已经登录本客户端的，pwd可传可不传  如果是非登录用户必传
    '''
    def startMD(account_id, pwd) :
        raise RspError({"code":RspError.NOT_SUPPORTED})


    '''
    *    策略级别的insert_order 下委托单  account_id必填  无strategy_platform_type和strategy_id参数    order_client_id和parent_order_id选填
    *    说明：通过该接口下单，会影响strategy的book和positionList
    *    入参：
    * @param    account_id	str	选填 交易账号（资金账号），默认为当前账号id
    * @param    instrument_id	str	必填 合约ID，如证券代码 "600000"(该参数与code参数必填其一)
    * @param    exchange_id	str	必填 交易所ID 参考Exchange对象 如"SSE"(该参数与code参数必填其一)
    * @param    limit_price    float 必填 价格 如10.32
    * @param    volume int 必填 数量 如100
    * @param    price_type	PriceType枚举	选填 报单类型，默认为Limit
    * @param    side	Side枚举	    选填 买卖方向，默认为Buy
    * @param    offset	Offset枚举	选填 开平方向，默认为Init
    * @param    order_client_id number 选填 客户自定义id，默认为0
    * @param    parent_order_id str 选填 母单编号，默认为""
    * @param    business_type str 选填 BusinessType下枚举值，默认为CASH
    * @param    callback function 选填 回调函数参数为下单后的返回结果 Order
    * @param    autoSplit boolean 选填 自动拆单，默认为False
    * @param    code str 必填 证券代码.交易所标识,600000.SH,000001.SZ(若该参数与instrument_id、exchange_id同时存在,以该参数为准)
    '''
    def insert_order(self,
                    account_id:str=None,
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
                    code:str=None) :
        return self.smart.insert_order(account_id, self.strategy_platform_type, self.strategy_id, instrument_id, exchange_id, limit_price, volume, price_type, side, offset, order_client_id, parent_order_id, business_type,callback,autoSplit,code)
    
    '''
    * 策略级别的撤单  account_id选填 注意后台的alphax第一个参数是order_id  第二个是account_id
    * @param account_id 选填 账号id，默认为当前账号id
    * @param order_id  必填
    * @param cb  选填
    '''
    def cancel_order(self,account_id:str=None, order_id:str=None,cb = None) :
        return self.smart.cancel_order(account_id, order_id,cb)

    '''
    * 订阅行情  注意无account_id参数  这里区别alphax后台的subscribe函数是后台第一个参数是source
    * @param account_id	str	选填 交易账号（资金账号），默认为当前账号id
    * @param instruments 必填 订阅的股票列表 数组 如['600000'](该参数与codes参数必填其一)
    * @param exchange_id 必填 交易所id 如Exchange.SSE(该参数与codes参数必填其一)
    * @param is_level2 选填 是否level2，默认为False bool类型 true or false 目前暂不支持level2
    * @param codes 必填 订阅股票的证券代码.交易所标识列表 数组 如['600000.SH','300001.SZ'](若该参数与instruments、exchange_id同时存在,以该参数为准)
    '''
    def subscribe(self,account_id:str=None, instruments:list[str]=None, exchange_id:str=None, is_level2:bool=False, callback=None, codes:list[str]=None) :
        return self.smart.subscribe(account_id, instruments, exchange_id, is_level2, self, callback, codes)

    '''
    * 取消订阅  注意无account_id参数  这里区别alphax后台的unsubscribe函数是后台第一个参数是source
    * @param  account_id   str	选填 交易账号（资金账号），默认为当前账号id
    * @param instruments 必填 订阅的股票列表 数组 如['600000'](该参数与codes参数必填其一)
    * @param exchange_id 必填 交易所id 如Exchange.SSE(该参数与codes参数必填其一)
    * @param is_level2 选填 是否level2，默认为False bool类型 true or false 目前暂不支持level2
    * @param codes 必填 订阅股票的证券代码.交易所标识列表 数组 如['600000.SH','300001.SZ'](若该参数与instruments、exchange_id同时存在,以该参数为准)
    '''
    def unsubscribe(self,account_id:str=None, instruments:list[str]=None, exchange_id:str=None, is_level2:bool=False, codes:list[str]=None) :
        return self.smart.unsubscribe(account_id, instruments, exchange_id, is_level2, self, codes)

    '''
    * on_strategy_quote 注册处理函数
    * @param fn 注册的处理函数
    '''
    def on_strategy_quote(self,fn) :
        self.addEventListener(Event.ON_QUOTE, fn)

    '''
    * on_order 注册处理函数
    * @param fn 注册的处理函数
    '''
    def on_order(self,fn) :
        self.addEventListener(Event.ON_ORDER, fn)

    '''
    * on_trade 注册处理函数
    * @param fn 注册的处理函数
    '''
    def on_trade(self,fn) :
        self.addEventListener(Event.ON_TRADE, fn)

    '''
    * on_position 注册处理函数
    * @param fn 注册的处理函数
    '''
    def on_position(self,fn) :
        self.addEventListener(Event.ON_POSITION, fn)

    '''
    * on_book 注册处理函数
    * @param fn 注册的处理函数
    '''
    def on_book(self,fn) :
        self.addEventListener(Event.ON_BOOK, fn)

    '''
    * on_strategy_cancel_fail 注册处理函数
    * @param fn 注册的处理函数
    '''
    def on_strategy_cancel_fail(self,fn) :
        self.addEventListener(Event.ON_STRATEGY_CANCEL_FAIL, fn)


    '''
    on_strategy_status_change 注册处理函数
    @param fn 注册的处理函数
    '''
    def on_strategy_status_change(self,fn) :
        self.addEventListener(Event.ON_STRATEGY_STATUS_CHANGE, fn)


    def download(self) :
        raise RspError({"code":RspError.NOT_SUPPORTED})


