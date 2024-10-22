#【同花顺APP上有申赎清单信息】

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
