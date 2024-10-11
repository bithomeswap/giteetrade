# coding=utf-8
# 这个策略执行的时候需要把运行文件放到指定位置执行，应该是有一些包需要调用
# python.exe -m pip install gm -i https://pypi.doubanio.com/simple
from __future__ import print_function, absolute_import, unicode_literals
from gm.api import *
import datetime
import pandas as pd
import math
import time

def symbol_convert(stock):#股票代码加后缀
    #北交所的股票8字开头，包括82、83、87、88，其中82开头的股票表示优先股；83和87开头的股票表示普通股票、88开头的股票表示公开发行的。
    if (stock.startswith("60"))or(#上交所主板
        stock.startswith("68"))or(#上交所科创板
        stock.startswith("11"))or(#上交所可转债
        (stock.startswith("51"))or(stock.startswith("56"))or(stock.startswith("58"))):#上交所ETF
        return "SHSE."+str(str(stock))
        # return str(str(stock)+".SS")
    elif (stock.startswith("00"))or(#深交所主板
        stock.startswith("30"))or(#深交所创业板
        stock.startswith("12"))or(#深交所可转债
        (stock.startswith("15"))):#深交所ETF
        return "SZSE."+str(str(stock))
    else:
        # print("不在后缀转换名录",str(stock))
        return str(str(stock))

def filter_kcb_stock(stocks):#过滤科创北交股票
    for stock in stocks[:]:#这里的5是第六位，算上引号的话就是第六位
        if stock[5]=="4" or stock[5]=="8" or stock[5:7]=="68":
            stocks.remove(stock)
    return stocks

# def on_tick(context,tick):
#     print(tick)

# basepath=r"C:\Users\13480\Desktop\quant\【本地选股（A股）】SDK\EMCSDK选股"
basepath=r"C:\Users\Admin\gitee\quant\【本地选股（A股）】SDK\EMCSDK选股"
def init(context):
    def choose_stocks(choosename,now,start_date,last_date,today,yesterday):
        if choosename=="打板":#A股中小板策略
            try:
                pd.read_csv(str(basepath)+str(today)+choosename+"买入.csv")
                print("******",str(basepath)+str(today)+choosename+"买入.csv"+"文件存在")
                pd.read_csv(str(basepath)+str(today)+choosename+"卖出.csv")
                print("******",str(basepath)+str(today)+choosename+"卖出.csv"+"文件存在")
            except Exception as e:
                print("******","******"+str(basepath)+str(today)+choosename+"买入.csv"+choosename+"卖出.csv"+"文件不同时存在")
                all_stock=get_instruments(exchanges="SHSE,SZSE",sec_types=[1],
                                        fields="symbol, listed_date, delisted_date",
                                        skip_suspended=True,#跳停牌
                                        # skip_st=True,#跳ST
                                        df=True)#这里还有一个前收和涨跌停，是根据当天的前收计算的当天涨跌停
                print(all_stock)
                #剔除停牌和st股和上市不足250日的新股和退市股和B股
                df=all_stock[
                    # (all_stock["listed_date"] < last_date)&(all_stock["delisted_date"] > start_date)
                                # & 
                                (all_stock["symbol"].str[5] != "9")
                                & (all_stock["symbol"].str[5] != "2")
                                & (all_stock["symbol"].str[5] != "4")#新三板或者北交所
                                & (all_stock["symbol"].str[5] != "8")#新三板或者北交所
                                & (all_stock["symbol"].str[5:7] != "68")#科创板
                                & (all_stock["symbol"].str[5:7] != "30")#创业板
                                ]
                stocks=df["symbol"].to_list()
                stocks=filter_kcb_stock(stocks)
                print(df)
                # symbol	str	标的代码
                # trade_date	datetime.datetime	交易日期
                # sec_level	int	1-正常,2-ST 股票,3-*ST 股票,4-股份转让,5-处于退市整理期的证券,6-上市开放基金LOF,7-交易型开放式指数基金(ETF),8-非交易型开放式基金(暂不交易,仅揭示基金净值及开放申购赎回业务),9-仅提供净值揭示服务的开放式基金;,10-仅在协议交易平台挂牌交易的证券,11-仅在固定收益平台挂牌交易的证券,12-风险警示产品,13-退市整理产品,99-其它
                # is_suspended	int	是否停牌. 1: 是, 0: 否
                # multiplier	float	合约乘数
                # margin_ratio	float	保证金比率
                # settle_price	float	结算价
                # pre_settle	float	昨结价
                # position	int	持仓量
                # pre_close	float	昨收价
                # upper_limit	float	涨停价 （可转债没有涨停价）
                # lower_limit	float	跌停价 （可转债没有跌停价）
                # adj_factor
                olddf=get_history_instruments(stocks,fields=["symbol","trade_date", 
                                                          "pre_settle","position","pre_close",
                                                          "upper_limit","lower_limit","adj_factor",
                ],start_date=(now-datetime.timedelta(days=30)).strftime("%Y%m%d"),end_date=today,df=True)#这里的涨跌停是前一天的收盘以及据此计算出来的当天的涨跌停价格
                olddf["trade_date"]=pd.to_datetime(olddf['trade_date']).dt.tz_convert('Asia/Shanghai').dt.strftime('%Y%m%d').astype(str)
                tradedaylist=olddf['trade_date'].unique()
                tradedaylist=sorted(tradedaylist, reverse=True)[1:5]
                olddf=olddf[olddf["trade_date"].isin(tradedaylist)]
                print("交易日列表",tradedaylist)
                olddf=olddf[["symbol","trade_date","upper_limit","lower_limit"]]
                olddf=olddf.rename(columns={"trade_date":"日期"})
                print("涨跌停处理",len(olddf))
                # pip install xcsc-tushare
                import xcsc_tushare as ts
                # ts.set_token('7ed61c98882a320cadce6481aef04ebf7853807179d45ee7f72089d7')
                # ts.pro_api(server='http://116.128.206.39:7172')   #指定tocken对应的环境变量，此处以生产为例
                pro = ts.pro_api('7ed61c98882a320cadce6481aef04ebf7853807179d45ee7f72089d7',server='http://116.128.206.39:7172')
                #通过日期取历史某一天的全部股票数据【这里可能日期不对，容易获取到交易日】
                df = pro.daily(trade_date=tradedaylist[0])
                df = df.rename(columns={"ts_code":"symbol","trade_date":"日期"})
                df["symbol"]=df["symbol"].str.replace(r'\D','',regex=True).astype(str)
                df["symbol"]=df["symbol"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
                print("昨日数据",len(df))
                df=df.merge(olddf,on=["日期","symbol"],how='inner')
                df["close"]=df["close"].astype(str)
                df["upper_limit"]=df["upper_limit"].astype(str)
                df=df[(df["close"]==df["upper_limit"])]
                stocks=df["symbol"].to_list()
                print("昨日涨停股票池",len(stocks))
                
                thisdf = pro.daily(trade_date=tradedaylist[1])#把成交量拼接到之前的上
                thisdf = thisdf.rename(columns={"ts_code":"symbol","trade_date":"日期"})
                thisdf["symbol"]=thisdf["symbol"].str.replace(r'\D','',regex=True).astype(str)
                thisdf["symbol"]=thisdf["symbol"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
                thisdf["涨停前日_volume"]=thisdf["volume"]
                thisdf=thisdf[["symbol","涨停前日_volume"]]
                df=df.merge(thisdf,on="symbol",how='inner')
                df=df[df["涨停前日_volume"]<(3*df["volume"])]
                stocks=df["symbol"].to_list()
                df.to_csv("去掉涨停前一天三倍量能的标的.csv")
                print("去掉涨停前一天三倍量能的标的",len(stocks))
                
                # 下一步是筛选概念，只做概念下首板数量最多的三个概念下的二板标的
                time.sleep(100)
                notstocks=pd.DataFrame({})
                for tradeday in tradedaylist:
                    thisdf = pro.daily(trade_date=tradeday)
                    thisdf = thisdf.rename(columns={"ts_code":"symbol","trade_date":"日期"})
                    thisdf["symbol"]=thisdf["symbol"].str.replace(r'\D','',regex=True).astype(str)
                    thisdf["symbol"]=thisdf["symbol"].apply(lambda x:symbol_convert(x)).astype(str)#需要指定类型为字符串
                    thisdf=thisdf.merge(olddf,on=["日期","symbol"],how='inner')
                    thisdf["close"]=thisdf["close"].astype(str)
                    thisdf["upper_limit"]=thisdf["upper_limit"].astype(str)
                    thisdf=thisdf[(thisdf["close"]==thisdf["upper_limit"])]
                    print("n日前涨停股票池",thisdf["symbol"].tolist())
                    notstocks=pd.concat([notstocks,thisdf])
                notstocks.to_csv("需要过滤的历史涨停标的.csv")
                df=df[(df["symbol"].isin(notstocks["symbol"].to_list()))]
                df.to_csv(str(basepath)+str(today)+choosename+"买入.csv")
                # df.to_csv(str(basepath)+str(today)+choosename+"卖出.csv")
                stocks=df["symbol"].to_list()
                print("去掉历史涨停之后",stocks)
                
                #获取实时tick
                # print(datetime.datetime.now())
                price_df=current(symbols=stocks)
                price_df=pd.DataFrame(price_df)
                price_df=price_df[price_df["price"]>4]
                price_df=price_df[["symbol","price"]]
                # price_df.to_csv("price_df.csv")
                stocks=price_df["symbol"].tolist()
                print(price_df)
                print(datetime.datetime.now())
                # #筛选净利润
                # olddf=get_fundamentals_n("prim_finance_indicator",stocks,now,fields=["NPCUT"],count=1,df=True)
                # olddf=olddf[olddf["NPCUT"]>0]#加上之后是3331只，不加是原始的4326
                # stocks=olddf["symbol"].tolist()
                # print(olddf)
                # 获取所有股票市值
                olddf=get_fundamentals_n("trading_derivative_indicator",stocks,now,fields=["TOTAL_SHARE"],count=1,df=True)
                olddf=olddf.rename(columns={"TOTAL_SHARE":"总股本"})
                print(olddf)
                olddf=olddf.merge(price_df,on="symbol",how="inner")
                olddf["总市值"]=olddf["总股本"]*olddf["price"]
                print(len(olddf))
                olddf=olddf[(olddf["总市值"]>20*(10**8))&(olddf["总市值"]<100*(10**8))]
                olddf.to_csv(str(basepath)+str(today)+choosename+"买入.csv")
                olddf.to_csv(str(basepath)+str(today)+choosename+"卖出.csv")
                print(len(olddf))

        if choosename=="微盘股":#A股中小板策略
            try:
                pd.read_csv(str(basepath)+str(today)+choosename+"买入.csv")
                print("******",str(basepath)+str(today)+choosename+"买入.csv"+"文件存在")
                pd.read_csv(str(basepath)+str(today)+choosename+"卖出.csv")
                print("******",str(basepath)+str(today)+choosename+"卖出.csv"+"文件存在")
            except Exception as e:
                print("******","******"+str(basepath)+str(today)+choosename+"买入.csv"+choosename+"卖出.csv"+"文件不同时存在")
                # SEC_TYPE_STOCK=1                          # 股票
                # SEC_TYPE_FUND=2                           # 基金
                # SEC_TYPE_INDEX=3                          # 指数
                # SEC_TYPE_FUTURE=4                         # 期货
                # SEC_TYPE_OPTION=5                         # 期权
                # SEC_TYPE_CREDIT=6                         # 信用交易
                # SEC_TYPE_BOND=7                           # 债券
                # SEC_TYPE_BOND_CONVERTIBLE=8               # 可转债
                # SEC_TYPE_CONFUTURE=10                     # 虚拟合约
                all_stock=get_instruments(exchanges="SHSE,SZSE",sec_types=[1],
                                            fields="symbol, listed_date, delisted_date",
                                            skip_suspended=True,#跳停牌
                                            skip_st=True,#跳ST
                                            df=True)
                print(all_stock)
                #剔除停牌和st股和上市不足250日的新股和退市股和B股
                df=all_stock[(all_stock["listed_date"] < last_date)
                                & (all_stock["delisted_date"] > start_date)
                                & (all_stock["symbol"].str[5] != "9")
                                & (all_stock["symbol"].str[5] != "2")
                                & (all_stock["symbol"].str[5] != "4")#新三板或者北交所
                                & (all_stock["symbol"].str[5] != "8")#新三板或者北交所
                                & (all_stock["symbol"].str[5:7] != "68")#科创板
                                ]
                stocks=df["symbol"].to_list()
                print(df)
                #获取实时tick
                # print(datetime.datetime.now())
                price_df=current(symbols=stocks)
                price_df=pd.DataFrame(price_df)
                price_df=price_df[price_df["price"]>4]
                price_df=price_df[["symbol","price"]]
                # price_df.to_csv("price_df.csv")
                stocks=price_df["symbol"].tolist()
                print(price_df)
                print(datetime.datetime.now())
                #筛选净利润
                olddf=get_fundamentals_n("prim_finance_indicator",stocks,now,fields=["NPCUT"],count=1,df=True)
                olddf=olddf[olddf["NPCUT"]>0]#加上之后是3331只，不加是原始的4326
                stocks=olddf["symbol"].tolist()
                print(olddf)
                # 获取所有股票市值
                olddf=get_fundamentals_n("trading_derivative_indicator",stocks,now,fields=["TOTAL_SHARE"],count=1,df=True)
                olddf=olddf.rename(columns={"TOTAL_SHARE":"总股本"})
                print(olddf)
                olddf=olddf.merge(price_df,on="symbol",how="inner")
                olddf["总市值"]=olddf["总股本"]*olddf["price"]
                # print(olddf)
                olddf["排名"]=olddf["总市值"].rank(method="max", ascending=True,na_option='bottom')
                olddf=olddf.drop(columns=['end_date',"pub_date"])#datetime格式的数据不能输出csv
                olddf=olddf.rename(columns={"symbol":"代码"})#datetime格式的数据不能输出csv
                olddf["代码"]=olddf["代码"].astype(str)
                numbuystock=5#设置持仓数量
                dfone=olddf.nsmallest(math.ceil(numbuystock),"总市值")
                dftwo=olddf.nsmallest(math.ceil(1.5*numbuystock),"总市值")
                print(dfone,dfone)
                
                dftwo.to_csv(str(basepath)+str(today)+choosename+"卖出.csv")
                dfone.to_csv(str(basepath)+str(today)+choosename+"买入.csv")
                buylisttwo=dftwo["代码"].values
                buylistone=dfone["代码"].values
                print("******",buylistone,buylisttwo)
                
    now=datetime.datetime.now()
    start_date=now.strftime("%Y-%m-%d %H:%M:%S")#测试当天的数据
    last_date=(now-datetime.timedelta(days=250)).strftime("%Y-%m-%d %H:%M:%S")
    # 获取交易日期，上交所SHSE，深交所SZSE，ID
    tradelist=get_trading_dates(exchange="SZSE",start_date=str(last_date),end_date=str(start_date))
    print(tradelist)
    today=tradelist[-1]
    print(today)
    yesterday=tradelist[-2]
    print(yesterday)
    print("******","today",today,"yesterday",yesterday)
    
    # 获取当前所有仓位
    # account_id="5326420"
    # account_id="510100031083"#设置账户ID
    # account_id="627e4104-d835-11ee-9c8b-52560acd7da0"#7*24小时测试
    account_id="80602109-d842-11ee-9c8b-52560acd7da0"#7*24小时测试
    #设置交易参数并且获取买卖计划
    bidrate=0.005#设置盘口价差为0.004
    timecancellwait=60#设置撤单函数筛选订单的确认时间
    timetickwait=60#设置每次下单时确认是否是最新tick的确认时间【tick时间可能在60秒不是很快，3秒一根但是返回的速度不够快】
    timeseconds=40#设置获取tick的函数的时间长度【避免没有数据】

    targetmoney=20000#设置下单时对手盘需要达到的厚度（即单笔目标下单金额，因为手数需要向下取整，所以实际金额比这个值低）
    traderate=2#设置单次挂单金额是targetmoney的traderate倍
    cancellorder=False#取消一分钟不成交或者已成交金额达到目标值自动撤单并回补撤单金额的任务
    # cancellorder=True#设置一分钟不成交或者已成交金额达到目标值自动撤单并回补撤单金额的任务

    if (account_id=='627e4104-d835-11ee-9c8b-52560acd7da0'):
        choosename="微盘股"
        # tradeway="taker"#设置主动吃单
        tradeway="maker"#设置被动吃单
    if (account_id=='80602109-d842-11ee-9c8b-52560acd7da0'):
        choosename="打板"
        # tradeway="taker"#设置主动吃单
        tradeway="maker"#设置被动吃单
    print(now,choosename,account_id,start_date,last_date,today,yesterday)
    choose_stocks(choosename,now,start_date,last_date,today,yesterday)#使用特定函数根据策略名称配置相应参数

    buyfilename=choosename+"买入.csv"
    sellfilename=choosename+"卖出.csv"
    print(buyfilename,sellfilename)
    buydf=pd.read_csv(str(basepath)+str(today)+buyfilename)
    selldf=pd.read_csv(str(basepath)+str(today)+sellfilename)

    #确认买入数量【即持仓数量】
    targetnum=len(buydf)
    print("预计持仓只数",targetnum)
    
    # 平不在标的池的仓位
    positions=get_position(account_id)
    for position in positions:
        symbol=position["symbol"]
        if symbol not in selldf["代码"].tolist():
            order=order_target_percent(symbol=symbol,percent=0,order_type=OrderType_Market,position_side=PositionSide_Long,account=account_id)
            print("市价单平不在标的池的",symbol,order)
    #获取持仓
    dfpositions=pd.DataFrame({})
    positions=get_position(account_id)
    for position in positions:
        symbol=position["symbol"]
        thispostion=pd.DataFrame({"symbol":[position["symbol"]],
                                  "volume":[position["volume"]],
                                  "volume_today":[position["volume_today"]],
                                  "market_value":[position["market_value"]],
                                  "amount":[position["amount"]],
                                  "vwap":[position["vwap"]],
                                  "price":[position["price"]],
                                  "available":[position["available"]],
                                  "available_today":[position["available_today"]],
                                  })
        dfpositions=pd.concat([dfpositions,thispostion])
    cash=get_cash(account_id)
    frozencash=cash.frozen
    availablecash=cash.available
    allcash=cash.nav
    print(frozencash,availablecash,allcash)
    buydf=buydf[~(buydf["代码"].isin(dfpositions["symbol"].tolist()))]
    if not buydf.empty:
        tradenum=len(buydf)
        prevalue=availablecash/tradenum
        # 买需要买入的标的
        for symbol in buydf["代码"].tolist():
            tick=current(symbols=[symbol])
            tick=tick[0]
            bid_price_1=tick["quotes"][0]["bid_p"]
            bid_volume_1=tick["quotes"][0]["bid_v"]
            bid_price_2=tick["quotes"][1]["bid_p"]
            bid_volume_2=tick["quotes"][1]["bid_v"]
            ask_price_1=tick["quotes"][0]["ask_p"]
            ask_volume_1=tick["quotes"][0]["ask_v"]
            ask_price_2=tick["quotes"][1]["ask_p"]
            ask_volume_2=tick["quotes"][1]["ask_v"]
            print(bid_price_1,bid_volume_1,bid_price_2,bid_volume_2)
            # [{'quotes': [{'bid_p': 14.3, 'bid_v': 33900, 'ask_p': 14.31, 'ask_v': 3200}, {'bid_p': 14.29, 'bid_v': 5000, 'ask_p': 14.32, 'ask_v': 11000}, {'bid_p': 14.28, 'bid_v': 1600, 'ask_p': 14.33, 'ask_v': 500}, {'bid_p': 14.27, 'bid_v': 1400, 'ask_p': 14.34, 'ask_v': 1700}, {'bid_p': 14.26, 'bid_v': 1800, 'ask_p': 14.35, 'ask_v': 10400}], 'cum_volume': 2532906, 'cum_amount': 35984017.26, 'trade_type': 8, 'created_at': datetime.datetime(2024, 3, 1, 15, 4, 51, tzinfo=tzfile('PRC'))}]
            print("tick",tick)
            order=order_target_value(symbol=symbol,value=prevalue,price=0,order_type=OrderType_Market,position_side=PositionSide_Long,account=account_id)
            print(symbol,"以市价单调整至金额",prevalue,order)
    else:
        print("无需建仓")
        
if __name__ == "__main__":
    """
    strategy_id策略ID,由系统生成
    filename文件名,请与本文件名保持一致
    mode实时模式:MODE_LIVE回测模式:MODE_BACKTEST
    token绑定计算机的ID,可在系统设置-密钥管理中生成
    backtest_start_time回测开始时间
    backtest_end_time回测结束时间
    backtest_adjust股票复权方式不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
    backtest_initial_cash回测初始资金
    backtest_commission_ratio回测佣金比例
    backtest_slippage_ratio回测滑点比例
    """
    run(
        # token="ea0688371610c5fe4fe5cc8331d9eedf472c00de",##用户标识，跟账户ID不是一个东西，这个是7*24小时的
        token="2e9baa9b1b0ad52034ff4662223510fd4797a17b",#用户标识
        filename="EMCSDK选股.py",#策略文件名称
        # mode策略模式,MODE_LIVE(实时)=1,MODE_BACKTEST(回测) =2
        mode=MODE_LIVE,
        # mode=MODE_BACKTEST,
        # strategy_id="95a9ca90-d76e-11ee-baf9-00e04c57861f",#策略id
        # backtest_start_time="2005-01-01 08:00:00",#回测开始时间(%Y-%m-%d %H:%M:%S格式)
        # backtest_end_time="2020-10-01 16:00:00",#回测开始时间(%Y-%m-%d %H:%M:%S格式)
        # backtest_adjust=ADJUST_PREV,#回测复权方式(默认不复权)
        # ADJUST_NONE(不复权)=0
        # ADJUST_PREV(前复权)=1
        # ADJUST_POST(后复权)=2
        # backtest_initial_cash=1000000,#回测初始资金, 默认1000000
        # backtest_commission_ratio=0.0001,#回测佣金比例, 默认0
        # backtest_slippage_ratio=0.0001,#回测滑点比例, 默认0
        )
