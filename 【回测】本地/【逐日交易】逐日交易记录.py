import pandas as pd
import numpy as np
import decimal
import os
import datetime
import matplotlib.pyplot as plt
# 设置参数
a=40 # 将数据划分成a个等距离的区间

from loguru import logger # pip install loguru # 这个框架可以解决中文不显示的问题
logger.add(
    sink=f"log.log",#sink: 创建日志文件的路径。
    level="INFO",#level: 记录日志的等级，低于这个等级的日志不会被记录。等级顺序为 debug < info < warning < error。设置 INFO 会让 logger.debug 的输出信息不被写入磁盘。
    rotation="00:00",#rotation: 轮换策略，此处代表每天凌晨创建新的日志文件进行日志 IO；也可以通过设置 "2 MB" 来指定 日志文件达到 2 MB 时进行轮换。   
    retention="7 days",#retention: 只保留 7 天。 
    compression="zip",#compression: 日志文件较大时会采用 zip 进行压缩。
    encoding="utf-8",#encoding: 编码方式
    enqueue=True,#enqueue: 队列 IO 模式，此模式下日志 IO 不会影响 python 主进程，建议开启。
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"#format: 定义日志字符串的样式，这个应该都能看懂。
)

basepath=r"C:\Users\13480\Desktop\quant\【回测】本地\数据文件"
# basepath=r"/home/wth000/gitee/quant/【回测】本地/数据文件"

# MAD:中位数去极值
def extreme_MAD(dt,n):
    median = dt.quantile(0.5) #找出中位数
    new_median = (abs((dt - median)).quantile(0.5)) #偏差值的中位数
    dt_up = median + n*new_median #上限
    dt_down = median - n*new_median #下限
    return dt_up,dt_down

# paths=[r"全体A股",r"半小时资金流",r"半小时量价"]
paths=[r"全体A股"]
for path in paths:
    if path==r"全体A股":
        timetarget="floattoday"
    elif path==r"半小时资金流": #文件夹路径
        timetarget="float价格分时"
    elif path==r"半小时量价": #文件夹路径
        timetarget="float价格分时"

    # tradetypes=["全部"]
    tradetypes=["小市值"]
    for tradetype in tradetypes:
        print("path",path,"tradetype",tradetype)
        df=pd.read_csv(f"{basepath}/{path}/{path}{tradetype}.csv")
        df=df.sort_values(by=timetarget) #以日期列为索引,避免计算错误

        # #第一次日期截取
        # datelist=df[timetarget].unique().tolist() # 获取观察周期的所有日期数据
        # testdays=700#只要最后testdays日期的数据
        # # testdays=len(datelist)#截取全部数据
        # print("日期截取前",len(df))
        # dateprediction=datelist[len(datelist)-testdays]
        # print("截取日期",dateprediction)
        # df=df[df[timetarget]>=dateprediction]
        # print("日期截取后",len(df))

        # 因子数据处理
        df["次日开盘"]=df.groupby("代码")["开盘"].shift(-1)
        df["次日真实开盘价格"]=df.groupby("代码")["真实开盘价格"].shift(-1)
        df["每股未分配利润"]=df["未分配利润"]/df["总股本"]
        df["股息率"]=df["股息率"]/100
        df["当年股息率"]=df["股息率"]
        # df["当年总分红"]=df["总市值"]*df["股息率"]
        df.sort_values(by=timetarget, inplace=True)#日期升序排序
        df["去年股息率"]=df.groupby("代码")["当年股息率"].shift(250)
        # df["去年总分红"]=df.groupby("代码")["当年总分红"].shift(250)
        # df["前年总分红"]=df.groupby("代码")["当年总分红"].shift(500)
        # df["两年总分红"]=df["当年总分红"]+df["去年总分红"]
        # df["股息率"]=df["两年总分红"]/df["总市值"]*100
        df["股息率"]=(df["当年股息率"]+df["去年股息率"])/2
        # df.to_csv("df.csv")
        
        #乖离率因子及其排名
        thiscolumns=["10日乖离率"]
        for mubiao in thiscolumns:
            df[f"{mubiao}处理前"]=df[mubiao]
            df.loc[df[mubiao]>=1.2,mubiao]=1.2
            df.loc[df[mubiao]<=0.8,mubiao]=0.8
            df[mubiao]=(df[mubiao]-1)*100
            df[mubiao]=abs(df[mubiao]-1.5)#标准化并且取绝对值
        for mubiao in thiscolumns:
            #处理后的因子排名
            df = df.dropna(subset=[mubiao])#去掉空值
            df[f"{mubiao}_rank"] = df.groupby(timetarget)[mubiao].rank(ascending=True)
            df[f"{mubiao}_rank_rate"] = df[f"{mubiao}_rank"] / len(df)
            
        # 第二次日期截取
        datelist=df[timetarget].unique().tolist() # 获取观察周期的所有日期数据
        testdays=200#只要最后testdays日期的数据
        # testdays=len(datelist)#截取全部数据
        print("日期截取前",len(df))
        dateprediction=datelist[len(datelist)-testdays]
        print("截取日期",dateprediction)
        df=df[df[timetarget]>=dateprediction]
        print("日期截取后",len(df))
        df = df.loc[:,~df.columns.str.contains('Unnamed')]#去掉包含Unnamed的列

        groupdf=df.groupby(timetarget,group_keys=False)
        #设置初始金额
        thismoney=1000000
        allpostions=pd.DataFrame({})
        allorders=pd.DataFrame({})
        import time
        import math
        for index,thisdf in groupdf:#分组之后就不用考虑.iterrows()去选择每一行的数据
            print(index)#日期
            logger.info(f"thisdf基本面筛选前,{thisdf},{type(thisdf)}")

            thisdf=thisdf[thisdf["归母净利润"]>0]#21年达标标的最小市值7-10亿元【小市值到这里还有数据】
            # thisdf=thisdf[thisdf["每股未分配利润"]>1]#每股未分配利润1元以上
            # thisdf=thisdf[thisdf["基本每股收益"]>0.1]#每股收益0.1元以上
            # thisdf=thisdf[thisdf["归母净利润季度增长率"]>0]
            # thisdf=thisdf[thisdf["净资产年度增长率"]>1]#百分比
            # thisdf=thisdf[thisdf["当年股息率"]>0]
            # thisdf=thisdf[thisdf["去年股息率"]>0]
            # thisdf=thisdf[thisdf["当年总分红"]>0]
            # thisdf=thisdf[thisdf["去年总分红"]>0]
            # thisdf=thisdf[thisdf["前年总分红"]>0]

            # thisdf=thisdf[~(thisdf["次日is_st"]==1)]
            # thisdf=thisdf[~(thisdf["次日is_paused"]==1)]
            
            #这里就已经没数据了
            logger.info(f"thisdf基本面筛选后,{thisdf},{type(thisdf)}")

            ranklist=["总市值"]
            if "全体A股" in path:
                newrank=["归母净利润","基本每股收益","归母净利润季度增长率","净资产年度增长率","股息率","每股未分配利润"]
                for rank in newrank:
                    ranklist.append(rank)
            print(ranklist)
            for mubiao in ranklist:
                # thisdf = thisdf.dropna(subset=[mubiao])#去掉空值
                thisdf[f"{mubiao}_rank"] = thisdf.groupby(timetarget)[mubiao].rank(ascending=True)
                thisdf[f"{mubiao}_rank_rate"] = thisdf[f"{mubiao}_rank"] / len(thisdf)
            if "全体A股" in path:
                thisdf["基本面打分"]=0
                for rank in newrank:
                    thisdf["基本面打分"]+=thisdf[f"{rank}_rank_rate"]
                mubiao="基本面打分"
                # thisdf[f"{mubiao}_rank"] = thisdf.groupby(timetarget)[mubiao].rank(ascending=True)
                thisdf[f"{mubiao}_rank"] = thisdf.groupby(timetarget)[mubiao].rank(ascending=False)#基本面打分越大越好
                thisdf[f"{mubiao}_rank_rate"] = thisdf[f"{mubiao}_rank"] / len(thisdf)

                thisdf["综合打分"]=thisdf["10日乖离率_rank_rate"]+thisdf["基本面打分_rank_rate"]+thisdf["总市值_rank_rate"]
                mubiao="综合打分"
                thisdf[f"{mubiao}_rank"] = thisdf.groupby(timetarget)[mubiao].rank(ascending=False)#基本面打分越大越好
                thisdf[f"{mubiao}_rank_rate"] = thisdf[f"{mubiao}_rank"] / len(thisdf)
                thisdf.to_csv(f"{index}thisdf.csv")
                logger.info(f"{index},thisdf,{thisdf}")
            stocknum=30#设置持仓数量
            dfone=thisdf.nsmallest(stocknum,"综合打分")
            dftwo=thisdf.nsmallest(stocknum*2,"综合打分")
            time.sleep(2)
            if allpostions.empty:
                premoney=thismoney/stocknum
                buydf=dfone.copy()
                buydf=buydf[~(buydf["次日开盘涨停"]==1)]
                selldf=dftwo.copy()
                buydf=buydf[~(buydf["次日开盘涨停"]==1)]
                
                buydf["建仓数量"]=buydf["次日开盘"].apply(lambda x:math.floor((premoney/x)/100)*100)
                buydf["建仓成本"]=buydf["次日开盘"]*buydf["建仓数量"]
                buydf["建仓时次日真实开盘价格"]=buydf["次日真实开盘价格"]
                buydf["建仓时次日开盘"]=buydf["次日开盘"]
                allpostions=buydf[["代码","建仓时次日真实开盘价格","建仓时次日开盘","建仓数量","建仓成本"]]
                
                canusemoney=thismoney-allpostions["建仓成本"].sum()
                allpostions["持仓金额"]=allpostions["建仓成本"].sum()
                allpostions["可用余额"]=canusemoney
                allpostions["建仓日期"]=index
                allorders=pd.concat([allorders,allpostions])

                buydf.to_csv(f"{index}buydf.csv")
                logger.info(f"{index},buy,buydf,{buydf}")
                selldf.to_csv(f"{index}selldf.csv")
                logger.info(f"{index},buy,selldf,{selldf}")
                allpostions.to_csv(f"{index}allpostions.csv")
                logger.info(f"{index},buy,allpostions,{allpostions}")
            else:
                buydf=dfone.copy()
                buydf=buydf[~(buydf["次日开盘涨停"]==1)]
                buydf=buydf[~(buydf["次日开盘跌停"]==1)]
                selldf=dftwo.copy()
                buydf=buydf[~(buydf["次日开盘涨停"]==1)]
                buydf=buydf[~(buydf["次日开盘跌停"]==1)]
                for symbol in allpostions["代码"].tolist():
                    if symbol not in selldf["代码"].tolist():
                        thispostion=allpostions[allpostions["代码"]==symbol]
                        thispostion.to_csv(f"{index}thispostion.csv")
                        logger.info(f"{index},sell,thispostion,{thispostion}")
                        thisselldf=thisdf[thisdf["代码"]==symbol]
                        thisselldf["清仓时次日真实开盘价格"]=thisselldf["次日真实开盘价格"]
                        thisselldf["清仓时次日开盘"]=thisselldf["次日开盘"]
                        thisorder=thisselldf[["代码","清仓时次日真实开盘价格","清仓时次日开盘"]]
                        thisorder["清仓日期"]=index
                        # thisorder.to_csv(f"{index}thisorder.csv")
                        # logger.info(f"{index},sell,thisorder,{thisorder}")

                        thisorder=thisorder.merge(thispostion,on="代码")
                        thisorder["收益率"]=thisorder["清仓时次日真实开盘价格"]/thisorder["建仓时次日真实开盘价格"]
                        thisorder["清仓收入"]=thisorder["建仓成本"]*thisorder["收益率"]
                        thisorder.to_csv(f"{index}thisorder.csv")
                        allpostions["持仓金额"]=allpostions["持仓金额"].values[0]-thisorder["建仓成本"].values[0]
                        allpostions["可用余额"]=allpostions["可用余额"].values[0]+thisorder["清仓收入"].values[0]
                        allpostions=allpostions[~(allpostions["代码"]==symbol)]#去掉已经卖出的标的
                        thisorder.to_csv(f"{index}thisorder.csv")
                        logger.info(f"{index},sell,thisorder,{thisorder}")
                        allpostions.to_csv(f"{index}allpostions.csv")
                        logger.info(f"{index},sell,allorders,{allpostions}")
                        allorders=pd.concat([allorders,allpostions])
                #计算上一轮之后实际总资产金额【为了跟实盘一致尽量实时统计当前的金额】
                thismoney=allpostions["持仓金额"].values[0]+allpostions["可用余额"].values[0]
                premoney=thismoney/stocknum
                for symbol in buydf["代码"].tolist():
                    if symbol not in allpostions["代码"].tolist():
                        if len(allpostions)>=stocknum:
                            break
                        else:
                            thisbuydf=buydf[buydf["代码"]==symbol]
                            thisbuydf["建仓数量"]=thisbuydf["次日开盘"].apply(lambda x:math.floor((premoney/x)/100)*100)
                            thisbuydf["建仓成本"]=thisbuydf["次日开盘"]*thisbuydf["建仓数量"]
                            thisbuydf["建仓时次日真实开盘价格"]=thisbuydf["次日真实开盘价格"]
                            thisbuydf["建仓时次日开盘"]=thisbuydf["次日开盘"]
                            thisorder=thisbuydf[["代码","建仓时次日真实开盘价格","建仓时次日开盘","建仓数量","建仓成本"]]
                            thisorder["建仓日期"]=index
                            allorders=pd.concat([allorders,allpostions])
                            allpostions=pd.concat([allpostions,thisorder])
                            allpostions["持仓金额"]=allpostions["持仓金额"].values[0]+thisorder["建仓成本"].values[0]
                            allpostions["可用余额"]=allpostions["可用余额"].values[0]-thisorder["建仓成本"].values[0]
            allpostions.to_csv(f"{index}allorders.csv")
            logger.info(f"{index},sell,allorders,{allorders}")
