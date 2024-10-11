'''
各种转换数据函数
'''
from datetime import datetime
import traceback
import json
from typing import Any
from .type import *
import time
import base64
import random
import math
import logging
import math
logger = logging.getLogger()

smart = None #由外部初始化
'''
             接受smart框架的 账户级别的委托推送 向插件提供on_order事件派发
            Order 委托确认
            属性      	      类型	    说明                                          对应SMART字段         示例
            rcv_time	                    String	数据接收时间                                              "20200608140053830"
            order_id	                    String	委托编号ID(xtpid)                     orderXtpId         "36934130021173201"
            insert_time	                String	委托写入时间                           insertTime         "20200608140053830"
            update_time	                String	委托更新时间                           updateTime         "20200608140053830"
            trading_day	                String	交易日                                insertTime中截取    "20200608"
            instrument_id	            String	合约ID（证券代码）                      ticker             "600000"
            exchange_id	                String	交易所ID                              xtpMarketType转换   "SZE"
            account_id	                String	账号ID                                userName           "10912133333344"
            client_id	            String	用户自定义报单编号                     orderClientId(rowId优先)   "6a1071e1-a94d-11ea-810c-4b25bab2cda3"
            instrument_type	            Number	合约类型                               xtpBusinessType转换  InstrumentType.Stock
            limit_price	                Number	价格                                  price
            frozen_price	                Number	冻结价格（市价单冻结价格为0.0）          price
            volume	                    Number	数量                                  quantity
            volume_traded	            Number	成交数量                              qty_traded
            volume_left	                Number	剩余数量                              qty_left
            tax	                        Number	税                                   todo:
            commission	                Number	手续费                                todo:
            status	                    Number	订单状态                              orderStatus
            error_id	                    Number	错误ID                               xtpErrorId
            error_msg	                String	错误信息                              xtpErrorMsg
            side	                        Number	买卖方向                              xtpSideType
            offset	                    Number	开平方向                              xtpPositionEffectType
            price_type	                Number	价格类型                              xtpPriceType
            volume_condition             Number	成交量类型
            time_condition	            Number	成交时间类型
            parent_order_id	            String	母单ID                               runtimeId
            以下为新增：
            traffic                      String  业务渠道标识                           business_type        "AlphaX"
            traffic_sub_id               String  业务子标识，一般填策略名称               businessSubId        "网格交易"
            cancel_time                  String  撤单时间                              cancelTime           "20200608140053830"
            order_cancel_client_id       String  撤单自定义编号                         orderCancelClientId  "0"
            order_cancel_xtp_id          String  所撤原单的编号(原xtpid）                orderCancelXtpId     "0"
            instrument_name              String  合约名称（证券名称）                    tickerName            "浦发银行"
            trade_amount                 Number  委托金额                              tradeAmount           0
            xtp_business_type            String  xtp证券业务类型                       xtpBusinessType       "XTP_BUSINESS_TYPE_CASH"
            xtp_market_type              String  xtp市场类型                           xtpMarketType         "XTP_MKT_SZ_A"
            以下为xtp的冗余字段，为了获取xtp的原值
            xtp_price_type                String  xtp价格类型                         xtpPriceType          "XTP_PRICE_LIMIT"
            xtp_position_effect_type     String  xtp开平方向                          xtpPositionEffectType "XTP_POSITION_EFFECT_OPEN"
            xtp_side_type                String  xtp交易方向                          xtpSideType           "XTP_SIDE_BUY"
            xtp_order_status             String  xtp订单状态                          orderStatus           "XTP_ORDER_STATUS_INIT"
            以下为xtp和alphax枚举值翻译为中文的名称
            exchange_id_name             String  交易所名称                                                  "上交所"
            instrument_type_name         String  合约类型名称                                                "股票"
            status_name                  String  订单状态名称                                                "全部成交"
            side_name                    String  买卖方向名称                                                "买"
            offset_name                  String  开平方向名称                                                "开"
            price_type_name              String  价格类型名称                                                "限价"
            xtp_business_type_name       String  xtp证券业务类型名称                                          "现货"
            xtp_market_name              String  xtp市场类型名称                                             "沪市"
            xtp_price_type_name          String  xtp价格类型名称                                             "限价"
            xtp_position_effect_type_name String  xtp开平方向名称                                             "开"
            xtp_side_type_name           String  xtp交易方向名称                                             "买"
            xtp_order_status_name        String  xtp价格类型名称                                             "限价"
            volume_condition_name        String  成交量类型名称                                              "任何数量" "最小数量" "全部数量"
            time_condition_name          String  成交时间类型名称                                            "立即完成" "本节有效"  "当日有效" "指定日期前有效" "撤销前有效" "集合竞价有效"
            traffic_name                 String  业务渠道名称                                                "策略"
'''
# 2022-4-13
def convertOrderFromSmartToPlugin(xtpOrder:dict):
    alphaXOrder = Order()
    alphaXOrder.rcv_time = xtpOrder.get('updateTime') or xtpOrder.get('insertTime') #优先取updateTime  ???? todo：或许应该取smart server的时间
    alphaXOrder.order_id = xtpOrder.get('orderXtpId')
    alphaXOrder.source_order_id = xtpOrder.get('orderXtpId')
    alphaXOrder.insert_time = xtpOrder.get('insertTime')
    alphaXOrder.update_time = xtpOrder.get('updateTime') 
    alphaXOrder.trading_day = str(xtpOrder.get('insertTime'))[0:8] if xtpOrder.get('insertTime') else None #实际没找到，对于能否找到要进行判断
    alphaXOrder.instrument_id = xtpOrder.get('ticker')
    alphaXOrder.exchange_id = convertExchangeIdFromxtpMarketType(xtpOrder.get('xtpMarketType')) if xtpOrder.get('xtpMarketType') else None
    alphaXOrder.account_id = xtpOrder.get('userName')
    alphaXOrder.client_id = xtpOrder.get('orderClientId')
    alphaXOrder.xtp_business_type = xtpOrder.get('xtpBusinessType')
    alphaXOrder.instrument_type = getInstrumentType(alphaXOrder.instrument_id,alphaXOrder.exchange_id)
    alphaXOrder.limit_price = xtpOrder.get('price')
    alphaXOrder.frozen_price = xtpOrder.get('price')
    alphaXOrder.volume = xtpOrder.get('quantity')
    alphaXOrder.volume_traded = xtpOrder.get('qtyTraded')
    alphaXOrder.volume_left = xtpOrder.get('qtyLeft')
    alphaXOrder.tax = None #todo:
    alphaXOrder.commission = None #todo:
    alphaXOrder.status = convertOrderStatus(xtpOrder.get('orderStatus')) if xtpOrder.get('orderStatus') else None # 实际没找到，对于能否找到要进行判断
    alphaXOrder.error_id = xtpOrder.get('xtpErrorId')
    alphaXOrder.error_msg = xtpOrder.get('xtpErrorMsg')
    alphaXOrder.side = convertSide(xtpOrder.get('xtpSideType'))
    alphaXOrder.offset = convertOffset(xtpOrder.get('xtpPositionEffectType')) if xtpOrder.get('xtpPositionEffectType') else None
    alphaXOrder.price_type = convertPriceType(xtpOrder.get('xtpPriceType')) if xtpOrder.get('xtpPriceType') else None
    alphaXOrder.volume_condition = VolumeCondition.Any #成交量类型
    alphaXOrder.time_condition = TimeCondition.GFD #成交时间类型  当日有效
    alphaXOrder.parent_order_id = xtpOrder.get('parentOrderId') if xtpOrder.get('parentOrderId') else xtpOrder.get('runtimeId')  #母订单ID xtpOrder.get('runtimeId']
    alphaXOrder.code = alphaXOrder.instrument_id + "." + getExchangeStrFromExchangeId(alphaXOrder.exchange_id)

    #以下是功夫缺少的
    alphaXOrder.traffic = xtpOrder.get('businessType') #业务渠道
    alphaXOrder.traffic_sub_id = xtpOrder.get('businessSubId') #业务子标识，一般填策略名称
    alphaXOrder.cancel_time = xtpOrder.get('cancelTime')
    alphaXOrder.order_cancel_client_id = xtpOrder.get('orderCancelClientId')
    alphaXOrder.order_cancel_xtp_id = xtpOrder.get('orderCancelXtpId')
    alphaXOrder.instrument_name = xtpOrder.get('tickerName')
    alphaXOrder.trade_amount = xtpOrder.get('tradeAmount')
    alphaXOrder.xtp_business_type = xtpOrder.get('xtpBusinessType')
    alphaXOrder.xtp_market_type = xtpOrder.get('xtpMarketType')

    #以下是冗余的xtp字段，用于得到xtp中的原值
    alphaXOrder.xtp_price_type = xtpOrder.get('xtpPriceType')
    alphaXOrder.xtp_position_effect_type = xtpOrder.get('xtpPositionEffectType')
    alphaXOrder.xtp_side_type = xtpOrder.get('xtpSideType')
    alphaXOrder.xtp_order_status = xtpOrder.get('orderStatus')
    alphaXOrder.business_type = xtpOrder.get('businessType')
    alphaXOrder.rowId = xtpOrder.get('rowId')


    #以下为xtp和alphax枚举值翻译为中文的名称
    alphaXOrder.exchange_id_name = dataTypeToName(alphaXOrder.exchange_id, "ALPHAX_EXCHANGE_TYPE") if not alphaXOrder.exchange_id == None else None
    alphaXOrder.instrument_type_name = dataTypeToName(alphaXOrder.instrument_type, "ALPHAX_INSTRUMENT_TYPE") if not alphaXOrder.instrument_type == None else None
    alphaXOrder.status_name = dataTypeToName(alphaXOrder.status, "ALPHAX_ORDER_STATUS") if not alphaXOrder.status == None else None
    alphaXOrder.side_name = dataTypeToName(alphaXOrder.side, "ALPHAX_SIDE") if not alphaXOrder.side == None else None
    alphaXOrder.offset_name = dataTypeToName(alphaXOrder.offset, "ALPHAX_OFFSET") if not alphaXOrder.offset == None else None
    alphaXOrder.price_type_name = dataTypeToName(alphaXOrder.price_type, "ALPHAX_PRICE_TYPE") if not alphaXOrder.price_type == None else None
    alphaXOrder.xtp_business_type_name = dataTypeToName(xtpOrder.get('xtpBusinessType'), "XTP_BUSINESS_TYPE") if xtpOrder.get('xtpBusinessType') else None

    alphaXOrder.xtp_market_name = dataTypeToName(xtpOrder.get('xtpMarketType'), "XTP_MARKET_TYPE") if xtpOrder.get('xtpMarketType') else None
    alphaXOrder.xtp_price_type_name = dataTypeToName(xtpOrder.get('xtpPriceType'), "XTP_PRICE_TYPE") if xtpOrder.get('xtpPriceType') else None
    alphaXOrder.xtp_position_effect_type_name = dataTypeToName(xtpOrder.get('xtpPositionEffectType'), "XTP_POSITION_EFFECT_TYPE") if xtpOrder.get('xtpPositionEffectType') else None
    alphaXOrder.xtp_side_type_name = transXtpSideType(xtpOrder.get('xtpSideType'), xtpOrder.get('xtpBusinessType'))
    alphaXOrder.xtp_order_status_name = dataTypeToName(xtpOrder.get('orderStatus') , "XTP_ORDER_STATUS_TYPE") if xtpOrder.get('orderStatus') else None
    alphaXOrder.volume_condition_name = dataTypeToName(alphaXOrder.volume_condition, "ALPHAX_VOLUME_TYPE") if not alphaXOrder.volume_condition == None else None
    alphaXOrder.time_condition_name = dataTypeToName(alphaXOrder.time_condition, "ALPHAX_TIME_TYPE") if not alphaXOrder.time_condition == None else None
    alphaXOrder.traffic_name = dataTypeToName(alphaXOrder.traffic, "SMART_BUSINESS_TYPE") if not alphaXOrder.traffic == None else None

    return alphaXOrder


'''
     接受smart框架的 账户级别的成交回报 向插件提供on_trade事件派发
    Trade 成交回报
    属性      	      类型	    说明                                          对应SMART字段         示例
    rcv_time	                    String	数据接收时间                                              "20200608140053830"
    order_id	                    String	委托编号ID(xtpid)                     orderXtpId         "36934130021173201"
    parent_order_id	            String	母单ID                               runtimeId           "6a1071e1-a94d-11ea-810c-4b25bab2cda3"
    trade_time	                String	成交时间                              tradeTime           "20200608140053830"
    instrument_id	            String	合约ID（证券代码）                     ticker              "600000"
    exchange_id	                String	交易所ID                             xtpMarketType转换    "SZE"
    account_id	                String	账号ID                               userName            "10912133333344"
    client_id	            String	用户自定义报单编号                     orderClientId(rowId优先)   "6a1071e1-a94d-11ea-810c-4b25bab2cda3"
    instrument_type	            Number	合约类型                              xtpBusinessType转换  InstrumentType.Stock
    side	                        Number	买卖方向                              xtpSideType
    offset	                    Number	开平方向                              xtpPositionEffectType
    price    	                Number	成交交割                              price                10.23
    volume	                    Number	成交数量                              quantity             100
    tax	                        Number	税                                   todo:
    commission	                Number	手续费                                todo:

    以下为新增：
    traffic                      String  业务渠道标识                           business_type        "AlphaX"
    traffic_sub_id               String  业务子标识，一般填策略名称               businessSubId        "网格交易"
    instrument_name              String  合约名称（证券名称）                    tickerName            "浦发银行"
    trade_amount                 Number  成交金额                              tradeAmount           0
    xtp_business_type            String  xtp证券业务类型                        xtpBusinessType       "XTP_BUSINESS_TYPE_CASH"
    xtp_market_type              String  xtp市场类型                           xtpMarketType         "XTP_MKT_SZ_A"

    xtp_exec_id                  String  成交编号()                            execId                "15790"
    xtp_report_index             String  成交序号()                            reportIndex           "6806"
    xtp_order_exch_id            String  报单编号 –交易所单号，上交所为空，深交所有此字段 orderExchId     ""
    xtp_trade_type               String  成交类型                              tradeType             "1" 代表XTP_TRDT_CASH 现金替代"
    xtp_branch_pbu               String  交易所交易员代码                       branchPbu             "13688"

    以下为xtp的冗余字段，为了获取xtp的原值
    xtp_position_effect_type     String  xtp开平方向                           xtpPositionEffectType "XTP_POSITION_EFFECT_OPEN"
    xtp_side_type                String  xtp交易方向                           xtpSideType           "XTP_SIDE_BUY"
    以下为xtp和alphax枚举值翻译为中文的名称
    exchange_id_name             String  交易所名称                                                  "上交所"
    instrument_type_name         String  合约类型名称                                                "股票"
    side_name                    String  买卖方向名称                                                "买"
    offset_name                  String  开平方向名称                                                "开"
    xtp_business_type_name       String  xtp证券业务类型名称                                          "现货"
    xtp_market_name              String  xtp市场类型名称                                             "沪市"
    xtp_price_type_name          String  xtp价格类型名称                                             "限价"
    xtp_position_effect_type_name String  xtp开平方向名称                                             "开"
    xtp_side_type_name           String  xtp交易方向名称                                             "买"
    traffic_name                 String  业务渠道名称                                                "策略"
'''
# 2022-4-13
def convertTradeFromSmartToPlugin(xtpTrade:dict):
    alphaXTrade = Trade()
    alphaXTrade.rcv_time = xtpTrade.get('tradeTime') #优先取updateTime  ???? todo：或许应该取smart server的时间
    alphaXTrade.order_id = xtpTrade.get('orderXtpId')
    alphaXTrade.parent_order_id =  xtpTrade.get('parentOrderId') if xtpTrade.get('parentOrderId') else xtpTrade.get('runtimeId') #母订单ID xtpTrade.get('runtimeId')
    alphaXTrade.trade_time = xtpTrade.get('tradeTime')
    alphaXTrade.instrument_id = xtpTrade.get('ticker')
    alphaXTrade.exchange_id = convertExchangeIdFromxtpMarketType(xtpTrade.get('xtpMarketType')) if xtpTrade.get('xtpMarketType') else None
    alphaXTrade.account_id = xtpTrade.get('userName')
    alphaXTrade.client_id = xtpTrade.get('orderClientId')
    alphaXTrade.instrument_type = getInstrumentType(alphaXTrade.instrument_id,alphaXTrade.exchange_id)
    alphaXTrade.side = convertSide(xtpTrade.get('xtpSideType'))
    alphaXTrade.offset = convertOffset(xtpTrade.get('xtpPositionEffectType')) if xtpTrade.get('xtpPositionEffectType') else None
    alphaXTrade.price = xtpTrade.get('price')
    alphaXTrade.volume = xtpTrade.get('quantity')
    alphaXTrade.tax = None #todo:
    alphaXTrade.commission = None #todo:
    alphaXTrade.code = alphaXTrade.instrument_id + "." + getExchangeStrFromExchangeId(alphaXTrade.exchange_id)

    #以下是功夫缺少的
    alphaXTrade.traffic = xtpTrade.get('businessType') # 业务渠道
    alphaXTrade.traffic_sub_id = xtpTrade.get('businessSubId') #业务子标识，一般填策略名称
    alphaXTrade.instrument_name = xtpTrade.get('tickerName')
    alphaXTrade.trade_amount = xtpTrade.get('tradeAmount')
    alphaXTrade.xtp_business_type = xtpTrade.get('xtpBusinessType')
    alphaXTrade.xtp_market_type = xtpTrade.get('xtpMarketType')

    alphaXTrade.xtp_exec_id = xtpTrade.get('execId') #成交编号，深交所唯一，上交所每笔交易唯一，当发现2笔成交回报拥有相同的exec_id，则可以认为此笔交易自成交  如"15790"
    alphaXTrade.xtp_report_index = xtpTrade.get('reportIndex') #成交序号 –回报记录号，每个交易所唯一,report_index+market字段可以组成唯一标识表示成交回报  如"6806"
    alphaXTrade.xtp_order_exch_id = xtpTrade.get('orderExchId') #报单编号 –交易所单号，上交所为空，深交所有此字段 如""
    alphaXTrade.xtp_trade_type = xtpTrade.get('tradeType') #成交类型 –成交回报中的执行类型  如'1'代表XTP_TRDT_CASH 现金替代
    alphaXTrade.xtp_branch_pbu = xtpTrade.get('branchPbu') #交易所交易员代码 如"13688"

    #以下是冗余的xtp字段，用于得到xtp中的原值
    alphaXTrade.xtp_position_effect_type = xtpTrade.get('xtpPositionEffectType')
    alphaXTrade.xtp_side_type = xtpTrade.get('xtpSideType')

    #以下为xtp和alphax枚举值翻译为中文的名称
    alphaXTrade.exchange_id_name = dataTypeToName(alphaXTrade.exchange_id, "ALPHAX_EXCHANGE_TYPE") if alphaXTrade.exchange_id else None
    alphaXTrade.instrument_type_name = dataTypeToName(alphaXTrade.instrument_type, "ALPHAX_INSTRUMENT_TYPE") if alphaXTrade.instrument_type else None
    alphaXTrade.side_name = dataTypeToName(alphaXTrade.side, "ALPHAX_SIDE") if alphaXTrade.side else None
    alphaXTrade.offset_name = dataTypeToName(alphaXTrade.offset, "ALPHAX_OFFSET") if alphaXTrade.offset else None
    alphaXTrade.xtp_business_type_name = dataTypeToName(xtpTrade.get('xtpBusinessType'), "XTP_BUSINESS_TYPE") if xtpTrade.get('xtpBusinessType') else None

    alphaXTrade.xtp_market_name = dataTypeToName(xtpTrade.get('xtpMarketType'), "XTP_MARKET_TYPE") if xtpTrade.get('xtpMarketType') else None
    alphaXTrade.xtp_position_effect_type_name = dataTypeToName(xtpTrade.get('xtpPositionEffectType'), "XTP_POSITION_EFFECT_TYPE") if xtpTrade.get('xtpPositionEffectType') else None
    alphaXTrade.xtp_side_type_name = transXtpSideType(xtpTrade.get('xtpSideType'), xtpTrade.get('xtpBusinessType'))
    alphaXTrade.xtp_trade_type_name = dataTypeToName(xtpTrade.get("tradeType"), "TXTPTradeTypeType") if xtpTrade.get("tradeType") else None
    alphaXTrade.traffic_name = dataTypeToName(alphaXTrade.traffic, "SMART_BUSINESS_TYPE") if not alphaXTrade.traffic == None else None

    alphaXTrade.rowId = xtpTrade.get('rowId')
    alphaXTrade.trade_id = alphaXTrade.xtp_business_type + "_" + alphaXTrade.xtp_market_type + "_" + alphaXTrade.xtp_exec_id + "_" + alphaXTrade.xtp_side_type + "_" + alphaXTrade.instrument_id + "_" + alphaXTrade.xtp_trade_type

    return alphaXTrade


# 2022-4-14 变更类
def convertAssetsFromSmartToPlugin(smartAssets:dict):
    pluginAssets = Assets()
    pluginAssets.total_asset = smartAssets.get('totalAsset') + smartAssets.get('marketCapitalization')
    pluginAssets.buying_power = smartAssets.get('buyingPower')
    pluginAssets.security_asset = smartAssets.get('securityAsset')

    pluginAssets.fund_buy_amount = smartAssets.get('fundBuyAmount')
    pluginAssets.fund_buy_fee = smartAssets.get('fundBuyFee')
    pluginAssets.fund_sell_amount = smartAssets.get('fundSellAmount')
    pluginAssets.fund_sell_fee = smartAssets.get('fundSellFee')
    pluginAssets.withholding_amount = smartAssets.get('withholdingAmount')

    pluginAssets.frozen_margin = smartAssets.get('frozenMargin')
    pluginAssets.frozen_exec_cash = smartAssets.get('frozenExecCash')
    pluginAssets.frozen_exec_fee = smartAssets.get('frozenExecFee')
    pluginAssets.pay_later = smartAssets.get('payLater')
    pluginAssets.preadva_pay = smartAssets.get('preadvaPay')
    pluginAssets.orig_banlance = smartAssets.get('origBanlance')
    pluginAssets.banlance = smartAssets.get('banlance')
    pluginAssets.deposit_withdraw = smartAssets.get('depositWithdraw')
    pluginAssets.trade_netting = smartAssets.get('tradeNetting')
    pluginAssets.captial_asset = smartAssets.get('totalAsset')
    pluginAssets.force_freeze_amount = smartAssets.get('forceFreezeAmount')
    pluginAssets.preferred_amount = smartAssets.get('preferredAmount')
    pluginAssets.market_value = smartAssets.get('marketCapitalization')# 市值的计算 应该在smart中订阅了行情算了推过来
    updateTime = smartAssets.get('updateTime')
    if(updateTime):pluginAssets.update_time = datetime.fromtimestamp(updateTime/ 1000, None).strftime("%H:%M:%S")
    return pluginAssets

# 2022-4-18 新增信用函数 TODO:
def convertCreditAssetsFromSmartToPlugin(creditAssets:dict):
    #填充信用资产信息
    pluginCreditAssets = {}
    if creditAssets.get("allAsset"): pluginCreditAssets["all_asset"] = creditAssets['allAsset']#总资产
    if creditAssets.get("allDebt"): pluginCreditAssets["all_debt"] = creditAssets['allDebt']#总负债
    if creditAssets.get("guaranty"): pluginCreditAssets["guaranty"] = creditAssets['guaranty']#两融保证金可用数
    if creditAssets.get("lineOfCredit"): pluginCreditAssets["line_of_credit"] = creditAssets['lineOfCredit']#两融授信额度
    if creditAssets.get("maintenanceRatio"): pluginCreditAssets["maintenance_ratio"] = creditAssets['maintenanceRatio']#维持担保品比例
    if creditAssets.get("remainAmount"): pluginCreditAssets["remain_amount"] = creditAssets['remainAmount']#信用账户待还资金
    if creditAssets.get("securityInterest"): pluginCreditAssets["security_interest"] = creditAssets['securityInterest']#融券合约利息
    if creditAssets.get("cashRemainAmt"): pluginCreditAssets["cash_remain_amt"] = creditAssets['cashRemainAmt']#融资合约金额
    if creditAssets.get("cashInterest"): pluginCreditAssets["cash_interest"] = creditAssets['cashInterest']#融资合约利息
    if creditAssets.get("extrasMoney"): pluginCreditAssets["extras_money"] = creditAssets['extrasMoney']#融券卖出所得购买货币基金占用金额
    return pluginCreditAssets

    '''
    * 将功夫平台的策略资产转换为插件中策略的资产格式
    * @param {Object} alphaxAssets - kungfu平台的策略资产
    * @returns 策略对象的book属性
    '''

# 2022-4-14 变更类
def convertPositionFromSmartToPlugin(smartPosition:dict):
    pluginPosition = Position()
    pluginPosition.instrument_id = smartPosition['ticker'] #合约ID（证券代码)
    pluginPosition.instrument_name = smartPosition['tickerName'] #证券名称
    pluginPosition.direction = convertDirectory(smartPosition['positionDirectionType']) # 持仓方向
    pluginPosition.direction_name = dataTypeToName(pluginPosition.direction, "ALPHAX_OPS_DIRECTION") if pluginPosition.direction else ''
    pluginPosition.name_py = smartPosition['namePy'] #拼音首字母  如"安诺其"为"anq"
    pluginPosition.volume = smartPosition['totalQty'] #持仓量
    pluginPosition.sellable_volume = smartPosition['sellableQty'] #可卖持仓
    pluginPosition.position_cost_price = smartPosition['avgPrice'] # 持仓成本 avgPrice
    pluginPosition.profit_price = smartPosition['profitPrice'] # 盈亏成本 profitPrice 在SDK1.1.0新增
    pluginPosition.last_price = 0 #最新价 todo:每次从smart一起推过来
    pluginPosition.unrealized_pnl = smartPosition['unrealizedPnl'] #浮动盈亏（保留字段,未计算） 未实现盈亏
    pluginPosition.yesterday_volume = smartPosition['yesterdayPosition'] #昨日持仓
    pluginPosition.purchase_redeemable_qty = smartPosition['purchaseRedeemableQty'] #今日申购赎回数量
    pluginPosition.executable_option = smartPosition['executableOption'] #可行权合约
    pluginPosition.executable_underlying = smartPosition['executableUnderlying'] #可行权标的
    pluginPosition.locked_position = smartPosition['lockedPosition'] #可锁定标的
    pluginPosition.usable_locked_position = smartPosition['usableLockedPosition'] #可用已锁定标的
    if (smartPosition['exchangeId'] == 1) :
        pluginPosition.exchange_id = Exchange.SSE #交易所ID   1:XTP_EXCHANGE_SH
    elif (smartPosition['exchangeId'] == 2) :
        pluginPosition.exchange_id = Exchange.SZE # 2:'XTP_EXCHANGE_SZ'
    elif (smartPosition['exchangeId'] == 3) :
        pluginPosition.exchange_id = Exchange.BSE # 2:'XTP_EXCHANGE_NQ'
    else:
        pluginPosition.exchange_id = Exchange.Unknown # 3:XTP_EXCHANGE_UNKNOWN
    pluginPosition.exchange_id_name = dataTypeToName(pluginPosition.exchange_id, "ALPHAX_EXCHANGE_TYPE") #交易所名称
    pluginPosition.xtp_market_type = smartPosition['xtpMarketType'] #交易市场
    pluginPosition.xtp_market_name = dataTypeToName(smartPosition['xtpMarketType'], "XTP_MARKET_TYPE") #交易市场名称
    pluginPosition._instrument_id_direction = str(pluginPosition.instrument_id) + '_' + str(pluginPosition.direction)
    # 市值
    if (isSPO(pluginPosition.instrument_id)):
        # 配股缴款
        pluginPosition.market_value = 0
    else:
        if (isReverseRepo(pluginPosition.instrument_id, pluginPosition.exchange_id)) :
            pluginPosition.market_value = 100 * pluginPosition.volume #国债逆回购
        else: 
            pluginPosition.market_value = pluginPosition.last_price * pluginPosition.volume #普通股票
    pluginPosition.code = pluginPosition.instrument_id + "." + getExchangeStrFromExchangeId(pluginPosition.exchange_id)
    return pluginPosition


# 2022-4-14
def convertQuoteFromSmartToPlugin(smartQuote:dict):
    pluginQuote = Quote()
    pluginQuote.source_id = smartQuote['source_id'] if 'source_id' in smartQuote else Source.XTP #源
    pluginQuote.trading_day= str(smartQuote['dataTime'])[0:8] #交易日
    pluginQuote.rcv_time= str(smartQuote['dataTime']) #数据接收时间 取的数据生成时间
    pluginQuote.data_time= str(smartQuote['dataTime'])#数据生成时间
    pluginQuote.instrument_id= smartQuote["ticker"] #合约ID(证券代码)
    pluginQuote.exchange_id= convertExchangeIdFromxtpExchangeId(smartQuote['exchangeId']) #交易所ID
    instrument = smart.getInstrument(pluginQuote.instrument_id, pluginQuote.exchange_id)
    pluginQuote.instrument_type= instrument.instrument_type if instrument.instrument_type else InstrumentType.Stock # 合约类型
    pluginQuote.pre_close_price= smartQuote['preClosePrice'] #昨收价
    pluginQuote.pre_settlement_price= None #昨结价 xtp缺少
    pluginQuote.last_price= smartQuote['lastPrice'] #最新价
    pluginQuote.volume= smartQuote['qty'] #成交数量
    pluginQuote.turnover= smartQuote['turnover'] #成交金额 xtp缺少
    pluginQuote.pre_open_interest= None #昨持仓量 xtp缺少
    pluginQuote.open_interest= None #持仓量 xtp缺少
    pluginQuote.open_price= smartQuote['openPrice'] #今开盘
    pluginQuote.high_price= smartQuote['highPrice'] #最高价
    pluginQuote.low_price= smartQuote['lowPrice'] #涨停板价
    pluginQuote.upper_limit_price= smartQuote['upperLimitPrice'] #涨停板价
    pluginQuote.lower_limit_price= smartQuote['lowerLimitPrice'] #跌停板价
    pluginQuote.close_price= smartQuote['closePrice'] #收盘价
    pluginQuote.settlement_price= None #结算价  xtp缺少
    pluginQuote.bid_price= smartQuote['bid'] #申买价 数组
    pluginQuote.ask_price= smartQuote['ask'] #申卖价 数组
    pluginQuote.bid_volume= smartQuote['bidQty'] #申买量 数组
    pluginQuote.ask_volume= smartQuote['askQty'] #申卖量 数组
    pluginQuote.code = pluginQuote.instrument_id + "." + getExchangeStrFromExchangeId(pluginQuote.exchange_id)
    # #以下是alphax缺少的
    pluginQuote.avg_price= smartQuote['avgPrice'] #当日均价
    pluginQuote.iopv= smartQuote['iopv'] #iopv
    pluginQuote.instrument_status= smartQuote['tickerStatus'] #证券状态
    return pluginQuote

#将指标行情转化为对象
def convertQuoteIndicatorFromSmartToPlugin(type:str,smartQuote:dict):
    pluginQuote = Bar()
    if type:
        pluginQuote.type = type
    else:
        pluginQuote.type = smartQuote['type']
    pluginQuote.code= smartQuote['code'] # 证券代码
    pluginQuote.instrument_id= smartQuote['instrument_id'] # 证券编号
    pluginQuote.exchange_id= smartQuote['exchange_id'] # 市场
    pluginQuote.trading_day= smartQuote['trading_day'] # 交易日
    pluginQuote.source_id = smartQuote['source_id'] # 柜台ID
    pluginQuote.start_time = smartQuote['start_time']  # 开始时间
    pluginQuote.end_time = smartQuote['end_time']  # 结束时间
    pluginQuote.time_interval = smartQuote['time_interval']  # 时间间隔，例如：1 单位分钟
    pluginQuote.period = smartQuote['period']  # 周期，例如 1m、2d、3w
    pluginQuote.high= smartQuote['high'] # 最高价
    pluginQuote.low= smartQuote['low'] # 最低价
    pluginQuote.open= smartQuote['open'] # 开盘价
    pluginQuote.close= smartQuote['close'] # 收盘价
    pluginQuote.volume = smartQuote['volume']  # 区间交易量
    pluginQuote.start_volume = smartQuote['start_volume']  # 初始总交易量:qty-volume
    pluginQuote.turnover = smartQuote['turnover']  # 区间成交金额
    pluginQuote.start_turnover = smartQuote['start_turnover']  # 初始总成交金额 total_turnover - turnover
    return pluginQuote

# 该转化动作专用于query_market_data_async接口的
def convertQuoteFromServerToPlugin(smartQuote):
    pluginQuote =  Quote()
    pluginQuote.source_id = smartQuote['source_id'] if 'source_id' in smartQuote else Source.XTP #源
    pluginQuote.trading_day = smartQuote['trading_day'] #交易日
    pluginQuote.rcv_time = smartQuote['trading_day']  + "" # 数据接收时间 取的数据生成时间
    pluginQuote.data_time = smartQuote['date_time']  + "" # 数据生成时间
    pluginQuote.instrument_id = smartQuote['instrument_id']  # 合约ID(证券代码)
    pluginQuote.exchange_id = smartQuote['exchange_id']  # 交易所ID
    pluginQuote.instrument_type = InstrumentType.Stock  # 
    pluginQuote.pre_close_price = smartQuote['pre_close_price']  # 昨收价
    pluginQuote.pre_settlement_price = None # 昨结价 xtp缺少
    pluginQuote.last_price = smartQuote['last_price']  # 最新价
    pluginQuote.volume = smartQuote['volume']  # 成交数量
    pluginQuote.turnover = smartQuote['turnover']  # 成交金额 xtp缺少
    pluginQuote.pre_open_interest = None # 昨持仓量 xtp缺少
    pluginQuote.open_interest = None # 持仓量 xtp缺少
    pluginQuote.open_price = smartQuote['open_price']  # 今开盘
    pluginQuote.high_price = smartQuote['high_price']  # 最高价
    pluginQuote.low_price = smartQuote['low_price']  # 涨停板价
    pluginQuote.upper_limit_price = smartQuote['upper_limit_price']  # 涨停板价
    pluginQuote.lower_limit_price = smartQuote['lower_limit_price']  # 跌停板价
    pluginQuote.close_price = smartQuote['close_price'] if 'close_price' in smartQuote else 0 # 收盘价
    pluginQuote.settlement_price = None # 结算价  xtp缺少
    pluginQuote.bid_price = smartQuote['bid_price']  # 申买价 数组
    pluginQuote.ask_price = smartQuote['ask_price']  # 申卖价 数组
    pluginQuote.bid_volume = smartQuote['bid_volume']  # 申买量 数组
    pluginQuote.ask_volume = smartQuote['ask_volume']  # 申卖量 数组
    pluginQuote.code = smartQuote['code']  # 证券代码['交易所标识
    # 以下是alphax缺少的
    pluginQuote.avg_price = None # 当日均价
    pluginQuote.iopv = None  # iopv
    pluginQuote.instrument_status = None  # 证券状态
    return pluginQuote

INSTRUCTMENT_TYPE_MAPPING = {
    # InstrumentType.Stock
    "XTP_BUSINESS_TYPE_CASH": InstrumentType.Stock,
    "XTP_BUSINESS_TYPE_IPOS": InstrumentType.Stock,
    "XTP_BUSINESS_TYPE_ETF": InstrumentType.Stock,
    "XTP_BUSINESS_TYPE_MARGIN": InstrumentType.Stock,
    "XTP_BUSINESS_TYPE_DESIGNATION": InstrumentType.Stock,
    "XTP_BUSINESS_TYPE_ALLOTMENT": InstrumentType.Stock,
    "XTP_BUSINESS_TYPE_STRUCTURED_FUND_PURCHASE_REDEMPTION": InstrumentType.Stock,
    "XTP_BUSINESS_TYPE_STRUCTURED_FUND_SPLIT_MERGE": InstrumentType.Stock,
    "XTP_BUSINESS_TYPE_MONEY_FUND": InstrumentType.Stock,
    # InstrumentType.Future
    "XTP_BUSINESS_TYPE_OPTION": InstrumentType.Future,
    "XTP_BUSINESS_TYPE_EXECUTE": InstrumentType.Future,
    # InstrumentType.Bond
    "XTP_BUSINESS_TYPE_REPO": InstrumentType.Bond
}

def convertInstructmentTypeFromXtpBusinessType(xtpBusinessType:str)->int:
    instrument_type = INSTRUCTMENT_TYPE_MAPPING[xtpBusinessType]
    if (not instrument_type):
        instrument_type = InstrumentType.Unknown
    
    return instrument_type


def convertDirectory(positionDirectionType:str)->int:
    if (positionDirectionType == 'XTP_POSITION_DIRECTION_NET') :
        return Direction.Net
    elif (positionDirectionType == 'XTP_POSITION_DIRECTION_LONG') :
        return Direction.Long
    elif (positionDirectionType == 'XTP_POSITION_DIRECTION_SHORT') :
        return Direction.Short
    elif (positionDirectionType == 'XTP_POSITION_DIRECTION_COVERED'):
         return Direction.Covered


def convertExchangeIdFromxtpMarketType(xtpMarketType:str)->str:
    if (xtpMarketType == 'XTP_MKT_SH_A' or xtpMarketType == 2) :
        return Exchange.SSE
    elif (xtpMarketType == 'XTP_MKT_SZ_A' or xtpMarketType == 1) :
        return Exchange.SZE
    elif (xtpMarketType == 'XTP_MKT_BJ_A' or xtpMarketType == 2) :
        return Exchange.BSE
    elif (xtpMarketType == 'XTP_MKT_HS') :
        return Exchange.HSE
    elif (xtpMarketType == 'XTP_MKT_XG') :
        return Exchange.XGE
    elif (xtpMarketType == 'XTP_MKT_YT') :
        return Exchange.YTE
    elif (xtpMarketType == 'XTP_MKT_ZQ') :
        return Exchange.ZQE
    elif (xtpMarketType == 'XTP_MKT_QT') :
        return Exchange.QTE
    elif (xtpMarketType == 'XTP_MKT_QQ') :
        return Exchange.QQE
    return Exchange.Unknown


def convertExchangeIdFromxtpExchangeId(xtpExchangeId:str)->str:
    if (xtpExchangeId == 'XTP_EXCHANGE_SH'):
        return Exchange.SSE #交易所ID
    elif (xtpExchangeId == 'XTP_EXCHANGE_SZ') :
        return Exchange.SZE
    elif (xtpExchangeId == 'XTP_EXCHANGE_NQ') :
        return Exchange.BSE
    elif (xtpExchangeId == "XTP_EXCHANGE_HS") :
        return Exchange.HSE
    elif (xtpExchangeId == "XTP_EXCHANGE_XG") :
        return Exchange.XGE
    elif (xtpExchangeId == "XTP_EXCHANGE_YT") :
        return Exchange.YTE
    elif (xtpExchangeId == "XTP_EXCHANGE_ZQ") :
        return Exchange.ZQE
    elif (xtpExchangeId == "XTP_EXCHANGE_QT") :
        return Exchange.QTE
    elif (xtpExchangeId == "XTP_EXCHANGE_QQ") :
        return Exchange.QQE
    else:
        return Exchange.Unknown


def converXTPExchangeIdFromExchangeId(exchange_id:str)->int:
    if (exchange_id == Exchange.SSE) :
        return 1
    if (exchange_id == Exchange.SZE) :
        return 2
    if (exchange_id == Exchange.BSE) :
        return 3
    return 4


XTP_ORDER_STATUS_MAPPING = {
    "XTP_ORDER_STATUS_INIT": OrderStatus.Submitted,
    "XTP_ORDER_STATUS_ALLTRADED": OrderStatus.Filled,
    "XTP_ORDER_STATUS_PARTTRADEDQUEUEING": OrderStatus.PartialFilledActive,
    "XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING": OrderStatus.PartialFilledNotActive,
    "XTP_ORDER_STATUS_NOTRADEQUEUEING": OrderStatus.Pending,
    "XTP_ORDER_STATUS_CANCELED": OrderStatus.Cancelled,
    "XTP_ORDER_STATUS_REJECTED": OrderStatus.Error
}

def convertOrderStatus(xtpOrderStatus:str)->int:
    return XTP_ORDER_STATUS_MAPPING[xtpOrderStatus] or OrderStatus.Unknown


ALPHAX_ORDER_STATUS_MAPPING = [
    "XTP_ORDER_STATUS_UNKNOWN", # 0
    "XTP_ORDER_STATUS_INIT", # 1
    "XTP_ORDER_STATUS_NOTRADEQUEUEING", # 2
    "XTP_ORDER_STATUS_CANCELED", # 3
    "XTP_ORDER_STATUS_REJECTED", # 4
    "XTP_ORDER_STATUS_ALLTRADED", # 5
    "XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING", # 6
    "XTP_ORDER_STATUS_PARTTRADEDQUEUEING" # 7
]



#####################/ 策略状态
def convertStrategyStatusToChiness(status:str)->str:
    if (status == StrategyStatus.Unknown):
         return ''
    elif (status == StrategyStatus.Starting):
         return '启动中'
    elif (status == StrategyStatus.Started) :
        return '已启动'
    elif (status == StrategyStatus.Pause) :
        return '暂停'
    elif (status == StrategyStatus.Stopping):
         return '停止中'
    elif (status == StrategyStatus.Stopped) :
        return '已停止'
    elif (status == StrategyStatus.Errored) :
        return '错误'

#####################/ 证券类型
'''
 * XTP中的证券类型，对应到插件中的证券类型
'''
secrityTypeMap = {
    "XTP_SECURITY_MAIN_BOARD": InstrumentType.Stock,#主板股票,
    "XTP_SECURITY_SECOND_BOARD": InstrumentType.Stock,#中小板股票
    "XTP_SECURITY_STARTUP_BOARD": InstrumentType.Stock,#创业板股票 
    "XTP_SECURITY_TECH_BOARD": InstrumentType.Stock,#科创板股票(上海) 
    "XTP_SECURITY_ALLOTMENT": InstrumentType.Stock,#配股
    "XTP_SECURITY_INDEX": InstrumentType.Index,#指数
    "XTP_SECURITY_STATE_BOND": InstrumentType.Bond,#国债 
    "XTP_SECURITY_ENTERPRICE_BOND": InstrumentType.Bond,#企业债 
    "XTP_SECURITY_COMPANEY_BOND": InstrumentType.Bond,#公司债 
    "XTP_SECURITY_CONVERTABLE_BOND": InstrumentType.Bond,#转换债券 
    "XTP_SECURITY_NATIONAL_BOND_REVERSE_REPO": InstrumentType.Bond,#国债逆回购 
    "XTP_SECURITY_ETF_SINGLE_MARKET_STOCK": InstrumentType.Fund,#本市场股票ETF
    "XTP_SECURITY_ETF_INTER_MARKET_STOCK": InstrumentType.Fund,#跨市场股票ETF
    "XTP_SECURITY_ETF_CROSS_BORDER_STOCK": InstrumentType.Fund,#跨境股票ETF
    "XTP_SECURITY_ETF_SINGLE_MARKET_BOND": InstrumentType.Fund,#本市场实物债券ETF
    "XTP_SECURITY_TYPE_ETF_CASH_BOND": InstrumentType.Fund,#现金债券ETF
    "XTP_SECURITY_ETF_GOLD": InstrumentType.Fund,#黄金ETF
    "XTP_SECURITY_ETF_COMMODITY_FUTURES": InstrumentType.Fund,#商品期货ETF
    "XTP_SECURITY_STRUCTURED_FUND_CHILD": InstrumentType.Fund,#分级基金子基金
    "XTP_SECURITY_SZSE_RECREATION_FUND": InstrumentType.Fund,#深交所仅申赎基金
    "XTP_SECURITY_MONETARY_FUND_SHCR": InstrumentType.Fund,#上交所申赎型货币基金
    "XTP_SECURITY_MONETARY_FUND_SHTR": InstrumentType.Fund,#上交所交易型货币基金
    "XTP_SECURITY_MONETARY_FUND_SZ": InstrumentType.Fund,#深交所货币基金
    "XTP_SECURITY_STOCK_OPTION": InstrumentType.StockOption,#个股期权
    "XTP_SECURITY_ETF_OPTION": InstrumentType.StockOption,#ETF期权
    "XTP_SECURITY_OTHERS": InstrumentType.Unknown,#其他
    "XTP_TICKER_TYPE_STOCK": InstrumentType.Stock,#股票
    "XTP_TICKER_TYPE_INDEX": InstrumentType.Index,#指数 
    "XTP_TICKER_TYPE_FUND": InstrumentType.Fund,#黄金ETF
    'XTP_TICKER_TYPE_BOND': InstrumentType.Bond,#国债逆回购 
    'XTP_TICKER_TYPE_OPTION': InstrumentType.StockOption,#个股期权
    'XTP_TICKER_TYPE_TECH_STOCK': InstrumentType.Stock,#科创股票
    'XTP_TICKER_TYPE_UNKNOWN': InstrumentType.Unknown,#其他
}

'''
 * 将xtp中的插件类型转换为插件中的证券类型
 * @param {String xtpSecurityType xtp中的证券类型
 * @returns String - 插件中的证券类型
'''
def convertInstrumentTypeFromXtpSecurityType(xtpSecurityType:str)->str:
    return secrityTypeMap[xtpSecurityType] or InstrumentType.Unknown


#####################/ 买卖方向
SIDE_MAPPING = {
    "XTP_SIDE_BUY": Side.Buy,
    "XTP_SIDE_SELL": Side.Sell,
    "XTP_SIDE_PURCHASE": Side.Purchase, #申购
    "XTP_SIDE_REDEMPTION": Side.Pedemption, #赎回
    "XTP_SIDE_SPLIT": Side.Split, #拆分
    "XTP_SIDE_MERGE": Side.Merge, #合并
    "XTP_SIDE_COVER": Side.Cover, #备兑
    'XTP_SIDE_FREEZE': Side.Lock, #锁仓  冻结
    'XTP_SIDE_MARGIN_TRADE': Side.MarginTrade, #融资买入
    'XTP_SIDE_SHORT_SELL': Side.ShortSell, #融券卖出
    'XTP_SIDE_REPAY_MARGIN': Side.RepayMargin, #卖券还款
    'XTP_SIDE_REPAY_STOCK': Side.RepayStock, # 买券还券
    'XTP_SIDE_STOCK_REPAY_STOCK': Side.StockRepayStock, #现券还券
    'XTP_SIDE_SURSTK_TRANS': Side.SurstkTrans, #余券划转
    'XTP_SIDE_GRTSTK_TRANSIN': Side.GrtstkTransin, #担保品转入
    'XTP_SIDE_GRTSTK_TRANSOUT': Side.GrtstkTransout, #担保品转出
}

# TODO 缺少Unlock解锁  Exec行权  Drop放弃行权
SIDE_KF_MAPPING = [Side.Buy, Side.Sell, Side.Lock]

def convertSide(xtpSideType:str)->int:
    return SIDE_MAPPING[xtpSideType] or Side.Unknown
    #xtp缺少  Unlock解锁  Exec行权  Drop放弃行权？


#####################/ 开平标志
POSITION_EFFECT_MAPPING = {
    'XTP_POSITION_EFFECT_INIT': Offset.Init, #初始，用于现货
    'XTP_POSITION_EFFECT_OPEN': Offset.Open, #开
    'XTP_POSITION_EFFECT_CLOSE': Offset.Close, #平
    'XTP_POSITION_EFFECT_CLOSETODAY': Offset.CloseToday, #平今
    'XTP_POSITION_EFFECT_CLOSEYESTERDAY': Offset.CloseYesterday, #平昨
    'XTP_POSITION_EFFECT_FORCECLOSE': Offset.ForceClose, #强平
    'XTP_POSITION_EFFECT_FORCEOFF': Offset.ForceOff, #强减
    'XTP_POSITION_EFFECT_LOCALFORCECLOSE': Offset.LocalForceClose, #本地强平
    'XTP_POSITION_EFFECT_CREDIT_FORCE_COVER': Offset.CreditForceCover, #信用业务追保强平
    'XTP_POSITION_EFFECT_CREDIT_FORCE_CLEAR': Offset.CreditForceClear, #信用业务清偿强平
    'XTP_POSITION_EFFECT_CREDIT_FORCE_DEBT': Offset.CreditForceDebt, #信用业务合约到期强平
    'XTP_POSITION_EFFECT_CREDIT_FORCE_UNCOND': Offset.CreditForceUncond #信用业务清偿强平
}

def convertOffset(xtpPositionEffectType:str)->int:
    return POSITION_EFFECT_MAPPING[xtpPositionEffectType] or Offset.Unknown


#####################/ 价格条件

XTP_PRICE_TYPE_MAPPING = {
    'XTP_PRICE_LIMIT': PriceType.Limit, #限价
    'XTP_PRICE_BEST_OR_CANCEL': PriceType.Fak, #即时成交剩余转撤销，市价单-深 / 沪期权
    'XTP_PRICE_BEST5_OR_LIMIT': PriceType.ReverseBest, #最优五档即时成交剩余转限价，市价单-沪
    'XTP_PRICE_BEST5_OR_CANCEL': PriceType.FakBest5, #最优五档即时成交剩余转撤销，市价单-沪深
    'XTP_PRICE_ALL_OR_CANCEL': PriceType.Fok, #全部成交或撤销,市价单-深 / 沪期权
    'XTP_PRICE_FORWARD_BEST': PriceType.ForwardBest, #本方最优，市价单-深
    'XTP_PRICE_REVERSE_BEST_LIMIT': PriceType.ReverseBest, #对方最优剩余转限价，市价单-深 / 沪期权
    'XTP_PRICE_LIMIT_OR_CANCEL': PriceType.Fok, #期权限价申报FOK  ?
}

def convertPriceType(xtpPriceType:str)->int:
    return XTP_PRICE_TYPE_MAPPING[xtpPriceType] or PriceType.Unknown #未知或者无效价格类型


ALPHAX_PRICE_TYPE_MAPPING = [
    PriceType.Limit,
    PriceType.Any,
    PriceType.FakBest5,
    PriceType.ForwardBest,
    PriceType.ReverseBest,
    PriceType.Fak,
    PriceType.Fok,
    PriceType.Unknown
]



def convertCreditTickerAssignInfoFromSmartToPlugin(item:dict)->CreditTickerAssignInfo:
    exchange_id = convertExchangeIdFromxtpMarketType(item.get('marketType')) if item.get('marketType') else None
    assignInfo = CreditTickerAssignInfo()
    assignInfo.instrument_id = item.get('ticker')
    assignInfo.instrument_name = item.get('tickerName')
    assignInfo.exchange_id = exchange_id
    assignInfo.exchange_id_name = dataTypeToName(exchange_id, "ALPHAX_EXCHANGE_TYPE") if exchange_id else None  #交易所名称
    assignInfo.name_py = item.get('namePy')
    assignInfo.limit_volume = item.get('limitQty')
    assignInfo.left_volume = item.get('leftQty')
    assignInfo.frozen_volume = item.get('frozenQty')
    assignInfo.yesterday_volume = item.get('yesterdayQty')
    assignInfo.xtp_market_type = item.get('marketType')
    assignInfo.code = assignInfo.instrument_id + "." + getExchangeStrFromExchangeId(assignInfo.exchange_id)
    return assignInfo

def convertCreditDebtFinanceFromSmartToPlugin(item:dict)->CreditDebtFinance:
    exchange_id = convertExchangeIdFromxtpMarketType(item['marketType']) 
    debt = CreditDebtFinance() 
    debt.debt_id = item['debtId']   # 负债合约编号
    debt.instrument_id = item['ticker']   # 证券代码
    debt.instrument_name = item['tickerName']   # 证券名称
    debt.exchange_id = exchange_id   # 交易所id
    debt.exchange_id_name = dataTypeToName(exchange_id, "ALPHAX_EXCHANGE_TYPE")   #交易所名称
    debt.name_py = item['namePy']   # 拼音首字母  如"安诺其"为"anq"  alphax缺少
    debt.xtp_market_type = item['marketType']   #  xtp交易市场
    debt.remain_amt = item['remainAmt']   # 未偿还金额
    debt.remain_principal = item['remainPrincipal']   # 未偿还本金
    debt.remain_interest = item['remainInterest']  # 未偿还利息
    debt.debt_status = item['debtStatus']  #合约状态
    debt.end_date = item['endDate']  #负债截止日期
    debt.orig_end_date = item['origEndDate']  #负债原始截止日期
    debt.order_xtp_id = item['orderXtpId']  #负债订单编号
    debt.order_date = item['orderDate'] #委托日期
    debt.extended = item['extended']  #是否接收到展期
    debt.code = debt.instrument_id + "." + getExchangeStrFromExchangeId(debt.exchange_id)
    return debt 

def convertCreditDebtSecurityFromSmartToPlugin(item:dict)->CreditDebtSecurity:
    exchange_id = convertExchangeIdFromxtpMarketType(item['marketType'])
    debt = CreditDebtSecurity()
    debt.debt_id = item['debtId'] # 负债合约编号
    debt.instrument_id = item['ticker'] # 证券代码
    debt.instrument_name = item['tickerName'] # 证券名称
    debt.exchange_id = exchange_id # 交易所id
    debt.exchange_id_name = dataTypeToName(exchange_id, "ALPHAX_EXCHANGE_TYPE") #交易所名称
    debt.name_py = item['namePy'] # 拼音首字母  如"安诺其"为"anq"  alphax缺少
    debt.xtp_market_type = item['marketType'] #  xtp交易市场
    debt.due_right_volume = item['dueRightQty'] # 未偿还金额
    debt.remain_volume = item['remainQty'] # 未偿还本金
    debt.remain_interest = item['remainInterest'] # 未偿还利息
    debt.debt_status = item['debtStatus'] #合约状态
    debt.end_date = item['endDate'] #负债截止日期
    debt.orig_end_date = item['origEndDate'] #负债原始截止日期
    debt.order_xtp_id = item['orderXtpId'] #负债订单编号
    debt.order_date = item['orderDate'] #委托日期
    debt.extended = item['extended'] #是否接收到展期
    debt.code = debt.instrument_id + "." + getExchangeStrFromExchangeId(debt.exchange_id)
    return debt

'''
 * 通过交易所类型转换为xtp的MarketType
 * exchange_id ：如'SZE'
 * @param {string  xtp的MarketType 如'XTP_MKT_SZ_A'
'''
def getXtpMarketTypeFromExchange(exchange_id:str)->str:
    if (exchange_id == Exchange.SSE):
         return 'XTP_MKT_SH_A'
    elif (exchange_id == Exchange.SZE):
         return 'XTP_MKT_SZ_A'
    elif (exchange_id == Exchange.BSE):
         return 'XTP_MKT_BJ_A'
    elif (exchange_id == Exchange.HSE):
         return 'XTP_MKT_HS'
    elif (exchange_id == Exchange.XGE):
         return 'XTP_MKT_XG'
    elif (exchange_id == Exchange.YTE):
         return 'XTP_MKT_YT'
    elif (exchange_id == Exchange.ZQE):
         return 'XTP_MKT_ZQ'
    elif (exchange_id == Exchange.QTE):
         return 'XTP_MKT_QT'
    elif (exchange_id == Exchange.QQE):
         return 'XTP_MKT_QQ'
    else: 
        return 'XTP_EXCHANGE_UNKNOWN'

'''
 * 通过交易所标识转换为交易所ID
 * exchange_id ：如'SZE'
 * @param {string  xtp的MarketType 如'XTP_MKT_SZ_A'
'''
def getExchangeIdFromExchangeStr(exchangeStr:str)->str:
    if (exchangeStr == "SH"):
        return Exchange.SSE
    elif (exchangeStr == "SZ"):
        return Exchange.SZE
    elif (exchangeStr == "BJ"):
        return Exchange.BSE
    elif (exchangeStr == "HS"):
        return Exchange.HSE
    elif (exchangeStr == "XG"):
        return Exchange.XGE
    elif (exchangeStr == "YT"):
        return Exchange.YTE
    elif (exchangeStr == "ZQ"):
        return Exchange.ZQE
    elif (exchangeStr == "QT"):
        return Exchange.QTE
    elif (exchangeStr == "QQ"):
        return Exchange.QQE
    else: 
        return  Exchange.Unknown

'''
 * 校验code并通过code获取instrument_id和exchange_id
 * instrument_id:如'600000',exchange_id如'Exchange.SSE'
 * @param {string  code 如'600000.SH'
'''
def getInstrumentIdAndExchangeIdFromCode(code:str):
    code = code.upper() #默认转大写
    result = code.partition(".") #按照.拆分成三元组("600000",".","SH")
    if not result[0] or not result[2]:
        msg = f"code传参{code}的格式错误,格式应如：600000.SH"
        params = {
            "level": "error",
            "title": "bar行情订阅或取消订阅的code格式错误",
            "msg": msg,
        }
        smart.notice(params)
        raise Exception(msg)
    instrument_id = result[0]
    exchange_id = getExchangeIdFromExchangeStr(result[2])
    if exchange_id == Exchange.Unknown:
        raise Exception(f"code传参{code}交易所标识格式错误,格式应如：SZ SH BJ")
    return instrument_id, exchange_id

'''
 * 通过交易所ID转换为交易所标识
 * exchange_str ：如'600018.SH'
 * @param {string  exchangeId 交易所ID
'''
def getExchangeStrFromExchangeId(exchangeId:str)->str:
    if (exchangeId == Exchange.SSE):
        return "SH"
    elif (exchangeId == Exchange.SZE):
        return "SZ"
    elif (exchangeId == Exchange.BSE):
        return "BJ"
    elif (exchangeId == Exchange.HSE):
        return "HS"
    elif (exchangeId == Exchange.XGE):
        return "XG"
    elif (exchangeId == Exchange.YTE):
        return "YT"
    elif (exchangeId == Exchange.ZQE):
        return "ZQ"
    elif (exchangeId == Exchange.QTE):
        return "QT"
    elif (exchangeId == Exchange.QQE):
        return "QQ"
    else: 
        return ""

'''
 * 通过买卖方向类型转换为xtp的SideType
 * side ：数字
 * @param {string  xtp的SideType 如'XTP_SIDE_BUY'
'''
SIDE_MAPPING2 = {
    1: 'XTP_SIDE_BUY',
    2: 'XTP_SIDE_SELL',
    12: 'XTP_SIDE_FREEZE',
    7: 'XTP_SIDE_PURCHASE',
    8: 'XTP_SIDE_REDEMPTION',
    9: 'XTP_SIDE_SPLIT',
    10: 'XTP_SIDE_MERGE',
    11: 'XTP_SIDE_COVER',
    21: 'XTP_SIDE_MARGIN_TRADE',
    22: 'XTP_SIDE_SHORT_SELL',
    23: 'XTP_SIDE_REPAY_MARGIN',
    24: 'XTP_SIDE_REPAY_STOCK',
    26: 'XTP_SIDE_STOCK_REPAY_STOCK',
    27: 'XTP_SIDE_SURSTK_TRANS',
    28: 'XTP_SIDE_GRTSTK_TRANSIN',
    29: 'XTP_SIDE_GRTSTK_TRANSOUT',
    0: 'XTP_SIDE_UNKNOWN'
}

def getXtpSideTypeFromSide(side:int)->str:
    xtpSide = SIDE_MAPPING2[side]
    if (not xtpSide):
        return 'XTP_SIDE_UNKNOWN'
    
    return xtpSide


BUSINESS_TYPE_MAPPING2 = {
    0: 'XTP_BUSINESS_TYPE_CASH',
    2: 'XTP_BUSINESS_TYPE_REPO',
    3: 'XTP_BUSINESS_TYPE_ETF',
    4: 'XTP_BUSINESS_TYPE_MARGIN',
    13: 'XTP_BUSINESS_TYPE_UNKNOWN'
}

def getXtpBusinessTypeFromBusinessType(business_type:int)->str:
    xtpBusinessType = BUSINESS_TYPE_MAPPING2[business_type]
    if (not xtpBusinessType):
        return 'XTP_BUSINESS_TYPE_UNKNOWN'
    return xtpBusinessType



'''
 * 通过开平方向类型转换为xtp的持仓开平方向
 * offset ：数字
 * @param {string   如'XTP_POSITION_EFFECT_OPEN'
'''
POSITION_EFFECT_MAPPING2 = {
    0: 'XTP_POSITION_EFFECT_OPEN',
    1: 'XTP_POSITION_EFFECT_CLOSE',
    2: 'XTP_POSITION_EFFECT_CLOSETODAY',
    3: 'XTP_POSITION_EFFECT_CLOSEYESTERDAY',
    13: 'XTP_POSITION_EFFECT_FORCECLOSE',
    6: 'XTP_POSITION_EFFECT_FORCEOFF',
    7: 'XTP_POSITION_EFFECT_LOCALFORCECLOSE',
    8: 'XTP_POSITION_EFFECT_CREDIT_FORCE_COVER',
    9: 'XTP_POSITION_EFFECT_CREDIT_FORCE_CLEAR',
    10: 'XTP_POSITION_EFFECT_CREDIT_FORCE_DEBT',
    11: 'XTP_POSITION_EFFECT_CREDIT_FORCE_UNCOND',
    100: 'XTP_POSITION_EFFECT_INIT',
    12: 'XTP_POSITION_EFFECT_UNKNOWN'
}

def getXtpOffsetTypeFromOffset(offset:int)->str:
    xtpOffset = POSITION_EFFECT_MAPPING2[offset]
    if (not xtpOffset):
        return 'XTP_POSITION_EFFECT_UNKNOWN'
    
    return xtpOffset

'''
 * 通过价格类型和交易所类型转换为xtp的价格类型
 * priceType ：数字  exchange_id
 * @param {string   如'XTP_PRICE_LIMIT'
'''
PRICE_TYPE_MAPPING = {
    0: 'XTP_PRICE_TYPE_UNKNOWN',
    1: 'XTP_PRICE_LIMIT',
    2: {
        "SSE": 'XTP_PRICE_BEST5_OR_CANCEL',
        "SZE": 'XTP_PRICE_BEST_OR_CANCEL'
    }
    ,
    4: 'XTP_PRICE_BEST5_OR_CANCEL',
    6: 'XTP_PRICE_FORWARD_BEST',
    3: {
        "SSE": 'XTP_PRICE_BEST5_OR_LIMIT',
        "SZE": 'XTP_PRICE_REVERSE_BEST_LIMIT'
    },
    5: {
        "SZE": 'XTP_PRICE_ALL_OR_CANCEL'
    }
    
}

def getXtpPriceTypeFromPriceTypeWithExchange(priceType:int, exchange_id:str)->str:
    xtpPriceType = PRICE_TYPE_MAPPING.get(priceType)
    if (isinstance(xtpPriceType,str)):
        return xtpPriceType
    

    if (xtpPriceType and isinstance(xtpPriceType,object)):
        xtpPriceType = xtpPriceType.get(exchange_id,"XTP_PRICE_TYPE_UNKNOWN")
        if (isinstance(xtpPriceType,str)):
            return xtpPriceType

    return 'XTP_PRICE_TYPE_UNKNOWN'

'''
* 是否是普通股票
* @param {string} instrumentId 股票代码
'''
def isStock(instrumentId, exchangeId) :
    if (not instrumentId) :
        return False
    #按照静态行情中的股票代码判断科创板股票。
    try:
        stock = smart.instrument_map[instrumentId + "_" + exchangeId]
        if (not stock) :
            return False
    except Exception as e:
        return False
    return stock.instrument_type_ext == "XTP_SECURITY_MAIN_BOARD" or stock.instrument_type_ext == "XTP_SECURITY_SECOND_BOARD" or stock.instrument_type_ext == "XTP_SECURITY_STARTUP_BOARD" or stock.instrument_type_ext == "XTP_SECURITY_TECH_BOARD"

'''
 * 是否科创板股票
 * 科创板 ：Science and technology innovation board
 * @param {string instrument_id 股票代码
'''
def isSTIStock(instrument_id:str)->bool:

    if (not instrument_id) :return False
    # 按照静态行情中的股票代码判断科创板股票。
    stock = getTickerByCode(instrument_id)
    if (not stock):return False
    return stock.instrument_type_ext == "XTP_SECURITY_TECH_BOARD"

'''
 * 是否创业板股票
 * 创业板 ：Second-board Market
 * @param {string} instrument_id 股票代码     
'''
def isSBMStock(instrument_id:str)->bool:
        if (not instrument_id) : return False
        stock = getTickerByCode(instrument_id)
        if (not stock): return False
        return stock.instrument_type_ext == "XTP_SECURITY_STARTUP_BOARD"


'''
 * 判断股票下单价格类型是否是科创板的市价
 * @param {string instrument_id 股票代码
 * @param {integer xtpPriceType 下单价格条件
'''
def isSTIMarketOrder(instrument_id:str, xtpPriceType:int)->bool:
    isSTI = isSTIStock(instrument_id)
    if (not isSTI): return False
    return xtpPriceType in [3, 4, 6, 7]

'''
 * 是否ETF基金
 * @param {string instrument_id 股票代码
 * add by sunlh 2020.4.2
'''
def isETF(instrument_id:str)->bool:
    if (not instrument_id):
        return False
    
    stock = getTickerByCode(instrument_id)
    if (not stock) :
        return False
    etfTypes = ["XTP_SECURITY_ETF_SINGLE_MARKET_STOCK", "XTP_SECURITY_ETF_INTER_MARKET_STOCK", "XTP_SECURITY_ETF_CROSS_BORDER_STOCK", "XTP_SECURITY_TYPE_ETF_CASH_BOND", "XTP_SECURITY_ETF_GOLD", "XTP_SECURITY_ETF_COMMODITY_FUTURES", "XTP_SECURITY_ETF_SINGLE_MARKET_BOND"]
    return stock.instrument_type_ext in etfTypes

def getTickerByCode(code:str)->Instrument:
    key1 = code + "_SSE"
    key2 = code + "_SZE"
    return smart.instrument_map.get(key1) or smart.instrument_map.get(key2)

'''
 * 是否配股代码
 * 700*** 沪市配股代码
 * 080*** 深市配股代码
 * 785000~785999 科创板配股（上海）
 * 创业板配股代码？？？
 *
 *
 * 《竞价撮合平台市场参与者接口规格说明书（1.410版）》
 * 2.3申报接口ordwth
 * （6）卖出配股代码（700***、760***； 702***、762***；704***、764***、742***、753***等等）转义为对对应证券参与配股。
 * 卖出价格为配股价。卖出数量为参加配股的数量。指令即时处理，不可撤单。
 * 600***股票、601***股票对应的配股代码为700***、760***；职工股配股代码为702***、762***；配转债代码为704***、764***。
 * @param {string instrument_id 股票代码
 *
 * 《深圳证券交易所数据接口规范（Ver 4.72）》
 * 证券代码区间定义表
 * 包含 主板、中小企业板、创业板的配股
'''
def isSPO(instrument_id:str)->bool:
    if (not instrument_id):
        print('not instrument_id')
        return False
    return len(instrument_id) == 6 and (str(instrument_id[0:3]) in ["700", "760", "702", "762", "704", "764", "742", "753", "785", "771", "031"]) or (str(instrument_id[0:2]) in ["08", "38"])



repos_sh = ["204001", "204002", "204003", "204004", "204007", "204014", "204028", "204091", "204182"]
repos_sz = ["131810", "131811", "131800", "131809", "131801", "131802", "131803", "131805", "131806"]

bondReverseRepoMap = {}
for code in repos_sh:
    bondReverseRepoMap[code] = "SSE"

for code in repos_sz:
    bondReverseRepoMap[code] = "SZE"


'''
 * 判断一个证券是否是国债逆回购
 * @param {string instrument_id 证券代码
 * @param {number exchange_id 交易所id
 * @returns 是国债返回true，否则false
'''
def isReverseRepo(instrument_id:str, exchange_id:str)->bool:
    instrument = smart.getInstrument(instrument_id, exchange_id)
    if (instrument and instrument.instrument_type_ext ==  "XTP_SECURITY_NATIONAL_BOND_REVERSE_REPO"):
        return True
    
    return False

'''
 * 将xtp的买卖方向枚举值转换为汉语
 * @param {* str
'''
def transXtpSideType(type:str, xtpBusinessType:str)->str:
    label = None
    xtpBusinessType = xtpBusinessType if xtpBusinessType else ""
    if ("XTP_BUSINESS_TYPE_REPO" in xtpBusinessType):
        label = ("借出" if "XTP_SIDE_SELL" == type else dataTypeToName(type, "XTP_SIDE_TYPE"))
    else:
        label = dataTypeToName(type, "XTP_SIDE_TYPE")
    
    return label


'''
 * 将xtp的枚举值转换为汉语
 * @param {* str
'''
def dataTypeToName(v:str, k:str)->str:
    #v: SZE  #k: ALPHAX_EXCHANGE_TYPE
    return smart.dataType[str(k)][str(v)]["name"] if smart.dataType[str(k)][str(v)] else ''

'''
 * 将xtp的枚举值转换为枚举的index索引
 * @param {* str
'''
def dataTypeToIndex(v:str, k:str)->str:
    return smart.dataType[k][v]["i"] if smart.dataType[k][v] else -1

def dataTypeToXTPKey(v:str, k:str)->str:
    typeObj = smart.dataType.get(k)
    if typeObj:
        valObj = typeObj.get(str(v))
        if valObj:
            return valObj.get("key")
    return None

'''
 * 将全角字符转换为半角字符
 * @param {* str
'''
def toCDB(ustring:str)->str:
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换            
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring

def toString(obj)->str:
    if type(obj) != dict and hasattr(obj,"__dict__"):
        return json.dumps(obj.__dict__,ensure_ascii=False)
    else:
        return json.dumps(obj,ensure_ascii=False)
    # return ''.join(['%s:%s,' % item for item in obj.__dict__.items()])

'''
 * 去掉字符串两头的空白
 * @param {* str
'''
def trimAll(str:str)->str:
    if (not str):
         return str
    return str.strip()

'''
 * 得到当前日期的格式化形式
'''
def getNowFormatDate()->str:
    return time.strftime("%Y-%m-%d", time.localtime())

'''
 * 获取买盘或者买盘的盘口最优价格，往最新价格靠近，取有效价格
 * @param quote 行情对象
 * @param pk 盘口,B1-B5,S1-S5,涨停:H,跌停:L,现价:P
'''
def getBestPrice(quote:Quote, pk:str)->float:
    price = 0
    if (pk == "P"):
        price = quote.last_price
    elif (pk == "H"):
        #涨停价
        price = quote.upper_limit_price
    elif (pk == "L"):
        #跌停价
        price = quote.lower_limit_price
    elif (pk[0] == "S"):
        #卖盘
        n = int(pk[1:2])
        for i in range(n,0,-1): 
            price = quote.ask_price[i - 1]
            # console.log("S get price at ",i)
            if (price > 0):
                break
        
        if (price <= 0):
            # console.log("S get price at lastPrice")
            price = quote.last_price
            if (price <= 0):
                price = quote.bid_price[0] #买一价
            
    elif (pk[0] == "B"):
        #买盘
        n = int(pk[1:2])
        for i in range(n,0,-1):  #从n->1依次检查有效价格
            price = quote.bid_price[i - 1]
            # console.log("B get price at ",i)
            if (price > 0):
                break
            
        
        if (price <= 0): #没有价格取最新价
            # console.log("B get price at lastPrice")
            price = quote.last_price
            if (price <= 0):
                price = quote.ask_price[0] #卖一价
            
    if (price <= 0):
        price = quote.pre_close_price # 价格取不到，取昨收
             
    if (not price): price = 0
    return price


def mixin(fr, to):
    for k in fr:
        to[k] = fr[k]

def assign(target,source):
    targetDict = type(target) == dict
    if(type(source) == dict ):
        for k in source:
            if(targetDict):
                target[k] = source[k]
            else:
                if(k in target.__dict__):
                    setattr(target,k,source[k])
    else:
        for k in source.__dict__:
            if(targetDict):
                target[k] = getattr(source,k)
            else:
                if(k in target.__dict__):
                    setattr(target,k,getattr(source,k))

def decodeRsp(str:str)->Any:
    rsp = None
    try:
        rsp = json.loads(str)
    except Exception as err:
        rsp = {
            "code":"9999",
            "message":err
        }
        raise RspError(rsp)

    if(rsp["code"] == "0000"):
        return rsp.get("data")
    else:
        raise RspError(rsp)

def convertStrategyStatusToChiness(status:str)->str :
    if (status == StrategyStatus.Unknown): return ""
    elif (status == StrategyStatus.Starting): return "启动中"
    elif (status == StrategyStatus.Started): return "已启动"
    elif (status == StrategyStatus.Pause): return "暂停"
    elif (status == StrategyStatus.Stopping): return "停止中"
    elif (status == StrategyStatus.Stopped): return "已停止"
    elif (status == StrategyStatus.Errored): return "错误"

#将科学计数法转化为字符型数值
def scienceNum2numstr(num:float):
    strNum= str(num)
    if("e-" in strNum):
        lead, power = strNum.split("e-")
        if("." in lead):
            a, b = lead.split(".")
            numstr = "0." + "0"*(int(power)-1) + a + b
        else:
            a = lead[0]
            numstr = "0." + "0"*(int(power)-1) + a
        return numstr
    return num


SellLikeSide = [Side.Sell, Side.ShortSell, Side.RepayMargin]
# 按交易所单笔最大委托数量固定拆单
SPLIT_TYPE_EXCHANGE_FIXED_MAX_QTY = 0
# 按用户设置上限固定拆单
SPLIT_TYPE_CUSTOM_FIXED_MAX_QTY = 1
# 按交易所规定的单笔委托上下限范围随机拆单
SPLIT_TYPE_EXCHANGE_RANDOM = 2
# 按单笔委托市值范围随机拆单
SPLIT_TYPE_CUSTOM_RANDOM_MARKET_CAP = 3
# 按自定义股数范围随机拆单
SPLIT_TYPE_CUSTOM_RANDOM_QTY = 4

def getTickerMaxLimitQty(instrument_id,exchange_id,isSell,price_type):
    TEMP_MAX = 1e6 #1000000
    isPriceLimit = True # 是否为限价
    if (price_type != PriceType.Limit):
        isPriceLimit = False
    maxQty = TEMP_MAX
    stock = smart.getInstrument(instrument_id, exchange_id)
    if (not stock) :
        return maxQty
    if (isPriceLimit) : # 限价
        if (isSell) : # 卖
            maxQty = stock.ask_upper_limit_volume
        else:
            maxQty = stock.bid_upper_limit_volume

    else: # 市价
        if (isSell): # 卖
            maxQty = stock.market_ask_upper_limit_volume
        else:
            maxQty = stock.market_bid_upper_limit_volume
    
    if(maxQty > 0):return maxQty
    else:return maxQty

'''
根据系统设置进行拆单
'''
def splitOrder(instrument_id,exchange_id,volume,side,price_type,business_type):
    return fixedSplitUnit(instrument_id,exchange_id,side,volume,price_type,business_type)


# 交易所上限固定拆单
def fixedSplitUnit(ticker, exchangeId, xtpSideType, quantity, xtpPriceType,business_type):
    maxQty = getTickerMaxLimitQty(ticker, exchangeId, xtpSideType in SellLikeSide, xtpPriceType)
    if (business_type == BusinessType.ETF):
        maxQty = quantity
    return randomSplitByUpDown(ticker, exchangeId, xtpSideType, quantity, xtpPriceType, maxQty, maxQty)

# 固定上限拆单
def fixedSplitUnitByUpValue (ticker, exchangeId, xtpSideType,  quantity, xtpPriceType):
    splitMaxSplitQty = smart.systemset.get("splitMaxSplitQty",quantity)
    return randomSplitByUpDown(ticker, exchangeId, xtpSideType,  quantity, xtpPriceType, splitMaxSplitQty, splitMaxSplitQty)

# 自定义上下限拆单
def randomSplitByCustom(ticker, exchangeId, xtpSideType,  quantity, xtpPriceType):
    splitMinRandomQty = smart.systemset.get("splitMinRandomQty",quantity)
    splitMaxRandomQty = smart.systemset.get("splitMaxRandomQty",quantity)
    return randomSplitByUpDown(ticker, exchangeId, xtpSideType,  quantity, xtpPriceType, splitMinRandomQty,splitMaxRandomQty)

# 随机拆单
def randomSplitByQuantiy(ticker, exchangeId, xtpSideType,  quantity, xtpPriceType):
    maxQty = getTickerMaxLimitQty(ticker, exchangeId, SellLikeSide.includes(xtpSideType), xtpPriceType)
    staticTicker = smart.getInstrument(ticker, exchangeId)
    bidQtyUnit = 100 
    if(staticTicker):
        bidQtyUnit = staticTicker.bid_volume_unit #买入单位
    return randomSplitByUpDown(ticker, exchangeId, xtpSideType,  quantity, xtpPriceType, bidQtyUnit, maxQty)


#随机拆单按数量上限下限
def randomSplitByUpDown (ticker, exchangeId, xtpSideType,  quantity, xtpPriceType, downQuantity, upQuantity) :
    staticTicker:Instrument = smart.getInstrument(ticker, exchangeId)
    bidQtyLowerLimit = 100 #买入下限
    bidQtyUnit = 100 #买入单位
    if(staticTicker):
        bidQtyLowerLimit = staticTicker.bid_lower_limit_volume #买入下限
        bidQtyUnit = staticTicker.bid_volume_unit #买入单位
    
    #拆分后的数据
    tickerSplitUnitList = []

    #最大申购数量
    maxQty = getTickerMaxLimitQty(ticker, exchangeId, xtpSideType in SellLikeSide, xtpPriceType)
    minQty = bidQtyLowerLimit

    #求最大数量
    upQty = upQuantity
    #求最小数量
    downQty = downQuantity
    downQty = minQty if minQty > downQty else downQty
    upQty = maxQty if upQty > maxQty else upQty
    downQty = upQty if downQty >= upQty else downQty
    downQty = downQty if downQty > bidQtyUnit else bidQtyUnit
    downQty = downQty if downQty > bidQtyLowerLimit else  bidQtyLowerLimit
    upQty = upQty if upQty > bidQtyLowerLimit else bidQtyLowerLimit

    #查询持股数量
    countQuantity = quantity

    #循环产生新的单据
    while (countQuantity > 0) :
        if (countQuantity > downQty) : #数量多于最小拆单下限，可以拆单
            upQty_d = upQty if countQuantity > upQty else countQuantity
            
            max = upQty_d / bidQtyUnit
            min = downQty / bidQtyUnit
            random1 = round((random.random() * (max - min) + min) * 10) / 10
            rNum = math.floor(random1) * bidQtyUnit

            if (rNum > 0) :
                tickerSplitUnitList.append(rNum)
                countQuantity -= rNum
        else:
            tickerSplitUnitList.append(countQuantity)
            countQuantity = 0 #置零结束

    return tickerSplitUnitList



# 为组件添加监听
def addListener(event, callback) :
    def timeCallback(): # 优先级：callback > smart.on()> 默认
        listeners = smart.listeners(event)
        if callback:
            if (listeners and len(listeners) > 0) :
                smart.removeAllListeners(event)
            # 根据参入的回调函数进行注册
            smart.on(event, callback)
            return
        if (not listeners) : # 未进行smart.on()注册监听
            # 判断是否定义了默认的回调
            if (event == smart.Event.ON_BAR and smart.on_bar) :
                smart.on(event, smart.on_bar)
            elif (event == smart.Event.ON_INDICATOR and smart.on_indicator) :
                smart.on(event, smart.on_indicator)
            elif (event == smart.Event.ON_QUOTE and smart.on_quote) :
                smart.on(event, smart.on_quote)
    smart.add_timer(5, timeCallback)

'''
    * 匹配时间周期的正则表达式
    * @param input 必填 被校验值
    * @param endsWith 选填 以什么结尾
'''
def isFormatPeriod(input=None,endsWith=None):
    import re
    pattern = re.compile(r'^([1-9]|[1-5][0-9]|60)(m|d|w)$')
    if (endsWith == "m"):
        pattern = re.compile(r'^([1-9]|[1-5][0-9]|60)(m)$')
    return pattern.match(str(input))

# 获取买入基准价格
def getBuyBasePrice(quote):
    if not quote:
        return None
    price = quote.ask_price[0]
    if price:
        return price
    price = quote.bid_price[0]
    if price:
        return price
    price = quote.last_price
    if price:
        return price
    price = quote.pre_close_price
    return price

# 获取卖出基准价格
def getSellBasePrice(quote):
    if not quote:
        return None
    price = quote.bid_price[0]
    if price:
        return price
    price = quote.ask_price[0]
    if price:
        return price
    price = quote.last_price
    if price:
        return price
    price = quote.pre_close_price
    return price

# 获取价格笼子内的有效限价
def get_limit_price(side:int, quote:Quote, rate:float=2, units:int=10):
    if not side:
        raise Exception("side required!")
    if not quote:
        raise Exception("quote required!")
    # 获取价格变动限制百分比
    defautlRate = 2
    if rate < 0 or rate > defautlRate:
        rate = defautlRate
    rate /= 100
    # 获取最小价格变动单位的个数
    defaultUnits = 10
    if units < 0 or units > defaultUnits:
        units = defaultUnits
    instrument = smart.getInstrument(quote.instrument_id, quote.exchange_id)
    divisor = 10 ** instrument.precision
    if side == Side.Buy or side == Side.MarginTrade or side == Side.RepayStock:  # 买入
        # 获取买入基准价格
        price = getBuyBasePrice(quote)
        if not price:
            return 0
        # 计算买入基准102%
        price1 = math.floor(price * (1 + rate) * divisor) / divisor
        # 上海科创版
        if instrument.instrument_type_ext == "XTP_SECURITY_TECH_BOARD":
            if price1 > quote.upper_limit_price:
                price1 = quote.upper_limit_price
            return price1
        # 计算买入基准+10个最小变动单位
        price2 = price + units * instrument.price_tick
        price2 = round(price2, instrument.precision)
        # 计算max(买入基准102%, 买入基准+10个最小变动单位)
        price = price1 if price1 > price2 else price2
        # 超出涨停价
        if price > quote.upper_limit_price:
            price = quote.upper_limit_price
        return price
    elif side == Side.Sell or side == Side.ShortSell or side == Side.RepayMargin:  # 卖出
        # 获取卖出基准价格
        price = getSellBasePrice(quote)
        if not price:
            return 0
        # 计算卖出基准98%
        price1 = math.ceil(price * (1 - rate) * divisor) / divisor
        # 上海科创版
        if instrument.instrument_type_ext == "XTP_SECURITY_TECH_BOARD":
            if price1 < quote.lower_limit_price:
                price1 = quote.lower_limit_price
            return price1
        # 计算卖出基准-10个最小变动单位
        price2 = price - units * instrument.price_tick
        price2 = round(price2, instrument.precision)
        # 计算min(卖出基准98%, 卖出基准-10个最小变动单位)
        price = price2 if price1 > price2 else price1
        # 超出跌停价
        if price < quote.lower_limit_price:
            price = quote.lower_limit_price
        return price
    else:
        return 0

def getInstrumentType(instrumentId:str=None, exchangeId:str=None, code:str=None):
    if (code):
        instrumentId, exchangeId = getInstrumentIdAndExchangeIdFromCode(code)
    instrument = smart.getInstrument(instrumentId, exchangeId)
    instrumentType = InstrumentType.Unknown
    if instrument:
        instrumentType = instrument.instrument_type
    return instrumentType


# __all__ = [
# "convertOrderFromSmartToPlugin",
# "convertTradeFromSmartToPlugin",
# "convertAssetsFromSmartToPlugin",
# "convertCreditAssetsFromSmartToPlugin",
# "convertPositionFromSmartToPlugin",
# "convertQuoteFromSmartToPlugin",
# "convertInstructmentTypeFromXtpBusinessType",
# "convertDirectory",
# "convertExchangeIdFromxtpMarketType",
# "convertExchangeIdFromxtpExchangeId",
# "converXTPExchangeIdFromExchangeId",
# "convertOrderStatus",
# "convertSide",
# "convertOffset",
# "convertPriceType",
# "convertInstrumentTypeFromXtpSecurityType",
# "getXtpMarketTypeFromExchange",
# "getXtpSideTypeFromSide",
# "getXtpBusinessTypeFromBusinessType",
# "getXtpOffsetTypeFromOffset",
# "getXtpPriceTypeFromPriceTypeWithExchange",
# "isSTIStock",
# "isSTIMarketOrder",
# "isETF",
# "isSPO",
# "isReverseRepo",
# "transXtpSideType",
# "dataTypeToName",
# "dataTypeToIndex",
# "toCDB",
# "toString",
# "trimAll",
# "getNowFormatDate",
# "getBestPrice",
# "mixin",
# "assign",
# "decodeRsp",
# "convertStrategyStatusToChiness"
# ]

