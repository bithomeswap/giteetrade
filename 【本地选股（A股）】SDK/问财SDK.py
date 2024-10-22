#【据说湘财证券在研发相关的ETF套利模块，未来会给普通用户使用，自己从头去写成本过高了】
import pandas as pd
import datetime
import time
now=datetime.datetime.now()
startday=now.strftime("%Y%m%d")
# lastday=(now-datetime.timedelta(days=365)).strftime("%Y%m%d")
lastday=(now-datetime.timedelta(days=60)).strftime("%Y%m%d")

# pip install xcsc-tushare
import xcsc_tushare as ts
# ts.set_token('7ed61c98882a320cadce6481aef04ebf7853807179d45ee7f72089d7')
# ts.pro_api(server='http://116.128.206.39:7172')   #指定tocken对应的环境变量，此处以生产为例
pro = ts.pro_api('7ed61c98882a320cadce6481aef04ebf7853807179d45ee7f72089d7',server='http://116.128.206.39:7172')
tradedaydf = pro.query('trade_cal',
                exchange='SSE',#交易所 SZN-深股通,SHN-沪股通,SSE-上海证券交易所,SZSE-深圳证券交易所
                start_date=lastday,
                end_date=startday)
tradedaydf['trade_date'] = pd.to_datetime(tradedaydf['trade_date'], format='%Y%m%d')
tradedaydf['trade_date'] = tradedaydf['trade_date'].dt.strftime('%Y-%m-%d')
print(tradedaydf)
tradedays=tradedaydf["trade_date"].tolist()



# node -v
# #需要提前安装node.js抓网页数据，如果没node.js会报错
# pip install pywencai -U#python3.7版本调用这个函数就报错：module 'pywencai' has no attribute 'get'
import pywencai

word=f'{tradedays[-2]},所有ETF,申赎额度,申赎状态,成分股比例'#申赎状态-基金@申购赎回状态[20240904]要求是开放申购|开放赎回
df=pywencai.get(question=word,#query参数
                    loop=True,
                    query_type="fund",
                    # pro=True, #付费版才使用
                    # cookie='xxxx',
                   )
# print(len(df))
print(df)
df.to_csv("ETF全部信息.csv")

word=f'{tradedays[-2]}所有ETF价格及净值'
df=pywencai.get(question=word,#query参数
                    loop=True,
                    query_type="fund",
                    # pro=True, #付费版才使用
                    # cookie='xxxx',
                   )
# print(len(df))
df["昨日成交额"]=df[f"基金@成交额[{tradedays[-2].replace('-','')}]"].astype(float)
df=df.sort_values(by="昨日成交额",ascending=False)#溢价率降序排列
df=df[df["昨日成交额"]>10000000]#卡在一个亿的金额直接去掉了一半多
symbols=df["基金代码"].tolist()
# print(len(df))
print(df)
df.to_csv("ETF昨日成交额.csv")

# ETF净值数据【当天】
word=f'{startday}所有ETF价格及净值'
df=pywencai.get(question=word,#query参数
                    loop=True,
                    query_type="fund",
                    # pro=True, #付费版才使用
                    # cookie='xxxx',
                   )
# print(len(df))
df["ETF溢价率"]=df[f"基金@收盘价[{startday}]"].astype(float)/df["基金@最新单位净值"].astype(float)-1
df=df.sort_values(by="ETF溢价率",ascending=False)#溢价率降序排列
df=df[df["基金代码"].isin(symbols)]
# print(len(df))
print(df)
df.to_csv("ETF实时净值.csv")


# #使用问财的python库获取数据【同花顺的利润口径不同，同花顺是另一种归母净利润，这里是ttm的归母净利润】
# # targets=["股性数据","人气股","竞价数据","竞价数据"]
# targets=["人气股","竞价数据","竞价数据"]
# for target in targets:
#     alldf=pd.DataFrame({})
#     for tradeday in tradedays:
#         try:
#             time.sleep(1)
#             if target=="股性数据":
#                 word=f"{tradeday}股性极佳的个股"
#                 df = pywencai.get(question=word, 
#                                                 domain='股票',
#                                                 # timeout=6,
#                                                 # df=False
#                                                 )
#                 # print("股性数据:",df)
#                 df["日期"]=tradeday
#                 thisday=pd.to_datetime(tradeday, format='%Y-%m-%d').strftime('%Y%m%d')
#                 # print(thisday)
#                 cols=[col for col in df.columns if thisday in col]
#                 # print(columns)
#                 for col in cols:
#                     newcol=col.replace('[', '').replace(']', '').replace(thisday, '')
#                     print(col,newcol)
#                     df=df.rename(columns={col:newcol})
#                 alldf=pd.concat([alldf,df])
#             if target=="人气股":
#                 word = f"{tradeday}人气榜排行前200名"
#                 df = pywencai.get(question=word, 
#                                 domain='股票',
#                                 # timeout=6,
#                                 # df=False
#                                 )
#                 # print("人气数据:",df)
#                 df["日期"]=tradeday
#                 thisday=pd.to_datetime(tradeday, format='%Y-%m-%d').strftime('%Y%m%d')
#                 # print(thisday)
#                 cols=[col for col in df.columns if thisday in col]
#                 # print(columns)
#                 for col in cols:
#                     newcol=col.replace('[', '').replace(']', '').replace(thisday, '')
#                     print(col,newcol)
#                     df=df.rename(columns={col:newcol})
#                 alldf=pd.concat([alldf,df])
#             if target=="竞价数据":#有的日期数据少，需要单独处理
#                 word = f"{tradeday},所有股票,竞价金额,竞价涨幅,竞价量,竞价未匹配量"
#                 df = pywencai.get(question=word, 
#                                                 domain='股票',
#                                                 # timeout=6,
#                                                 # df=False
#                                                 )
#                 # print("竞价数据:",df)
#                 df["日期"]=tradeday
#                 thisday=pd.to_datetime(tradeday, format='%Y-%m-%d').strftime('%Y%m%d')
#                 # print(thisday)
#                 cols=[col for col in df.columns if thisday in col]
#                 # print(columns)
#                 for col in cols:
#                     newcol=col.replace('[', '').replace(']', '').replace(thisday, '')
#                     print(col,newcol)
#                     df=df.rename(columns={col:newcol})
#                 alldf=pd.concat([alldf,df])
#             if target=="ETF净值":
#                 word=f'{tradeday}所有ETF价格及净值'
#                 df=pywencai.get(question=word,#query参数
#                                     loop=True,
#                                     query_type="fund",
#                                     # pro=True, #付费版才使用
#                                     # cookie='xxxx',
#                                 )
#                 # print("ETF净值数据:",df)
#                 df["日期"]=tradeday
#                 thisday=pd.to_datetime(tradeday, format='%Y-%m-%d').strftime('%Y%m%d')
#                 # print(thisday)
#                 cols=[col for col in df.columns if thisday in col]
#                 # print(columns)
#                 for col in cols:
#                     newcol=col.replace('[', '').replace(']', '').replace(thisday, '')
#                     print(col,newcol)
#                     df=df.rename(columns={col:newcol})
#                 alldf=pd.concat([alldf,df])
#         except Exception as e:
#             print(e)
#     alldf.to_csv(f"{target}.csv")


# # ETF净值数据【历史】
# word=f'2023-08-06所有ETF价格及净值'
# df=pywencai.get(question=word,#query参数
#                     loop=True,
#                     query_type="fund",
#                     # pro=True, #付费版才使用
#                     # cookie='xxxx',
#                    )
# print(df)
# df.to_csv("ETF实时净值.csv")

# # 通过问财可以获得集合竞价未匹配量【历史】100只
# # current_date_str="20230806"
# # current_date_str="2023-08-06"# 【日期参赛用-链接后可以取到历史数据】
# current_date_str="2024-08-08"# 【日期参赛用-链接后可以取到历史数据】
# stock_code="000001.SZ"
# # word = f"{current_date_str},{stock_code},竞价金额,竞价涨幅,竞价量,竞价未匹配量"
# word = f"{current_date_str},所有股票,竞价金额,竞价涨幅,竞价量,竞价未匹配量"
# df = pywencai.get(question=word, 
#                                 domain='股票',
#                                 # timeout=6,
#                                 # df=False
#                                 )
# print("竞价数据:",df)
# df.to_csv("df.csv")

# # 人气股【历史】100只
# # word = f"2023-06-05人气榜排行前200名"
# word = f"2024-08-08人气榜排行前200名"
# df = pywencai.get(question=word, 
#                 domain='股票',
#                 # timeout=6,
#                 # df=False
#                 )
# print("人气数据:",df)
# df.to_csv("df.csv")

# # 游资数据【历史】
# # word="2023-08-08龙虎榜"
# word="2023-06-05游资营业部连续3天买入"
# df = pywencai.get(question=word, 
#                                 domain='股票',
#                                 # timeout=6,
#                                 # df=False
#                                 )
# print("游资数据:",df)
# df.to_csv("df.csv")

# # 股性数据【历史】数据全用不同方式能拿到，但是接口一次只能返回100
# word="2023-06-05股性评分排名最好的200只个股"
# # word="2023-06-05股性评分排名最差的200只个股"
# df = pywencai.get(question=word, 
#                                 domain='股票',
#                                 # timeout=6,
#                                 # df=False
#                                 )
# print("股性数据:",df)
# df.to_csv("df.csv")

# # 机构目标价数据【最近】
# word="距离机构目标价还有翻倍空间的股票"
# df = pywencai.get(question=word, 
#                                 domain='股票',
#                                 # timeout=6,
#                                 # df=False
#                                 )
# print("机构目标价数据:",df)

# #小市值数据【最近】
# print("问财下载财务数据")
# import datetime
# strday=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y%m%d")
# print("strday",strday)
# # word=f'主板创业板股票昨日的总股本及净利润'
# word=f'中小综指成分股票昨天的总股本及净利润，取其中总市值最小的三十只'
# olddf=pywencai.get(question=word,
#                     loop=True,
#                     query_type="stock",
#                     # pro=True, #付费版才使用
#                     # cookie='xxxx',
#                    )
#                     取值	含义
#                     stock	股票
#                     zhishu	指数
#                     fund	基金
#                     hkstock	港股
#                     usstock	美股
#                     threeboard	新三板
#                     conbond	可转债
#                     insurance	保险
#                     futures	期货
#                     lccp	理财
#                     foreign_exchange	外汇
# print(olddf)
# olddf=olddf[~(olddf[f"股票简称"].str.contains("S"))]
# olddf=olddf[~(olddf[f"股票简称"].str.contains("退"))]
# guben=[column for column in olddf.columns if f"总股本[" in column]
# olddf["总股本"]=olddf[guben]
# lirun=[column for column in olddf.columns if f"归属母公司股东的净利润(ttm)[" in column]
# olddf["归母净利润"]=olddf[lirun]
# # olddf["总股本"]=olddf[f"总股本[{strday}]"]
# # olddf["归母净利润"]=olddf[f"归属母公司股东的净利润(ttm)[{strday}]"]
# # olddf=olddf[["最新价","股票简称","股票代码","总股本","归母净利润"]]
# olddf=olddf.dropna(subset=['最新价'])#去掉未上市的标的【当然停牌数据也被去掉了】
# olddf=olddf[olddf["归母净利润"]>0]
# olddf["代码"]=olddf["股票代码"]
# print(olddf)
# olddf.to_csv("中小综指.csv")