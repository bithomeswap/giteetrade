import datetime
import time
import akshare as ak
import requests
import pandas as pd
import math
from supermind.api import *
from supermind.data.main import command
from supermind.mod.mindgo.utils.recorder import log
from supermind.mod.mindgo.research import (
    bonus,
    valuation,
    balance,
    cashflow,
    income,
    profit_report,
    profit_forecast,
    operating,
    debtrepay,
    profit,
    growth,
    cashflow_sq,
    income_sq,
    profit_sq,
    growth_sq,
    asharevalue,
    ashareoperate,
    asharedebt,
    ashareprofit,
)
from supermind.mod.mindgo.research.research_api import (
    pd_Panel,
    normalize_symbol,
    get_security_info,
    get_price,
    get_candle_stick,
    get_all_trade_days,
    get_trade_days,
    get_last_trade_day,
    query,
    run_query,
    get_fundamentals,
    read_file,
    write_file,
    remove_file,
    superreload,
    notify_push,
    set_log_level,
    get_api_usage,
    upload_file,
    download_file,
)
from supermind.mod.stock.research_api import (
    get_price_future,
    get_candle_stick_future,
    get_futures_dominate,
    get_futures_info,
    get_future_code,
    get_all_securities,
    get_dividend_information,
    get_option_code,
    get_tick,
)
from supermind.mod.analyser.research_api import research_strategy
from supermind.mod.realtime.research_api import research_trade
from supermind.mod.tradeapi.api import (
    TradeAPI,
    TradeCredit,
    TradeFutures,
)
from wxpusher import WxPusher
import subprocess
### 这个只能是3.10的虚拟python环境才有效，不能在基础环境安装 ###
# 创建3.10的环境
# conda deactivate # 退出当前环境
# conda remove -n my_env --all # 删除没用的版本【base是根目录不可以删除】
# conda remove -n env3.8 --all # 删除没用的版本【base是根目录不可以删除】
# conda create -n env3.10 python=3.10 # 安装目标版本
# conda activate base # 激活目标版本

# 按照及更新supermind库【安装之前应该先安装Cpython库以免报错】
# pip install supermind # 安装
# pip install --upgrade supermind # 更新

# # subprocess.call("supermind data setpath -d C:/Users/13480/Desktop/----SDK-huaxin/【本地选股】同花顺SDK",shell=True) # 本地
# subprocess.call("supermind data setpath -d /root/test/quant/【本地选股】同花顺SDK",shell=True) # 设置数据存储路径
# subprocess.call("supermind login -u 19511189162 -p wthWTH00",shell=True)# 填写账号密码【就第一次用的时候需要】
# # python -m supermind data ingest -b daily # 加载日k数据

# # 执行环境
# pandas~=1.3.5
# numpy~=1.21.1
# mgquant>=3.0.9
# pyarrow==8.0.0
# requests~=2.28.1
# msgpack~=1.0.4
# pyyaml~=5.4.1
# cachetools~=5.2.0
# cython~=0.29.32
# xarray~=2022.10.0
# tqdm~=4.64.1
# protobuf~=3.11
# pycryptodome~=3.9
# python-snappy~=0.6

# 发布到微信机器人
def postmessage(text):
    # # 查询用户
    # # query_user=WxPusher.query_user("<page>","<page_size>","<appToken>")
    # for pagenum in range(1,5):
    #     uidslist=[]
    #     query_user=WxPusher.query_user(str(pagenum),"50","AT_tFRZgjToc6XnG5dzR2MGyv1DzECNYOIU")
    #     # print(query_user["data"]["records"])
    #     if len(query_user["data"]["records"])>0:
    #         for query in query_user["data"]["records"]:
    #             print(query["uid"])
    #             uidslist.append(query["uid"])
    #             # UID_4HGW0dvl7EA7zaZLYe8bjegTSZFS # 姨父畅海东UID
    # # 发送消息
    # # WxPusher.send_message('<content>',
    # #                       uids=['<uids>'],
    # #                       topic_ids=['<topic_ids>'],
    # #                       token='<appToken>')      
    message=WxPusher.send_message(
        "【风险提示】本消息仅作为策略演示及研究使用，严禁任何个人或组织以此作为投资依据，因为使用或者传播本订阅信息而产生的任何风险由使用者自行承担。\n"+
        "【策略说明】状态列为初始建仓说明标的低估适合建仓，如果某持仓股票不在状态列为持仓观察的标的当中，说明风险加大不宜继续持有。\n"+
        str(text),
        uids=["UID_qkmjMTBknX0I5ZZoVY3IBFv7WVV1"],
        # uids=uidslist,
        topic_ids=["12417"],
        token="AT_tFRZgjToc6XnG5dzR2MGyv1DzECNYOIU",
    )
    messageId=message["data"][0]["messageId"]
    print(message,messageId)


def symbol_convert(x):#股票代码加后缀
    if x.startswith("6"):#主板（上交所）
        return str(str(x)+".SH")
    elif x.startswith("00"):#主板（深交所）
        return str(str(x)+".SZ")
    elif x.startswith("30"):#创业板（深交所）
        return str(str(x)+".SZ")
    elif x.startswith("11"):#可转债（上交所）
        return str(str(x)+".SH")
    elif x.startswith("12"):#可转债（深交所）
        return str(str(x)+".SZ")
    elif x.startswith("51"):#ETF（上交所）
        return str(str(x)+".SH")
    elif x.startswith("15"):#ETF（深交所）
        return str(str(x)+".SZ")
    else:
        print("不在后缀转换名录",str(x))
        return str(str(x))
def filter_kcb_stock(stocks):#过滤科创北交股票
    for stock in stocks[:]:
        if stock[0]=="4" or stock[0]=="8" or stock[:2]=="68":
            stocks.remove(stock)
    return stocks

now=datetime.datetime.now()
start_date=now.strftime("%Y-%m-%d")#测试当天的数据
last_date=(now-datetime.timedelta(days=250)).strftime("%Y-%m-%d")
#allstocks=get_all_securities("stock",start_date)
#allstocks=allstocks[allstocks["start_date"]<last_date].index.values
#print("******非次新股【已经去除次新股】",allstocks,len(allstocks))#过滤次新股
today=get_trade_days(end_date=start_date,count=2).values[1]
today=np.datetime_as_string(today,unit="D").replace("-","")
yesterday=get_trade_days(end_date=start_date,count=2).values[0]
yesterday=np.datetime_as_string(yesterday,unit="D").replace("-","")
print("******",today,yesterday)

print("启动",get_api_usage())  # 查询流量使用情况
newdf=ak.stock_zh_a_spot_em()
newdf=newdf[["今开","代码","名称"]]
newdf=newdf[~newdf["名称"].str.contains("ST")]  # 过滤掉ST股票
newdf=newdf[~newdf["名称"].str.contains("退")]  # 过滤掉退市股票
newdflist=filter_kcb_stock(newdf["代码"].tolist())
newdf=newdf[newdf["代码"].isin(newdflist)]
newdf.rename(columns={"今开":"open"},inplace=True)
newdf=newdf[newdf["open"]>4]
newdf["代码"]=newdf["代码"].apply(lambda x: str(x))
# newdf.to_csv("东方财富.csv")
# newdf=pd.read_csv("东方财富.csv")
print("东方财富",newdf)

def choose_stocks(choosename,start_date,last_date,today,yesterday):
    if (choosename=="龙头股（同花顺）") or (choosename=="龙头股（聚宽）"):
        if choosename=="龙头股（同花顺）":
            filename=f"【行业】同花顺一级行业对照表.csv"
        if choosename=="龙头股（聚宽）":
            filename=f"【行业】聚宽一级行业对照表.csv"   
        try:
            pd.read_csv(str(start_date)+choosename+"买入.csv")
            print("******",str(start_date)+choosename+"买入.csv"+"文件存在")
            pd.read_csv(str(start_date)+choosename+"卖出.csv")
            print("******",str(start_date)+choosename+"卖出.csv"+"文件存在")
        except Exception as e:
            print("******","******"+str(start_date)+choosename+"买入.csv"+choosename+"卖出.csv"+"文件不同时存在")
            # 获取基本面数据
            olddf=get_fundamentals(
                query(
                    asharevalue.symbol,
                    income.overall_income,
                    income.np_atsopc,
                    asharevalue.ashare_total_shares,
                    asharevalue.total_shares,
                ),
                date=yesterday,
            )
            olddf=olddf.rename(columns={
                        "asharevalue_symbol":"代码",
                        "income_overall_income":"营业总收入",
                        # income.overall_income[营业总收入],income.operating_income[营业收入]
                        "income_np_atsopc":"归母净利润",
                        # "asharevalue_total_mv_object": "总市值",# 纯A股总市值，比总市值A+B+H要好，但还是不如用总股本计算当日市值好
                        # "asharevalue_total_mv": "总市值",# 总市值A+B+H
                        "asharevalue_total_shares": "总股本",# 包括新股发行前的股份和新发行的股份的数量的总和(同花顺计算)
                        # "asharevalue_ashare_total_shares": "总股本",# 上市公司发行的人民币普通股合计股数(同花顺计算)
                    })
            olddf=olddf[olddf["营业总收入"]>100000000]
            olddf=olddf[olddf["归母净利润"]>0]
            print(choosename,olddf)
            thisnewdf=newdf.copy()
            thisnewdf["代码"]=thisnewdf["代码"].apply(lambda x:symbol_convert(x)).astype(str) # 需要指定类型为字符串
            olddf=olddf.merge(thisnewdf,on="代码",how="inner")
            olddf["总市值"]=olddf["总股本"]*olddf["open"]
            olddf["总市值"]=olddf["总市值"].astype(float)
            print(f"同花顺处理后",len(olddf))
            # # 本地使用这个
            # bkdf=pd.read_csv(f"./【本地选股】同花顺SDK/{filename}")
            # # 服务器上使用这个
            bkdf=pd.read_csv(f"/root/test/quant/【本地选股】同花顺SDK/{filename}")
            bkdf["代码"]=bkdf["代码"].str.replace("\D","",regex=True).astype(str)
            bkdf["代码"]=bkdf["代码"].apply(lambda x:symbol_convert(x)).astype(str) # 需要指定类型为字符串
            olddf=bkdf.merge(olddf,on="代码",how="inner")
            olddfcode=olddf["板块"].unique().tolist()
            print(olddfcode)
            olddf=olddf[["板块","代码","总市值","总股本","营业总收入","归母净利润"]]
            olddf["排名"]=olddf["总市值"].rank(method="max", ascending=True,na_option='bottom')
            olddf["代码"]=olddf["代码"].str.replace("\D","",regex=True).astype(str)
            numbuystock=30
            rate=len(olddf)/numbuystock
            # 下面的模型适合跑聚宽板块
            dftwo=olddf.groupby("板块").apply(lambda x: x.nsmallest(int(2*math.ceil(x.shape[0]/rate)),"总市值"))
            dftwo=dftwo.nsmallest(math.ceil(2*numbuystock),"总市值")
            # dftwo=olddf.groupby("板块").apply(lambda x: x.nsmallest(int(1.5*math.ceil(x.shape[0]/numbuystock)),"总市值"))
            # dftwo=dftwo.nsmallest(math.ceil(1.5*numbuystock),"总市值")
            dfone=olddf.groupby("板块").apply(lambda x: x.nsmallest(int(math.ceil(x.shape[0]/rate)), "总市值"))
            dfone=dfone.nsmallest(math.ceil(numbuystock),"总市值")
            dftwo.to_csv(str(start_date)+choosename+"卖出.csv")
            dfone.to_csv(str(start_date)+choosename+"买入.csv")
            dftwo["代码"]=dftwo["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            dfone["代码"]=dfone["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            buylisttwo=dftwo["代码"].tolist()
            buylistone=dfone["代码"].tolist()
            print("******",buylistone,buylisttwo)
        try:
            pd.read_csv(str(start_date)+choosename+"买入.csv")
            print("******",str(start_date)+choosename+"买入.csv"+"文件存在")
            pd.read_csv(str(start_date)+choosename+"卖出.csv")
            print("******",str(start_date)+choosename+"卖出.csv"+"文件存在")
        except Exception as e:
            print("******","******"+str(start_date)+choosename+"买入.csv"+choosename+"卖出.csv"+"文件不同时存在")
            # 获取基本面数据
            olddf=get_fundamentals(query(
                asharevalue.symbol,
                income.overall_income,
                income.np_atsopc,
                asharevalue.ashare_total_shares,
                asharevalue.total_shares,
                asharevalue.pb_mrq,# 市净率MRQ
                ),date=yesterday)
            olddf=olddf.rename(columns={
                    "asharevalue_symbol":"代码",
                    "income_overall_income":"营业总收入",
                    # income.overall_income[营业总收入],income.operating_income[营业收入]
                    "income_np_atsopc":"归母净利润",
                    # "asharevalue_total_mv_object": "总市值", # 纯A股总市值，比总市值A+B+H要好，但还是不如用总股本计算当日市值好
                    # "asharevalue_total_mv": "总市值", # 总市值A+B+H
                    "asharevalue_total_shares": "总股本",# 包括新股发行前的股份和新发行的股份的数量的总和(同花顺计算)
                    # "asharevalue_ashare_total_shares": "总股本",# 上市公司发行的人民币普通股合计股数(同花顺计算)
                    "asharevalue_pb_mrq":"市净率",
                })
            # # olddf=olddf[olddf["营业总收入"]>100000000]
            # olddf=olddf[olddf["归母净利润"]>0]
            print(choosename,olddf)
            thisnewdf=newdf.copy()
            thisnewdf["代码"]=thisnewdf["代码"].apply(lambda x:symbol_convert(x)).astype(str) # 需要指定类型为字符串
            olddf=olddf.merge(thisnewdf,on="代码",how="inner")
            olddf["总市值"]=olddf["总股本"]*olddf["open"]
            olddf=olddf.nlargest(20,"总市值")
            olddf["排名"]=olddf["市净率"].rank(method="max", ascending=True,na_option='bottom')
            olddf["代码"]=olddf["代码"].str.replace("\D","").astype(str)
            numbuystock=5 # 设置持仓数量
            olddf["市净率"]=1/olddf["市净率"]
            dfone=olddf.nlargest(math.ceil(numbuystock),"市净率")
            dftwo=olddf.nlargest(math.ceil(2*numbuystock),"市净率")
            dfone.to_csv(str(start_date)+"大市值（同花顺）买入.csv")
            dftwo.to_csv(str(start_date)+"大市值（同花顺）卖出.csv")
            dfone["代码"]=dfone["代码"].apply(lambda x: symbol_convert(x)).astype(str) # 需要指定类型为字符串
            dftwo["代码"]=dftwo["代码"].apply(lambda x: symbol_convert(x)).astype(str) # 需要指定类型为字符串
            buylistone=dfone["代码"].values
            buylisttwo=dftwo["代码"].values
            print("******",buylistone,buylisttwo)
        try:
            pd.read_csv(str(start_date)+choosename+"买入.csv")
            print("******",str(start_date)+choosename+"买入.csv"+"文件存在")
            pd.read_csv(str(start_date)+choosename+"卖出.csv")
            print("******",str(start_date)+choosename+"卖出.csv"+"文件存在")
        except Exception as e:
            print("******","******"+str(start_date)+choosename+"买入.csv"+choosename+"卖出.csv"+"文件不同时存在")
            #获取基本面数据
            olddf=get_fundamentals(query(
                asharevalue.symbol,
                income.overall_income,
                income.np_atsopc,
                asharevalue.total_shares,
                #asharevalue.ashare_total_shares,
                ),date=yesterday)
            olddf=olddf.rename(columns={
                    "asharevalue_symbol":"代码",
                    "income_overall_income":"营业总收入",
                    "income_np_atsopc":"归母净利润",
                    "asharevalue_total_shares":"总股本",#包括新股发行前的股份和新发行的股份的数量的总和(同花顺计算)
                    #"asharevalue_ashare_total_shares":"总股本",#上市公司发行的人民币普通股合计股数(同花顺计算)
                })
            #olddf=olddf[olddf["营业总收入"]>100000000]
            olddf=olddf[olddf["归母净利润"]>0]
            print(choosename,olddf)
            thisnewdf=newdf.copy()
            thisnewdf["代码"]=thisnewdf["代码"].apply(lambda x:symbol_convert(x)).astype(str) # 需要指定类型为字符串
            olddf=olddf.merge(thisnewdf,on="代码",how="inner")
            olddf["总市值"]=olddf["总股本"]*olddf["open"]
            olddf["代码"]=olddf["代码"].str.replace("\D","").astype(str)
            olddf["排名"]=olddf["总市值"].rank(method="max",ascending=True,na_option='bottom')
            numbuystock=300#设置持仓数量
            dftwo=olddf.nsmallest(math.ceil(1.2*numbuystock),"总市值")
            dfone=olddf.nsmallest(math.ceil(numbuystock),"总市值")
            dftwo.to_csv(str(start_date)+choosename+"卖出.csv")
            dfone.to_csv(str(start_date)+choosename+"买入.csv")
            dftwo["代码"]=dftwo["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            dfone["代码"]=dfone["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            buylisttwo=dftwo["代码"].values
            buylistone=dfone["代码"].values
            print("******",buylistone,buylisttwo)

choose_stocks("龙头股（聚宽）",start_date,last_date,today,yesterday)

# # # 数据比对
# # # 【本地化数据】同花顺数据源
# # dfone=pd.read_csv(f"{start_date}龙头股（聚宽）买入.csv")[["板块","代码","总市值"]]
# # dfone["代码"]=dfone["代码"].astype(str).str.zfill(6)
# # dftwo=pd.read_csv(f"{start_date}龙头股（聚宽）买入.csv")[["板块","代码","总市值"]]
# # dftwo["代码"]=dftwo["代码"].astype(str).str.zfill(6)
# # 【对照组数据】聚宽数据源
# fileone=pd.read_csv(f"{start_date}龙头股买入.csv")[["板块","代码","总市值","总股本","营业总收入","归母净利润"]]
# fileone["代码"]=fileone["代码"].astype(str).str.zfill(6)
# filetwo=pd.read_csv(f"{start_date}龙头股卖出.csv")[["板块","代码","总市值","总股本","营业总收入","归母净利润"]]
# filetwo["代码"]=filetwo["代码"].astype(str).str.zfill(6)
# # 基本面拼接
# fileone=pd.merge(dfone,fileone,on="代码",how="outer")
# filetwo=pd.merge(dftwo,filetwo,on="代码",how="outer")
# # fileone=fileone[~fileone["代码"].isin(buylistone)]# 去重
# # filetwo=filetwo[~filetwo["代码"].isin(buylisttwo)]# 去重
# # 基本面对比
# fileone=fileone.merge(olddf,on="代码",how="inner")
# filetwo=filetwo.merge(olddf,on="代码",how="inner")
# print(f"{fileone}",f"{filetwo}")
# fileone.to_csv(f"{newfilename}fileone.csv")
# filetwo.to_csv(f"{newfilename}filetwo.csv")