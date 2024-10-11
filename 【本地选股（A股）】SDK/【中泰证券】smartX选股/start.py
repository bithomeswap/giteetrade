# # 需要在官方的名叫SmartX-Studio的IDE当中才能运行

# 【中泰证券（smartX）：
# 股票类型{登录账号:253191004031，登录密码:B1t2GwXb，Key:b8aa7173bba3470e390d787219b2112e，
#      账号资金已补齐至10亿，交易地址:122.112.139.0:6102，行情地址:119.3.103.38:6002，
#      SDK下载：https://xtp.zts.com.cn/service/download，
#      在线文档：https://xtp.zts.com.cn/doc/api/xtpDoc}，
# 算法类型{登录账号:353191001488，登录密码:tVu77rX4，Key:b8aa7173bba3470e390d787219b2112e，
#      账号资金已补齐至10亿，交易地址:122.112.139.0:6202，行情地址:119.3.103.38:6002，
#      SDK下载：https://xtp.zts.com.cn/service/download，
#      在线文档：https://xtp.zts.com.cn/doc/api/xtpDoc，
#      算法总线地址：119.3.40.4:8602，算法总线密码：algox@abc.cn}】

from smart import *
import time
import logging
logger = logging.getLogger()

#希望能够本地调用，但是不成功【在软件当中不是这样调用的】
def getETFListCB(arr,err):
    if(err):
        logger.debug("get error from getETFList:%s",err)
    else:
        print("get getETFList length:%d",arr)
        # for i in range(len(arr)):
        #     logger.debug("get getETFList:%s",smart.utils.toString(arr[i]))
        #     # 输出：{"instrument_id": "159601", "instrument_name": "A50ETF", "instrument_type": "Fund", "instrument_type_ext": "XTP_SECURITY_ETF_INTER_MARKET_STOCK", "exchange_id": "SZE", "exchange_id_name": "深交所", "xtp_market_type": "XTP_MKT_SZ_A", "name_py": "a50etf", "price_tick": 0.001, "precision": 3, "buy_volume_unit": 100, "sell_volume_unit": 1, "bid_volume_unit": 100, "ask_volume_unit": 1, "bid_upper_limit_volume": 1000000, "bid_lower_limit_volume": 100, "ask_upper_limit_volume": 1000000, "ask_lower_limit_volume": 1, "market_bid_volume_unit": 100, "market_ask_volume_unit": 1, "market_bid_upper_limit_volume": 1000000, "market_bid_lower_limit_volume": 100, "market_ask_upper_limit_volume": 1000000, "market_ask_lower_limit_volume": 1, "pre_close_price": 0.784, "upper_limit_price": 0.862, "lower_limit_price": 0.7060000000000001, "is_registration": false, "kw": "A50ETF", "code": "159601.SZ", "cash_component": 1671.42, "estimate_amount": 2261.42, "max_cash_ratio": 0.5, "net_value": 0.7837, "redemption_status": 1, "total_amount": 2037534.42, "unit": 2600000, "basket": []}
smart.getETFList(getETFListCB)#查询可交易的ETF列表


# def init():
#     # #是否ETF基金
#     # smart.utils.isETF(instrument_id) # return False

#     # 获取有效申报价格范围-get_limit_price
#     # 获取买盘的最高有效申报价或者卖盘的最低有效申报价
#     # side Number(必填) - 买卖方向，参考Side枚举值
#     # quote Object(必填) - 行情对象，参考Quote对象
#     # rate Number(选填) - 有效申报价格范围，默认值为2（即为2%），可选填不大于2的值如1.8（即为1.8%），若所填超过默认值则按默认值计算
#     # units Number(选填) - 最小价格变动单位的个数，默认值为10，可选填不大于10的值如8，若所填超过默认值则按默认值计算
#     # smart.utils.get_limit_price(side, quote, rate, units)

#     # 盘口最优价格-getBestPrice
#     # 获取买盘或者卖盘的盘口最优价格，往最新价格靠近，取有效价格
#     # marketData String(必填) - 行情对象
#     # flag String(必填) - 盘口。涨停:H；跌停:L；现价:P；买一到买五分别为：B1、B2、B3、B4、B5；卖一到卖五分别为：S1、S2、S3、S4、S5。 返回价格，类型是数字
#     # smart.utils.getBestPrice(marketData, flag)

#     # 对象转字符串-toString
#     # 将对象转换为json字符串
#     # obj Object(必填) - 要转换的对象
#     # 返回值将对象转换为json字符串
#     # smart.utils.toString(obj) # return "obj对应的json字符串"

#     # 客户端当前日期-getNowFormatDate
#     # 得到当前日期的格式化形式。"yyyy-MM-dd"
#     # 返回格式化的数据，类型是string
#     # smart.utils.getNowFormatDate() # retrun "2021-03-01"

#     # # 所有证券列表
#     # instrument_list = smart.instrument_list
#     # logger.debug("get instrument_list:%s",smart.utils.toString(instrument_list[1]))
#     # # 输出：{"instrument_id": "000001", "instrument_name": "上证指数", "instrument_type": "Index", "instrument_type_ext": "XTP_SECURITY_INDEX", "exchange_id": "SSE", "exchange_id_name": "上交所", "xtp_market_type": "XTP_MKT_SH_A", "name_py": "szzs", "price_tick": 0.0001, "precision": 4, "buy_volume_unit": 0, "sell_volume_unit": 0, "bid_volume_unit": 0, "ask_volume_unit": 0, "bid_upper_limit_volume": 0, "bid_lower_limit_volume": 0, "ask_upper_limit_volume": 0, "ask_lower_limit_volume": 0, "market_bid_volume_unit": 0, "market_ask_volume_unit": 0, "market_bid_upper_limit_volume": 0, "market_bid_lower_limit_volume": 0, "market_ask_upper_limit_volume": 0, "market_ask_lower_limit_volume": 0, "pre_close_price": 3189.248, "upper_limit_price": 9999.9999, "lower_limit_price": 0, "is_registration": false, "kw": "上证指数", "code": "000001.SH"}

#     def getETFListCB(arr,err):
#         if(err):
#             logger.debug("get error from getETFList:%s",err)
#         else:
#             print("get getETFList length:%d",arr)
#             # for i in range(len(arr)):
#             #     logger.debug("get getETFList:%s",smart.utils.toString(arr[i]))
#             #     # 输出：{"instrument_id": "159601", "instrument_name": "A50ETF", "instrument_type": "Fund", "instrument_type_ext": "XTP_SECURITY_ETF_INTER_MARKET_STOCK", "exchange_id": "SZE", "exchange_id_name": "深交所", "xtp_market_type": "XTP_MKT_SZ_A", "name_py": "a50etf", "price_tick": 0.001, "precision": 3, "buy_volume_unit": 100, "sell_volume_unit": 1, "bid_volume_unit": 100, "ask_volume_unit": 1, "bid_upper_limit_volume": 1000000, "bid_lower_limit_volume": 100, "ask_upper_limit_volume": 1000000, "ask_lower_limit_volume": 1, "market_bid_volume_unit": 100, "market_ask_volume_unit": 1, "market_bid_upper_limit_volume": 1000000, "market_bid_lower_limit_volume": 100, "market_ask_upper_limit_volume": 1000000, "market_ask_lower_limit_volume": 1, "pre_close_price": 0.784, "upper_limit_price": 0.862, "lower_limit_price": 0.7060000000000001, "is_registration": false, "kw": "A50ETF", "code": "159601.SZ", "cash_component": 1671.42, "estimate_amount": 2261.42, "max_cash_ratio": 0.5, "net_value": 0.7837, "redemption_status": 1, "total_amount": 2037534.42, "unit": 2600000, "basket": []}
#     smart.getETFList(getETFListCB)#查询可交易的ETF列表


#     def getETFBasketCB(arr,err):
#         if(err):
#             logger.debug("get error from getETFBasket:%s",err)
#         else:
#             logger.debug("get getETFBasket length:%d",arr)
#             # for i in range(len(arr)):
#             #     logger.debug("get getETFBasket:%s",smart.utils.toString(arr[i]))
#             #     # 输出：{"instrument_id": "688599", "instrument_name": "天合光能", "instrument_type": "Stock", "instrument_type_ext": "XTP_SECURITY_TECH_BOARD", "exchange_id": "SSE", "exchange_id_name": "上交所", "xtp_market_type": "XTP_MKT_SH_A", "name_py": "thgn", "price_tick": 0.01, "precision": 2, "buy_volume_unit": 1, "sell_volume_unit": 1, "bid_volume_unit": 1, "ask_volume_unit": 1, "bid_upper_limit_volume": 100000, "bid_lower_limit_volume": 200, "ask_upper_limit_volume": 100000, "ask_lower_limit_volume": 200, "market_bid_volume_unit": 1, "market_ask_volume_unit": 1, "market_bid_upper_limit_volume": 50000, "market_bid_lower_limit_volume": 200, "market_ask_upper_limit_volume": 50000, "market_ask_lower_limit_volume": 200, "pre_close_price": 36.02, "upper_limit_price": 43.22, "lower_limit_price": 28.82, "is_registration": true, "kw": "天合光能", "code": "688599.SH", "amount": 0, "creation_amount": 0, "creation_premium_ratio": 0.1, "premium_ratio": 0.1, "quantity": 374, "redemption_amount": 0, "redemption_discount_ratio": 0, "replace_type": "ERT_CASH_OPTIONAL", "ticker": "510050"}
#     smart.getETFBasket("510050",getETFBasketCB)#查询ETF成分股列表


#     # #订阅ETF折溢价预期利润，第一次订阅没有缓存，回调正常返回空
#     # def etfProfitCB(arr,err):
#     #     if(err):
#     #         logger.debug("get error from subscribeETFProfit:%s",err)
#     #     else:
#     #         for i in range(len(arr)):
#     #             if ((i+1)==len(arr)):
#     #                 logger.debug("subscribeETFProfitTest【OK】:%s",smart.utils.toString(arr[i]))
#     #                 # 输出：{"instrument_id": "588460", "iopv": 0.8998, "iopv_buy": 0.8995, "iopv_sale": 0.9002, "diopv": 0.8997, "dis_profit": -3137.442789999935, "pre_profit": -541.2358000000652}
#     # smart.subscribeETFProfit(etfProfitCB)
#     # #接收ETF折溢价预期利润
#     # def on_etf_profit(etfProfit):
#     #     logger.debug(f"on_etf_profit:{smart.utils.toString(etfProfit)}")
#     #     # 输出：{"instrument_id": "159869", "iopv": 1.0179, "iopv_buy": 1.0177, "iopv_sale": 1.0188, "diopv": 1.0184, "dis_profit": -2040.7242999999814, "pre_profit": -1073.9139600000187}
#     # smart.on(smart.Event.ON_ETF_PROFIT, on_etf_profit)
#     # # 取消订阅ETF折溢价预期利润
#     # def time_callback():
#     #     smart.unsubscribeETFProfit()
#     # smart.add_timer(2000, time_callback)#添加单次定时-add_timer,整句代码的意思是2000ms之后取消订阅

#     # #委托下单
#     # def insert_callback(order,err):
#     #     if(err):
#     #         logger.debug("get error from insert_order:%s",err)
#     #         # 输出：RspError({'code': '9003', 'message': KeyError('')})
#     #     else:
#     #         logger.debug("get insert_order: %s",smart.utils.toString(order))
#     #         # 输出：{"rcv_time": null, "order_id": "37906458003637227", "source_order_id": "37906458003637227", "insert_time": null, "update_time": null, "trading_day": null, "instrument_id": "300001", "exchange_id": "SZE", "account_id": "253191000961", "client_id": "d21562c1-3b0b-11ee-b730-3319f43f98a4", "instrument_type": 1, "limit_price": 19.18, "frozen_price": 19.18, "volume": 200, "volume_traded": 0, "volume_left": 200, "tax": null, "commission": null, "status": 1, "error_id": null, "error_msg": null, "side": 1, "offset": 100, "price_type": 1, "volume_condition": 0, "time_condition": 2, "parent_order_id": null, "code": "300001.SZ", "traffic": "frontpy", "traffic_sub_id": "PythonDemo-_dev_", "cancel_time": null, "order_cancel_client_id": null, "order_cancel_xtp_id": null, "instrument_name": "特锐德", "trade_amount": 0, "xtp_business_type": "XTP_BUSINESS_TYPE_CASH", "xtp_market_type": "XTP_MKT_SZ_A", "xtp_price_type": "XTP_PRICE_LIMIT", "xtp_position_effect_type": "XTP_POSITION_EFFECT_INIT", "xtp_side_type": "XTP_SIDE_BUY", "xtp_order_status": "XTP_ORDER_STATUS_INIT", "exchange_id_name": "深交所", "instrument_type_name": "股票", "status_name": "初始化", "side_name": "买", "offset_name": "初始值", "price_type_name": "限价", "xtp_business_type_name": "普通股票", "xtp_market_name": "深A", "xtp_price_type_name": "限价", "xtp_position_effect_type_name": "初始值", "xtp_side_type_name": "买", "xtp_order_status_name": "初始化", "volume_condition_name": "任何数量", "time_condition_name": "本节有效", "traffic_name": "Python策略", "business_type": "frontpy"}
#     # smart.insert_order(
#     #     instrument_id='300001', 
#     #     exchange_id=smart.Type.Exchange.SZE, 
#     #     price_type=smart.Type.PriceType.Limit, 
#     #     limit_price=19.18, 
#     #     volume=200,
#     #     side=smart.Type.Side.Buy,
#     #     offset=smart.Type.Offset.Init,
#     #     business_type=smart.Type.BusinessType.CASH,
#     #     callback=insert_callback)

#     # # 撤单
#     # def cancel_callback(data,err):
#     #     if(err):
#     #         logger.debug("get error from cancel_insert:%s",err)
#     #         # 输出：RspError({'code': '9003', 'message': KeyError('')})
#     #     else:
#     #         logger.debug("get cancel_insert:%s",data)
#     #         # 输出：{'orderXtpId': '37906458003637226', 'userName': '253191000961', 'reqID': '00000000007', 'requestID': 'cancelOrder_18'}
#     # smart.cancel_order(account_id=None, order_id="37906458003637226", cb=cancel_callback)

#     # #接收资产变化推送
#     # def callback(assets):
#     #     logger.debug("get on_assets: %s",smart.utils.toString(assets))
#     #     # 输出：{"banlance": 0, "buying_power": 999919485.65, "captial_asset": 0, "deposit_withdraw": 0, "force_freeze_amount": 0, "frozen_exec_cash": 0, "frozen_exec_fee": 0, "frozen_margin": 0, "fund_buy_amount": 58534.5, "fund_buy_fee": 135.26, "fund_sell_amount": 0, "fund_sell_fee": 0, "orig_banlance": 0, "pay_later": 0, "preadva_pay": 0, "preferred_amount": 0, "security_asset": 0, "total_asset": 999941330.24, "market_value": 4267231298.5, "trade_netting": 0, "withholding_amount": 21844.59, "update_time": "15:08:52", "all_asset": 0, "all_debt": 0, "guaranty": 0, "line_of_credit": 0, "maintenance_ratio": 0, "remain_amount": 0, "security_interest": 0, "cash_remain_amt": 0, "cash_interest": 0, "extras_money": 0}
#     # smart.current_account.on_assets(callback)

    
#     # #接收成交回报推送 不保序
#     # def callback(trade):
#     #     logger.debug("get on_trade: %s",smart.utils.toString(trade))
#     #     # 输出：{"rcv_time": 20230815150550932, "order_id": "37906458003637235", "parent_order_id": "cm_2ad7c5f0-3b3a-11ee-b730-3319f43f98a4", "trade_time": 20230815150550932, "instrument_id": "600000", "exchange_id": "SSE", "account_id": "253191000961", "client_id": 13, "instrument_type": 1, "side": 1, "offset": 100, "price": 7.17, "volume": 1000, "tax": null, "commission": null, "code": "600000.SH", "traffic": "common", "traffic_sub_id": "", "instrument_name": "浦发银行", "trade_amount": 7170, "xtp_business_type": "XTP_BUSINESS_TYPE_CASH", "xtp_market_type": "XTP_MKT_SH_A", "xtp_exec_id": "0000000000001198", "xtp_report_index": "6549825126420", "xtp_order_exch_id": "0141020000001262", "xtp_trade_type": "0", "xtp_branch_pbu": "13688", "xtp_position_effect_type": "XTP_POSITION_EFFECT_INIT", "xtp_side_type": "XTP_SIDE_BUY", "exchange_id_name": "上交所", "instrument_type_name": "股票", "side_name": "买", "offset_name": "初始值", "xtp_business_type_name": "普通股票", "xtp_market_name": "沪A", "xtp_position_effect_type_name": "初始值", "xtp_side_type_name": "买", "traffic_name": "普通下单", "xtp_trade_type_name": "普通成交", "business_type": "", "_rowid": "XTP_BUSINESS_TYPE_CASH_XTP_MKT_SH_A_0000000000001198_XTP_SIDE_BUY_600000_0"}
#     # smart.current_account.on_trade(callback)

    
#     # #接收委托推送 不保序
#     # def callback(order):
#     #     logger.debug("get on_order: %s",smart.utils.toString(order))
#     #     # 输出：{"rcv_time": 20230815150122628, "order_id": "37906458003637233", "source_order_id": "37906458003637233", "insert_time": 20230815150122612, "update_time": 20230815150122628, "trading_day": "20230815", "instrument_id": "600000", "exchange_id": "SSE", "account_id": "253191000961", "client_id": 13, "instrument_type": 1, "limit_price": 7.17, "frozen_price": 7.17, "volume": 100, "volume_traded": 50, "volume_left": 50, "tax": null, "commission": null, "status": 7, "error_id": 0, "error_msg": "", "side": 1, "offset": 100, "price_type": 1, "volume_condition": 0, "time_condition": 2, "parent_order_id": "cm_8aebd4f0-3b39-11ee-b730-3319f43f98a4", "code": "600000.SH", "traffic": "common", "traffic_sub_id": "", "cancel_time": 0, "order_cancel_client_id": 0, "order_cancel_xtp_id": "0", "instrument_name": "浦发银行", "trade_amount": 358.5, "xtp_business_type": "XTP_BUSINESS_TYPE_CASH", "xtp_market_type": "XTP_MKT_SH_A", "xtp_price_type": "XTP_PRICE_LIMIT", "xtp_position_effect_type": "XTP_POSITION_EFFECT_INIT", "xtp_side_type": "XTP_SIDE_BUY", "xtp_order_status": "XTP_ORDER_STATUS_PARTTRADEDQUEUEING", "exchange_id_name": "上交所", "instrument_type_name": "股票", "status_name": "部分成交", "side_name": "买", "offset_name": "初始值", "price_type_name": "限价", "xtp_business_type_name": "普通股票", "xtp_market_name": "沪A", "xtp_price_type_name": "限价", "xtp_position_effect_type_name": "初始值", "xtp_side_type_name": "买", "xtp_order_status_name": "部分成交", "volume_condition_name": "任何数量", "time_condition_name": "本节有效", "traffic_name": "普通下单", "business_type": "common"}
#     # smart.current_account.on_order(callback)


#     # import tushare as ts
#     # # 输出：1.2.89
#     # pro = ts.pro_api(token='YOUR_API_TOKEN')  # 需要在Tushare Pro官网注册并获取接口令牌
#     # pd.set_option('display.max_rows', None)  # 显示所有行
#     # pd.set_option('display.max_columns', None)  # 显示所有列
#     # df = pro.query('daily', ts_code='601318.SH', start_date='20230801', end_date='20230813')
#     # logger.debug(df)
#     # # 输出：
#     # #      ts_code trade_date   open   high    low  close  pre_close  change  pct_chg         vol       amount
#     # # 0  601318.SH   20230811  51.30  51.41  49.35  49.37      51.36   -1.99  -3.8746   748920.93  3751696.963 
#     # # 1  601318.SH   20230810  51.05  51.47  50.88  51.36      51.26    0.10   0.1951   299263.22  1531979.641 
#     # # 2  601318.SH   20230809  51.08  51.58  50.95  51.26      51.26    0.00   0.0000   372852.64  1911450.576 
#     # # 3  601318.SH   20230808  51.47  51.69  50.46  51.26      51.70   -0.44   -0.8511  523263.42  2671294.850  
#     # # 4  601318.SH   20230807  51.38  51.77  51.20  51.70      51.90   -0.20   -0.3854  436896.13  2246940.970  
#     # # 5  601318.SH   20230804  53.23  53.85  51.90  51.90      52.41   -0.51   -0.9731 1051652.84  5566174.314
#     # # 6  601318.SH   20230803  51.41  52.60  51.11  52.41      51.41    1.00    1.9451  654944.21  3398760.968  
#     # # 7  601318.SH   20230802  51.60  52.56  50.93  51.41      51.74   -0.33   -0.6378  608798.17  3136350.132 
#     # # 8  601318.SH   20230801  52.50  53.00  51.44  51.74      52.60   -0.86   -1.6350  670613.72  3493879.471 

#     # #获取当天任意分钟的bar
#     # codes = ['000001.SZ','600000.SH']
#     # period = "5m"
#     # datalist = smart.query_bar_today(codes, period) # 正常传值
#     # for k,v in datalist.items():
#     #             logger.debug("query_bar_today_async【OK】:%s", k)
#     #             # query_bar_today_async【OK】:000001.SZ
#     #             for i in range(len(v)):
#     #                 if i < 5:   
#     #                     logger.debug("query_bar_today_async【OK】前5个:%s",smart.utils.toString(v[i]))
#     #                     # query_bar_today_async【OK】前5个:{"type": "bar_5min", "code": "000001.SZ", "instrument_id": "000001", "exchange_id": "SZE", "trading_day": "2024-01-18", "source_id": "xtp", "start_time": "2024-01-18 09:30:00", "end_time": "2024-01-18 09:35:00", "time_interval": 5,"period": "5m",  "high": 9.24, "low": 9.12, "open": 9.21, "close": 9.13, "volume": 14017000, "start_volume": 0, "turnover": 128664195, "start_turnover": 0}




#     # ETF配方表-ETF
#     # ETF配方表对象

#     # #ETF配方表对象
#     # class ETF(Instrument):
#     #     def __init__(self):
#     #         # 证券基础字段参见Instrument
#     #         super().__init__()
#     #         self.cash_component = None  # T-1日现金差额
#     #         self.estimate_amount = None  # T日预估现金余额
#     #         self.max_cash_ratio = None  # 现金替代比率上限
#     #         self.net_value = None  # T-1日基金份额净值
#     #         self.redemption_status = None  # 基金当天赎回状态：1可以，0不可以
#     #         self.total_amount = None  # 最小申赎单位净值
#     #         self.unit = None  # 最小申购赎回单位
#     #         self.basket = []  # 成分股篮子列表
#     # ETF成分股-ETFCompoment
#     # ETF成分股对象

#     # #ETF成分股对象
#     # class ETFCompoment(Instrument):
#     #     def __init__(self):
#     #         # 证券基础字段参见Instrument
#     #         super().__init__()
#     #         self.amount = None  # 替代金额
#     #         self.creation_amount = None  # 溢价替代金额
#     #         self.creation_premium_ratio = None  # 溢价比例
#     #         self.premium_ratio = None  # 溢价比例
#     #         self.quantity = None  # 股票数量
#     #         self.redemption_amount = None  # 折价替代金额
#     #         self.redemption_discount_ratio = None  # 折价比例
#     #         self.replace_type = None  # 现金替代类型 参考ETFReplaceType
#     #         self.ticker = None  # 申赎代码如：510501
#     #         self.creation_amount = None  # 申购现金替代金额
#     #         self.redemption_amount = None  # 赎回现金替代金额
#     # ETF预期利润-ETFProfit
#     # ETF预期利润

#     # class ETFProfit:
#     #     def __init__(self):
#     #         self.instrument_id = None  # ETF的证券代码
#     #         self.iopv = 0  # ETF的模拟净值
#     #         self.iopv_buy = 0  # ETF的买模拟净值
#     #         self.iopv_sale = 0  # ETF的卖模拟净值
#     #         self.diopv = 0  # ETF的动态模拟净值
#     #         self.dis_profit = 0  # ETF折价预期利润
#     #         self.pre_profit = 0  # ETF溢价预期利润
#     # 持仓-Position
#     # 持仓对象定义

#     # class Position:
#     #     def __init__(self):
#     #         self.instrument_id = None  # 合约ID（证券代码)
#     #         self.instrument_name = ""  # 证券名称
#     #         # self.instrument_type = InstrumentType.Unknown  # 合约类型  alphax有但xtp目前缺少 需要去静态信息关联 可能影响性能  可以空着
#     #         self.exchange_id = Exchange.Unknown  # 交易所id
#     #         self.exchange_id_name = "未知"  # 交易所名称
#     #         self.direction = None  # 持仓方向
#     #         self.direction_name = ""  # 持仓方向名称
#     #         self.name_py = ""  # 拼音首字母  如"安诺其"为"anq"  alphax缺少
#     #         self.volume = 0  # 持仓量
#     #         self.sellable_volume = 0  # 可卖持仓  alphax缺少
#     #         self.position_cost_price = 0  # 持仓成本 profitPrice
#     #         self.last_price = 0  # 最新价
#     #         self.market_value = 0  # 市值
#     #         self.unrealized_pnl = 0  # 浮动盈亏（保留字段,未计算） 未实现盈亏
#     #         self.yesterday_volume = 0  # 昨日持仓
#     #         self.purchase_redeemable_qty = 0  # 今日申购赎回数量 alphax缺少
#     #         self.executable_option = 0  # 可行权合约 alphax缺少
#     #         self.executable_underlying = 0  # 可行权标的 alphax缺少
#     #         self.locked_position = 0  # 已锁定标的 alphax缺少
#     #         self.usable_locked_position = 0  # 可用已锁定标的 alphax缺少
#     #         self.xtp_market_type = "XTP_EXCHANGE_UNKNOWN"  # 交易市场
#     #         self.xtp_market_name = "未知"  # 交易市场名称
#     #         self._instrument_id_direction = ""  # 内部使用  代码+持仓方向的联合主键 如"300067_XTP_POSITION_DIRECTION_NET"
#     #         self.code = None  # 证券代码.交易所标识 如"600000.SH"
            
#     # 委托回报-Order
#     # 委托回报

#     # class Order:
#     #     def __init__(self):
#     #         self.rcv_time = None  # String	数据接收时间                                              "20200608140053830"
#     #         self.order_id = None  # String	订单ID（对应xtpid）                    orderXtpId         "36934130021173201"
#     #         self.source_order_id = None
#     #         self.insert_time = None  # String	'XTP_MKT_UNKNOWN''XTP_MKT_UNKNOWN'委托写入时间                           insertTime         "20200608140053830"
#     #         self.update_time = None  # String	委托更新时间                           updateTime         "20200608140053830"
#     #         self.trading_day = None  # String	交易日                                insertTime中截取    "20200608"
#     #         self.instrument_id = None  # String	合约ID（证券代码）                     ticker              "600000"
#     #         self.exchange_id = Exchange.Unknown  # String	交易所ID                              xtpMarketType转换   "SSE"
#     #         self.account_id = None  # String	账号ID（资金账号）                     userName            "10912133333344"
#     #         self.client_id = None  # String	用户自定义编号                         rowId || orderClientId (rowid优先)  "6a1071e1-a94d-11ea-810c-4b25bab2cda3"
#     #         self.instrument_type = None  # Number	合约类型                              xtpBusinessType转换  InstrumentType.Stock
#     #         self.limit_price = None  # Number	价格                                  price               10.23
#     #         self.frozen_price = None  # Number	冻结价格（市价单冻结价格为0.0）          price               10.23
#     #         self.volume = None  # Number	数量                                  quantity            100
#     #         self.volume_traded = None  # Number	成交数量                              qty_traded           0
#     #         self.volume_left = None  # Number	剩余数量                              qty_left             100
#     #         self.tax = None  # Number	税                                   todo:
#     #         self.commission = None  # Number	手续费                                todo:
#     #         self.status = None  # Number	订单状态                              order_status
#     #         self.error_id = None  # Number	错误ID                               xtpErrorId
#     #         self.error_msg = None  # String	错误信息                              xtpErrorMsg
#     #         self.side = Side.Unknown  # Number	买卖方向                              xtpSideType
#     #         self.offset = Offset.Unknown  # Number	开平方向                              xtpPositionEffectType
#     #         self.price_type = None  # Number	价格类型                              xtpPriceType
#     #         self.volume_condition = None  # Number	成交量类型
#     #         self.time_condition = None  # Number	成交时间类型
#     #         self.parent_order_id = None  # String	母单ID                               #篮子为runtimeId一个篮子一次交易一个值   etf套利为etf标签页期间是一个值  其他取alphax或smartserver传的      "6a1071e1-a94d-11ea-810c-4b25bab2cda3"
#     #         self.code = None  # String  证券代码.交易所标识                            "600000.SH"

#     #         self.traffic = None  # String  业务渠道标识                           business_type         "AlphaX"
#     #         self.traffic_sub_id = None  # String  业务子标识，一般填策略名称               businessSubId         "网格交易"
#     #         self.cancel_time = None  # String  撤单时间                              cancelTime            "20200608140053830"
#     #         self.order_cancel_client_id = None  # String  撤单自定义编号                         orderCancelClientId   "0"
#     #         self.order_cancel_xtp_id = None  # String  所撤原单的编号(原xtpid)                orderCancelXtpId      "0"
#     #         self.instrument_name = None  # String  合约名称（证券名称）                    tickerName            "浦发银行"
#     #         self.trade_amount = None  # Number  委托金额                              tradeAmount           0
#     #         self.xtp_business_type = None  # String  xtp证券业务类型                        xtpBusinessType       "XTP_BUSINESS_TYPE_CASH"
#     #         self.xtp_market_type = "XTP_MKT_UNKNOWN"  # String  xtp市场类型                            xtpMarketType         "XTP_MKT_SZ_A"

#     #         # 以下为xtp的冗余字段，为了获取xtp的原值
#     #         self.xtp_price_type = None  # String  xtp价格类型                            xtpPriceType          "XTP_PRICE_LIMIT"
#     #         self.xtp_position_effect_type = None  # String xtp开平方向                  xtpPositionEffectType "XTP_POSITION_EFFECT_OPEN"
#     #         self.xtp_side_type = None  # String  xtp交易方向                            xtpSideType           "XTP_SIDE_BUY"
#     #         self.xtp_order_status = None  # String  xtp订单状态                            orderStatus           "XTP_ORDER_STATUS_INIT"

#     #         # 以下为xtp和alphax枚举值翻译为中文的名称
#     #         self.exchange_id_name = None  # String  交易所名称                                                  "上交所"
#     #         self.instrument_type_name = None  # String  合约类型名称                                                "股票"
#     #         self.status_name = None  # String  订单状态名称                                                "全部成交"
#     #         self.side_name = None  # String  买卖方向名称                                                "买"
#     #         self.offset_name = None  # String  开平方向名称                                                "开"
#     #         self.price_type_name = None  # String  价格类型名称                                                "限价"
#     #         self.xtp_business_type_name = None  # String  xtp证券业务类型名称                                          "现货"
#     #         self.xtp_market_name = None  # String  xtp市场类型名称                                             "沪市"
#     #         self.xtp_price_type_name = None  # String  xtp价格类型名称                                             "限价"
#     #         self.xtp_position_effect_type_name = None  # String  xtp开平方向名称                                             "开"
#     #         self.xtp_side_type_name = None  # String  xtp交易方向名称                                             "买"
#     #         self.xtp_order_status_name = None  # String  xtp价格类型名称                                             "限价"
#     #         self.volume_condition_name = None  # String  成交量类型名称                                              "任何数量" "最小数量" "全部数量"
#     #         self.time_condition_name = None  # String  成交时间类型名称                                            "立即完成" "本节有效"  "当日有效" "指定日期前有效" "撤销前有效" "集合竞价有效"
#     #         self.traffic_name = None  # String  业务渠道名称                                                "策略"    
#     # 成交回报-Trade
#     # 成交回报

#     # class Trade():
#     #     def __init__(self):
#     #         self.rcv_time = None  # String	数据接收时间                                              "20200608140053830"
#     #         self.order_id = None  # String	订单ID（对应xtpid）                    orderXtpId         "36934130021173201"
#     #         self.parent_order_id = None  # String	母单ID                               # runtimeId          "6a1071e1-a94d-11ea-810c-4b25bab2cda3"
#     #         self.trade_time = None  # String	成交时间                              tradeTime          "20200608140053830"
#     #         self.instrument_id = None  # String	合约ID（证券代码）                     ticker              "600000"
#     #         self.exchange_id = Exchange.Unknown  # String	交易所ID                              xtpMarketType转换   "SSE"
#     #         self.account_id = None  # String	账号ID（资金账号）                     userName            "10912133333344"
#     #         self.client_id = None  # String	用户自定义编号                         rowId || orderClientId (rowid优先)  "6a1071e1-a94d-11ea-810c-4b25bab2cda3"
#     #         self.instrument_type = None  # Number	合约类型                              xtpBusinessType转换  InstrumentType.Stock
#     #         self.side = None  # Number	买卖方向                              xtpSideType
#     #         self.offset = None  # Number	开平方向                              xtpPositionEffectType
#     #         self.price = None  # Number	价格                                  price               10.23
#     #         self.volume = None  # Number	数量                                  quantity            100
#     #         self.tax = None  # Number	税                                   todo:
#     #         self.commission = None  # Number	手续费                                todo:
#     #         self.code = None  # String  证券代码.交易所标识                     "600000.SH"

#     #         self.instrument_name = None  # String  合约名称（证券名称）                    tickerName            "浦发银行"
#     #         self.trade_amount = None  # Number  委托金额                              tradeAmount           0
#     #         self.xtp_business_type = None  # String  xtp证券业务类型                        xtpBusinessType       "XTP_BUSINESS_TYPE_CASH"
#     #         self.xtp_market_type = "XTP_MKT_UNKNOWN"  # String  xtp市场类型                            xtpMarketType         "XTP_MKT_SZ_A"

#     #         self.xtp_exec_id = None  # String  成交编号()                            execId                "15790"
#     #         self.xtp_report_index = None  # String  成交序号()                            reportIndex           "6806"
#     #         self.xtp_order_exch_id = None  # String  报单编号 –交易所单号，上交所为空，深交所有此字段 orderExchId     ""
#     #         self.xtp_trade_type = None  # String  成交类型                              tradeType             "1" 代表XTP_TRDT_CASH 现金替代"
#     #         self.xtp_branch_pbu = None  # String  交易所交易员代码                       branchPbu             "13688"

#     #         # 以下为xtp的冗余字段，为了获取xtp的原值
#     #         self.xtp_position_effect_type = None  # String xtp开平方向                  xtpPositionEffectType "XTP_POSITION_EFFECT_OPEN"
#     #         self.xtp_side_type = None  # String  xtp交易方向                            xtpSideType           "XTP_SIDE_BUY"

#     #         # 以下为xtp和alphax枚举值翻译为中文的名称
#     #         self.exchange_id_name = None  # String  交易所名称                                                  "上交所"
#     #         self.instrument_type_name = None  # String  合约类型名称                                                "股票"
#     #         self.side_name = None  # String  买卖方向名称                                                "买"
#     #         self.offset_name = None  # String  开平方向名称                                                "开"
#     #         self.xtp_business_type_name = None  # String  xtp证券业务类型名称                                          "现货"
#     #         self.xtp_market_name = None  # String  xtp市场类型名称                                             "沪市"
#     #         self.xtp_position_effect_type_name = None  # String  xtp开平方向名称                                             "开"
#     #         self.xtp_side_type_name = None  # String  xtp交易方向名称                                             "买"
#     #         self.traffic_name = None  # String  业务渠道名称                                                "策略"
#     #         self.xtp_trade_type_name = None  # String  成交类型名称                                                "现金替代"
#     #         self._rowid = None #String 仅用于内部标识
#     # 行情信息-Quote
#     # 行情信息

#     # class Quote():
#     #     def __int__(self):
#     #         self.source_id = None  # 柜台ID xtp缺少
#     #         self.trading_day = None  # 交易日 xtp缺少
#     #         self.rcv_time = None  # 数据接收时间 xtp缺少
#     #         self.data_time = None  # 数据生成时间 dataTime
#     #         self.instrument_id = None  # 合约ID ticker
#     #         self.exchange_id = None  # 交易所 exchangeId XTP_EXCHANGE_SH
#     #         self.instrument_type = None  # 合约类型 xtp缺少
#     #         self.pre_close_price = None  # 昨收价 preClosePrice
#     #         self.pre_settlement_price = None  # 昨结价 xtp缺少
#     #         self.last_price = None  # 最新价 lastPrice
#     #         self.volume = None  # 成交数量 qty
#     #         self.turnover = None  # 成交金额 turnover
#     #         self.pre_open_interest = None  # 昨持仓量 xtp缺少
#     #         self.open_interest = None  # 持仓量 xtp缺少
#     #         self.open_price = None  # 今开盘 openPrice
#     #         self.high_price = None  # 最高价 highPrice
#     #         self.low_price = None  # 最低价 lowPrice
#     #         self.upper_limit_price = None  # 涨停板价 upperLimitPrice
#     #         self.lower_limit_price = None  # 跌停板价 lowerLimitPrice
#     #         self.close_price = None  # 收盘价 closePrice
#     #         self.settlement_price = None  # 结算价 xtp缺少
#     #         self.bid_price = None  # 申买价数组 如[11, 10.55, 10, 0, 0, 0, 0, 0, 0, 0] bid
#     #         self.ask_price = None  # 申卖价数组 ask
#     #         self.bid_volume = None  # 申买量数组 如[1000, 14700, 100, 0, 0, 0, 0, 0, 0, 0] bidQty
#     #         self.ask_volume = None  # 申卖量数组 askQty
#     #         self.code = None  # 证券代码.交易所标识 如"600000.SH"
#     #         # 以下是alphax缺少的
#     #         self.avg_price = None  # 当日均价 alphax缺少
#     #         self.iopv = None  # iopv alphax缺少
#     #         self.instrument_status = None  # 证券状态 如"E110    "详见https://xtp.zts.com.cn/doc/api/FAQ 问题编号64
#     # 证券instrument_status状态信息：

#     # 对于普通股票，具体值如下 第0位： S=启动（开市前） C=集合竞价(不分开盘收盘) T=连续竞价 B=休市 E=闭市 P=停牌 A=盘后交易 V=波段性中断 第1位： 0=不可正常交易， 1=可正常交易， 无意义填空格 第2位： 0=未上市， 1=已上市； （深交所忽略该字段） 如图所示：

# def show():
#     print("show")
# def hide():
#     print("hide")
# def close():
#     print("close")

# smart.on_init(init)
# smart.on_show(show)
# smart.on_hide(hide)
# smart.on_close(close)