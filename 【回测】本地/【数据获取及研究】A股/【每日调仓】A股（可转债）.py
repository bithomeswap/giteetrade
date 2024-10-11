import pandas as pd
import numpy as np
import math
import time
import os
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

#import psutil #调整内存占用
##获取当前进程的内存占用情况
#process=psutil.Process()
#memory_info=process.memory_info()
##打印内存占用信息
#print("内存占用：")
#print(f"物理内存占用：{memory_info.rss/(1024**2)} MB")
#print(f"虚拟内存占用：{memory_info.vms/(1024**2)} MB")

# path=r"概念" #文件夹路径
# #数据拼接【概念】
# all_files=os.listdir(f"{basepath}/{path}") #获取文件夹中的所有文件名
# alldf=pd.DataFrame({})
# num=0
# for filename in all_files:
#     num+=1
#     if (filename.endswith(".csv")): #只处理以 .csv 结尾的文件、
#         if ("all" not in filename)and(
#                             filename!=f"{path}.csv")and(
#                             filename!=f"{path}小市值.csv")and(
#                             filename!=f"{path}全部.csv"):
#             print(filename)
#             file_path=os.path.join(f"{basepath}/{path}",filename) #构建文件的完整路径
#             df=pd.read_csv(file_path) #读取 csv 文件
#             alldf=pd.concat([df,alldf])
# alldf.to_csv(f"{basepath}/{path}/{path}.csv")

# #所有概念列表
# df=pd.read_csv(f"{basepath}/{path}/{path}.csv")
# import ast
# df["概念名称"] = df["概念名称"].apply(ast.literal_eval)
# unique_gainian = list(set([sub for sublist in df["概念名称"].tolist() for sub in sublist]))
# print(unique_gainian,len(unique_gainian),type(unique_gainian))

#成分股提取
# for gainian in unique_gainian:
#     result_df=pd.DataFrame({"概念名称":gainian,"成分股":""})
#     if not os.path.exists(f"{basepath}/概念成分股"):
#         os.makedirs(f"{basepath}/概念成分股")
#     result_df.round(decimals=6).to_csv(f"{basepath}/概念成分股/概念成分股分布.csv")
#     print("任务已经完成")

# path=r"全体A股备份" #文件夹路径【专门用来获取历史数据的】
path=r"全体A股" #文件夹路径
# # path=r"可转债" #文件夹路径
timetarget="floattoday"

# path=r"分时" #文件夹路径
# timetarget="float价格分时"

if "可转债" in path:
    holdnum=30#设置持仓数量【加上这个极值处理之后，无论持仓数量多少，效果都有的提高】
if "全体A股" in path:
    holdnum=30#设置持仓数量【加上这个极值处理之后，无论持仓数量多少，效果都有的提高】
if "分时" in path:
    holdnum=30#设置持仓数量【加上这个极值处理之后，无论持仓数量多少，效果都有的提高】
thiscangwei="其他"
direction="long"

##是否重新计算数据
newtrade="数据处理"
# newtrade="收益计算"
# newtrade="聚宽格式"

##选择小市值还是全部
# tradetype="小市值"
tradetype="全部"
# tradetype="涨停"
# tradetype="跌停"

def technology(df): #定义计算技术指标的函数
    try:
        df=df.sort_values(by=timetarget) #以日期列为索引,避免计算错误
        #df=df.sort_values(by=timetarget,ascending=False) #从大到小排序

        window_size=20
        df[f'{window_size}日量价相关性系数均值']=df['量价相关性系数'].rolling(window=window_size).mean()
        df[f'{window_size}日量价相关性系数标准差']=df['量价相关性系数'].rolling(window=window_size).std()

        df["target_stock"]=(df["真实开盘价格"].shift(-1-1)/(df["真实开盘价格"].shift(-1)))-1
        for holddays in [1,3,5,7,10]:
            df[f"target_stock{holddays}"]=(df["真实开盘价格"].copy().shift(-holddays-1)/(df["真实开盘价格"].shift(-1).copy()))-1

        # #根据复权因子，其实可以推断未来的实际涨幅
        # df[f"换手率均值"]=df["换手率"].rolling(40).mean()
        # df[f"换手率比值"]=df["换手率"]/df["换手率均值"]

        df.loc[df["开盘涨停"].shift(-1)==1,"次日开盘涨停"]=1
        df.loc[df["开盘跌停"].shift(-1)==1,"次日开盘跌停"]=1
        df.loc[df["收盘涨停"].shift(-1)==1,"次日收盘涨停"]=1
        df.loc[df["收盘跌停"].shift(-1)==1,"次日收盘跌停"]=1

        df.loc[df["开盘涨停"].shift(1)==1,"昨日开盘涨停"]=1
        df.loc[df["开盘跌停"].shift(1)==1,"昨日开盘跌停"]=1
        df.loc[df["收盘涨停"].shift(1)==1,"昨日收盘涨停"]=1
        df.loc[df["收盘跌停"].shift(1)==1,"昨日收盘跌停"]=1
        
        if "全体A股" in path:
            df.loc[df["is_st"].shift(-1)==1,"次日is_st"]=1
        df.loc[df["is_paused"].shift(-1)==1,"次日is_paused"]=1
        if "可转债" not in path:
            window_size=3
            df[f"{window_size}日最高价格"]=df["真实最高价格"].rolling(window=window_size).max()
            df[f"{window_size}日次日开盘价格与最高价格比值"]=df["真实开盘价格"].shift(-1)/df[f"{window_size}日最高价格"]
            
            window_size=10
            df[f"{window_size}日均线"]=df["真实收盘价格"].rolling(window=window_size).mean()
            df[f"{window_size}日乖离率"]=df["真实收盘价格"]/df[f"{window_size}日均线"]
            df[f"{window_size}日乖离率均线"]=df[f"{window_size}日乖离率"].rolling(window=window_size).mean()
            df[f"{window_size}日乖离率均线乖离率"]=df[f"{window_size}日乖离率"]/df[f"{window_size}日乖离率均线"]

            window_size=20
            df["隔日涨幅ABS"]=abs(df["隔日涨幅"]-1)
            df["隔日涨幅ABS归一化"]=df["隔日涨幅ABS"]
            df.loc[(df["隔日涨幅ABS归一化"]>0.1),"隔日涨幅ABS归一化"]=0.1
            # df["累积隔日涨幅"]=df["真实开盘价格"].shift(window_size)/df["真实开盘价格"].shift(-1)-1
            df["累积隔日涨幅"]=df["真实开盘价格"].shift(window_size)/df["真实收盘价格"]-1#shift没有参数window
            df["累积隔日涨幅ABS"]=df[f"隔日涨幅ABS"].rolling(window=window_size).sum()
            df["累积隔日涨幅ABS归一化"]=df[f"隔日涨幅ABS归一化"].rolling(window=window_size).sum()
            df["趋势强度"]=df["累积隔日涨幅"]/df["累积隔日涨幅ABS"]
            # window_size=300
            # df[f"{window_size}日均线"]=df["真实收盘价格"].rolling(window=window_size).mean()
            # df[f"{window_size}日乖离率"]=df["真实收盘价格"]/df[f"{window_size}日均线"]

            # #3日平均涨跌幅
            # df[f"3日平均隔日涨幅"]=df["隔日涨幅"].rolling(window=3).mean()
        df=df.iloc[300:]
    except Exception as e:
        print(f"发生bug: {e}")
    return df

def stocktechnology(df): #定义计算股性指标的函数【可能不对】
    try:
        df=df.sort_values(by=timetarget) #以日期列为索引,避免计算错误
        window_size=100#百日
        # for columns in ["涨停","跌停","上涨","下跌"]:
        for columns in ["涨停","跌停"]:
            df[f"{columns}溢价"]=df[columns]*df["开盘涨幅"]#不能减一，因为有的数据是0
            df[f"{window_size}日{columns}次数"]=df[columns].rolling(window=window_size).sum().fillna(0)
            df[f"{window_size}日{columns}平均溢价"]=df[f"{columns}溢价"].rolling(window=window_size).sum().fillna(0)/df[f"{window_size}日{columns}次数"].where(df[f"{window_size}日{columns}次数"]==0,1)
        if "分时" not in path:
            for columns in ["换手率","隔日涨幅","日内涨幅","日内振幅","10日乖离率"]:
                df[f"{window_size}日平均{columns}"]=df[f"{columns}"].rolling(window=window_size).mean()
                df[f'RollingStd{columns}'] = np.log(df[columns]).rolling(window=window_size).std()# 计算因子值的对数收益率并使用rolling函数计算过去100天的滚动标准差
                df[f'{window_size}日年化波动率{columns}'] = df[f'RollingStd{columns}']*np.sqrt(252)# 用标准差乘以时间因子（假设一年有252个交易日，则时间因子就是252的平方根），就是年化滚动标准差
        # df=df.iloc[100:]
    except Exception as e:
        print(f"发生bug: {e}")
    return df

if newtrade=="数据处理":
    #数据拼接
    all_files=os.listdir(f"{basepath}/{path}") #获取文件夹中的所有文件名
    # alldf=pd.DataFrame({})
    # num=0
    # for filename in all_files:
    #     num+=1
    #     if (filename.endswith(".csv")): #只处理以 .csv 结尾的文件、
    #         if ("all" not in filename)and(
    #                             filename!=f"{path}.csv")and(
    #                             filename!=f"{path}小市值.csv")and(
    #                             filename!=f"{path}大市值.csv")and(
    #                             filename!=f"{path}涨停.csv")and(
    #                             filename!=f"{path}跌停.csv")and(
    #                             filename!=f"{path}全部.csv"):
    #             print(filename)
    #             file_path=os.path.join(f"{basepath}/{path}",filename) #构建文件的完整路径
    #             # 尝试不同的编码方式来读取 CSV 文件【有一些列类型错误，需要指定解码方式】
    #             try:
    #                 df = pd.read_csv(file_path, encoding='utf-8')
    #             except UnicodeDecodeError:
    #                 # 如果 utf-8 解码失败，尝试其他常见的编码方式
    #                 try:
    #                     df = pd.read_csv(file_path, encoding='gbk')
    #                 except UnicodeDecodeError:
    #                     # 如果其他编码方式也不行，你可以尝试使用 ISO-8859-1 编码【这个界面】
    #                     df = pd.read_csv(file_path, encoding='ISO-8859-1')
    #             if not alldf.empty:#只保留df当中之前没有过的日期的数据
    #                 df=df[~(df[timetarget].isin(alldf[timetarget].tolist()))]
    #             alldf=pd.concat([df,alldf])
    # alldf=alldf.sort_values(by=timetarget) #以日期列为索引排序,避免计算错误
    # alldf.to_csv(f"{basepath}/{path}/{path}.csv")
    # print("拼接完成")

    # 执行任务
    df=pd.read_csv(f"{basepath}/{path}/{path}.csv")#按说是对的
    # df=pd.read_csv(rf"C:\Users\13480\Desktop\quant\【回测】本地\数据文件\全体A股\__全体A股全体A股20140926.0_回测环境dt.csv")
    # if "分时"in path:#这个在获取数据的时候处理了
    #     df["float价格分时"]=df["价格分时"].str.replace(r'\D','',regex=True).astype(float)
    #     print(df["float价格分时"][0])
    df["真实收盘价格"]=df["close"]*df["factor"]
    df["真实开盘价格"]=df["open"]*df["factor"]
    df["真实最高价格"]=df["high"]*df["factor"]
    df["真实最高价格"]=df["low"]*df["factor"]
    df.loc[df["open"]==df["high_limit"],"开盘涨停"]=1
    df.loc[df["open"]==df["low_limit"],"开盘跌停"]=1
    df.loc[df["close"]==df["high_limit"],"收盘涨停"]=1
    df.loc[df["close"]==df["low_limit"],"收盘跌停"]=1

    df=df.rename(columns={"prev_close":"前收",
                            "high":"最高",
                            "low":"最低",
                            "close":"收盘",
                            "open":"开盘",
                            "turnover":"成交额",
                            "volume":"成交量",
                            })
    if "可转债" in path:
        df["可转债总市值"]=df["可转债总市值"]*1000000
        df["换手率"]=(df["成交额"]/df["可转债总市值"])
        df["总市值"]=df["可转债总市值"]
    if "全体A股" in path:
        # df["总市值"]=df["收盘"]*df["总股本"]
        df["总市值"]=df["开盘"]*df["总股本"]
        df["换手率"]=df["成交量"]/df["总股本"]
        # df["换手率"]=df["成交量"]/df["流通股本"]
    if "分时" in path:
        # df["总市值"]=df["收盘"]*df["总股本"]
        df["总市值"]=df["开盘"]*df["总股本"]
        df["换手率"]=df["成交量"]/df["总股本"]
        # df["换手率"]=df["成交量"]/df["流通股本"]
    if "分时" not in path:
        df["收盘均价比"]=df["收盘"]/df["avg_price"]
        df["开盘涨幅"]=df["开盘"]/df["前收"] #填写涨幅数据【隔夜】
        df["隔日涨幅"]=df["收盘"]/df["前收"] #填写涨幅数据【隔夜】
    df["日内涨幅"]=df["收盘"]/df["开盘"]
    df["日内振幅"]=(df["最高"]-df["最低"])/df["收盘"] #3.874781
    df=df.groupby("代码",group_keys=False).apply(technology) #计算复权因子
    print("复权因子计算后",len(df))

    if ("全体A股" in path)or("分时" in path):
        #择时指标
        df["涨停"] = np.where(df["收盘"] == df["high_limit"],1,0)
        df["跌停"] = np.where(df["收盘"] == df["low_limit"],1,0)
        if "全体A股" in path:
            df["上涨"] = np.where(df["收盘"]>df["前收"],1,0)
            df["下跌"] = np.where(df["收盘"]<df["前收"],1,0)
            df=df.groupby("代码",group_keys=False).apply(stocktechnology)#计算股性相关数据
        else:
            df["上涨"]=np.where(df["收盘"]>df["开盘"],1,0)
            df["下跌"]=np.where(df["收盘"]<df["开盘"],1,0)

        print("全市场的动态指标计算完毕")
        try:#有的里面没有这个数据
        #     #庄家行为
        #     df["总主动卖出庄家金额"]=df["主动卖出特大单金额"]+df["主动卖出大单金额"]
        #     df["总被动卖出庄家金额"]=df["被动卖出特大单金额"]+df["被动卖出大单金额"]
        #     df["总主动买入庄家金额"]=df["主动买入特大单金额"]+df["主动买入大单金额"]
        #     df["总被动买入庄家金额"]=df["被动买入特大单金额"]+df["被动买入大单金额"]
        #     df["总卖出庄家金额"]=df["总主动卖出庄家金额"]+df["总被动卖出庄家金额"]
        #     df["总买入庄家金额"]=df["总主动买入庄家金额"]+df["总被动买入庄家金额"]
        #     df["净流入庄家金额"]=df["总买入庄家金额"]-df["总卖出庄家金额"]
        #     df["净流入庄家金额成交额比"]=df["净流入庄家金额"]/df["成交额"]
            #过滤垃圾股
            df=df[df["代码"].str.startswith(("60","00","30"))]#只要沪深主板创业板
        except Exception as e:
            print(e)

    newdf=df.copy()
    newdf.to_csv(f"{basepath}/{path}/{path}全部.csv")
    print("全部已经输出")
    newdf=df.copy().groupby(timetarget,group_keys=False).apply(lambda x: x.nsmallest(400,"总市值"))#【竞价涨幅低的一般会盈利1.33（扣完手续费1.04）】50只就1.06
    newdf.to_csv(f"{basepath}/{path}/{path}小市值.csv")
    print("小市值已经输出")
    newdf=df.copy().groupby(timetarget,group_keys=False).apply(lambda x: x.nlargest(400,"总市值"))#【竞价涨幅低的一般会盈利1.33（扣完手续费1.04）】50只就1.06
    newdf.to_csv(f"{basepath}/{path}/{path}大市值.csv")
    print("大市值已经输出")
    if "全体A股" in path:
        newdf=df.copy()[df["收盘涨停"]==1]
        newdf.to_csv(f"{basepath}/{path}/{path}涨停.csv")
        newdf=df.copy()[df["收盘跌停"]==1]
        newdf.to_csv(f"{basepath}/{path}/{path}跌停.csv")
    elif "分时" in path:
        newdf=df.copy()[df["收盘涨停"]==1]
        newdf.to_csv(f"{basepath}/{path}/{path}涨停.csv")
        newdf=df.copy()[df["收盘跌停"]==1]
        newdf.to_csv(f"{basepath}/{path}/{path}跌停.csv")
    print("涨停跌停已经输出")
else:
    pass
if newtrade=="收益计算":
    df=pd.read_csv(f"{basepath}/{path}/{path}{tradetype}.csv")
    df=df.sort_values(by=timetarget) #以日期列为索引,避免计算错误
    # # 日期截取
    # datelist=df[timetarget].unique().tolist() # 获取观察周期的所有日期数据
    # # testdays=1500#只要最后testdays日期的数据
    # testdays=len(datelist)#截取全部数据
    # print("日期截取前",len(df))
    # dateprediction=datelist[len(datelist)-testdays]
    # print("截取日期",dateprediction)
    # df=df[df[timetarget]>=dateprediction]
    # print("日期截取后",len(df))
    
    if "可转债" in path:
        # df=df[~(df["次日is_st"]==1)]
        df=df[~(df["次日is_paused"]==1)]
        # df=df[~(df["次日开盘涨停"]==1)]

        # df=df[df["收盘"]<150]
        # df["当前日期"]=df[timetarget].astype(int).astype(str)
        # df["当前日期"]=pd.to_datetime(df["当前日期"])
        # df["end_date"]=pd.to_datetime(df["end_date"])
        # df["转债余额变更日"]=pd.to_datetime(df["转债余额变更日"])
        # df=df[(df["end_date"]-df["当前日期"])>pd.Timedelta(days=180)]

        df["总市值"]=df["三低指数"] #针对可转债【三低指数=转股溢价率*总市值】
        # df.loc[(df["转股溢价率"]>1.2),"总市值"]*=1.5 # 针对溢价率高的标的进行加权
        # df.loc[(df["隔日涨幅"]>1.08),"总市值"]*=df["隔日涨幅"]
    if "全体A股" in path:
        # df=df[~(df["is_st"]==1)]
        # df=df[~(df["is_paused"]==1)]
        # df=df[~(df["开盘涨停"]==1)]
        df=df[~(df["次日is_st"]==1)]
        df=df[~(df["次日is_paused"]==1)]
        df=df[~(df["次日开盘涨停"]==1)]
        # #过滤垃圾股
        df=df[df["代码"].str.startswith(("60","00","30"))]#只要沪深主板创业板
        # df=df[df["开盘"]>4]
        # df=df[df["归母净利润"]>0]
    print("过滤非主板创业板之后",len(df))

    if "分时" not in path:
        # # 分阶段选股【设置持仓数量】
        # # df["收盘均价比_rank"]=df.groupby(timetarget)["收盘均价比"].rank(ascending=True)
        # # df["因子值"]=df["收盘均价比_rank"]
        df["累积隔日涨幅ABS_rank"]=df.groupby(timetarget)["累积隔日涨幅ABS"].rank(ascending=True)
        df["因子值"]=df["累积隔日涨幅ABS_rank"]
        # df["因子值"]=df["总市值"]
        # # df=df.groupby(timetarget,group_keys=False).apply(lambda x: x.nsmallest(2000,"因子值"))
        # df=df.groupby(timetarget,group_keys=False).apply(lambda x: x.nsmallest(holdnum,"因子值"))
        
        df["权重"]=df["累积隔日涨幅ABS_rank"]#进行挡位处理
        print("权重赋值之后",len(df))
        
    #初始化权重
    if thiscangwei=="分级靠档模式":
        df["权重"]=1
        print(thiscangwei)
        #分级靠档模式【三档制，股票数量较多的时候这样相对稳定一些】
        #df["因子值排名"]=df.groupby(timetarget,group_keys=False)["因子值"].rank(ascending=False)#从大到小排序
        df["因子值排名"]=df.groupby(timetarget,group_keys=False)["因子值"].rank(ascending=True)#从小到大排序
        maxvalue=df["因子值排名"].max()
        print("挡位划分最大值",maxvalue)
        allnum=3 #设置总挡位数【为allnum-1】档位越高越好
        for thinum in range(1,allnum):
            if thinum==1:
                newdf=df.loc[(df["因子值排名"]<=math.ceil(maxvalue*((thinum)/(allnum-1)))),"挡位值"]=allnum-thinum
            elif thinum==allnum-1:
                newdf=df.loc[(df["因子值排名"]>=math.ceil(maxvalue*((thinum-1)/(allnum-1)))),"挡位值"]=allnum-thinum
            elif (thinum>1)and(thinum<(allnum-1)):
                newdf=df.loc[((df["因子值排名"]>=math.ceil(maxvalue*((thinum-1)/(allnum-1))))&(df["因子值排名"]<=math.ceil(maxvalue*((thinum)/(allnum-1))))),"挡位值"]=allnum-thinum
        df["挡位值之和"]=df.groupby(timetarget,group_keys=False)["挡位值"].transform(lambda x: x.sum())
        #df["权重因子"]=(df["挡位值之和"]-df["挡位值"])/df["挡位值之和"]#这个是值越小的权重越高
        df["权重因子"]=(df["挡位值"])/df["挡位值之和"]#这个是值越大的权重越低
        df["权重因子和"]=df.groupby(timetarget,group_keys=False)["权重因子"].transform(lambda x: x.sum())
        df["权重"]=df["权重因子"]/df["权重因子和"]#进行挡位处理
        print("权重",df["权重"])
    else:
        print(thiscangwei)


    cost=0.001  #设置交易滑点及手续费【平时设置为0是为了便于观察方向，如果单纯作为多头的话可以设置为0.0005】

    groups=df.groupby(timetarget,group_keys=False)
    print("数据分组后",groups)
    df=pd.DataFrame({})
    oldcodes=[]
    tradenum=0
    for group in groups:
        group=group[1]
        if len(oldcodes)==0:
            newgroup=group
        if len(oldcodes)>0:
            oldnum=len(group.loc[~group["代码"].isin(oldcodes)])#计算哪些股票需要调仓
            tradenum+=oldnum
            group.loc[~group["代码"].isin(oldcodes),["target_stock"]]+=1
            if direction=="long":#多头【针对现货】
                group.loc[~group["代码"].isin(oldcodes),["target_stock"]]*=(1-cost)
            else:
                group.loc[~group["代码"].isin(oldcodes),["target_stock"]]*=1/(1-cost)
            group.loc[~group["代码"].isin(oldcodes),["target_stock"]]-=1
            newgroup=group
        oldcodes=group["代码"].tolist()
        df=pd.concat([df,newgroup])
    df["总交易次数"]=tradenum
    print("扣除手续费之后",len(df))
    
    df.to_csv(f"{basepath}/{path}/all_{path}_{direction}_{thiscangwei}_{holdnum}只持仓_thisstock.csv")
    print("输出持仓成功")
    
    thisstock=df.copy()
    if thiscangwei=="分级靠档模式":
        thisstock["target_stock"]=thisstock["target_stock"]*thisstock["权重"]
        target_stock_value=thisstock.groupby(timetarget).apply(lambda x: pd.DataFrame({"target_stock_value": [x["target_stock"].sum()]}))  #绝对涨跌幅
    else:
        target_stock_value=thisstock.groupby(timetarget).apply(lambda x: pd.DataFrame({"target_stock_value": [x["target_stock"].mean()]}))  #绝对涨跌幅
        thisstock=thisstock.reset_index(drop=True)
    
    #暂时用不到利润隔日计算【但是实际上如果换成策略的话应该隔日计算】
    value=pd.DataFrame({})
    value["now_stock_value"]=((target_stock_value["target_stock_value"]+1)).cumprod()
    #value["now_stock_value_cost"]=((target_stock_value["target_stock_value"]+1)*(1-cost)).cumprod() #这里应该是每天都扣一次手续费
    value["总交易次数"]=tradenum
    value.to_csv(f"{basepath}/{path}/all_{path}_{direction}_{thiscangwei}_{holdnum}只持仓_value.csv")
    print("净值输出之后",value)

    
if newtrade=="聚宽格式":
    thisstock=pd.read_csv(f"{basepath}/{path}/all_{path}_{direction}_{thiscangwei}_{holdnum}只持仓_thisstock.csv")
    #将同花顺的股票后缀换成聚宽的股票后缀之后才输出
    thisstock["代码"]=thisstock["代码"].str.replace(r".SH", ".XSHG")#替换沪市后缀
    thisstock["代码"]=thisstock["代码"].str.replace(r".SZ", ".XSHE")#替换深市后缀
    thisstock=thisstock[thisstock[timetarget]>20200101]
    thisstock.to_csv(f"聚宽.csv")
    # thisstock=thisstock[thisstock[timetarget]>20240101]
    # thisstock.to_csv(f"聚宽近期.csv")
    try:
        thisstock=pd.read_csv(f"聚宽.csv")
        #转变为聚宽要求的比赛模式
        enddf=pd.DataFrame({})
        pivotdf=thisstock.groupby(timetarget)
        for pivot in pivotdf:
            thisdf=pivot[1][["代码","权重",timetarget]]
            # floattoday=pivot[0]
            floattoday=pivot[1][timetarget].values[0]
            print(f"{floattoday},{thisdf}")
            thisdf=thisdf.pivot(columns="代码",values="权重")
            #thisdf=thisdf.fillna(method="bfill")#向上填充
            thisdf=thisdf.bfill()#填充方式升级
            thisdf=thisdf[:1]
            thisdf["date"]=floattoday
            print(thisdf["date"])
            # 通过明确指定regex=True，可以确保代码在将来的Pandas版本中也能正常运行而不会受到默认值变化的影响。如果你有任何其他问题或疑问，请随时告诉我。
            thisdf["date"] = thisdf["date"].astype(str).str.replace(r"\.0", "", regex=True)#需要加上\才能恰好去掉.0，可能.字符需要转义
            print(thisdf["date"])
            # thisdf["date"]=pd.to_datetime(thisdf["date"],format="%Y%m%d",errors="coerce")
            thisdf["date"]=pd.to_datetime(thisdf["date"],format="%Y%m%d")

            print(thisdf)
            enddf=pd.concat([enddf,thisdf])
        enddf=enddf.set_index("date")
        enddf=enddf.fillna(0)
        enddf.to_csv(f"{basepath}/{path}/all_{path}_{direction}_{thiscangwei}_{holdnum}只持仓_聚宽仓位.csv")
        enddf.to_csv(f"{basepath}/{path}/all_{path}_{direction}_{thiscangwei}_{holdnum}只持仓_聚宽仓位.csv.gz",compression="gzip")
    except Exception as e:
        enddf.to_csv(f"{basepath}/{path}/all_{path}_{direction}_{thiscangwei}_{holdnum}只持仓_聚宽仓位.csv")
        enddf.to_csv(f"{basepath}/{path}/all_{path}_{direction}_{thiscangwei}_{holdnum}只持仓_聚宽仓位.csv.gz",compression="gzip")
        logger.info(f"发生bug: {e},{pivot}")