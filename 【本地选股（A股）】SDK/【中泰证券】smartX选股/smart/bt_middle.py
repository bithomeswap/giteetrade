import json

from .event import *
from .utils import *

from . import smartc

import logging
logger = logging.getLogger()


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

class DataType() :
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

class BtInstrumentType() :
    Unknown = 0       #未知
    Stock = 1         #普通股票
    Future = 2        #期货
    Bond = 3          #债券
    StockOption = 4   #股票期权
    Fund = 5          #基金
    TechStock = 6     #科创板股票
    Index = 7         #指数
    Repo = 8          #回购


class BT() :
    def __init__(self) -> None:
        pass

    # 接口名称区分 bt
    def bt_subscribe_tick(self, instruments, exchange_id, subscribe_callback) :
        sub_data = {
            "command" : CommandType.SubTick,
            "datatype" : DataType.ReqMsg,
            "data" : {
                "exchange_id" : exchange_id
            }
        }

        for instrument in instruments :
            sub_data["data"]["instrument_id"] = instrument
            smartc.bt_subscribe_tick(json.dumps(sub_data))


    # 接口名称区分 bt
    def bt_unsubscribe_tick(self, instruments, exchange_id) :
        sub_data = {
            "command" : CommandType.UnSubTick,
            "datatype" : DataType.ReqMsg,
            "data" : {
                "exchange_id" : exchange_id
            }
        }

        for instrument in instruments :
            sub_data["data"]["instrument_id"] = instrument
            smartc.bt_unsubscribe_tick(json.dumps(sub_data))

    def bt_insert_order(self, order_input, cb) :
        smartc.bt_insert_order(json.dumps(order_input), cb)

    def bt_cancel_order(self, order_id) :
        # logger.debug("order_id: %s", order_id)
        smartc.bt_cancel_order(int(order_id))
        # logger.debug("call smartc.bt_cancel_order done, order id: %s", order_id)


    def bt_subscribe_bar(self, codes, period) :
        logger.debug("enter bt_subscribe_bar, codes: %s, period: %s", json.dumps(codes), period)
        times = int(period[:-1])
        sub_data = {
            "command" : CommandType.SubBar,
            "datatype" : DataType.ReqMsg,
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

    def bt_unsubscribe_bar(self, codes, period) :
        logger.debug("enter bt_subscribe_bar, codes: %s, period: %s", json.dumps(codes), period)
        times = int(period[:-1])
        unsub_data = {
            "command" : CommandType.UnSubBar,
            "datatype" : DataType.ReqMsg,
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



bt = BT()