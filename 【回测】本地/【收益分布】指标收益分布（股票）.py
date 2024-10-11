import pandas as pd
import numpy as np
import os
import datetime
# 设置参数
a=40 # 将数据划分成a个等距离的区间
# a=200 # 将数据划分成a个等距离的区间

basepath=r"C:\Users\13480\Desktop\quant\【回测】本地\数据文件"
# basepath=r"/home/wth000/gitee/quant/【回测】本地/数据文件"
# MAD:中位数去极值
def extreme_MAD_up(dt,n):
    median = dt.quantile(0.5) #找出中位数
    new_median = (abs((dt - median)).quantile(0.5)) #偏差值的中位数
    dt_up = median + n*new_median #上限
    dt_down = median - n*new_median #下限
    return dt_up
def extreme_MAD_down(dt,n):
    median = dt.quantile(0.5) #找出中位数
    new_median = (abs((dt - median)).quantile(0.5)) #偏差值的中位数
    dt_up = median + n*new_median #上限
    dt_down = median - n*new_median #下限
    return dt_down
#用原始值又会导致反转
def technology(df): #定义计算技术指标的函数
    df=df.sort_values(by=timetarget) #以日期列为索引,避免计算错误
    #df=df.sort_values(by=timetarget,ascending=False) #从大到小排序
    
    # # 计算一个月（20日）振幅的涨幅的变动情况（百分比变动情况，也就是带正负）因子
    # window_size=20
    # df[f'{window_size}日内振幅变动情况']=df['日内振幅']/df['日内振幅'].shift(1)-1
    # df[f'{window_size}日内振幅动量']=df[f'{window_size}日内振幅变动情况'].rolling(window=window_size).sum()

    window_size=20
    # weights=1#等权重回归
    # df['slope总市值'] = df['总市值'].rolling(window=window_size).apply(lambda x: np.polyfit(x.index,x,1)[0]) 
    weights=np.linspace(1,2,window_size)#线性增加权重
    
    # #总市值
    # df['slope总市值']=df['总市值'].rolling(window=window_size).apply(lambda x: np.polyfit(x.index,x,1,w=weights)[0]) 
    # df["标准差总市值"]=df['总市值'].rolling(window=window_size).std()
    # df['标准差调整的线性回归斜率总市值']=df['slope总市值']/df['标准差总市值']
    # #数据极值处理
    # df["up标准差调整的线性回归斜率总市值"]= df['标准差调整的线性回归斜率总市值'].rolling(
    #     window=250).apply(lambda x: extreme_MAD_up(x,5.2))
    # df["down标准差调整的线性回归斜率总市值"]= df['标准差调整的线性回归斜率总市值'].rolling(
    #     window=250).apply(lambda x: extreme_MAD_down(x,5.2))
    # df.loc[df['标准差调整的线性回归斜率总市值']>=df[
    #     "up标准差调整的线性回归斜率总市值"],"标准差调整的线性回归斜率总市值"]=df.loc[df[
    #         '标准差调整的线性回归斜率总市值']>=df["up标准差调整的线性回归斜率总市值"
    #                                ],"up标准差调整的线性回归斜率总市值"]
    # df.loc[df['标准差调整的线性回归斜率总市值']>=df[
    #     "down标准差调整的线性回归斜率总市值"],"标准差调整的线性回归斜率总市值"]=df.loc[df[
    #         '标准差调整的线性回归斜率总市值']>=df["down标准差调整的线性回归斜率总市值"
    #                                ],"down标准差调整的线性回归斜率总市值"]
    # # #处理后的数据
    # df['max标准差调整的线性回归斜率总市值']=df['标准差调整的线性回归斜率总市值'].rolling(window=window_size).max()
    # df['min标准差调整的线性回归斜率总市值']=df['标准差调整的线性回归斜率总市值'].rolling(window=window_size).min()
    # df['250周期调整后标准差调整的线性回归斜率总市值']=2*(
    #     1-(df['max标准差调整的线性回归斜率总市值']+df['min标准差调整的线性回归斜率总市值'])/2
    #     )/(df['max标准差调整的线性回归斜率总市值']-df['min标准差调整的线性回归斜率总市值'])

    #涨跌幅
    df['slope涨跌幅']=df['隔日涨幅'].rolling(window=window_size).apply(lambda x: np.polyfit(x.index,x,1,w=weights)[0]) 
    df["标准差涨跌幅"]=df['隔日涨幅'].rolling(window=window_size).std()
    df['标准差调整的线性回归斜率涨跌幅']=df['slope涨跌幅']/df['标准差涨跌幅']
    # #数据极值处理
    # df["up标准差调整的线性回归斜率涨跌幅"]= df['标准差调整的线性回归斜率涨跌幅'].rolling(
    #     window=250).apply(lambda x: extreme_MAD_up(x,5.2))
    # df["down标准差调整的线性回归斜率涨跌幅"]= df['标准差调整的线性回归斜率涨跌幅'].rolling(
    #     window=250).apply(lambda x: extreme_MAD_down(x,5.2))
    # df.loc[df['标准差调整的线性回归斜率涨跌幅']>=df[
    #     "up标准差调整的线性回归斜率涨跌幅"],"标准差调整的线性回归斜率涨跌幅"]=df.loc[df[
    #         '标准差调整的线性回归斜率涨跌幅']>=df["up标准差调整的线性回归斜率涨跌幅"
    #                                ],"up标准差调整的线性回归斜率涨跌幅"]
    # df.loc[df['标准差调整的线性回归斜率涨跌幅']>=df[
    #     "down标准差调整的线性回归斜率涨跌幅"],"标准差调整的线性回归斜率涨跌幅"]=df.loc[df[
    #         '标准差调整的线性回归斜率涨跌幅']>=df["down标准差调整的线性回归斜率涨跌幅"
    #                                ],"down标准差调整的线性回归斜率涨跌幅"]
    # # #处理后的数据
    # df['max标准差调整的线性回归斜率涨跌幅']=df['标准差调整的线性回归斜率涨跌幅'].rolling(window=window_size).max()
    # df['min标准差调整的线性回归斜率涨跌幅']=df['标准差调整的线性回归斜率涨跌幅'].rolling(window=window_size).min()
    # df['250周期调整后标准差调整的线性回归斜率涨跌幅']=2*(
    #     1-(df['max标准差调整的线性回归斜率涨跌幅']+df['min标准差调整的线性回归斜率涨跌幅'])/2
    #     )/(df['max标准差调整的线性回归斜率涨跌幅']-df['min标准差调整的线性回归斜率涨跌幅'])
    
    # #乖离率
    # df['slope10日乖离率']=df['10日乖离率'].rolling(window=window_size).apply(lambda x: np.polyfit(x.index,x,1,w=weights)[0]) 
    # df["标准差10日乖离率"]=df['10日乖离率'].rolling(window=window_size).std()
    # df['标准差调整的线性回归斜率10日乖离率']=df['slope10日乖离率']/df['标准差10日乖离率']
    # #数据极值处理
    # df["up标准差调整的线性回归斜率10日乖离率"]= df['标准差调整的线性回归斜率10日乖离率'].rolling(
    #     window=250).apply(lambda x: extreme_MAD_up(x,5.2))
    # df["down标准差调整的线性回归斜率10日乖离率"]= df['标准差调整的线性回归斜率10日乖离率'].rolling(
    #     window=250).apply(lambda x: extreme_MAD_down(x,5.2))
    # df.loc[df['标准差调整的线性回归斜率10日乖离率']>=df[
    #     "up标准差调整的线性回归斜率10日乖离率"],"标准差调整的线性回归斜率10日乖离率"]=df.loc[df[
    #         '标准差调整的线性回归斜率10日乖离率']>=df["up标准差调整的线性回归斜率10日乖离率"
    #                                ],"up标准差调整的线性回归斜率10日乖离率"]
    # df.loc[df['标准差调整的线性回归斜率10日乖离率']>=df[
    #     "down标准差调整的线性回归斜率10日乖离率"],"标准差调整的线性回归斜率10日乖离率"]=df.loc[df[
    #         '标准差调整的线性回归斜率10日乖离率']>=df["down标准差调整的线性回归斜率10日乖离率"
    #                                ],"down标准差调整的线性回归斜率10日乖离率"]
    # #处理后的数据
    # df['max标准差调整的线性回归斜率10日乖离率']=df['标准差调整的线性回归斜率10日乖离率'].rolling(window=window_size).max()
    # df['min标准差调整的线性回归斜率10日乖离率']=df['标准差调整的线性回归斜率10日乖离率'].rolling(window=window_size).min()
    # df['250周期调整后标准差调整的线性回归斜率10日乖离率']=2*(
    #     1-(df['max标准差调整的线性回归斜率10日乖离率']+df['min标准差调整的线性回归斜率10日乖离率'])/2
    #     )/(df['max标准差调整的线性回归斜率10日乖离率']-df['min标准差调整的线性回归斜率10日乖离率'])
    
    df=df.iloc[250:]
    df=df.iloc[20:]
    # df.to_csv("测试.csv")
    # print(df)
    # print(len(df))
    return df

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

    tradetypes=["全部"]
    # tradetypes=["小市值"]
    # tradetypes=["小市值","大市值","涨停","跌停","全部"]
    for tradetype in tradetypes:
        print("path",path,"tradetype",tradetype)
        df=pd.read_csv(f"{basepath}/{path}/{path}{tradetype}.csv")
        df=df.groupby("代码",group_keys=False).apply(technology)
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
        if "全体A股" in path:
            # df["每股未分配利润"]=df["未分配利润"]/df["总股本"]
            # df["股息率"]=df["股息率"]/100
            # df["当年股息率"]=df["股息率"]
            # # df["当年总分红"]=df["总市值"]*df["股息率"]
            # df.sort_values(by=timetarget,inplace=True)#日期升序排序
            # df["去年股息率"]=df.groupby("代码",group_keys=False)["当年股息率"].shift(250)
            # # df["去年总分红"]=df.groupby("代码",group_keys=False)["当年总分红"].shift(250)
            # # df["前年总分红"]=df.groupby("代码",group_keys=False)["当年总分红"].shift(500)
            # # df["两年总分红"]=df["当年总分红"]+df["去年总分红"]
            # # df["股息率"]=df["两年总分红"]/df["总市值"]*100
            # df["股息率"]=(df["当年股息率"]+df["去年股息率"])/2

            # # 日期截取【尽量不截取】
            # datelist=df[timetarget].unique().tolist() # 获取观察周期的所有日期数据
            # print("日期截取前",len(df))
            # dateprediction=datelist[250]#只保留250天之后的数据，避免股息率的干扰
            # print("截取日期",dateprediction)
            # df=df[df[timetarget]>=dateprediction]
            # print("日期截取后",len(df))

            #基本面筛选
            df=df[df["归母净利润"]>0]#21年达标标的最小市值7-10亿元
            # df=df[df["每股未分配利润"]>1]#每股未分配利润1元以上
            # df=df[df["基本每股收益"]>0.1]#每股收益0.1元以上
            # df=df[df["归母净利润季度增长率"]>0]
            # df=df[df["净资产年度增长率"]>1]#百分比
            # df=df[df["当年股息率"]>0]
            # df=df[df["去年股息率"]>0]
            # df=df[df["当年总分红"]>0]
            # df=df[df["去年总分红"]>0]
            # df=df[df["前年总分红"]>0]

            # #【这里限制的只要小市值】
            # df=df.copy().groupby(timetarget,group_keys=False).apply(lambda x: x.nsmallest(400,"总市值"))#【竞价涨幅低的一般会盈利1.33（扣完手续费1.04）】50只就1.06
            # df.to_csv(f"小市值.csv")
            # df=pd.read_csv(f"小市值.csv")

            # ranklist=["上涨溢价","下跌溢价","涨停溢价","跌停溢价","百日上涨次数","百日上涨平均溢价","百日下跌次数","百日下跌平均溢价","百日涨停次数","百日涨停平均溢价","百日跌停次数","百日跌停平均溢价",]
            # ranklist=["上涨溢价","下跌溢价","涨停溢价","跌停溢价",]
            # for mubiao in ranklist:
            #     # df = df.dropna(subset=[mubiao])#去掉空值
            #     df[f"{mubiao}_rank"]=df.groupby(timetarget,group_keys=False)[f"{mubiao}"].rank(ascending=True)
            #     df=df.groupby(timetarget,group_keys=False).apply(lambda x: x.assign(
            #         **{f"{mubiao}_rank_rate": (x[f"{mubiao}_rank"]/len(x))}
            #         ))
        if "可转债" in path:
            df=df[~(df["次日is_paused"]==1)]
            # df["总市值"]=df["三低指数"] #针对可转债
            df.loc[(df["转股溢价率"]>1.2),"总市值"]*=1.5 # 针对溢价率高的标的进行加权
        if "全体A股" in path:
            df=df[~(df["次日is_st"]==1)]
            df=df[~(df["次日is_paused"]==1)]
            df=df[~(df["次日开盘涨停"]==1)]

        # #每个标的删掉前三十行数据【避免空数据的干扰】
        # df=df.sort_values(by=timetarget)#以日期列为索引,避免计算错误
        # df=df.groupby("代码",group_keys=False).apply(lambda x: x.iloc[10:])
        #保留处理前的数据
        # thiscolumns=["3日平均隔日涨幅","10日乖离率"]
        # for mubiao in thiscolumns:
        #     df[f"{mubiao}处理前"]=df[mubiao]
        #     df.loc[df[mubiao]>=1.2,mubiao]=1.2
        #     df.loc[df[mubiao]<=0.8,mubiao]=0.8
        #     df[mubiao]=(df[mubiao]-1)*100

        #     df[mubiao]=abs(df[mubiao]-1.5)#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-0.5)#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-0)#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-1)#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-2)#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-3)#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-(-1))#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-(-2))#标准化并且取绝对值
        #     # df[mubiao]=abs(df[mubiao]-(-3))#标准化并且取绝对值
        # # 直接删掉空值
        # for mubiao in thiscolumns:
        #     #处理后的因子排名
        #     df = df.dropna(subset=[mubiao])#去掉空值
        #     df[f"{mubiao}_rank"]=df.groupby(timetarget,group_keys=False)[f"{mubiao}"].rank(ascending=True)
        #     df=df.groupby(timetarget,group_keys=False).apply(lambda x: x.assign(
        #         **{f"{mubiao}_rank_rate": (x[f"{mubiao}_rank"]/len(x))}
        #         ))
        #     #处理前的因子排名
        #     df = df.dropna(subset=[f"{mubiao}处理前"])#去掉空值
        #     df[f"{mubiao}处理前_rank"]=df.groupby(timetarget,group_keys=False)[f"{mubiao}处理前"].rank(ascending=True)
        #     df=df.groupby(timetarget,group_keys=False).apply(lambda x: x.assign(
        #         **{f"{mubiao}处理前_rank_rate": (x[f"{mubiao}处理前_rank"]/len(x))}
        #         ))

        ranklist=[
            "总市值",
            # "收盘均价比",
            #   "标准差调整的线性回归斜率总市值",
            #   "标准差调整的线性回归斜率涨跌幅",
            #   "标准差调整的线性回归斜率10日乖离率"
                ]
        
        # window_size=3#计算三日最高点偏离的rank分布的收益率
        # ranklist.append(f"{window_size}日次日开盘价格与最高价格比值")
        # window_size=20
        # ranklist.append(f"{window_size}日内振幅动量")

        # ranklist=["年化波动率","收盘均价比","隔日涨幅","日内涨幅","日内振幅","换手率","成交额","总市值"]
        # if "可转债" in path:#这个排名管用
        #     newrank=["三低指数"]
        #     for rank in newrank:
        #         ranklist.append(rank)
        # if "全体A股" in path:
        #     # newrank=["净流入庄家金额成交额比"]
        #     # newrank=["金额流入率","总主动卖出庄家金额","总被动卖出庄家金额","总主动买入庄家金额","总被动买入庄家金额","总卖出庄家金额","总买入庄家金额","净流入庄家金额","净流入庄家金额成交额比"]
        #     newrank=["归母净利润","基本每股收益","归母净利润季度增长率","净资产年度增长率","股息率","每股未分配利润"]
        #     for rank in newrank:
        #         ranklist.append(rank)
        
        # window_size=10
        # df[f"{window_size}日乖离率均线"]=df[f"{window_size}日乖离率"]/df[f"{window_size}日乖离率均线乖离率"]
        # newrank=["累积隔日涨幅ABS","累积隔日涨幅ABS归一化","趋势强度",f"{window_size}日乖离率",f"{window_size}日乖离率均线乖离率",f"{window_size}日乖离率均线"]
        # for rank in newrank:
        #     ranklist.append(rank)

        #列处理【添加上含有标准差相关因子的的列】
        # newrank=[column for column in df.columns if ("标准差" in column)]
        newrank=[column for column in df.columns if ("量价相关性" in column)or("标准差" in column)]
        for rank in newrank:
            ranklist.append(rank)

        print(ranklist)
        for mubiao in ranklist:
            # df = df.dropna(subset=[mubiao])#去掉空值【如果不去的话可能导致报错】
            df[f"{mubiao}_rank"]=df.groupby(timetarget,group_keys=False)[f"{mubiao}"].rank(ascending=True)
            df=df.groupby(timetarget,group_keys=False).apply(lambda x: x.assign(
                **{f"{mubiao}_rank_rate": (x[f"{mubiao}_rank"]/len(x))}
                ))

        # #打印部分标的
        # printdf=df[(df["累积隔日涨幅ABS_rank_rate"]<=0.05)]
        # printdf.to_csv("printdf.csv")

        # if "全体A股" in path:
        #     df["基本面打分"]=0
        #     for rank in newrank:
        #         df["基本面打分"]+=df[f"{rank}_rank_rate"]
        #     # df[f"基本面打分_rank"]=df.groupby(timetarget,group_keys=False)[f"基本面打分"].rank(ascending=True)
        #     df[f"基本面打分_rank"]=df.groupby(timetarget,group_keys=False)[f"基本面打分"].rank(ascending=False)#基本面打分越大越好
        #     df=df.groupby(timetarget,group_keys=False).apply(lambda x: x.assign(
        #         **{f"基本面打分_rank_rate": (x[f"基本面打分_rank"]/len(x))}
        #         ))
            
        # df["综合打分"]=df["10日乖离率_rank_rate"]+df["基本面打分_rank_rate"]+df["总市值_rank_rate"]
        # df[f"综合打分_rank"]=df.groupby(timetarget,group_keys=False)[f"综合打分"].rank(ascending=True)
        # df=df.groupby(timetarget,group_keys=False).apply(lambda x: x.assign(
        #     **{f"综合打分_rank_rate": (x[f"综合打分_rank"]/len(x))}
        #     ))
        # df = df.loc[:,~df.columns.str.contains('Unnamed')]#去掉包含Unnamed的列
        # df.to_csv("每日因子值.csv")
        # newdf=df.groupby(timetarget,group_keys=False).apply(lambda x: x.nsmallest(30,"综合打分"))
        # newdf.to_csv("每日因子值（前三十）.csv")
        
        # 统计收益的时候不能注重平均涨跌幅，更应该统计逐日累乘净值
        for thiscsv in [f"{path}"]:
            df=df.sort_values(by=timetarget)#以日期列为索引,避免计算错误
            # 删除数据类型不是float或者int的列
            non_float_cols = df.select_dtypes(exclude="float").columns.tolist()
            non_int_cols = df.select_dtypes(exclude="int").columns.tolist()
            intersection = list(set(non_float_cols) & set(non_int_cols))
            df = df.drop(intersection,axis=1)

            print("准备统计各个因子rank之后不同区间的未来收益")
            # #排名类多指标组合
            sorttype="rank"
            for holddays in [1,3,5,7]:
            # for holddays in [1,3]:
                all_result_df=pd.DataFrame({})
                ranges=[]
                left=0
                right=1
                step=(right-left)/a
                for i in range(a):
                    ranges.append((left+i*step,left+(i+1)*step))
                # 生成收益率分布表
                # result_df=pd.DataFrame({})
                # 循环处理每个指标和区间
                thiscolumns=df.filter(like="_rank_rate").columns.tolist() # 筛选出列名中包含"rank"的列
                # thiscolumns=[column for column in thiscolumns if "乖离率" in column]
                for rank_range in ranges:
                    result_df=pd.DataFrame() # 创建一个空的DataFrame，用于存储指标的结果
                    for mubiao in thiscolumns:
                        # 根据区间筛选DataFrame
                        thisdf=df[(df[mubiao]>=rank_range[0])&(df[mubiao]<rank_range[1])]
                        #计算逐日数据【可以输出数据看看这个逐日数据对不对】
                        thisdf[f"target_stock_mean{holddays}"]=thisdf.groupby(timetarget,group_keys=False)["target_stock"].transform("mean")
                        mean_thisdf=thisdf.copy().groupby(timetarget,group_keys=False).apply(lambda x:x[:1]).reset_index(0,drop=True)
                        mean_thisdf[f"target_stock_mean{holddays}"].fillna(0,inplace=True) # 将"target_stock_mean"列中缺失值填充为 0
                        # 计算不同因子值的收益分布
                        # print(len(thisdf))
                        # 逐日累乘净值
                        thisvalue=(mean_thisdf[f"target_stock_mean{holddays}"]+1).cumprod().dropna(axis=0).values
                        # thisvalue=[x for x in thisvalue if x != None]
                        if len(thisvalue)==1:
                            cummax=np.maximum.accumulate(thisvalue)
                            drawdown=(cummax-thisvalue)/cummax
                            max_drawdown=np.max(drawdown)
                            thisvalue=thisvalue[0]
                            # print(max_drawdown,thisvalue,type(thisvalue))
                        elif len(thisvalue)>1:
                            cummax=np.maximum.accumulate(thisvalue)
                            drawdown=(cummax-thisvalue)/cummax
                            max_drawdown=np.max(drawdown)
                            thisvalue=thisvalue[-1]
                            # print(max_drawdown,thisvalue,type(thisvalue))
                        else:
                            max_drawdown=0
                            thisvalue=[]
                        # 计算收益
                        thisdf_mean=thisdf.mean(numeric_only=True) # 均值法
                        # 构造包含指标名和涨跌幅的DataFrame，并添加到列结果DataFrame中
                        onedf=pd.DataFrame({
                            mubiao:[thisdf_mean[f"target_stock{holddays}"]],
                            f"{mubiao}逐日累乘净值":[thisvalue],
                            },
                            index=[rank_range])
                        result_df=pd.concat([result_df,onedf],axis=1)
                    all_result_df=pd.concat([all_result_df,result_df])
                # 新建涨跌分布文件夹在上级菜单下，并保存结果
                if not os.path.exists(f"{basepath}/{path}资产多指标平均收益分布{tradetype}"):
                    os.makedirs(f"{basepath}/{path}资产多指标平均收益分布{tradetype}")
                all_result_df.round(decimals=6).to_csv(f"{basepath}/{path}资产多指标平均收益分布{tradetype}/持有{holddays}日平均收益分布.csv")
                print(f"排名类因子{holddays}日收益输出完毕")

            print("准备统计各个因子值本身不同区间的未来收益")
            sorttypes=["等长度","等样本"]
            for sorttype in sorttypes:
                # # 普通类单指标展现
                # thiscolumns=[column for column in df.columns if not ((
                #     "target" in column)or(
                #     "Unnamed" in column)or(
                #     "float" in column)or(
                #     "_rate" in column))]

                #标准差相关列的处理
                # thiscolumns=[column for column in df.columns if ("标准差" in column)and("rank" not in column)]
                thiscolumns=[column for column in df.columns if(("量价相关性" in column)and("rank" not in column))or(("标准差" in column)and("rank" not in column))]
                # thiscolumns.append("累积隔日涨幅ABS")
                # window_size=20
                # thiscolumns.append(f'{window_size}日内振幅动量')
                for mubiao in thiscolumns:
                    all_result_df=pd.DataFrame({})
                    for holddays in [1,3,5,7]:
                        print(mubiao,f"输出{holddays}日收益分布")
                        if sorttype=="等样本":
                            # 等样本分段
                            sorted_list=np.sort(df[f"{mubiao}"].copy())#排序
                            indices=np.linspace(0,len(df[f"{mubiao}"].copy()),num=a+1,endpoint=True,dtype=int) #分段
                            ranges=[]
                            for i in range(len(indices)-1):
                                start_idx=indices[i]
                                end_idx=indices[i+1] if i !=(len(indices)-2) else len(df[f"{mubiao}"].copy()) # 最后一段需要特殊处理
                                upper_bound=sorted_list[end_idx-1] # 注意索引从0开始，因此要减1
                                ranges.append((sorted_list[start_idx],upper_bound))
                            maxnum=sorted_list[-1]
                            minnum=sorted_list[0]
                            print(maxnum,minnum)
                        elif sorttype=="等长度":
                            #等长度分段【排序后取值更加准确】
                            sorted_list = df[f"{mubiao}"].copy().tolist()
                            sorted_list.sort(reverse=True)#目标列转列表并从大到小排序
                            maxnum=sorted_list[0]
                            minnum=sorted_list[-1]

                            # #等长度分段【直接取min、max，容易受到精度干扰】
                            # maxnum=df[f"{mubiao}"].copy().max()
                            # minnum=df[f"{mubiao}"].copy().min()
                            
                            print(maxnum,minnum)
                            # 等长度分段
                            ranges=[]
                            for i in range(0,a):
                                start_idx=minnum+(i/a)*(maxnum-minnum)
                                end_idx=start_idx+(1/a)*(maxnum-minnum)
                                ranges.append([start_idx,end_idx])
                            # print(ranges)
                        # 生成收益率分布表
                        result_df=pd.DataFrame({})
                        value_df=pd.DataFrame({})
                        for rank_range in ranges:
                            thisdf=df.copy()
                            thisdf=thisdf[(thisdf[f"{mubiao}"]>=rank_range[0])&(thisdf[f"{mubiao}"]<rank_range[1])]
                            #计算总的数据
                            up_thisdf=thisdf[thisdf[f"target_stock{holddays}"]>0].copy()
                            zero_thisdf=thisdf[thisdf[f"target_stock{holddays}"]==0].copy()
                            down_thisdf=thisdf[thisdf[f"target_stock{holddays}"]<0].copy()
                            #计算逐日数据【可以输出数据看看这个逐日数据对不对】
                            thisdf[f"target_stock_mean{holddays}"]=thisdf.groupby(timetarget,group_keys=False)["target_stock"].transform("mean")
                            mean_thisdf=thisdf.copy().groupby(timetarget,group_keys=False).apply(lambda x:x[:1]).reset_index(0,drop=True)
                            mean_thisdf[f"target_stock_mean{holddays}"].fillna(0,inplace=True) # 将"target_stock_mean"列中缺失值填充为 0
                            # 计算不同因子值的收益分布
                            # print(len(thisdf))
                            # 逐日累乘净值
                            thisvalue=(mean_thisdf[f"target_stock_mean{holddays}"]+1).cumprod().dropna(axis=0).values
                            # thisvalue=[x for x in thisvalue if x != None]
                            if len(thisvalue)==1:
                                cummax=np.maximum.accumulate(thisvalue)
                                drawdown=(cummax-thisvalue)/cummax
                                max_drawdown=np.max(drawdown)
                                thisvalue=thisvalue[0]
                                # print(max_drawdown,thisvalue,type(thisvalue))
                            elif len(thisvalue)>1:
                                cummax=np.maximum.accumulate(thisvalue)
                                drawdown=(cummax-thisvalue)/cummax
                                max_drawdown=np.max(drawdown)
                                thisvalue=thisvalue[-1]
                                # print(max_drawdown,thisvalue,type(thisvalue))
                            else:
                                max_drawdown=0
                                thisvalue=[]
                            ondf=pd.DataFrame({
                                f"{tradetype}模块的{mubiao}{sorttype}指标值区间": [f"[{rank_range[0]:.6f},{rank_range[1]:.6f}]"],
                                f"未来{holddays}日上涨次数":[len(up_thisdf)],
                                # f"未来{holddays}日横盘次数":[len(zero_thisdf)],
                                # f"未来{holddays}日下跌次数":[len(down_thisdf)],
                                f"未来总次数":[len(thisdf)],
                                f"未来{holddays}日平均涨跌幅":[thisdf[f"target_stock{holddays}"].mean()],
                                # f"未来{holddays}日日均涨跌幅平均绝对误差":[
                                #     np.mean(np.absolute(mean_thisdf[f"target_stock_mean{holddays}"]-thisdf[f"target_stock{holddays}"].mean()))
                                #     ],
                                # f"未来{holddays}日日均涨跌幅均方误差":[
                                #     np.mean(np.square(mean_thisdf[f"target_stock_mean{holddays}"]-thisdf[f"target_stock{holddays}"].mean()))
                                #     ],
                                # f"逐日累乘净值":[thisvalue],
                                # f"逐日最大回撤":[max_drawdown],
                                # f"":["本行用于不同表单的间隔无意义"],
                                })
                            ondf.set_index(f"{tradetype}模块的{mubiao}{sorttype}指标值区间",inplace=True)
                            result_df=pd.concat([result_df,ondf])
                        # # #每个表单独生成一个文件
                        # if not os.path.exists(f"{basepath}/{path}资产{n}日单指标平均收益分布{tradetype}{mubiao}"):
                        #     os.makedirs(f"{basepath}/{path}资产{n}日单指标平均收益分布{tradetype}{mubiao}")
                        # result_df.round(decimals=6).to_csv(f"{basepath}/{path}资产{n}日单指标平均收益分布{tradetype}{mubiao}/{tradetype}{sorttype}持有{n}日平均收益分布.csv")
                        
                        #这个是新版的一堆因子怼进一个表的情况
                        # result_df=result_df.reset_index(drop=True)
                        if all_result_df.empty:
                            all_result_df=pd.concat([all_result_df,result_df])
                        else:
                            all_result_df=pd.concat([all_result_df,result_df],axis=1)
                    if not os.path.exists(f"{basepath}/{path}资产{sorttype}单指标平均收益分布{tradetype}{mubiao}"):
                        os.makedirs(f"{basepath}/{path}资产{sorttype}单指标平均收益分布{tradetype}{mubiao}")
                    all_result_df.round(decimals=6).to_csv(f"{basepath}/{path}资产{sorttype}单指标平均收益分布{tradetype}{mubiao}/{tradetype}{sorttype}平均收益分布.csv")
                    all_result_df=pd.DataFrame({})
                    print("任务已经完成")
