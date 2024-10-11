from .type import *
from .event import *
from .emitter import *
from .utils import *
import logging
logger = logging.getLogger()

'''
 smart提供的账号对象  代表一个资金账号及资产、持仓信息
'''
class Account(Emitter):
    def __init__(self,context):
        super().__init__()
        self.smart = context
        self.account_id = ''  # 资金账号
        self.nick_name = ''  # 资金账号的昵称
        self.exchange_right = "unknown"  # 沪深交易权限  all两市   sh上海  sz深圳  双中心用户登录一个节点只有一个市场的权限
        self.account_type = AccountType.Unknown  # 账户类型 AccountType
        self.source = Source.Unknown  # 账户使用的柜台类型  Source枚举
        self.xtp_account_type = 'XTP_ACCOUNT_UNKNOWN'  # xtpd账户类型 如XTP_ACCOUNT_NORMAL
        self.isLevel2 = False  # 是否支持level2,默认False，不支持
        self.assets = Assets()  # 该账号的实时资产信息
        self.position_list = []  # 该账号的实时持仓信息
        self.positionMap = {}  # 账户持仓的map集合
        self.order_list = []  # 该账户的实时委托确认列表
        self.order_map = {}  # 根据order_id（xtpid）快速查找某个实时委托单
        self.trade_list = []  # 该账户的实时成交回报列表
        self.trade_map = {}  # 根据order_id（xtpid）快速查找某个实时成交
        self.ipo_list = []  # 该账号的打新列表 # todo: 待实现 绍光  1.0.0未写入文档,独立接口smart初始化未请求，需要单独请求
        self.strategy_map = {}  # 该资金账号的策略集合 key为strategy_id+'_'+StrategyPlatformType value为strategy对象
        self.alphax_td_status = StrategyStatus.Unknown  # alphax td的运行状态
        self.alphax_md_status = StrategyStatus.Unknown  # alphax md的运行状态
        self.credit_ticker_assign_list = []  #该账号的信用实时可融券头寸信息
        self.credit_ticker_assign_map = {}  #该账号的信用实时可融券头寸信息 map集合
        self.credit_debt_finance_list = [] #融资负债合约列表
        self.credit_debt_finance_map = {} #融资负债合约索引
        self.credit_debt_security_list = [] #融券负债合约列表
        self.credit_debt_security_map = {} #融券负债合约索引
        self.book = None #子账户Book

    '''
    新增委托回报
    '''
    #2022-4-13
    def _addOrderInfo(self, orderInfo:Order):
        oldOrderInfo = None #  todo：这里判断可能条件不足 特别是多账号下可能冲突
        if self.order_map.get(orderInfo.order_id,None) :
            oldOrderInfo = self.order_map[orderInfo.order_id]  #  todo：这里判断可能条件不足 特别是多账号下可能冲突

        if not oldOrderInfo :
            self.order_map[orderInfo.order_id] = orderInfo
            self.order_list.append(orderInfo)
        else:
            assign(oldOrderInfo,orderInfo)
        self.emit(Event.ON_ORDER, orderInfo)

    '''
    新增成交回报
    '''
    #2022-4-13
    def _addTradeReport(self,report:Trade):
        oldReport = None
        if self.trade_map.get(report.trade_id) :
            oldReport = self.trade_map[report.trade_id]
        
        if not oldReport:
            self.trade_map[report.trade_id] = report
            self.trade_list.append(report)
            self.emit(Event.ON_TRADE, report)

    '''
    刷新持仓信息
    '''
    def refreshPositionList(self,list:list[Position]):
        self.position_list = list
        self.positionMap = {}
        for position in list :
            key = "{}_{}_{}".format(position.instrument_id,position.exchange_id,position.direction)
            self.positionMap[key] = position

    '''
     *    账号级别的insert_order 下委托单  不支持account_id和strategy_platform_type、strategy_id参数 client_id和parent_order_id选填
     *    说明：通过该接口下单，不会记在任何策略上
     *    入参：
     * @param    instrument_id	str	必填 合约ID，如证券代码 "600000"(该参数与code参数必填其一)
     * @param    exchange_id	str	必填 交易所ID 参考Exchange对象 如"SSE"(该参数与code参数必填其一)
     * @param    limit_price    float 必填 价格 如10.32
     * @param    volume int 必填 数量 如100
     * @param    price_type	PriceType枚举 选填 报单类型，默认为Limit
     * @param    side	Side枚举 选填 买卖方向，默认为Buy
     * @param    offset	Offset枚举	选填 开平方向，默认为Init
     * @param    order_client_id str 选填 客户自定义id，默认为0
     * @param    parent_order_id str 选填 母单编号，默认为""
     * @param    business_type str 选填 BusinessType下枚举值，默认为CASH
     * @param    autoSplit boolean 选填 自动拆单，默认为False
     * @param    code str 必填 证券代码.交易所标识,600000.SH,000001.SZ(若该参数与instrument_id、exchange_id同时存在,以该参数为准)
     *   返回：
     *   {
     *       order_id,//	 String	订单ID  对alphax为功夫order_id  对其他都是xtpid
     *       counter_order_id,//  String  柜台订单id 对alphax为external_order_id即xtpid
     *   }
    '''
    #2022-4-11
    def insert_order(self,
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
        
        return self.smart.insert_order(self.account_id, None, None, instrument_id, exchange_id, limit_price, volume,  price_type,
                              side, offset, order_client_id, parent_order_id, business_type,callback,autoSplit,code)

    '''
    账号级别的撤单  不支持account_id参数
    '''
    2022-4-11
    def cancel_order(self,order_id:str=None, cb=None):
        return self.smart.cancel_order(self.account_id, order_id,cb)

    '''
     * 订阅行情  注意无account_id参数  这里区别alphax后台的subscribe函数是后台第一个参数是source
     * @param instruments 必填 订阅的股票列表 数组 如['600000'](该参数与codes参数必填其一)
     * @param exchange_id 必填 交易所id 如Exchange.SSE(该参数与codes参数必填其一)
     * @param is_level2 选填 是否level2，默认为False bool类型 True or False 目前暂不支持level2
     * @param codes 必填 订阅股票的证券代码.交易所标识列表 数组 如['600000.SH','300001.SZ'](若该参数与instruments、exchange_id同时存在,以该参数为准)
     '''
     #2022-4-11
    def subscribe(self, instruments:list[str]=None, exchange_id:str=None, is_level2:bool=False,callback=None,codes:list[str]=None):
        return self.smart.subscribe(self.account_id, instruments, exchange_id, is_level2, self, callback, codes)

    '''
     * 取消订阅  注意无account_id参数  这里区别alphax后台的unsubscribe函数是后台第一个参数是source
     * @param instruments 必填 订阅的股票列表 数组 如['600000'](该参数与codes参数必填其一)
     * @param exchange_id 必填 交易所id 如Exchange.SSE(该参数与codes参数必填其一)
     * @param is_level2 选填，默认为False 是否level2 bool类型 True or False 目前暂不支持level2
     * @param codes 必填 订阅股票的证券代码.交易所标识列表 数组 如['600000.SH','300001.SZ'](若该参数与instruments、exchange_id同时存在,以该参数为准)
    '''
    #2022-4-11
    def unsubscribe(self,instruments:list[str]=None, exchange_id:str=None, is_level2:bool=False, codes:list[str]=None):
        return self.smart.unsubscribe(self.account_id, instruments, exchange_id, is_level2, self, codes)

    '''
     * 订阅指数行情  注意无account_id参数
     * @param instruments 必填 订阅的指数列表 数组 如["000001", "CESCPD", "931646"]
     * @param is_level2 选填 是否level2，默认为False bool类型 True or False 目前暂不支持level2
     * @param callback 选填 订阅后的数据或错误返回信息参数(quoteList,err)
     '''
    def subscribe_index(self, instruments:list[str]=None, is_level2:bool=False,callback=None):
        return self.smart.subscribe_index(self.account_id, instruments, is_level2, self, callback)
    
    '''
     * 取消订阅指数行情  注意无account_id参数
     * @param instruments 必填 订阅的指数列表 数组 如["000001", "CESCPD", "931646"]
     * @param is_level2 选填，默认为False 是否level2 bool类型 True or False 目前暂不支持level2
    '''
    def unsubscribe_index(self, instruments:list[str]=None, is_level2:bool=False):
        return self.smart.unsubscribe_index(self.account_id, instruments, is_level2, self)
    
    def createStrategy(self, strategy_platform_type:str=None, strategy_id:str=None, config:dict=None,cb=None):
        self.smart.createStrategy(self.account_id, strategy_platform_type, strategy_id, config,cb)

    def startStrategy(self, strategy_platform_type:str=None, clent_id:str=None,cb=None):
        self.smart.startStrategy(self.account_id, strategy_platform_type, clent_id,cb)
    
    def insertAlgoOrder(self, strategy_id:str=None, config:dict=None,cb=None):
        self.smart.insertAlgoOrder(self.account_id, strategy_id, config,cb)

    # 券源申请提交
    def submit_source_apply(self,applySources:list[SourceQuoteInfo]=None, cb=None):
        self.smart.submit_source_apply(self.account_id,applySources, cb)

    '''
    #  
    #   * 获取本账号登记的策略列表map集合
    #   * 返回一个map集合 key：strategy_id  value:{strategy_id:'',strategy_platform_type:'' }
    #   * alphax：返回server端记录的该资金账号下可见的策略集合   algo：返回该客户有权限的策略集合
    #  
    #  // Account.prototype._reQueryStrategyMap = async function () {
    #  //     this.strategy_map = await strategyManager.getStrategyMap(/* platform_type */ null, /* account */ this);
    #  //     return this.strategy_map;
    #  // };

    #  /**
    #   * 向本账号登记一个策略
    #   * @param strategy_platform_type String必填 策略平台类型  StrategyPlatformType的枚举值  不同的策略有不同的行为：
    #   *              AlphaX类型的登记后smart server形成一条记录  客户端策略列表中会出现，需要进一步调用newStrategyInstance拿到实例后进行uploadFile后再startStrategy
    #   *              Algo类型的不允许客户主动登记策略
    #   *              ProgramTrade类型和Spec类型的可由客户主动登记策略，记录在smartserver  提供的信息比AlphaX的多一些
    #   *              Front类型的实际就是客户向组件市场登记一个私有策略，记录在smartserver，如果之后uploadFile则为向组件市场上传一个纯前端的私有策略，如果是不调用uploadFile直接startStrategy则直接启动本地组件目录中的该策略（只能是.smart包格式），如果本地不存在该策略则菜单中不显示
    #   * @param strategy_id String可选 策略id  可以含中文，为了防止冲突，尽量特殊些，不要用"网格交易"这种很通用的命名，很容易冲突
    #   * @param config 策略信息对象  记录在smartserver
    #   *              {
    #   *                  strategy_path:'',//String(可选)  对Front为.smart包的文件名   对AlphaX不需要传，自动取strategy_id作为策略存放相对路径   对Algo不需要传    对ProgramTrade和Spec类型的为策略所在文件夹在托管机器的全路径（removeStrategy时会删除该文件夹）
    #   *                  strategy_configfile_path_list: [''],//Array< String >(可选)  策略配置文件路径列表  对AlphaX和ProgramTrade和Spec类型的需要传递  可以多个路径
    #   *                  strategy_log_path_list: [''],//Array< String >(可选) 策略日志文件的路径列表  仅ProgramTrade和Spec类型的需要传递  可以多个，里面的路径都会被smart的logstash收集  Front类型的日志自动被smart收集无需传递
    #   *                  startStrategyCMD: '',//String(可选) 策略启动的cmd命令字符串  仅ProgramTrade和Spec类型的需要传递
    #   *                  template_code: '',//String(可选) 策略模板代码  AlphaX平台创建公共策略时必填
    #   *              }
    #   *
    #   * await形式返回Strategy对象
    #   *
    #   * 不同的策略有不同的行为：
    #   * AlphaX类型的登记后smart server形成一条记录 客户端策略列表中会出现，需要进一步调用newStrategyInstance拿到实例后进行uploadFile后再startStrategy
    #   * Algo类型的不允许客户主动登记策略
    #   * ProgramTrade类型和Spec类型的可由客户主动登记策略，记录在smartserver 提供的信息比AlphaX的多一些
    #   * Front类型的实际就是客户向组件市场登记一个私有策略，记录在smartserver，如果之后uploadFile则为向组件市场上传一个纯前端的私有策略， 如果是不调用uploadFile直接startStrategy则直接启动本地组件目录中的该策略（只能是.smart包格式），如果本地不存在该策略则菜单中不显示
    #   *
    #   */
    #  Account.prototype.registryStrategy = function (strategy_platform_type, strategy_id, config) {
    #      return self.smart.registryStrategy(this.account_id, strategy_platform_type, strategy_id, config);
    #  };
    #  Account.prototype.createStrategy = function (strategy_platform_type, strategy_id, config) {
    #      return self.smart.createStrategy(this.account_id, strategy_platform_type, strategy_id, config);
    #  };
    #  /**
    #   * 修改注册的策略信息
    #   * 参数见addStrategy
    #   */
    #  Account.prototype.modifyStrategy = function (strategy_platform_type, strategy_id, strategy_info) {
    #      return self.smart.modifyStrategy(this.account_id, strategy_platform_type, strategy_id, strategy_info);
    #  };
    #  /**
    #   * 创建策略实例 不论是哪种策略  都需要创建策略实例，拿到一个js的Strategy对象，才能操作该策略的方法，注意这里只是语言级别的，并非启动策略
    #   * @param strategy_platform_type  策略平台类型  StrategyPlatformType的枚举值
    #   * @param strategy_id
    #   *
    #   * 返回一个Strategy对象  然后调用strategy.startStrategy()等方法
    #   */
    #  // Account.prototype.newStrategyInstance = function (strategy_platform_type, strategy_id) {
    #  //     let strategy = self.smart.newStrategyInstance(this.account_id, strategy_platform_type, strategy_id);
    #  //     strategy.relation_account_map[this.account_id] = this;
    #  //     return strategy;
    #  // };
    #  /**
    #   * 删除一个策略 对AlphaX、ProgramTrade、Spec  后台策略目录下的策略文件会被删除  注册的策略也会被删除   对Front 该策略的.smart包会被删除，注册的策略也会被删除，但文件夹形式的组件不会被删除
    #   * @param strategy_platform_type
    #   * @param strategy_id
    #   */
    #  Account.prototype.removeStrategy = function (strategy_platform_type, strategy_id) {
    #      return self.smart.removeStrategy(this.account_id, strategy_platform_type, strategy_id);
    #  };
    '''
    '''
     * on_order注册处理函数
     * @param fn 注册的处理函数
    '''
    #2022-4-13
    def on_order(self,fn):
        self.addEventListener(Event.ON_ORDER, fn)


    '''
     * on_trade注册处理函数
     * @param fn 注册的处理函数
    '''
    #2022-4-13
    def on_trade(self,fn):
        self.addEventListener(Event.ON_TRADE, fn)
        

    '''
     * on_assets注册处理函数
     * @param fn 注册的处理函数
    '''
    #2022-4-14
    def on_assets(self,fn):
        self.addEventListener(Event.ON_ASSETS, fn)
        

    '''
     * on_position注册处理函数
     * @param fn 注册的处理函数
    '''
    def on_position(self,fn):
        self.addEventListener(Event.ON_POSITION, fn)
        

    '''
     * on_quote注册处理函数
     * @param fn 注册的处理函数
    '''
    def on_quote(self,fn):
        self.addEventListener(Event.ON_QUOTE, fn)
        

    '''
     * on_cancel_fail注册处理函数
     * @param fn 注册的处理函数
    '''
    def on_cancel_fail(self,fn):  # 参数为order对象  ？？？ 是否应该是xtpid、msg？？？
        self.addEventListener(Event.ON_CANCEL_FAIL, fn)


    '''/**
    * 获取最新的信用资产信息
    */'''
    def queryCreditAssets(self,cb):
        return self.smart.queryCreditAssets(self.account_id, cb)
    

    '''/**
    * on_credit_ticker_assign注册处理函数
    * 处理信用可融券头寸更新
    * @param fn 注册的处理函数
    */'''
    def on_credit_ticker_assign(self,fn):
        self.addEventListener(Event.ON_CREDIT_TICKER_ASSIGN, fn)

    
    '''/**
    * on_credit_debt_finance注册处理函数
    * 处理信用融资负债合约更新
    * @param fn 注册的处理函数
    */'''
    def on_credit_debt_finance(self,fn):
        self.addEventListener(Event.ON_CREDIT_DEBT_FINANCE, fn)

    
    '''/**
    * on_credit_debt_security注册处理函数
    * 处理信用融券负债合约更新
    * @param fn 注册的处理函数
    */'''
    def on_credit_debt_security(self,fn):
        self.addEventListener(Event.ON_CREDIT_DEBT_SECURITY, fn)

    
    '''/**
    * 
    * 获取指定的证券持仓
    * @param fn 持仓信息
    */'''
    def get_position(self,instrument_id:str=None, exchange_id:str=None, direction = Direction.Net, code:str=None):
        try:
            if (code):
                    instrument_id, exchange_id = getInstrumentIdAndExchangeIdFromCode(code)
            key = "{}_{}_{}".format(instrument_id ,exchange_id,direction)
            return self.positionMap.get(key,None)
        except Exception as e:
            logger.error(e,exc_info=True, stack_info=True)

    def init_book():
        pass
        
