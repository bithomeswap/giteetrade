# import Account
# from ./strategy/Round import Round
# from ./strategy/Strategy import Strategy

# 柜台类型源
class Source():
    Unknown = "unknown"
    XTP = "xtp"  # xtp
    CTP = "ctp"  # ctp
    SIM = "sim"  # sim


# 交易所 对应xtp XTP_MARKET_TYPE市场类型
class Exchange():
    Unknown = "Unknown"  # 未知 xtp =3 XTP_MKT_UNKNOWN 或 0 XTP_MKT_INIT初始化值或者未知
    SZE = "SZE"  # 深交所 xtp =1 XTP_MKT_SZ_A深圳A股
    SSE = "SSE"  # 上交所 xtp =2 XTP_MKT_SH_A上海A股
    BSE = "BSE" #  北交所 xtp = 3 XTP_MKT_BJ_A北京A股
    SHFE = "SHFE"  # 上期所
    DCE = "DCE"  # 大商所
    CZCE = "CZCE"  # 郑商所
    CFFEX = "CFFEX"  # 中金所
    INE = "INE"  # 能源中心

    # 以下交易所类型仅指数通支持
    HSE = "HSE"  # 沪深
    XGE = "XGE"  # 香港
    YTE = "YTE"  # 亚太
    ZQE = "ZQE"  # 债券市场
    QTE = "QTE"  # 其它
    QQE = "QQE"  # 全球


# get_data查询结果的转出类型
class OutFormat():
    Unknown = "Unknown"  # 未知 
    List = "List"  # list类型
    DataFrame = "DataFrame"  # DataFrame类型
    Ndarray = "Ndarray" #  Ndarray类型
    
# 证券类型 xtp =XTP_TICKER_TYPE
class InstrumentType():
    Unknown = 0  # 未知 xtp =5 XTP_TICKER_TYPE_UNKNOWN
    Stock = 1  # 股票 xtp =0 XTP_TICKER_TYPE_STOCK普通股票
    Future = 2  # 期货
    Bond = 3  # 债券 xtp =3 XTP_TICKER_TYPE_BOND债券
    StockOption = 4  # 股票期权 xtp =4 XTP_TICKER_TYPE_OPTION期权
    # 以下为alphax缺少
    Index = 5  # 指数 xtp =1 XTP_TICKER_TYPE_INDEX指数
    Fund = 6  # 基金 xtp =2 XTP_TICKER_TYPE_FUND基金


# ????? 好像没用到  功夫定义的？ 1.0.0未写入文档
# ExecType():
#     Unknown = 0
#     Cancel = 1
#     Trade = 2
#

'''
 * 价格条件
'''


class PriceType():
    # 无效  xtp =XTP_PRICE_TYPE_UNKNOWN
    Unknown = 0

    # 限价,通用  xtp:1 XTP_PRICE_LIMIT限价单-沪 / 深 / 沪期权（除普通股票业务外，其余业务均使用此种类型）
    Limit = 1

    #  市价，通用，
    #  对于股票上海为最优五档剩余撤销，深圳为即时成交剩余撤销
    #  xtp:4 XTP_PRICE_BEST5_OR_CANCEL最优5档即时成交剩余转撤销，市价单-沪
    #  或
    #  xtp:2 XTP_PRICE_BEST_OR_CANCEL即时成交剩余转撤销，市价单-深 / 沪期权
    Any = 2

    #  上海深圳最优五档即时成交剩余撤销，上交所的市价需要报价，深交所的市价不需要报价  xtp:4 XTP_PRICE_BEST5_OR_CANCEL最优5档即时成交剩余转撤销，市价单-沪深
    FakBest5 = 4

    #  仅深圳本方最优价格申报, 不需要报价  xtp:6 XTP_PRICE_FORWARD_BEST本方最优，市价单-深
    ForwardBest = 6

    #  上海最优五档即时成交剩余转限价，需要报价；深圳对手方最优价格申报，不需要报价
    #  xtp:3 XTP_PRICE_BEST5_OR_LIMIT最优五档即时成交剩余转限价，市价单-沪
    #  或
    #   7 XTP_PRICE_REVERSE_BEST_LIMIT对方最优剩余转限价，市价单-深 / 沪期权
    ReverseBest = 3

    #  股票（仅深圳）即时成交剩余撤销，不需要报价；期货即时成交剩余撤销，需要报价
    #  xtp:2 XTP_PRICE_BEST_OR_CANCEL即时成交剩余转撤销，市价单-深 / 沪期权
    Fak = 2

    #  股票（仅深圳）市价全额成交或者撤销，不需要报价；期货全部或撤销，需要报价
    #  xtp:5 XTP_PRICE_ALL_OR_CANCEL全部成交或撤销,市价单-深 / 沪期权
    #  或
    #  8 XTP_PRICE_LIMIT_OR_CANCEL期权限价申报FOK
    Fok = 5


# 买卖方向
class Side():
    Unknown = 0  # 无效
    Buy = 1  # 买
    Sell = 2  # 卖
    Lock = 12  # 锁仓  对应xtp的XTP_SIDE_FREEZE 12
    # 以下3个需要找到具体值定义
    # Unlock = 0 #解锁？ 1.0.0未写入文档
    # Exec = 0 #行权   1.0.0未写入文档
    # Drop = 0 #放弃行权？ 1.0.0未写入文档
    # 以下是alphax缺少的
    Purchase = 7  # 申购
    Pedemption = 8  # 赎回
    Split = 9  # 拆分
    Merge = 10  # 合并
    Cover = 11  # 备兑
    MarginTrade = 21  # 融资买入
    ShortSell = 22  # 融券卖出
    RepayMargin = 23  # 卖券还款
    RepayStock = 24  # 买券还券
    StockRepayStock = 26  # 现券还券
    SurstkTrans = 27  # 余券划转
    GrtstkTransin = 28  # 担保品转入
    GrtstkTransout = 29  # 担保品转出


# 开平标志
class Offset():
    Open = 0  # 开  alphax:0  xtp:1 XTP_POSITION_EFFECT_OPEN
    Close = 1  # 平 alphax:1  xtp:2 XTP_POSITION_EFFECT_CLOSE
    CloseToday = 2  # 平今  alphax:2 xtp:4 XTP_POSITION_EFFECT_CLOSETODAY
    CloseYesterday = 3  # 平昨 alphax:3 xtp:5 XTP_POSITION_EFFECT_CLOSEYESTERDAY
    # 以下为alphax缺少的
    ForceClose = 13  # 强平  xtp:3 XTP_POSITION_EFFECT_FORCECLOSE
    ForceOff = 6  # 强减  xtp:6 XTP_POSITION_EFFECT_FORCEOFF
    LocalForceClose = 7  # 本地强平  xtp:7 XTP_POSITION_EFFECT_LOCALFORCECLOSE
    CreditForceCover = 8  # 信用业务追保强平 xtp:8 XTP_POSITION_EFFECT_CREDIT_FORCE_COVER
    CreditForceClear = 9  # 信用业务清偿强平 xtp:9 XTP_POSITION_EFFECT_CREDIT_FORCE_CLEAR
    CreditForceDebt = 10  # 信用业务合约到期强平 xtp:10 XTP_POSITION_EFFECT_CREDIT_FORCE_DEBT
    CreditForceUncond = 11  # 信用业务清偿强平 xtp:11 XTP_POSITION_EFFECT_CREDIT_FORCE_UNCOND
    Unknown = 12  # 未知 xtp:12 XTP_POSITION_EFFECT_UNKNOWN
    Init = 100  # 初始值或未知值开平标识，现货适用  对应xtp:0 XTP_POSITION_EFFECT_INIT


class BusinessType():
    CASH = 0  # 普通股票
    REPO = 2  # 国债逆回购
    ETF = 3  # ETF申赎
    MARGIN= 4 # 融资融券
    Unknown= 13


# 持仓方向 多空  对应xtp的XTP_POSITION_DIRECTION_TYPE
class Direction():
    Long = 0  # 多 xtp:1 XTP_POSITION_DIRECTION_LONG
    Short = 1  # 空 xtp:2 XTP_POSITION_DIRECTION_SHORT
    # 以下为alphax缺少的
    Net = 2  # 净 xtp:0 XTP_POSITION_DIRECTION_NET
    Covered = 3  # 备兑 xtp:3 XTP_POSITION_DIRECTION_COVERED


# 委托状态
class OrderStatus():
    Unknown = 0  # 未知(xtp:8 XTP_ORDER_STATUS_UNKNOWN）
    Submitted = 1  # 已提交(对应xtp:0 XTP_ORDER_STATUS_INIT初始化）
    Pending = 2  # 等待(对应xtp =5 XTP_ORDER_STATUS_NOTRADEQUEUEING未成交）
    Cancelled = 3  # 已撤单(xtp:6 XTP_ORDER_STATUS_CANCELED已撤单)
    Error = 4  # 错误（对应xtp:7 XTP_ORDER_STATUS_REJECTED拒单）
    Filled = 5  # 已成交（对应xtp:1 XTP_ORDER_STATUS_ALLTRADED全部成交）
    PartialFilledNotActive = 6  # 部成部撤（xtp:3 XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING部分撤单）
    PartialFilledActive = 7  # 部分成交（对应xtp:2 XTP_ORDER_STATUS_PARTTRADEDQUEUEING部分成交）


# 成交量条件
class VolumeCondition():
    Any = 0  # 任何数量 == 对成交数量不做要求  对应ctp:'1' THOST_FTDC_VC_AV
    Min = 1  # 最小数量 == 要求本次委托须成交的数量的最小值 对应ctp:'2' THOST_FTDC_VC_NV
    All = 2  # 全部数量 == 要求本次委托须全部成交 对应ctp:'3' THOST_FTDC_VC_CV


# 成交时间条件
class TimeCondition():
    IOC = 0  # 立即完成，否则撤销 对应ctp:'1' THOST_FTDC_VC_IOC
    GFS = 1  # 本节有效 对应ctp:'2' THOST_FTDC_VC_GFS
    GFD = 2  # 当日有效 对应ctp:'3' THOST_FTDC_VC_GFD
    # 以下为alphax缺少但ctp有的
    GTD = 3  # 指定日期前有效  对应ctp:'4' THOST_FTDC_VC_GTD
    GTC = 4  # 撤销前有效  对应ctp:'5' THOST_FTDC_VC_GTC
    GFA = 5  # 集合竞价有效  对应ctp:'6' THOST_FTDC_VC_GFA


# 账号类型 对应XTP_ACCOUNT_TYPE
class AccountType():
    Stock = 0  # 普通账户  xtp:0 XTP_ACCOUNT_NORMAL普通账户
    Credit = 1  # 信用账户 xtp:1 XTP_ACCOUNT_CREDIT信用账户
    Future = 2  # 期货账户
    # 以下为alphax缺少：
    Derive = 3  # 期权衍生品账户 xtp:2 XTP_ACCOUNT_DERIVE衍生品账户
    Unknown = 4  # 未知  xtp:4 XTP_ACCOUNT_UNKNOWN


# 策略平台类型  Smart私有的定义
class StrategyPlatformType():
    Front = "front"  # 客户端直接运行的js前端策略
    AlphaX = "alphax"  # AlphaX即功夫
    Algo = "algo"  # 算法平台
    ProgramTrade = "programTrade"  # 程序化交易
    Spec = "spec"  # 特定平台 按ProgramTrade相同的逻辑处理  1.0.0未写入文档
    FrontPy = "frontpy" # 客户端python策略类型


# ETF替代类型
class ETFReplaceType():
    class ERT_CASH_FORBIDDEN():
        name = "禁止现金替代"
        i = 0

    class ERT_CASH_OPTIONAL():
        name = "可以现金替代"
        i = 1

    class ERT_CASH_MUST():
        name = "必须现金替代"
        i = 2

    class ERT_CASH_RECOMPUTE_INTER_SZ():
        name = "深市退补现金替代"
        i = 3

    class ERT_CASH_MUST_INTER_SZ():
        name = "深市必须现金替代"
        i = 4

    class ERT_CASH_RECOMPUTE_INTER_OTHER():
        name = "非沪深市场成分证券退补现金替代"
        i = 5

    class ERT_CASH_MUST_INTER_OTHER():
        name = "表示非沪深市场成份证券必须现金替代"
        i = 6

    class EPT_INVALID():
        name = "无效值"
        i = 7

    


class QuotePositionType():
    P = "P"  # 最新价
    S1 = "S1"  # 卖一价
    S2 = "S2"  # 卖二价
    S3 = "S3"  # 卖三价
    S4 = "S4"  # 卖四价
    S5 = "S5"  # 卖五价
    B1 = "B1"  # 买一价
    B2 = "B2"  # 买二价
    B3 = "B3"  # 买三价
    B4 = "B4"  # 买四价
    B5 = "B5"  # 买五价
    H = "H"  # 涨停价
    L = "L"  # 跌停价


'''
 合约信息（证券信息）
 * 证券的静态信息
 *  属性	                    类型	    说明              对应smart字段
 *  instrument_id	        String	合约ID(证券代码)   ticker
 *  instrument_name         String  证券名称     name
 *  instrument_type         Number	证券类型          securityType
 *  exchange_id	            String	交易所ID
 *  exchange_id_name        String  交易所名称
 *  xtp_market_type	        String	xtp市场类型
 *  name_py	                String	名称拼音首字母     namePy
 *
 *  price_tick	            Number	最小价格变动单位   priceTick
 *  precision	            Number	最小价格变动单位精度（小数点后位数）
 *
 *  pre_close_price	        Number	昨收价            preClosePrice
 *  upper_limit_price	    Number	涨停价            upperLimitPrice
 *  lower_limit_price	    Number	跌停价            lowerLimitPrice
 *
 *  buy_volume_unit	        Number	弃用 最小买入数量       bidQtyUnit
 *  sell_volume_unit	    Number	弃用 最小卖出数量       askQtyUnit
 *
 *  bid_volume_unit	        Number	限价买单位       bidQtyUnit
 *  ask_volume_unit	        Number	限价卖单位       askQtyUnit
 *  bid_upper_limit_volume	Number	限价买上限       bidQtyUpperLimit
 *  bid_lower_limit_volume	Number	限价买下限       bidQtyLowerLimit
 *  ask_upper_limit_volume	Number	限价卖上限       askQtyUpperLimit
 *  ask_upper_limit_volume	Number	限价卖下限       askQtyLowerLimit
 *
 *  market_bid_volume_unit	Number	市价买单位       marketBidQtyUnit
 *  market_ask_volume_unit	Number	市价卖单位       marketAskQtyUnit
 *  market_bid_upper_limit_volume	Number	市价买上限       marketBidQtyUpperLimit
 *  market_bid_lower_limit_volume	Number	市价买下限       marketBidQtyLowerLimit
 *  market_ask_upper_limit_volume	Number	市价卖上限       marketAskQtyUpperLimit
 *  market_ask_upper_limit_volume	Number	市价卖下限       marketAskQtyLowerLimit
 *
 *  kw                      String  证券名称关键词     name
'''


class Instrument:
    def __init__(self):
        self.instrument_id = None  # 合约ID(证券代码) ticker
        self.instrument_name = ""  # 证券名称
        self.instrument_type = None  # 证券类型 InstrumentType枚举值  对应smart的securityType
        self.instrument_type_ext = None  # 用于标识具体的证券类型
        self.exchange_id = Exchange.Unknown  # 交易所ID "SZE"
        self.exchange_id_name = None  # 交易所名称
        self.xtp_market_type = None  # 市场ID "XTP_MKT_SZ_A"
        self.name_py = None  # 名称拼音首字母 namePy
        self.price_tick = None  # 最小价格变动单位 priceTick 0.01
        self.precision = None  # 最小价格变动单位精度（小数点后位数） precision
        self.buy_volume_unit = None  # 弃用 最小买入数量 bidQtyUnit 100
        self.sell_volume_unit = None  # 弃用 最小卖出数量 askQtyUnit
        self.bid_volume_unit = None  # 限价买单位 bidQtyUnit
        self.ask_volume_unit = None  # 限价卖单位 askQtyUnit
        self.bid_upper_limit_volume = None  # 限价买上限 bidQtyUpperLimit
        self.bid_lower_limit_volume = None  # 限价买下限 bidQtyLowerLimit
        self.ask_upper_limit_volume = None  # 限价卖上限 askQtyUpperLimit
        self.ask_lower_limit_volume = None  # 限价卖下限 askQtyLowerLimit
        self.market_bid_volume_unit = None  # 市价买单位 marketBidQtyUnit
        self.market_ask_volume_unit = None  # 市价卖单位 marketAskQtyUnit
        self.market_bid_upper_limit_volume = None  # 市价买上限 marketBidQtyUpperLimit
        self.market_bid_lower_limit_volume = None  # 市价买下限 marketBidQtyLowerLimit
        self.market_ask_upper_limit_volume = None  # 市价卖上限 marketAskQtyUpperLimit
        self.market_ask_lower_limit_volume = None  # 市价卖下限 marketAskQtyLowerLimit
        self.pre_close_price = None  # 昨收价 preClosePrice
        self.upper_limit_price = None  # 涨停价 upperLimitPrice
        self.lower_limit_price = None  # 跌停价 lowerLimitPrice
        self.is_registration = None  # 是否注册制 isRegistration
        self.kw = None  # keyword 证券名称删除其中的空格 转换为半角 搜索证券名称模糊匹配使用
        self.code = None  # 证券代码.交易所标识,600000.SH,000001.SZ
        

# 北交所静态行情信息
class NQInstrument(Instrument):
    def __init__(self):
        # 证券基础字段参见Instrument
        super().__init__()


# ETF配方表对象
class ETF(Instrument):
    def __init__(self):
        # 证券基础字段参见Instrument
        super().__init__()
        self.cash_component = None  # T-1日现金差额
        self.estimate_amount = None  # T日预估现金余额
        self.max_cash_ratio = None  # 现金替代比率上限
        self.net_value = None  # T-1日基金份额净值
        self.redemption_status = None  # 基金当天赎回状态
        self.total_amount = None  # 最小申赎单位净值
        self.unit = None  # 最小申购赎回单位
        self.basket = []  # 成分股篮子列表

# 可转债正股对象
class ConvertableBond(Instrument):
    def __init__(self):
        # 证券基础字段参见Instrument
        super().__init__()
        self.qtyMax = None # 最大可转数量
        self.qtyMin = None # 最小可转数量
        self.swapFlag = None # 是否可转
        self.swapPrice = None # 转换价格
        self.underlyingTicker = None # 正股代码
        self.unit = None # 转换单位


# ETF成分股对象
class ETFCompoment(Instrument):
    def __init__(self):
        # 证券基础字段参见Instrument
        super().__init__()
        self.amount = None  # 替代金额
        self.creation_amount = None  # 溢价替代金额
        self.creation_premium_ratio = None  # 溢价比例
        self.premium_ratio = None  # 溢价比例
        self.quantity = None  # 股票数量
        self.redemption_amount = None  # 折价替代金额
        self.redemption_discount_ratio = None  # 折价比例
        self.replace_type = None  # 现金替代类型 参考ETFReplaceType
        self.ticker = None  # 申赎代码如：510501
        self.creation_amount = None  # 申购现金替代金额
        self.redemption_amount = None  # 赎回现金替代金额
        


# 新股对象
class IPO(Instrument):
    def __init__(self):
        # 证券基础字段参见Instrument
        super().__init__()
        self.price = None  # 价格
        self.qty_upper_limit = None  # 持仓数量
        self.instrument_id = None  # 股票代码
        self.instrument_name = None  # 股票名称
        self.instrument_type = None  # 股票类型
        self.unit = None  # 最小申购赎回单位
        


class ETFProfitParam:
    def __init__(self):
        self.instrument_id = None  # ETF的证券代码
        self.exchange_id = Exchange.Unknown  # ETF的交易所，参见Exchange
        self.profit_type = None  # 预期利润方向：dis|pre
        self.etf_price_range = None  # etf的盘口，参见QuotePositionType
        self.basket_price_range = None  # 股票篮的盘口，参见QuotePositionType
        


class ETFProfit:
    def __init__(self):
        self.instrument_id = None  # ETF的证券代码
        self.iopv = 0  # ETF的模拟净值
        self.iopv_buy = 0  # ETF的买模拟净值
        self.iopv_sale = 0  # ETF的卖模拟净值
        self.diopv = 0  # ETF的动态模拟净值
        self.dis_profit = 0  # ETF折价预期利润
        self.pre_profit = 0  # ETF溢价预期利润
        


# 账号资产对象 account.assets对象

class Assets:
    def __init__(self):
        self.banlance = 0   # 当前余额
        self.buying_power = 0   # 可用资金
        self.captial_asset = 0   # 资金资产
        self.deposit_withdraw = 0   # 当天出入金
        self.force_freeze_amount = 0   # 强锁资金
        self.frozen_exec_cash = 0   # 行权冻结资金
        self.frozen_exec_fee = 0   # 行权费用
        self.frozen_margin = 0   # 冻结的保证金
        self.fund_buy_amount = 0   # 累计买入成交证券占用资金
        self.fund_buy_fee = 0   # 累计买入成交交易费用
        self.fund_sell_amount = 0   # 累计卖出成交证券所得资金
        self.fund_sell_fee = 0   # 累计卖出成交交易费用
        self.orig_banlance = 0   # 昨日余额
        self.pay_later = 0   # 垫付资金
        self.preadva_pay = 0   # 预垫付资金
        self.preferred_amount = 0   # 可取资金
        self.security_asset = 0   # 证券资产（保留字段，目前为0）
        self.total_asset = 0   # 总资产(=可用资金 + 持仓市值 + 预扣的资金)
        self.market_value = 0   # 持仓市值
        self.trade_netting = 0   # 当日交易资金轧差
        self.withholding_amount = 0   # XTP系统预扣的资金（包括购买卖股票时预扣的交易资金+预扣手续费）
        self.update_time = ''   # 最后更新时间 smart内部产生
        '''/***************以下为信用资产数据**************/'''
        self.all_asset= 0 #总资产（仅限信用业务）
        self.all_debt= 0 #总负债（仅限信用业务）
        self.guaranty= 0 #两融保证金可用数（仅限信用业务）
        self.line_of_credit= 0 #两融授信额度（仅限信用业务）
        self.maintenance_ratio= 0 #维持担保品比例（仅限信用业务）
        self.remain_amount= 0 #信用账户待还资金（仅限信用业务）
        self.security_interest= 0 #融券合约利息（仅限信用业务）
        self.cash_remain_amt= 0 #融资合约金额（仅限信用业务）
        self.cash_interest= 0 #融资合约利息（仅限信用业务）
        self.extras_money= 0 #融券卖出所得购买货币基金占用金额（仅限信用业务）

# 策略账簿对象 即strategy.book对象

# 持仓对象
class Position:
    def __init__(self):
        self.instrument_id = None  # 合约ID（证券代码)
        self.instrument_name = ""  # 证券名称
        # self.instrument_type = InstrumentType.Unknown  # 合约类型  alphax有但xtp目前缺少 需要去静态信息关联 可能影响性能  可以空着
        self.exchange_id = Exchange.Unknown  # 交易所id
        self.exchange_id_name = "未知"  # 交易所名称
        self.direction = None  # 持仓方向
        self.direction_name = ""  # 持仓方向名称
        self.name_py = ""  # 拼音首字母  如"安诺其"为"anq"  alphax缺少
        self.volume = 0  # 持仓量
        self.sellable_volume = 0  # 可卖持仓  alphax缺少
        self.position_cost_price = 0  # 持仓成本 profitPrice
        self.profit_price = 0 #盈亏成本
        self.last_price = 0  # 最新价
        self.market_value = 0  # 市值
        self.unrealized_pnl = 0  # 浮动盈亏（保留字段,未计算） 未实现盈亏
        self.yesterday_volume = 0  # 昨日持仓
        self.purchase_redeemable_qty = 0  # 今日申购赎回数量 alphax缺少
        self.executable_option = 0  # 可行权合约 alphax缺少
        # self.lockable_position = 0  # 可锁定标的 alphax缺少
        self.executable_underlying = 0  # 可行权标的 alphax缺少
        self.locked_position = 0  # 已锁定标的 alphax缺少
        self.usable_locked_position = 0  # 可用已锁定标的 alphax缺少
        self.xtp_market_type = "XTP_EXCHANGE_UNKNOWN"  # 交易市场
        self.xtp_market_name = "未知"  # 交易市场名称
        self._instrument_id_direction = ""  # 内部使用  代码+持仓方向的联合主键 如"300067_XTP_POSITION_DIRECTION_NET"
        self.code = None  # 证券代码.交易所标识,600000.SH,000001.SZ
        


# 账户委托确认、策略委托确认对象
class Order:
    def __init__(self):
        self.rcv_time = None  # String	数据接收时间                                              "20200608140053830"
        self.order_id = None  # String	订单ID（对应xtpid）                    orderXtpId         "36934130021173201"
        self.source_order_id = None
        self.insert_time = None  # String	'XTP_MKT_UNKNOWN''XTP_MKT_UNKNOWN'委托写入时间                           insertTime         "20200608140053830"
        self.update_time = None  # String	委托更新时间                           updateTime         "20200608140053830"
        self.trading_day = None  # String	交易日                                insertTime中截取    "20200608"
        self.instrument_id = None  # String	合约ID（证券代码）                     ticker              "600000"
        self.exchange_id = Exchange.Unknown  # String	交易所ID                              xtpMarketType转换   "SSE"
        self.account_id = None  # String	账号ID（资金账号）                     userName            "10912133333344"
        self.client_id = None  # String	用户自定义编号                         orderClientId
        self.instrument_type = None  # Number	合约类型                              xtpBusinessType转换  InstrumentType.Stock
        self.limit_price = None  # Number	价格                                  price               10.23
        self.frozen_price = None  # Number	冻结价格（市价单冻结价格为0.0）          price               10.23
        self.volume = None  # Number	数量                                  quantity            100
        self.volume_traded = None  # Number	成交数量                              qty_traded           0
        self.volume_left = None  # Number	剩余数量                              qty_left             100
        self.tax = None  # Number	税                                   todo:
        self.commission = None  # Number	手续费                                todo:
        self.status = None  # Number	订单状态                              order_status
        self.error_id = None  # Number	错误ID                               xtpErrorId
        self.error_msg = None  # String	错误信息                              xtpErrorMsg
        self.side = Side.Unknown  # Number	买卖方向                              xtpSideType
        self.offset = Offset.Unknown  # Number	开平方向                              xtpPositionEffectType
        self.price_type = None  # Number	价格类型                              xtpPriceType
        self.volume_condition = None  # Number	成交量类型
        self.time_condition = None  # Number	成交时间类型
        self.parent_order_id = None  # String	母单ID                               #篮子为runtimeId一个篮子一次交易一个值   etf套利为etf标签页期间是一个值  其他取alphax或smartserver传的      "6a1071e1-a94d-11ea-810c-4b25bab2cda3"
        self.code = None  # 证券代码.交易所标识,600000.SH,000001.SZ

        self.traffic = None  # String  业务渠道标识                           business_type         "AlphaX"
        self.traffic_sub_id = None  # String  业务子标识，一般填策略名称               businessSubId         "网格交易"
        self.cancel_time = None  # String  撤单时间                              cancelTime            "20200608140053830"
        self.order_cancel_client_id = None  # String  撤单自定义编号                         orderCancelClientId   "0"
        self.order_cancel_xtp_id = None  # String  所撤原单的编号(原xtpid)                orderCancelXtpId      "0"
        self.instrument_name = None  # String  合约名称（证券名称）                    tickerName            "浦发银行"
        self.trade_amount = None  # Number  委托金额                              tradeAmount           0
        self.xtp_business_type = None  # String  xtp证券业务类型                        xtpBusinessType       "XTP_BUSINESS_TYPE_CASH"
        self.xtp_market_type = "XTP_MKT_UNKNOWN"  # String  xtp市场类型                            xtpMarketType         "XTP_MKT_SZ_A"

        # 以下为xtp的冗余字段，为了获取xtp的原值
        self.xtp_price_type = None  # String  xtp价格类型                            xtpPriceType          "XTP_PRICE_LIMIT"
        self.xtp_position_effect_type = None  # String xtp开平方向                  xtpPositionEffectType "XTP_POSITION_EFFECT_OPEN"
        self.xtp_side_type = None  # String  xtp交易方向                            xtpSideType           "XTP_SIDE_BUY"
        self.xtp_order_status = None  # String  xtp订单状态                            orderStatus           "XTP_ORDER_STATUS_INIT"

        # 以下为xtp和alphax枚举值翻译为中文的名称
        self.exchange_id_name = None  # String  交易所名称                                                  "上交所"
        self.instrument_type_name = None  # String  合约类型名称                                                "股票"
        self.status_name = None  # String  订单状态名称                                                "全部成交"
        self.side_name = None  # String  买卖方向名称                                                "买"
        self.offset_name = None  # String  开平方向名称                                                "开"
        self.price_type_name = None  # String  价格类型名称                                                "限价"
        self.xtp_business_type_name = None  # String  xtp证券业务类型名称                                          "现货"
        self.xtp_market_name = None  # String  xtp市场类型名称                                             "沪市"
        self.xtp_price_type_name = None  # String  xtp价格类型名称                                             "限价"
        self.xtp_position_effect_type_name = None  # String  xtp开平方向名称                                             "开"
        self.xtp_side_type_name = None  # String  xtp交易方向名称                                             "买"
        self.xtp_order_status_name = None  # String  xtp价格类型名称                                             "限价"
        self.volume_condition_name = None  # String  成交量类型名称                                              "任何数量" "最小数量" "全部数量"
        self.time_condition_name = None  # String  成交时间类型名称                                            "立即完成" "本节有效"  "当日有效" "指定日期前有效" "撤销前有效" "集合竞价有效"
        self.traffic_name = None  # String  业务渠道名称       
        self.business_type = "" #    下的类型                                         "策略"
        self.rowId = None
        


# 账户成交回报、策略成交回报对象
class Trade():
    def __init__(self):
        self.trade_id = None # String 成交唯一编号
        self.rcv_time = None  # String	数据接收时间                                              "20200608140053830"
        self.order_id = None  # String	订单ID（对应xtpid）                    orderXtpId         "36934130021173201"
        self.parent_order_id = None  # String	母单ID                               # runtimeId          "6a1071e1-a94d-11ea-810c-4b25bab2cda3"
        self.trade_time = None  # String	成交时间                              tradeTime          "20200608140053830"
        # self.trading_day = None  # String	交易日                                insertTime中截取    "20200608"
        self.instrument_id = None  # String	合约ID（证券代码）                     ticker              "600000"
        self.exchange_id = Exchange.Unknown  # String	交易所ID                              xtpMarketType转换   "SSE"
        self.account_id = None  # String	账号ID（资金账号）                     userName            "10912133333344"
        self.client_id = None  # String	用户自定义编号                         orderClientId
        self.instrument_type = None  # Number	合约类型                              xtpBusinessType转换  InstrumentType.Stock
        self.side = None  # Number	买卖方向                              xtpSideType
        self.offset = None  # Number	开平方向                              xtpPositionEffectType
        self.price = None  # Number	价格                                  price               10.23
        self.volume = None  # Number	数量                                  quantity            100
        self.tax = None  # Number	税                                   todo:
        self.commission = None  # Number	手续费                                todo:
        self.code = None  # 证券代码.交易所标识,600000.SH,000001.SZ

        self.traffic = None  # String  业务渠道标识                           business_type         "AlphaX"
        self.traffic_sub_id = None  # String  业务子标识，一般填策略名称               businessSubId         "网格交易"
        self.instrument_name = None  # String  合约名称（证券名称）                    tickerName            "浦发银行"
        self.trade_amount = None  # Number  委托金额                              tradeAmount           0
        self.xtp_business_type = None  # String  xtp证券业务类型                        xtpBusinessType       "XTP_BUSINESS_TYPE_CASH"
        self.xtp_market_type = "XTP_MKT_UNKNOWN"  # String  xtp市场类型                            xtpMarketType         "XTP_MKT_SZ_A"

        self.xtp_exec_id = None  # String  成交编号()                            execId                "15790"
        self.xtp_report_index = None  # String  成交序号()                            reportIndex           "6806"
        self.xtp_order_exch_id = None  # String  报单编号 –交易所单号，上交所为空，深交所有此字段 orderExchId     ""
        self.xtp_trade_type = None  # String  成交类型                              tradeType             "1" 代表XTP_TRDT_CASH 现金替代"
        self.xtp_branch_pbu = None  # String  交易所交易员代码                       branchPbu             "13688"

        # 以下为xtp的冗余字段，为了获取xtp的原值
        self.xtp_position_effect_type = None  # String xtp开平方向                  xtpPositionEffectType "XTP_POSITION_EFFECT_OPEN"
        self.xtp_side_type = None  # String  xtp交易方向                            xtpSideType           "XTP_SIDE_BUY"

        # 以下为xtp和alphax枚举值翻译为中文的名称
        self.exchange_id_name = None  # String  交易所名称                                                  "上交所"
        self.instrument_type_name = None  # String  合约类型名称                                                "股票"
        self.side_name = None  # String  买卖方向名称                                                "买"
        self.offset_name = None  # String  开平方向名称                                                "开"
        self.xtp_business_type_name = None  # String  xtp证券业务类型名称                                          "现货"
        self.xtp_market_name = None  # String  xtp市场类型名称                                             "沪市"
        self.xtp_position_effect_type_name = None  # String  xtp开平方向名称                                             "开"
        self.xtp_side_type_name = None  # String  xtp交易方向名称                                             "买"
        self.traffic_name = None  # String  业务渠道名称                                                "策略"
        self.xtp_trade_type_name = None  # String  成交类型名称     
        self.business_type = "" #    下的类型                                           "现金替代"
        self.rowId = None #String 仅用于内部标识


''' 行情信息
 *  属性	                    类型	    说明              对应xtp字段         对应上证云字段
 *  source_id	            String	柜台ID            xtp缺少
 *  trading_day	            String	交易日            xtp缺少
 *  rcv_time	            String	数据接收时间       xtp缺少
 *  data_time	            String	数据生成时间       dataTime
 *  instrument_id	        Number	合约ID            ticker
 *  exchange_id	            String	交易所            exchangeId
 *  instrument_type	        Number	合约类型          xtp缺少
 *  pre_close_price	        Number	昨收价            preClosePrice
 *  pre_settlement_price    Number	昨结价            xtp缺少
 *  last_price	            Number	最新价            lastPrice
 *  volume	                Number	成交数量          qty
 *  turnover	            Number	成交金额          turnover
 *  pre_open_interest	    Number	昨持仓量          xtp缺少
 *  open_interest	        Number	持仓量            xtp缺少
 *  open_price	            Number	今开盘            openPrice
 *  high_price	            Number	最高价            highPrice
 *  low_price	            Number	最低价            lowPrice
 *  upper_limit_price	    Number	涨停板价          upperLimitPrice
 *  lower_limit_price	    Number	跌停板价          lowerLimitPrice
 *  close_price	            Number	收盘价            closePrice
 *  settlement_price	    Number	结算价            xtp缺少
 *  bid_price	    list of Number	申买价            bid
 *  ask_price	    list of Number	申卖价            ask
 *  bid_volume	    list of Number	申买量            bidQty
 *  ask_volume	    list of Number	申卖量            askQty
 *  以下是alphax缺少的
 *  avg_price               Number  当日均价          avgPrice
 *  iopv                    Number  iopv             iopv
 *  instrument_status       String  证券状态          tickerStatus
 '''


class Quote():
    def __int__(self):
        self.source_id = None  # 柜台ID xtp缺少
        self.trading_day = None  # 交易日 xtp缺少
        self.rcv_time = None  # 数据接收时间 xtp缺少
        self.data_time = None  # 数据生成时间 dataTime
        self.instrument_id = None  # 合约ID ticker
        self.exchange_id = None  # 交易所 exchangeId XTP_EXCHANGE_SH
        self.instrument_type = None  # 合约类型 xtp缺少
        self.pre_close_price = None  # 昨收价 preClosePrice
        self.pre_settlement_price = None  # 昨结价 xtp缺少
        self.last_price = None  # 最新价 lastPrice
        self.volume = None  # 成交数量 qty
        self.turnover = None  # 成交金额 turnover
        self.pre_open_interest = None  # 昨持仓量 xtp缺少
        self.open_interest = None  # 持仓量 xtp缺少
        self.open_price = None  # 今开盘 openPrice
        self.high_price = None  # 最高价 highPrice
        self.low_price = None  # 最低价 lowPrice
        self.upper_limit_price = None  # 涨停板价 upperLimitPrice
        self.lower_limit_price = None  # 跌停板价 lowerLimitPrice
        self.close_price = None  # 收盘价 closePrice
        self.settlement_price = None  # 结算价 xtp缺少
        self.bid_price = None  # 申买价数组 如[11, 10.55, 10, 0, 0, 0, 0, 0, 0, 0] bid
        self.ask_price = None  # 申卖价数组 ask
        self.bid_volume = None  # 申买量数组 如[1000, 14700, 100, 0, 0, 0, 0, 0, 0, 0] bidQty
        self.ask_volume = None  # 申卖量数组 askQty
        self.code = None  # 证券代码.交易所标识,600000.SH,000001.SZ
        # 以下是alphax缺少的
        self.avg_price = None  # 当日均价 alphax缺少
        self.iopv = None  # iopv alphax缺少
        self.instrument_status = None  # 证券状态 如"E110    "详见xtp文档 alphax缺少

''' 指标bar行情信息
 *  属性	           示例值          类型	    说明   
    type               bar_1min        String   行情类型
    code               600000.SH       String   证券代码
    instrument_id      600000          String   证券编号   
    exchange_id        SSE             String   市场 SZE: 深圳、SSE: 上海
    high	           13.93	       Number	最高价
    low	               13.92	       Number	最低价
    open	           13.93	       Number	开盘价
    close	           13.93	       Number	收盘价
    num_trades	       162	           Number	bar内交易笔数
    datetime	       1678069560000   Number	bar 结束时间, 若计算9点30到9点31分钟线, 则值为9点31 毫秒值
    total_turnover	   1958218.0	   Number	bar内交易金额
    volumn	           140600	       Number	bar 内交易量
    createtime	       1678069560419   Number	bar计算时间
    turnover	       7.633250206E8   Number	截至目前总交易金额（来源XTP）
    trades_count	   39618	       Number	截至目前总交易笔数（来源XTP）
    qty	               54448665	       Number	截至目前总交易量（来源XTP）
 '''
class Bar():
    def __int__(self):
        self.type = None  # 类型 行情类型：bar_1min/macd_1min
        self.code = None  # 证券代码 例如600000.SH
        self.instrument_id = None  # 证券编号
        self.exchange_id = None  # 市场 SZE: 深圳、SSE: 上海
        self.trading_day = None # 交易日根据datetime计算
        self.source_id = None # 柜台ID 固定值xtp
        self.start_time = None  # 开始时间 datetime-1min   
        self.end_time = None  # 结束时间  datetime
        self.time_interval = None  # 时间间隔，例如：1 单位分钟
        self.period = None  # 周期，例如 1m、2d、3w
        self.high = None  # 最高价
        self.low = None  # 最低价
        self.open = None  # 开盘价
        self.close = None  # 收盘价
        self.volume = None  # 区间交易量
        self.start_volume = None  # 初始总交易量:qty-volume
        self.turnover = None  # 区间成交金额
        self.start_turnover = None  #初始总成交金额 total_turnover - turnover

        # self.num_trades = None  # bar内交易笔数
        # self.datetime = None  # bar 结束时间, 若计算9点30到9点31分钟线, 则值为9点31 毫秒值
        # self.total_turnover = None  # bar内交易金额
        # self.createtime = None  # bar计算时间
        # self.trades_count = None  # 截至目前总交易笔数（来源XTP）
        # self.qty = None  # 截至目前总交易量（来源XTP）


# 策略的状态 smart新增 （td和md也复用该状态）
class StrategyStatus():
    Unknown = "Unknown"  # 未知
    Starting = "Starting"  # 启动中  预留暂时无用
    Started = "Started"  # 启动完毕运行中
    Pause = "Pause"  # 暂停  预留暂时无用
    Stopping = "Stopping"  # 停止中  预留暂时无用
    Stopped = "Stopped"  # 已停止
    Errored = "Errored"  # 错误


# 向插件进程进行数据通信的成功与否代码 内部使用 （无需）未写入文档
class IPCRespCode():
    class SUCCESS():
        code = "0000"
        message = "成功"

    class ECOMM():  # 通用失败  如需自定义失败代码后面继续扩展
        code = "0001"
        message = "失败"


# 信用可融券头寸信息
class CreditTickerAssignInfo():
    def __int__(self):
        self.instrument_id = None  # 证券代码
        self.instrument_name = None  # 证券名称
        self.exchange_id = Exchange.Unknown  # 交易所id
        self.exchange_id_name = "未知"  # 交易所名称
        self.name_py = ""  # 拼音首字母  如"安诺其"为"anq"  alphax缺少
        self.left_volume = 0  # 剩余可融券数量
        self.frozen_volume = 0  # 冻结融券数量
        self.yesterday_volume = 0 #昨日日融券数量
        self.xtp_market_type = "XTP_EXCHANGE_UNKNOWN"  # xtp交易市场
        self.code = None  # 证券代码.交易所标识,600000.SH,000001.SZ

# 信用融资负债信息
class CreditDebtFinance():
    def __int__(self):
        self.debt_id = None  # 负债合约编号
        self.instrument_id = None  # 证券代码
        self.instrument_name = None  # 证券名称
        self.exchange_id = Exchange.Unknown  # 交易所id
        self.exchange_id_name = "未知"  # 交易所名称
        self.name_py = ""  # 拼音首字母  如"安诺其"为"anq"  alphax缺少
        self.xtp_market_type = None  #  xtp交易市场
        self.remain_amt = 0  # 未偿还金额
        self.remain_principal = 0  # 未偿还本金
        self.remain_interest = 0  # 未偿还利息
        self.debt_status = 0 #合约状态
        self.end_date = None #负债截止日期
        self.orig_end_date = None #负债原始截止日期
        self.order_xtp_id = None #负债订单编号
        self.order_date = None #委托日期
        self.extended = None #是否接收到展期
        self.code = None  # 证券代码.交易所标识,600000.SH,000001.SZ

# 信用融券负债信息
class CreditDebtSecurity():
    def __int__(self):
        self.debt_id = None  # 负债合约编号
        self.instrument_id = None  # 证券代码
        self.instrument_name = None  # 证券名称
        self.exchange_id = Exchange.Unknown  # 交易所id
        self.exchange_id_name = "未知"  # 交易所名称
        self.name_py = ""  # 拼音首字母  如"安诺其"为"anq"  alphax缺少
        self.xtp_market_type = None  #  xtp交易市场
        self.remain_interest = 0  # 未偿还利息
        self.remain_volume = 0 #未偿还融券数量
        self.due_right_volume = 0 #应偿还权益数量
        self.debt_status = 0 #合约状态
        self.end_date = None #负债截止日期
        self.orig_end_date = None #负债原始截止日期
        self.order_xtp_id = None #负债订单编号
        self.order_date = None #委托日期
        self.extended = None #是否接收到展期
        self.code = None  # 证券代码.交易所标识,600000.SH,000001.SZ

# 券源行情信息
class SourceQuoteInfo():
    def __int__(self):
        self.sno = None # 行情序号
        self.stk_code = None# 证券代码
        self.stk_name = None # 证券名称
        self.quotation_type = '0' # 行情类型 0：库存券源 1：意向券源 2：准库存券
        self.end_date = None # 到期日期
        self.term_rate = 0 # 费率 券源申请时:若为意向券需维护该字段,注：0.1即为10%
        self.lend_qty = 0 # 可出借数量
        self.reallend_qty = 0 # 发布出借数量
        self.match_qty = 0 # 已成交数量
        self.market = None # 交易市场
        self.term_code = None # 期限(天)
        self.lend_qty_des = None # 出借数量描述
        self.remark = None # 备注
        self.sys_date = None # 系统日期
        self.req_qty = 0 # 数量：券源申请时使用字段
        self.prepare_date = ""  # 筹券开始日期：券源申请时使用字段
        self.prepare_date_end = "" # 筹券结束日期：券源申请时使用字段
        self.error_msg = None # 错误信息

#getData信息类
class DataPageInfo():
    def __int__(self):        
        self.currentPage = None # 当前页码数
        self.data = None# 查询结果集
        self.pageSize = None # 每页记录数
        self.totalCount = None # 总记录数
        self.totalPage = None# 总页数
        
# #账户资产对象定义
# function Assets() {
#
#
# #策略账簿对象定义
# function Book() {
#


class RspError(Exception):
    NOT_SUPPORTED="9000"
    PARSE_ERROR="9999"
    SUCCESS="0000"
    ARGS_ERROR="9001"
    NOT_EXIST="9002"
    RUNTIME_ERROR="9003"

    def __init__(self, rsp):
        self.code = rsp.get("code")
        self.message = rsp.get("message")
        self.value = rsp
    def __str__(self):
        return repr(self.value)

class Type:
    # 枚举值
    Source = Source
    Exchange = Exchange
    InstrumentType = InstrumentType
    # ExecType = ExecType
    PriceType = PriceType
    Side = Side
    Offset = Offset
    BusinessType = BusinessType
    Direction = Direction
    OrderStatus = OrderStatus
    VolumeCondition = VolumeCondition
    TimeCondition = TimeCondition
    AccountType = AccountType
    StrategyPlatformType = StrategyPlatformType
    StrategyStatus = StrategyStatus
    IPCRespCode = IPCRespCode
    OutFormat = OutFormat
    # 类定义
    ETF = ETF
    ETFCompoment = ETFCompoment
    Assets = Assets
    Position = Position
    Order = Order
    Trade = Trade
    Quote = Quote
    Bar = Bar
    Instrument = Instrument
    NQInstrument = NQInstrument
    # Round = Round
    IPO = IPO
    ETFProfit = ETFProfit
    SourceQuoteInfo = SourceQuoteInfo
    DataPageInfo = DataPageInfo
    ConvertableBond = ConvertableBond

