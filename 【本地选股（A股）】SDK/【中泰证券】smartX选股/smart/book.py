from .bookpyd import Book as BookBase,OrderInput,Order as BookOrder,Trade as BookTrade,constants,utils as bookUtils
from typing import Dict
from .utils import *
import uuid
import os
from datetime import datetime
import logging
logger = logging.getLogger()

_PriceType = constants.PriceType
_Side = constants.Side
_Offset = constants.Offset
_InstrumentType = constants.InstrumentType
_BusinessType = constants.BusinessType
_OrderStatus = constants.OrderStatus


#####对应的KF的枚举值#######
PRICE_TYPE_BOOK = {
    0:_PriceType.UnKnown,#Unknown
    1:_PriceType.Limit,#Limit
    2:_PriceType.Any,#Any
    4:_PriceType.FakBest5,#FakBest5
    6:_PriceType.ForwardBest,#ForwardBest
    3:_PriceType.ReverseBest,#ReverseBest
    2:_PriceType.Fak,#Fak
    5:_PriceType.Fok,#Fok
}


SIDE_BOOK = {
        1:_Side.Buy,#Buy买
        2:_Side.Sell,#Sell卖
        12:_Side.Lock,#Lock锁定(功夫原生)Freeze锁定（对应开平标识为开）/解锁（对应开平标识为平）
        7:_Side.Purchase,# Purchase申购
        8:_Side.Redemption,# Redemption赎回
        9:_Side.Split,# Split拆分
        10:_Side.Merge,# Merge合并
        11:_Side.Cover,# Cover备兑
        21:_Side.MarginTrade,# MarginTrade融资买入
        22:_Side.ShortSell,# ShortSell融券卖出
        23:_Side.RepayMargin,# RepayMargin卖券还款
        24:_Side.RepayStock,# RepayStock买券还券
        26:_Side.StockRepayStock,# StockRepayStock现券还券
        0:_Side.Unknown # Unknown未知或者无效买卖方向
}


OFFSET_BOOK = {
    12: _Offset.Unknown,#Unknown
    100: _Offset.Init,#Init
    0: _Offset.Open,#Open
    1: _Offset.Close,#Close
    2: _Offset.CloseToday,#CloseToday
    3: _Offset.CloseYesterday,#CloseYesterday
    13: _Offset.ForceClose,#ForceClose
    6: _Offset.ForceOff,#ForceOff
    7: _Offset.LocalForceClose,#LocalForceClose
    8: _Offset.CreditForceCover,#CreditForceCover
    9: _Offset.CreditForceClear,#CreditForceClear
    10: _Offset.CreditForceDebt,#CreditForceDebt
    11 : _Offset.CreditForceUncond #CreditForceUncond
}


BUSINESS_TYPE_BOOK = {
    "XTP_BUSINESS_TYPE_CASH":_BusinessType.CASH, #CASH<普通股票业务（股票买卖，ETF买卖等）
                                        #1IPOS<新股申购业务（对应的price type需选择限价类型）
    "XTP_BUSINESS_TYPE_REPO":_BusinessType.REPO, #REPO<回购业务 ( 对应的price type填为限价，side填为卖 )
    "XTP_BUSINESS_TYPE_ETF":_BusinessType.ETF, #ETF<ETF申赎业务
    "XTP_BUSINESS_TYPE_MARGIN":_BusinessType.MARGIN, #MARGIN<融资融券业务
    # DESIGNATION,                         #<转托管（未支持）
    # ALLOTMENT,                           #<配股业务（对应的price type需选择限价类型,side填为买）
    # STRUCTURED_FUND_PURCHASE_REDEMPTION, #<分级基金申赎业务
    # STRUCTURED_FUND_SPLIT_MERGE,         #<分级基金拆分合并业务
    # MONEY_FUND,                          #<货币基金业务（暂未支持）
    # OPTION,                              #<期权业务
    # EXECUTE,                             #<行权
    # FREEZE,                              #<锁定解锁，暂不支持
    # OPTION_COMBINE,                      #<期权组合策略 组合和拆分业务
    # EXECUTE_COMBINE,                     #<期权行权合并业务
    # BOND_SWAP_STOCK,                     #<债转股业务
    "XTP_BUSINESS_TYPE_UNKNOWN":_BusinessType.UNKNOWN #UNKNOWN<未知类型
}


INSTRUMENT_TYPE_BOOK = {
    0:_InstrumentType.Unknown, #Unknown<未知
    1:_InstrumentType.Stock, #Stock<普通股票
    2:_InstrumentType.Future, #Future<期货
    3:_InstrumentType.Bond, #Bond<债券
    4:_InstrumentType.StockOption, #StockOption<股票期权
    6:_InstrumentType.Fund, #Fund<基金
    # :6, #TechStock<科创板股票
    5:_InstrumentType.Index, #Index<指数
    # 0:8  #Repo<回购
}

ORDER_STATUS_BOOK = {
    OrderStatus.Submitted:_OrderStatus.Submitted,
    OrderStatus.Pending:_OrderStatus.Pending,
    OrderStatus.Cancelled:_OrderStatus.Cancelled,
    OrderStatus.Error:_OrderStatus.Error,
    OrderStatus.Filled:_OrderStatus.Filled,
    OrderStatus.PartialFilledNotActive:_OrderStatus.PartialFilledNotActive,
    OrderStatus.PartialFilledActive:_OrderStatus.PartialFilledActive,
    OrderStatus.Unknown:_OrderStatus.Unknown
}

############################################
'''   
* 转换smart Order到Book Order
* @param    xtpOrder Dict xtp委托数据
* @param    isInput bool  是否是下委托单数据

'''
def convertOrderInputFromSmartToBook(xtpOrder:Dict = None):
    input = OrderInput()
    try:
        xtpBusinessType = xtpOrder.get('xtpBusinessType') # str
        xtpMarketType = xtpOrder.get('xtpMarketType') #str
        xtpPriceType = xtpOrder.get('xtpPriceType') #str
        xtpSideType = xtpOrder.get('xtpSideType') #str
        xtpPositionEffectType = xtpOrder.get('xtpPositionEffectType')#str
        rowId = xtpOrder.get("rowId")

        xtpBusinessType = dataTypeToXTPKey(xtpBusinessType,"XTP_BUSINESS_TYPE") #int->str
        xtpMarketType = dataTypeToXTPKey(xtpMarketType,"XTP_MARKET_TYPE") #int->str
        xtpPriceType = dataTypeToXTPKey(xtpPriceType,"XTP_PRICE_TYPE") #int->str
        xtpSideType = dataTypeToXTPKey(xtpSideType,"XTP_SIDE_TYPE") #int->str
        xtpPositionEffectType = dataTypeToXTPKey(xtpOrder.get('offset'),"XTP_POSITION_EFFECT_TYPE") #int->str

        price = xtpOrder.get('price',0)
        if(type(price) == str):
            price = float(price)

        input.instrument_id = xtpOrder.get('ticker',"")
        input.exchange_id = convertExchangeIdFromxtpMarketType(xtpMarketType)
        input.account_id = str(xtpOrder.get('userName',""))
        input.instrument_type = INSTRUMENT_TYPE_BOOK.get(getInstrumentType(input.instrument_id,input.exchange_id),_InstrumentType.Unknown) 
        input.limit_price = price
        input.frozen_price = price
        input.volume = xtpOrder.get('quantity',0)
        input.price_type = PRICE_TYPE_BOOK.get(convertPriceType(xtpPriceType),_PriceType.UnKnown)
        input.side = SIDE_BOOK.get(convertSide(xtpSideType),_Side.Unknown)
        input.offset = OFFSET_BOOK.get(convertOffset(xtpPositionEffectType),_Offset.Unknown)
        input.business_type = BUSINESS_TYPE_BOOK.get(xtpBusinessType,_BusinessType.UNKNOWN) 
        input.order_id = int(rowId) #rowId代表order_id

        # input.turns = 0 # xtpOrder.get("runtimeId",0) #同一批委托的编号

    except Exception as err:
        logger.error(err,exc_info=True, stack_info=True)
        input = None

    return input

'''   
* 转换smart Order到Book Order
* @param    xtpOrder Dict xtp委托数据
* @param    isInput bool  是否是下委托单数据

'''
def convertOrderFromSmartToBook(order:Order = None):
    bookOrder = BookOrder()
    try:
        rowId = 0
        if order.rowId and order.rowId.isdigit():
            rowId = order.rowId
        else:
            return None

        insertTime = order.insert_time

        bookOrder.instrument_id = order.instrument_id
        bookOrder.exchange_id = order.exchange_id
        bookOrder.account_id = order.account_id
        bookOrder.instrument_type = INSTRUMENT_TYPE_BOOK.get(order.instrument_type,_InstrumentType.Unknown) 
        bookOrder.limit_price = order.limit_price
        bookOrder.frozen_price = order.frozen_price
        bookOrder.volume = order.volume
        bookOrder.price_type = PRICE_TYPE_BOOK.get(order.price_type,_PriceType.UnKnown)
        bookOrder.side = SIDE_BOOK.get(order.side,_Side.Unknown)
        bookOrder.offset = OFFSET_BOOK.get(order.offset,_Offset.Unknown)
        bookOrder.business_type = BUSINESS_TYPE_BOOK.get(order.xtp_business_type,_BusinessType.UNKNOWN) 
        bookOrder.order_id =  int(rowId)   #  #rowId用于book的order编号
        bookOrder.external_order_id = int(order.order_id)
        bookOrder.volume_traded = order.volume_traded
        bookOrder.volume_left = order.volume_left
        bookOrder.amount_traded = order.trade_amount
        bookOrder.status = ORDER_STATUS_BOOK.get(order.status,_OrderStatus.Unknown) #OrderStatus
        bookOrder.trading_day = str(insertTime)[0:8] if insertTime else ""

        # bookOrder.turns = 0 # xtpOrder.get("runtimeId",0) #同一批委托的编号
        # bookOrder.external_cancel_order_id = int(xtpOrder.get('orderCancelXtpId',"0"))
        # bookOrder.error_id = xtpOrder.get('xtpErrorId',0)
        # bookOrder.error_msg = xtpOrder.get('xtpErrorMsg',"")
        # bookOrder.cancel_time = xtpOrder.get('cancelTime',0)
        # bookOrder.parent_id = int(xtpOrder.get('parentOrderId'))
        # bookOrder.insert_time = insertTime #int64_t
        # bookOrder.update_time = xtpOrder.get('updateTime',0) #int64_t
        

    except Exception as err:
        logger.error(err,exc_info=True, stack_info=True)
        bookOrder = None

    return bookOrder

# 转换smart Trade到Book Trade
def convertTradeFromSmartToBook(trade:Trade):
    bookTrade = BookTrade()
    try:
        rowId = 0
        if trade.rowId and trade.rowId.isdigit():
            rowId = trade.rowId
        else:
            return None

        tradeTime = trade.trade_time

        bookTrade.instrument_id = trade.instrument_id
        bookTrade.exchange_id = trade.exchange_id
        bookTrade.account_id = trade.account_id
        bookTrade.order_id =  int(rowId)   #  #rowId代表order_id
        bookTrade.instrument_type = INSTRUMENT_TYPE_BOOK.get(trade.instrument_type,_InstrumentType.Unknown) 
        bookTrade.side = SIDE_BOOK.get(trade.side,_Side.Unknown)
        bookTrade.price = trade.price
        bookTrade.volume = trade.volume
        bookTrade.business_type = BUSINESS_TYPE_BOOK.get(trade.xtp_business_type,_BusinessType.UNKNOWN) 
        bookTrade.external_order_id = int(trade.order_id)
        bookTrade.trading_day = str(tradeTime)[0:8] if tradeTime else ""
        bookTrade.trade_id = 0
        bookTrade.report_index = int(trade.xtp_report_index)
        bookTrade.trade_amount = trade.trade_amount

        # bookTrade.exec_id = trade.xtp_exec_id
        # bookTrade.offset = OFFSET_BOOK.get(convertOffset(xtpPositionEffectType),-2)
        # bookTrade.trade_time = tradeTime

    except Exception as err:
        logger.error(err,exc_info=True, stack_info=True)
        bookTrade = None

    return bookTrade




class Book(BookBase):
    def __init__(self) -> None:
        super().__init__()
        self.name = ""
        self.dbPath = "" #book数据存储根路径
        self.lastTradeId = 0 #最新的映射成交编号，日内有效 自增ID
        self.tradeIdMap = {} #成交编号映射表 xtptradeId:虚拟自增ID 如：xtp_xx_1239u4324_dafdff:1
        # bookUtils.init_log("d:/output1.txt")

    def printLog(self,title):
        logger.debug("Book（%s）:%s==trading_day:%s,initial_equity:%s,static_equity:%s,avail:%s,frozen_cash:%s,intraday_fee:%s,accumulated_fee:%s,realized_pnl:%s",self.name,title,self.trading_day_in_string,self.initial_equity,self.static_equity,self.avail,self.frozen_cash,self.intraday_fee,self.accumulated_fee,self.realized_pnl)

    def printAll(self,title):
        logger.debug("%s:%s==trading_day:%s,initial_equity:%s,static_equity:%s,avail:%s,frozen_cash:%s,intraday_fee:%s,accumulated_fee:%s,realized_pnl:%s",self.name,title,self.trading_day_in_string,self.initial_equity,self.static_equity,self.avail,self.frozen_cash,self.intraday_fee,self.accumulated_fee,self.realized_pnl)
        for p in self.positions:
            logger.debug("%s volume：%s,sellable%s",p.instrument_id,p.volume,p.sellable)
        logger.debug("===============================================================")

    #override 收到下单
    def on_order_input_impl(self,orderInput:Dict):
        try:
            input = convertOrderInputFromSmartToBook(orderInput)
            if input:
                # logger.debug("Book（%s）on_order_input input:%s",self.name,str(input))
                # self.printLog("下单前")
                super().on_order_input(None,input)
                # self.printLog("下单后")
            # else:
                # logger.debug("Book（%s）on_order_input input is None",self.name)
        except Exception as err:
            logger.error(err,exc_info=True, stack_info=True)

    #override 收到委托回报
    def on_order_impl(self,order:Order):
        try:
            bookOrder = convertOrderFromSmartToBook(order)
            if bookOrder:
                # logger.debug("Book（%s）on_order bookOrder:%s",self.name,str(bookOrder))
                # self.printLog("收到委托前")
                super().on_order(None,bookOrder)
                # self.printLog("收到委托后")
            # else:
            #     logger.debug("Book（%s）on_order bookOrder is None",self.name)
        except Exception as err:
            logger.error(err,exc_info=True, stack_info=True)

    #override 收到成交回报
    def on_trade_impl(self,trade:Trade):
        try:
            bookTrade = convertTradeFromSmartToBook(trade)
            if bookTrade:
                # 处理trade_id映射
                temp_trade_id = self.tradeIdMap.get(trade.trade_id,0) #通过xtp trade_id获取映射的book trade_id
                if(temp_trade_id == 0):
                    self.lastTradeId  = self.lastTradeId +1 #自增
                    temp_trade_id = self.lastTradeId
                    self.tradeIdMap["lastTradeId"] = self.lastTradeId
                    self.tradeIdMap[trade.trade_id] = temp_trade_id
                bookTrade.trade_id = temp_trade_id

                # logger.debug("Book（%s）on_trade bookTrade:%s",self.name,str(bookTrade))
                # self.printLog("收到成交前")
                super().on_trade(None,bookTrade)
                # self.printLog("收到成交后")
            # else:
            #     logger.debug("Book（%s）on_trade bookTrade is None",self.name)
        except Exception as err:
            logger.error(err,exc_info=True, stack_info=True)

    #override 切换交易日
    def on_trading_day_impl(self,daytimeStr):
        super().on_trading_day(None,bookUtils.strptime(daytimeStr, "%Y%m%d"))
        self.dump()

    # 以下为市价下单数据计算使用
    #override 接收行情 TODO 暂未处理
    # def on_quote(self,quote):
    #     return
    #     super().on_quote(quote)

    #override 获取静态行情涨停价 TODO 暂未处理
    # def get_upper_limit_price(self,instrument_id,exchange_id):
    #     return 0.0

    #override 获取证券类型根据静态行情信息 TODO 暂未处理
    # def get_instrument_type(self,instrument_id,exchange_id):
    #     return super().get_instrument_type(instrument_id,exchange_id)

    ##################BOOK存盘########################################
    def dump(self):
        #批量存取arr数据
        def write_db(db,arr,isDict=False):
            total = len(arr)
            db.write(str(total))
            db.write("\n")
            tempLines = []
            index = 0
            while index < total:
                obj = arr[index]
                #每满100写入一批
                if(index != 0 and index % 100 == 0):
                    db.writelines(tempLines)
                    db.flush()
                    tempLines.clear()
                
                #序列化数据
                jsonStr = None
                if isDict:
                    jsonStr = json.dumps(obj)+"\n"
                else:
                    jsonStr = str(obj)+"\n"
                tempLines.append(jsonStr)
                index += 1
            
            #处理不满100条的批量写入
            if(len(tempLines)>0):
                db.writelines(tempLines)
                db.flush()

        def pos_list(positions):
            tempPosList = []
            for p in positions:
                tempPos = {
                    "avg_open_price" : p.avg_open_price,
                    "close_price" : p.close_price,
                    "direction" : int(p.direction),
                    "exchange_id" : p.exchange_id,
                    "frozen_total" : p.frozen_total,
                    "frozen_yesterday" : p.frozen_yesterday,
                    "instrument_id" : p.instrument_id,
                    "instrument_type" : int(p.instrument_type),
                    "last_price" : p.last_price,
                    "margin" : p.margin,
                    "market_value" : p.market_value,
                    "position_cost_price" : p.position_cost_price,
                    "pre_close_price" : p.pre_close_price,
                    "profit_price" : p.profit_price,
                    "purchase_redeemable_qty" : p.purchase_redeemable_qty,
                    "realized_pnl" : p.realized_pnl,
                    "sellable" : p.sellable,
                    "uname" : p.uname,
                    "unrealized_pnl" : p.unrealized_pnl,
                    "volume" : p.volume,
                    "yesterday_volume" : p.yesterday_volume,
                    "avg_open_price_td":p.avg_open_price_td,
                    "profit_price_td":p.profit_price_td,
                }
                tempPosList.append(tempPos)
            return tempPosList

        try:
            local_db_name = self.name
            local_db_path = os.path.join(self.dbPath,local_db_name)
            # logger.debug("dump local_db_path:%s",local_db_path)

            if(not os.path.exists(self.dbPath)):os.makedirs(self.dbPath)

            db = open(local_db_path, 'w',encoding="utf8")
            b = {
                "trading_day":self.trading_day_in_string,
                "initial_equity":self.initial_equity,
                "static_equity":self.static_equity,
                "avail":self.avail,
                "frozen_cash":self.frozen_cash,
                "frozen_margin":self.frozen_margin,
                "intraday_fee":self.intraday_fee,
                "accumulated_fee":self.accumulated_fee,
                "realized_pnl":self.realized_pnl,
                "avail_td":self.avail_td,
                "frozen_cash_td":self.frozen_cash_td,
                "intraday_fee_td":self.intraday_fee_td,
                "realized_pnl_td":self.realized_pnl_td
            }
            db.writelines([json.dumps(b)+"\n"])#写入book assets
            db.flush()
            write_db(db,pos_list(self.positions),True)#写入positions
            write_db(db,list(self._orders.values()),False)#写入orders
            write_db(db,list(self._trades.values()),False)#写入trades
            db.writelines([json.dumps(self.tradeIdMap)+"\n"])#写入book tradeIdMap
            db.flush()

            db.close()

        except Exception as err:
            logger.error(err,exc_info=True, stack_info=True)

    ##################BOOK恢复上一日的存盘数据############################
    '''
    恢复book读取本地存储数据
    '''
    def restore(self,hisOrders,hisTrades):
        #读取数据文件
        def read_db(db):
            rows = []
            try:
                rowSize = int(db.readline())
                for i in range(rowSize):
                    rows.append(json.loads(db.readline()))
            except Exception as err:
                pass
            return rows

        try:
            local_db_name = self.name
            local_db_path = os.path.join(self.dbPath,local_db_name)
            # logger.debug("Book（%s）restore local_db_path:%s",self.name,local_db_path)
            
            if(not os.path.exists(local_db_path)):return
            if(os.stat(local_db_path).st_size<=0):return

            db =  open(local_db_path, 'r',encoding="utf8")
            assets = json.loads(db.readline())#读取book assets
            positions = read_db(db)#读取positions
            orders = read_db(db)#读取orders
            trades = read_db(db)#读取trades
            tradeIdMapStr  = db.readline()#读取book tradeIdMap
            if(tradeIdMapStr):
                self.tradeIdMap = json.loads(tradeIdMapStr)
                self.lastTradeId = self.tradeIdMap.get("lastTradeId",0)

            db.close()
            # logger.debug("**************restore data orders:%s,trades:%s,positions:%s,book:%s",len(orders),len(trades),len(positions),str(assets))
            paramObj = assets
            assets["positions"] = positions
            self.do_init(paramObj)
            self.init_orders_from_json(orders)
            self.init_trades_from_json(trades)

            #判断存盘日期是否是当天，不是则清算
            today=datetime.now()
            todayStr= today.strftime("%Y%m%d")
            if(self.trading_day_in_string != todayStr):
                # self.printLog("Book on_trading_day before")
                # logger.debug("Book（%s）on_trading_day %s -> %s",self.name,self.trading_day_in_string,todayStr)
                # 换日清算
                self.on_trading_day_impl(todayStr)
            else:
                # 当天的需要继续灌入已有未使用的order和trade 恢复最新book
                # logger.debug("resume book order and trade,hisOrders:%d,hisTrades:%d",len(hisOrders),len(hisTrades))
                
                #根据order_id分组存储trade
                tradeMap = {}
                for trade in hisTrades:
                    order_id = trade.order_id
                    trades = tradeMap.get(order_id,None)
                    if not trades:
                        trades = []
                        tradeMap[order_id] = trades
                    trades.append(trade)

                hisOrders.sort(key=lambda od: od.order_id)

                #orders和trades混合排序
                for order in hisOrders:
                    order_id = order.order_id
                    trades = tradeMap.get(order_id,[])
                    #order处于结束状态
                    if(order.status in [OrderStatus.Filled,OrderStatus.PartialFilledNotActive,OrderStatus.Cancelled,OrderStatus.Error]):
                        # logger.debug("%s:order.status is Final,trades:%s",order_id,len(trades))
                        for trade in trades:
                            self.on_trade_impl(trade)
                        self.on_order_impl(order)
                    else:
                        # logger.debug("%s:order.status is Uncompleted,trades:%s",order_id,len(trades))
                        self.on_order_impl(order)
                        for trade in trades:
                            self.on_trade_impl(trade)

            # logger.debug("Book（%s）**************restore success**************",self.name)
            # self.printLog("Book Restore Done")

        except Exception as err:
            logger.error(err,exc_info=True, stack_info=True)
    ######################################################################

    def get_ticker2(self,symbol_id):
        return super().get_ticker2(symbol_id)
    
    def on_position_change(self,pos):
        super().on_position_change(pos)
    
    def on_asset_change(self):
        super().on_asset_change()
    
    def exit_divident_and_rights3(self):
        super().exit_divident_and_rights3()
    
    
