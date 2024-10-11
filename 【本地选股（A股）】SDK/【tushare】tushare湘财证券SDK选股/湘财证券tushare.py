import datetime
import pandas as pd
# pip install xcsc-tushare
import xcsc_tushare as ts
# ts.set_token('7ed61c98882a320cadce6481aef04ebf7853807179d45ee7f72089d7')
# ts.pro_api(server='http://116.128.206.39:7172')   #指定tocken对应的环境变量，此处以生产为例
pro = ts.pro_api('7ed61c98882a320cadce6481aef04ebf7853807179d45ee7f72089d7',server='http://116.128.206.39:7172')

# # 获取南华沪铜指数【拿不到数据】
# df = pro.index_daily(ts_code='CU.NH', start_date='20210101', end_date='20221201')
# print(df)

# #【ETF基础信息】
# #输出所有ETF详情
# df = pro.fund_basic(market='E')
# df=df.rename(columns={
#                 "ts_code":"基金代码",#strY	
#                 "name":"简称",#strY	
#                 "management":"管理人",#strY	
#                 "custodian":"托管人",#strY	
#                 "fund_type":"投资类型",#strY	
#                 "found_date":"成立日期",#strY	
#                 "due_date":"到期日期",#strY	
#                 "list_date":"上市时间",#strY	
#                 "issue_date":"发行日期",#strY	
#                 "delist_date":"退市日期",#strY	
#                 "issue_amount":"发行份额",#(亿)	strY	
#                 "m_fee":"管理费",#floatY	
#                 "c_fee":"托管费",#floatY	
#                 "duration_year":"存续期",#floatY	
#                 "p_value":"面值",#floatY	
#                 "min_amount":"起点金额",#(万元)#floatY	
#                 "exp_return":"预期收益率",#floatY
#                 "benchmark":"业绩比较基准",#strY	
#                 "status":"存续状态",#D摘牌 I发行 L已上市#strY	
#                 "invest_type":"投资风格",#strY	
#                 "type":"基金类型",#strY	
#                 "trustee":"受托人",#strY	
#                 "purc_startdate":"日常申购起始日",#strY	
#                 "redm_startdate":"日常赎回起始日",#strY	
#                 "market":"E场内O场外",#strY	
#                 })
# print(df)
# #输出基金持仓信息（只有十大重仓股）
# df = pro.fund_portfolio(ts_code='510680.SH')
# df=df.rename(columns={
#                 "ts_code":"基金代码",# str	Y
#                 "ann_date":"公告日期",# str	Y
#                 "end_date":"截止日期",#	str	Y	
#                 "symbol":"股票代码",# str Y	
#                 "mkv":"持有股票市值(元)",# float Y	
#                 "amount":"持有股票数量（股）",# float Y	
#                 "stk_mkv_ratio":"占股票市值比",# float Y	
#                 "stk_float_ratio":"占流通股本比例",# float Y	
#                 "update_flag":"更新标识",#（1为最新）str Y	
#                 })
# print(df)#这个只更新了十大重仓股的权重
# df.to_csv("基金调仓信息.csv")

# # #获取每周末或不定期更新的基金净值
# # df=pro.fund_nav_1(price_date='20181231')
# # print(df)

# # 共同基金持券明细
# # df=pro.fund_bond_portfolio(ts_code='000001.OF')#华夏成长混合基金
# # print(df)


# #【可转债基础信息】
# df=pro.cb_basic(fields="ts_code,bond_full_name,stk_code,remain_size,conv_price,maturity_date")
# df=df.reset_index()
# df=df.rename(columns={"ts_code":"代码",
#                     "bond_full_name":"转债名称",
#                     "stk_code":"正股代码",
#                     "remain_size":"债券余额",
#                     "conv_price":"最新转股价",
#                     "maturity_date":"到期日期",})
# df=df[df["债券余额"]>0]#只要还有余额的转债
# df["到期日期"]=pd.to_datetime(df['到期日期'], format='%Y-%m-%d')#到期日列字符串格式转datetime格式
# alldf=df[df["到期日期"]>(datetime.datetime.now()+datetime.timedelta(days=180))]#只保留180日后到期的
# alldf.to_csv("可转债基础信息.csv")
# #可转债赎回信息（历史上只有40个到期赎回的标的，基本都是转股或者强赎）
# # ts_code	str	Y	转债代码
# # call_type	str	Y	赎回类型：
# # is_call	str	Y	是否赎回：公告到期赎回、公告强赎、公告不强赎
# # ann_date	str	Y	公告日期
# # call_date	str	Y	赎回日期
# # call_price	float	Y	赎回价格(含税，元/张)
# # call_price_tax	float	Y	赎回价格(扣税，元/张)
# # call_vol	float	Y	赎回债券数量(张)
# # call_amount	float	Y	赎回金额(万元)
# # payment_date	str	Y	行权后款项到账日
# # call_reg_date	str	Y	赎回登记日
# df=pro.cb_call(fields=['ts_code', 'call_type', 'is_call', 'ann_date', 'call_date','call_price'])
# df=df.reset_index()
# df=df.rename(columns={"ts_code":"代码",
#                     "call_type":"赎回类型",#到赎、强赎
#                     "is_call":"是否赎回",#公告到期赎回、公告强赎、公告不强赎
#                     "ann_date":"公告日期",
#                     "call_date":"赎回日期",})
# df["赎回日期"]=pd.to_datetime(df['赎回日期'], format='%Y-%m-%d')#到期日列字符串格式转datetime格式
# df.to_csv("可转债强赎信息.csv")
# dropalldf=df[(df["赎回类型"]=="到赎")|(df["是否赎回"]=="公告到期赎回")]#未来180日内公告到期赎回的需要去掉【一般上述两列的数据是一致的】
# dropalldf=dropalldf[(dropalldf["赎回日期"]<(datetime.datetime.now()+datetime.timedelta(days=180)))]#只保留在未来180日只能到期赎回的可转债
# dropalldf=dropalldf[(dropalldf["赎回日期"]>(datetime.datetime.now()-datetime.timedelta(days=50)))]#去掉10天前已经赎回的干扰数据
# dropalldf.to_csv("可转债近期到赎.csv")
# dropdf=df[df["赎回类型"]=="强赎"]#未来180日内公告到期赎回的需要去掉
# dropdf=dropdf[(dropdf["是否赎回"]=="公告实施强赎")]
# dropdf=dropdf[(dropdf["赎回日期"]<(datetime.datetime.now()+datetime.timedelta(days=180)))]#只保留在未来180日只能强赎的可转债
# dropdf=dropdf[(dropdf["赎回日期"]>(datetime.datetime.now()-datetime.timedelta(days=50)))]#去掉10天前已经赎回的干扰数据
# dropdf.to_csv("可转债近期强赎.csv")
# alldf=alldf[~((alldf["代码"].isin(dropdf["代码"].tolist())|alldf["代码"].isin(dropalldf["代码"].tolist())))]
# alldf.to_csv("可转债去掉近期赎回标的后.csv")



# # #获取交易日数据
# # df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001')
# # print(df)
# # df = pro.query('trade_cal', exchange='', start_date='20180901', end_date='20181001')
# # print(df)
# # #除息除权数据
# # df = pro.div(start_date='20230121',end_date='20240221',fields='ts_code,ex_date,ex_type,ex_description,cash_dividend_ratio')
# # print(df)
# # # 财报披露计划
# # df = pro.disclosure_date(end_date='20240221')
# # print(df)
# # #获取财报数据
# # df = pro.fin_indicator_basic(ts_code='600000.SH',fields='ts_code,report_period,s_fa_extraordinary,s_fa_orps')
# # print(df)
# #股东人数【每次财报周期都会公布】
# df = pro.stk_holdernumber(ts_code='300199.SZ', start_date='20190101', end_date='20240431')
# print(df)#这个股东人数可能是衡量投资者关注度的优秀指标
# #大宗交易【每天大概100条】
# df = pro.block_trade(trade_date='20240513')#一般交易日都有数据【大概50-100条左右】
# print(df)
# # #获取股票开户数据【已停用】
# # df = pro.stk_account(start_date='20210101', end_date='20231231')
# # print(df)
# # #总股本【测试账户无法使用】
# # df = pro.daily_basic_ts(trade_date='20020220', fields="ts_code,trade_date,total_share")
# # print(df)