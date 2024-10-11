import pandas as pd

# merge=False
merge=True
if merge==True:
    file_path=r"C:\Users\13480\Desktop\quant\【回测】本地\数据文件\分时\分时.csv"
    try:
        dfminute = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        # 如果 utf-8 解码失败，尝试其他常见的编码方式
        try:
            dfminute = pd.read_csv(file_path, encoding='gbk')
        except UnicodeDecodeError:
            # 如果其他编码方式也不行，你可以尝试使用 ISO-8859-1 编码【这个界面】
            dfminute = pd.read_csv(file_path, encoding='ISO-8859-1')
    # dfminute=pd.read_csv(r"C:\Users\13480\Desktop\quant\【回测】本地\数据文件\半小时资金流\半小时资金流.csv")
    dfminute["分时close"]=dfminute["close"]
    dfminute["分时open"]=dfminute["open"]
    dfminute=dfminute[["代码","floattoday","float价格分时","分时close","分时open"]]

    # dfday=pd.read_csv(r"C:\Users\13480\Desktop\quant\【回测】本地\数据文件\全体A股\全体A股全部.csv")
    dfday=pd.read_csv(r"C:\Users\13480\Desktop\quant\【回测】本地\数据文件\全体A股\全体A股小市值.csv")
    timetarget="floattoday"
    dfday=dfday.sort_values(by=timetarget) #以日期列为索引,避免计算错误
    # dfday=dfday.sort_values(by=timetarget,ascending=True) #跟上面的一个意思
    # 日期截取
    datelist=dfday[timetarget].unique().tolist() # 获取观察周期的所有日期数据
    # testdays=400#只要最后testdays日期的数据
    # print("日期截取前",len(dfday))
    # dateprediction=datelist[len(datelist)-testdays]
    # print("截取日期",dateprediction)
    # dfday=dfday[dfday[timetarget]>=dateprediction]
    # print("日期截取后",len(dfday))
    dfday=dfday.merge(dfminute,on=["floattoday","代码"],how='inner')
    print(dfday)
    dfday.to_csv("合成后.csv")
elif merge==False:
    pass

df=pd.read_csv("合成后.csv")
df=df[df["代码"].str.startswith(("60","00","30"))]#只要沪深主板创业板
timetarget="floattoday"
df["分时close涨幅"]=df["分时close"]/df["前收"]
df["分时open涨幅"]=df["分时open"]/df["前收"]
df["分时close/open涨幅"]=df["分时close"]/df["分时open"]
# df["真实收盘价格"]=df["close"]*df["factor"]
# df["真实开盘价格"]=df["open"]*df["factor"]
df["分时真实收盘价格"]=df["分时close"]*df["factor"]
df["分时真实开盘价格"]=df["分时open"]*df["factor"]

df.loc[df["分时open"]==df["high_limit"],"分时开盘涨停"]=1
df.loc[df["分时open"]==df["low_limit"],"分时开盘跌停"]=1
df.loc[df["分时close"]==df["high_limit"],"分时收盘涨停"]=1
df.loc[df["分时close"]==df["low_limit"],"分时收盘跌停"]=1
df=df[[column for column in df.columns if ("Unnamed" not in column)]]
def technology(df): #定义计算技术指标的函数
    try:
        df=df.sort_values(by=timetarget) #以日期列为索引,避免计算错误
        # print(df)
        #df=df.sort_values(by=timetarget,ascending=False) #从大到小排序 
        holddays=1
        df["target_stock"]=(df["分时真实开盘价格"].copy().shift(-holddays)/(df["分时真实开盘价格"].copy()))-1
        # #未来-holddays-1日价格除以当下价格就是holddays周期之后的涨跌幅隔日涨幅
        # for holddays in [1,3,5,10]:
        #     df[f"target_stock{holddays}"]=(df["分时真实收盘价格"].copy().shift(-holddays-1)/(df["分时真实收盘价格"].copy().shift(-1)))-1
    except Exception as e:
        print(f"发生bug: {e}")
    return df
df=df.groupby("代码",group_keys=False).apply(lambda x:technology(x)) #计算复权因子
print(df)

#过滤垃圾股
import os
import numpy as np
df=df[df["代码"].str.startswith(("60","00","30"))]#只要沪深主板创业板
df=df[~(df["is_st"]==1)]
df=df[~(df["is_paused"]==1)]
df=df[df["归母净利润"]>0]
#指数变成两百只就正常了
df=df.copy().groupby(timetarget,group_keys=False).apply(lambda x: x.nsmallest(200,"总市值"))#【竞价涨幅低的一般会盈利1.33（扣完手续费1.04）】50只就1.06

# df["上涨"] = np.where(df["分时open"]>df["前收"],1,0)#分时上涨
# df["下跌"] = np.where(df["分时open"]<df["前收"],1,0)#分时下跌
# df[f"平均分时涨跌幅"]=df.groupby(timetarget)["分时open涨幅"].transform("mean") # 平均数

df["上涨"] = np.where(df["分时close"]>df["前收"],1,0)#分时上涨
df["下跌"] = np.where(df["分时close"]<df["前收"],1,0)#分时下跌
df[f"平均分时涨跌幅"]=df.groupby(timetarget,group_keys=False)["分时close涨幅"].transform("mean") # 平均数
# for holddays in [1,3,5,10]:
#     df=df.dropna(subset=[f"target_stock{holddays}"])#去掉空数据
#     df[f"平均target_stock{holddays}"]=df.groupby(timetarget)[f"target_stock{holddays}"].transform("mean") # 平均数

df[f"平均target_stock"]=df.groupby(timetarget)[f"target_stock"].transform("mean") # 平均数
df[f"上涨家数"]=df.groupby(timetarget)["上涨"].transform("sum") # 平均数
# df[f"下跌家数"]=df.groupby(timetarget)["下跌"].transform("sum") # 平均数
df[f"上涨比例"]=df.groupby(timetarget)[f"上涨家数"].transform(lambda x: x / len(x))
# df[f"下跌比例"]=df.groupby(timetarget)[f"下跌家数"].transform(lambda x: x / len(x))
# df["上涨比例标准化"]=df[f"上涨比例"]*2-1#没上涨的是-1，全上涨是1
df=df.groupby(timetarget).apply(lambda x:x.tail(1))
df=df.reset_index(drop=True)
df[f"指数平均target_stock净值"]=(df[f"平均target_stock"]+1).cumprod()
df[f"历史净值"]=df[f"指数平均target_stock净值"].copy().shift(1)


for holddays in [1,3,5,10]:
    df[f"指数平均target_stock{holddays}"]=df[f"指数平均target_stock净值"].shift(-holddays)/df[f"指数平均target_stock净值"]# 平均数
df.to_csv("指数合成后.csv")


thisshort=10
df[f"{thisshort}日线"]=df[f"历史净值"].rolling(thisshort).mean()
df[f"{thisshort}高点"]=df[f"历史净值"].rolling(thisshort).max()
df[f"{thisshort}低点"]=df[f"历史净值"].rolling(thisshort).min()
df[f"{thisshort}均值"]=(df[f"{thisshort}高点"]+df[f"{thisshort}低点"])/2
#高低点
df[f"均线强度【高低点】"]=df[f"历史净值"]/df[f"{thisshort}均值"]
df.loc[df[f"均线强度【高低点】"]>=1.1,f"均线强度【高低点】"]=1.1
df.loc[df[f"均线强度【高低点】"]<=0.9,f"均线强度【高低点】"]=0.9
df[f"均线强度刻度【高低点】"]=(2*(df[f"均线强度【高低点】"]-(2)/2)/(0.2))
#乖离率
df[f"均线强度【乖离率】"]=df[f"历史净值"]/df[f"{thisshort}日线"]
df.loc[df[f"均线强度【乖离率】"]>=1.1,f"均线强度【乖离率】"]=1.1
df.loc[df[f"均线强度【乖离率】"]<=0.9,f"均线强度【乖离率】"]=0.9
df[f"均线强度刻度【乖离率】"]=(2*(df[f"均线强度【乖离率】"]-(2)/2)/(0.2))
 
# MAD:中位数去极值
def extreme_MAD(dt,n):
    median = dt.quantile(0.5) #找出中位数
    new_median = (abs((dt - median)).quantile(0.5)) #偏差值的中位数
    dt_up = median + n*new_median #上限
    dt_down = median - n*new_median #下限
    return dt_up,dt_down
kedunbames=["上涨比例",] # "上涨下跌比例"
slow=9#后面不行的话换成更短时间，数据补充到最近几天的，或者
fast=3
for kedunbame in kedunbames:
    ##单纯快线
    df[f"{kedunbame}{fast}日线"]=df[f"{kedunbame}"].rolling(fast).mean()
    # 极端值向临界值靠拢
    # thisdf.loc[thisdf[f"{kedunbame}{slow}、{fast}均线均值"]>=dt_up,f"{kedunbame}{slow}、{fast}均线均值"]=dt_up
    # thisdf.loc[thisdf[f"{kedunbame}{slow}、{fast}均线均值"]<=dt_down,f"{kedunbame}{slow}、{fast}均线均值"]=dt_down
    # df.loc[df[timetarget]==thisday,f"{windowslong}{kedunbame}均线刻度"]=(2*(thisdf.loc[thisdf[timetarget]==thisday,f"{kedunbame}{slow}、{fast}均线均值"]-(dt_up+dt_down)/2)/(dt_up-dt_down))
    # print("双临界值",dt_up,dt_down)
    df[f"{kedunbame}均线刻度"]=(2*(df[f"{kedunbame}{fast}日线"]-0.5)/(1))
    df[f"{kedunbame}均线刻度组合【乖离率】"]=df[f"{kedunbame}均线刻度"]+df[f"均线强度刻度【乖离率】"]
    df[f"{kedunbame}均线刻度组合【高低点】"]=df[f"{kedunbame}均线刻度"]+df[f"均线强度刻度【高低点】"]




    ##快慢线结合
    # df[f"{kedunbame}{slow}日线"]=df[f"{kedunbame}"].rolling(slow).mean()
    # df[f"{kedunbame}{fast}日线"]=df[f"{kedunbame}"].rolling(fast).mean()
    # df[f"{kedunbame}{slow}、{fast}均线均值"]=(df[f"{kedunbame}{slow}日线"]+df[f"{kedunbame}{fast}日线"])/2
    # df[f"{kedunbame}{slow}、{fast}均线差"]=df[f"{kedunbame}{fast}日线"]-df[f"{kedunbame}{slow}日线"]
    # df.loc[(df[f"{kedunbame}{slow}、{fast}均线差"]>0)&(df[f"{kedunbame}{slow}、{fast}均线差"].copy().shift(1)<0),f"{kedunbame}金叉"]=1
    # df.loc[(df[f"{kedunbame}{slow}、{fast}均线差"]<0)&(df[f"{kedunbame}{slow}、{fast}均线差"].copy().shift(1)>0),f"{kedunbame}死叉"]=1
    # # df[f"成交额极大值"] = df[f"成交额"].rolling(10).max()
    # # df[f"成交额极小值"] = df[f"成交额"].rolling(10).min()
    # # df[f"净值极大值"] = df[f"净值"].rolling(10).max()
    # # df[f"净值极小值"] = df[f"净值"].rolling(10).min()
    # df.loc[df[f"{kedunbame}金叉"]==1,f"{kedunbame}交叉状态"]="金叉"
    # df.loc[df[f"{kedunbame}死叉"]==1,f"{kedunbame}交叉状态"]="死叉"  
    # df[f"{kedunbame}交叉状态填充后"]=df[f"{kedunbame}交叉状态"].fillna(method='ffill')
    # # df[f"{kedunbame}交叉状态填充后"]=df[f"{kedunbame}交叉状态"].fillna(method='bfill')

    # # 设置1000天的windows长度
    # windowslong=1000
    # rollingdf=df.rolling(window=windowslong)
    # for thisdf in rollingdf:
    #     if len(thisdf)>=windowslong:
    #         thisday=thisdf[timetarget].values[-1]
    #         # print(thisday,thisdf)
    #         # print(len(thisdf[f"{kedunbame}{slow}日线"]))
    #         # 方差法确定上下轨
    #         data=pd.concat([
    #             # thisdf[f"{kedunbame}{slow}日线"],
    #             thisdf[f"{kedunbame}{fast}日线"],
    #                         ])
    #         # 极端值向临界值靠拢
    #         dt_up,dt_down = extreme_MAD(data,5.2)
    #         # thisdf.loc[thisdf[f"{kedunbame}{slow}、{fast}均线均值"]>=dt_up,f"{kedunbame}{slow}、{fast}均线均值"]=dt_up
    #         # thisdf.loc[thisdf[f"{kedunbame}{slow}、{fast}均线均值"]<=dt_down,f"{kedunbame}{slow}、{fast}均线均值"]=dt_down
    #         # df.loc[df[timetarget]==thisday,f"{windowslong}{kedunbame}均线刻度"]=(2*(thisdf.loc[thisdf[timetarget]==thisday,f"{kedunbame}{slow}、{fast}均线均值"]-(dt_up+dt_down)/2)/(dt_up-dt_down))
    #         # print("双临界值",dt_up,dt_down)
    #         df.loc[df[timetarget]==thisday,f"{windowslong}{kedunbame}均线刻度"]=(2*(thisdf.loc[thisdf[timetarget]==thisday,f"{kedunbame}{slow}、{fast}均线均值"]-0.5)/(1))
    #         df[f"{windowslong}{kedunbame}均线刻度组合【乖离率】"]=df[f"{windowslong}{kedunbame}均线刻度"]+df[f"均线强度刻度【乖离率】"]
    #         df[f"{windowslong}{kedunbame}均线刻度组合【高低点】"]=df[f"{windowslong}{kedunbame}均线刻度"]+df[f"均线强度刻度【高低点】"]




f=df[1000:]
df.to_csv("指数处理后.csv")

a=20#划分20个区间
tradetype="个股"
# for tradetype in tradetypes:
all_result_df=pd.DataFrame({})
sorttypes=["等样本","等长度"]
for sorttype in sorttypes:
    try:
        # 上涨比例、均线强度
        thiscolumns=["平均分时涨跌幅","上涨比例"]
        thiscolumns=[column for column in df.columns if (("均线强度刻度" in column)or("均线刻度" in column))]
        
        print(thiscolumns)
        for mubiao in thiscolumns:
            for n in [1,3,5,10]:
                # 统计收益率分布
                df[f"平均target_stock"]=df[f"指数平均target_stock{n}"]-1
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
                        start_idx=minnum
                        for i in range(0,a):
                            end_idx=start_idx+1/a*(maxnum-minnum)
                            ranges.append([start_idx,end_idx])
                            start_idx+=1/a*(maxnum-minnum)
                            # print(ranges)
                    print(len(df))
                    result_df=pd.DataFrame({})
                    for rank_range in ranges:
                        thisdf=df.copy()
                        thisdf=thisdf[(thisdf[f"{mubiao}"]>=rank_range[0])&(thisdf[f"{mubiao}"]<rank_range[1])]
                        #计算总的数据
                        up_thisdf=thisdf[thisdf[f"平均target_stock"]>0].copy()
                        zero_thisdf=thisdf[thisdf[f"平均target_stock"]==0].copy()
                        down_thisdf=thisdf[thisdf[f"平均target_stock"]<0].copy()
                        #计算逐日数据【可以输出数据看看这个逐日数据对不对】
                        thisdf["target_stock_mean"]=thisdf.groupby(timetarget)[f"平均target_stock"].transform("mean")
                        mean_thisdf=thisdf.copy().groupby(timetarget,group_keys=False).apply(lambda x:x[:1]).reset_index(0, drop=True)
                        mean_thisdf["target_stock_mean"].fillna(0,inplace=True) # 将"target_stock_mean"列中缺失值填充为 0
                        # 计算不同因子值的收益分布
                        # print(len(thisdf))
                        # 逐日累乘净值
                        thisvalue=(mean_thisdf[f"平均target_stock"]+1).cumprod().dropna(axis=0).values
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
                            
                        # thatdf=df.copy()
                        # thatdf=thatdf[(thatdf[f"{mubiao}"]>=rank_range[0])&(thatdf[f"{mubiao}"]<rank_range[1])]
                        # dt_up,dt_down = extreme_MAD(thatdf[f"平均target_stock"],5.2)
                        # #极端值向临界值靠拢
                        # thatdf.loc[thatdf[f"平均target_stock"]>=dt_up,f"平均target_stock"]=dt_up
                        # thatdf.loc[thatdf[f"平均target_stock"]<=dt_down,f"平均target_stock"]=dt_down
                        # print("双临界值",thisdf,dt_up,dt_down)
                        
                        ondf=pd.DataFrame({
                            f"{tradetype}模块的{mubiao}{sorttype}指标值区间": [f"[{rank_range[0]:.6f}, {rank_range[1]:.6f}]"],
                            f"未来{n}日上涨次数":[len(up_thisdf)],
                            f"未来{n}日横盘次数":[len(zero_thisdf)],
                            f"未来{n}日下跌次数":[len(down_thisdf)],
                            f"未来总次数":[len(thisdf)],
                            f"未来{n}日平均涨跌幅":[thisdf[f"平均target_stock"].mean()],
                            # f"未来{n}日平均涨跌幅【不含极端值】":[thatdf[f"平均target_stock"].mean()],
                            # f"未来{n}日日均涨跌幅平均绝对误差":[
                            #     np.mean(np.absolute(mean_thisdf[f"target_stock_mean"]-thisdf[f"平均target_stock"].mean()))
                            #     ],
                            # f"未来{n}日日均涨跌幅均方误差":[
                            #     np.mean(np.square(mean_thisdf[f"target_stock_mean"]-thisdf[f"平均target_stock"].mean()))
                            #     ],
                            # f"逐日累乘净值":[thisvalue],
                            # f"逐日最大回撤":[max_drawdown],
                            # f"":["本行用于不同表单的间隔无意义"],
                            })
                        ondf.set_index(f"模块的{mubiao}{sorttype}指标值区间",inplace=True)
                        result_df=pd.concat([result_df,ondf])
                    # # #每个表单独生成一个文件
                    # if not os.path.exists(f"资产{n}日单指标平均收益分布{mubiao}"):
                    #     os.makedirs(f"资产{n}日单指标平均收益分布{mubiao}")
                    # result_df.round(decimals=6).to_csv(f"资产{n}日单指标平均收益分布{mubiao}/{sorttype}持有{n}日平均收益分布.csv")
                    
                    #这个是新版的一堆因子怼进一个表的情况
                    # result_df=result_df.reset_index(drop=True)
                    if all_result_df.empty:
                        all_result_df=pd.concat([all_result_df,result_df])
                    else:
                        all_result_df=pd.concat([all_result_df,result_df], axis=1)
            if not os.path.exists(f"资产{sorttype}单指标平均收益分布{mubiao}"):
                os.makedirs(f"资产{sorttype}单指标平均收益分布{mubiao}")
            all_result_df.round(decimals=6).to_csv(f"资产{sorttype}单指标平均收益分布{mubiao}/{sorttype}平均收益分布.csv")
            all_result_df=pd.DataFrame({})
        # if not os.path.exists(f"资产{sorttype}单指标平均收益分布"):
        #     os.makedirs(f"资产{sorttype}单指标平均收益分布")
        # all_result_df.round(decimals=6).to_csv(f"资产{sorttype}单指标平均收益分布/{sorttype}平均收益分布.csv")
        # all_result_df=pd.DataFrame({})
        print("任务已经完成")
    except Exception as e:
        print(e)



