#申请的时候用一套全新的手机号和邮箱还有姓名地址就行
#pip install jqdatasdk

import datetime
import time
import akshare as ak
import requests
import pandas as pd
import math
from jqdatasdk import *
askapi=auth('15803281949','wthWTH00') #账号是申请时所填写的手机号；密码为聚宽官网登录密码
print(askapi)
def symbol_convert(x):  # 股票代码加后缀
    if x.startswith("6"):
        return str(str(x)+".XSHG")
    elif x.startswith("00"):
        return str(str(x)+".XSHE")
    elif x.startswith("30"):
        return str(str(x)+".XSHE")
    else:
        pass
def filter_kcb_stock(stocks): #过滤科创北交股票
    for stock in stocks[:]:
        if stock[0] == "4" or stock[0] == "8" or stock[:2] == "68":
        # if stock[0] == "4" or stock[0] == "8" or stock[:2] == "68" or stock[:2] == "30":
            stocks.remove(stock)
    return stocks

now = datetime.datetime.now()
start_date = now.strftime("%Y-%m-%d")  # 测试当天的数据
# start_date = (now - datetime.timedelta(days=300)).strftime("%Y-%m-%d")  # 测试昨天的数据
today = get_trade_days(start_date=None, end_date=start_date, count=2)[1]
yesterday = get_trade_days(start_date=None, end_date=start_date, count=2)[0]
print(today,yesterday)

# 行业数据获取(聚宽)
try:
    pd.read_csv("【行业】聚宽一级行业对照表"+str(start_date)+".csv")
    print("******","【行业】聚宽一级行业对照表"+str(start_date)+".csv"+ "文件存在")
except Exception as e:
    print("******","******" +"【行业】聚宽一级行业对照表"+str(start_date)+".csv"+ "文件不同时存在")
    yesterday=today-datetime.timedelta(days=1)
    yesterday=yesterday.strftime("%Y%m%d") # 回测前一天
    stockslist=get_industries(name="jq_l1",date=today).index.tolist() # 聚宽一级行业数据(一创聚宽)
    print(stockslist)
    bkdf=pd.DataFrame()
    for stock in stockslist: # 获取行业类成分股
        stocks=get_industry_stocks(stock,date=today) # 行业成分股
#         stocks = filter_kcb_stock(stocks) # 去除科创北交
        df=pd.DataFrame({"代码":stocks})
        df["板块"]=stock
        bkdf=pd.concat([bkdf,df],axis=0,sort=False)
    bkdf=bkdf.reset_index()
    print("len(bkdf)",bkdf)
    bkdf.to_csv("【行业】聚宽一级行业对照表"+str(start_date)+".csv")



# 行业数据获取(聚宽)
try:
    pd.read_csv("聚宽（中小板）买入"+str(start_date)+".csv")
    print("******","聚宽（中小板）买入"+str(start_date)+".csv"+ "文件存在")
    pd.read_csv("聚宽（中小板）卖出"+str(start_date)+".csv")
    print("******","聚宽（中小板）卖出"+str(start_date)+".csv"+ "文件存在")
except Exception as e:
    print("******","******" +"聚宽（中小板）买入"+str(start_date)+".csv"+"聚宽（中小板）卖出"+str(start_date)+".csv"+ "文件不同时存在")
    stocks = get_index_stocks("399101.XSHE",date=today) # 中小综指【1000】
    stocks = filter_kcb_stock(stocks) # 去除科创北交
    stdf=get_extras('is_st',stocks,end_date=today,df=True,count=1).T # 去除ST
    stdf=stdf[stdf[str(today)]==False]
    stocks=stdf.index.values
    stocks=[stock for stock in stocks]
    print(stdf,stocks,len(stocks))
    df=get_price(stocks,frequency="1d",count=1,end_date=today,fields=["open","close","high_limit","low_limit","paused"])
    df=df.reset_index()
    df=df[df["paused"]==0]#1是停牌0是正常
    df=df[df["open"]>4]
    df=df.rename(columns={"code": "代码"})
    bkdf=df
    print(df)
    oldstocks=bkdf["代码"].tolist()
    # 基本面数据
    olddf=get_fundamentals(query(valuation,indicator,balance,income).filter(valuation.code.in_(oldstocks)),date=yesterday)
    olddf=olddf.rename(columns={
        "code":"代码",
        "np_parent_company_owners":"归母净利润",
        "total_operating_revenue":"营业总收入",
        # "market_cap":"总市值",
        "capitalization":"总股本", # 拿前日总股本乘以当日开盘价更加贴合实际总市值
    })
    olddf = bkdf.merge(olddf, on="代码", how="inner")
    olddf["总市值"]=olddf["总股本"]*olddf["open"]*1e4
    olddf=olddf[olddf["归母净利润"]>0]
    # olddf=olddf[olddf["营业总收入"]>100000000]
    olddf=olddf[["代码","总股本","总市值","归母净利润"]]
    numbuystock=5
    olddf["代码"] = olddf["代码"].str.replace("\D","",regex=True).astype(str)
    dftwo=olddf.nsmallest(math.ceil(1.5*numbuystock),"总市值")
    dfone=olddf.nsmallest(math.ceil(numbuystock),"总市值")
    dfone["代码"]=dfone["代码"].apply(lambda x: symbol_convert(x)).astype(str) # 需要指定类型为字符串
    dftwo["代码"]=dftwo["代码"].apply(lambda x: symbol_convert(x)).astype(str) # 需要指定类型为字符串
    dfone.to_csv("聚宽（中小板）买入"+str(start_date)+".csv")
    dftwo.to_csv("聚宽（中小板）卖出"+str(start_date)+".csv")
    buylistone=dfone["代码"].values
    buylisttwo=dftwo["代码"].values
    print("dfone",dfone,"dftwo",dftwo)
