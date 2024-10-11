import pandas as pd
# pip install alphalens-reloaded
from alphalens.utils import get_clean_factor_and_forward_returns
import os

basepath=r"C:\Users\13480\Desktop\quant"


# thistarget="全部"
# path=basepath+rf"\全体A股标准化完成.csv"
# time="floattoday"
# thisclose="沪深收盘"
# columns=["均线刻度","全部庄家净流入成交额比"]
    

# thistarget="大市值"
thistarget="全部"
path=basepath+rf"\【回测】本地\数据文件\全体A股\全体A股{thistarget}.csv"
time="量价数据日期"
thisclose="收盘"
columns=["金额流入率","净流入庄家金额成交额比"]


# thistarget="全部"
# path=basepath+rf"\【回测】本地\数据文件\半小时资金流\半小时资金流{thistarget}.csv"
# time="价格分时"
# thisclose="收盘"
# columns=["金额流入率","净流入庄家金额成交额比"]

###半小时的材料的日期数据将每过半小时默认过了一天###
# prices.index=pd.to_datetime(prices.index, utc=True)



#使用这种平滑处理之后的移动平均线重新计算一下EMA
import numpy as np
import talib#这个库切换3.8环境就自带talib，3.11就不行，3.8版本自带talib或者说是我之前装过
# conda install -c conda-forge ta-lib#这个应该是在3.8里面装过

df=pd.read_csv(path)
if "标准化完成.csv"in path:
    df["代码"]="大盘"
    # 假设df是包含浮点数日期列的DataFrame，列名为"floattoday"
    df["floattoday"] = df["floattoday"].astype(str).str.replace(r'\.0','',regex=True).astype(str)  # 将浮点数日期列转换为字符串
    # df["floattoday"] = pd.to_datetime(df["floattoday"], format='%Y%m%d')  # 将字符串日期转换为datetime格式
    # print(df["floattoday"])



# if "全体A股" in path:
#     df["上涨溢价_rank"]=df.groupby("floattoday")["上涨溢价"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(上涨溢价_rank_rate=(x["上涨溢价_rank"]/len(x))))
#     df["下跌溢价_rank"]=df.groupby("floattoday")["下跌溢价"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(下跌溢价_rank_rate=(x["下跌溢价_rank"]/len(x))))
#     df["百日上涨次数_rank"]=df.groupby("floattoday")["百日上涨次数"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(百日上涨次数_rank_rate=(x["百日上涨次数_rank"]/len(x))))
#     df["百日上涨平均溢价_rank"]=df.groupby("floattoday")["百日上涨平均溢价"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(百日上涨平均溢价_rank_rate=(x["百日上涨平均溢价_rank"]/len(x))))
#     df["百日下跌次数_rank"]=df.groupby("floattoday")["百日下跌次数"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(百日下跌次数_rank_rate=(x["百日下跌次数_rank"]/len(x))))
#     df["百日下跌平均溢价_rank"]=df.groupby("floattoday")["百日下跌平均溢价"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(百日下跌平均溢价_rank_rate=(x["百日下跌平均溢价_rank"]/len(x))))

#     df["涨停溢价_rank"]=df.groupby("floattoday")["涨停溢价"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(涨停溢价_rank_rate=(x["涨停溢价_rank"]/len(x))))
#     df["跌停溢价_rank"]=df.groupby("floattoday")["跌停溢价"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(跌停溢价_rank_rate=(x["跌停溢价_rank"]/len(x))))
#     df["百日涨停次数_rank"]=df.groupby("floattoday")["百日涨停次数"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(百日涨停次数_rank_rate=(x["百日涨停次数_rank"]/len(x))))
#     df["百日涨停平均溢价_rank"]=df.groupby("floattoday")["百日涨停平均溢价"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(百日涨停平均溢价_rank_rate=(x["百日涨停平均溢价_rank"]/len(x))))
#     df["百日跌停次数_rank"]=df.groupby("floattoday")["百日跌停次数"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(百日跌停次数_rank_rate=(x["百日跌停次数_rank"]/len(x))))
#     df["百日跌停平均溢价_rank"]=df.groupby("floattoday")["百日跌停平均溢价"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(百日跌停平均溢价_rank_rate=(x["百日跌停平均溢价_rank"]/len(x))))
# if "全体A股" not in  path:
#     df["收盘均价比_rank"]=df.groupby("floattoday")["收盘均价比"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(收盘均价比_rank_rate=(x["收盘均价比_rank"]/len(x))))
# df["日内回落_rank"]=df.groupby("floattoday")["日内回落"].rank(ascending=True)
# df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(日内回落_rank_rate=(x["日内回落_rank"]/len(x))))
# df["日内上攻_rank"]=df.groupby("floattoday")["日内上攻"].rank(ascending=True)
# df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(日内上攻_rank_rate=(x["日内上攻_rank"]/len(x))))
# df["日内涨幅_rank"]=df.groupby("floattoday")["日内涨幅"].rank(ascending=True)
# df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(日内涨幅_rank_rate=(x["日内涨幅_rank"]/len(x))))
# df["隔日涨幅_rank"]=df.groupby("floattoday")["隔日涨幅"].rank(ascending=True)
# df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(隔日涨幅_rank_rate=(x["隔日涨幅_rank"]/len(x))))
# df["日内振幅_rank"]=df.groupby("floattoday")["日内振幅"].rank(ascending=True)
# df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(日内振幅_rank_rate=(x["日内振幅_rank"]/len(x))))
# df["换手率_rank"]=df.groupby("floattoday")["换手率"].rank(ascending=True)
# df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(换手率_rank_rate=(x["换手率_rank"]/len(x))))  
# df["换手率比值_rank"]=df.groupby("floattoday",group_keys=False)["换手率比值"].rank(ascending=True)
# df=df.groupby("floattoday",group_keys=False).apply(lambda x: x.assign(换手率比值_rank_rate=(x["换手率比值_rank"]/len(x))))
# df["成交额_rank"]=df.groupby("floattoday")["成交额"].rank(ascending=True)
# df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(成交额_rank_rate=(x["成交额_rank"]/len(x))))
# df["总市值_rank"]=df.groupby("floattoday")["总市值"].rank(ascending=True)
# df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(总市值_rank_rate=(x["总市值_rank"]/len(x))))

# df["资金贡献_rank"]=df.groupby("floattoday")["资金贡献"].rank(ascending=True)
# df=df.groupby("floattoday",group_keys=False).apply(lambda x: x.assign(资金贡献_rank_rate=(x["资金贡献_rank"]/len(x))))
# df["资金波动_rank"]=df.groupby("floattoday")["资金波动"].rank(ascending=True)
# df=df.groupby("floattoday",group_keys=False).apply(lambda x: x.assign(资金波动_rank_rate=(x["资金波动_rank"]/len(x))))
# if "可转债" in path:
#     df["三低指数_rank"]=df.groupby("floattoday")["三低指数"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(三低指数_rank_rate=(x["三低指数_rank"]/len(x))))
# if "全体A股" in path:
#     df["金额流入率_rank"]=df.groupby("floattoday")["金额流入率"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(金额流入率_rank_rate=(x["金额流入率_rank"]/len(x))))
#     #庄家行为
#     df["总主动卖出庄家金额_rank"]=df.groupby("floattoday")["总主动卖出庄家金额"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(总主动卖出庄家金额_rank_rate=(x["总主动卖出庄家金额_rank"]/len(x))))
#     df["总被动卖出庄家金额_rank"]=df.groupby("floattoday")["总被动卖出庄家金额"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(总被动卖出庄家金额_rank_rate=(x["总被动卖出庄家金额_rank"]/len(x))))
#     df["总主动买入庄家金额_rank"]=df.groupby("floattoday")["总主动买入庄家金额"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(总主动买入庄家金额_rank_rate=(x["总主动买入庄家金额_rank"]/len(x))))
#     df["总被动买入庄家金额_rank"]=df.groupby("floattoday")["总被动买入庄家金额"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(总被动买入庄家金额_rank_rate=(x["总被动买入庄家金额_rank"]/len(x))))
#     df["总卖出庄家金额_rank"]=df.groupby("floattoday")["总卖出庄家金额"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(总卖出庄家金额_rank_rate=(x["总卖出庄家金额_rank"]/len(x))))
#     df["总买入庄家金额_rank"]=df.groupby("floattoday")["总买入庄家金额"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(总买入庄家金额_rank_rate=(x["总买入庄家金额_rank"]/len(x))))
#     df["总卖出庄家金额成交额比_rank"]=df.groupby("floattoday")["总卖出庄家金额成交额比"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(总卖出庄家金额成交额比_rank_rate=(x["总卖出庄家金额成交额比_rank"]/len(x))))
#     df["总买入庄家金额总市值比_rank"]=df.groupby("floattoday")["总买入庄家金额总市值比"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(总买入庄家金额总市值比_rank_rate=(x["总买入庄家金额总市值比_rank"]/len(x))))
#     df["净流入庄家金额_rank"]=df.groupby("floattoday")["净流入庄家金额"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(净流入庄家金额_rank_rate=(x["净流入庄家金额_rank"]/len(x))))
#     df["净流入庄家金额总市值比_rank"]=df.groupby("floattoday")["净流入庄家金额总市值比"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(净流入庄家金额总市值比_rank_rate=(x["净流入庄家金额总市值比_rank"]/len(x))))
#     df["净流入庄家金额成交额比_rank"]=df.groupby("floattoday")["净流入庄家金额成交额比"].rank(ascending=True)
#     df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(净流入庄家金额成交额比_rank_rate=(x["净流入庄家金额成交额比_rank"]/len(x))))
# if "可转债" in path:
#     df=df[~(df["次日is_paused"]==1)]
#     # df["总市值"]=df["三低指数"] #针对可转债
#     df.loc[(df["转股溢价率"]>1.2),"总市值"]*=1.5 # 针对溢价率高的标的进行加权
# if "全体A股" in path:
#     df=df[~(df["次日is_st"]==1)]
#     df=df[~(df["次日is_paused"]==1)]
#     df=df[~(df["次日开盘涨停"]==1)]
    
# columns=[column for column in df.columns.tolist() if not ((
#             "target" in column)or(
#             "Unnamed" in column)or(
#             "float" in column)or(
#             "_rate" in column))]

print(columns)
for columnname in columns:
    try:
        factor=df.copy()
        factor=factor[[time,"代码",columnname]]
        # factor = pd.concat(factor)
        factor.rename(columns = {"代码":"asset",columnname:"factor",time:"date"}, inplace=True)
        factor["date"] = pd.to_datetime(factor["date"], utc=True)
        factor.set_index(["date", "asset"], inplace=True)
        print(factor.index,type(factor.index.values[0]))
        prices=df.copy()
        prices.rename(columns = {thisclose:"close"}, inplace=True)
        prices=prices[[time,"代码","close"]]
        prices.rename(columns = {"代码":"asset"}, inplace=True)
        prices=prices.pivot(index=time, columns="asset", values="close")
        prices.index=pd.to_datetime(prices.index, utc=True)
        prices.rename_axis('date', inplace=True)
        print(prices.index,type(factor.index.values[0]))
        #默认从小到大排序
        factor_data = get_clean_factor_and_forward_returns(
            factor,
            prices,
            groupby=None,
            binning_by_group=False,
            quantiles=1,#一般分成十组
            bins=None,
            periods=(1, 5, 10),
            filter_zscore=20,
            groupby_labels=None,
            max_loss=0.35,
            zero_aware=False)        
        if not os.path.exists(f"{path}因子分析"):
            os.makedirs(f"{path}因子分析")
        factor_data.to_csv(f"{path}因子分析/{columnname}factor_data.csv")
        print(factor_data)
    except Exception as e:
        print("******报错",e)

