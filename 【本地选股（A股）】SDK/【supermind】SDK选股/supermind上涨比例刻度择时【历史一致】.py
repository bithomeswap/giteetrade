import datetime
import time
import pandas as pd
import math
# pip install supermind#需要科学上网
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
import subprocess
# # 填写账号密码【就第一次用的时候需要】
# subprocess.call("supermind login -u 19511189162 -p wthWTH00",shell=True)
# # 设置数据存储路径【因为需要取日线数据所以需要提前下载】
# subprocess.call(r"supermind data setpath -d C:\Users\13480\Desktop\quant\【本地选股（A股）】SDK\【supermind】SDK选股",shell=True)
# python -m supermind data ingest -b daily # 加载日k数据
# subprocess.call("python -m supermind data ingest -b daily",shell=True)
def filter_kcb_stock(stocks): # 过滤科创北交股票
    for stock in stocks[:]:
        if stock[0]=="4" or stock[0]=="8" or stock[:2]=="68":
            stocks.remove(stock)
        # if stock[0]=="4" or stock[0]=="8" or stock[:2]=="68" or stock[:2]=="30":
        #     stocks.remove(stock)
    return stocks

# MAD:中位数去极值
def extreme_MAD(dt,n):
    median = dt.quantile(0.5) #找出中位数
    new_median = (abs((dt - median)).quantile(0.5)) #偏差值的中位数
    dt_up = median + n*new_median #上限
    dt_down = median - n*new_median #下限
    return dt_up,dt_down

# #设置计算刻度因子的周期【在200的基础上预留20天计算均线用】

# long=20
long=220
now=datetime.datetime.now()
tradeday=get_trade_days(end_date=(
    # now#其实可以在盘中从当天开始拿数据更好
    now-datetime.timedelta(days=1)#只从上一个交易日开始算【因子检验用100天前的对比】
    ).strftime("%Y-%m-%d"),count=(long+1)).tolist()#多留一天要不下面第一天没法取数据
print(tradeday)

basepath=r"C:\Users\13480\Desktop\quant\【本地选股（A股）】SDK\【supermind】SDK选股"

try:
    oldopenclosedf=pd.read_csv("openclosedf.csv")
    oldopenclosedf["日期"]=oldopenclosedf["日期"].astype(str)
    print(type(oldopenclosedf["日期"][0]))
    openclosedf=oldopenclosedf#开仓平仓因子数据
except Exception as e:
    openclosedf=pd.DataFrame({"日期":[]})#开仓平仓因子数据
    print(e)
time.sleep(10)
for thisday in tradeday:
    index=tradeday.index(thisday)
    print(index)
    # print(type(thisday),type(thisday.strftime('%Y%m%d')))
    if index>0:
        yesterday=tradeday[index-1]
        print(thisday,index,yesterday)
        if (yesterday.strftime('%Y%m%d')) not in openclosedf["日期"].tolist():
            #上涨比例空仓法、资金流入空仓法
            stocks=get_all_securities('stock',thisday)
            stocks=stocks.index.values # 获取当天所有标的
            stocks=[stock for stock in stocks]
            stocks=filter_kcb_stock(stocks) # 去除科创北交
            print(len(stocks))
            stocks=[stock for stock in stocks if stock!="301587.SZ"]#当日数据有报错
            df=get_price(
                securities=stocks,
                start_date=None,
                end_date=yesterday,
                fre_step='1d',
                fields=["close","prev_close","is_paused","is_st"], # 获取全部数据列，其中昨日收盘价是用来计算总股本的
                fq='pre',
                # fq=None, # 这里动态复权或者不复权都是可以的
                bar_count=1,
                is_panel=1).to_frame()
            # df=df[(df["is_paused"]==0)&(df["is_st"]==0)]
            df=df[(df["is_paused"]==0)]
            df["隔日涨幅"]=df["close"]/df["prev_close"]
            df=df.reset_index()
            df=df.rename(columns={"minor":"代码"})
            thisdf=pd.DataFrame({"涨跌幅":[df["隔日涨幅"].mean()],
                                "上涨比例":[len(df[df["隔日涨幅"]>1])/len(df)],
                                "日期":[yesterday.strftime('%Y%m%d')],
                                #  "日期":[thisday.strftime('%Y%m%d')],
                                })
            # print(thisdf)
            openclosedf=pd.concat([openclosedf,thisdf])
        else:
            print("已经有数据不需要获取")
print(len(openclosedf),openclosedf)
openclosedf["上涨比例"] = openclosedf["上涨比例"].round(16)# 将 "上涨比例" 列保留 16 位小数
# 【转CSV会有小数位数的偏差，直接拿出来的好像就是恰好16位小数】
openclosedf.to_csv(f"{basepath}\openclosedf.csv")
openclosedf=pd.read_csv(f"{basepath}\openclosedf.csv")
openclosedf=openclosedf.sort_values(by='日期',ascending=True)
#sort_values加上inplace=True这个参数之后直接在原值上修改不用前面等式
datelist=openclosedf["日期"].unique().tolist()#获取观察周期的所有日期数据
targetdf=openclosedf.copy()#只保留最近long天的数据
# targetdf["上涨比例"] = targetdf["上涨比例"].round(16)# 将 "上涨比例" 列保留 16 位小数
targetdf["上涨比例快线"]=targetdf["上涨比例"].rolling(12).mean()
targetdf["上涨比例慢线"]=targetdf["上涨比例"].rolling(3).mean()
targetdf["上涨比例均线均值"]=(targetdf["上涨比例快线"]+targetdf["上涨比例慢线"])/2
targetdf=targetdf[targetdf["日期"]>=datelist[-(long-20)]]#保留long个日期且去掉其中算均线产生的空值

# 计算上涨比例均线刻度
data=pd.concat([targetdf["上涨比例快线"],targetdf["上涨比例慢线"]])
dt_up,dt_down=extreme_MAD(data,5.2)
print("双临界值",dt_up,dt_down)
targetdf.loc[targetdf["上涨比例均线均值"]>=dt_up,"上涨比例均线均值"]=dt_up
targetdf.loc[targetdf["上涨比例均线均值"]<=dt_down,"上涨比例均线均值"]=dt_down
lastday=datelist[-1]
targetdf.loc[targetdf["日期"]==lastday,"上涨比例均线刻度"]=(2*(targetdf.loc[targetdf["日期"]==lastday,"上涨比例均线均值"]-(dt_up+dt_down)/2)/(dt_up-dt_down))
targetdf.to_csv(f"{basepath}\刻度择时处理后.csv")
lastdf=targetdf[targetdf["日期"]>=datelist[-1]]
if (lastdf["上涨比例均线刻度"].values[0]>-0.5):
    trade=True
    print("持仓",lastdf["上涨比例均线刻度"].values[0])
else:
    trade=False
    print("空仓",lastdf["上涨比例均线刻度"].values[0])
print(trade)#这个是发送的是否持仓的信号