#勾选独立交易之后，行情、交易、交易+行情选项一个都不要选择，才能启动miniqmt成功，否则无法执行订单
#【其实就是启动的时间短很多模块没加载出来导致下单功能和数据功能无法使用，等个几分钟就正常了】
import datetime
import time
import math
import pandas as pd#conda install pandas
import numpy as np#pip install numpy

#【只要不用supermind，就可以直接使用3.12最新版的python执行策略】
# supermind的SDK作废了拿不到数据，尽量使用pywencai库直接从问财接口获取
# conda create -n my_env8 python=3.8#创建环境
# conda env remove -n my_env8#删除环境

# xtdata提供和MiniQmt的交互接口,本质是和MiniQmt建立连接,由MiniQmt处理行情数据请求,再把结果回传返回到python层。使用的行情服务器以及能获取到的行情数据和MiniQmt是一致的,要检查数据或者切换连接时直接操作MiniQmt即可。
# 对于数据获取接口,使用时需要先确保MiniQmt已有所需要的数据,如果不足可以通过补充数据接口补充,再调用数据获取接口获取。
# 对于订阅接口,直接设置数据回调,数据到来时会由回调返回。订阅接收到的数据一般会保存下来,同种数据不需要再单独补充。
from xtquant import xtdata

# #测试里面买不了深证的是因为没开相关记录,上证的正常买入没有限制
# 配置日志
basepath=r"C:\Users\13480\gitee\trade\【本地选股（A股）】SDK\【QMT】miniqmtSDK"
# pip install loguru # 这个框架可以解决中文不显示的问题
from loguru import logger
logger.add(
    sink=f"{basepath}/log.log",#sink: 创建日志文件的路径。
    # sink=f"log.log",#sink: 创建日志文件的路径。
    level="INFO",#level: 记录日志的等级,低于这个等级的日志不会被记录。等级顺序为 debug < info < warning < error。设置 INFO 会让 logger.debug 的输出信息不被写入磁盘。
    rotation="00:00",#rotation: 轮换策略,此处代表每天凌晨创建新的日志文件进行日志 IO；也可以通过设置 "2 MB" 来指定 日志文件达到 2 MB 时进行轮换。   
    retention="7 days",#retention: 只保留 7 天。 
    compression="zip",#compression: 日志文件较大时会采用 zip 进行压缩。
    encoding="utf-8",#encoding: 编码方式
    enqueue=True,#enqueue: 队列 IO 模式,此模式下日志 IO 不会影响 python 主进程,建议开启。
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"#format: 定义日志字符串的样式,这个应该都能看懂。
)

def symbol_convert(stock):#股票代码加后缀
    #北交所的股票8字开头，包括82、83、87、88，其中82开头的股票表示优先股；83和87开头的股票表示普通股票、88开头的股票表示公开发行的。
    if (stock.startswith("60"))or(#上交所主板
        stock.startswith("68"))or(#上交所科创板
        stock.startswith("11"))or(#上交所可转债
        (stock.startswith("5"))):#上交所ETF：51、52、56、58都是
        return str(str(stock)+".SH")
        # return str(str(stock)+".SS")
    elif (stock.startswith("00"))or(#深交所主板
        stock.startswith("30"))or(#深交所创业板
        stock.startswith("12"))or(#深交所可转债
        (stock.startswith("159"))):#深交所ETF：暂时只有159的是深交所ETF
        return str(str(stock)+".SZ")
    else:
        print("不在后缀转换名录",str(stock))
        return str(str(stock))
    
def filter_kcb_stock(stocks):#过滤科创北交股票
    for stock in stocks[:]:
        if stock[0]=="4" or stock[0]=="8" or stock[:2]=="68":
            stocks.remove(stock)
    return stocks

def choose_stocks(choosename,now,start_date,last_date,today,yesterday):
    if choosename=="可转债":#A股可转债策略
        try:
            pd.read_csv(str(basepath)+f"/{str(start_date)}"+choosename+"买入.csv")
            logger.info(f"******"+str(basepath)+f"/{str(start_date)}"+choosename+"买入.csv"+"文件存在")
            pd.read_csv(str(basepath)+f"/{str(start_date)}"+choosename+"卖出.csv")
            logger.info(f"******"+str(basepath)+f"/{str(start_date)}"+choosename+"卖出.csv"+"文件存在")
        except Exception as e:
            logger.info(f"******"+"******"+str(basepath)+f"/{str(start_date)}"+choosename+"买入.csv"+choosename+"卖出.csv"+"文件不同时存在")
            #pip install akshare
            import akshare as ak
            df_cbonds=ak.bond_cb_redeem_jsl()#强制赎回信息【实时数据】
            df_cbonds["代码"]=df_cbonds["代码"].str.replace(r'\D','',regex=True).astype(str)
            logger.info(f"去掉强制赎回之前,{len(df_cbonds)}")
            df_cbonds=df_cbonds[~(df_cbonds["强赎状态"]=="已公告强赎")]
            logger.info(f"去掉强制赎回之后,{len(df_cbonds)}")
            df_cbonds["总市值"]=df_cbonds["现价"]*df_cbonds["剩余规模"]        
            df_cbonds["转股溢价率"]=df_cbonds["现价"]/((100/df_cbonds["转股价"])*df_cbonds["正股价"])
            df_cbonds["三低指数"]=df_cbonds["总市值"]*df_cbonds["转股溢价率"]
            df_cbonds["排名"]=df_cbonds["三低指数"].rank(method="max", ascending=True,na_option='bottom')
            # df_cbonds.to_csv("可转债强制赎回信息.csv")

            olddf=ak.bond_zh_cov_info_ths()
            olddf["代码"]=olddf["债券代码"].str.replace(r'\D','',regex=True).astype(str)
            olddf=olddf[olddf["到期时间"]>(datetime.datetime.now()+datetime.timedelta(days=180)).date()]
            logger.info(f"当前展示K线,{len(olddf)}")
            # olddf.to_csv("债券评级同花顺.csv")
            df_cbonds=df_cbonds[df_cbonds["代码"].isin(olddf["代码"].tolist())]
            logger.info(f"去掉到期时间之后,{len(olddf)}")

            #评级接口需要开集思录会员,如果要用的话开了再改,目前使用阉割版
            olddf=ak.bond_cb_jsl()
            olddf["代码"]=olddf["代码"].str.replace(r'\D','',regex=True).astype(str)
            logger.info(f"当前展示K线,{len(olddf)}")
            # olddf=olddf[olddf["到期时间"]>(datetime.datetime.now()+datetime.timedelta(days=180)).date()]
            # olddf=olddf[(olddf["债券评级"]=="BBB")|(olddf["债券评级"]=="BBB+")|(olddf["债券评级"].str.contains("A"))]
            # olddf["总市值"]=olddf["现价"]*olddf["剩余规模"]  
            # olddf["转股溢价率"]=olddf["转股溢价率"]+1
            # # olddf["转股溢价率"]=olddf["现价"]/((100/olddf["转股价"])*olddf["正股价"])
            # olddf["三低指数"]=olddf["总市值"]*olddf["转股溢价率"]
            # olddf["排名"]=olddf["三低指数"].rank(method="max", ascending=True,na_option='bottom')
            # olddf.to_csv("债券评级.csv")
            # logger.info(f"去掉平级和到期时间之后K线,{len(olddf)}")
            # olddf=olddf[olddf["代码"].isin(cbonds)]
            # logger.info(f"去掉强制赎回之后K线,{len(olddf)}")

            notbonds=olddf[~(olddf["债券评级"]=="BBB")|(olddf["债券评级"]=="BBB+")|(olddf["债券评级"].str.contains("A"))]
            df_cbonds=df_cbonds[~df_cbonds["代码"].isin(notbonds)]
            logger.info(f"去掉强制赎回之后K线,{len(df_cbonds)}")

            df_cbonds=df_cbonds[df_cbonds["现价"]<150]
            logger.info(f"去掉价格高于150之后,{len(df_cbonds)}")
                    
            df_cbonds["正股代码"]=df_cbonds["正股代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            stocks=df_cbonds["正股代码"].tolist()
            
            # 处理停牌和ST数据
            for stock in stocks:
                df=xtdata.get_instrument_detail(stock, iscomplete=False)
                try:
                    logger.info(f"{df},{type(df)}")
                    # InstrumentStatus#停牌状态
                    # InstrumentName#合约名称
                    logger.info(f'{df["InstrumentStatus"]},{type(df["InstrumentStatus"])}')
                    logger.info(f'{df["InstrumentName"]},{type(df["InstrumentName"])}')
                    # if (df["InstrumentStatus"]!=0):#-1是跌停没有数据了,3是算上当天停牌了三个交易日,数越大停牌时间越长
                    #     if stock in stocks:
                    #         stocks.remove(stock)
                    #         logger.info("去掉停牌",stock,df["InstrumentStatus"])
                    if ("S" in df["InstrumentName"])or("退" in df["InstrumentName"]):
                        if stock in stocks:
                            stocks.remove(stock)
                            logger.info(f'去掉ST,{stock},{df["InstrumentName"]}')
                except Exception as e:
                    logger.info(e,stock)
            # logger.info("过滤完ST和停牌标的之后",len(stocks))
            df_cbonds=df_cbonds[df_cbonds["正股代码"].isin(stocks)]
            logger.info(f"过滤完正股ST和停牌标的之后,{len(df_cbonds)}")

            olddf=df_cbonds.copy()
            olddf['代码']=olddf['代码'].str.replace(r'\D','',regex=True).astype(str)
            numbuystock=10 # 设置持仓数量
            dftwo=olddf.nsmallest(math.ceil(1.5*numbuystock), "三低指数")
            dfone=olddf.nsmallest(math.ceil(numbuystock), "三低指数")
            dftwo.to_csv(str(basepath)+f"/{str(start_date)}"+choosename+"卖出.csv")
            dfone.to_csv(str(basepath)+f"/{str(start_date)}"+choosename+"买入.csv")
            dftwo["代码"]=dftwo["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            dfone["代码"]=dfone["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            buylisttwo=dftwo["代码"].values
            buylistone=dfone["代码"].values
            logger.info(f"******,{buylistone},{buylisttwo}")
    if (choosename=="中小板")or(choosename=="微盘股"):#A股中小板策略
        try:
            pd.read_csv(str(basepath)+f"/{str(start_date)}"+choosename+"买入.csv")
            logger.info(f"******"+str(basepath)+f"/{str(start_date)}"+choosename+"买入.csv"+"文件存在")
            pd.read_csv(str(basepath)+f"/{str(start_date)}"+choosename+"卖出.csv")
            logger.info(f"******"+f"/{str(start_date)}"+choosename+"卖出.csv"+"文件存在")
        except Exception as e:
            logger.info(f"******"+"******"+f"/{str(start_date)}"+choosename+"买入.csv"+choosename+"卖出.csv"+"文件不同时存在")
            # 获取板块列表
            stocks=xtdata.get_stock_list_in_sector("沪深A股")
            stocks=filter_kcb_stock(stocks)
            logger.info(stocks)#000和300是SZ结尾,600是SH结尾
            # 处理停牌和ST数据
            for stock in stocks:
                df=xtdata.get_instrument_detail(stock,iscomplete=False)
                # InstrumentStatus#停牌状态
                # InstrumentName#合约名称
                # logger.info(df["InstrumentStatus"],type(df["InstrumentStatus"]))
                try:#有可能报错
                    if (df["InstrumentStatus"]!=0):#-1是跌停没有数据了,3是算上当天停牌了三个交易日,数越大停牌时间越长
                        if stock in stocks:
                            stocks.remove(stock)
                            logger.info(f'去掉停牌,{stock},{df["InstrumentStatus"]}')
                    if ("S" in df["InstrumentName"])or(("退" in df["InstrumentName"])):
                        if stock in stocks:
                            stocks.remove(stock)
                            logger.info(f'去掉ST,{stock},{df["InstrumentName"]}')
                except Exception as e:#报索引越界一般是tick数据没出来
                    logger.info(e)
            logger.info(f"过滤完ST和停牌标的之后,{len(stocks)}")
        
            #使用问财python库获取数据【同花顺利润口径不同,普遍是ttm的归母净利润】
            #问财获取数据【需要提前安装node.js进行页面解析,接口获取到的最新价列就是实时最新价】
            # pip install pywencai
            logger.info("问财下载财务数据")
            import pywencai
            import datetime
            try:
                # 获取交易日期
                tradelist=xtdata.get_trading_dates("SH",start_time="",end_time=start_date,count=2)
                strday=datetime.datetime.fromtimestamp(tradelist[0]/1000).strftime("%Y%m%d")
            except Exception as e:#报索引越界一般是tick数据没出来
                logger.info("获取交易日失败直接用前一个自然日")
                strday=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y%m%d")
            logger.info(f"strday,{strday}")
            word=f'主板创业板股票昨天的总股本及净利润'
            # word=f'中小综指所有成分股票昨天的总股本及净利润'
            olddf=pywencai.get(question=word,loop=True)
            logger.info(f"{olddf}")
            olddf=olddf[~(olddf[f"股票简称"].str.contains("S"))]
            olddf=olddf[~(olddf[f"股票简称"].str.contains("退"))]
            guben=[column for column in olddf.columns if f"总股本[" in column]
            olddf["总股本"]=olddf[guben]
            lirun=[column for column in olddf.columns if f"归属母公司股东的净利润(ttm)[" in column]
            olddf["归母净利润"]=olddf[lirun]
            # olddf["总股本"]=olddf[f"总股本[{strday}]"]
            # olddf["归母净利润"]=olddf[f"归属母公司股东的净利润(ttm)[{strday}]"]
            # olddf=olddf[["最新价","股票简称","股票代码","总股本","归母净利润"]]
            olddf=olddf.dropna(subset=['最新价'])#去掉未上市的标的【当然停牌数据也被去掉了】
            olddf=olddf[olddf["归母净利润"]>0]
            olddf["代码"]=olddf["股票代码"]
            olddf.to_csv("问财数据.csv")
            olddf=olddf[olddf["代码"].isin(stocks)]
            olddf=olddf[["代码","总股本","最新价"]]
            olddf["总股本"]=olddf["总股本"].astype(float)
            olddf["最新价"]=olddf["最新价"].astype(float)
            olddf=olddf[olddf["最新价"]>4]#只要大于4元的
            logger.info(f"{olddf}")#如果不修改数据格式,那么很可能数据大小越界
        
            #股本数据结合价格合成市值数据
            olddf["总市值"]=olddf["总股本"]*olddf["最新价"]
            olddf["排名"]=olddf["总市值"].rank(method="max",ascending=True,na_option='bottom')
            olddf['代码']=olddf['代码'].str.replace(r'\D','',regex=True).astype(str)
            if (choosename=="中小板"):
                numbuystock=10#设置持仓数量
            if (choosename=="微盘股"):
                numbuystock=30#设置持仓数量
            dfone=olddf.nsmallest(math.ceil(numbuystock),"排名")
            dftwo=olddf.nsmallest(math.ceil(1.5*numbuystock),"排名")
            dftwo.to_csv(str(basepath)+f"/{str(start_date)}"+choosename+"卖出.csv")
            dfone.to_csv(str(basepath)+f"/{str(start_date)}"+choosename+"买入.csv")
            dftwo["代码"]=dftwo["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            dfone["代码"]=dfone["代码"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
            buylisttwo=dftwo["代码"].values
            buylistone=dfone["代码"].values
            logger.info(f"******,{buylistone},{buylisttwo}")

now=datetime.datetime.now()

start_date=now.strftime("%Y%m%d")#测试当天的数据
# last_date=(now-datetime.timedelta(days=730)).strftime("%Y%m%d")
last_date=(now-datetime.timedelta(days=250)).strftime("%Y%m%d")
while True:
    # 获取交易日期
    tradelist=xtdata.get_trading_dates("SH",start_time="",end_time=start_date,count=2)
    logger.info(f"{tradelist}")
    if len(tradelist)!=0:
        logger.info("日期获取成功")
        today=tradelist[-1]
        today=datetime.datetime.fromtimestamp(today/1000)
        today=today.strftime("%Y%m%d")
        yesterday=tradelist[0]
        yesterday=datetime.datetime.fromtimestamp(yesterday/1000)
        yesterday=yesterday.strftime("%Y%m%d")
        break
    else:
        logger.info("日期获取失败")
        time.sleep(10)
        today=now.strftime("%Y%m%d")
        yesterday=(now-datetime.timedelta(days=1)).strftime("%Y%m%d")
        break
logger.info(f"******"+"today"+today+"yesterday"+yesterday)

#交易模块
import random
from xtquant.xttype import StockAccount
from xtquant.xttrader import XtQuantTrader
from xtquant import xtconstant
# QMT账号
# mini_qmt_path = r"D:\迅投极速交易终端 睿智融科版\userdata_mini"# miniQMT安装路径
# account_id = "2011506"# QMT账号
# account_id = "2011908"
# mini_qmt_path = r"D:\国金QMT交易端模拟\userdata_mini"# miniQMT安装路径
mini_qmt_path = r"C:\国金QMT交易端模拟\userdata_mini"# miniQMT安装路径

account_id = "55013189"
if (account_id=='55013189')or(account_id=='2011506')or(account_id=="2011908"):#密码:wth000
    # choosename="可转债"
    choosename="微盘股"
    tradeway="taker"#设置主动吃单
    # tradeway="maker"#设置被动吃单
else:
    choosename="微盘股"
    tradeway="taker"#设置主动吃单
session_id = int(random.randint(100000,999999))# 创建session_id
trade_api = XtQuantTrader(mini_qmt_path,session_id)# 创建交易对象
trade_api.start()# 启动交易对象

while True:
    connect_result = trade_api.connect()# 连接客户端
    print("连接结果",connect_result)
    if connect_result==0:
        logger.info("连接成功")
        break
    else:
        logger.info("重新链接")
        time.sleep(1)

# import pandas as pd
# # 【需要额外判断交易日判断数据对不对，错了及时推送报错到微信或者钉钉】
# dfstock=pd.read_csv(r"C:\Users\13480\gitee\trade\【本地选股（A股）】SDK\【华鑫证券】奇点\ETF成份证券信息20241016.csv")
# # ,交易日,交易所代码,ETF交易代码,ETF成份证券代码,成分证券名称,成分证券数量,现金替代标志,溢价比例,申购替代金额,赎回替代金额,挂牌市场,ETF申赎类型
# #关键数据：最大现金替代比例【也就是说可以如果股票数量{实物申购}不足，最多可以使用多大比例的现金进行替代】
# dfetf=pd.read_csv(r"C:\Users\13480\gitee\trade\【本地选股（A股）】SDK\【华鑫证券】奇点\ETF清单信息20241016.csv")
# # ,交易日,交易所代码,ETF交易代码,ETF申赎代码,最小申购赎回单位份数,最大现金替代比例,预估现金差额,前一交易日现金差额,前一交易日基金单位净值,前一交易日申赎基准单位净值,当日申购赎回基准单位的红利金额,ETF申赎类型,ETF证券名称
# # dfetf["前一交易日申赎基准单位净值"]=dfetf["前一交易日基金单位净值"]*dfetf["最小申购赎回单位份数"]#这里的前一交易日基金单位净值是四舍五入之后的数据，应该以前一交易日申赎基准单位净值为准计算单笔最小下单金额和单位净值
# dfetf["前一交易日基金单位净值"]=dfetf["前一交易日申赎基准单位净值"]/dfetf["最小申购赎回单位份数"]#这里的前一交易日基金单位净值是四舍五入之后的数据，应该以前一交易日申赎基准单位净值为准计算单笔最小下单金额和单位净值
# # dfetf["ETF交易代码"].tolist()#ETF详情
#[获取IOPV数据]（不适合miniqmt）
# etfiopv=xtdata.get_etf_iopv("510050.SH")
# print(etfiopv)
# #下载所有ETF数据[VIP权限数据]（否则程序会报错需要升级客户端或者使用投研版）
# # xtdata.download_etf_info()
# # etfinfo=xtdata.get_etf_info()#获取ETF基金代码为511050的全部ETF申赎清单数据【需要升级成投研版或者升级客户端】
# # #实时申赎数据[VIP权限数据]
# # from xtquant import xtdata
# # xtdata.download_history_data(stock, 'etfstatistics', start_time, end_time, incrementally = True)
# # data = xtdata.get_market_data_ex([], stock_list, period = 'etfstatistics', start_time = "", end_time = "")

acc = StockAccount(account_id)# 创建账号对象
trade_api.subscribe(acc)# 订阅账号
#设置交易参数并且获取买卖计划
bidrate=0.005#设置盘口价差为0.004
timecancellwait=60#设置撤单函数筛选订单的确认时间
timetickwait=600#设置每次下单时确认是否是最新tick的确认时间【3秒一根，但是模拟盘的tick滞后五分钟左右】
timeseconds=60#设置获取tick的函数的时间长度【避免没有数据】
targetmoney=20000#设置下单时对手盘需要达到的厚度（即单笔目标下单金额,因为手数需要向下取整,所以实际金额比这个值低）
traderate=2#设置单次挂单金额是targetmoney的traderate倍
# cancellorder=False#取消一分钟不成交或者已成交金额达到目标值自动撤单并回补撤单金额的任务
cancellorder=True#设置一分钟不成交或者已成交金额达到目标值自动撤单并回补撤单金额的任务

logger.info(f"{now},{choosename},{account_id},{start_date},{last_date},{today},{yesterday}")
choose_stocks(choosename,now,start_date,last_date,today,yesterday)#使用特定函数根据策略名称配置相应参数

buyfilename=choosename+"买入.csv"
sellfilename=choosename+"卖出.csv"
logger.info(f"{buyfilename},{sellfilename}")
buydf=pd.read_csv(str(basepath)+f"/{str(start_date)}"+buyfilename)
selldf=pd.read_csv(str(basepath)+f"/{str(start_date)}"+sellfilename)
#确认买入数量【即持仓数量】
targetnum=len(buydf)#一般是30
logger.info(f"预计持仓只数,{targetnum}")

#查询资产
portfolio=trade_api.query_stock_asset(account=acc)
logger.info(f"查询资产,portfolio")#收盘之后估计会返回空值
available_cash=portfolio.cash#available_cash可用资金
market_value=portfolio.market_value#market_value证券市值
frozen_cash=portfolio.frozen_cash#frozen_cash冻结资金
total_value=portfolio.total_asset#total_asset总资产
logger.info(f"******"+"可用资金"+str(available_cash)+"证券市值"+str(market_value)+"冻结资金"+str(frozen_cash)+"总资产"+str(total_value))
premoney=(total_value)/targetnum#确定每只股票的交易金额（根据目标持仓数量制定）

#同花顺内打出来的数据（字符串数据）
buydf["代码"]=buydf["代码"].astype(str).str.zfill(6).apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
selldf["代码"]=selldf["代码"].astype(str).str.zfill(6).apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
logger.info(f"buydf,{buydf}")

logger.info(f"针对涨停标的不进行卖出处理之前selldf,{len(selldf)}")
positions=trade_api.query_stock_positions(account=acc)
for position in positions:
    symbol=position.stock_code
    logger.info(symbol)
    if position.volume>0:
        logger.info(position.volume)
        try:
            #返回五档数据
            tick=xtdata.get_full_tick([symbol])
            tick=tick[symbol]
            ask_price_1=tick["askPrice"][0]
            ask_volume_1=tick["askVol"][0]
            ask_price_2=tick["askPrice"][1]
            ask_volume_2=tick["askVol"][1]
            logger.info(f"{ask_price_1},{ask_volume_1},{ask_price_2},{ask_volume_2}")
            if (ask_price_2==0)and(ask_price_1==0):
                logger.info(f"{symbol},涨停不进行卖出")
                if symbol not in selldf["代码"].tolist():
                    selldf=pd.concat([selldf,pd.DataFrame({"代码":[symbol],"排名":[0]})])
        except Exception as e:#报索引越界一般是tick数据没出来
            logger.info(f"******,发生bug:,{symbol},{e}")
logger.info(f"针对涨停标的不进行卖出处理之后selldf,{len(selldf)}")

logger.info(f"针对跌停标的不进行买入处理之前buydf,{len(buydf)}")
for symbol in buydf["代码"].tolist():
    try:
        #返回五档数据
        tick=xtdata.get_full_tick([symbol])
        tick=tick[symbol]
        ask_price_1=tick["askPrice"][0]
        ask_volume_1=tick["askVol"][0]
        ask_price_2=tick["askPrice"][1]
        ask_volume_2=tick["askVol"][1]
        logger.info(f"{ask_price_1},{ask_volume_1},{ask_price_2},{ask_volume_2}")
        if (ask_price_2==0)and(ask_price_1==0):
            logger.info(symbol,"涨停不进行买入")
            buydf=pd.concat([buydf,pd.DataFrame({"代码":[symbol],"排名":[0]})])
        bid_price_1=tick["bidPrice"][0]
        bid_volume_1=tick["bidVol"][0]
        bid_price_2=tick["bidPrice"][1]
        bid_volume_2=tick["bidVol"][1]
        logger.info(f"{bid_price_1},{ask_volume_1},{bid_price_2},{bid_volume_2}")
        if (bid_price_2==0)and(bid_price_1==0):
            logger.info(symbol,"跌停不进行买入")
            buydf=buydf[~(buydf["代码"]==symbol)]
    except Exception as e:#报索引越界一般是tick数据没出来
        logger.info("******","发生bug:",symbol,e)
logger.info("针对跌停标的不进行买入处理之后buydf",len(buydf))
logger.info("注意事项【停牌标的也算作涨跌停标的了】")
            
targetcolumn="排名"
dfone=buydf.copy()
dftwo=selldf.copy()
buydf=buydf[["代码",targetcolumn]]
selldf=selldf[["代码",targetcolumn]]
buydf["moneymanage"]=premoney
moneymanage=buydf[["代码","moneymanage"]]
ordernum=0#初始化当前交易轮次为0
logger.info(f"策略启动,account_id,{account_id},premoney,{premoney}")

dfposition=pd.DataFrame([])
positions=trade_api.query_stock_positions(account=acc)
for position in positions:
    symbol=position.stock_code
    logger.info(symbol,position.volume)
    if position.volume>0:
        dfposition=pd.concat([dfposition,pd.DataFrame({"symbol":[symbol],
                                                        "volume":[position.volume],
                                                        "can_use_volume":[position.can_use_volume],
                                                        "frozen_volume":[position.frozen_volume],
                                                        "market_value":[position.market_value],
                                                        })],ignore_index=True)
logger.info(f"******,本轮持仓,{dfposition}")
dfposition.to_csv(str(basepath)+"_dfposition.csv")
#判断交易计划
selldflist=dftwo["代码"].tolist()
buydflist=dfone["代码"].tolist()

# 获取当前时间
thistime=datetime.datetime.now()

# #【设置1、4月空仓】
# thistime=(context.blotter.current_dt)
# if ((thistime.month==4)or(thistime.month==1)):
    # print(thistime.month,"当前月份空仓")
    # selldflist=[]
    # buydflist=[]
    
#【设置一键清仓】
selldflist=[]
buydflist=[]

if not dfposition.empty:#持仓不为空值
    positionsymbols=dfposition["symbol"].tolist()
    falsesymbol=[x for x in positionsymbols if x not in selldflist]
    truesymbol=[x for x in positionsymbols if x in selldflist]
    havesymbol=[x for x in buydflist if x in positionsymbols]
    nothavesymbol=[x for x in buydflist if x not in positionsymbols]
    logger.info("******"+
        "不在卖出观察池的需卖出标的"+
        f"{falsesymbol}"+
        "在卖出观察池的正确持仓标的"+
        f"{truesymbol}"+
        "在买入观察池的已持仓标的"+
        f"{havesymbol}"+
        "在买入观察池的未持仓标的"+
        f"{nothavesymbol}"+
        "持仓标的"+
        f"{positionsymbols}"
    )
    selldf=dfposition.copy()#只针对持仓当中的标的筛选应卖出标的
    buydf=dfone[dfone["代码"].isin(buydflist)]
    # buydf=buydf[~(buydf["symbol"].isin(upstocks))]#涨停不买【本地代码当中在前面已经对此单独进行了验证，这里无需执行ptrade上类似的代码】
    selldf=selldf[~(selldf["symbol"].isin(selldflist))]
    print("实际应卖出股票，去掉应持有标的后",len(selldf))
    # selldf=selldf[~(selldf["symbol"].isin(upstocks))]#涨停不卖【本地代码当中在前面已经对此单独进行了验证，这里无需执行ptrade上类似的代码】
    # selldf=selldf[~(selldf["symbol"].isin(downstocks))]#跌停不卖【本地代码当中在前面已经对此单独进行了验证，这里无需执行ptrade上类似的代码】
    print("实际应卖出股票，去掉涨停标的后",len(selldf))
    if len(selldf)>0:
        # print("应卖出股票只数大于0，需要先根据是否涨停再次计算卖出计划")
        # # 只保留未停牌的股票【获取当前tick确认其trade_status不为STOPT】【本地代码当中在前面已经对此单独进行了验证，这里无需执行ptrade上类似的代码】
        # notstopstocks=[]
        # for stock in selldf["symbol"].tolist():#错在没有分别对每一个标的进行过滤参数传错了
        #     stock_trade_status=get_snapshot(stock)[stock]["trade_status"]
        #     print("stock_trade_status",stock_trade_status,type(stock_trade_status))
        #     # if (stock_trade_status!="STOPT"):#仅仅保留未停牌状态的标的                    
        #     if (stock_trade_status=="TRADE"):#仅仅保留处于连续竞价状态的标的
        #         print(stock,"未停牌")
        #         notstopstocks.append(stock)
        # selldf=selldf[(selldf["symbol"].isin(notstopstocks))]
        # print("实际应卖出股票，只保留可以交易标的后",len(selldf))
        #应买入股票处理
        buydf=buydf[~(buydf["代码"].isin(selldf["symbol"].tolist()))]
        buydf=buydf[~(buydf["代码"].isin(dfposition["symbol"].tolist()))]
        logger.info(f"实际应买入股票,去除应卖出标的后,{len(buydf)}")
        #计算卖出后剩余持仓数量
        hodlstocks=len(dfposition["symbol"].tolist())-len(selldf["symbol"].tolist())
        logger.info(f"卖出后剩余持仓数量,{hodlstocks}")
        if hodlstocks!=0:
            buydf=buydf.sort_values(by=targetcolumn)
            buydf=buydf[:(targetnum-hodlstocks)]#这里减去的是持仓股票数量,然后在持仓标的中选择金额不足的向上拼接
            logger.info(f"对买入计划重新配置之后,{len(buydf)}")
    else:
        logger.info("应卖出股票只数小于0,直接去除掉当前的持仓标的计算买入计划")
        #应买入股票处理
        buydf=buydf[~(buydf["symbol"].isin(dfposition["symbol"].tolist()))]
        logger.info(f"实际应买入股票,去除应卖出标的后,{len(buydf)}")
        #计算卖出后剩余持仓数量
        hodlstocks=len(dfposition["symbol"].tolist())-len(selldf["symbol"].tolist())
        logger.info(f"全部卖出后剩余持仓数量,{hodlstocks}")
        if hodlstocks!=0:
            buydf=buydf.sort_values(by=targetcolumn)
            buydf=buydf[:(targetnum-hodlstocks)]#这里减去的是持仓股票数量,然后在持仓标的中选择金额不足的向上拼接
            logger.info(f"对买入计划重新配置之后,{len(buydf)}")
else:
    if (len(selldflist)==0)and(len(buydflist)==0):
        logger.info(f"{thistime.month},当月空仓")
        selldf=pd.DataFrame({"代码":[],"总市值":[]})
        buydf=pd.DataFrame({"代码":[],"总市值":[]})
    else:
        logger.info(f"{thistime.month},正常交易")
        selldf=dftwo.copy()
        buydf=dfone.copy()
    logger.info(f"实际应卖出股票,{len(selldf)}")
    logger.info(f"实际应买入股票,{len(buydf)}")
selldf=selldf.reset_index(drop=True)
selldf.to_csv(str(basepath)+"selldf.csv")
buydf=buydf.reset_index(drop=True)
buydf.to_csv(str(basepath)+"buydf.csv")
logger.info(f"实际卖出计划,{selldf},实际买入计划,{buydf}")

#进行交易计划之前的资金管理机制【计算需要对哪些进行买入对哪些进行卖出】
premoney=(total_value)/targetnum#每股理论应持仓金额
#注意这个金额还得补之前超跌的股票的部分的差额
buydf["moneymanage"]=premoney
moneymanage=buydf[["代码","moneymanage"]]
logger.info("单股金额"+str(premoney)+"moneymanage"+str(moneymanage))
if not dfposition.empty:
    holddf=dfposition.copy()
    holddf=holddf[~(holddf["symbol"].isin(selldf["symbol"].tolist()))]
    for index,thisposition in holddf.iterrows():#余额不为零才进行下一步免得浪费时间
        logger.info(f"{index},{thisposition}")
        symbol=thisposition["symbol"]
        # logger.info("symbol",symbol)
        if thisposition["volume"]>0:#只对当前持仓大于0的标的进行处理，如果第一次执行就是volume，如果二次执行需要使用can_use_volume
            thispositionmoney=thisposition["market_value"]
            # if (premoney-thispositionmoney)>float(0.0000001)*premoney:#持仓标的与其总资产平均后的理论应持仓市值的偏差在百分之十以上才执行
            if (premoney-thispositionmoney)>float(0.1)*premoney:#持仓标的与其总资产平均后的理论应持仓市值的偏差在百分之十以上才执行
                logger.info(f"{symbol},thispositionmoney,{thispositionmoney},premoney,{premoney},持仓标的与其总资产平均后的理论应持仓市值的偏差在百分之十以上执行补仓操作")
                if symbol not in moneymanage["代码"].tolist():
                    newdata=pd.DataFrame([{"代码":symbol,"moneymanage":(premoney-thispositionmoney)}])
                    moneymanage=pd.concat([moneymanage,newdata],ignore_index=True)
                    logger.info(f"******,拼接上之前应买入未买全的股票,之后最新的下单金额计划,{moneymanage}")
                elif symbol in moneymanage["代码"].tolist():
                    moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]=(premoney-thispositionmoney)
                    logger.info(f"******,更新完之前应买入未买全的股票,之后最新的下单金额计划,{moneymanage}")
    moneymanage=moneymanage[moneymanage["moneymanage"]>=targetmoney]#只保留应下单金额大于targetmoney的标的
else:
    logger.info("当前没有持仓,无需对下单计划进行调整")
logger.info(moneymanage)

#初始化存储已经撤销订单的列表【只初始化一次,不要重置】
dfordercancelled=pd.DataFrame({})
while True:
    dforderalls=pd.DataFrame({})#初始化存储全部订单的列表【每一轮都可以重置】
    ordernum+=1#交易轮次计数,避免频繁撤单
    if ordernum>1:
        logger.info(f"{datetime.datetime.now()},从第二轮开始每执行一轮休息5秒避免订单过度冲击市场,当前轮次,{ordernum}")
        # time.sleep(5)#休息一秒,避免空转
        time.sleep(1)#休息一秒,避免空转
    # # 成交XtTrade
    # trades = trade_api.query_stock_trades(account=acc)#成交记录
    # logger.info(trades)
    # # 属性	类型	注释
    # # account_type	int	账号类型,参见数据字典
    # # account_id	str	资金账号
    # # stock_code	str	证券代码
    # # order_type	int	委托类型,参见数据字典
    # # traded_id	str	成交编号
    # # traded_time	int	成交时间
    # # traded_price	float	成交均价
    # # traded_volume	int	成交数量
    # # traded_amount	float	成交金额
    # # order_id	int	订单编号
    # # order_sysid	str	柜台合同编号
    # # strategy_name	str	策略名称
    # # order_remark	str	委托备注
    # # direction	int	多空方向,股票不需要；参见数据字典
    # # offset_flag	int	交易操作,用此字段区分股票买卖,期货开、平仓,期权买卖等；参见数据字典
    # 委托XtOrder
    # 属性	类型	注释
    # account_type	int	账号类型,参见数据字典
    # account_id	str	资金账号
    # stock_code	str	证券代码,例如"600000.SH"
    # order_id	int	订单编号
    # order_sysid	str	柜台合同编号
    # order_time	int	报单时间
    # order_type	int	委托类型,参见数据字典
    # order_volume	int	委托数量
    # price_type	int	报价类型,参见数据字典
    # price	float	委托价格
    # traded_volume	int	成交数量
    # traded_price	float	成交均价
    # order_status	int	委托状态,参见数据字典【决定是否撤单用这个】
    # status_msg	str	委托状态描述,如废单原因
    # strategy_name	str	策略名称
    # order_remark	str	委托备注
    # direction	int	多空方向,股票不需要；参见数据字典
    # offset_flag	int	交易操作,用此字段区分股票买卖,期货开、平仓,期权买卖等；参见数据字典
    if ordernum%20==0:
    # if ordernum%2==0:
        logger.info("交易轮次达标,执行撤单任务")
        if cancellorder:#如果cancellorder设置为true则执行以下撤单流程【最低撤单金额一万元】
            orderalls = trade_api.query_stock_orders(account=acc,cancelable_only=False)#仅查询可撤委托
            for orderall in orderalls:
                # #模拟盘下午无法识别到撤单（orderall.status_msg无数据）把这块拿出来单独研究
                # logger.info(f"{orderall},{type(orderall.offset_flag)},{orderall.direction},{orderall.price_type},{orderall.order_id}")
                # 账号状态(account_status)
                # xtconstant.ORDER_UNREPORTED	48	未报
                # xtconstant.ORDER_WAIT_REPORTING	49	待报
                # xtconstant.ORDER_REPORTED	50	已报
                # xtconstant.ORDER_REPORTED_CANCEL	51	已报待撤
                # xtconstant.ORDER_PARTSUCC_CANCEL	52	部成待撤
                # xtconstant.ORDER_PART_CANCEL	53	部撤
                # xtconstant.ORDER_CANCELED	54	已撤
                # xtconstant.ORDER_PART_SUCC	55	部成
                # xtconstant.ORDER_SUCCEEDED	56	已成
                # xtconstant.ORDER_JUNK	57	废单【这个也得算金额】
                # xtconstant.ORDER_UNKNOWN	255	未知
                #拼接orderall的数据【不对已成（56）、待报（49）、未报（48）订单进行处理】大部分是54已撤、55部成、56已成、57废单
                if ((orderall.order_status!=int(56))and(orderall.order_status!=int(49))and(orderall.order_status!=int(48))):
                    dforderall=pd.DataFrame({
                        "order_status":[orderall.order_status],
                        "order_id":[orderall.order_id],
                        "status_msg":[orderall.status_msg],
                        "symbol":[orderall.stock_code],
                        "amount":[orderall.order_volume],
                        "trade_amount":[orderall.traded_volume],
                        "trade_price":[orderall.traded_price],
                        "order_type":[orderall.order_type],#int,24卖出,23买入
                        "direction":[orderall.direction],#int,多空方向,股票不需要；参见数据字典
                        "offset_flag":[orderall.offset_flag],#int,交易操作,用此字段区分股票买卖,期货开、平仓,期权买卖等；参见数据字典
                        "price":[orderall.price],
                        "price_type":[orderall.price_type],
                        "datetime":[datetime.datetime.fromtimestamp(orderall.order_time).strftime("%Y%m%d %H:%M:%S")],
                        "secondary_order_id":[orderall.order_id]})
                    dforderalls=pd.concat([dforderalls,dforderall],ignore_index=True)
                    if ((orderall.order_status==int(55))or(orderall.order_status==int(50))):
                        logger.info(f"******,不是已成交订单,{orderall.order_id}")
                        #60秒内不成交就撤单【这个是要小于当前时间,否则就一直无法执行】
                        if (datetime.datetime.fromtimestamp(orderall.order_time)+datetime.timedelta(seconds=timecancellwait))<datetime.datetime.now():#成交额还得超过targetmoney才可以最终撤单
                            if (orderall.traded_volume*orderall.price>targetmoney):
                                try:
                                    cancel_result = trade_api.cancel_order_stock(account=acc,order_id=orderall.order_id)
                                    # .cancel_order(orderall.order_id)
                                    logger.info(f"******,已成交金额达标执行撤单,{orderall.order_id,cancel_result}")
                                except:
                                    logger.info(f"******","已完成或取消中的条件单不允许取消")
                            elif orderall.traded_volume==0:#未成交撤单
                                try:#如果该委托已成交或者已撤单则会报错
                                    cancel_result = trade_api.cancel_order_stock(account=acc,order_id=orderall.order_id)
                                    # .cancel_order(orderall.order_id)
                                    logger.info(f"******,执行撤单,{orderall.order_id},cancel_result,{cancel_result}")
                                except:
                                    logger.info(f"******,已完成或取消中的条件单不允许取消")
                    else:#撤单或者废单之后的金额回补
                        # 交易操作(offset_flag)
                        # 枚举变量名	值	含义
                        # xtconstant.OFFSET_FLAG_OPEN	48	买入,开仓
                        # xtconstant.OFFSET_FLAG_CLOSE	49	卖出,平仓
                        # xtconstant.OFFSET_FLAG_FORCECLOSE	50	强平
                        # xtconstant.OFFSET_FLAG_CLOSETODAY	51	平今
                        # xtconstant.OFFSET_FLAG_ClOSEYESTERDAY	52	平昨
                        # xtconstant.OFFSET_FLAG_FORCEOFF	53	强减
                        # xtconstant.OFFSET_FLAG_LOCALFORCECLOSE	54	本地强平
                        if (orderall.order_type==int(23)):#这里只计算BUY方向的订单,24是卖23是买
                            # logger.info("该订单是买入")
                            # time.sleep(10)
                            if (orderall.order_status==int(54)):
                                thiscancel_amount=orderall.order_volume-orderall.traded_volume
                                logger.info(f"{orderall}")
                                logger.info(f"******,撤单成功,{orderall},{orderall.order_status},{thiscancel_amount}")
                                if dfordercancelled.empty:#dfordercancelled一开始是个空值,这里主要是确认一下之前有没有数据,有数据才需要检验之前是否撤销过
                                    dfordercancelled=pd.concat([dfordercancelled,dforderall],ignore_index=True)
                                    cancel_money=thiscancel_amount*orderall.price#然后就是计算撤销了的订单的未完成金额,加给下单金额当中
                                    moneymanage.loc[moneymanage["代码"]==str(orderall.stock_code),"moneymanage"]+=cancel_money
                                else:
                                    if orderall.order_id not in dfordercancelled["order_id"].tolist():
                                        dfordercancelled=pd.concat([dfordercancelled,dforderall],ignore_index=True)
                                        cancel_money=thiscancel_amount*orderall.price#然后就是计算撤销了的订单的未完成金额,加给下单金额当中
                                        moneymanage.loc[moneymanage["代码"]==str(orderall.stock_code),"moneymanage"]+=cancel_money
                            elif (orderall.order_status==int(57)):
                                logger.info(f"******,废单处理,{orderall},{orderall.order_status},{orderall.order_volume}")
                                if dfordercancelled.empty:#dfordercancelled一开始是个空值,这里主要是确认一下之前有没有数据,有数据才需要检验之前是否撤销过
                                    dfordercancelled=pd.concat([dfordercancelled,dforderall],ignore_index=True)
                                    cancel_money=orderall.order_volume*orderall.price#然后就是计算撤销了的订单的未完成金额,加给下单金额当中
                                    moneymanage.loc[moneymanage["代码"]==str(orderall.stock_code),"moneymanage"]+=cancel_money
                                if orderall.order_id not in dfordercancelled["order_id"].tolist():
                                    dfordercancelled=pd.concat([dfordercancelled,dforderall],ignore_index=True)
                                    cancel_money=orderall.order_volume*orderall.price#然后就是计算撤销了的订单的未完成金额,加给下单金额当中
                                    moneymanage.loc[moneymanage["代码"]==str(orderall.stock_code),"moneymanage"]+=cancel_money
            dforderalls.to_csv(str(basepath)+"_dforderalls.csv")#输出所有未全部成交的订单【针对所有订单】
            dfordercancelled.to_csv(str(basepath)+"_dfordercancelled.csv")#输出已经撤销或者作废的订单【只针对的买入订单】
            logger.info("******","资金管理","premoney",premoney,"moneymanage",moneymanage)
    moneymanage.to_csv(str(basepath)+"_dfmoneymanage.csv")
    #重置并获取持仓信息【这里的目的是重新获取最新持仓以避免执行卖出成功后数据没有更新导致的持仓数量不对的情况】
    dfposition=pd.DataFrame([])
    positions=trade_api.query_stock_positions(account=acc)
    for position in positions:
        symbol=position.stock_code
        logger.info(symbol,position.volume)
        if position.volume>0:
            dfposition=pd.concat([dfposition,pd.DataFrame({"symbol":[symbol],
                                                            "volume":[position.volume],
                                                            "can_use_volume":[position.can_use_volume],
                                                            "frozen_volume":[position.frozen_volume],
                                                            "market_value":[position.market_value],
                                                            })],ignore_index=True)
    logger.info(f"******,本轮持仓,{dfposition}")
    dfposition.to_csv(str(basepath)+"_dfposition.csv")
    logger.info(f"******,卖出")
    if not dfposition.empty:#有持仓则验证是否卖出
        for symbol in dfposition["symbol"].tolist():
            if symbol in selldf["symbol"].tolist():
                thisposition=dfposition[dfposition["symbol"]==symbol]
                logger.info(f"{thisposition},{thisposition.can_use_volume.values[0]}")
                if (thisposition.can_use_volume.values[0]>0):#余额及可用余额都要大于0才执行卖出动作
                    logger.info(f"******,{symbol},持仓数量,{thisposition}")
                    try:
                        #返回五档数据
                        tick=xtdata.get_full_tick([symbol])
                        tick=tick[symbol]
                        logger.info(f"{tick}")
                        ask_price_1=tick["askPrice"][0]
                        ask_volume_1=tick["askVol"][0]
                        bid_price_1=tick["bidPrice"][0]
                        bid_volume_1=tick["bidVol"][0]
                        ask_price_2=tick["askPrice"][1]
                        ask_volume_2=tick["askVol"][1]
                        bid_price_2=tick["bidPrice"][1]
                        bid_volume_2=tick["bidVol"][1]
                        lastPrice=tick["lastPrice"]
                        timetag= datetime.datetime.strptime(tick["timetag"],"%Y%m%d %H:%M:%S")
                        logger.info(f"{lastPrice},{type(lastPrice)},timetag:{timetag},{type(timetag)}")
                        if (timetag+datetime.timedelta(seconds=timetickwait)>datetime.datetime.now()):
                            logger.info(f"******,确认是最新tick,执行交易")
                            if (ask_price_1-bid_price_1)<=(((ask_price_1+bid_price_1)/2)*bidrate):#盘口价差
                                logger.info(f"******,盘口价差适宜,适合执行交易")
                                if ((symbol.startswith("12")) or (symbol.startswith("11"))):#针对11开头或者12开头的转债单独处理
                                    ask_volume_1*=10
                                    bid_volume_1*=10
                                    if tradeway=="maker":#maker下单【不需要考虑深度问题】
                                        if (thisposition.can_use_volume.values[0]*ask_price_1)<(traderate*targetmoney):
                                            logger.info("******","剩余全部卖出")
                                            sellvolume =(math.floor(thisposition.can_use_volume.values[0]/10)*10)
                                            sellorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                            order_type=xtconstant.STOCK_SELL,
                                                                            order_volume=sellvolume,
                                                                            price_type=xtconstant.FIX_PRICE,#限价
                                                                            strategy_name=choosename,#策略名称
                                                                            price=ask_price_1)
                                            logger.info(f"下单成功{sellorder},{ask_price_1},{sellvolume}")
                                        else:#限价卖出最小下单金额
                                            logger.info(f"******,卖出目标金额")
                                            sellvolume=(math.floor((targetmoney/ask_price_1)/10)*10)
                                            if (thisposition.can_use_volume.values[0]*bid_price_1)>500000:#针对余额高于500000的标的单独扩大下单数量
                                                sellvolume*=10
                                            logger.info(f"sellvolume{sellvolume},{sellvolume*ask_price_1}")
                                            sellorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                            order_type=xtconstant.STOCK_SELL,
                                                                            order_volume=sellvolume,
                                                                            price_type=xtconstant.FIX_PRICE,#限价
                                                                            strategy_name=choosename,#策略名称
                                                                            price=ask_price_1)
                                            logger.info(f"下单成功{sellorder},{ask_price_1},{sellvolume}")
                                        time.sleep(1)
                                    if tradeway=="taker":#maker下单【需要考虑深度问题】
                                        if (bid_price_1*bid_volume_1)>targetmoney:#盘口深度【己方一档买入】（转债价格较高,一档深度相对小一些）                                 
                                            if (thisposition.can_use_volume.values[0]*bid_price_1)<(traderate*targetmoney):
                                                logger.info(f"******,剩余全部卖出")
                                                sellvolume =(math.floor(thisposition.can_use_volume.values[0]/10)*10)
                                                sellorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                            order_type=xtconstant.STOCK_SELL,
                                                                            order_volume=sellvolume,
                                                                            price_type=xtconstant.FIX_PRICE,#限价
                                                                            strategy_name=choosename,#策略名称
                                                                            price=bid_price_1)
                                                logger.info(f"下单成功{sellorder},{bid_price_1},{sellvolume}")
                                            else:#限价卖出最小下单金额
                                                logger.info(f"******,卖出目标金额")
                                                sellvolume=(math.floor((targetmoney/bid_price_1)/10)*10)
                                                if (thisposition.can_use_volume.values[0]*bid_price_1)>500000:#针对余额高于500000的标的单独扩大下单数量
                                                    sellvolume*=10
                                                logger.info(f"sellvolume{sellvolume},{sellvolume*bid_price_1}")
                                                sellorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                            order_type=xtconstant.STOCK_SELL,
                                                                            order_volume=sellvolume,
                                                                            price_type=xtconstant.FIX_PRICE,#限价
                                                                            strategy_name=choosename,#策略名称
                                                                            price=bid_price_1)
                                                logger.info(f"下单成功{sellorder},{bid_price_1},{sellvolume}")
                                else:#非可转债交易方式
                                    ask_volume_1*=100
                                    bid_volume_1*=100
                                    if tradeway=="maker":#maker下单【不需要考虑深度问题】
                                        if (thisposition.can_use_volume.values[0]*ask_price_1)<(traderate*targetmoney):
                                            logger.info(f"******,剩余全部卖出")
                                            sellvolume =(math.floor(thisposition.can_use_volume.values[0]/100)*100)
                                            sellorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                            order_type=xtconstant.STOCK_SELL,
                                                                            order_volume=sellvolume,
                                                                            price_type=xtconstant.FIX_PRICE,#限价
                                                                            strategy_name=choosename,#策略名称
                                                                            price=ask_price_1)
                                            logger.info(f"下单成功{sellorder},{ask_price_1},{sellvolume}")
                                        else:#限价卖出最小下单金额
                                            logger.info("******","卖出目标金额")
                                            sellvolume=(math.floor((targetmoney/ask_price_1)/100)*100)
                                            if (thisposition.can_use_volume.values[0]*ask_price_1)>500000:#针对余额高于500000的标的单独扩大下单数量
                                                sellvolume*=10
                                            logger.info(f"sellvolume{sellvolume},{sellvolume*ask_price_1}")
                                            sellorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                            order_type=xtconstant.STOCK_SELL,
                                                                            order_volume=sellvolume,
                                                                            price_type=xtconstant.FIX_PRICE,#限价
                                                                            strategy_name=choosename,#策略名称
                                                                            price=ask_price_1)
                                            logger.info(f"下单成功{sellorder},{ask_price_1},{sellvolume}")
                                    if tradeway=="taker":#maker下单【需要考虑深度问题】
                                        if (bid_price_1*bid_volume_1)>targetmoney:#盘口深度【对手盘一档买入】                                            
                                            if (thisposition.can_use_volume.values[0]*bid_price_1)<(traderate*targetmoney):
                                                logger.info(f"******,剩余全部卖出")
                                                sellvolume =(math.floor(thisposition.can_use_volume.values[0]/100)*100)
                                                sellorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                            order_type=xtconstant.STOCK_SELL,
                                                                            order_volume=sellvolume,
                                                                            price_type=xtconstant.FIX_PRICE,#限价
                                                                            strategy_name=choosename,#策略名称
                                                                            price=bid_price_1)
                                                logger.info(f"下单成功{sellorder},{bid_price_1},{sellvolume}")
                                            else:#限价卖出最小下单金额
                                                logger.info(f"******,卖出目标金额")
                                                sellvolume=(math.floor((targetmoney/bid_price_1)/100)*100)
                                                if (thisposition.can_use_volume.values[0]*bid_price_1)>500000:#针对余额高于500000的标的单独扩大下单数量
                                                    sellvolume*=10
                                                logger.info(f"sellvolume{sellvolume},{sellvolume*bid_price_1}")
                                                sellorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                            order_type=xtconstant.STOCK_SELL,
                                                                            order_volume=sellvolume,
                                                                            price_type=xtconstant.FIX_PRICE,#限价
                                                                            strategy_name=choosename,#策略名称
                                                                            price=bid_price_1)
                                                logger.info(f"下单成功{sellorder},{bid_price_1},{sellvolume}")
                    except Exception as e:#报索引越界一般是tick数据没出来
                        logger.info("******","发生bug:",symbol,e)
    logger.info("******","买入")
    moneymanage=moneymanage.sort_values(by="moneymanage",ascending=False)#这里是由大到小排序,默认由小到大
    for symbol in moneymanage["代码"].tolist():#如果恰好是三十只以上股票,且没有需要卖出的股票时,moneymanage为空会导致报错
        buymoney=moneymanage[moneymanage["代码"]==str(symbol)]["moneymanage"].iloc[0]
        if buymoney>targetmoney:#只针对待买入金额超过targetmoney的标的进行买入,否则直接掠过
                #查询资产
                portfolio=trade_api.query_stock_asset(account=acc)
                portfolio_available_cash=portfolio.cash#available_cash可用资金
                logger.info(f"当前余额,{portfolio_available_cash}")
                if portfolio_available_cash>targetmoney:
                    logger.info(f"******,买入余额充足,{symbol},{buymoney}")
                    try:
                        #返回五档数据
                        tick=xtdata.get_full_tick([symbol])
                        tick=tick[symbol]
                        logger.info(f"{tick}")
                        ask_price_1=tick["askPrice"][0]
                        ask_volume_1=tick["askVol"][0]
                        bid_price_1=tick["bidPrice"][0]
                        bid_volume_1=tick["bidVol"][0]
                        ask_price_2=tick["askPrice"][1]
                        ask_volume_2=tick["askVol"][1]
                        bid_price_2=tick["bidPrice"][1]
                        bid_volume_2=tick["bidVol"][1]
                        lastPrice=tick["lastPrice"]
                        timetag= datetime.datetime.strptime(tick["timetag"],"%Y%m%d %H:%M:%S")
                        logger.info(f"{lastPrice},{type(lastPrice)},timetag:{timetag},{type(timetag)}")
                        if (timetag+datetime.timedelta(seconds=timetickwait)>datetime.datetime.now()):
                            logger.info(f"******,确认是最新tick,执行交易")
                            if (ask_price_1-bid_price_1)<=(((ask_price_1+bid_price_1)/2)*bidrate):#盘口价差
                                logger.info(f"******,盘口价差适宜,适合执行交易")        
                                if ((symbol.startswith("12")) or (symbol.startswith("11"))):#针对11开头或者12开头的转债单独处理
                                    ask_volume_1*=10
                                    bid_volume_1*=10
                                    if tradeway=="maker":#maker下单【不需要考虑深度问题】
                                        if buymoney<(traderate*targetmoney):
                                            logger.info(f"******,剩余全部买入")
                                            buyvolume=(math.floor((buymoney/bid_price_1)/10)*10)
                                            buyorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                                order_type=xtconstant.STOCK_BUY,
                                                                                order_volume=buyvolume,
                                                                                price_type=xtconstant.FIX_PRICE,#限价
                                                                                strategy_name=choosename,#策略名称
                                                                                price=bid_price_1)
                                            logger.info(f"下单成功{buyorder}")
                                            bidmoney=float(bid_price_1)*buyvolume
                                            moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
                                        else:
                                            logger.info(f"******,买入目标金额")
                                            buyvolume=(math.floor((targetmoney/bid_price_1)/10)*10)
                                            if buymoney>500000:#针对总下单余额高于500000的标的单独扩大下单数量
                                                buyvolume*=10
                                            buyorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                                order_type=xtconstant.STOCK_BUY,
                                                                                order_volume=buyvolume,
                                                                                price_type=xtconstant.FIX_PRICE,#限价
                                                                                strategy_name=choosename,#策略名称
                                                                                price=bid_price_1)
                                            logger.info(f"下单成功{buyorder}")
                                            bidmoney=float(bid_price_1)*buyvolume
                                            moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
                                        time.sleep(1)
                                    if tradeway=="taker":#taker下单【跟其他地方一样需要考虑深度】
                                        if (ask_price_1*ask_volume_1)>targetmoney:#盘口深度【己方一档买入】（转债价格较高,一档深度相对小一些） 
                                            if buymoney<(traderate*targetmoney):
                                                logger.info(f"******,剩余全部买入")
                                                buyvolume=(math.floor((buymoney/ask_price_1)/10)*10)
                                                buyorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                                order_type=xtconstant.STOCK_BUY,
                                                                                order_volume=buyvolume,
                                                                                price_type=xtconstant.FIX_PRICE,#限价
                                                                                strategy_name=choosename,#策略名称
                                                                                price=ask_price_1)
                                                logger.info(f"下单成功{buyorder}")
                                                bidmoney=float(ask_price_1)*buyvolume
                                                moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
                                            else:
                                                logger.info(f"******,买入目标金额")
                                                buyvolume=(math.floor((targetmoney/ask_price_1)/10)*10)
                                                if buymoney>500000:#针对总下单余额高于500000的标的单独扩大下单数量
                                                    buyvolume*=10
                                                buyorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                                order_type=xtconstant.STOCK_BUY,
                                                                                order_volume=buyvolume,
                                                                                price_type=xtconstant.FIX_PRICE,#限价
                                                                                strategy_name=choosename,#策略名称
                                                                                price=ask_price_1)
                                                logger.info(f"下单成功{buyorder}")
                                                bidmoney=float(ask_price_1)*buyvolume
                                                moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
                                else:#其他交易情况
                                    ask_volume_1*=100
                                    bid_volume_1*=100
                                    if tradeway=="maker":#maker下单【不需要考虑深度问题】
                                        if buymoney<(traderate*targetmoney):
                                            logger.info(f"******,剩余全部买入")
                                            buyvolume=(math.floor((buymoney/bid_price_1)/100)*100)
                                            buyorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                                order_type=xtconstant.STOCK_BUY,
                                                                                order_volume=buyvolume,
                                                                                price_type=xtconstant.FIX_PRICE,#限价
                                                                                strategy_name=choosename,#策略名称
                                                                                price=bid_price_1)
                                            logger.info(f"下单成功{buyorder}")
                                            bidmoney=float(bid_price_1)*buyvolume
                                            moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
                                        else:
                                            logger.info(f"******,买入目标金额")
                                            buyvolume=(math.floor((targetmoney/bid_price_1)/100)*100)
                                            if buymoney>500000:#针对总下单余额高于500000的标的单独扩大下单数量
                                                buyvolume*=10
                                            buyorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                                order_type=xtconstant.STOCK_BUY,
                                                                                order_volume=buyvolume,
                                                                                price_type=xtconstant.FIX_PRICE,#限价
                                                                                strategy_name=choosename,#策略名称
                                                                                price=bid_price_1)
                                            logger.info(f"下单成功{buyorder}")
                                            bidmoney=float(bid_price_1)*buyvolume
                                            moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
                                    if tradeway=="taker":#taker下单【跟其他地方一样需要考虑深度】
                                        if (ask_price_1*ask_volume_1)>targetmoney:#盘口深度【对手盘一档买入】
                                            if buymoney<(traderate*targetmoney):
                                                logger.info(f"******,剩余全部买入")
                                                buyvolume=(math.floor((buymoney/ask_price_1)/100)*100)
                                                buyorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                                order_type=xtconstant.STOCK_BUY,
                                                                                order_volume=buyvolume,
                                                                                price_type=xtconstant.FIX_PRICE,#限价
                                                                                strategy_name=choosename,#策略名称
                                                                                price=ask_price_1)
                                                logger.info(f"下单成功{buyorder}")
                                                bidmoney=float(ask_price_1)*buyvolume
                                                moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
                                            else:
                                                logger.info(f"******,买入目标金额")
                                                buyvolume=(math.floor((targetmoney/ask_price_1)/100)*100)
                                                if buymoney>500000:#针对总下单余额高于500000的标的单独扩大下单数量
                                                    buyvolume*=10
                                                buyorder=trade_api.order_stock(acc, stock_code=symbol,
                                                                                order_type=xtconstant.STOCK_BUY,
                                                                                order_volume=buyvolume,
                                                                                price_type=xtconstant.FIX_PRICE,#限价
                                                                                strategy_name=choosename,#策略名称
                                                                                price=ask_price_1)
                                                logger.info(f"下单成功{buyorder}")
                                                bidmoney=float(ask_price_1)*buyvolume
                                                moneymanage.loc[moneymanage["代码"]==str(symbol),"moneymanage"]-=bidmoney
                    except Exception as e:#报索引越界一般是tick数据没出来
                        logger.info(f"******,发生bug:,{symbol},{e}")
    logger.info(f"******,任务结束")

    # ETF申赎
    # 申购 - xtconstant.ETF_PURCHASE
    # 赎回 - xtconstant.ETF_REDEMPTION

    # #返回五档数据
    # tick=xtdata.get_full_tick([symbol])
    # tick=tick[symbol]
    # # logger.info(tick)
    # ask_price_1=tick["askPrice"][0]
    # ask_volume_1=tick["askVol"][0]
    # ask_price_2=tick["askPrice"][1]
    # ask_volume_2=tick["askVol"][1]

    # #每日自动打新
    # df=xtdata.get_ipo_info(today,today)#获取新股申购数据
    # logger.info(df,"当日可申购新股数据")
    # df=trade_api.query_new_purchase_limit(acc)#当前账户新股申购额度查询
    # logger.info(df,"当前账户新股申购额度")
    # df=xtdata.query_ipo_data()#当日新股信息查询

    # #获取ETF实时净值（貌似得从旧QMT获取）
    # logger.info(trade_api.get_etf_iopv("510050.SH"))    

    # 异步下单委托反馈XtOrderResponse
    # 属性	类型	注释
    # account_type	int	账号类型,参见数据字典
    # account_id	str	资金账号
    # order_id	int	订单编号
    # strategy_name	str	策略名称
    # order_remark	str	委托备注
    # seq	int	异步下单的请求序号
    # 异步撤单委托反馈XtCancelOrderResponse
    # 属性	类型	注释
    # account_type	int	账号类型,参见数据字典
    # account_id	str	资金账号
    # order_id	int	订单编号
    # order_sysid	str	柜台委托编号
    # cancel_result	int	撤单结果
    # seq	int	异步撤单的请求序号
    # 下单失败错误XtOrderError
    # 属性	类型	注释
    # account_type	int	账号类型,参见数据字典
    # account_id	str	资金账号
    # order_id	int	订单编号
    # error_id	int	下单失败错误码
    # error_msg	str	下单失败具体信息
    # strategy_name	str	策略名称
    # order_remark	str	委托备注
    # 撤单失败错误XtCancelError
    # 属性	类型	注释
    # account_type	int	账号类型,参见数据字典
    # account_id	str	资金账号
    # order_id	int	订单编号
    # market	int	交易市场 0:上海 1:深圳
    # order_sysid	str	柜台委托编号
    # error_id	int	下单失败错误码
    # error_msg	str	下单失败具体信息
