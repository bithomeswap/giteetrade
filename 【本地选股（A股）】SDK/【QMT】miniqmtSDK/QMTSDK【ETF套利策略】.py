# #【同花顺APP上有申赎清单信息，但是没接口拿到】
# #【iopv数据据说软件上的计算方式有延迟，而且抢的人多肯定要高频低延迟才能抢到】
# # 集思录的ETF净值数据比问财出来的速度快【估值就是iopv，现价除以估值就是溢价率】
# # 爬虫循环获取网页信息比较可靠【每一个基金也可以单独获取申赎额度等信息】
# # 集思录ETF净值数据地址：https://www.jisilu.cn/data/etf/#index
# # 景顺长城申赎详情：https://www.igwfmc.com/main/jjcp/product/513980/detail.html
# # 国联安申赎详情：https://www.cpicfunds.com/product/516480/index.shtml

# pip install lxml
import requests
import pandas as pd
# 目标网页URL
# url = r'https://www.jisilu.cn/data/etf/#index'
url = "https://www.jisilu.cn/webapi/etf/index_history/"
r = requests.get(url)
from akshare.utils import demjson
data_dict = demjson.decode(r.text)["data"]
temp_df = pd.DataFrame(data_dict)
print(temp_df)

# #申赎清单可以从上交所，iopv可以走集思录，成交额直接问财一遍过
# #【据说湘财证券在研发相关的ETF套利模块，未来会给普通用户使用，自己从头去写成本过高了】
# import pandas as pd
# import datetime
# import time
# now=datetime.datetime.now()
# startday=now.strftime("%Y%m%d")
# # lastday=(now-datetime.timedelta(days=365)).strftime("%Y%m%d")
# lastday=(now-datetime.timedelta(days=60)).strftime("%Y%m%d")

# # pip install xcsc-tushare
# import xcsc_tushare as ts
# # ts.set_token('7ed61c98882a320cadce6481aef04ebf7853807179d45ee7f72089d7')
# # ts.pro_api(server='http://116.128.206.39:7172')   #指定tocken对应的环境变量，此处以生产为例
# pro = ts.pro_api('7ed61c98882a320cadce6481aef04ebf7853807179d45ee7f72089d7',server='http://116.128.206.39:7172')
# tradedaydf = pro.query('trade_cal',
#                 exchange='SSE',#交易所 SZN-深股通,SHN-沪股通,SSE-上海证券交易所,SZSE-深圳证券交易所
#                 start_date=lastday,
#                 end_date=startday)
# tradedaydf['trade_date'] = pd.to_datetime(tradedaydf['trade_date'], format='%Y%m%d')
# tradedaydf['trade_date'] = tradedaydf['trade_date'].dt.strftime('%Y-%m-%d')
# print(tradedaydf)
# tradedays=tradedaydf["trade_date"].tolist()

# # node -v
# # #需要提前安装node.js抓网页数据，如果没node.js会报错
# # pip install pywencai -U#python3.7版本调用这个函数就报错：module 'pywencai' has no attribute 'get'
# import pywencai#同花顺的最新净值数据不是iopv不能用来计算溢价率
# try:
#     df=pd.read_csv(f"ETF详情{startday}.csv")
#     print(f"ETF详情{startday}.csv","存在")
# except Exception as e:
#     print(e)
#     print(f"ETF详情{startday}.csv","不存在")
#     # ETF净值数据【当天】
#     # 【申购、赎回费率】跟官网对比了一下问财的最高申购赎回费率是准确的【具体说法是：申购赎回代理券商可按照不超过 0.4%的标准收取佣金】
#     # 【价格及净值数据】，不是实时的，
#     # 【最近十日成交额】和【最近十日逐日成交额】有差异，但是都是准确的现在用的【最近十日逐日成交额】
#     # 【成分股详情】只包含重仓股
#     word=f'{startday}所有ETF，最高申购费率、最高赎回费率，最近十日逐日成交额'
#     df=pywencai.get(question=word,#query参数
#                     loop=True,
#                     query_type="fund",
#                     # pro=True, #付费版才使用
#                     # cookie='xxxx',
#                     )
#     for day in tradedays[-10:]:
#         print(day)
#         df[f"{day.replace('-','')}日成交额"]=df[f"基金@成交额[{day.replace('-','')}]"].astype(float)
#         df=df.sort_values(by=f"{day.replace('-','')}日成交额",ascending=False)#成交额降序排列
#         df=df[df[f"{day.replace('-','')}日成交额"]>10000000]#卡在最近十天每天成交额大于一个亿从999只变成了418只
#     print(df)
#     df.to_csv(f"ETF详情{startday}.csv")






# #现在就是差一个iopv一个ETF申赎清单【上交所官网有公布】
# # "//query.sse.com.cn/etfDownload/downloadETF2Bulletin.do?etfType=006"






# # #勾选独立交易之后，行情、交易、交易+行情选项一个都不要选择，才能启动miniqmt成功，否则无法执行订单
# # import datetime
# # import time
# # import math
# # import pandas as pd#conda install pandas
# # import numpy as np#pip install numpy

# # #【只要不用supermind，就可以直接使用3.12最新版的python执行策略】
# # # supermind的SDK作废了拿不到数据，尽量使用pywencai库直接从问财接口获取
# # # conda create -n my_env8 python=3.8#创建环境
# # # conda env remove -n my_env8#删除环境

# # xtdata提供和MiniQmt的交互接口,本质是和MiniQmt建立连接,由MiniQmt处理行情数据请求,再把结果回传返回到python层。使用的行情服务器以及能获取到的行情数据和MiniQmt是一致的,要检查数据或者切换连接时直接操作MiniQmt即可。
# # 对于数据获取接口,使用时需要先确保MiniQmt已有所需要的数据,如果不足可以通过补充数据接口补充,再调用数据获取接口获取。
# # 对于订阅接口,直接设置数据回调,数据到来时会由回调返回。订阅接收到的数据一般会保存下来,同种数据不需要再单独补充。
# from xtquant import xtdata

# # #测试里面买不了深证的是因为没开相关记录,上证的正常买入没有限制
# # 配置日志
# basepath=r"C:\Users\13480\gitee\trade\【本地选股（A股）】SDK\【QMT】miniqmtSDK"
# # pip install loguru # 这个框架可以解决中文不显示的问题
# from loguru import logger
# logger.add(
#     sink=f"{basepath}/log.log",#sink: 创建日志文件的路径。
#     # sink=f"log.log",#sink: 创建日志文件的路径。
#     level="INFO",#level: 记录日志的等级,低于这个等级的日志不会被记录。等级顺序为 debug < info < warning < error。设置 INFO 会让 logger.debug 的输出信息不被写入磁盘。
#     rotation="00:00",#rotation: 轮换策略,此处代表每天凌晨创建新的日志文件进行日志 IO；也可以通过设置 "2 MB" 来指定 日志文件达到 2 MB 时进行轮换。   
#     retention="7 days",#retention: 只保留 7 天。 
#     compression="zip",#compression: 日志文件较大时会采用 zip 进行压缩。
#     encoding="utf-8",#encoding: 编码方式
#     enqueue=True,#enqueue: 队列 IO 模式,此模式下日志 IO 不会影响 python 主进程,建议开启。
#     format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"#format: 定义日志字符串的样式,这个应该都能看懂。
# )

# def symbol_convert(stock):#股票代码加后缀
#     #北交所的股票8字开头，包括82、83、87、88，其中82开头的股票表示优先股；83和87开头的股票表示普通股票、88开头的股票表示公开发行的。
#     if (stock.startswith("60"))or(#上交所主板
#         stock.startswith("68"))or(#上交所科创板
#         stock.startswith("11"))or(#上交所可转债
#         (stock.startswith("5"))):#上交所ETF：51、52、56、58都是
#         return str(str(stock)+".SH")
#         # return str(str(stock)+".SS")
#     elif (stock.startswith("00"))or(#深交所主板
#         stock.startswith("30"))or(#深交所创业板
#         stock.startswith("12"))or(#深交所可转债
#         (stock.startswith("159"))):#深交所ETF：暂时只有159的是深交所ETF
#         return str(str(stock)+".SZ")
#     else:
#         print("不在后缀转换名录",str(stock))
#         return str(str(stock))

# import datetime
# import time
# now=datetime.datetime.now()
# start_date=now.strftime("%Y%m%d")#测试当天的数据
# # last_date=(now-datetime.timedelta(days=730)).strftime("%Y%m%d")
# last_date=(now-datetime.timedelta(days=250)).strftime("%Y%m%d")
# while True:
#     # 获取交易日期
#     tradelist=xtdata.get_trading_dates("SH",start_time="",end_time=start_date,count=2)
#     logger.info(f"{tradelist}")
#     if len(tradelist)!=0:
#         logger.info("日期获取成功")
#         today=tradelist[-1]
#         today=datetime.datetime.fromtimestamp(today/1000)
#         today=today.strftime("%Y%m%d")
#         yesterday=tradelist[0]
#         yesterday=datetime.datetime.fromtimestamp(yesterday/1000)
#         yesterday=yesterday.strftime("%Y%m%d")
#         break
#     else:
#         logger.info("日期获取失败")
#         time.sleep(10)
#         today=now.strftime("%Y%m%d")
#         yesterday=(now-datetime.timedelta(days=1)).strftime("%Y%m%d")
#         break
# logger.info(f"******"+"today"+today+"yesterday"+yesterday)

# #交易模块
# import random
# from xtquant.xttype import StockAccount
# from xtquant.xttrader import XtQuantTrader
# from xtquant import xtconstant
# # QMT账号
# # mini_qmt_path = r"D:\迅投极速交易终端 睿智融科版\userdata_mini"# miniQMT安装路径
# # account_id = "2011506"# QMT账号
# # account_id = "2011908"
# # mini_qmt_path = r"D:\国金QMT交易端模拟\userdata_mini"# miniQMT安装路径
# mini_qmt_path = r"C:\国金QMT交易端模拟\userdata_mini"# miniQMT安装路径

# account_id = "55013189"
# if (account_id=='55013189')or(account_id=='2011506')or(account_id=="2011908"):#密码:wth000
#     # choosename="可转债"
#     choosename="微盘股"
#     tradeway="taker"#设置主动吃单
#     # tradeway="maker"#设置被动吃单
# else:
#     choosename="微盘股"
#     tradeway="taker"#设置主动吃单
# session_id = int(random.randint(100000,999999))# 创建session_id
# trade_api = XtQuantTrader(mini_qmt_path,session_id)# 创建交易对象
# trade_api.start()# 启动交易对象

# while True:
#     connect_result = trade_api.connect()# 连接客户端
#     print("连接结果",connect_result)
#     if connect_result==0:
#         logger.info("连接成功")
#         break
#     else:
#         logger.info("重新链接")
#         time.sleep(1)

# acc = StockAccount(account_id)# 创建账号对象
# trade_api.subscribe(acc)# 订阅账号
# # #设置交易参数并且获取买卖计划
# # bidrate=0.005#设置盘口价差为0.004
# # timecancellwait=60#设置撤单函数筛选订单的确认时间
# # timetickwait=600#设置每次下单时确认是否是最新tick的确认时间【3秒一根，但是模拟盘的tick滞后五分钟左右】
# # timeseconds=60#设置获取tick的函数的时间长度【避免没有数据】
# # targetmoney=20000#设置下单时对手盘需要达到的厚度（即单笔目标下单金额,因为手数需要向下取整,所以实际金额比这个值低）
# # traderate=2#设置单次挂单金额是targetmoney的traderate倍
# # # cancellorder=False#取消一分钟不成交或者已成交金额达到目标值自动撤单并回补撤单金额的任务
# # cancellorder=True#设置一分钟不成交或者已成交金额达到目标值自动撤单并回补撤单金额的任务

# logger.info(f"{now},{choosename},{account_id},{start_date},{last_date},{today},{yesterday}")

# buyfilename=choosename+"买入.csv"
# sellfilename=choosename+"卖出.csv"
# logger.info(f"{buyfilename},{sellfilename}")
# buydf=pd.read_csv(str(basepath)+f"/{str(start_date)}"+buyfilename)
# selldf=pd.read_csv(str(basepath)+f"/{str(start_date)}"+sellfilename)
# #确认买入数量【即持仓数量】
# targetnum=len(buydf)#一般是30
# logger.info(f"预计持仓只数,{targetnum}")

# #查询资产
# portfolio=trade_api.query_stock_asset(account=acc)
# logger.info(f"查询资产,portfolio")#收盘之后估计会返回空值
# available_cash=portfolio.cash#available_cash可用资金
# market_value=portfolio.market_value#market_value证券市值
# frozen_cash=portfolio.frozen_cash#frozen_cash冻结资金
# total_value=portfolio.total_asset#total_asset总资产
# logger.info(f"******"+"可用资金"+str(available_cash)+"证券市值"+str(market_value)+"冻结资金"+str(frozen_cash)+"总资产"+str(total_value))
# premoney=(total_value)/targetnum#确定每只股票的交易金额（根据目标持仓数量制定）

# #同花顺内打出来的数据（字符串数据）
# buydf["代码"]=buydf["代码"].astype(str).str.zfill(6).apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
# selldf["代码"]=selldf["代码"].astype(str).str.zfill(6).apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
# logger.info(f"buydf,{buydf}")

# logger.info(f"针对涨停标的不进行卖出处理之前selldf,{len(selldf)}")
# positions=trade_api.query_stock_positions(account=acc)
# for position in positions:
#     symbol=position.stock_code
#     logger.info(symbol)
#     if position.volume>0:
#         logger.info(position.volume)
#         try:
#             #返回五档数据
#             tick=xtdata.get_full_tick([symbol])
#             tick=tick[symbol]
#             ask_price_1=tick["askPrice"][0]
#             ask_volume_1=tick["askVol"][0]
#             ask_price_2=tick["askPrice"][1]
#             ask_volume_2=tick["askVol"][1]
#             logger.info(f"{ask_price_1},{ask_volume_1},{ask_price_2},{ask_volume_2}")
#             if (ask_price_2==0)and(ask_price_1==0):
#                 logger.info(f"{symbol},涨停不进行卖出")
#                 if symbol not in selldf["代码"].tolist():
#                     selldf=pd.concat([selldf,pd.DataFrame({"代码":[symbol],"排名":[0]})])
#         except Exception as e:#报索引越界一般是tick数据没出来
#             logger.info(f"******,发生bug:,{symbol},{e}")
# logger.info(f"针对涨停标的不进行卖出处理之后selldf,{len(selldf)}")

# logger.info(f"针对跌停标的不进行买入处理之前buydf,{len(buydf)}")
# for symbol in buydf["代码"].tolist():
#     try:
#         #返回五档数据
#         tick=xtdata.get_full_tick([symbol])
#         tick=tick[symbol]
#         ask_price_1=tick["askPrice"][0]
#         ask_volume_1=tick["askVol"][0]
#         ask_price_2=tick["askPrice"][1]
#         ask_volume_2=tick["askVol"][1]
#         logger.info(f"{ask_price_1},{ask_volume_1},{ask_price_2},{ask_volume_2}")
#         if (ask_price_2==0)and(ask_price_1==0):
#             logger.info(symbol,"涨停不进行买入")
#             buydf=pd.concat([buydf,pd.DataFrame({"代码":[symbol],"排名":[0]})])
#         bid_price_1=tick["bidPrice"][0]
#         bid_volume_1=tick["bidVol"][0]
#         bid_price_2=tick["bidPrice"][1]
#         bid_volume_2=tick["bidVol"][1]
#         logger.info(f"{bid_price_1},{ask_volume_1},{bid_price_2},{bid_volume_2}")
#         if (bid_price_2==0)and(bid_price_1==0):
#             logger.info(symbol,"跌停不进行买入")
#             buydf=buydf[~(buydf["代码"]==symbol)]
#     except Exception as e:#报索引越界一般是tick数据没出来
#         logger.info("******","发生bug:",symbol,e)
# logger.info("针对跌停标的不进行买入处理之后buydf",len(buydf))
# logger.info("注意事项【停牌标的也算作涨跌停标的了】")
            
# targetcolumn="排名"
# dfone=buydf.copy()
# dftwo=selldf.copy()
# buydf=buydf[["代码",targetcolumn]]
# selldf=selldf[["代码",targetcolumn]]
# buydf["moneymanage"]=premoney
# moneymanage=buydf[["代码","moneymanage"]]
# ordernum=0#初始化当前交易轮次为0
# logger.info(f"策略启动,account_id,{account_id},premoney,{premoney}")

# dfposition=pd.DataFrame([])
# positions=trade_api.query_stock_positions(account=acc)
# for position in positions:
#     symbol=position.stock_code
#     logger.info(symbol,position.volume)
#     if position.volume>0:
#         dfposition=pd.concat([dfposition,pd.DataFrame({"symbol":[symbol],
#                                                         "volume":[position.volume],
#                                                         "can_use_volume":[position.can_use_volume],
#                                                         "frozen_volume":[position.frozen_volume],
#                                                         "market_value":[position.market_value],
#                                                         })],ignore_index=True)
# logger.info(f"******,本轮持仓,{dfposition}")
# dfposition.to_csv(str(basepath)+"_dfposition.csv")
# #判断交易计划
# selldflist=dftwo["代码"].tolist()
# buydflist=dfone["代码"].tolist()

# # 获取当前时间
# thistime=datetime.datetime.now()

# # #【设置1、4月空仓】
# # if ((thistime.month==4)or(thistime.month==1)):
# #     logger.info(thistime.month,"当前月份空仓")
# #     selldflist=[]
# #     buydflist=[]

# if not dfposition.empty:#持仓不为空值
#     positionsymbols=dfposition["symbol"].tolist()
#     falsesymbol=[x for x in positionsymbols if x not in selldflist]
#     truesymbol=[x for x in positionsymbols if x in selldflist]
#     havesymbol=[x for x in buydflist if x in positionsymbols]
#     nothavesymbol=[x for x in buydflist if x not in positionsymbols]
#     logger.info("******"+
#         "不在卖出观察池的需卖出标的"+
#         f"{falsesymbol}"+
#         "在卖出观察池的正确持仓标的"+
#         f"{truesymbol}"+
#         "在买入观察池的已持仓标的"+
#         f"{havesymbol}"+
#         "在买入观察池的未持仓标的"+
#         f"{nothavesymbol}"+
#         "持仓标的"+
#         f"{positionsymbols}"
#     )
#     selldf=dfposition.copy()#只针对持仓当中的标的筛选应卖出标的
#     buydf=dfone.copy()
#     selldf=selldf[~(selldf["symbol"].isin(dftwo["代码"].tolist()))]
#     logger.info(f"实际应卖出股票,去掉应持有标的后,{len(selldf)}")
#     # selldf=selldf[~(selldf["symbol"].isin(upstocks))]
#     logger.info(f"实际应卖出股票,去掉涨停标的后,{len(selldf)}")
#     if len(selldf)>0:
#         #应买入股票处理
#         buydf=buydf[~(buydf["代码"].isin(selldf["symbol"].tolist()))]
#         buydf=buydf[~(buydf["代码"].isin(dfposition["symbol"].tolist()))]
#         logger.info(f"实际应买入股票,去除应卖出标的后,{len(buydf)}")
#         #计算卖出后剩余持仓数量
#         hodlstocks=len(dfposition["symbol"].tolist())-len(selldf["symbol"].tolist())
#         logger.info(f"卖出后剩余持仓数量,{hodlstocks}")
#         if hodlstocks!=0:
#             buydf=buydf.sort_values(by=targetcolumn)
#             buydf=buydf[:(targetnum-hodlstocks)]#这里减去的是持仓股票数量,然后在持仓标的中选择金额不足的向上拼接
#             logger.info(f"对买入计划重新配置之后,{len(buydf)}")
#     else:
#         logger.info("应卖出股票只数小于0,直接去除掉当前的持仓标的计算买入计划")
#         #应买入股票处理
#         buydf=buydf[~(buydf["代码"].isin(dfposition["symbol"].tolist()))]
#         logger.info(f"实际应买入股票,去除应卖出标的后,{len(buydf)}")
#         #计算卖出后剩余持仓数量
#         hodlstocks=len(dfposition["symbol"].tolist())-len(selldf["symbol"].tolist())
#         logger.info(f"全部卖出后剩余持仓数量,{hodlstocks}")
#         if hodlstocks!=0:
#             buydf=buydf.sort_values(by=targetcolumn)
#             buydf=buydf[:(targetnum-hodlstocks)]#这里减去的是持仓股票数量,然后在持仓标的中选择金额不足的向上拼接
#             logger.info(f"对买入计划重新配置之后,{len(buydf)}")
# else:
#     if (len(selldflist)==0)and(len(buydflist)==0):
#         logger.info(f"{thistime.month},当月空仓")
#         selldf=pd.DataFrame({"代码":[],"总市值":[]})
#         buydf=pd.DataFrame({"代码":[],"总市值":[]})
#     else:
#         logger.info(f"{thistime.month},正常交易")
#         selldf=dftwo.copy()
#         buydf=dfone.copy()
#     logger.info(f"实际应卖出股票,{len(selldf)}")
#     logger.info(f"实际应买入股票,{len(buydf)}")
# selldf=selldf.reset_index(drop=True)
# selldf.to_csv(str(basepath)+"selldf.csv")
# buydf=buydf.reset_index(drop=True)
# buydf.to_csv(str(basepath)+"buydf.csv")
# logger.info(f"实际卖出计划,{selldf},实际买入计划,{buydf}")

# #进行交易计划之前的资金管理机制【计算需要对哪些进行买入对哪些进行卖出】
# premoney=(total_value)/targetnum#每股理论应持仓金额
# #注意这个金额还得补之前超跌的股票的部分的差额
# buydf["moneymanage"]=premoney
# moneymanage=buydf[["代码","moneymanage"]]
# logger.info("单股金额"+str(premoney)+"moneymanage"+str(moneymanage))
# if not dfposition.empty:
#     holddf=dfposition.copy()
#     holddf=holddf[~(holddf["symbol"].isin(selldf["symbol"].tolist()))]
#     for index,thisposition in holddf.iterrows():#余额不为零才进行下一步免得浪费时间
#         logger.info(f"{index},{thisposition}")
#         symbol=thisposition["symbol"]
#         # logger.info("symbol",symbol)
#         if thisposition["volume"]>0:#只对当前持仓大于0的标的进行处理，如果第一次执行就是volume，如果二次执行需要使用can_use_volume
#             thispositionmoney=thisposition["market_value"]
#             # if (premoney-thispositionmoney)>float(0.0000001)*premoney:#持仓标的与其总资产平均后的理论应持仓市值的偏差在百分之十以上才执行
#             if (premoney-thispositionmoney)>float(0.1)*premoney:#持仓标的与其总资产平均后的理论应持仓市值的偏差在百分之十以上才执行
#                 logger.info(f"{symbol},thispositionmoney,{thispositionmoney},premoney,{premoney},持仓标的与其总资产平均后的理论应持仓市值的偏差在百分之十以上执行补仓操作")
#                 if symbol not in moneymanage["代码"].tolist():
#                     newdata=pd.DataFrame([{"代码":symbol,"moneymanage":(premoney-thispositionmoney)}])
#                     moneymanage=pd.concat([moneymanage,newdata],ignore_index=True)
#                     logger.info(f"******,拼接上之前应买入未买全的股票,之后最新的下单金额计划,{moneymanage}")
#                 elif symbol in moneymanage["代码"].tolist():
#                     moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]=(premoney-thispositionmoney)
#                     logger.info(f"******,更新完之前应买入未买全的股票,之后最新的下单金额计划,{moneymanage}")
#     moneymanage=moneymanage[moneymanage["moneymanage"]>=targetmoney]#只保留应下单金额大于targetmoney的标的
# else:
#     logger.info("当前没有持仓,无需对下单计划进行调整")
# logger.info(moneymanage)

# #初始化存储已经撤销订单的列表【只初始化一次,不要重置】
# dfordercancelled=pd.DataFrame({})
# while True:
#     dforderalls=pd.DataFrame({})#初始化存储全部订单的列表【每一轮都可以重置】
#     ordernum+=1#交易轮次计数,避免频繁撤单
#     if ordernum>1:
#         logger.info(f"{datetime.datetime.now()},从第二轮开始每执行一轮休息5秒避免订单过度冲击市场,当前轮次,{ordernum}")
#         # time.sleep(5)#休息一秒,避免空转
#         time.sleep(1)#休息一秒,避免空转
#     # # 成交XtTrade
#     # trades = trade_api.query_stock_trades(account=acc)#成交记录
#     # logger.info(trades)
#     # # 属性	类型	注释
#     # # account_type	int	账号类型,参见数据字典
#     # # account_id	str	资金账号
#     # # stock_code	str	证券代码
#     # # order_type	int	委托类型,参见数据字典
#     # # traded_id	str	成交编号
#     # # traded_time	int	成交时间
#     # # traded_price	float	成交均价
#     # # traded_volume	int	成交数量
#     # # traded_amount	float	成交金额
#     # # order_id	int	订单编号
#     # # order_sysid	str	柜台合同编号
#     # # strategy_name	str	策略名称
#     # # order_remark	str	委托备注
#     # # direction	int	多空方向,股票不需要；参见数据字典
#     # # offset_flag	int	交易操作,用此字段区分股票买卖,期货开、平仓,期权买卖等；参见数据字典
#     # 委托XtOrder
#     # 属性	类型	注释
#     # account_type	int	账号类型,参见数据字典
#     # account_id	str	资金账号
#     # stock_code	str	证券代码,例如"600000.SH"
#     # order_id	int	订单编号
#     # order_sysid	str	柜台合同编号
#     # order_time	int	报单时间
#     # order_type	int	委托类型,参见数据字典
#     # order_volume	int	委托数量
#     # price_type	int	报价类型,参见数据字典
#     # price	float	委托价格
#     # traded_volume	int	成交数量
#     # traded_price	float	成交均价
#     # order_status	int	委托状态,参见数据字典【决定是否撤单用这个】
#     # status_msg	str	委托状态描述,如废单原因
#     # strategy_name	str	策略名称
#     # order_remark	str	委托备注
#     # direction	int	多空方向,股票不需要；参见数据字典
#     # offset_flag	int	交易操作,用此字段区分股票买卖,期货开、平仓,期权买卖等；参见数据字典
#     if ordernum%20==0:
#     # if ordernum%2==0:
#         logger.info("交易轮次达标,执行撤单任务")
#         if cancellorder:#如果cancellorder设置为true则执行以下撤单流程【最低撤单金额一万元】
#             orderalls = trade_api.query_stock_orders(account=acc,cancelable_only=False)#仅查询可撤委托
#             for orderall in orderalls:
#                 # #模拟盘下午无法识别到撤单（orderall.status_msg无数据）把这块拿出来单独研究
#                 # logger.info(f"{orderall},{type(orderall.offset_flag)},{orderall.direction},{orderall.price_type},{orderall.order_id}")
#                 # 账号状态(account_status)
#                 # xtconstant.ORDER_UNREPORTED	48	未报
#                 # xtconstant.ORDER_WAIT_REPORTING	49	待报
#                 # xtconstant.ORDER_REPORTED	50	已报
#                 # xtconstant.ORDER_REPORTED_CANCEL	51	已报待撤
#                 # xtconstant.ORDER_PARTSUCC_CANCEL	52	部成待撤
#                 # xtconstant.ORDER_PART_CANCEL	53	部撤
#                 # xtconstant.ORDER_CANCELED	54	已撤
#                 # xtconstant.ORDER_PART_SUCC	55	部成
#                 # xtconstant.ORDER_SUCCEEDED	56	已成
#                 # xtconstant.ORDER_JUNK	57	废单【这个也得算金额】
#                 # xtconstant.ORDER_UNKNOWN	255	未知
#                 #拼接orderall的数据【不对已成（56）、待报（49）、未报（48）订单进行处理】大部分是54已撤、55部成、56已成、57废单
#                 if ((orderall.order_status!=int(56))and(orderall.order_status!=int(49))and(orderall.order_status!=int(48))):
#                     dforderall=pd.DataFrame({
#                         "order_status":[orderall.order_status],
#                         "order_id":[orderall.order_id],
#                         "status_msg":[orderall.status_msg],
#                         "symbol":[orderall.stock_code],
#                         "amount":[orderall.order_volume],
#                         "trade_amount":[orderall.traded_volume],
#                         "trade_price":[orderall.traded_price],
#                         "order_type":[orderall.order_type],#int,24卖出,23买入
#                         "direction":[orderall.direction],#int,多空方向,股票不需要；参见数据字典
#                         "offset_flag":[orderall.offset_flag],#int,交易操作,用此字段区分股票买卖,期货开、平仓,期权买卖等；参见数据字典
#                         "price":[orderall.price],
#                         "price_type":[orderall.price_type],
#                         "datetime":[datetime.datetime.fromtimestamp(orderall.order_time).strftime("%Y%m%d %H:%M:%S")],
#                         "secondary_order_id":[orderall.order_id]})
#                     dforderalls=pd.concat([dforderalls,dforderall],ignore_index=True)
#                     if ((orderall.order_status==int(55))or(orderall.order_status==int(50))):
#                         logger.info(f"******,不是已成交订单,{orderall.order_id}")
#                         #60秒内不成交就撤单【这个是要小于当前时间,否则就一直无法执行】
#                         if (datetime.datetime.fromtimestamp(orderall.order_time)+datetime.timedelta(seconds=timecancellwait))<datetime.datetime.now():#成交额还得超过targetmoney才可以最终撤单
#                             if (orderall.traded_volume*orderall.price>targetmoney):
#                                 try:
#                                     cancel_result = trade_api.cancel_order_stock(account=acc,order_id=orderall.order_id)
#                                     # .cancel_order(orderall.order_id)
#                                     logger.info(f"******,已成交金额达标执行撤单,{orderall.order_id,cancel_result}")
#                                 except:
#                                     logger.info(f"******","已完成或取消中的条件单不允许取消")
#                             elif orderall.traded_volume==0:#未成交撤单
#                                 try:#如果该委托已成交或者已撤单则会报错
#                                     cancel_result = trade_api.cancel_order_stock(account=acc,order_id=orderall.order_id)
#                                     # .cancel_order(orderall.order_id)
#                                     logger.info(f"******,执行撤单,{orderall.order_id},cancel_result,{cancel_result}")
#                                 except:
#                                     logger.info(f"******,已完成或取消中的条件单不允许取消")
#                     else:#撤单或者废单之后的金额回补
#                         # 交易操作(offset_flag)
#                         # 枚举变量名	值	含义
#                         # xtconstant.OFFSET_FLAG_OPEN	48	买入,开仓
#                         # xtconstant.OFFSET_FLAG_CLOSE	49	卖出,平仓
#                         # xtconstant.OFFSET_FLAG_FORCECLOSE	50	强平
#                         # xtconstant.OFFSET_FLAG_CLOSETODAY	51	平今
#                         # xtconstant.OFFSET_FLAG_ClOSEYESTERDAY	52	平昨
#                         # xtconstant.OFFSET_FLAG_FORCEOFF	53	强减
#                         # xtconstant.OFFSET_FLAG_LOCALFORCECLOSE	54	本地强平
#                         if (orderall.order_type==int(23)):#这里只计算BUY方向的订单,24是卖23是买
#                             # logger.info("该订单是买入")
#                             # time.sleep(10)
#                             if (orderall.order_status==int(54)):
#                                 thiscancel_amount=orderall.order_volume-orderall.traded_volume
#                                 logger.info(f"{orderall}")
#                                 logger.info(f"******,撤单成功,{orderall},{orderall.order_status},{thiscancel_amount}")
#                                 if dfordercancelled.empty:#dfordercancelled一开始是个空值,这里主要是确认一下之前有没有数据,有数据才需要检验之前是否撤销过
#                                     dfordercancelled=pd.concat([dfordercancelled,dforderall],ignore_index=True)
#                                     cancel_money=thiscancel_amount*orderall.price#然后就是计算撤销了的订单的未完成金额,加给下单金额当中
#                                     moneymanage.loc[moneymanage["代码"]==str(orderall.stock_code),"moneymanage"]+=cancel_money
#                                 else:
#                                     if orderall.order_id not in dfordercancelled["order_id"].tolist():
#                                         dfordercancelled=pd.concat([dfordercancelled,dforderall],ignore_index=True)
#                                         cancel_money=thiscancel_amount*orderall.price#然后就是计算撤销了的订单的未完成金额,加给下单金额当中
#                                         moneymanage.loc[moneymanage["代码"]==str(orderall.stock_code),"moneymanage"]+=cancel_money
#                             elif (orderall.order_status==int(57)):
#                                 logger.info(f"******,废单处理,{orderall},{orderall.order_status},{orderall.order_volume}")
#                                 if dfordercancelled.empty:#dfordercancelled一开始是个空值,这里主要是确认一下之前有没有数据,有数据才需要检验之前是否撤销过
#                                     dfordercancelled=pd.concat([dfordercancelled,dforderall],ignore_index=True)
#                                     cancel_money=orderall.order_volume*orderall.price#然后就是计算撤销了的订单的未完成金额,加给下单金额当中
#                                     moneymanage.loc[moneymanage["代码"]==str(orderall.stock_code),"moneymanage"]+=cancel_money
#                                 if orderall.order_id not in dfordercancelled["order_id"].tolist():
#                                     dfordercancelled=pd.concat([dfordercancelled,dforderall],ignore_index=True)
#                                     cancel_money=orderall.order_volume*orderall.price#然后就是计算撤销了的订单的未完成金额,加给下单金额当中
#                                     moneymanage.loc[moneymanage["代码"]==str(orderall.stock_code),"moneymanage"]+=cancel_money
#             dforderalls.to_csv(str(basepath)+"_dforderalls.csv")#输出所有未全部成交的订单【针对所有订单】
#             dfordercancelled.to_csv(str(basepath)+"_dfordercancelled.csv")#输出已经撤销或者作废的订单【只针对的买入订单】
#             logger.info("******","资金管理","premoney",premoney,"moneymanage",moneymanage)
#     moneymanage.to_csv(str(basepath)+"_dfmoneymanage.csv")
#     #重置并获取持仓信息【这里的目的是重新获取最新持仓以避免执行卖出成功后数据没有更新导致的持仓数量不对的情况】
#     dfposition=pd.DataFrame([])
#     positions=trade_api.query_stock_positions(account=acc)
#     for position in positions:
#         symbol=position.stock_code
#         logger.info(symbol,position.volume)
#         if position.volume>0:
#             dfposition=pd.concat([dfposition,pd.DataFrame({"symbol":[symbol],
#                                                             "volume":[position.volume],
#                                                             "can_use_volume":[position.can_use_volume],
#                                                             "frozen_volume":[position.frozen_volume],
#                                                             "market_value":[position.market_value],
#                                                             })],ignore_index=True)
#     logger.info(f"******,本轮持仓,{dfposition}")
#     dfposition.to_csv(str(basepath)+"_dfposition.csv")
#     logger.info(f"******,卖出")
#     if not dfposition.empty:#有持仓则验证是否卖出
#         for symbol in dfposition["symbol"].tolist():
#             if symbol in selldf["symbol"].tolist():
#                 thisposition=dfposition[dfposition["symbol"]==symbol]
#                 logger.info(f"{thisposition},{thisposition.can_use_volume.values[0]}")
#                 if (thisposition.can_use_volume.values[0]>0):#余额及可用余额都要大于0才执行卖出动作
#                     logger.info(f"******,{symbol},持仓数量,{thisposition}")
#                     try:
#                         #返回五档数据
#                         tick=xtdata.get_full_tick([symbol])
#                         tick=tick[symbol]
#                         logger.info(f"{tick}")
#                         ask_price_1=tick["askPrice"][0]
#                         ask_volume_1=tick["askVol"][0]
#                         bid_price_1=tick["bidPrice"][0]
#                         bid_volume_1=tick["bidVol"][0]
#                         ask_price_2=tick["askPrice"][1]
#                         ask_volume_2=tick["askVol"][1]
#                         bid_price_2=tick["bidPrice"][1]
#                         bid_volume_2=tick["bidVol"][1]
#                         lastPrice=tick["lastPrice"]
#                         timetag= datetime.datetime.strptime(tick["timetag"],"%Y%m%d %H:%M:%S")
#                         logger.info(f"{lastPrice},{type(lastPrice)},timetag:{timetag},{type(timetag)}")
#                         if (timetag+datetime.timedelta(seconds=timetickwait)>datetime.datetime.now()):
#                             logger.info(f"******,确认是最新tick,执行交易")
#                             if (ask_price_1-bid_price_1)<=(((ask_price_1+bid_price_1)/2)*bidrate):#盘口价差
#                                 logger.info(f"******,盘口价差适宜,适合执行交易")
#                                 if ((symbol.startswith("12")) or (symbol.startswith("11"))):#针对11开头或者12开头的转债单独处理
#                                     ask_volume_1*=10
#                                     bid_volume_1*=10
#                                     if tradeway=="maker":#maker下单【不需要考虑深度问题】
#                                         if (thisposition.can_use_volume.values[0]*ask_price_1)<(traderate*targetmoney):
#                                             logger.info("******","剩余全部卖出")
#                                             sellvolume =(math.floor(thisposition.can_use_volume.values[0]/10)*10)
#                                             sellorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                             order_type=xtconstant.STOCK_SELL,
#                                                                             order_volume=sellvolume,
#                                                                             price_type=xtconstant.FIX_PRICE,#限价
#                                                                             strategy_name=choosename,#策略名称
#                                                                             price=ask_price_1)
#                                             logger.info(f"下单成功{sellorder},{ask_price_1},{sellvolume}")
#                                         else:#限价卖出最小下单金额
#                                             logger.info(f"******,卖出目标金额")
#                                             sellvolume=(math.floor((targetmoney/ask_price_1)/10)*10)
#                                             if (thisposition.can_use_volume.values[0]*bid_price_1)>500000:#针对余额高于500000的标的单独扩大下单数量
#                                                 sellvolume*=10
#                                             logger.info(f"sellvolume{sellvolume},{sellvolume*ask_price_1}")
#                                             sellorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                             order_type=xtconstant.STOCK_SELL,
#                                                                             order_volume=sellvolume,
#                                                                             price_type=xtconstant.FIX_PRICE,#限价
#                                                                             strategy_name=choosename,#策略名称
#                                                                             price=ask_price_1)
#                                             logger.info(f"下单成功{sellorder},{ask_price_1},{sellvolume}")
#                                         time.sleep(1)
#                                     if tradeway=="taker":#maker下单【需要考虑深度问题】
#                                         if (bid_price_1*bid_volume_1)>targetmoney:#盘口深度【己方一档买入】（转债价格较高,一档深度相对小一些）                                 
#                                             if (thisposition.can_use_volume.values[0]*bid_price_1)<(traderate*targetmoney):
#                                                 logger.info(f"******,剩余全部卖出")
#                                                 sellvolume =(math.floor(thisposition.can_use_volume.values[0]/10)*10)
#                                                 sellorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                             order_type=xtconstant.STOCK_SELL,
#                                                                             order_volume=sellvolume,
#                                                                             price_type=xtconstant.FIX_PRICE,#限价
#                                                                             strategy_name=choosename,#策略名称
#                                                                             price=bid_price_1)
#                                                 logger.info(f"下单成功{sellorder},{bid_price_1},{sellvolume}")
#                                             else:#限价卖出最小下单金额
#                                                 logger.info(f"******,卖出目标金额")
#                                                 sellvolume=(math.floor((targetmoney/bid_price_1)/10)*10)
#                                                 if (thisposition.can_use_volume.values[0]*bid_price_1)>500000:#针对余额高于500000的标的单独扩大下单数量
#                                                     sellvolume*=10
#                                                 logger.info(f"sellvolume{sellvolume},{sellvolume*bid_price_1}")
#                                                 sellorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                             order_type=xtconstant.STOCK_SELL,
#                                                                             order_volume=sellvolume,
#                                                                             price_type=xtconstant.FIX_PRICE,#限价
#                                                                             strategy_name=choosename,#策略名称
#                                                                             price=bid_price_1)
#                                                 logger.info(f"下单成功{sellorder},{bid_price_1},{sellvolume}")
#                                 else:#非可转债交易方式
#                                     ask_volume_1*=100
#                                     bid_volume_1*=100
#                                     if tradeway=="maker":#maker下单【不需要考虑深度问题】
#                                         if (thisposition.can_use_volume.values[0]*ask_price_1)<(traderate*targetmoney):
#                                             logger.info(f"******,剩余全部卖出")
#                                             sellvolume =(math.floor(thisposition.can_use_volume.values[0]/100)*100)
#                                             sellorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                             order_type=xtconstant.STOCK_SELL,
#                                                                             order_volume=sellvolume,
#                                                                             price_type=xtconstant.FIX_PRICE,#限价
#                                                                             strategy_name=choosename,#策略名称
#                                                                             price=ask_price_1)
#                                             logger.info(f"下单成功{sellorder},{ask_price_1},{sellvolume}")
#                                         else:#限价卖出最小下单金额
#                                             logger.info("******","卖出目标金额")
#                                             sellvolume=(math.floor((targetmoney/ask_price_1)/100)*100)
#                                             if (thisposition.can_use_volume.values[0]*ask_price_1)>500000:#针对余额高于500000的标的单独扩大下单数量
#                                                 sellvolume*=10
#                                             logger.info(f"sellvolume{sellvolume},{sellvolume*ask_price_1}")
#                                             sellorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                             order_type=xtconstant.STOCK_SELL,
#                                                                             order_volume=sellvolume,
#                                                                             price_type=xtconstant.FIX_PRICE,#限价
#                                                                             strategy_name=choosename,#策略名称
#                                                                             price=ask_price_1)
#                                             logger.info(f"下单成功{sellorder},{ask_price_1},{sellvolume}")
#                                     if tradeway=="taker":#maker下单【需要考虑深度问题】
#                                         if (bid_price_1*bid_volume_1)>targetmoney:#盘口深度【对手盘一档买入】                                            
#                                             if (thisposition.can_use_volume.values[0]*bid_price_1)<(traderate*targetmoney):
#                                                 logger.info(f"******,剩余全部卖出")
#                                                 sellvolume =(math.floor(thisposition.can_use_volume.values[0]/100)*100)
#                                                 sellorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                             order_type=xtconstant.STOCK_SELL,
#                                                                             order_volume=sellvolume,
#                                                                             price_type=xtconstant.FIX_PRICE,#限价
#                                                                             strategy_name=choosename,#策略名称
#                                                                             price=bid_price_1)
#                                                 logger.info(f"下单成功{sellorder},{bid_price_1},{sellvolume}")
#                                             else:#限价卖出最小下单金额
#                                                 logger.info(f"******,卖出目标金额")
#                                                 sellvolume=(math.floor((targetmoney/bid_price_1)/100)*100)
#                                                 if (thisposition.can_use_volume.values[0]*bid_price_1)>500000:#针对余额高于500000的标的单独扩大下单数量
#                                                     sellvolume*=10
#                                                 logger.info(f"sellvolume{sellvolume},{sellvolume*bid_price_1}")
#                                                 sellorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                             order_type=xtconstant.STOCK_SELL,
#                                                                             order_volume=sellvolume,
#                                                                             price_type=xtconstant.FIX_PRICE,#限价
#                                                                             strategy_name=choosename,#策略名称
#                                                                             price=bid_price_1)
#                                                 logger.info(f"下单成功{sellorder},{bid_price_1},{sellvolume}")
#                     except Exception as e:#报索引越界一般是tick数据没出来
#                         logger.info("******","发生bug:",symbol,e)
#     logger.info("******","买入")
#     moneymanage=moneymanage.sort_values(by="moneymanage",ascending=False)#这里是由大到小排序,默认由小到大
#     for symbol in moneymanage["代码"].tolist():#如果恰好是三十只以上股票,且没有需要卖出的股票时,moneymanage为空会导致报错
#         buymoney=moneymanage[moneymanage["代码"]==str(symbol)]["moneymanage"].iloc[0]
#         if buymoney>targetmoney:#只针对待买入金额超过targetmoney的标的进行买入,否则直接掠过
#                 #查询资产
#                 portfolio=trade_api.query_stock_asset(account=acc)
#                 portfolio_available_cash=portfolio.cash#available_cash可用资金
#                 logger.info(f"当前余额,{portfolio_available_cash}")
#                 if portfolio_available_cash>targetmoney:
#                     logger.info(f"******,买入余额充足,{symbol},{buymoney}")
#                     try:
#                         #返回五档数据
#                         tick=xtdata.get_full_tick([symbol])
#                         tick=tick[symbol]
#                         logger.info(f"{tick}")
#                         ask_price_1=tick["askPrice"][0]
#                         ask_volume_1=tick["askVol"][0]
#                         bid_price_1=tick["bidPrice"][0]
#                         bid_volume_1=tick["bidVol"][0]
#                         ask_price_2=tick["askPrice"][1]
#                         ask_volume_2=tick["askVol"][1]
#                         bid_price_2=tick["bidPrice"][1]
#                         bid_volume_2=tick["bidVol"][1]
#                         lastPrice=tick["lastPrice"]
#                         timetag= datetime.datetime.strptime(tick["timetag"],"%Y%m%d %H:%M:%S")
#                         logger.info(f"{lastPrice},{type(lastPrice)},timetag:{timetag},{type(timetag)}")
#                         if (timetag+datetime.timedelta(seconds=timetickwait)>datetime.datetime.now()):
#                             logger.info(f"******,确认是最新tick,执行交易")
#                             if (ask_price_1-bid_price_1)<=(((ask_price_1+bid_price_1)/2)*bidrate):#盘口价差
#                                 logger.info(f"******,盘口价差适宜,适合执行交易")        
#                                 if ((symbol.startswith("12")) or (symbol.startswith("11"))):#针对11开头或者12开头的转债单独处理
#                                     ask_volume_1*=10
#                                     bid_volume_1*=10
#                                     if tradeway=="maker":#maker下单【不需要考虑深度问题】
#                                         if buymoney<(traderate*targetmoney):
#                                             logger.info(f"******,剩余全部买入")
#                                             buyvolume=(math.floor((buymoney/bid_price_1)/10)*10)
#                                             buyorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                                 order_type=xtconstant.STOCK_BUY,
#                                                                                 order_volume=buyvolume,
#                                                                                 price_type=xtconstant.FIX_PRICE,#限价
#                                                                                 strategy_name=choosename,#策略名称
#                                                                                 price=bid_price_1)
#                                             logger.info(f"下单成功{buyorder}")
#                                             bidmoney=float(bid_price_1)*buyvolume
#                                             moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
#                                         else:
#                                             logger.info(f"******,买入目标金额")
#                                             buyvolume=(math.floor((targetmoney/bid_price_1)/10)*10)
#                                             if buymoney>500000:#针对总下单余额高于500000的标的单独扩大下单数量
#                                                 buyvolume*=10
#                                             buyorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                                 order_type=xtconstant.STOCK_BUY,
#                                                                                 order_volume=buyvolume,
#                                                                                 price_type=xtconstant.FIX_PRICE,#限价
#                                                                                 strategy_name=choosename,#策略名称
#                                                                                 price=bid_price_1)
#                                             logger.info(f"下单成功{buyorder}")
#                                             bidmoney=float(bid_price_1)*buyvolume
#                                             moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
#                                         time.sleep(1)
#                                     if tradeway=="taker":#taker下单【跟其他地方一样需要考虑深度】
#                                         if (ask_price_1*ask_volume_1)>targetmoney:#盘口深度【己方一档买入】（转债价格较高,一档深度相对小一些） 
#                                             if buymoney<(traderate*targetmoney):
#                                                 logger.info(f"******,剩余全部买入")
#                                                 buyvolume=(math.floor((buymoney/ask_price_1)/10)*10)
#                                                 buyorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                                 order_type=xtconstant.STOCK_BUY,
#                                                                                 order_volume=buyvolume,
#                                                                                 price_type=xtconstant.FIX_PRICE,#限价
#                                                                                 strategy_name=choosename,#策略名称
#                                                                                 price=ask_price_1)
#                                                 logger.info(f"下单成功{buyorder}")
#                                                 bidmoney=float(ask_price_1)*buyvolume
#                                                 moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
#                                             else:
#                                                 logger.info(f"******,买入目标金额")
#                                                 buyvolume=(math.floor((targetmoney/ask_price_1)/10)*10)
#                                                 if buymoney>500000:#针对总下单余额高于500000的标的单独扩大下单数量
#                                                     buyvolume*=10
#                                                 buyorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                                 order_type=xtconstant.STOCK_BUY,
#                                                                                 order_volume=buyvolume,
#                                                                                 price_type=xtconstant.FIX_PRICE,#限价
#                                                                                 strategy_name=choosename,#策略名称
#                                                                                 price=ask_price_1)
#                                                 logger.info(f"下单成功{buyorder}")
#                                                 bidmoney=float(ask_price_1)*buyvolume
#                                                 moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
#                                 else:#其他交易情况
#                                     ask_volume_1*=100
#                                     bid_volume_1*=100
#                                     if tradeway=="maker":#maker下单【不需要考虑深度问题】
#                                         if buymoney<(traderate*targetmoney):
#                                             logger.info(f"******,剩余全部买入")
#                                             buyvolume=(math.floor((buymoney/bid_price_1)/100)*100)
#                                             buyorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                                 order_type=xtconstant.STOCK_BUY,
#                                                                                 order_volume=buyvolume,
#                                                                                 price_type=xtconstant.FIX_PRICE,#限价
#                                                                                 strategy_name=choosename,#策略名称
#                                                                                 price=bid_price_1)
#                                             logger.info(f"下单成功{buyorder}")
#                                             bidmoney=float(bid_price_1)*buyvolume
#                                             moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
#                                         else:
#                                             logger.info(f"******,买入目标金额")
#                                             buyvolume=(math.floor((targetmoney/bid_price_1)/100)*100)
#                                             if buymoney>500000:#针对总下单余额高于500000的标的单独扩大下单数量
#                                                 buyvolume*=10
#                                             buyorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                                 order_type=xtconstant.STOCK_BUY,
#                                                                                 order_volume=buyvolume,
#                                                                                 price_type=xtconstant.FIX_PRICE,#限价
#                                                                                 strategy_name=choosename,#策略名称
#                                                                                 price=bid_price_1)
#                                             logger.info(f"下单成功{buyorder}")
#                                             bidmoney=float(bid_price_1)*buyvolume
#                                             moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
#                                     if tradeway=="taker":#taker下单【跟其他地方一样需要考虑深度】
#                                         if (ask_price_1*ask_volume_1)>targetmoney:#盘口深度【对手盘一档买入】
#                                             if buymoney<(traderate*targetmoney):
#                                                 logger.info(f"******,剩余全部买入")
#                                                 buyvolume=(math.floor((buymoney/ask_price_1)/100)*100)
#                                                 buyorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                                 order_type=xtconstant.STOCK_BUY,
#                                                                                 order_volume=buyvolume,
#                                                                                 price_type=xtconstant.FIX_PRICE,#限价
#                                                                                 strategy_name=choosename,#策略名称
#                                                                                 price=ask_price_1)
#                                                 logger.info(f"下单成功{buyorder}")
#                                                 bidmoney=float(ask_price_1)*buyvolume
#                                                 moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
#                                             else:
#                                                 logger.info(f"******,买入目标金额")
#                                                 buyvolume=(math.floor((targetmoney/ask_price_1)/100)*100)
#                                                 if buymoney>500000:#针对总下单余额高于500000的标的单独扩大下单数量
#                                                     buyvolume*=10
#                                                 buyorder=trade_api.order_stock(acc, stock_code=symbol,
#                                                                                 order_type=xtconstant.STOCK_BUY,
#                                                                                 order_volume=buyvolume,
#                                                                                 price_type=xtconstant.FIX_PRICE,#限价
#                                                                                 strategy_name=choosename,#策略名称
#                                                                                 price=ask_price_1)
#                                                 logger.info(f"下单成功{buyorder}")
#                                                 bidmoney=float(ask_price_1)*buyvolume
#                                                 moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
#                     except Exception as e:#报索引越界一般是tick数据没出来
#                         logger.info(f"******,发生bug:,{symbol},{e}")
#     logger.info(f"******,任务结束")

#     # ETF申赎
#     # 申购 - xtconstant.ETF_PURCHASE
#     # 赎回 - xtconstant.ETF_REDEMPTION

#     # #返回五档数据
#     # tick=xtdata.get_full_tick([symbol])
#     # tick=tick[symbol]
#     # # logger.info(tick)
#     # ask_price_1=tick["askPrice"][0]
#     # ask_volume_1=tick["askVol"][0]
#     # ask_price_2=tick["askPrice"][1]
#     # ask_volume_2=tick["askVol"][1]

#     # #每日自动打新
#     # df=xtdata.get_ipo_info(today,today)#获取新股申购数据
#     # logger.info(df,"当日可申购新股数据")
#     # df=trade_api.query_new_purchase_limit(acc)#当前账户新股申购额度查询
#     # logger.info(df,"当前账户新股申购额度")
#     # df=xtdata.query_ipo_data()#当日新股信息查询

#     # #获取ETF实时净值（貌似得从旧QMT获取）
#     # logger.info(trade_api.get_etf_iopv("510050.SH"))    

#     # 异步下单委托反馈XtOrderResponse
#     # 属性	类型	注释
#     # account_type	int	账号类型,参见数据字典
#     # account_id	str	资金账号
#     # order_id	int	订单编号
#     # strategy_name	str	策略名称
#     # order_remark	str	委托备注
#     # seq	int	异步下单的请求序号
#     # 异步撤单委托反馈XtCancelOrderResponse
#     # 属性	类型	注释
#     # account_type	int	账号类型,参见数据字典
#     # account_id	str	资金账号
#     # order_id	int	订单编号
#     # order_sysid	str	柜台委托编号
#     # cancel_result	int	撤单结果
#     # seq	int	异步撤单的请求序号
#     # 下单失败错误XtOrderError
#     # 属性	类型	注释
#     # account_type	int	账号类型,参见数据字典
#     # account_id	str	资金账号
#     # order_id	int	订单编号
#     # error_id	int	下单失败错误码
#     # error_msg	str	下单失败具体信息
#     # strategy_name	str	策略名称
#     # order_remark	str	委托备注
#     # 撤单失败错误XtCancelError
#     # 属性	类型	注释
#     # account_type	int	账号类型,参见数据字典
#     # account_id	str	资金账号
#     # order_id	int	订单编号
#     # market	int	交易市场 0:上海 1:深圳
#     # order_sysid	str	柜台委托编号
#     # error_id	int	下单失败错误码
#     # error_msg	str	下单失败具体信息




# # 交易函数介绍（ETF套利）
# # #（1）综合交易下单 passorder()
# # 用法： passorder(opType, orderType, accountid, orderCode, prType, price, volume,[strategyName, quickTrade, userOrderId], ContextInfo)

# # 释义： 综合交易下单

# # 参数：

# # opType，操作类型，可选值：

# # 期货六键：

# # 0：开多

# # 1：平昨多

# # 2：平今多

# # 3：开空

# # 4：平昨空

# # 5：平今空

# # 期货四键：

# # 6：平多,优先平今

# # 7：平多,优先平昨

# # 8：平空,优先平今

# # 9：平空,优先平昨

# # 期货两键：

# # 10：卖出,如有多仓,优先平仓,优先平今,如有余量,再开空

# # 11：卖出,如有多仓,优先平仓,优先平昨,如有余量,再开空

# # 12：买入,如有空仓,优先平仓,优先平今,如有余量,再开多

# # 13：买入,如有空仓,优先平仓,优先平昨,如有余量,再开多

# # 14：买入,不优先平仓

# # 15：卖出,不优先平仓

# # 股票买卖：

# # 23：股票买入，或沪港通、深港通股票买入

# # 24：股票卖出，或沪港通、深港通股票卖出

# # 融资融券：

# # 27：融资买入

# # 28：融券卖出

# # 29：买券还券

# # 30：直接还券

# # 31：卖券还款

# # 32：直接还款

# # 33：信用账号股票买入

# # 34：信用账号股票卖出

# # 组合交易：

# # 25：组合买入，或沪港通、深港通的组合买入

# # 26：组合卖出，或沪港通、深港通的组合卖出

# # 27：融资买入

# # 28：融券卖出

# # 29：买券还券

# # 31：卖券还款

# # 33：信用账号股票买入

# # 34：信用账号股票卖出

# # 35：普通账号一键买卖

# # 36：信用账号一键买卖

# # 40：期货组合开多

# # 43：期货组合开空

# # 46：期货组合平多,优先平今

# # 47：期货组合平多,优先平昨

# # 48：期货组合平空,优先平今

# # 49：期货组合平空,优先平昨

# # 期权交易：

# # 50：买入开仓

# # 51：卖出平仓

# # 52：卖出开仓

# # 53：买入平仓

# # 54：备兑开仓

# # 55：备兑平仓

# # 56：认购行权

# # 57：认沽行权

# # 58：证券锁定

# # 59：证券解锁

# # ETF交易：

# # 60：申购

# # 61：赎回

# # 专项两融：

# # 70：专项融资买入

# # 71：专项融券卖出

# # 72：专项买券还券

# # 73：专项直接还券

# # 74：专项卖券还款

# # 75：专项直接还款

# # 可转债：

# # 80：普通账户转股

# # 81：普通账户回售

# # 82：信用账户转股

# # 83：信用账户回售

# # orderType，下单方式

# # 注意

# # 一、期货不支持 1102 和 1202

# # 二、对所有账号组的操作相当于对账号组里的每个账号做一样的操作，如 passorder(23, 1202, 'testS', '000001.SZ', 5, -1, 50000, ContextInfo)，意思就是对账号组 testS 里的所有账号都以最新价开仓买入 50000 元市值的 000001.SZ 平安银行；passorder(60,1101,"test",'510050.SH',5,-1,1,ContextInfo)意思就是账号test申购1个单位(900000股)的华夏上证50ETF(只申购不买入成分股)。

# # 可选值：

# # 1101：单股、单账号、普通、股/手方式下单

# # 1102：单股、单账号、普通、金额（元）方式下单（只支持股票）

# # 1113：单股、单账号、总资产、比例 [0 ~ 1] 方式下单

# # 1123：单股、单账号、可用、比例[0 ~ 1]方式下单

# # 1201：单股、账号组（无权重）、普通、股/手方式下单

# # 1202：单股、账号组（无权重）、普通、金额（元）方式下单（只支持股票）

# # 1213：单股、账号组（无权重）、总资产、比例 [0 ~ 1] 方式下单

# # 1223：单股、账号组（无权重）、可用、比例 [0 ~ 1] 方式下单

# # 2101：组合、单账号、普通、按组合股票数量（篮子中股票设定的数量）方式下单 > 对应 volume 的单位为篮子的份

# # 2102：组合、单账号、普通、按组合股票权重（篮子中股票设定的权重）方式下单 > 对应 volume 的单位为元

# # 2103：组合、单账号、普通、按账号可用方式下单 > （底层篮子股票怎么分配？答：按可用资金比例后按篮子中股票权重分配，如用户没填权重则按相等权重分配）只对股票篮子支持

# # 2201：组合、账号组（无权重）、普通、按组合股票数量方式下单

# # 2202：组合、账号组（无权重）、普通、按组合股票权重方式下单

# # 2203：组合、账号组（无权重）、普通、按账号可用方式下单只对股票篮子支持

# # 组合套利交易接口特殊设置（accountID、orderType 特殊设置）

# # passorder(opType, orderType, accountID, orderCode, prType, hedgeRatio, volume, ContextInfo)

# # accountID = 'stockAccountID, futureAccountID'

# # orderCode = 'basketName, futureName'

# # hedgeRatio：套利比例（0 ~ 2 之间值，相当于 %0 至 200% 套利）

# # volume：份数 \ 资金 \ 比例

# # orderType（特殊设置）

# # orderType 可选值：

# # 2331：组合、套利、合约价值自动套利、按组合股票数量方式下单

# # 2332：组合、套利、按合约价值自动套利、按组合股票权重方式下单

# # 2333：组合、套利、按合约价值自动套利、按账号可用方式下单

# # accountID，资金账号

# # passorder(opType, orderType, accountID, orderCode, prType, price, volume, ContextInfo)

# # 提示

# # 下单的账号ID（可多个）或账号组名或套利组名（一个篮子一个套利账号，如 accountID = '股票账户名, 期货账号'）

# # orderCode，下单代码

# # passorder(opType, orderType, accountID, orderCode, prType, price, volume, ContextInfo)

# # 提示

# # 一、如果是单股或单期货、港股，则该参数填合约代码；

# # 二、如果是组合交易,则该参数填篮子名称；

# # 三、如果是组合套利，则填一个篮子名和一个期货合约名（如orderCode = '篮子名, 期货合约名'）

# # prType，下单选价类型

# # passorder(opType, orderType, accountID, orderCode, prType, price, volume, ContextInfo)

# # 可选值（特别的对于套利，这个 prType 只对篮子起作用，期货的采用默认的方式）：

# # -1：无效（实际下单时,需要用交易面板交易函数那设定的选价类型）

# # 0：卖5价

# # 1：卖4价

# # 2：卖3价

# # 3：卖2价

# # 4：卖1价

# # 5：最新价

# # 6：买1价

# # 7：买2价（组合不支持）

# # 8：买3价（组合不支持）

# # 9：买4价（组合不支持）

# # 10：买5价（组合不支持）

# # 11：（指定价）模型价（只对单股情况支持,对组合交易不支持）

# # 12：涨跌停价 （自动判断，买入时使用涨停价，卖出时使用跌停价）

# # 13：己方盘口一档价，即买入时用盘口买一价下单，卖出时用卖一价下单，

# # 14：对手价（对方盘口一档价）

# # 27：市价即成剩撤(仅对股票期权申报有效)

# # 28：市价即全成否则撤(仅对股票期权申报有效)

# # 29：市价剩转限价(仅对股票期权申报有效)

# # 42：最优五档即时成交剩余撤销申报(仅对上交所申报有效)

# # 43：最优五档即时成交剩转限价申报(仅对上交所申报有效)

# # 44：对手方最优价格委托(上交所股票、深交所股票和深交所期权有效)

# # 45：本方最优价格委托(上交所股票、深交所股票和深交所期权有效)

# # 46：即时成交剩余撤销委托(仅对深交所申报有效)

# # 47：最优五档即时成交剩余撤销委托(仅对深交所申报有效)

# # 48：全额成交或撤销委托(仅对深交所申报有效)

# # 49：科创板盘后定价

# # price，下单价格

# # passorder(opType, orderType, accountID, orderCode, prType, price, volume, ContextInfo)

# # 提示

# # 一、单股下单时，prType 是模型价/科创板盘后定价时 price 有效；其它情况无效；即单股时， prType 参数为 11，49 时被使用。 prType 参数不为 11，49 时也需填写，填写的内容可为 -1，0，2，100 等任意数字；

# # 二、组合下单时，是组合套利时，price 作套利比例有效，其它情况无效。

# # volume，下单数量（股 / 手 / 元 / %）

# # passorder(opType, orderType, accountID, orderCode, prType, price, volume, ContextInfo)

# # 根据 orderType 值最后一位确定 volume 的单位：

# # 单股下单时：

# # 1：股 / 手 （股票:股， 股票期权:张， 期货:手， 可转债:张， 基金：份）

# # 2：金额（元）

# # 3：比例（%）

# # 组合下单时：

# # 1：按组合股票数量（份）

# # 2：按组合股票权重（元）

# # 3：按账号可用（%）

# # strategyName，string，自定义策略名，可缺省不写，用来区分 order 委托和 deal 成交来自不同的策略。根据该策略名，get_trade_detail_data，get_last_order_id 函数可以获取相应策略名对应的委托或持仓结果。

# # 提示

# # strategyName 只对同账号本地客户端有效，即 strategyName 只对当前客户端下的单进行策略区分，且该策略区分只能当前客户端使用。

# # quickTrade，int，设定是否立即触发下单，可选值：

# # 0：否

# # 1：是

# # 2：是

# # 提示

# # passorder是对最后一根K线完全走完后生成的模型信号在下一根K线的第一个tick数据来时触发下单交易；采用quickTrade参数设置为1时，非历史bar上执行时（ContextInfo.is_last_bar()为True），只要策略模型中调用到就触发下单交易。quickTrade参数设置为2时，不判断bar状态，只要策略模型中调用到就触发下单交易，历史bar上也能触发下单，请谨慎使用。

# # userOrderId，string，用户自设委托 ID，可缺省不写，写的时候必须把起前面的 strategyName 和 quickTrade 参数也填写。对应 order 委托对象和 deal 成交对象中的 m_strRemark 属性，通过 get_trade_detail_data 函数或委托主推函数 order_callback 和成交主推函数 deal_callback 可拿到这两个对象信息。

# # 返回： 无

# # 示例：

# # def handlebar(ContextInfo):
# #     # 单股单账号期货最新价买入 10 手
# #     passorder(0, 1101, 'test', target, 5, -1, 10, ContextInfo)
    
# #     # 单股单账号期货指定价买入 10 手
# #     passorder(0, 1101, 'test', target, 11, 3000, 10, ContextInfo)
    
# #     # 单股单账号股票最新价买入 100 股（1 手）   
# #     passorder(23, 1101, 'test', target, 5, 0, 100, ContextInfo)
    
# #     # 单股单账号股票指定价买入 100 股（1 手）  
# #     passorder(23, 1101, 'test', target, 11, 7, 100, ContextInfo)

# #     # 申购 中证500指数ETF  
# #     passorder(60, 1101, 'test', '510030.SH', 5, 0, 1, 2, ContextInfo)  
    
# #     # 赎回 中证500指数ETF
# #     passorder(61, 1101, 'test', '510030.SH', 5, 0, 1, 2, ContextInfo)  