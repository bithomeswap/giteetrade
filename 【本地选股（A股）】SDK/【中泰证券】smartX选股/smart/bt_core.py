import uuid

import struct

import logging


from .type import *
from .event import *

from . import utils
from .utils import *

from . import bt_utils
from .bt_utils import *

from .bt_type import *

from . import smartc

logger = logging.getLogger()

smart = None   #由外部初始化


# 接口名称区分 bt
def bt_subscribe_tick(instruments, exchange_id, subscribe_callback) :
    sub_data = {
        "command" : CommandType.SubTick,
        "datatype" : BtDataType.ReqMsg,
        "data" : {
            "exchange_id" : exchange_id
        }
    }

    for instrument in instruments :
        sub_data["data"]["instrument_id"] = instrument
        smartc.bt_subscribe_tick(json.dumps(sub_data))


# 接口名称区分 bt
def bt_unsubscribe_tick(instruments, exchange_id) :
    sub_data = {
        "command" : CommandType.UnSubTick,
        "datatype" : BtDataType.ReqMsg,
        "data" : {
            "exchange_id" : exchange_id
        }
    }

    for instrument in instruments :
        sub_data["data"]["instrument_id"] = instrument
        smartc.bt_unsubscribe_tick(json.dumps(sub_data))

def bt_insert_order(order_input, cb) :
    smartc.bt_insert_order(json.dumps(order_input), cb)

def bt_cancel_order(order_id) :
    # logger.debug("order_id: %s", order_id)
    smartc.bt_cancel_order(int(order_id))
    # logger.debug("call smartc.cancel_order done, order id: %s", order_id)


def bt_subscribe_bar(codes, period) :
    # logger.debug("enter bt_subscribe_bar, codes: %s, period: %s", json.dumps(codes), period)
    times = int(period[:-1])
    sub_data = {
        "command" : CommandType.SubBar,
        "datatype" : BtDataType.ReqMsg,
        "data" : {
            "period" : "min",
            "times" : times
        }
    }

    for code in codes :
        instrument_id, exchange_id = getInstrumentIdAndExchangeIdFromCode(code)
        sub_data["data"]["instrument_id"] = instrument_id
        sub_data["data"]["exchange_id"] = exchange_id

        # 暂时先用 BtInstrumentFullType.BtInstrumentFullTypeMainBoard
        sub_data["data"]["instrument_type"] = BtInstrumentFullType.BtInstrumentFullTypeMainBoard

        smartc.bt_subscribe_bar(json.dumps(sub_data))

def bt_unsubscribe_bar(codes, period) :
    # logger.debug("enter bt_subscribe_bar, codes: %s, period: %s", json.dumps(codes), period)
    times = int(period[:-1])
    unsub_data = {
        "command" : CommandType.UnSubBar,
        "datatype" : BtDataType.ReqMsg,
        "data" : {
            "period" : "min",
            "times" : times
        }
    }

    for code in codes :
        instrument_id, exchange_id = getInstrumentIdAndExchangeIdFromCode(code)
        unsub_data["data"]["instrument_id"] = instrument_id
        unsub_data["data"]["exchange_id"] = exchange_id

        # 暂时先用 BtInstrumentFullType.BtInstrumentFullTypeMainBoard
        unsub_data["data"]["instrument_type"] = BtInstrumentFullType.BtInstrumentFullTypeMainBoard

        smartc.bt_unsubscribe_bar(json.dumps(unsub_data))



def get_share_order() :
    # logger.debug("enter get_share_order")
    order = Order()

    [order.client_id, order.insert_time, order.update_time, order.trading_day, order.instrument_id, order.exchange_id, order.account_id, order.instrument_type, \
        order.price_type, order.limit_price, order.volume, order.volume_traded, order.trade_amount, order.volume_left, order.status, order.side, \
        order.order_id, order.cancel_time] = struct.unpack('=qqq8s6s3s32sqqdqqdqqqqq', smart.order_share_mem[0:161])
    
    order.trading_day = order.trading_day.decode("utf-8")
    order.instrument_id = order.instrument_id.decode("utf-8")
    order.exchange_id = order.exchange_id.decode("utf-8")
    order.account_id = order.account_id.decode("utf-8", errors="replace").replace("\x00", "")

    if order.order_id == -1 :
        logger.error("insert failed, order id == -1")
        return order

    '''
    logger.debug("client_id: %d, insert_time: %d, update_time: %s, trading_day: %s, instrument_id: %s, exchange_id: %s, account_id: %s, instrument_type: %d, \
        price_type: %d, limit_price: %f, volume: %d, volume_traded: %d, trade_amount: %f, volume_left: %d, status: %d, side: %d, order_id: %d, \
            cancel_time: %d", order.client_id, order.insert_time, order.update_time, order.trading_day, order.instrument_id, order.exchange_id, order.account_id, \
                order.instrument_type, order.price_type, order.limit_price, order.volume, order.volume_traded, order.trade_amount, \
                    order.volume_left, order.status, order.side, order.order_id, order.cancel_time)
    '''

    '''
    logger.debug("insert_time: %d, update_time: %d, trading_day: %s, instrument_id: %s, exchange_id: %s, account_id: %s, instrument_type: %d, \
        price_type: %d, limit_price: %f, volume: %d, volume_traded: %d, trade_amount: %f, volume_left: %d, status: %d, side: %d, order_id: %d, \
            cancel_time: %d", order.insert_time, order.update_time, order.trading_day, order.instrument_id, order.exchange_id, \
            order.account_id, order.instrument_type, order.price_type, order.limit_price, order.volume, \
            order.volume_traded, order.trade_amount, order.volume_left, order.status, order.side, order.order_id, order.cancel_time)
    '''

    convert_order_from_bt(order)

    # logger.debug("receive order, order id: %s, instrument_id: %s", order.order_id, order.instrument_id)

    # logger.debug("order data: " + utils.toString(order))
    
    return order

def get_share_trade() :

    '''
    struct Trade {
        unsigned long long external_order_id;
        unsigned long long trade_id;
        unsigned long long order_id;
        unsigned long long trade_time;
        char account_id[32];
        char trading_day[8];
        char instrument_id[6];
        char exchange_id[3];
        // char client_id[8];
        char exec_id[8];
        long long instrument_type;
        double price;
        long long volume;
        int side;
        char trade_type;
        double trade_amount;
    };
    '''

    trade = Trade()

    [trade.order_id, trade.xtp_report_index, trade.client_id, trade.trade_time, trade.account_id] = struct.unpack('=QQQQ32s', smart.trade_share_mem[0:64])

    # logger.debug("xtp_report_index: %d, order_id: %d, trade_time: %d", trade.xtp_report_index, trade.order_id, trade.trade_time)

    [trade.instrument_id, trade.exchange_id, trade.xtp_exec_id, trade.instrument_type, trade.price, trade.volume, trade.side, trade.xtp_trade_type, \
        trade.trade_amount] = struct.unpack('=6s3s8sqdqicd', smart.trade_share_mem[72:126])

    trade.account_id = trade.account_id.decode("utf-8", errors="replace").replace("\x00", "")
    trade.instrument_id = trade.instrument_id.decode("utf-8")
    trade.exchange_id = trade.exchange_id.decode("utf-8")
    trade.xtp_trade_type = trade.xtp_trade_type.decode("utf-8")
    trade.xtp_exec_id = trade.xtp_exec_id.decode("utf-8")

    '''
    logger.debug("xtp_report_index: %d, order_id: %d, client_id: %d, trade_time: %d, account_id: %s, instrument_id: %s, exchange_id: %s \
        , xtp_exec_id: %s, instrument_type: %d, price: %f, volume: %d, side: %d, xtp_trade_type: %s, trade_amount: %f", \
        trade.xtp_report_index, trade.order_id, trade.client_id, trade.trade_time, trade.account_id, trade.instrument_id, trade.exchange_id, \
        trade.xtp_exec_id, trade.instrument_type, trade.price, trade.volume, trade.side, trade.xtp_trade_type, trade.trade_amount)
    '''

    convert_trade_from_bt(trade)

    # logger.debug("trade data: " + utils.toString(trade))

    return trade

def get_share_quote() :
    quote = Quote()

    [quote.data_time, quote.trading_day, quote.instrument_id, quote.exchange_id, quote.pre_close_price, quote.last_price,  quote.volume, quote.turnover, \
        quote.open_price, quote.high_price, quote.low_price, quote.upper_limit_price, quote.lower_limit_price, quote.close_price] \
        = struct.unpack('=q8s6s3sddqddddddd', smart.quote_share_mem[0:105])

    quote.bid_price = struct.unpack('=10d', smart.quote_share_mem[105:185])
    quote.ask_price = struct.unpack('=10d', smart.quote_share_mem[185:265])
    quote.bid_volume = struct.unpack('=10q', smart.quote_share_mem[265:345])
    quote.ask_volume = struct.unpack('=10q', smart.quote_share_mem[345:425])

    quote.trading_day = quote.trading_day.decode("utf-8")
    quote.instrument_id = quote.instrument_id.decode("utf-8")
    quote.exchange_id = quote.exchange_id.decode("utf-8")

    '''
    logger.debug("trading_day: %d, instrument_id: %s, exchange_id: %s, pre_close_price: %f, last_price: %f, volume: %d, turnover: %f, \
        open_price: %f, high_price: %f, low_price: %f, upper_limit_price: %f, lower_limit_price: %f, close_price: %f", \
        quote.trading_day, quote.instrument_id, quote.exchange_id, quote.pre_close_price, quote.last_price, quote.volume, quote.turnover, \
            quote.open_price, quote.high_price, quote.low_price, quote.upper_limit_price, quote.lower_limit_price, quote.close_price)

    logger.debug("bid_price:  %s", [str(v) for v in quote.bid_price])
    logger.debug("ask_price:  %s", [str(v) for v in quote.ask_price])
    logger.debug("bid_volume:  %s", [str(v) for v in quote.bid_volume])
    logger.debug("ask_volume:  %s", [str(v) for v in quote.ask_volume])
    '''

    convert_quote_from_bt(quote)

    smart.current_time = int(quote.data_time)

    #logger.debug("cur quote time: %s", smart.current_time)


    return quote

def get_share_bar() :
    # logger.debug("get_share_bar called")

    bar = Bar()

    [bar.trading_day, bar.instrument_id, bar.exchange_id, bar.start_time, bar.end_time, bar.open, bar.high, bar.low, bar.close, bar.volume, bar.turnover] \
        = struct.unpack('=8s6s3sqqddddqd', smart.bar_share_mem[0:81])

    bar.trading_day = bar.trading_day.decode("utf-8")
    bar.instrument_id = bar.instrument_id.decode("utf-8")
    bar.exchange_id = bar.exchange_id.decode("utf-8")

    '''
    logger.debug("trading day: %s, instrument id: %s, exchange id: %s, start time: %s, end time: %s, open: %f, high: %f, low: %f, close: %f, volume: %d, turnover: %f", \
        bar.trading_day, bar.instrument_id, bar.exchange_id, bar.start_time, bar.end_time, bar.open, bar.high, bar.low, bar.close, bar.volume, bar.turnover)
    '''

    # 更新当前时间
    smart.current_time = bar.end_time

    bt_utils.convert_bar_from_bt(bar)

    # logger.debug("receive bar, code: %s, period: %s", bar.code, bar.period)

    '''
    logger.debug("source id: %s, time interval: %d, period: %s, type: %s, start time: %s, end time: %s", \
        bar.source_id, bar.time_interval, bar.period, bar.type, bar.start_time, bar.end_time)
    '''

    return bar

def get_share_static_quote(quote_num, instrument_list, instrument_map, instrument_type_map, rever_repo_list) :
    # logger.debug("enter get_share_static_quote, quote_num: %d", quote_num)
    # logger.debug("quotes data: %s", smart.static_quote_share_mem)


    for i in range(quote_num) :
        static_quote_index = smart.bt_static_quote_size * i
        
        # logger.debug("bt_static_quote_size: %d, i: %d, static_quote_index: %ld", smart.bt_static_quote_size, i, static_quote_index)

        
        quote = Instrument()


        [quote.instrument_id, quote.exchange_id, quote.instrument_name, quote.instrument_type_ext] = struct.unpack('=32s16s64sb', smart.static_quote_share_mem[static_quote_index : (static_quote_index + 113)])

        #logger.debug("instrument_type_ext: %s", quote.instrument_type_ext)

        # quote.instrument_type_ext = ord(quote.instrument_type_ext)

        [quote.is_registration] = struct.unpack('=?', smart.static_quote_share_mem[(static_quote_index + 114) : (static_quote_index + 115)])

        [quote.upper_limit_price, \
            quote.lower_limit_price, \
            quote.pre_close_price, \
            quote.price_tick, \
            quote.bid_upper_limit_volume, \
            quote.bid_lower_limit_volume, \
            quote.bid_volume_unit, \
            quote.ask_upper_limit_volume, \
            quote.ask_lower_limit_volume, \
            quote.ask_volume_unit, \
            quote.market_bid_upper_limit_volume, \
            quote.market_bid_lower_limit_volume, \
            quote.market_bid_volume_unit, \
            quote.market_ask_upper_limit_volume, \
            quote.market_ask_lower_limit_volume, \
            quote.market_ask_volume_unit] \
            = struct.unpack('=ddddiiiiiiiiiiii', smart.static_quote_share_mem[(static_quote_index + 119) : (static_quote_index + 199)])

        #logger.debug("unpack done, i: %d", i)

        quote.instrument_id = quote.instrument_id.decode("utf-8", errors="replace").replace("\x00", "")
        quote.exchange_id = quote.exchange_id.decode("utf-8", errors="replace").replace("\x00", "")
        quote.instrument_name = quote.instrument_name.decode("utf-8", errors="replace").replace("\x00", "")

        exchange_str = getExchangeStrFromExchangeId(quote.exchange_id)
        if (exchange_str):
            quote.code = quote.instrument_id + "." + exchange_str

        
        # quote.instrument_type_ext = convert_instrument_full_type_from_bt(quote.instrument_type_ext)

        quote.instrument_type_ext = bt_utils.get_instrument_full_type(quote.instrument_id)
        quote.instrument_type = convertInstrumentTypeFromXtpSecurityType(quote.instrument_type_ext)

        '''
        logger.debug("instrument_id: %s, exchange_id: %s, instrument_name: %s, instrument_type: %d, instrument_type_ext: %s, is_registration: %s, \
            upper_limit_price: %f, lower_limit_price: %f, pre_close_price: %f, price_tick: %f, bid_upper_limit_volume: %d, \
            bid_lower_limit_volume: %d, bid_volume_unit: %d, ask_upper_limit_volume: %d, ask_lower_limit_volume: %d, \
            ask_volume_unit: %d, market_bid_upper_limit_volume: %d, market_bid_lower_limit_volume: %d, market_bid_volume_unit: %d, \
            market_ask_upper_limit_volume: %d, market_ask_lower_limit_volume: %d, market_ask_volume_unit: %d, code: %s", quote.instrument_id, \
            quote.exchange_id, quote.instrument_name, quote.instrument_type, quote.instrument_type_ext, quote.is_registration, quote.upper_limit_price, \
            quote.lower_limit_price, quote.pre_close_price, quote.price_tick, quote.bid_upper_limit_volume, quote.bid_lower_limit_volume, \
            quote.bid_volume_unit, quote.ask_upper_limit_volume, quote.ask_lower_limit_volume, quote.ask_volume_unit, \
            quote.market_bid_upper_limit_volume, quote.market_bid_lower_limit_volume, quote.market_bid_volume_unit, \
            quote.market_ask_upper_limit_volume, quote.market_ask_lower_limit_volume, quote.market_ask_volume_unit, quote.code)
        '''

        instrument_list.append(quote)
        instrument_map[quote.instrument_id + "_" + quote.exchange_id] = quote
        instrument_type_map[quote.instrument_type].append(quote)
        if (quote.instrument_type_ext == "XTP_SECURITY_NATIONAL_BOND_REVERSE_REPO"):
            rever_repo_list.append(quote)

    # logger.debug("instrument_list length: %d", len(instrument_list))


# 接收从 bt 返回的静态行情
def init_all_static_tickers_from_bt(tick_num:str) :
    # logger.info("tick_num: %s", tick_num)

    try :
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

        get_share_static_quote(int(tick_num), _instrumentList, _instrumentMap, _instrumentTypeMap, _reverseRepoList)

        smart.instrument_map_by_type = _instrumentTypeMap # TODO: 为何要暴露ticker？
        smart.instrument_list = _instrumentList
        smart.instrument_map = _instrumentMap
        smart.reverse_repo_list = _reverseRepoList
        smart.emit("_INIT_ALL_TICKERS_DONE")
        #smart.initCallback()
    except Exception as err:
        logger.error(err,exc_info=True, stack_info=True)

# data 为 ""，此处用不到
def back_test_bar_handler(data:str) :

    try :
        bar = get_share_bar()
        
        # logger.debug("receive bar, data: " + utils.toString(bar))

        key = 'bar_' + bar.period + "_" + bar.code

        if not (key in smart.get_subIndicatorMap()):
            return

        smart.get_quoteIndicatorMap()[key] = bar  # 缓存更新行情数据

        subList = smart.get_subIndicatorMap().get(key)

        for subObj in subList:
            subObj["emitter"].emit(Event.ON_BAR, bar)
    
    except Exception as err:
        logger.error(err, exc_info=True, stack_info=True)

    # logger.debug("back_test_bar_handler finish")

def back_test_entrust_handler() :
    try :
        order_info = get_share_order()
        account_id = order_info.account_id
        account = smart.account_map.get(account_id)

        if account :
            # logger.debug("find account for order")
            account._addOrderInfo(order_info)
            # logger.debug("add order info done")
            #如果为算法单单独分发母单的子单
            if order_info.business_type == "algo" and order_info.parent_order_id :
                strategie = smart.strategy_map.get(order_info.parent_order_id + "_algo")
                if (strategie):strategie._addOrderInfo(order_info)
    except Exception as err:
        logger.error(err, exc_info=True, stack_info=True)


def back_test_trade_report_handler() :
    try :
        trade = get_share_trade()

        account_id = trade.account_id
        account = smart.account_map.get(account_id)

        if account:

            # logger.debug("find account for trade")
            account._addTradeReport(trade)
            # logger.debug("add trade done")

            #如果为算法单单独分发母单的子单
            if trade.business_type == "algo" and trade.parent_order_id:
                strategie = smart.strategy_map.get(trade.parent_order_id + "_algo")
                if (strategie):strategie._addTradeReport(trade)
    except Exception as err:
        logger.error(err, exc_info=True, stack_info=True)


def back_test_quote_handler() :
    try :
        quote = Quote()
        quote = get_share_quote()

        key = quote.instrument_id + "_" + quote.exchange_id
        #key = "600000"+"_"+"SSE"
        if not (key in smart.get_submap()) :
            logger.debug("not find key: %s", key)
            return #未订阅终止派发

        smart.get_quoteMap()[key] = quote #缓存更新行情数据
        subList = smart.get_submap().get(key)
        for subObj in subList:
            subObj["emitter"].emit(Event.ON_QUOTE,quote)
        
    except Exception as err:
        logger.error(err,exc_info=True, stack_info=True)


def add_timer_bt(msec:int, callback) :
    # logger.info("enter add_timer_bt, msec: {}".format(msec))

    sid = f'TIME_{uuid.uuid1()}'
    smart.bt_time_map[sid] = 1

    def timer_handler(rsp:str) :
        # logger.debug("timer_handler called, notify time: %s", rsp)

        smart.current_time = int(rsp)
        
        try:
            if not (sid in smart.bt_time_map):return
            callback()
        except Exception as err:
            logger.error(err,exc_info=True, stack_info=True)

    trigger_time = smart.current_time + msec

    # logger.debug("cur quote time: %d, trigger time: %d", smart.current_time, trigger_time)
    smartc.bt_add_timer(trigger_time, timer_handler)

    return sid

def clear_timer_bt(sid:str) :
    # logger.debug("sid:: " + sid)

    if(sid in smart.bt_time_map):
        del smart.bt_time_map[sid]


def add_timer_interval_bt(msec:int =0, callback=None) :
    # logger.debug("msec: " + str(msec))
    sid = f'TIME_INTERVAL_{uuid.uuid1()}'
    smart.bt_time_map[sid] = msec

    def timer_handler(rsp:str) :
        try :
            smart.current_time = int(rsp)

            if (sid not in smart.bt_time_map) :                    
                return

            callback()

            if (sid in smart.bt_time_map) :                    
                trigger_time = smart.current_time + msec
                smartc.bt_add_timer(trigger_time, timer_handler)

        except Exception as err :
            logger.error(err,exc_info=True, stack_info=True)

    trigger_time = smart.current_time + msec
    smartc.bt_add_timer(trigger_time, timer_handler)

    # logger.info("sid:: " + str(sid))

    return sid

def clear_time_interval_bt(sid:str=None):
    # logger.debug("sid:: " + sid)
    if not sid:
        raise Exception("sid required!")
    if(sid in smart.bt_time_map):
        del smart.bt_time_map[sid]


def checkBTData(instrumentCodeList,exchangeId,period):
    if exchangeId == None :
        ticker_map = {}
        for code in instrumentCodeList :
            code = code.upper()
            instrument_id, exchange_id = getInstrumentIdAndExchangeIdFromCode(code)
            key = instrument_id + "_" + exchange_id

            instrument_info = smart.instrument_map.get(key)

            if instrument_info :

                ticker_list = ticker_map.get(key)

                if not ticker_list :
                    ticker_list = []
                    ticker_map[key] = ticker_list

                ticker_list.append({"code": code, "market": exchange_id,"name": instrument_info.instrument_name, "type": "STK" if instrument_info.instrument_type == InstrumentType.Stock else "ETF"})


        for tickerList in ticker_map.values() :
                params = {"tickerList":tickerList,"period":period,"start":smart.config.get("enginConfig").get("data").get("begin_time"),"end":smart.config.get("enginConfig").get("data").get("end_time")}
                rsp = smartc.request_reply("checkBTData",json.dumps(params))

                # logger.debug("checkBTDATA rsp:%s",rsp)

    else :
        tickerList = []
        for code in instrumentCodeList:
            key = code+"_"+ exchangeId
            instrument_info = smart.instrument_map.get(key)
            # logger.debug("instrument map:%s",utils.toString( smart.instrument_map.get(key)))
            if instrument_info:
                tickerList.append({"code": code, "market": exchangeId,"name": instrument_info.instrument_name, "type": "STK" if instrument_info.instrument_type == InstrumentType.Stock else "ETF"})
        if len(tickerList)>0:
            # logger.debug("checkBTDATA, enginConfig:%s",json.dumps(smart.config.get("enginConfig")))
            params = {"tickerList":tickerList,"period":period,"start":smart.config.get("enginConfig").get("data").get("begin_time"),"end":smart.config.get("enginConfig").get("data").get("end_time")}
            rsp = smartc.request_reply("checkBTData",json.dumps(params))
            
            #result = decodeRsp(rsp)
            # logger.debug("checkBTDATA rsp:%s",rsp)
            # if result.code != 0 or result.code !=1:
            #     logger.error("行情文件下载失败，回测结果可能不正确！")