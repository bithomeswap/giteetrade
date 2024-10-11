import pandas as pd
# filename="微盘股指数\___bkname.csv"
# filename="COIN\__binance现货日K.csv"
# filename="COIN\__gate现货日k.csv"
# filename="/root/test/quant/本地回测/A股/指数000016.SH.csv"#4.65/2.91
# filename="/root/test/quant/本地回测/A股/指数000300.SH.csv"#6.88/3.63
filename="/root/test/quant/本地回测/A股/指数399852.SZ.csv"#15.98/6.25
# filename="/root/test/quant/本地回测/A股/指数399905.SZ.csv"#12.00/5.69

df=pd.read_csv(filename)

# df=df[df["代码"]=="BTCUSDT"]
# df=df[df["代码"]=="ETHUSDT"]
# df=df[df["代码"]=="SHIBUSDT"]

# df=df[df["代码"]=="BNB_USDT"]
# df=df[df["代码"]=="BTC_USDT"]
# df=df[df["代码"]=="ETH_USDT"]

df=df.sort_values(by="日期")
print(df["开盘"].tolist()[1])
df["开盘"]=df["开盘"]/df["开盘"].tolist()[1]
df["累积涨跌幅"]=df["开盘"]
# df=df[["timestamp","日期","累积涨跌幅"]]
df=df[["日期","累积涨跌幅"]]
print(df)

# df=df.drop(df.columns[0],axis=1) # 删除掉没有数据的第{1}列
# df=df.fillna(0)
# print("df.shape[0]",df.shape[0])
for n in range(1,10):
    if n==1:
        df[f"{n}阶斜率"]=df["累积涨跌幅"]/df["累积涨跌幅"].shift(1)
        # df.to_csv(f"微盘股指数\{n}阶斜率.csv")
    if n>1:
        df[f"{n}阶斜率"]=df[f"{n-1}阶斜率"]/df[f"{n-1}阶斜率"].shift(1)
# df.to_csv(f"微盘股指数\多阶斜率.csv")
# for n in range(1,10):
#     df[f"{n}阶斜率对应值"]=df[f"{n}阶斜率"]*df["累积涨跌幅"]
# df=df.fillna(0)
# df.iloc[0] = 0
# df.to_csv(f"{filename}多阶斜率对应值.csv")

# 增加仓位管理
uprate=1 # 设置加仓比例
downrate=-1 # 设置减仓比例
cost=0.0001 # 股指期货十万分之2.5的隔夜手续费，双向也就是十万分之5

# target="long"
target="short"

# n=3 # 12.526/2.05
# n=4 # 13.69/1.95
n=5 # 15.45/2.00
# n=6 # 13.62/1.81

df["当日涨幅（差值）"]=df["累积涨跌幅"].shift(-1)-df["累积涨跌幅"]
if target=="short":
    df.loc[df[f"{n}阶斜率"] <1, "当日涨幅（差值）"] *= downrate
    df.loc[df[f"{n}阶斜率"] <1, "卖出点"] = -1
    df["累积涨跌幅（减仓后）"]=df["当日涨幅（差值）"].cumsum()+1
    df["累积涨跌幅（减仓后）"]=df["累积涨跌幅（减仓后）"].shift(1)
    df["卖出换手次数"]=df["卖出点"].sum()
    df.loc[(df[f"卖出点"]==-1) & (df[f"卖出点"].shift(-1).isnull()), "空头结算"] = 1
    df=df[df["空头结算"].notnull()]
    df["空头手续费结算"]=df["空头结算"]*(1-cost*(-1*downrate))
    df["空头累积手续费"]=df["空头手续费结算"].cumprod()
    df["累积涨跌幅（减仓后）已扣除手续费"]=df["累积涨跌幅（减仓后）"]*df["空头累积手续费"]
if target=="long":
    df.loc[df[f"{n}阶斜率"] >1, "当日涨幅（差值）"] *= uprate
    df.loc[df[f"{n}阶斜率"] >1, "买入点"] = 1
    df["累积涨跌幅（加仓后）"]=df["当日涨幅（差值）"].cumsum()+1
    df["累积涨跌幅（加仓后）"]=df["累积涨跌幅（加仓后）"].shift(1)
    df["买入换手次数"]=df["买入点"].sum()
    df.loc[(df[f"买入点"]==1) & (df[f"买入点"].shift(-1).isnull()), "多头结算"] = 1
    df=df[df["多头结算"].notnull()]
    df["多头手续费结算"]=df["多头结算"]*(1-cost*uprate)
    df["多头累积手续费"]=df["多头手续费结算"].cumprod()
    df["累积涨跌幅（加仓后）已扣除手续费"]=df["累积涨跌幅（加仓后）"]*df["多头累积手续费"]

df.iloc[0] = 0 # 填充初始值
df=df[[column for column in df.columns if ("累积涨跌幅" in column)or("日期" in column)]]
df.to_csv(f"{filename}多阶斜率{n}阶导数{target}收益率.csv")
print(df)

# ratenum=4
# for n in range(1,ratenum):
#     if n==1:
#         df[f"当日涨幅"]=df[f"当日涨幅（净值比）"]-1
#         # 计算高低点
#         df.loc[df[f"当日涨幅"] > 0,f"{n}阶高点"] = df[f"累积涨跌幅"]
#         df.loc[df[f"当日涨幅"] < 0,f"{n}阶低点"] = df[f"累积涨跌幅"]
#         # 设置未来函数，{n}阶高（低）点极值列，只能用之前{n}轮的这个数据，后面再通过向下平移，取消未来函数【目的是确认上{n}阶段极值】
#         df.loc[(df[f"{n}阶高点"].notnull()) & (df[f"{n}阶高点"].shift(-1).isnull()), f"{n}阶高点极值（未来函数）"] = df[f"{n}阶高点"]
#         df.loc[(df[f"{n}阶低点"].notnull()) & (df[f"{n}阶低点"].shift(-1).isnull()), f"{n}阶低点极值（未来函数）"] = df[f"{n}阶低点"]
#         highdf=df.copy()[df[f"{n}阶高点极值（未来函数）"].notnull()]
# 4        lowdf=df.copy()[df[f"{n}阶低点极值（未来函数）"].notnull()]
#         highdf[f"{n}阶高点极值"]=highdf[f"{n}阶高点极值（未来函数）"].shift(1)
#         lowdf[f"{n}阶低点极值"]=lowdf[f"{n}阶低点极值（未来函数）"].shift(1)
#         # 数据拼接
#         df=pd.merge(df,highdf[[f"日期",f"{n}阶高点极值"]],on="日期",how="left")
#         df=pd.merge(df,lowdf[[f"日期",f"{n}阶低点极值"]],on="日期",how="left")
#         # {n}阶高低点数据填充
#         df[f"{n}阶高点极值"].fillna(method="bfill", inplace=True)
#         df[f"{n}阶高点极值"]=df[f"{n}阶高点极值"].fillna(0)
#         df[f"{n}阶低点极值"].fillna(method="bfill", inplace=True)
#         df[f"{n}阶低点极值"]=df[f"{n}阶低点极值"].fillna(0)
#         # 换算成张总的指标
#         df[f"张总{n}阶高点"] = df[[f"{n}阶高点", f"{n}阶高点极值"]].max(axis=1)
#         df[f"张总{n}阶低点"] = df[[f"{n}阶低点", f"{n}阶低点极值"]].min(axis=1)
#     if n>1:
#         highdf=highdf[1:]
#         lowdf=lowdf[1:]
#         highdf[f"{n-1}阶高点极值涨幅"]=(highdf[f"{n-1}阶高点极值"]/highdf[f"{n-1}阶高点极值"].shift(1))-1
#         lowdf[f"{n-1}阶低点极值涨幅"]=(lowdf[f"{n-1}阶低点极值"]/lowdf[f"{n-1}阶低点极值"].shift(1))-1
#         # 计算高低点
#         lowdf.loc[lowdf[f"{n-1}阶低点极值涨幅"] < 0,f"{n}阶低点"] = lowdf[f"累积涨跌幅"]
#         highdf.loc[highdf[f"{n-1}阶高点极值涨幅"] > 0,f"{n}阶高点"] = highdf[f"累积涨跌幅"]
#         # 设置未来函数，{n}阶高（低）点极值列，只能用之前{n}轮的这个数据，后面再通过向下平移，取消未来函数【目的是确认上{n}阶段极值】
#         highdf.loc[(highdf[f"{n}阶高点"].notnull()) & (highdf[f"{n}阶高点"].shift(-1).isnull()), f"{n}阶高点极值（未来函数）"] = highdf[f"{n}阶高点"]
#         lowdf.loc[(lowdf[f"{n}阶低点"].notnull()) & (lowdf[f"{n}阶低点"].shift(-1).isnull()), f"{n}阶低点极值（未来函数）"] = lowdf[f"{n}阶低点"]
#         highdf[f"{n}阶高点极值"]=highdf[f"{n}阶高点极值（未来函数）"].shift(1)
#         lowdf[f"{n}阶低点极值"]=lowdf[f"{n}阶低点极值（未来函数）"].shift(1)
#         # {n}阶高低点数据填充
#         twohighdf=highdf.copy()[highdf[f"{n}阶高点极值（未来函数）"].notnull()]
#         twohighdf[f"{n}阶高点极值"]=twohighdf[f"{n}阶高点极值（未来函数）"].shift(1)
#         highdf=twohighdf
#         twolowdf=lowdf.copy()[lowdf[f"{n}阶低点极值（未来函数）"].notnull()]
#         twolowdf[f"{n}阶低点极值"]=twolowdf[f"{n}阶低点极值（未来函数）"].shift(1)
#         lowdf=twolowdf
#         # 数据拼接
#         df=pd.merge(df,highdf[[f"日期",f"{n}阶高点极值",f"{n}阶高点极值（未来函数）"]],on="日期",how="left")
#         df=pd.merge(df,lowdf[[f"日期",f"{n}阶低点极值",f"{n}阶低点极值（未来函数）"]],on="日期",how="left")
#         # {n}阶高低点数据填充
#         df[f"{n}阶高点极值"].fillna(method="bfill", inplace=True)
#         df[f"{n}阶高点极值"]=df[f"{n}阶高点极值"].fillna(0)
#         df[f"{n}阶低点极值"].fillna(method="bfill", inplace=True)
#         df[f"{n}阶低点极值"]=df[f"{n}阶低点极值"].fillna(0)
#         for a in range(1,n):
#             if n==1:
#                 # 换算成张总的指标
#                 df[f"张总{n}阶高点"] = df[[f"{a}阶高点极值",f"{n}阶高点极值"]].max(axis=1)
#                 df[f"张总{n}阶低点"] = df[[f"{a}阶低点极值",f"{n}阶低点极值"]].min(axis=1)
#             if n>1:
#                 # 换算成张总的指标
#                 df[f"张总{n}阶高点"] = df[[f"{n}阶高点极值",f"张总{n-1}阶高点"]].max(axis=1)
#                 df[f"张总{n}阶低点"] = df[[f"{n}阶低点极值",f"张总{n-1}阶低点"]].min(axis=1)
#     highdf.to_csv(f"微盘股指数\_{n}阶高点极值.csv")
#     lowdf.to_csv(f"微盘股指数\_{n}阶低点极值.csv")
#     # 计算高低点距离（近期偏离和远期偏离）
#     df[f"{n}阶高点偏离"]=df[f"张总{n}阶高点"]/df[f"累积涨跌幅"]
#     df[f"{n}阶低点偏离"]=df[f"张总{n}阶低点"]/df[f"累积涨跌幅"]
#     df[f"{n}阶高点极值（未来函数）"]=df[f"{n}阶高点极值（未来函数）"].fillna(0)
#     df[f"{n}阶低点极值（未来函数）"]=df[f"{n}阶低点极值（未来函数）"].fillna(0)
# print(df)
# df.to_csv("微盘股指数\____多阶高低点.csv")

# df=pd.read_csv("微盘股指数\____多阶高低点.csv")
# # df=df[[column for column in df.columns if (("累积涨跌幅" in column) or ("偏离" in column) or ("日期" in column) or ("当日涨幅" in column))]]
# df=df[[column for column in df.columns if (("累积涨跌幅" in column) 
#                                         or ("偏离" in column)
#                                         or ("日期" in column)
#                                         or ("当日涨幅" in column)
#                                         or (f"张总{n}阶" in column)
#                                         )]]

# # choose="网格调仓"
# choose="趋势调仓"
# # 这里需要判断高点先更新还是低点先更新【也就是把高点线的跳点和低点线的跳点拿出来单独算】
# df.loc[df[f"张总{n}阶高点"]!= df[f"张总{n}阶高点"].shift(1), "变更"] = 1
# df.loc[df[f"张总{n}阶低点"]!= df[f"张总{n}阶低点"].shift(1), "变更"] = -1
# df["变更"].fillna(method="ffill", inplace=True)
# if choose=="网格调仓":
#     # n=2 # 设置针对的高低点阶数
#     # lowpoint=0.87 # 低点涨幅净值比（倒数）
#     # uprate=0.5 # 设置低点偏离仓位缩放比例
#     # highpoint=1.10 # 高点跌幅跌幅比（倒数）
#     # downrate=2 # 设置高点偏离仓位缩放比例
#     n=1 # 设置针对的高低点阶数
#     lowpoint=0.9 # 低点涨幅净值比（倒数）
#     uprate=0.5 # 设置低点偏离仓位缩放比例
#     highpoint=1.10 # 高点跌幅跌幅比（倒数）
#     downrate=2 # 设置高点偏离仓位缩放比例
#     df=df.copy()
#     # df.loc[(df[f"{n}阶低点偏离"] < lowpoint)&(df["变更"]==-1), "卖出点"] = -1
#     # df.loc[(df[f"{n}阶高点偏离"] > highpoint)&(df["变更"]==1), "买入点"] = 1
#     df.loc[(df[f"{n}阶低点偏离"] < lowpoint)&(df["变更"]==1), "卖出点"] = -1
#     df.loc[(df[f"{n}阶高点偏离"] > highpoint)&(df["变更"]==-1), "买入点"] = 1
#     df=pd.merge(df,df[[f"日期","买入点","卖出点"]],on="日期",how="left")
#     df.iloc[0] = 0
#     df.loc[(df[f"买入点"].shift(1)!=1) & (df[f"买入点"]==1) , "加仓"]=1
#     df.loc[(df[f"卖出点"].shift(1)!=-1) & (df[f"卖出点"]==-1) , "减仓"]=-1
#     # df.loc[(df[f"买入点"]==1) & (df[f"买入点"].shift(-1)!=1), f"买入换手点"] = 1
#     # df.loc[(df[f"卖出点"]==1) & (df[f"卖出点"].shift(-1)!=1), f"卖出换手点"] = 1
#     # df["买入换手次数"]=df["买入换手点"].sum()
#     # df["卖出换手次数"]=df["卖出换手点"].sum()
#     thisdf=df[(df["加仓"]==1)|(df["减仓"]==-1)]
#     thisdf.loc[(thisdf[f"加仓"].shift(1)!=1) & (thisdf[f"加仓"]==1), "单调加仓"]=1
#     thisdf.loc[(thisdf[f"减仓"].shift(1)!=-1) & (thisdf[f"减仓"]==-1), "单调减仓"]=-1
#     print(thisdf)
#     df=pd.merge(df,thisdf[["日期","单调加仓","单调减仓"]],on="日期",how="left")
# if choose=="趋势调仓":
#     n=1 # 设置针对的高低点阶数
#     lowpoint=0.97 # 设置低点偏离阈值【这里是低点除以当前值，也就是突破】
#     uprate=2 # 设置低点偏离仓位缩放比例
#     highpoint=1.02 # 设置高点偏离阈值【这里是高点除以当前值，也就是回撤】
#     downrate=0.5 # 设置高点偏离仓位缩放比例
#     # df["当日涨幅（差值）"]=df["累积涨跌幅"].shift(-1)-df["累积涨跌幅"]
#     # # df=df.copy()
#     # # df.loc[df[f"{n}阶高点偏离"] > highpoint, "当日涨幅（差值）"] *= downrate
#     # # df["累积涨跌幅（减仓后）"]=df["当日涨幅（差值）"].cumsum()+1
#     # # df["累积涨跌幅（减仓后）"]=df["累积涨跌幅（减仓后）"].shift(1)
#     # # df=pd.merge(df,df[[f"日期","累积涨跌幅（减仓后）"]],on="日期",how="left")
#     # # df=df.copy()
#     # # df.loc[df[f"{n}阶低点偏离"] < lowpoint, "当日涨幅（差值）"] *= uprate
#     # # df["累积涨跌幅（加仓后）"]=df["当日涨幅（差值）"].cumsum()+1
#     # # df["累积涨跌幅（加仓后）"]=df["累积涨跌幅（加仓后）"].shift(1)
#     # # df=pd.merge(df,df[[f"日期","累积涨跌幅（加仓后）"]],on="日期",how="left")
#     df=df.copy()
#     # df.loc[df[f"{n}阶高点偏离"] > highpoint, "当日涨幅（差值）"] *= downrate
#     df.loc[(df[f"{n}阶低点偏离"] < lowpoint)&(df["变更"]==-1), "买入点"] = 1
#     # df.loc[df[f"{n}阶低点偏离"] < lowpoint, "当日涨幅（差值）"] *= uprate
#     df.loc[(df[f"{n}阶高点偏离"] > highpoint)&(df["变更"]==1), "卖出点"] = -1
#     # # df["累积涨跌幅（调整后）"]=df["当日涨幅（差值）"].cumsum()+1
#     # # df["累积涨跌幅（调整后）"]=df["累积涨跌幅（调整后）"].shift(1)
#     # # df=pd.merge(df,df[[f"日期","累积涨跌幅（调整后）","买入点","卖出点"]],on="日期",how="left")
#     # df[f"累积涨跌幅（减仓后）"]=df[f"累积涨跌幅（减仓后）"].fillna(1) # 填充初始值
#     # df[f"累积涨跌幅（加仓后）"]=df[f"累积涨跌幅（加仓后）"].fillna(1) # 填充初始值
#     # df[f"累积涨跌幅（调整后）"]=df[f"累积涨跌幅（调整后）"].fillna(1) # 填充初始值
    
#     df=pd.merge(df,df[[f"日期","买入点","卖出点"]],on="日期",how="left")
#     df.iloc[0] = 0
#     df.loc[(df[f"买入点"].shift(1)!=1) & (df[f"买入点"]==1) , "加仓"]=1
#     df.loc[(df[f"卖出点"].shift(1)!=-1) & (df[f"卖出点"]==-1) , "减仓"]=-1
#     # df.loc[(df[f"买入点"]==1) & (df[f"买入点"].shift(-1)!=1), f"买入换手点"] = 1
#     # df.loc[(df[f"卖出点"]==1) & (df[f"卖出点"].shift(-1)!=1), f"卖出换手点"] = 1
#     # df["买入换手次数"]=df["买入换手点"].sum()
#     # df["卖出换手次数"]=df["卖出换手点"].sum()
#     thisdf=df[(df["加仓"]==1)|(df["减仓"]==-1)]
#     thisdf.loc[(thisdf[f"加仓"].shift(1)!=1) & (thisdf[f"加仓"]==1), "单调加仓"]=1
#     thisdf.loc[(thisdf[f"减仓"].shift(1)!=-1) & (thisdf[f"减仓"]==-1), "单调减仓"]=-1
#     print(thisdf)
#     df=pd.merge(df,thisdf[["日期","单调加仓","单调减仓"]],on="日期",how="left")


# target=[column for column in df.columns if ("累积涨跌幅" in column) or (
#     "买入点" in column) or("卖出点" in column)or (
#     "单调加仓" in column) or("单调减仓" in column)]
# df=df[target]

# df.iloc[0] = 0
# len=len(df.columns)
# df.to_csv(f"微盘股指数\____多阶高低点（优化后数据）_高低点阶数{n}调仓方式{choose}低点偏离{lowpoint}仓位{uprate}高点偏离{highpoint}仓位{downrate}____列长度{len}.csv")
# print(df)