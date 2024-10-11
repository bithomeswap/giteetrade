import pandas as pd
import numpy as np
import decimal
import os
import datetime
import matplotlib.pyplot as plt
# 设置参数
a=40 # 将数据划分成a个等距离的区间

basepath=r"C:\Users\13480\Desktop\quant\【回测】本地\数据文件"
# basepath=r"/home/wth000/gitee/quant/【回测】本地/数据文件"
# holddays =30#统计三十天收益率
def technology(df): #定义计算技术指标的函数
    df=df.sort_values(by=timetarget) #以日期列为索引,避免计算错误
    #df=df.sort_values(by=timetarget,ascending=False) #从大到小排序

    # df["target_stock"]=(df["真实开盘价格"].shift(-1-1)/(df["真实开盘价格"].shift(-1)))-1
    # df[f"target_stock{holddays}"]=(df["真实开盘价格"].copy().shift(-holddays-1)/(df["真实开盘价格"].shift(-1).copy()))-1

    # window_size=10#时间窗口
    # # for columns in ["涨停","跌停","上涨","下跌"]:
    # for columns in ["涨停","跌停"]:
    #     df[f"{columns}溢价"]=df[columns]*df["开盘涨幅"]#不能减一，因为有的数据是0
    #     df[f"{window_size}日{columns}次数"]=df[columns].rolling(window=window_size).sum().fillna(0)
    #     df[f"{window_size}日{columns}平均溢价"]=df[f"{columns}溢价"].rolling(window=window_size).sum().fillna(0)/df[f"{window_size}日{columns}次数"].where(df[f"{window_size}日{columns}次数"]==0,1)
    # if "分时" not in path:
    #     for columns in ["换手率","隔日涨幅","日内涨幅","日内振幅","10日乖离率"]:
    #         df[f"{window_size}日平均{columns}"]=df[f"{columns}"].rolling(window=window_size).mean()
    #         df[f"RollingStd{columns}"] = np.log(df[columns]).rolling(window=window_size).std()# 计算因子值的对数收益率并使用rolling函数计算过去100天的滚动标准差
    #         df[f"{window_size}日年化波动率{columns}"] = df[f"RollingStd{columns}"]*np.sqrt(252)# 用标准差乘以时间因子（假设一年有252个交易日，则时间因子就是252的平方根），就是年化滚动标准差

    window_size=100#时间窗口
    df[f"{window_size}日涨幅"]=(df["真实开盘价格"].shift(window_size)/(df["真实开盘价格"].shift(-1)))-1
    for columns in ["隔日涨幅"]:
        for thiscolumns in ["换手率",f"{100}日年化波动率{columns}"]:
            df[f"{window_size}日{thiscolumns}"]=(df[thiscolumns].shift(window_size)/(df[thiscolumns]))-1
    return df

# paths=[r"全体A股",r"半小时资金流",r"半小时量价"]
paths=[r"全体A股"]
for path in paths:
    if path==r"全体A股":
        timetarget="floattoday"
    elif path==r"半小时资金流": #文件夹路径
        timetarget="float价格分时"
    elif path==r"半小时量价": #文件夹路径
        timetarget="float价格分时"

    # #通达信获取微盘股指数拼接
    # from pytdx.exhq import *
    # from pytdx.hq import TdxHq_API
    # import pandas as pd
    # from datetime import datetime
    # #通达信api地址：https://gitee.com/better319/pytdx/#5--%E8%8E%B7%E5%8F%96%E6%8C%87%E6%95%B0k%E7%BA%BF
    # ip="119.147.212.81"
    # api = TdxHq_API()
    # api.connect(ip,7709)
    # all_data=pd.DataFrame()
    # #每次只能取800组数据，循环取数
    # wp_data = api.to_df(api.get_index_bars(4, 1, "880823",0, 800))#微盘股指数
    # wp_data["datetime"] = pd.to_datetime(wp_data["datetime"])
    # wp_data["date"] = wp_data["datetime"].dt.strftime("%Y%m%d")
    # wp_data["floattoday"] = wp_data["date"].astype(float)
    # wp_data["通达信指数"]=wp_data["open"]
    # wp_data=wp_data[["floattoday","通达信指数"]]
    # wp_data.to_csv(f"通达信指数.csv")

    wp_data=pd.read_csv(f"通达信指数.csv")
    tradetypes=["全部"]
    # tradetypes=["小市值"]
    for tradetype in tradetypes:
        print("path",path,"tradetype",tradetype)
        df=pd.read_csv(f"{basepath}/{path}/{path}{tradetype}.csv")
        print(df.columns)
        df=df.groupby("代码",group_keys=False).apply(technology) #计算复权因子

        df=df.sort_values(by=timetarget) #以日期列为索引,避免计算错误
        # # 日期截取
        # datelist=df[timetarget].unique().tolist() # 获取观察周期的所有日期数据
        # testdays=500#只要最后testdays日期的数据
        # # testdays=len(datelist)#截取全部数据
        # print("日期截取前",len(df))
        # dateprediction=datelist[len(datelist)-testdays]
        # print("截取日期",dateprediction)
        # df=df[df[timetarget]>=dateprediction]
        # print("日期截取后",len(df))

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

        alldf=pd.DataFrame({})
        olddf=df.copy()

        plotnames=["归母净利润+每股未分配利润（原始策略，其实加了未分配之后这波地产行情在小市值里面就没吃到）",
                   "多因子+基本面",
                   "多因子+市值",
                   "多因子+量价",
                   "多因子市值量价",
                   
                   "多因子+基本面趋势强度",
                   "多因子+基本面乖离率",
                   "多因子+基本面多量价",
                   ]
        for plotname in plotnames:
            df=olddf.copy()
            # # 日期截取
            # datelist=df[timetarget].unique().tolist() # 获取观察周期的所有日期数据
            # testdays=500#只要最后testdays日期的数据
            # # testdays=len(datelist)#截取全部数据
            # print("日期截取前",len(df))
            # # #先去掉前一百天的数据
            # # dateprediction=datelist[100]
            # # print("截取日期",dateprediction)
            # # df=df[df[timetarget]>=dateprediction]
            # #只保留应保留的天数testdays天
            # dateprediction=datelist[len(datelist)-testdays]
            # print("截取日期",dateprediction)
            # df=df[df[timetarget]>=dateprediction]
            # print("日期截取后",len(df))

            #基本面筛选
            if not ("归母净利润+每股未分配利润" in plotname):
                if not ("多因子" in plotname):
                    pass
                else:
                    df=df[df["归母净利润"]>0]
                    df=df[df["每股未分配利润"]>0]#每股未分配利润1元以上

                    df=df[df["当年股息率"]>0]
                    df=df[df["每股未分配利润"]>1]#每股未分配利润1元以上
                    df=df[df["基本每股收益"]>0.1]#每股收益0.1元以上
                    df=df[df["归母净利润季度增长率"]>0]
                    df=df[df["净资产年度增长率"]>1]#百分比
                    df=df[df["去年股息率"]>0]
                    # df=df[df["当年总分红"]>0]
                    # df=df[df["去年总分红"]>0]
                    # df=df[df["前年总分红"]>0]
            else:
                df=df[df["归母净利润"]>0]
                df=df[df["每股未分配利润"]>0]#每股未分配利润1元以上

            # #这段代码是只保留小市值
            # stocknum=400
            # df=df.copy().groupby(timetarget,group_keys=False).apply(lambda x: x.nsmallest(stocknum,"总市值"))#【竞价涨幅低的一般会盈利1.33（扣完手续费1.04）】50只就1.06
            
            if "多因子"in plotname:#【貌似一次group之后后面能一直用】
                if "+基本面" in plotname:#True是值越小越靠前，False是值越大越靠前
                    #【倒序排名法】
                    df["股息率_rank"]=df.groupby(timetarget,group_keys=False)["股息率"].rank(
                        method="max", ascending=True,na_option="bottom")
                    df["基本每股收益_rank"]=df.groupby(timetarget,group_keys=False)["基本每股收益"].rank(
                        method="max", ascending=True,na_option="bottom")
                    df["每股未分配利润_rank"]=df.groupby(timetarget,group_keys=False)["每股未分配利润"].rank(
                        method="max", ascending=True,na_option="bottom")
                    df["归母净利润_rank"]=df.groupby(timetarget,group_keys=False)["归母净利润"].rank(
                        method="max", ascending=True,na_option="bottom")
                    df["归母净利润季度增长率_rank"]=df.groupby(timetarget,group_keys=False)["归母净利润季度增长率"].rank(
                        method="max", ascending=True,na_option="bottom")
                    df["净资产年度增长率_rank"]=df.groupby(timetarget,group_keys=False)["净资产年度增长率"].rank(
                        method="max", ascending=True,na_option="bottom")
                    df["基本面排名"]=df["股息率_rank"]+df["每股未分配利润_rank"]+df["归母净利润_rank"]+df["归母净利润季度增长率_rank"]+df["净资产年度增长率_rank"]+df["基本每股收益_rank"]
                    df["基本面排名_rank"]=df.groupby(timetarget,group_keys=False)["基本面排名"].rank(
                        method="max", ascending=False,na_option="bottom")#从小到大排名
                    df["排名"]=df["基本面排名_rank"]
                    if "+基本面趋势强度" in plotname:
                        # 累积隔日涨幅ABS【代表的波动的强度】本身是一个有效因子
                        df["隔日涨幅ABS"]=abs(df["隔日涨幅"]-1)
                        df["隔日涨幅ABS归一化"]=df["隔日涨幅ABS"]
                        df.loc[(df["隔日涨幅ABS归一化"]>0.1),"隔日涨幅ABS归一化"]=0.1
                        df["累积隔日涨幅ABS"]=df.groupby("代码",group_keys=False).apply(lambda x:x[f"隔日涨幅ABS"].rolling(50).sum())
                        df[f"累积隔日涨幅ABS_rank"]=df[f"累积隔日涨幅ABS"].rank(
                            method="max",ascending=True,na_option="bottom")/len(df)#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                        # df=df.dropna(subset=["累积隔日涨幅ABS_rank"])#去掉后1.118452，不去掉1.118452，所以空值无论咋排名都在后面
                        df["量价排名"]=df[f"累积隔日涨幅ABS_rank"]#20日1.118452，50日1.14，100日1.12
                    
                        # # #该因子的目的仅仅是把强势标的推到前排
                        # df["10日乖离率绝对值"]=abs(df["10日乖离率"]-1.01)
                        # # df["10日乖离率_rank"]=df.groupby(timetarget,group_keys=False)["10日乖离率绝对值"].rank(
                        # #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                        # # # df["10日乖离率_rank"]=df.groupby(timetarget,group_keys=False)["10日乖离率"].rank(
                        # # #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                        # # df["量价排名"]+=df["10日乖离率_rank"]
                        # # # df["量价排名"]*=df["10日乖离率_rank"]
                        
                        # #直接使用1.01轴的10日乖离率绝对值进行乘法修正 
                        # df["量价排名"]*=df["10日乖离率绝对值"]

                        df["量价排名_rank"]=df.groupby(timetarget,group_keys=False)["量价排名"].rank(
                            method="max", ascending=True,na_option="bottom")#从小到大排名
                        df["排名"]+=df["量价排名_rank"]
                        
                    if "+基本面乖离率" in plotname:
                        # # 累积隔日涨幅ABS【代表的波动的强度】本身是一个有效因子
                        # df["隔日涨幅ABS"]=abs(df["隔日涨幅"]-1)
                        # df["隔日涨幅ABS归一化"]=df["隔日涨幅ABS"]
                        # df.loc[(df["隔日涨幅ABS归一化"]>0.1),"隔日涨幅ABS归一化"]=0.1
                        # df["累积隔日涨幅ABS"]=df.groupby("代码",group_keys=False).apply(lambda x:x[f"隔日涨幅ABS"].rolling(50).sum())
                        # df[f"累积隔日涨幅ABS_rank"]=df[f"累积隔日涨幅ABS"].rank(
                        #     method="max",ascending=True,na_option="bottom")/len(df)#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                        # # df=df.dropna(subset=["累积隔日涨幅ABS_rank"])#去掉后1.118452，不去掉1.118452，所以空值无论咋排名都在后面
                        # df["量价排名"]=df[f"累积隔日涨幅ABS_rank"]#20日1.118452，50日1.14，100日1.12
                    
                        # #该因子的目的仅仅是把强势标的推到前排
                        df["10日乖离率绝对值"]=abs(df["10日乖离率"]-1.01)
                        df["10日乖离率_rank"]=df.groupby(timetarget,group_keys=False)["10日乖离率绝对值"].rank(
                            method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                        # df["10日乖离率_rank"]=df.groupby(timetarget,group_keys=False)["10日乖离率"].rank(
                        #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                        df["量价排名"]=df["10日乖离率_rank"]
                        # df["量价排名"]+=df["10日乖离率_rank"]
                        # # df["量价排名"]*=df["10日乖离率_rank"]
                        
                        # #直接使用1.01轴的10日乖离率绝对值进行乘法修正 
                        # df["量价排名"]*=df["10日乖离率绝对值"]

                        df["量价排名_rank"]=df.groupby(timetarget,group_keys=False)["量价排名"].rank(
                            method="max", ascending=True,na_option="bottom")#从小到大排名
                        df["排名"]+=df["量价排名_rank"]
                    if "+基本面多量价 " in plotname:
                        # 累积隔日涨幅ABS【代表的波动的强度】本身是一个有效因子
                        df["隔日涨幅ABS"]=abs(df["隔日涨幅"]-1)
                        df["隔日涨幅ABS归一化"]=df["隔日涨幅ABS"]
                        df.loc[(df["隔日涨幅ABS归一化"]>0.1),"隔日涨幅ABS归一化"]=0.1
                        df["累积隔日涨幅ABS"]=df.groupby("代码",group_keys=False).apply(lambda x:x[f"隔日涨幅ABS"].rolling(50).sum())
                        df[f"累积隔日涨幅ABS_rank"]=df[f"累积隔日涨幅ABS"].rank(
                            method="max",ascending=True,na_option="bottom")/len(df)#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                        # df=df.dropna(subset=["累积隔日涨幅ABS_rank"])#去掉后1.118452，不去掉1.118452，所以空值无论咋排名都在后面
                        df["量价排名"]=df[f"累积隔日涨幅ABS_rank"]#20日1.118452，50日1.14，100日1.12
                    
                        # # #该因子的目的仅仅是把强势标的推到前排
                        # df["10日乖离率绝对值"]=abs(df["10日乖离率"]-1.01)
                        # df["10日乖离率_rank"]=df.groupby(timetarget,group_keys=False)["10日乖离率绝对值"].rank(
                        #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                        # # df["10日乖离率_rank"]=df.groupby(timetarget,group_keys=False)["10日乖离率"].rank(
                        # #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                        # df["量价排名"]+=df["10日乖离率_rank"]
                        # # # df["量价排名"]*=df["10日乖离率_rank"]

                        # #直接使用1.01轴的10日乖离率绝对值进行乘法修正 
                        # df["量价排名"]*=df["10日乖离率绝对值"]

                        window_size=3#计算三日最高点偏离的rank分布的收益率
                        # df[f"{window_size}日开盘价格与最高价格比值绝对值"]=abs(df[f"{window_size}日开盘价格与最高价格比值"]-1.01)
                        # df[f"{window_size}日开盘价格与最高价格比值_rank"]=df.groupby(timetarget,group_keys=False)[f"{window_size}日开盘价格与最高价格比值绝对值"].rank(
                        #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                        # # df[f"{window_size}日开盘价格与最高价格比值_rank"]=df.groupby(timetarget,group_keys=False)[f"{window_size}日开盘价格与最高价格比值"].rank(
                        # #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                        # df["量价排名"]+=df[f"{window_size}日开盘价格与最高价格比值_rank"]
                        # # # df["量价排名"]*=df[f"{window_size}日开盘价格与最高价格比值_rank"]

                        #直接使用1.01轴的10日乖离率绝对值进行乘法修正 
                        df["量价排名"]*=df[f"{window_size}日开盘价格与最高价格比值"]

                        df["量价排名_rank"]=df.groupby(timetarget,group_keys=False)["量价排名"].rank(
                            method="max", ascending=True,na_option="bottom")#从小到大排名
                        df["排名"]+=df["量价排名_rank"]
                if "+市值" in plotname:#True是值越小越靠前，False是值越大越靠前
                    df["总市值_rank"]=df.groupby(timetarget,group_keys=False)["总市值"].rank(
                        method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                    df["排名"]=df["总市值_rank"]
                if "+量价" in plotname:#在小市值标的上有一定效果，但是没市值本身好，可能毕竟适合全市场
                    # 累积隔日涨幅ABS【代表的波动的强度】本身是一个有效因子
                    df["隔日涨幅ABS"]=abs(df["隔日涨幅"]-1)
                    df["隔日涨幅ABS归一化"]=df["隔日涨幅ABS"]
                    df.loc[(df["隔日涨幅ABS归一化"]>0.1),"隔日涨幅ABS归一化"]=0.1
                    df["累积隔日涨幅ABS"]=df.groupby("代码",group_keys=False).apply(lambda x:x[f"隔日涨幅ABS"].rolling(50).sum())
                    df[f"累积隔日涨幅ABS_rank"]=df[f"累积隔日涨幅ABS"].rank(
                        method="max",ascending=True,na_option="bottom")/len(df)#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                    # df=df.dropna(subset=["累积隔日涨幅ABS_rank"])#去掉后1.118452，不去掉1.118452，所以空值无论咋排名都在后面
                    df["量价排名"]=df[f"累积隔日涨幅ABS_rank"]#20日1.118452，50日1.14，100日1.12
                    
                    # # #该因子的目的仅仅是把强势标的推到前排
                    # df["10日乖离率绝对值"]=abs(df["10日乖离率"]-1.01)
                    # # df["10日乖离率_rank"]=df.groupby(timetarget,group_keys=False)["10日乖离率绝对值"].rank(
                    # #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                    # # # df["10日乖离率_rank"]=df.groupby(timetarget,group_keys=False)["10日乖离率"].rank(
                    # # #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                    # # df["量价排名"]+=df["10日乖离率_rank"]
                    # # # df["量价排名"]*=df["10日乖离率_rank"]
                    
                    # #直接使用1.01轴的10日乖离率绝对值进行乘法修正 
                    # df["量价排名"]*=df["10日乖离率绝对值"]

                    window_size=3#计算三日最高点偏离的rank分布的收益率
                    # df[f"{window_size}日开盘价格与最高价格比值绝对值"]=abs(df[f"{window_size}日开盘价格与最高价格比值"]-1.01)
                    # df[f"{window_size}日开盘价格与最高价格比值_rank"]=df.groupby(timetarget,group_keys=False)[f"{window_size}日开盘价格与最高价格比值绝对值"].rank(
                    #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                    # # df[f"{window_size}日开盘价格与最高价格比值_rank"]=df.groupby(timetarget,group_keys=False)[f"{window_size}日开盘价格与最高价格比值"].rank(
                    # #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                    # df["量价排名"]+=df[f"{window_size}日开盘价格与最高价格比值_rank"]
                    # # # df["量价排名"]*=df[f"{window_size}日开盘价格与最高价格比值_rank"]

                    #直接使用1.01轴的10日乖离率绝对值进行乘法修正 
                    df["量价排名"]*=df[f"{window_size}日开盘价格与最高价格比值"]

                    df["量价排名_rank"]=df.groupby(timetarget,group_keys=False)["量价排名"].rank(
                        method="max", ascending=True,na_option="bottom")#从小到大排名
                    df["排名"]=df["量价排名_rank"]
                if "市值量价" in plotname:
                    df["总市值_rank"]=df.groupby(timetarget,group_keys=False)["总市值"].rank(
                        method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                    df["排名"]=df["总市值_rank"]

                    # 累积隔日涨幅ABS【代表的波动的强度】本身是一个有效因子
                    df["隔日涨幅ABS"]=abs(df["隔日涨幅"]-1)
                    df["累积隔日涨幅ABS"]=df.groupby("代码",group_keys=False).apply(lambda x:x[f"隔日涨幅ABS"].rolling(50).sum())
                    df[f"累积隔日涨幅ABS_rank"]=df[f"累积隔日涨幅ABS"].rank(
                        method="max",ascending=True,na_option="bottom")/len(df)#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                    # df=df.dropna(subset=["累积隔日涨幅ABS_rank"])#去掉后1.118452，不去掉1.118452，所以空值无论咋排名都在后面
                    df["量价排名"]=df[f"累积隔日涨幅ABS_rank"]#20日1.118452，50日1.14，100日1.12
                    
                    # # #该因子的目的仅仅是把强势标的推到前排
                    # df["10日乖离率绝对值"]=abs(df["10日乖离率"]-1.01)
                    # # df["10日乖离率_rank"]=df.groupby(timetarget,group_keys=False)["10日乖离率绝对值"].rank(
                    # #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                    # # # df["10日乖离率_rank"]=df.groupby(timetarget,group_keys=False)["10日乖离率"].rank(
                    # # #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                    # # df["量价排名"]+=df["10日乖离率_rank"]
                    # # # df["量价排名"]*=df["10日乖离率_rank"]
                    
                    # #直接使用1.01轴的10日乖离率绝对值进行乘法修正 
                    # df["量价排名"]*=df["10日乖离率绝对值"]

                    window_size=3#计算三日最高点偏离的rank分布的收益率
                    # df[f"{window_size}日开盘价格与最高价格比值绝对值"]=abs(df[f"{window_size}日开盘价格与最高价格比值"]-1.01)
                    # df[f"{window_size}日开盘价格与最高价格比值_rank"]=df.groupby(timetarget,group_keys=False)[f"{window_size}日开盘价格与最高价格比值绝对值"].rank(
                    #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                    # # df[f"{window_size}日开盘价格与最高价格比值_rank"]=df.groupby(timetarget,group_keys=False)[f"{window_size}日开盘价格与最高价格比值"].rank(
                    # #     method="max", ascending=True,na_option="bottom")#method="max"： 表示当出现相同值时取最大排名，ascending=True： 表示按升序排列（从小到大），ascending=False：表示按升序排列（从大到小），na_option="bottom"：表示将缺失值放在最后。
                    # df["量价排名"]+=df[f"{window_size}日开盘价格与最高价格比值_rank"]
                    # # # df["量价排名"]*=df[f"{window_size}日开盘价格与最高价格比值_rank"]

                    #直接使用1.01轴的10日乖离率绝对值进行乘法修正 
                    df["量价排名"]*=df[f"{window_size}日开盘价格与最高价格比值"]

                    df["量价排名_rank"]=df.groupby(timetarget,group_keys=False)["量价排名"].rank(
                        method="max", ascending=True,na_option="bottom")#从小到大排名
                    # df["排名"]+=df["量价排名_rank"]#1.33314
                    df["排名"]*=df["量价排名_rank"]#1.37347
                    # df["排名"]*=df["累积隔日涨幅ABS"]#不能直接修正排名
            else:
                df["排名"]=df["总市值"]
            df=df[~(df["次日is_st"]==1)]
            df=df[~(df["次日is_paused"]==1)]
            df=df[~(df["次日开盘涨停"]==1)]
            df["资产负债率"]=df["负债合计"]/df["负债和股东权益总计"]
            df=df[df["资产负债率"]<1]

            stocknum=30
            # stocknum=5
            df=df.copy().groupby(timetarget,group_keys=False).apply(lambda x: x.nsmallest(stocknum,"排名"))#【竞价涨幅低的一般会盈利1.33（扣完手续费1.04）】50只就1.06
            
            # df.to_csv(f"小市值.csv")
            # df=pd.read_csv(f"小市值.csv")
            df.to_csv(f"【去ST和不可交易】合成指数{stocknum}只{plotname}样本数据.csv")


            # 【1日涨跌幅】
            df[f"指数涨跌幅"]=df.groupby(timetarget,group_keys=False)["target_stock"].transform("mean") # 平均数


            # #【多日涨跌幅】这里对收益率开了holddays次方
            # # holddays=30#holddays日涨跌幅
            # df[f"指数涨跌幅"]=df.groupby(timetarget,group_keys=False)[f"target_stock{holddays}"].transform("mean") # 平均数
            # df[f"指数涨跌幅"]=(1+df[f"指数涨跌幅"])**(1/holddays)-1


            df=df.groupby(timetarget).apply(lambda x: x.head(1))
            df=df[[f"指数涨跌幅",timetarget]]
            df[f"【去ST和不可交易】合成指数{stocknum}只{plotname}"]=(df[f"指数涨跌幅"]+1).cumprod()
            df=df.drop(columns="指数涨跌幅")
            df=df.reset_index(drop=True)
            if alldf.empty:
                alldf=pd.concat([alldf,df])
            else:
                alldf=alldf.merge(df,on=timetarget)
            print(alldf)
        # #通达信数据源的数据少这边尽量不要截取
        # alldf=wp_data.merge(alldf,on=timetarget,how="right")#拼接通达信的微盘股指数
        # # alldf["通达信指数"]=alldf["通达信指数"].shift(-1)
        # alldf["微盘股指数"]=alldf["通达信指数"].shift(-1)/alldf["通达信指数"].values[0]
        alldf.to_csv(f"【去ST和不可交易】合成指数{stocknum}只.csv")

        # #保留处理前的数据
        # thiscolumns=["3日平均隔日涨幅","10日乖离率"]
        # for mubiao in thiscolumns:
        #     df[f"{mubiao}处理前"]=df[mubiao]
        #     df.loc[df[mubiao]>=1.2,mubiao]=1.2
        #     df.loc[df[mubiao]<=0.8,mubiao]=0.8
        #     df[mubiao]=(df[mubiao]-1)*100
        #     # 设置不同值作为正负轴
        #     df[mubiao]=abs(df[mubiao]-1.5)#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-0.5)#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-0)#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-1)#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-2)#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-3)#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-(-1))#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-(-2))#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-(-3))#标准化并且取绝对值
