import datetime
import time
import akshare as ak
import requests
import pandas as pd
import math
# pip install supermind
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

# 填写账号密码【就第一次用的时候需要】
subprocess.call("supermind login -u 19511189162 -p wthWTH00",shell=True)
# # python -m supermind data ingest -b daily # 加载日k数据
# subprocess.call("python -m supermind data ingest -b daily",shell=True)
# 设置数据存储路径
subprocess.call(r"supermind data setpath -d C:\Users\13480\Desktop\quant\【本地选股（A股）】SDK\【supermind】SDK选股",shell=True)

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

def symbol_convert(stock):#股票代码加后缀
    #北交所的股票8字开头，包括82、83、87、88，其中82开头的股票表示优先股；83和87开头的股票表示普通股票、88开头的股票表示公开发行的。
    if (stock.startswith("60"))or(#上交所主板
        stock.startswith("68"))or(#上交所科创板
        stock.startswith("11"))or(#上交所可转债
        (stock.startswith("51"))or(stock.startswith("56"))or(stock.startswith("58"))):#上交所ETF
        return str(str(stock)+".SH")
        # return str(str(stock)+".SS")
    elif (stock.startswith("00"))or(#深交所主板
        stock.startswith("30"))or(#深交所创业板
        stock.startswith("12"))or(#深交所可转债
        (stock.startswith("15"))):#深交所ETF
        return str(str(stock)+".SZ")
    else:
        print("不在后缀转换名录",str(stock))
        return str(str(stock))
    
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
print("******","today",today,"yesterday",yesterday)

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
    if choosename=="中小板（同花顺）":#A股中小板策略
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
                asharevalue.total_shares,
                asharevalue.float_shares,#流通股本
                income.profit_before_tax,#利润总额【当计提历史亏损的时候利润总额大于当年净利润】
                income.net_profit,#净利润
                income.np_atsopc,#归母净利润
                income.overall_income,#营业总收入
                balance.undistributed_profits,#未分配利润
                balance.total_liabilities,#负债合计
                balance.total_liab_and_holders_equity,#负债和股东权益总计
                asharevalue.pb_mrq,#市净率MRQ
                ),date=yesterday)
            olddf=olddf.rename(columns={
                    "asharevalue_symbol":"代码",
                    "asharevalue_total_shares": "总股本",
                    # "asharevalue_float_shares": "流通股本",
                    "income_profit_before_tax":"利润总额",
                    "income_net_profit":"净利润",
                    "income_np_atsopc":"归母净利润",
                    "income_overall_income":"营业总收入",
                    "balance_undistributed_profits":"未分配利润",
                    # "income_overall_income":"营业总收入",
                    "balance_total_liabilities":"负债合计",
                    "balance_total_liab_and_holders_equity":"负债和股东权益总计",
                    "asharevalue_pb_mrq":"市净率",
                })
            olddf["资产负债率"]=olddf["负债合计"]/olddf["负债和股东权益总计"]
            olddf=olddf[olddf["资产负债率"]<1]#存在资产负债率大于1（资不抵债）的标的，跟历史数据一致
            olddf=olddf[olddf["利润总额"]>0]
            olddf=olddf[olddf["净利润"]>0]
            olddf=olddf[olddf["归母净利润"]>0]
            olddf=olddf[olddf["未分配利润"]>0]
            # olddf=olddf[olddf["营业总收入"]>100000000]
            print(choosename,olddf)
            thisnewdf=newdf.copy()
            dfcode=ak.index_stock_cons(symbol="399101")
            dfcode=dfcode.rename(columns={"品种代码":"代码"})
            thisnewdf=dfcode.merge(thisnewdf,on="代码",how="inner") 
            thisnewdf["代码"]=thisnewdf["代码"].apply(lambda x:symbol_convert(x)).astype(str) # 需要指定类型为字符串
            olddf=olddf.merge(thisnewdf,on="代码",how="inner")
            olddf["总市值"]=olddf["总股本"]*olddf["open"]
            olddf["排名"]=olddf["总市值"].rank(method="max", ascending=True,na_option='bottom')
            olddf["代码"]=olddf["代码"].str.replace(r"\D","",regex=True).astype(str)
            numbuystock=5#设置持仓数量
            dfone=olddf.nsmallest(math.ceil(numbuystock),"总市值")
            dftwo=olddf.nsmallest(math.ceil(1.5*numbuystock),"总市值")
            dftwo.to_csv(str(start_date)+choosename+"卖出.csv")
            dfone.to_csv(str(start_date)+choosename+"买入.csv")
            dftwo["代码"]=dftwo["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            dfone["代码"]=dfone["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            buylisttwo=dftwo["代码"].values
            buylistone=dfone["代码"].values
            print("******",buylistone,buylisttwo)
    elif (choosename=="龙头股（同花顺）") or (choosename=="龙头股（聚宽）"):  
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
                asharevalue.total_shares,
                asharevalue.float_shares,#流通股本
                income.profit_before_tax,#利润总额【当计提历史亏损的时候利润总额大于当年净利润】
                income.net_profit,#净利润
                income.np_atsopc,#归母净利润
                income.overall_income,#营业总收入
                balance.undistributed_profits,#未分配利润
                balance.total_liabilities,#负债合计
                balance.total_liab_and_holders_equity,#负债和股东权益总计
                asharevalue.pb_mrq,#市净率MRQ
                ),date=yesterday)
            olddf=olddf.rename(columns={
                    "asharevalue_symbol":"代码",
                    "asharevalue_total_shares": "总股本",
                    # "asharevalue_float_shares": "流通股本",
                    "income_profit_before_tax":"利润总额",
                    "income_net_profit":"净利润",
                    "income_np_atsopc":"归母净利润",
                    "income_overall_income":"营业总收入",
                    "balance_undistributed_profits":"未分配利润",
                    # "income_overall_income":"营业总收入",
                    "balance_total_liabilities":"负债合计",
                    "balance_total_liab_and_holders_equity":"负债和股东权益总计",
                    "asharevalue_pb_mrq":"市净率",
                })
            olddf["资产负债率"]=olddf["负债合计"]/olddf["负债和股东权益总计"]
            olddf=olddf[olddf["资产负债率"]<1]#存在资产负债率大于1（资不抵债）的标的，跟历史数据一致
            olddf=olddf[olddf["利润总额"]>0]
            olddf=olddf[olddf["净利润"]>0]
            olddf=olddf[olddf["归母净利润"]>0]
            olddf=olddf[olddf["未分配利润"]>0]
            # olddf=olddf[olddf["营业总收入"]>100000000]
            print(choosename,olddf)
            thisnewdf=newdf.copy()
            thisnewdf["代码"]=thisnewdf["代码"].apply(lambda x:symbol_convert(x)).astype(str) # 需要指定类型为字符串
            olddf=olddf.merge(thisnewdf,on="代码",how="inner")
            olddf["总市值"]=olddf["总股本"]*olddf["open"]
            olddf["总市值"]=olddf["总市值"].astype(float)
            print(f"同花顺处理后",len(olddf))
            if choosename=="龙头股（同花顺）":
                filename=f"【行业】同花顺一级行业对照表.csv"
            if choosename=="龙头股（聚宽）":
                filename=f"【行业】聚宽一级行业对照表.csv"   
            # # 本地使用这个
            bkdf=pd.read_csv(rf"C:\Users\13480\Desktop\quant\【本地选股（A股）】SDK\【supermind】SDK选股\{filename}")
            # # 服务器上使用这个
            # bkdf=pd.read_csv(rf"/root/test/quant/【本地选股】同花顺SDK/{filename}")
            bkdf["代码"]=bkdf["代码"].str.replace(r"\D","",regex=True).astype(str)
            bkdf["代码"]=bkdf["代码"].apply(lambda x:symbol_convert(x)).astype(str) # 需要指定类型为字符串
            olddf=bkdf.merge(olddf,on="代码",how="inner")
            olddfcode=olddf["板块"].unique().tolist()
            print(olddfcode)
            olddf=olddf[["板块","代码","总市值","总股本","营业总收入","归母净利润"]]
            olddf["排名"]=olddf["总市值"].rank(method="max", ascending=True,na_option='bottom')
            olddf["代码"]=olddf["代码"].str.replace(r"\D","",regex=True).astype(str)
            numbuystock=30
            rate=len(olddf)/numbuystock
            # 下面的模型适合跑聚宽板块
            # dftwo=olddf.groupby("板块").apply(lambda x: x.nsmallest(int(2*math.ceil(x.shape[0]/rate)),"总市值"))
            # dftwo=dftwo.nsmallest(math.ceil(2*numbuystock),"总市值")
            dftwo=olddf.groupby("板块").apply(lambda x: x.nsmallest(int(1.5*math.ceil(x.shape[0]/numbuystock)),"总市值"))
            dftwo=dftwo.nsmallest(math.ceil(1.5*numbuystock),"总市值")
            dfone=olddf.groupby("板块").apply(lambda x: x.nsmallest(int(math.ceil(x.shape[0]/rate)), "总市值"))
            dfone=dfone.nsmallest(math.ceil(numbuystock),"总市值")
            dftwo.to_csv(str(start_date)+choosename+"卖出.csv")
            dfone.to_csv(str(start_date)+choosename+"买入.csv")
            dftwo["代码"]=dftwo["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            dfone["代码"]=dfone["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            buylisttwo=dftwo["代码"].tolist()
            buylistone=dfone["代码"].tolist()
            print("******",buylistone,buylisttwo)
    elif choosename=="大市值（同花顺）":#A股大市值策略
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
                asharevalue.total_shares,
                asharevalue.float_shares,#流通股本
                income.profit_before_tax,#利润总额【当计提历史亏损的时候利润总额大于当年净利润】
                income.net_profit,#净利润
                income.np_atsopc,#归母净利润
                income.overall_income,#营业总收入
                balance.undistributed_profits,#未分配利润
                balance.total_liabilities,#负债合计
                balance.total_liab_and_holders_equity,#负债和股东权益总计
                asharevalue.pb_mrq,#市净率MRQ
                ),date=yesterday)
            olddf=olddf.rename(columns={
                    "asharevalue_symbol":"代码",
                    "asharevalue_total_shares": "总股本",
                    # "asharevalue_float_shares": "流通股本",
                    "income_profit_before_tax":"利润总额",
                    "income_net_profit":"净利润",
                    "income_np_atsopc":"归母净利润",
                    "income_overall_income":"营业总收入",
                    "balance_undistributed_profits":"未分配利润",
                    # "income_overall_income":"营业总收入",
                    "balance_total_liabilities":"负债合计",
                    "balance_total_liab_and_holders_equity":"负债和股东权益总计",
                    "asharevalue_pb_mrq":"市净率",
                })
            olddf["资产负债率"]=olddf["负债合计"]/olddf["负债和股东权益总计"]
            olddf=olddf[olddf["资产负债率"]<1]#存在资产负债率大于1（资不抵债）的标的，跟历史数据一致
            olddf=olddf[olddf["利润总额"]>0]
            olddf=olddf[olddf["净利润"]>0]
            olddf=olddf[olddf["归母净利润"]>0]
            olddf=olddf[olddf["未分配利润"]>0]
            # olddf=olddf[olddf["营业总收入"]>100000000]
            print(choosename,olddf)
            thisnewdf=newdf.copy()
            thisnewdf["代码"]=thisnewdf["代码"].apply(lambda x:symbol_convert(x)).astype(str) # 需要指定类型为字符串
            olddf=olddf.merge(thisnewdf,on="代码",how="inner")
            olddf["总市值"]=olddf["总股本"]*olddf["open"]
            olddf=olddf.nlargest(20,"总市值")
            olddf["排名"]=olddf["市净率"].rank(method="max", ascending=True,na_option='bottom')
            olddf["代码"]=olddf["代码"].str.replace(r"\D","").astype(str)
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
    elif choosename=="微盘股（同花顺）":#A股微盘股策略
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
                asharevalue.total_shares,
                asharevalue.float_shares,#流通股本
                income.profit_before_tax,#利润总额【当计提历史亏损的时候利润总额大于当年净利润】
                income.net_profit,#净利润
                income.np_atsopc,#归母净利润
                income.overall_income,#营业总收入
                balance.undistributed_profits,#未分配利润
                balance.total_liabilities,#负债合计
                balance.total_liab_and_holders_equity,#负债和股东权益总计
                asharevalue.pb_mrq,#市净率MRQ
                ),date=yesterday)
            olddf=olddf.rename(columns={
                    "asharevalue_symbol":"代码",
                    "asharevalue_total_shares": "总股本",
                    # "asharevalue_float_shares": "流通股本",
                    "income_profit_before_tax":"利润总额",
                    "income_net_profit":"净利润",
                    "income_np_atsopc":"归母净利润",
                    "income_overall_income":"营业总收入",
                    "balance_undistributed_profits":"未分配利润",
                    # "income_overall_income":"营业总收入",
                    "balance_total_liabilities":"负债合计",
                    "balance_total_liab_and_holders_equity":"负债和股东权益总计",
                    "asharevalue_pb_mrq":"市净率",
                })
            olddf["资产负债率"]=olddf["负债合计"]/olddf["负债和股东权益总计"]
            olddf=olddf[olddf["资产负债率"]<1]#存在资产负债率大于1（资不抵债）的标的，跟历史数据一致
            olddf=olddf[olddf["利润总额"]>0]
            olddf=olddf[olddf["净利润"]>0]
            olddf=olddf[olddf["归母净利润"]>0]
            olddf=olddf[olddf["未分配利润"]>0]
            # olddf=olddf[olddf["营业总收入"]>100000000]
            print(choosename,olddf)
            thisnewdf=newdf.copy()
            thisnewdf["代码"]=thisnewdf["代码"].apply(lambda x:symbol_convert(x)).astype(str) # 需要指定类型为字符串
            olddf=olddf.merge(thisnewdf,on="代码",how="inner")
            olddf["总市值"]=olddf["总股本"]*olddf["open"]
            olddf["代码"]=olddf["代码"].str.replace(r"\D","").astype(str)
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
    elif choosename=="ETF（同花顺）":#A股聚宽ETF轮动策略
        try:
            pd.read_csv(str(start_date)+choosename+"买入.csv")
            print("******",str(start_date)+choosename+"买入.csv"+"文件存在")
            pd.read_csv(str(start_date)+choosename+"卖出.csv")
            print("******",str(start_date)+choosename+"卖出.csv"+"文件存在")
        except Exception as e:
            print("******","******"+str(start_date)+choosename+"买入.csv"+choosename+"卖出.csv"+"文件不同时存在")
            #df=get_all_securities('etf',today).reset_index(drop=False)
            #df=df.rename(columns={"symbol":"代码"})
            #df.to_csv("ETF.csv")
            #1、设计理念：动量效应，优选国内大小盘、低波动、国外优秀标的进行轮动，当不符合筛选标准时转入货币基金避险；
            #2、回测标的：选择费率低廉、跟踪效率高的ETF为底层产品：中证1000（512100）、创业板50（159949）、纳指ETF（513100）、红利低波（515300）、银华日利（511880）；
            #3、买卖方法：
            #1）买入规则：近20日涨幅排名第1，且涨幅大于2%
            #2）卖出规则：近20日涨幅排名不是第1，或者涨幅小于1%
            #3）如果以上两个条件都不满足则买入银华日利（511880）
            #4）买入后只判断卖出条件，卖出后只判断买入条件，避免因为一段时间买入卖出规则同时满足，导致连续买入卖出。
            #4、仓位控制：【这个其实应该把资金分成多份，每天比对不同份数的资金】
            #5、回测数据：
            #回测时间：2017/01/01-2023/06/01
            #最优组合：[512100，159949，513100，515300，511880]【可以在不同日期分别做这个组合，也可以分成十份做不同的组合】
            #回测效果：总收益435.7%，年化收益29.9%，最大回撤21.4%
            etflist=[
                #   "159949.SZ",# 中证1000【盘中可以替换成近期最活跃的同类ETF】
                  "513100.SH",# 纳指ETF【盘中可以替换成近期最活跃的同类ETF】
                #   "515100.SH",# 红利低波【盘中可以替换成近期最活跃的同类ETF】
                #   "511880.SH",# 银华日利【盘中可以替换成近期最活跃的同类ETF】
                  "159934.SZ",# 黄金ETF【盘中可以替换成近期最活跃的同类ETF】
                  "513500.SH",# 标普ETF【盘中可以替换成近期最活跃的同类ETF】
                  ]
            print(etflist)
            df_etfs=pd.DataFrame({"代码":etflist})
            df_etfs["代码"]=df_etfs["代码"].str.replace(r"\D","").astype(str)
            #尝试以下组合方式后记得用乖离率判断标的相对强弱。以此作为大盘股的判断依据
            df_etfs["持仓数量"]=len(etflist)
            df_etfs["排名"]=df_etfs["持仓数量"]
            dftwo=df_etfs.copy()
            dfone=df_etfs.copy()
            dftwo.to_csv(str(start_date)+choosename+"卖出.csv")
            dfone.to_csv(str(start_date)+choosename+"买入.csv")
            dftwo["代码"]=dftwo["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            dfone["代码"]=dfone["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            buylisttwo=dftwo["代码"].values
            buylistone=dfone["代码"].values            
            print("******",buylistone,buylisttwo)

# choose_stocks("中小板（同花顺）",start_date,last_date,today,yesterday)
# choose_stocks("龙头股（聚宽工业股）",start_date,last_date,today,yesterday)
# choose_stocks("龙头股（同花顺）",start_date,last_date,today,yesterday)
choose_stocks("龙头股（聚宽）",start_date,last_date,today,yesterday)
# choose_stocks("大市值（同花顺）",start_date,last_date,today,yesterday)
# choose_stocks("微盘股（同花顺）",start_date,last_date,today,yesterday)
# choose_stocks("ETF（同花顺）",start_date,last_date,today,yesterday)

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