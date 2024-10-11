import uuid

import struct

import logging


from .type import *
from .event import *


from . import utils
from .utils import *

from . import smartc

from .bt_type import *

logger = logging.getLogger()




sz_instrument_map_instrument_full_type = {
    "000" : "XTP_SECURITY_MAIN_BOARD",
    "001" : "XTP_SECURITY_MAIN_BOARD",
    "002" : "XTP_SECURITY_MAIN_BOARD",
    "003" : "XTP_SECURITY_MAIN_BOARD",
    "004" : "XTP_SECURITY_MAIN_BOARD",
    "030" : "XTP_SECURITY_MAIN_BOARD",
    "031" : "XTP_SECURITY_MAIN_BOARD",
    "032" : "XTP_SECURITY_MAIN_BOARD",
    "036" : "XTP_SECURITY_MAIN_BOARD",
    "037" : "XTP_SECURITY_MAIN_BOARD",
    "038" : "XTP_SECURITY_MAIN_BOARD",
    "039" : "XTP_SECURITY_MAIN_BOARD",
    "070" : "XTP_SECURITY_MAIN_BOARD",
    "071" : "XTP_SECURITY_MAIN_BOARD",
    "072" : "XTP_SECURITY_MAIN_BOARD",
    "073" : "XTP_SECURITY_MAIN_BOARD",
    "074" : "XTP_SECURITY_MAIN_BOARD",
    "080" : "XTP_SECURITY_MAIN_BOARD",
    "081" : "XTP_SECURITY_MAIN_BOARD",
    "082" : "XTP_SECURITY_MAIN_BOARD",
    "083" : "XTP_SECURITY_MAIN_BOARD",
    "084" : "XTP_SECURITY_MAIN_BOARD",
    "100" : "XTP_SECURITY_STATE_BOND",
    "101" : "XTP_SECURITY_STATE_BOND",
    "102" : "XTP_SECURITY_STATE_BOND",
    "103" : "XTP_SECURITY_MAIN_BOARD",
    "104" : "XTP_SECURITY_STATE_BOND",
    "105" : "XTP_SECURITY_STATE_BOND",
    "106" : "XTP_SECURITY_STATE_BOND",
    "107" : "XTP_SECURITY_STATE_BOND",
    "108" : "XTP_SECURITY_STATE_BOND",
    "109" : "XTP_SECURITY_STATE_BOND",
    "111" : "XTP_SECURITY_STATE_BOND",
    "112" : "XTP_SECURITY_COMPANEY_BOND",
    "115" : "XTP_SECURITY_STATE_BOND",
    "117" : "XTP_SECURITY_MAIN_BOARD",
    "118" : "XTP_SECURITY_MAIN_BOARD",
    "119" : "XTP_SECURITY_MAIN_BOARD",
    "120" : "XTP_SECURITY_MAIN_BOARD",
    "121" : "XTP_SECURITY_MAIN_BOARD",
    "122" : "XTP_SECURITY_MAIN_BOARD",
    "123" : "XTP_SECURITY_CONVERTABLE_BOND",
    "124" : "XTP_SECURITY_MAIN_BOARD",
    "125" : "XTP_SECURITY_MAIN_BOARD",
    "126" : "XTP_SECURITY_MAIN_BOARD",
    "127" : "XTP_SECURITY_CONVERTABLE_BOND",
    "128" : "XTP_SECURITY_CONVERTABLE_BOND",
    "129" : "XTP_SECURITY_MAIN_BOARD",
    "131" : "XTP_SECURITY_NATIONAL_BOND_REVERSE_REPO",
    "133" : "XTP_SECURITY_STATE_BOND",
    "134" : "XTP_SECURITY_STATE_BOND",
    "138" : "XTP_SECURITY_STATE_BOND",
    "139" : "XTP_SECURITY_STATE_BOND",
    "140" : "XTP_SECURITY_MAIN_BOARD",
    "148" : "XTP_SECURITY_COMPANEY_BOND",
    "149" : "XTP_SECURITY_COMPANEY_BOND",
    "150" : "XTP_SECURITY_MAIN_BOARD",
    "151" : "XTP_SECURITY_MAIN_BOARD",
    "159" : "XTP_SECURITY_ETF_SINGLE_MARKET_STOCK",
    "160" : "XTP_SECURITY_MAIN_BOARD",
    "161" : "XTP_SECURITY_MAIN_BOARD",
    "162" : "XTP_SECURITY_MAIN_BOARD",
    "163" : "XTP_SECURITY_MAIN_BOARD",
    "164" : "XTP_SECURITY_MAIN_BOARD",
    "165" : "XTP_SECURITY_MAIN_BOARD",
    "166" : "XTP_SECURITY_MAIN_BOARD",
    "167" : "XTP_SECURITY_MAIN_BOARD",
    "168" : "XTP_SECURITY_MAIN_BOARD",
    "169" : "XTP_SECURITY_MAIN_BOARD",
    "184" : "XTP_SECURITY_MAIN_BOARD",
    "190" : "XTP_SECURITY_STATE_BOND",
    "191" : "XTP_SECURITY_STATE_BOND",
    "198" : "XTP_SECURITY_STATE_BOND",
    "200" : "XTP_SECURITY_MAIN_BOARD",
    "201" : "XTP_SECURITY_MAIN_BOARD",
    "202" : "XTP_SECURITY_MAIN_BOARD",
    "203" : "XTP_SECURITY_MAIN_BOARD",
    "204" : "XTP_SECURITY_MAIN_BOARD",
    "205" : "XTP_SECURITY_MAIN_BOARD",
    "206" : "XTP_SECURITY_MAIN_BOARD",
    "207" : "XTP_SECURITY_MAIN_BOARD",
    "208" : "XTP_SECURITY_MAIN_BOARD",
    "209" : "XTP_SECURITY_MAIN_BOARD",
    "238" : "XTP_SECURITY_MAIN_BOARD",
    "280" : "XTP_SECURITY_MAIN_BOARD",
    "281" : "XTP_SECURITY_MAIN_BOARD",
    "282" : "XTP_SECURITY_MAIN_BOARD",
    "283" : "XTP_SECURITY_MAIN_BOARD",
    "284" : "XTP_SECURITY_MAIN_BOARD",
    "285" : "XTP_SECURITY_MAIN_BOARD",
    "286" : "XTP_SECURITY_MAIN_BOARD",
    "287" : "XTP_SECURITY_MAIN_BOARD",
    "288" : "XTP_SECURITY_MAIN_BOARD",
    "289" : "XTP_SECURITY_MAIN_BOARD",
    "300" : "XTP_SECURITY_STARTUP_BOARD",
    "301" : "XTP_SECURITY_STARTUP_BOARD",
    "302" : "XTP_SECURITY_MAIN_BOARD",
    "303" : "XTP_SECURITY_MAIN_BOARD",
    "304" : "XTP_SECURITY_MAIN_BOARD",
    "305" : "XTP_SECURITY_MAIN_BOARD",
    "306" : "XTP_SECURITY_MAIN_BOARD",
    "307" : "XTP_SECURITY_MAIN_BOARD",
    "308" : "XTP_SECURITY_MAIN_BOARD",
    "309" : "XTP_SECURITY_MAIN_BOARD",
    "360" : "XTP_SECURITY_MAIN_BOARD",
    "361" : "XTP_SECURITY_MAIN_BOARD",
    "362" : "XTP_SECURITY_MAIN_BOARD",
    "363" : "XTP_SECURITY_MAIN_BOARD",
    "364" : "XTP_SECURITY_MAIN_BOARD",
    "365" : "XTP_SECURITY_MAIN_BOARD",
    "366" : "XTP_SECURITY_MAIN_BOARD",
    "367" : "XTP_SECURITY_MAIN_BOARD",
    "368" : "XTP_SECURITY_MAIN_BOARD",
    "369" : "XTP_SECURITY_MAIN_BOARD",
    "370" : "XTP_SECURITY_MAIN_BOARD",
    "371" : "XTP_SECURITY_MAIN_BOARD",
    "372" : "XTP_SECURITY_MAIN_BOARD",
    "373" : "XTP_SECURITY_MAIN_BOARD",
    "374" : "XTP_SECURITY_MAIN_BOARD",
    "375" : "XTP_SECURITY_MAIN_BOARD",
    "376" : "XTP_SECURITY_MAIN_BOARD",
    "377" : "XTP_SECURITY_MAIN_BOARD",
    "378" : "XTP_SECURITY_MAIN_BOARD",
    "379" : "XTP_SECURITY_MAIN_BOARD",
    "380" : "XTP_SECURITY_MAIN_BOARD",
    "381" : "XTP_SECURITY_MAIN_BOARD",
    "382" : "XTP_SECURITY_MAIN_BOARD",
    "383" : "XTP_SECURITY_MAIN_BOARD",
    "384" : "XTP_SECURITY_MAIN_BOARD",
    "385" : "XTP_SECURITY_MAIN_BOARD",
    "386" : "XTP_SECURITY_MAIN_BOARD",
    "387" : "XTP_SECURITY_MAIN_BOARD",
    "388" : "XTP_SECURITY_MAIN_BOARD",
    "389" : "XTP_SECURITY_MAIN_BOARD",
    "395" : "XTP_SECURITY_MAIN_BOARD",
    "399" : "XTP_SECURITY_MAIN_BOARD"
}


sh_instrument_map_instrument_full_type = {
    "000" : "XTP_SECURITY_INDEX",
    "009" : "XTP_SECURITY_MAIN_BOARD",
    "010" : "XTP_SECURITY_STATE_BOND",
    "018" : "XTP_SECURITY_STATE_BOND",
    "019" : "XTP_SECURITY_STATE_BOND",
    "020" : "XTP_SECURITY_STATE_BOND",
    "090" : "XTP_SECURITY_MAIN_BOARD",
    "091" : "XTP_SECURITY_MAIN_BOARD",
    "099" : "XTP_SECURITY_MAIN_BOARD",
    "100" : "XTP_SECURITY_MAIN_BOARD",   # 客户端 100 对应的为空
    "102" : "XTP_SECURITY_MAIN_BOARD",
    "103" : "XTP_SECURITY_MAIN_BOARD",
    "104" : "XTP_SECURITY_MAIN_BOARD",
    "105" : "XTP_SECURITY_MAIN_BOARD",
    "106" : "XTP_SECURITY_MAIN_BOARD",
    "107" : "XTP_SECURITY_MAIN_BOARD",
    "108" : "XTP_SECURITY_MAIN_BOARD",
    "110" : "XTP_SECURITY_CONVERTABLE_BOND",
    "111" : "XTP_SECURITY_CONVERTABLE_BOND",
    "113" : "XTP_SECURITY_CONVERTABLE_BOND",
    "118" : "XTP_SECURITY_CONVERTABLE_BOND",
    "120" : "XTP_SECURITY_ENTERPRICE_BOND",
    "121" : "XTP_SECURITY_MAIN_BOARD",
    "122" : "XTP_SECURITY_COMPANEY_BOND",
    "123" : "XTP_SECURITY_MAIN_BOARD",
    "124" : "XTP_SECURITY_COMPANEY_BOND",
    "125" : "XTP_SECURITY_MAIN_BOARD",
    "126" : "XTP_SECURITY_MAIN_BOARD",
    "127" : "XTP_SECURITY_COMPANEY_BOND",
    "128" : "XTP_SECURITY_MAIN_BOARD",
    "129" : "XTP_SECURITY_MAIN_BOARD",
    "130" : "XTP_SECURITY_STATE_BOND",
    "131" : "XTP_SECURITY_MAIN_BOARD",
    "132" : "XTP_SECURITY_MAIN_BOARD",
    "133" : "XTP_SECURITY_MAIN_BOARD",
    "134" : "XTP_SECURITY_MAIN_BOARD",
    "135" : "XTP_SECURITY_MAIN_BOARD",
    "136" : "XTP_SECURITY_COMPANEY_BOND",
    "137" : "XTP_SECURITY_MAIN_BOARD",
    "138" : "XTP_SECURITY_MAIN_BOARD",
    "139" : "XTP_SECURITY_MAIN_BOARD",
    "140" : "XTP_SECURITY_STATE_BOND",
    "141" : "XTP_SECURITY_MAIN_BOARD",
    "142" : "XTP_SECURITY_MAIN_BOARD",
    "143" : "XTP_SECURITY_COMPANEY_BOND",
    "144" : "XTP_SECURITY_MAIN_BOARD",
    "145" : "XTP_SECURITY_MAIN_BOARD",
    "146" : "XTP_SECURITY_MAIN_BOARD",
    "147" : "XTP_SECURITY_STATE_BOND",
    "149" : "XTP_SECURITY_MAIN_BOARD",
    "150" : "XTP_SECURITY_MAIN_BOARD",
    "151" : "XTP_SECURITY_MAIN_BOARD",
    "152" : "XTP_SECURITY_COMPANEY_BOND",
    "153" : "XTP_SECURITY_MAIN_BOARD",
    "154" : "XTP_SECURITY_MAIN_BOARD",
    "155" : "XTP_SECURITY_COMPANEY_BOND",
    "156" : "XTP_SECURITY_MAIN_BOARD",
    "157" : "XTP_SECURITY_STATE_BOND",
    "158" : "XTP_SECURITY_MAIN_BOARD",
    "159" : "XTP_SECURITY_ETF_GOLD",
    "160" : "XTP_SECURITY_STATE_BOND",
    "161" : "XTP_SECURITY_MAIN_BOARD",
    "162" : "XTP_SECURITY_MAIN_BOARD",
    "163" : "XTP_SECURITY_COMPANEY_BOND",
    "164" : "XTP_SECURITY_MAIN_BOARD",
    "165" : "XTP_SECURITY_MAIN_BOARD",
    "166" : "XTP_SECURITY_MAIN_BOARD",
    "167" : "XTP_SECURITY_MAIN_BOARD",
    "168" : "XTP_SECURITY_MAIN_BOARD",
    "169" : "XTP_SECURITY_MAIN_BOARD",
    "170" : "XTP_SECURITY_MAIN_BOARD",
    "171" : "XTP_SECURITY_STATE_BOND",
    "172" : "XTP_SECURITY_MAIN_BOARD",
    "173" : "XTP_SECURITY_STATE_BOND",
    "174" : "XTP_SECURITY_MAIN_BOARD",
    "175" : "XTP_SECURITY_COMPANEY_BOND",
    "176" : "XTP_SECURITY_MAIN_BOARD",
    "177" : "XTP_SECURITY_MAIN_BOARD",
    "178" : "XTP_SECURITY_MAIN_BOARD",
    "179" : "XTP_SECURITY_MAIN_BOARD",
    "181" : "XTP_SECURITY_MAIN_BOARD",
    "182" : "XTP_SECURITY_MAIN_BOARD",
    "186" : "XTP_SECURITY_STATE_BOND",
    "188" : "XTP_SECURITY_COMPANEY_BOND",
    "190" : "XTP_SECURITY_MAIN_BOARD",
    "191" : "XTP_SECURITY_MAIN_BOARD",
    "192" : "XTP_SECURITY_MAIN_BOARD",
    "193" : "XTP_SECURITY_MAIN_BOARD",
    "195" : "XTP_SECURITY_MAIN_BOARD",
    "201" : "XTP_SECURITY_MAIN_BOARD",
    "202" : "XTP_SECURITY_MAIN_BOARD",
    "203" : "XTP_SECURITY_MAIN_BOARD",
    "204" : "XTP_SECURITY_NATIONAL_BOND_REVERSE_REPO",
    "205" : "XTP_SECURITY_MAIN_BOARD",
    "206" : "XTP_SECURITY_MAIN_BOARD",
    "207" : "XTP_SECURITY_MAIN_BOARD",
    "310" : "XTP_SECURITY_MAIN_BOARD",
    "330" : "XTP_SECURITY_MAIN_BOARD",
    "360" : "XTP_SECURITY_MAIN_BOARD",
    "500" : "XTP_SECURITY_MAIN_BOARD",
    "501" : "XTP_SECURITY_MAIN_BOARD",
    "502" : "XTP_SECURITY_MAIN_BOARD",
    "505" : "XTP_SECURITY_MAIN_BOARD",
    "506" : "XTP_SECURITY_MAIN_BOARD",
    "510" : "XTP_SECURITY_ETF_SINGLE_MARKET_STOCK",
    "511" : "XTP_SECURITY_ETF_SINGLE_MARKET_BOND",
    "512" : "XTP_SECURITY_ETF_INTER_MARKET_STOCK",
    "513" : "XTP_SECURITY_MAIN_BOARD",
    "515" : "XTP_SECURITY_ETF_INTER_MARKET_STOCK",
    "516" : "XTP_SECURITY_MAIN_BOARD",
    "517" : "XTP_SECURITY_MAIN_BOARD",
    "518" : "XTP_SECURITY_MAIN_BOARD",
    "519" : "XTP_SECURITY_MAIN_BOARD",
    "521" : "XTP_SECURITY_MAIN_BOARD",
    "522" : "XTP_SECURITY_MAIN_BOARD",
    "523" : "XTP_SECURITY_MAIN_BOARD",
    "524" : "XTP_SECURITY_MAIN_BOARD",
    "550" : "XTP_SECURITY_MAIN_BOARD",
    "580" : "XTP_SECURITY_MAIN_BOARD",
    "582" : "XTP_SECURITY_MAIN_BOARD",
    "588" : "XTP_SECURITY_MAIN_BOARD",
    "600" : "XTP_SECURITY_MAIN_BOARD",
    "601" : "XTP_SECURITY_MAIN_BOARD",
    "603" : "XTP_SECURITY_MAIN_BOARD",
    "605" : "XTP_SECURITY_MAIN_BOARD",
    "688" : "XTP_SECURITY_TECH_BOARD",
    "689" : "XTP_SECURITY_MAIN_BOARD",
    "700" : "XTP_SECURITY_MAIN_BOARD",
    "701" : "XTP_SECURITY_MAIN_BOARD",
    "702" : "XTP_SECURITY_MAIN_BOARD",
    "703" : "XTP_SECURITY_MAIN_BOARD",
    "704" : "XTP_SECURITY_MAIN_BOARD",
    "705" : "XTP_SECURITY_MAIN_BOARD",
    "706" : "XTP_SECURITY_MAIN_BOARD",
    "707" : "XTP_SECURITY_MAIN_BOARD",
    "708" : "XTP_SECURITY_MAIN_BOARD",
    "709" : "XTP_SECURITY_MAIN_BOARD",
    "713" : "XTP_SECURITY_MAIN_BOARD",
    "714" : "XTP_SECURITY_MAIN_BOARD",
    "715" : "XTP_SECURITY_MAIN_BOARD",
    "716" : "XTP_SECURITY_MAIN_BOARD",
    "717" : "XTP_SECURITY_MAIN_BOARD",
    "718" : "XTP_SECURITY_MAIN_BOARD",
    "719" : "XTP_SECURITY_MAIN_BOARD",
    "726" : "XTP_SECURITY_MAIN_BOARD",
    "730" : "XTP_SECURITY_MAIN_BOARD",
    "731" : "XTP_SECURITY_MAIN_BOARD",
    "732" : "XTP_SECURITY_MAIN_BOARD",
    "733" : "XTP_SECURITY_MAIN_BOARD",
    "734" : "XTP_SECURITY_MAIN_BOARD",
    "735" : "XTP_SECURITY_MAIN_BOARD",
    "736" : "XTP_SECURITY_MAIN_BOARD",
    "737" : "XTP_SECURITY_MAIN_BOARD",
    "738" : "XTP_SECURITY_MAIN_BOARD",
    "739" : "XTP_SECURITY_MAIN_BOARD",
    "740" : "XTP_SECURITY_MAIN_BOARD",
    "741" : "XTP_SECURITY_MAIN_BOARD",
    "742" : "XTP_SECURITY_MAIN_BOARD",
    "743" : "XTP_SECURITY_MAIN_BOARD",
    "744" : "XTP_SECURITY_MAIN_BOARD",
    "745" : "XTP_SECURITY_MAIN_BOARD",
    "746" : "XTP_SECURITY_MAIN_BOARD",
    "747" : "XTP_SECURITY_MAIN_BOARD",
    "748" : "XTP_SECURITY_MAIN_BOARD",
    "749" : "XTP_SECURITY_MAIN_BOARD",
    "750" : "XTP_SECURITY_MAIN_BOARD",
    "751" : "XTP_SECURITY_MAIN_BOARD",
    "752" : "XTP_SECURITY_MAIN_BOARD",
    "753" : "XTP_SECURITY_MAIN_BOARD",
    "754" : "XTP_SECURITY_MAIN_BOARD",
    "755" : "XTP_SECURITY_MAIN_BOARD",
    "756" : "XTP_SECURITY_MAIN_BOARD",
    "758" : "XTP_SECURITY_MAIN_BOARD",
    "759" : "XTP_SECURITY_MAIN_BOARD",
    "760" : "XTP_SECURITY_MAIN_BOARD",
    "762" : "XTP_SECURITY_MAIN_BOARD",
    "764" : "XTP_SECURITY_MAIN_BOARD",
    "770" : "XTP_SECURITY_MAIN_BOARD",
    "771" : "XTP_SECURITY_MAIN_BOARD",
    "772" : "XTP_SECURITY_MAIN_BOARD",
    "773" : "XTP_SECURITY_MAIN_BOARD",
    "780" : "XTP_SECURITY_MAIN_BOARD",
    "783" : "XTP_SECURITY_MAIN_BOARD",
    "785" : "XTP_SECURITY_MAIN_BOARD",
    "787" : "XTP_SECURITY_MAIN_BOARD",
    "788" : "XTP_SECURITY_MAIN_BOARD",
    "789" : "XTP_SECURITY_MAIN_BOARD",
    "790" : "XTP_SECURITY_MAIN_BOARD",
    "791" : "XTP_SECURITY_MAIN_BOARD",
    "793" : "XTP_SECURITY_MAIN_BOARD",
    "794" : "XTP_SECURITY_MAIN_BOARD",
    "795" : "XTP_SECURITY_MAIN_BOARD",
    "796" : "XTP_SECURITY_MAIN_BOARD",
    "799" : "XTP_SECURITY_MAIN_BOARD",
    "888" : "XTP_SECURITY_MAIN_BOARD",
    "900" : "XTP_SECURITY_MAIN_BOARD",
    "938" : "XTP_SECURITY_MAIN_BOARD",
    "939" : "XTP_SECURITY_MAIN_BOARD",
    "970" : "XTP_SECURITY_MAIN_BOARD"
}


def get_instrument_full_type(instrument_id) :
    start_id = instrument_id[0 : 3]

    # logger.debug("start id: " + start_id)

    if start_id in sz_instrument_map_instrument_full_type :
        # logger.debug("sz instrument id : " + instrument_id + ", security type: " + sz_instrument_map_instrument_full_type.get(start_id))
        return sz_instrument_map_instrument_full_type.get(start_id)

    if start_id in sh_instrument_map_instrument_full_type :
        # logger.debug("sh instrument id : " + instrument_id + ", security type: " + sh_instrument_map_instrument_full_type.get(start_id))
        return sh_instrument_map_instrument_full_type.get(start_id)

    # logger.debug("not find " + instrument_id + " in sz and sh id set")

    return "XTP_SECURITY_MAIN_BOARD"



def convert_quote_from_bt(quote:Quote) :
    quote.source_id = "xtp"
    
    quote.instrument_type = InstrumentType.Stock

    am_ten_time = 100000000
    if quote.data_time < am_ten_time :
        quote.data_time = quote.trading_day + "0" + str(quote.data_time)
    else :
        quote.data_time = quote.trading_day + str(quote.data_time)

bt_instrument_type_map = {
    BtInstrumentType.BtInstrumentTypeStock : InstrumentType.Stock,
    BtInstrumentType.BtInstrumentTypeFuture : InstrumentType.Future,
    BtInstrumentType.BtInstrumentTypeBond : InstrumentType.Bond,
    BtInstrumentType.BtInstrumentTypeStockOption : InstrumentType.StockOption,
    BtInstrumentType.BtInstrumentTypeFund : InstrumentType.Fund,
    BtInstrumentType.BtInstrumentTypeIndex : InstrumentType.Index
}

def convert_instrument_type_from_bt(bt_instrument_type) :
    instrument_type = bt_instrument_type_map.get(bt_instrument_type)

    if (not instrument_type):
        instrument_type = InstrumentType.Unknown

    return instrument_type



bt_side_map = {
    BtSide.BtSideBuy : Side.Buy,
    BtSide.BtSideSell : Side.Sell,
    BtSide.BtSideLock : Side.Lock,
    # BtSide.BtSideUnlock : Side.,
    # BtSide.BtSideExec : Side.,
    # BtSide.BtSideDrop : Side.,
    BtSide.BtSidePurchase : Side.Purchase,
    BtSide.BtSideRedemption : Side.Pedemption,
    BtSide.BtSideSplit : Side.Split,
    BtSide.BtSideMerge : Side.Merge,
    BtSide.BtSideCover : Side.Cover,
    # BtSide.BtSideFreeze : Side.,
    BtSide.BtSideMarginTrade : Side.MarginTrade,
    BtSide.BtSideShortSell : Side.ShortSell,
    BtSide.BtSideRepayMargin : Side.RepayMargin,
    BtSide.BtSideRepayStock : Side.RepayStock,
    # BtSide.CashRepayMargin : Side.,
    # BtSide.BtSideStockRepayStock : Side.,
}

def convert_side_from_bt(bt_side) :
    side = bt_side_map[bt_side]

    if (not side) :
        side = Side.Unknown

    return side


exchange_map_xtp_market = {
    Exchange.Unknown : "XTP_MKT_UNKNOWN",
    Exchange.SZE : "XTP_MKT_SZ_A",
    Exchange.SSE : "XTP_MKT_SH_A",
    Exchange.BSE : "XTP_MKT_BJ_A"
}





'''
status 值相同，不需要转换
'''
def convert_order_from_bt(order:Order) :
    order.insert_time = str(order.insert_time)
    order.rcv_time = order.insert_time
    order.update_time = order.trading_day + str(order.update_time)
    order.order_id = str(order.order_id)
    order.source_order_id = order.order_id
    order.client_id = str(order.client_id)
    order.instrument_type = convert_instrument_type_from_bt(order.instrument_type)
    order.xtp_business_type = "XTP_BUSINESS_TYPE_UNKNOWN"  # bt 中没有 business_type， 在这里写死一个
    order.frozen_price = order.limit_price
    order.side = convert_side_from_bt(order.side)
    order.price_type = PriceType.Unknown  # bt 目前只支持限价
    order.code = order.instrument_id + "." + getExchangeStrFromExchangeId(order.exchange_id)
    order.offset = Offset.Init

    order.xtp_market_type = exchange_map_xtp_market.get(order.exchange_id)
    order.tax = None
    order.commission = None
    order.error_id = None
    order.error_msg = None
    order.volume_condition = VolumeCondition.Any
    order.time_condition = TimeCondition.GFD
    order.parent_order_id = None
    order.traffic = "frontpy"
    order.business_type = "frontpy"
    order.traffic_sub_id = None  # 非回测时类似于 "417-local"
    order.order_cancel_client_id = None
    order.order_cancel_xtp_id = None
    order.instrument_name = None
    order.xtp_price_type = order.price_type
    order.xtp_position_effect_type = None
    order.xtp_side_type = getXtpSideTypeFromSide(order.side)
    order.xtp_order_status = ALPHAX_ORDER_STATUS_MAPPING[order.side]
    order.exchange_id_name = dataTypeToName(order.exchange_id, "ALPHAX_EXCHANGE_TYPE") if not order.exchange_id == None else None
    order.instrument_type_name = dataTypeToName(order.instrument_type, "ALPHAX_INSTRUMENT_TYPE") if not order.instrument_type == None else None
    order.status_name = dataTypeToName(order.status, "ALPHAX_ORDER_STATUS") if not order.status == None else None
    order.side_name = dataTypeToName(order.side, "ALPHAX_SIDE") if not order.side == None else None
    order.offset_name = dataTypeToName(order.offset, "ALPHAX_OFFSET") if not order.offset == None else None
    order.price_type_name = dataTypeToName(order.price_type, "ALPHAX_PRICE_TYPE") if not order.price_type == None else None
    order.xtp_business_type_name = dataTypeToName(order.xtp_business_type, "XTP_BUSINESS_TYPE") if order.xtp_business_type else None
    order.xtp_market_name = dataTypeToName(order.xtp_market_type, "XTP_MARKET_TYPE") if order.xtp_market_type else None
    order.xtp_price_type_name = dataTypeToName(order.xtp_price_type, "XTP_PRICE_TYPE") if order.xtp_price_type else None
    order.xtp_position_effect_type_name = None
    order.xtp_side_type_name = transXtpSideType(order.side, order.xtp_business_type)
    order.xtp_order_status_name = dataTypeToName(order.xtp_order_status , "XTP_ORDER_STATUS_TYPE") if order.xtp_order_status else None
    order.volume_condition_name = dataTypeToName(order.volume_condition, "ALPHAX_VOLUME_TYPE") if not order.volume_condition == None else None
    order.time_condition_name = dataTypeToName(order.time_condition, "ALPHAX_TIME_TYPE") if not order.time_condition == None else None
    order.traffic_name = dataTypeToName(order.traffic, "SMART_BUSINESS_TYPE") if not order.traffic == None else None



def convert_trade_from_bt(trade:Trade) :
    trade.order_id = str(trade.order_id)
    trade.trade_time = str(trade.trade_time)
    trade.rcv_time = trade.trade_time
    trade.instrument_type = convert_instrument_type_from_bt(trade.instrument_type)
    trade.side = convert_side_from_bt(trade.side)
    trade.code = trade.instrument_id + "." + getExchangeStrFromExchangeId(trade.exchange_id)
    trade._rowid = str(trade.xtp_report_index)
    trade.offset = Offset.Unknown
    trade.xtp_market_type = exchange_map_xtp_market.get(trade.exchange_id)

    trade.parent_order_id = None
    trade.tax = None
    trade.commission = None
    trade.traffic = "frontpy"
    trade.traffic_sub_id = None  # 非回测时类似于 "417-local"
    trade.instrument_name = None
    trade.xtp_business_type = "XTP_BUSINESS_TYPE_UNKNOWN"   # bt 中没有 xtp_business_type， 在这里写死一个
    trade.xtp_order_exch_id = None
    trade.xtp_branch_pbu = None
    trade.xtp_position_effect_type = None
    trade.xtp_side_type = getXtpSideTypeFromSide(trade.side)
    trade.exchange_id_name = dataTypeToName(trade.exchange_id, "ALPHAX_EXCHANGE_TYPE") if trade.exchange_id else None
    trade.instrument_type_name = dataTypeToName(trade.instrument_type, "ALPHAX_INSTRUMENT_TYPE") if trade.instrument_type else None
    trade.side_name = dataTypeToName(trade.side, "ALPHAX_SIDE") if trade.side else None
    trade.offset_name = dataTypeToName(trade.offset, "ALPHAX_OFFSET") if trade.offset else None
    trade.xtp_business_type_name = dataTypeToName(trade.xtp_business_type, "XTP_BUSINESS_TYPE") if trade.xtp_business_type else None
    trade.xtp_market_name = dataTypeToName(trade.xtp_market_type, "XTP_MARKET_TYPE") if trade.xtp_market_type else None
    trade.xtp_position_effect_type_name = None
    trade.xtp_side_type_name = transXtpSideType(trade.side, trade.xtp_business_type)
    trade.traffic_name = dataTypeToName(trade.traffic, "SMART_BUSINESS_TYPE") if not trade.traffic == None else None
    trade.xtp_trade_type_name = dataTypeToName(trade.xtp_trade_type, "TXTPTradeTypeType") if trade.xtp_trade_type else None
    trade.trade_id = trade.order_id



bt_instrument_full_type_map_instrument_type_ext = {
    BtInstrumentFullType.BtInstrumentFullTypeUnknown : "XTP_TICKER_TYPE_UNKNOWN",
    BtInstrumentFullType.BtInstrumentFullTypeMainBoard : "XTP_SECURITY_MAIN_BOARD",
    BtInstrumentFullType.BtInstrumentFullTypeSecondBoard : "XTP_SECURITY_SECOND_BOARD",
    BtInstrumentFullType.BtInstrumentFullTypeStartupBoard : "XTP_SECURITY_STARTUP_BOARD",
    BtInstrumentFullType.BtInstrumentFullTypeIndex : "XTP_SECURITY_INDEX",
    BtInstrumentFullType.BtInstrumentFullTypeTechBoard : "XTP_SECURITY_TECH_BOARD",
    BtInstrumentFullType.BtInstrumentFullTypeStateBond : "XTP_SECURITY_STATE_BOND",
    BtInstrumentFullType.BtInstrumentFullTypeEnterpriceBond : "XTP_SECURITY_ENTERPRICE_BOND",
    BtInstrumentFullType.BtInstrumentFullTypeCompaneyBond : "XTP_SECURITY_COMPANEY_BOND",
    BtInstrumentFullType.BtInstrumentFullTypeConvertableBond : "XTP_SECURITY_CONVERTABLE_BOND",
    BtInstrumentFullType.BtInstrumentFullTypeNationalBondReverseRepo : "XTP_SECURITY_NATIONAL_BOND_REVERSE_REPO",
    BtInstrumentFullType.BtInstrumentFullTypeETFSingleMarketStock : "XTP_SECURITY_ETF_SINGLE_MARKET_STOCK",
    BtInstrumentFullType.BtInstrumentFullTypeETFInterMarketStock : "XTP_SECURITY_ETF_INTER_MARKET_STOCK",
    BtInstrumentFullType.BtInstrumentFullTypeETFCrossBorderStock : "XTP_SECURITY_ETF_CROSS_BORDER_STOCK",
    BtInstrumentFullType.BtInstrumentFullTypeETFSingleMarketBond : "XTP_SECURITY_ETF_SINGLE_MARKET_BOND",
    BtInstrumentFullType.BtInstrumentFullTypeETFSecurityCashBond : "XTP_SECURITY_TYPE_ETF_CASH_BOND",
    BtInstrumentFullType.BtInstrumentFullTypeETFGold : "XTP_SECURITY_ETF_GOLD",
    BtInstrumentFullType.BtInstrumentFullTypeETFCommondityFutures : "XTP_SECURITY_ETF_COMMODITY_FUTURES",
    BtInstrumentFullType.BtInstrumentFullTypeStructuredFundChild : "XTP_SECURITY_STRUCTURED_FUND_CHILD",
    BtInstrumentFullType.BtInstrumentFullTypeSZSERecreationFund : "XTP_SECURITY_SZSE_RECREATION_FUND",
    BtInstrumentFullType.BtInstrumentFullTypeStockOption : "XTP_SECURITY_STOCK_OPTION",
    BtInstrumentFullType.BtInstrumentFullTypeETFOption : "XTP_SECURITY_ETF_OPTION",
    BtInstrumentFullType.BtInstrumentFullTypeAllotment : "XTP_SECURITY_ALLOTMENT",
    BtInstrumentFullType.BtInstrumentFullTypeMonetaryFundSHcr : "XTP_SECURITY_MONETARY_FUND_SHCR",
    BtInstrumentFullType.BtInstrumentFullTypeMonetaryFundSHtr : "XTP_SECURITY_MONETARY_FUND_SHTR",
    BtInstrumentFullType.BtInstrumentFullTypeMonetaryFundSZ : "XTP_SECURITY_MONETARY_FUND_SZ"
}


def convert_instrument_full_type_from_bt(bt_instrument_full_type:int) :
    # return bt_instrument_full_type_map_instrument_type_ext[bt_instrument_full_type] or "XTP_TICKER_TYPE_UNKNOWN"

    # bt 返回的 bt_instrument_full_type 均为 BtInstrumentFullTypeUnknown，但此处若直接返回 BtInstrumentFullTypeUnknown 会导致后序有些地方走不通，比如 subscribe_bar
    if bt_instrument_full_type == BtInstrumentFullType.BtInstrumentFullTypeUnknown :
        return "XTP_SECURITY_MAIN_BOARD"

    return bt_instrument_full_type_map_instrument_type_ext.get(bt_instrument_full_type, "XTP_TICKER_TYPE_UNKNOWN")

# 将 20220104094000000 转换为 "2022-01-04 09:40:00"
def convert_bt_bar_time(time_int) :
    time_str = str(time_int)
    result = time_str[0:4] + "-" + time_str[4:6] + "-" + time_str[6:8] + " " + time_str[8:10] + ":" + time_str[10:12] + ":" + time_str[12:14]
    # logger.debug("converted time: " + result)
    return result



def convert_bar_from_bt(bar:Bar) :
    bar.source_id = "xtp"

    # todo: 60min 怎么处理

    # bar.time_interval = (bar.end_time // 10000000 - bar.start_time // 10000000) * 60 + (bar.end_time % 10000000 // 100000) - (bar.start_time % 10000000 // 100000)

    start_hour = bar.start_time // 10000000
    end_hour = bar.end_time // 10000000

    if end_hour >= 13 and start_hour < 13 :
        bar.time_interval = (end_hour - start_hour) * 60 + (bar.end_time % 10000000 // 100000) - (bar.start_time % 10000000 // 100000) - 90
    else :
        bar.time_interval = (end_hour - start_hour) * 60 + (bar.end_time % 10000000 // 100000) - (bar.start_time % 10000000 // 100000)


    bar.period = str(bar.time_interval) + "m"
    bar.type = "bar_" + bar.period
    bar.start_time = convert_bt_bar_time(bar.start_time)
    bar.end_time = convert_bt_bar_time(bar.end_time)
    bar.code = bar.instrument_id + "." + getExchangeStrFromExchangeId(bar.exchange_id)

    '''
    logger.debug("source id: %s, time interval: %d, period: %s, type: %s, start time: %s, end time: %s", \
            bar.source_id, bar.time_interval, bar.period, bar.type, bar.start_time, bar.end_time)
    '''

