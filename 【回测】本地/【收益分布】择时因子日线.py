import pandas as pd
import numpy as np
import os
import datetime
import time

def technology(df): #定义计算技术指标的函数
    try:
        df=df.sort_values(by=timetarget) #以日期列为索引,避免计算错误
        #df=df.sort_values(by=timetarget,ascending=False) #从大到小排序 
        
        df.loc[df["开盘涨停"].copy().shift(-1)==1,"次日开盘涨停"]=1
        df.loc[df["开盘跌停"].copy().shift(-1)==1,"次日开盘跌停"]=1
        df.loc[df["收盘涨停"].copy().shift(-1)==1,"次日收盘涨停"]=1
        df.loc[df["收盘跌停"].copy().shift(-1)==1,"次日收盘跌停"]=1
        
        #未来-holddays-1日价格除以当下价格就是holddays周期之后的涨跌幅隔日涨幅
        df["target_stock"]=(df["真实开盘价格"].copy().shift(-holddays-1)/(df["真实开盘价格"].copy().shift(-1)))-1
        # if "可转债" not in path:
        #     thisshort=5
        #     tiislong=20
        #     df=df.iloc[tiislong:]
        #     df[f"个股均线强度"]=df[f"{thisshort}日均线"]/df[f"{tiislong}日均线"]
    except Exception as e:
        print(f"发生bug: {e}")
    return df

# MAD:中位数去极值
def extreme_MAD(dt,n):
    median = dt.quantile(0.5) #找出中位数
    new_median = (abs((dt - median)).quantile(0.5)) #偏差值的中位数
    dt_up = median + n*new_median #上限
    dt_down = median - n*new_median #下限
    return dt_up,dt_down

# 设置参数
a=20 # 将数据划分成a个等距离的区间
# global holddays
holddays=1 # 观察不同的持仓周期的涨跌分布

tradetypes=["小市值","大市值","全部"]
# tradetypes=["全部"]
# tradetypes=["小市值"]
# tradetypes=["大市值"]
basepath=r"C:\Users\13480\Desktop\quant\【回测】本地\数据文件"
# basepath=r"/home/wth000/gitee/quant/【回测】本地/数据文件"

# computer=True # 确认是否重新计算指标
computer=False # 确认是否重新计算指标

# paths=[r"全体A股",r"半小时资金流",r"半小时量价"]
paths=[r"全体A股"]
for path in paths:
    if path==r"全体A股":
        timetarget="floattoday"
    elif path==r"半小时资金流": #文件夹路径
        timetarget="float价格分时"
    elif path==r"半小时量价": #文件夹路径
        timetarget="float价格分时"

    if computer==True:
        for tradetype in tradetypes:
            print("path",path,"tradetype",tradetype)
            df=pd.read_csv(f"{basepath}/{path}/{path}{tradetype}.csv")
            #重新计算收益率
            df=df.groupby("代码",group_keys=False).apply(lambda x:technology(x)) #重新计算涨跌幅
            print(df)
            # #过滤垃圾股
            # df=df[df["代码"].str.startswith(("60","00","30"))]#只要沪深主板创业板
            # df=df[df["开盘"]>4]
            # df=df[df["归母净利润"]>0]

            df[f"{tradetype}成交额"]=df.groupby(timetarget)["成交额"].transform("sum")
            df[f"{tradetype}总市值"]=df.groupby(timetarget)["总市值"].transform("sum")
            df[f"{tradetype}换手率"]=df[f"{tradetype}成交额"]/df[f"{tradetype}总市值"]
            
            # df[f"{tradetype}平均均线强度"]=df.groupby(timetarget)["个股均线强度"].transform("mean")
            if "全体A股" in path:
                df[f"{tradetype}平均隔日涨幅"]=df.groupby(timetarget)["隔日涨幅"].transform("mean") # 平均数

            #计算预期收益相关指标
            df[f"{tradetype}平均target_stock"]=df.groupby(timetarget)["target_stock"].transform("mean") # 平均数
            df[f"{tradetype}平均日内涨幅"]=df.groupby(timetarget)["日内涨幅"].transform("mean") # 平均数
            
            df[f"{tradetype}上涨家数"]=df.groupby(timetarget)["上涨"].transform("sum") # 平均数
            df[f"{tradetype}下跌家数"]=df.groupby(timetarget)["下跌"].transform("sum") # 平均数
            df[f"{tradetype}上涨比例"]=df.groupby(timetarget)[f"{tradetype}上涨家数"].transform(lambda x: x / len(x))
            df[f"{tradetype}下跌比例"]=df.groupby(timetarget)[f"{tradetype}下跌家数"].transform(lambda x: x / len(x))
            # df[f"{tradetype}涨停家数"]=df.groupby(timetarget)["涨停"].transform("sum") # 平均数
            # df[f"{tradetype}跌停家数"]=df.groupby(timetarget)["跌停"].transform("sum") # 平均数
            # df[f"{tradetype}涨停比例"]=df.groupby(timetarget)[f"{tradetype}涨停家数"].transform(lambda x: x / len(x))
            # df[f"{tradetype}跌停比例"]=df.groupby(timetarget)[f"{tradetype}跌停家数"].transform(lambda x: x / len(x))

            # try:
            #     df[f"{tradetype}平均金额流入率"]=df.groupby(timetarget)["金额流入率"].transform("mean")
            #     df["总主动卖出庄家金额"]=df["主动卖出特大单金额"]+df["主动卖出大单金额"]
            #     df["总被动卖出庄家金额"]=df["被动卖出特大单金额"]+df["被动卖出大单金额"]
            #     df["总主动买入庄家金额"]=df["主动买入特大单金额"]+df["主动买入大单金额"]
            #     df["总被动买入庄家金额"]=df["被动买入特大单金额"]+df["被动买入大单金额"]
            #     df["总卖出庄家金额"]=df["总主动卖出庄家金额"]+df["总被动卖出庄家金额"]
            #     df["总买入庄家金额"]=df["总主动买入庄家金额"]+df["总被动买入庄家金额"]
            #     df["净流入庄家金额"]=df["总买入庄家金额"]-df["总卖出庄家金额"]
            #     # df[f"{tradetype}成交额"].fillna(0, inplace=True)#有成交额为空的情况
            #     df[f"{tradetype}庄家净流入"]=df.groupby(timetarget)["净流入庄家金额"].transform("sum")
            #     df[f"{tradetype}庄家净流入成交额比"]=df.apply(lambda row: row[f"{tradetype}庄家净流入"] / row[f"{tradetype}成交额"] if row[f"{tradetype}成交额"] != 0 else 0, axis=1)
            #     # df[f"{tradetype}庄家净流入成交额比"]=df[f"{tradetype}庄家净流入"]/df[f"{tradetype}成交额"]
            #     df[f"{tradetype}庄家净流入总市值比"]=df[f"{tradetype}庄家净流入"]/df[f"{tradetype}总市值"]
            # except Exception as e:
            #     print(e)
            
            dfcolumns=[column for column in df.columns if (f"{tradetype}" in column)or(timetarget in column)or("float" in column)]
            print(dfcolumns)
            df=df[dfcolumns]
            df=df.groupby(timetarget).apply(lambda x: x.head(1))
            df.to_csv(f"{path}{tradetype}{holddays}日.csv")
            
for path in paths:
    dt=pd.DataFrame({})
    for tradetype in tradetypes:
        df=pd.read_csv(f"{path}{tradetype}{holddays}日.csv")
        dfcolumns=[column for column in df.columns if (f"{tradetype}" in column)or(timetarget in column)or("float" in column)]
        print(dfcolumns)
        df=df[dfcolumns]
        if tradetype in ["全部","大市值","小市值"]:
            df=df.reset_index(drop=True)
            if dt.empty:
                dt=pd.concat([dt,df])
            else:
                dt=dt.merge(df,on=timetarget)
    dt.to_csv(f"{path}大小盘切换{holddays}日.csv")
    df=pd.read_csv(f"{path}大小盘切换{holddays}日.csv")
    df=df.iloc[100:]#去除前100条数据排除空值
    df=df.sort_values(by=timetarget, ascending=True)#从小到大
    # df=df.sort_values(by=timetarget, ascending=False)
    # df=df.loc[:-200]#排除最后200条数据验证均线对不对
    print(df)
    
    if r"全体A股" in path:
        import akshare as ak#指数没有半小时线
        # 获取A股指数代码列表
        codes = ["000001","399001"]
        indexdf=pd.DataFrame({})
        for code in codes:
            # 通过 akshare 获取目标指数的日K线数据
            data = ak.index_zh_a_hist(symbol=code,period="daily")
            print(data)
            data[f"{code}开盘"]=data[f"开盘"]
            data[f"{code}收盘"]=data[f"收盘"]
            data=data[["日期",f"{code}开盘",f"{code}收盘"]]
            # print(data)
            if indexdf.empty:
                indexdf=pd.concat([indexdf,data])
            else:
                indexdf=indexdf.merge(data,on="日期")
        indexdf[timetarget]=indexdf["日期"].str.replace("-","").astype(float)
        indexdf.to_csv("沪深指数.csv")
        print(indexdf)
        indexdf=pd.read_csv("沪深指数.csv")
        indexdf["沪深收盘"]=indexdf["000001收盘"]+indexdf["399001收盘"]
        indexdf["沪深收盘涨跌幅"]=indexdf["沪深收盘"].shift(-1)/indexdf["沪深收盘"]-1
        indexdf["沪深开盘"]=indexdf["000001开盘"]+indexdf["399001开盘"]
        indexdf["沪深开盘涨跌幅"]=indexdf["沪深开盘"].shift(-1)/indexdf["沪深开盘"]-1
        df=df.merge(indexdf,on=timetarget)
        df[f"沪深收盘涨跌幅净值"]=(df[f"沪深收盘涨跌幅"]+1).cumprod()
        for tradetype in tradetypes:
            df[f"{tradetype}净值"]=(df[f"{tradetype}平均target_stock"]+1).cumprod()
            df[f"历史{tradetype}净值"]=df[f"{tradetype}净值"].copy().shift(1)
        print(len(df))
    
    thisshort=10
    for tradetype in tradetypes:        
        df[f"{tradetype}{thisshort}日线"]=df[f"历史{tradetype}净值"].rolling(thisshort).mean()
        df[f"{tradetype}{thisshort}高点"]=df[f"历史{tradetype}净值"].rolling(thisshort).max()
        df[f"{tradetype}{thisshort}低点"]=df[f"历史{tradetype}净值"].rolling(thisshort).min()
        df[f"{tradetype}{thisshort}均值"]=(df[f"{tradetype}{thisshort}高点"]+df[f"{tradetype}{thisshort}低点"])/2
        #高低点
        df[f"{tradetype}均线强度【高低点】"]=df[f"历史{tradetype}净值"]/df[f"{tradetype}{thisshort}均值"]
        df.loc[df[f"{tradetype}均线强度【高低点】"]>=1.1,f"{tradetype}均线强度【高低点】"]=1.1
        df.loc[df[f"{tradetype}均线强度【高低点】"]<=0.9,f"{tradetype}均线强度【高低点】"]=0.9
        df[f"{tradetype}均线强度刻度【高低点】"]=(2*(df[f"{tradetype}均线强度【高低点】"]-(2)/2)/(0.2))
        #乖离率
        df[f"{tradetype}均线强度【乖离率】"]=df[f"历史{tradetype}净值"]/df[f"{tradetype}{thisshort}日线"]
        df.loc[df[f"{tradetype}均线强度【乖离率】"]>=1.1,f"{tradetype}均线强度【乖离率】"]=1.1
        df.loc[df[f"{tradetype}均线强度【乖离率】"]<=0.9,f"{tradetype}均线强度【乖离率】"]=0.9
        df[f"{tradetype}均线强度刻度【乖离率】"]=(2*(df[f"{tradetype}均线强度【乖离率】"]-(2)/2)/(0.2))

        # df[f"{tradetype}均线强度"]=df[f"历史{tradetype}净值"]/df[f"{tradetype}{thisshort}日线"]
        # df.loc[(df[f"{tradetype}均线强度"]>1)&(df[f"{tradetype}均线强度"].copy().shift(1)<1),f"{tradetype}金叉"]=1
        # df.loc[(df[f"{tradetype}均线强度"]<1)&(df[f"{tradetype}均线强度"].copy().shift(1)>1),f"{tradetype}死叉"]=1
        # df.loc[df[f"{tradetype}金叉"]==1,f"{tradetype}交叉状态"]="金叉"
        # df.loc[df[f"{tradetype}死叉"]==1,f"{tradetype}交叉状态"]="死叉"
        # df[f"{tradetype}交叉状态填充后"]=df[f"{tradetype}交叉状态"].fillna(method='ffill')
        # #因子去空值
        # df.dropna(subset=[f"{tradetype}交叉状态填充后"])
        # df=df.sort_values(by=timetarget)
        # thisnum=0
        # thisstaut=0
        # for index,thisdf in df.iterrows():
        #     # print(index,thisdf)
        #     floattoday=thisdf["floattoday"]
        #     print(floattoday,)
        #     if thisdf[f"{tradetype}交叉状态填充后"]!=thisstaut:
        #         thisnum=0
        #     else:
        #         thisnum+=1
        #     df.loc[df["floattoday"]==floattoday,f"{tradetype}交叉间隔"]=thisnum
        #     thisstaut=thisdf[f"{tradetype}交叉状态填充后"]
        #     print(thisstaut)

    kedunbames=["上涨比例",] # "上涨下跌比例"
    slow=12
    fast=3
    for kedunbame in kedunbames:
        for tradetype in tradetypes:
            df[f"{tradetype}{kedunbame}{slow}日线"]=df[f"{tradetype}{kedunbame}"].rolling(slow).mean()
            df[f"{tradetype}{kedunbame}{fast}日线"]=df[f"{tradetype}{kedunbame}"].rolling(fast).mean()
            # df[f"{tradetype}{kedunbame}{slow}日线"]=df[f"{tradetype}{kedunbame}"].ewm(span=slow, adjust=False).mean()
            # df[f"{tradetype}{kedunbame}{fast}日线"]=df[f"{tradetype}{kedunbame}"].ewm(span=fast, adjust=False).mean()
            # thisfast,thisslow=StochRSI(df[f"{tradetype}庄家净流入成交额比"],14,3)
            # print(len(thisfast),len(thisslow))
            # slow="慢"
            # fast="快"
            # df[f"{tradetype}{kedunbame}{slow}日线"]=thisslow
            # df[f"{tradetype}{kedunbame}{fast}日线"]=thisfast
            df[f"{tradetype}{kedunbame}{slow}、{fast}均线均值"]=(df[f"{tradetype}{kedunbame}{slow}日线"]+df[f"{tradetype}{kedunbame}{fast}日线"])/2
            df[f"{tradetype}{kedunbame}{slow}、{fast}均线差"]=df[f"{tradetype}{kedunbame}{fast}日线"]-df[f"{tradetype}{kedunbame}{slow}日线"]
            df.loc[(df[f"{tradetype}{kedunbame}{slow}、{fast}均线差"]>0)&(df[f"{tradetype}{kedunbame}{slow}、{fast}均线差"].copy().shift(1)<0),f"{tradetype}{kedunbame}金叉"]=1
            df.loc[(df[f"{tradetype}{kedunbame}{slow}、{fast}均线差"]<0)&(df[f"{tradetype}{kedunbame}{slow}、{fast}均线差"].copy().shift(1)>0),f"{tradetype}{kedunbame}死叉"]=1
            df[f"{tradetype}平均target_stock历史周期均线"]=df[f"{tradetype}平均target_stock"].rolling(200).mean().copy().shift(1)#计算当前周期的平均涨跌幅统计误差
            # df[f"{tradetype}成交额极大值"] = df[f"{tradetype}成交额"].rolling(10).max()
            # df[f"{tradetype}成交额极小值"] = df[f"{tradetype}成交额"].rolling(10).min()
            # df[f"{tradetype}净值极大值"] = df[f"{tradetype}净值"].rolling(10).max()
            # df[f"{tradetype}净值极小值"] = df[f"{tradetype}净值"].rolling(10).min()
            df.loc[df[f"{tradetype}{kedunbame}金叉"]==1,f"{tradetype}{kedunbame}交叉状态"]="金叉"
            df.loc[df[f"{tradetype}{kedunbame}死叉"]==1,f"{tradetype}{kedunbame}交叉状态"]="死叉"  
            df[f"{tradetype}{kedunbame}交叉状态填充后"]=df[f"{tradetype}{kedunbame}交叉状态"].fillna(method='ffill')
            # df[f"{tradetype}{kedunbame}交叉状态填充后"]=df[f"{tradetype}{kedunbame}交叉状态"].fillna(method='bfill')
            
        # 设置200天的windows长度
        windowslong=200
        rollingdf=df.rolling(window=windowslong)
        for thisdf in rollingdf:
            if len(thisdf)>=windowslong:
                thisday=thisdf[timetarget].values[-1]
                # print(thisday,thisdf)
                for tradetype in tradetypes:#只能根据一个标的确定
                    print(len(thisdf[f"{tradetype}{kedunbame}{slow}日线"]))
                    # 方差法确定上下轨
                    data=pd.concat([thisdf[f"{tradetype}{kedunbame}{slow}日线"],thisdf[f"{tradetype}{kedunbame}{fast}日线"]])
                    dt_up,dt_down = extreme_MAD(data,5.2)
                    # 极端值向临界值靠拢
                    thisdf.loc[thisdf[f"{tradetype}{kedunbame}{slow}、{fast}均线均值"]>=dt_up,f"{tradetype}{kedunbame}{slow}、{fast}均线均值"]=dt_up
                    thisdf.loc[thisdf[f"{tradetype}{kedunbame}{slow}、{fast}均线均值"]<=dt_down,f"{tradetype}{kedunbame}{slow}、{fast}均线均值"]=dt_down
                    # print("双临界值",thisdf,dt_up,dt_down)
                    print("双临界值",dt_up,dt_down)
                    df.loc[df[timetarget]==thisday,f"{tradetype}{windowslong}{kedunbame}均线刻度"]=(2*(thisdf.loc[thisdf[timetarget]==thisday,f"{tradetype}{kedunbame}{slow}、{fast}均线均值"]-(dt_up+dt_down)/2)/(dt_up-dt_down))
                    df[f"{tradetype}{windowslong}{kedunbame}均线刻度组合【乖离率】"]=df[f"{tradetype}{windowslong}{kedunbame}均线刻度"]+df[f"{tradetype}均线强度刻度【乖离率】"]
                    df[f"{tradetype}{windowslong}{kedunbame}均线刻度组合【高低点】"]=df[f"{tradetype}{windowslong}{kedunbame}均线刻度"]+df[f"{tradetype}均线强度刻度【高低点】"]
        print(f"{path}标准化完成",len(df))
       
        # # 设置1000天的windows长度
        # windowslong=1000
        # rollingdf=df.rolling(window=windowslong)
        # for thisdf in rollingdf:
        #     if len(thisdf)>=windowslong:
        #         thisday=thisdf[timetarget].values[-1]
        #         # print(thisday,thisdf)
        #         for tradetype in tradetypes:#只能根据一个标的确定
        #             print(len(thisdf[f"{tradetype}{kedunbame}{slow}日线"]))
        #             # 方差法确定上下轨
        #             data=pd.concat([thisdf[f"{tradetype}{kedunbame}{slow}日线"],thisdf[f"{tradetype}{kedunbame}{fast}日线"]])
        #             dt_up,dt_down = extreme_MAD(data,5.2)
        #             # 极端值向临界值靠拢
        #             thisdf.loc[thisdf[f"{tradetype}{kedunbame}{slow}、{fast}均线均值"]>=dt_up,f"{tradetype}{kedunbame}{slow}、{fast}均线均值"]=dt_up
        #             thisdf.loc[thisdf[f"{tradetype}{kedunbame}{slow}、{fast}均线均值"]<=dt_down,f"{tradetype}{kedunbame}{slow}、{fast}均线均值"]=dt_down
        #             # print("双临界值",thisdf,dt_up,dt_down)
        #             print("双临界值",dt_up,dt_down)
        #             df.loc[df[timetarget]==thisday,f"{tradetype}{windowslong}{kedunbame}均线刻度"]=(2*(thisdf.loc[thisdf[timetarget]==thisday,f"{tradetype}{kedunbame}{slow}、{fast}均线均值"]-(dt_up+dt_down)/2)/(dt_up-dt_down))
        #             df[f"{tradetype}{windowslong}{kedunbame}均线刻度组合【乖离率】"]=df[f"{tradetype}{windowslong}{kedunbame}均线刻度"]+df[f"{tradetype}均线强度刻度【乖离率】"]
        #             df[f"{tradetype}{windowslong}{kedunbame}均线刻度组合【高低点】"]=df[f"{tradetype}{windowslong}{kedunbame}均线刻度"]+df[f"{tradetype}均线强度刻度【高低点】"]
        # print(f"{path}标准化完成",len(df))

    # for tradetype in tradetypes:
    #     df[f"{tradetype}双因子"]=0
    #     for kedunbame in kedunbames:
    #         df[f"{tradetype}双因子"]+=df[f"{tradetype}{kedunbame}均线刻度"]
    #         print(df[f"{tradetype}双因子"].values[0],df[f"{tradetype}{kedunbame}均线刻度"].values[0])
    # df=df[windowslong:]
    
    df.to_csv(f"{path}标准化完成.csv")
    for tradetype in tradetypes:
        all_result_df=pd.DataFrame({})
        sorttypes=["等样本","等长度"]
        for sorttype in sorttypes:
            try:
                ### 统计收益率分布【等样本和等距离两种】###
                df=pd.read_csv(f"{path}标准化完成.csv")
                print(len(df))
                
                # #金叉死叉需要单独输出
                # df=df[df[f"{tradetype}{kedunbame}交叉状态填充后"]=="死叉"]
                # df=df[df[f"{tradetype}{kedunbame}交叉状态填充后"]=="金叉"]
                
                print("path",path,"tradetype",tradetype)
                
                # #固定待研究因子值
                # thiscolumns=[]
                # for kedunbame in kedunbames:
                #     thiscolumns.append(f"{tradetype}{kedunbame}均线刻度")
                #     thiscolumns.append(f"{tradetype}{kedunbame}")
                
                # #双因子
                # thiscolumns=[f"{tradetype}双因子"]
                
                # #交叉间隔
                # df=df[df[f"{tradetype}交叉状态填充后"]=="死叉"]
                # df=df[df[f"{tradetype}交叉状态填充后"]=="金叉"]
                # thiscolumns=[f"{tradetype}交叉间隔"]
                
                # #涨跌幅绝对值
                # # df[f"{tradetype}平均隔日涨幅"]=df[f"{tradetype}平均隔日涨幅"]-1
                # df[f"{tradetype}平均日内涨幅"]=df[f"{tradetype}平均日内涨幅"]-1
                # thiscolumns=[f"{tradetype}平均隔日涨幅"]
                
                # 上涨比例、均线强度
                thiscolumns=[column for column in df.columns if 
                             (f"{tradetype}" in column)
                             and
                             ((
                    # "上涨比例均线刻度" in column)or(
                    # "均线强度刻度" in column)or(
                    "组合" in column)
                    )]
                print(thiscolumns)

                # #全部列
                # thiscolumns=[column for column in df.columns if not ((
                #     "target" in column)or(
                #     "Unnamed" in column)or(
                #     "float" in column)or(
                #     "_rate" in column)or(
                #     "日期" in column)or(
                #     "状态" in column))]
                # print(thiscolumns)
                for mubiao in thiscolumns:
                    for n in [1,3,5,8]:
                        # 统计收益率分布
                        # df[f"{tradetype}平均target_stock"]=df[f"宽基涨跌幅{n}日"]
                        df[f"{tradetype}平均target_stock"]=df[f"历史{tradetype}净值"].shift(-n)/df[f"历史{tradetype}净值"]-1
                        if True:
                            print(mubiao,"输出概率分布")
                            if sorttype=="等样本":
                                # 等样本分段
                                sorted_data=np.sort(df[f"{mubiao}"])#排序
                                indices=np.linspace(0,len(df[f"{mubiao}"]),num=a+1,endpoint=True,dtype=int) #分段
                                ranges=[]
                                for i in range(len(indices)-1):
                                    start_idx=indices[i]
                                    end_idx=indices[i+1] if i!=(len(indices)-2) else len(df[f"{mubiao}"]) # 最后一段需要特殊处理
                                    upper_bound=sorted_data[end_idx-1] # 注意索引从0开始，因此要减1
                                    ranges.append((sorted_data[start_idx],upper_bound))
                                    # print(ranges)
                            elif sorttype=="等长度":
                                maxnum=df[f"{mubiao}"].max()
                                minnum=df[f"{mubiao}"].min()
                                # 等长度分段
                                ranges=[]
                                for i in range(0,a):
                                    start_idx=minnum+i/a*(maxnum-maxnum)
                                    end_idx=start_idx+1/a*(maxnum-maxnum)
                                    ranges.append([start_idx,end_idx])
                                    # print(ranges)
                            print(len(df))
                            result_df=pd.DataFrame({})
                            for rank_range in ranges:
                                thisdf=df.copy()
                                thisdf=thisdf[(thisdf[f"{mubiao}"]>=rank_range[0])&(thisdf[f"{mubiao}"]<rank_range[1])]
                                #计算总的数据
                                up_thisdf=thisdf[thisdf[f"{tradetype}平均target_stock"]>0].copy()
                                zero_thisdf=thisdf[thisdf[f"{tradetype}平均target_stock"]==0].copy()
                                down_thisdf=thisdf[thisdf[f"{tradetype}平均target_stock"]<0].copy()
                                #计算逐日数据【可以输出数据看看这个逐日数据对不对】
                                thisdf["target_stock_mean"]=thisdf.groupby(timetarget)[f"{tradetype}平均target_stock"].transform("mean")
                                mean_thisdf=thisdf.copy().groupby(timetarget,group_keys=False).apply(lambda x:x[:1]).reset_index(0, drop=True)
                                mean_thisdf["target_stock_mean"].fillna(0,inplace=True) # 将"target_stock_mean"列中缺失值填充为 0
                                # 计算不同因子值的收益分布
                                # print(len(thisdf))
                                # 逐日累乘净值
                                thisvalue=(mean_thisdf[f"{tradetype}平均target_stock"]+1).cumprod().dropna(axis=0).values
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
                                    
                                thatdf=df.copy()
                                thatdf=thatdf[(thatdf[f"{mubiao}"]>=rank_range[0])&(thatdf[f"{mubiao}"]<rank_range[1])]
                                dt_up,dt_down = extreme_MAD(thatdf[f"{tradetype}平均target_stock"],5.2)
                                #极端值向临界值靠拢
                                thatdf.loc[thatdf[f"{tradetype}平均target_stock"]>=dt_up,f"{tradetype}平均target_stock"]=dt_up
                                thatdf.loc[thatdf[f"{tradetype}平均target_stock"]<=dt_down,f"{tradetype}平均target_stock"]=dt_down
                                # print("双临界值",thisdf,dt_up,dt_down)
                                
                                ondf=pd.DataFrame({
                                    f"{tradetype}模块的{mubiao}{sorttype}指标值区间": [f"[{rank_range[0]:.6f}, {rank_range[1]:.6f}]"],
                                    # f"未来{n}日上涨次数":[len(up_thisdf)],
                                    # f"未来{n}日横盘次数":[len(zero_thisdf)],
                                    # f"未来{n}日下跌次数":[len(down_thisdf)],
                                    # f"未来总次数":[len(thisdf)],
                                    f"未来{n}日平均涨跌幅":[thisdf[f"{tradetype}平均target_stock"].mean()],
                                    # f"未来{n}日平均涨跌幅【不含极端值】":[thatdf[f"{tradetype}平均target_stock"].mean()],
                                    # f"未来{n}日日均涨跌幅平均绝对误差":[
                                    #     np.mean(np.absolute(mean_thisdf[f"target_stock_mean"]-thisdf[f"{tradetype}平均target_stock"].mean()))
                                    #     ],
                                    # f"未来{n}日日均涨跌幅均方误差":[
                                    #     np.mean(np.square(mean_thisdf[f"target_stock_mean"]-thisdf[f"{tradetype}平均target_stock"].mean()))
                                    #     ],
                                    # f"逐日累乘净值":[thisvalue],
                                    # f"逐日最大回撤":[max_drawdown],
                                    # f"":["本行用于不同表单的间隔无意义"],
                                    })
                                ondf.set_index(f"{tradetype}模块的{mubiao}{sorttype}指标值区间",inplace=True)
                                result_df=pd.concat([result_df,ondf])
                            # # #每个表单独生成一个文件
                            # if not os.path.exists(f"{basepath}/{path}/{path}资产{n}日单指标平均收益分布{tradetype}{mubiao}"):
                            #     os.makedirs(f"{basepath}/{path}/{path}资产{n}日单指标平均收益分布{tradetype}{mubiao}")
                            # result_df.round(decimals=6).to_csv(f"{basepath}/{path}/{path}资产{n}日单指标平均收益分布{tradetype}{mubiao}/{tradetype}{sorttype}持有{n}日平均收益分布.csv")
                            
                            #这个是新版的一堆因子怼进一个表的情况
                            # result_df=result_df.reset_index(drop=True)
                            if all_result_df.empty:
                                all_result_df=pd.concat([all_result_df,result_df])
                            else:
                                all_result_df=pd.concat([all_result_df,result_df], axis=1)
                    if not os.path.exists(f"{basepath}/{path}/{path}资产{sorttype}单指标平均收益分布{tradetype}{mubiao}"):
                        os.makedirs(f"{basepath}/{path}/{path}资产{sorttype}单指标平均收益分布{tradetype}{mubiao}")
                    all_result_df.round(decimals=6).to_csv(f"{basepath}/{path}/{path}资产{sorttype}单指标平均收益分布{tradetype}{mubiao}/{tradetype}{sorttype}平均收益分布.csv")
                    all_result_df=pd.DataFrame({})
                # if not os.path.exists(f"{basepath}/{path}/{path}资产{sorttype}单指标平均收益分布{tradetype}"):
                #     os.makedirs(f"{basepath}/{path}/{path}资产{sorttype}单指标平均收益分布{tradetype}")
                # all_result_df.round(decimals=6).to_csv(f"{basepath}/{path}/{path}资产{sorttype}单指标平均收益分布{tradetype}/{tradetype}{sorttype}平均收益分布.csv")
                # all_result_df=pd.DataFrame({})
                print("任务已经完成")
            except Exception as e:
                print(e)
        
    ###【量价择时】###
    # #平时持仓，价格或者成交额新低空仓
    # df["持仓风格"]="小市值"
    # df.loc[df["小市值净值"].copy().shift(1)<=df["小市值净值极小值"].copy().shift(1),"持仓风格"]="空仓"
    # df.loc[df["小市值成交额"]<=df["小市值成交额极小值"],"持仓风格"]="空仓"
    # #平时空仓，价格或者成交额新高的时候持仓
    # df.loc[(df["小市值平均隔日涨幅"]<0)&(df["大市值平均隔日涨幅"]<0)&(df["全部平均隔日涨幅"]<0),"持仓风格"]="空仓"#交投活跃了选择小市值
    # df.loc[(df["大市值涨停家数"]>=1),"持仓风格"]="小市值"
    # df.loc[df["小市值成交额"]>=df["小市值成交额极大值"],"持仓风格"]="小市值"#交投活跃了选择小市值

    ##加上这个IC和IR就会少数据
    # rollingdf=df.rolling(window=30)
    # for thisdf in rollingdf:
    #     if len(thisdf)>=30:
    #         thisday=thisdf[timetarget].values[-1]
    #         # print(thisday,thisdf)
    #         for tradetype in tradetypes:
    #             df.loc[df[timetarget]==thisday,f"{tradetype}相关性IC"]=thisdf[f"{tradetype}平均target_stock"].copy().shift(-1).corr(thisdf[f"{tradetype}平均target_stock历史周期均线"])
    #         # 在 Pandas 中，corr() 方法默认计算的是 Pearson 相关系数，用于衡量两个变量之间的线性相关性强弱。Pearson 相关系数的取值范围在 -1 到 1 之间，具体含义如下：
    #         # 当 Pearson 相关系数为 1 时，表示两个变量呈完全正相关关系，即一个变量增大时，另一个变量也相应增大。
    #         # 当 Pearson 相关系数为 -1 时，表示两个变量呈完全负相关关系，即一个变量增大时，另一个变量减小。
    #         # 当 Pearson 相关系数接近 0 时，表示两个变量之间基本没有线性相关性。
    #         # 如果需要计算其他类型的相关性，可以在corr()方法中指定method参数，例如：
    #         # method="spearman"：计算 Spearman 秩相关系数，适合处理非线性关系。
    #         # method="kendall"：计算 Kendall 秩相关系数，适合处理非线性关系且对异常值不敏感。
    #         # 在你提供的代码中，并没有指定method参数，因此默认使用的是 Pearson 相关系数进行计算。如果需要其他类型的相关性计算，可以根据需求设定相应的参数。
    # rollingdf=df.rolling(window=30*2)
    # for thisdf in rollingdf:
    #     if len(thisdf)>=30:
    #         thisday=thisdf[timetarget].values[-1]
    #         # print(thisday,thisdf)
    #         for tradetype in tradetypes:
    #             df.loc[df[timetarget]==thisday,f"{tradetype}稳定性IR"]=thisdf[f"{tradetype}相关性IC"].mean()/thisdf[f"{tradetype}相关性IC"].std()
    # print(len(df))
    # df.to_csv(f"{path}因子动态相关性")