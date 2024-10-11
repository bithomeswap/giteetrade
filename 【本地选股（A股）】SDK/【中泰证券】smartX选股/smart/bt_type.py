


class BtInstrumentType() :
    BtInstrumentTypeUnknown = 0       #未知
    BtInstrumentTypeStock = 1         #普通股票
    BtInstrumentTypeFuture = 2        #期货
    BtInstrumentTypeBond = 3          #债券
    BtInstrumentTypeStockOption = 4   #股票期权
    BtInstrumentTypeFund = 5          #基金
    BtInstrumentTypeTechStock = 6     #科创板股票
    BtInstrumentTypeIndex = 7         #指数
    BtInstrumentTypeRepo = 8


class BtOrderStatus() :
    BtOrderStatusUnknown = 0
    BtOrderStatusSubmitted = 1
    BtOrderStatusPending = 2
    BtOrderStatusCancelled = 3
    BtOrderStatusError = 4
    BtOrderStatusFilled = 5
    BtOrderStatusPartialFilledNotActive = 6
    BtOrderStatusPartialFilledActive = 7


class BtSide() :
	BtSideBuy = 0
	BtSideSell =1
	BtSideLock = 2
	BtSideUnlock = 3
	BtSideExec = 4
	BtSideDrop = 5
	BtSidePurchase = 107    # 申购
	BtSideRedemption = 108  # 赎回
	BtSideSplit = 109       # 拆分
	BtSideMerge = 110
	BtSideCover = 111       # 备兑
	BtSideFreeze = 112      # 锁定（对应开平标识为开）/解锁（对应开平标识为平）
	BtSideMarginTrade = 113 # 融资买入
	BtSideShortSell = 114   # 融券卖出
	BtSideRepayMargin = 115 # 卖券还款
	BtSideRepayStock = 116  # 买券还券
	# CashRepayMargin,// 现金还款,这个字段应该在XTP中不再使用了
	BtSideStockRepayStock = 117 # 现券还券
	BtSideUnknown = 118        # 未知或者无效买卖方向


class BtInstrumentFullType() :
    BtInstrumentFullTypeUnknown = 0                   # 未知/其他
    BtInstrumentFullTypeMainBoard = 1                 # 主板股票
    BtInstrumentFullTypeSecondBoard = 2               # 中小板股票
    BtInstrumentFullTypeStartupBoard = 3              # 创业板股票
    BtInstrumentFullTypeIndex = 4                     # 指数
    BtInstrumentFullTypeTechBoard = 5                 # 科创板股票(上海)
    BtInstrumentFullTypeStateBond = 6                 # 国债
    BtInstrumentFullTypeEnterpriceBond = 7            # 企业债
    BtInstrumentFullTypeCompaneyBond = 8              # 公司债
    BtInstrumentFullTypeConvertableBond = 9           # 转换债券
    BtInstrumentFullTypeNationalBondReverseRepo = 13  # 国债逆回购
    BtInstrumentFullTypeETFSingleMarketStock = 15     # 本市场股票 ETF
    BtInstrumentFullTypeETFInterMarketStock = 16      # 跨市场股票 ETF
    BtInstrumentFullTypeETFCrossBorderStock = 17      # 跨境股票 ETF
    BtInstrumentFullTypeETFSingleMarketBond = 18      # 本市场实物债券 ETF
    BtInstrumentFullTypeETFSecurityCashBond = 19      # 现金债券
    BtInstrumentFullTypeETFGold = 20                  # 黄金 ETF
    BtInstrumentFullTypeETFCommondityFutures = 23     # 商品期货ETF
    BtInstrumentFullTypeStructuredFundChild = 25      # 分级基金子基金
    BtInstrumentFullTypeSZSERecreationFund = 27,      # 深交所仅申赎基金
    BtInstrumentFullTypeStockOption = 30,             # 个股期权
    BtInstrumentFullTypeETFOption = 31,               # ETF期权
    BtInstrumentFullTypeAllotment = 101,              # 配股
    BtInstrumentFullTypeMonetaryFundSHcr = 111,       # 上交所申赎型货币基金
    BtInstrumentFullTypeMonetaryFundSHtr = 112,       # 上交所交易型货币基金
    BtInstrumentFullTypeMonetaryFundSZ = 113          # 深交所货币基金


class CommandType() :
    Unknown = -1
    InsertOrder = 0
    InsertOrderRsp = 1
    CancelOrder = 2
    CancelOrderRsp = 3
    SubBar = 4
    SubBarRsp = 5
    SubTick = 6
    SubTickRsp = 7
    GetStaticQuotes = 8
    GetStaticQuotesRsp = 9
    Config = 10
    Next = 11
    DataRsp = 12
    NextDay = 13
    End = 14
    SubBarAll = 15
    SubBarAllRsp = 16
    TimerReq = 17
    TimerRes = 18
    UnSubBar = 19
    UnSubBarRsp = 20
    UnSubTick = 21
    UnSubTickRsp = 22
    SubTickAll = 23
    SubTickAllRsp = 24
    Error =- 2
    Exit =- 3

class BtDataType() :
    Unknown =-1,
    ReqMsg = 0
    RspMsg = 1
    StaticQuotes = 2
    Tick = 3
    Bar = 4
    Order = 5
    Entrust = 6
    Trade = 7
    Timer = 8

