import pandas as pd
import numpy as np
# #大牛市的时候可以专门排一字板的开板，一般是适当洗牌换人，这种时候普涨情绪好，拉的高不容易被监管，游资主力也都比较格局。【大牛市一般不套人，排错了问题不大】



#通过问财获取ETF近期的成交额数据
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
import pywencai#同花顺的最新净值数据不是iopv不能用来计算溢价率
try:
  df=pd.read_csv(f"ETF详情{startday}.csv")
  df=df.iloc[:, 1:]
  df["code"]=df["code"].apply(lambda x:str(x).zfill(6))#生成六位字符串
  print(f"ETF详情{startday}.csv","存在")
except Exception as e:
  print(e)
  print(f"ETF详情{startday}.csv","不存在")
  # ETF净值数据【当天】
  # 【申购、赎回费率】跟官网对比了一下问财的最高申购赎回费率是准确的【具体说法是：申购赎回代理券商可按照不超过 0.4%的标准收取佣金】
  # 【价格及净值数据】，不是实时的，
  # 【最近十日成交额】和【最近十日逐日成交额】有差异，但是都是准确的现在用的【最近十日逐日成交额】
  # 【成分股详情】只包含重仓股
  word=f'{startday}所有ETF，最高申购费率、最高赎回费率，最近十日逐日成交额'
  df=pywencai.get(question=word,#query参数
                  loop=True,
                  query_type="fund",
                  # pro=True, #付费版才使用
                  # cookie='xxxx',
                  )
  print(df)
  df["code"]=df["code"].apply(lambda x:str(x).zfill(6))#生成六位字符串
  df.to_csv(f"ETF详情{startday}.csv")
#过滤最近十天的成交额
for day in tradedays[-10:]:
    print(day)
    df[f"{day.replace('-','')}日成交额"]=df[f"基金@成交额[{day.replace('-','')}]"].astype(float)
    df=df.sort_values(by=f"{day.replace('-','')}日成交额",ascending=False)#成交额降序排列
    df=df[df[f"{day.replace('-','')}日成交额"]>10000000]#卡在最近十天每天成交额大于一个亿从999只变成了418只
# print(df)
df=df[["基金代码","基金简称","code","基金@最高申购费率","基金@最高赎回费率"]]
print(df)



#获取iopv数据，跟上面的成交额数据和费率数据合并
import getiopv#网页里面请求的网络资源当中{:}符号标注的一般是后端的数据库
# listdf=getiopv.getetflist()#获取申赎清单【只要成分股都是A股主板的，六位纯字母】
# print(listdf)
iopvdf=getiopv.getiopv()#获取实时iopv
print(iopvdf)
iopvdf=iopvdf.rename(columns={
                      "fund_nm":"名称",
                      "fund_id":"code",#不含.SH或者.SZ的后缀
                      "last_dt":"日期",
                      "last_time":"推送时间",
                      "last_est_time":"数据时间",
                      "urls":"链接",
                      "fee":"总管理费用",
                      "m_fee":"管理费",
                      "t_fee":"托管费",
                      "creation_unit":"最小申购单位",#单位万份
                      "issuer_nm":"管理人",
                      "t0":"是否T0",#N不T0，Y是T0，主要是外盘和债券T0，美股ETF好像直接被过滤掉了
                      "amount":"份额",#亿份【这个份额可能是实时的，跟同花顺有偏差】
                      "unit_total":"规模",#单位是亿元
                      "unit_incr":"规模变化",
                      "price":"现价",
                      "volume":"成交额",#万元【这个是确确实实的成交额】
                      "ex_dt":"分红除权日",
                      "ex_info":"分红除权信息",
                      "index_nm":"指数名称",
                      "increase_rt":"涨跌幅",
                      "index_increase_rt":"指数涨跌幅",
                      "estimate_value":"估值",
                      "fund_nav":"昨日基金净值",
                      "nav_dt":"昨日基金净值发布时间",
                      "discount_rt":"溢价率",#-0.12，-0.13
                      "idx_price_dt":"指数价格时间",
                      "eval_flg":"是否有估值",#为N的话估值列为空，为Y的话可能有值【但是也有没值的部分，没值的部分可能是集思录没有进行计算，同花顺上反正是有数据的】，据kimi的说法：在集思录中，eval_flg字段通常用于表示某个项目或数据是否经过了评估（evaluation）的标志。在
                    #   "amount_notes":"",#没有数据
                    #   "owned":"",#没有数据
                    #   "holded":"",#没有数据
                    #   "pe":"",#没有数据
                    #   "pb":"",#没有数据
                      })
iopvdf=iopvdf[iopvdf["估值"]!="-"]#去掉不含估值数据的标的
iopvdf["现价"]=iopvdf["现价"].astype(float)
iopvdf["估值"]=iopvdf["估值"].astype(float)
iopvdf["溢价率"]=iopvdf["现价"]/iopvdf["估值"]-1
iopvdf["code"]=iopvdf["code"].apply(lambda x:str(x).zfill(6))#生成六位字符串
df=df.merge(iopvdf,on="code",how="inner")#拼接只要两边都有的数据
df=df.sort_values(by='溢价率',ascending=False)
df["基金@最高申购费率"]=df["基金@最高申购费率"].astype(float)
df["基金@最高赎回费率"]=df["基金@最高赎回费率"].astype(float)
df.loc[df["溢价率"]>0,"申购费后利润率"]=abs(df["溢价率"])-df["基金@最高申购费率"]/100
df.loc[df["溢价率"]<0,"赎回费后利润率"]=abs(df["溢价率"])-df["基金@最高赎回费率"]/100
df["最小申购单位"]=df["最小申购单位"].astype(float)
#进行成交额等数据清洗之后再排序
topdf=df.copy()
topdf=topdf.sort_values(by="申购费后利润率",ascending=False)
# topdf=topdf[topdf["申购费后利润率"]>=0.01]
topdf.to_csv("iopv高溢价率.csv")
lowdf=df.copy()
lowdf=lowdf.sort_values(by="赎回费后利润率",ascending=False)
# lowdf=lowdf[lowdf["申购赎回利润率"]>=0.01]
lowdf.to_csv("iopv高折价率.csv")










# #勾选独立交易之后，行情、交易、交易+行情选项一个都不要选择，才能启动miniqmt成功，否则无法执行订单
# import datetime
# import time
# import math
# import pandas as pd#conda install pandas
# import numpy as np#pip install numpy

# #【只要不用supermind，就可以直接使用3.12最新版的python执行策略】
# # supermind的SDK作废了拿不到数据，尽量使用pywencai库直接从问财接口获取
# # conda create -n my_env8 python=3.8#创建环境
# # conda env remove -n my_env8#删除环境

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

import datetime
import time
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

acc = StockAccount(account_id)# 创建账号对象
trade_api.subscribe(acc)# 订阅账号
# #设置交易参数并且获取买卖计划
# bidrate=0.005#设置盘口价差为0.004
# timecancellwait=60#设置撤单函数筛选订单的确认时间
# timetickwait=600#设置每次下单时确认是否是最新tick的确认时间【3秒一根，但是模拟盘的tick滞后五分钟左右】
# timeseconds=60#设置获取tick的函数的时间长度【避免没有数据】
# targetmoney=20000#设置下单时对手盘需要达到的厚度（即单笔目标下单金额,因为手数需要向下取整,所以实际金额比这个值低）
# traderate=2#设置单次挂单金额是targetmoney的traderate倍
# # cancellorder=False#取消一分钟不成交或者已成交金额达到目标值自动撤单并回补撤单金额的任务
# cancellorder=True#设置一分钟不成交或者已成交金额达到目标值自动撤单并回补撤单金额的任务

logger.info(f"{now},{choosename},{account_id},{start_date},{last_date},{today},{yesterday}")

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

#同花顺内打出来的数据（字符串数据）
lowdf["代码"]=lowdf["code"].astype(str).str.zfill(6).apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
topdf["代码"]=topdf["code"].astype(str).str.zfill(6).apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
for index,thisdf in lowdf.iterrows():
    thisrate=thisdf["赎回费后利润率"]#浮点数
    symbol=thisdf["代码"]
    print(type(thisrate),symbol)
    if thisrate>0.003:#只做高溢价率的标的
        print("赎回费后利润率较大，适合赎回套利")
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
              logger.info(f"{symbol},涨停不参与交易")#无法买入
          else:
            thisvolume=thisdf["最小申购单位"]*100000
            print(thisvolume)
            thismoney=ask_price_1*thisvolume
            cashmoney=trade_api.query_stock_asset(account=acc).cash#可用资金余额
            print(thismoney,type(thismoney),cashmoney,type(cashmoney))
            if cashmoney>thismoney*1.1:#余额是最小下单金额的1.1倍
              print("余额充足适合下单")
              buyorder=trade_api.order_stock(acc, stock_code=symbol,
                                order_type=xtconstant.STOCK_BUY,
                                order_volume=thisvolume,
                                price_type=xtconstant.FIX_PRICE,#限价
                                strategy_name=choosename,#策略名称
                                price=ask_price_1)
              logger.info(f"下单成功{buyorder}")
        except Exception as e:#报索引越界一般是tick数据没出来
            logger.info(f"******,发生bug:,{symbol},{e}")
        break
    

cancellorder=True#是否执行超时下单
ordernum=0#当前交易轮次
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
                        # #60秒内不成交就撤单【这个是要小于当前时间,否则就一直无法执行】
                        # if (datetime.datetime.fromtimestamp(orderall.order_time)+datetime.timedelta(seconds=timecancellwait))<datetime.datetime.now():#成交额还得超过targetmoney才可以最终撤单
                            # if (orderall.traded_volume*orderall.price>targetmoney):
                            #     try:
                            #         cancel_result = trade_api.cancel_order_stock(account=acc,order_id=orderall.order_id)
                            #         # .cancel_order(orderall.order_id)
                            #         logger.info(f"******,已成交金额达标执行撤单,{orderall.order_id,cancel_result}")
                            #     except:
                            #         logger.info(f"******","已完成或取消中的条件单不允许取消")
                            # elif orderall.traded_volume==0:#未成交撤单
                            #     try:#如果该委托已成交或者已撤单则会报错
                            #         cancel_result = trade_api.cancel_order_stock(account=acc,order_id=orderall.order_id)
                            #         # .cancel_order(orderall.order_id)
                            #         logger.info(f"******,执行撤单,{orderall.order_id},cancel_result,{cancel_result}")
                            #     except:
                            #         logger.info(f"******,已完成或取消中的条件单不允许取消")
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
                                    # moneymanage.loc[moneymanage["代码"]==str(orderall.stock_code),"moneymanage"]+=cancel_money
                                else:
                                    if orderall.order_id not in dfordercancelled["order_id"].tolist():
                                        dfordercancelled=pd.concat([dfordercancelled,dforderall],ignore_index=True)
                                        cancel_money=thiscancel_amount*orderall.price#然后就是计算撤销了的订单的未完成金额,加给下单金额当中
                                        # moneymanage.loc[moneymanage["代码"]==str(orderall.stock_code),"moneymanage"]+=cancel_money
                            elif (orderall.order_status==int(57)):
                                logger.info(f"******,废单处理,{orderall},{orderall.order_status},{orderall.order_volume}")
                                if dfordercancelled.empty:#dfordercancelled一开始是个空值,这里主要是确认一下之前有没有数据,有数据才需要检验之前是否撤销过
                                    dfordercancelled=pd.concat([dfordercancelled,dforderall],ignore_index=True)
                                    cancel_money=orderall.order_volume*orderall.price#然后就是计算撤销了的订单的未完成金额,加给下单金额当中
                                    # moneymanage.loc[moneymanage["代码"]==str(orderall.stock_code),"moneymanage"]+=cancel_money
                                if orderall.order_id not in dfordercancelled["order_id"].tolist():
                                    dfordercancelled=pd.concat([dfordercancelled,dforderall],ignore_index=True)
                                    cancel_money=orderall.order_volume*orderall.price#然后就是计算撤销了的订单的未完成金额,加给下单金额当中
                                    # moneymanage.loc[moneymanage["代码"]==str(orderall.stock_code),"moneymanage"]+=cancel_money
            dforderalls.to_csv(str(basepath)+"_dforderalls.csv")#输出所有未全部成交的订单【针对所有订单】
            dfordercancelled.to_csv(str(basepath)+"_dfordercancelled.csv")#输出已经撤销或者作废的订单【只针对的买入订单】
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
            
