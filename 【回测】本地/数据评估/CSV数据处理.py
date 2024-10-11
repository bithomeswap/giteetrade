import pandas as pd
import math

# df=pd.read_csv(r"C:\Users\13480\Desktop\quant\【格式转换、压缩、解压缩】\刻度择时.csv",encoding='GBK')
# df=df.sort_values(by="日期")
# df.loc[((df["上涨比例均线刻度"]>-0.5)&(df["上涨比例均线刻度"].shift(1)<-0.5)),"持仓状态"]="持仓"
# df.loc[((df["上涨比例均线刻度"]<-0.5)&(df["上涨比例均线刻度"].shift(1)>-0.5)),"持仓状态"]="0"
# df[f"持仓状态填充后"]=df[f"持仓状态"].fillna(method='ffill')
# # df[f"持仓状态填充后"]=df[f"持仓状态"].fillna(method='bfill')
# df.to_csv("空仓持仓.csv")
# print(df)

df=pd.read_csv(r"C:\Users\13480\gitee\trade\【回测】本地\数据评估\openclosedf.csv")
df = df.iloc[:, 1:]#去掉第一列
# df=df.sort_values(by="yesterday") #以日期列为索引,避免计算错误
df=df.sort_values(by="日期") #以日期列为索引,避免计算错误
df = df.set_index('日期')#设置日期列为索引
df["累乘净值"]=df["平均涨幅"].cumprod()
# df["平均涨幅0轴"]=df["平均涨幅"]-1


# #主力控盘线
# for n in [10,20,60]:
#     df[f"{n}累乘净值均线"]=df[f"累乘净值"].rolling(n).mean()
#     df[f"{n}累乘净值均线的均线"]=df[f"{n}累乘净值均线"].rolling(n).mean()
#     df[f"{n}累乘净值控盘线"]=df[f"{n}累乘净值均线的均线"]/df[f"{n}累乘净值均线的均线"].shift(1)-1#越大代表越强

# #均线、乖离率
# for n in [5,10,15]:
    # # df[f"{n}累乘净值均线"]=df[f"累乘净值"].rolling(n).mean()
    # # df[f"{n}累乘净值乖离率"]=df[f"累乘净值"]/df[f"{n}累乘净值均线"]
    # # #【市净率曲线站上5、10、15三根均线的一根择认为市场环境比较好，适合交易】
    # df[f"{n}平均市净率均线"]=df[f"平均市净率"].rolling(n).mean()
    # df[f"{n}平均市净率乖离率"]=df[f"平均市净率"]/df[f"{n}平均市净率均线"]
    # # df[f"{n}平均市净率均线乖离率"]=df[f"{n}平均市净率均线"]/df[f"{n}平均市净率均线"].rolling(n).mean()

# df=df[2*n:]

# #趋势强度
# for n in [15,30,60,120]:
#     df[f"{n}日高点距离"]=(df["累乘净值"]/df["累乘净值"].rolling(n).max()-1)
#     # df[f"{n}日涨跌幅"]=(df["累乘净值"]/df["累乘净值"].shift(n)-1)
#     # df[f"{n}日乖离率"]=df["累乘净值"]/(df["累乘净值"].rolling(n).mean())-1
#     # df[f"{n}日趋势强度"]=(df["累乘净值"]/df["累乘净值"].shift(n)-1)/abs(df["平均涨幅0轴"]).cumsum()

#龙系长线
for n in [5,10,15]:
# for n in [2]:
# for n in [3]:
# for n in [150,200,250]:
    df[f"{n}累乘净值均线"]=df[f"累乘净值"].rolling(n).mean()
    df[f"{n}累乘净值均线趋势"]=df[f"{n}累乘净值均线"]/df[f"{n}累乘净值均线"].shift(1)-1
    # df[f"{n}累乘净值均线^"]=df[f"{n}累乘净值均线"].rolling(math.floor(n)).mean()
    # df[f"{n}累乘净值均线^趋势"]=df[f"{n}累乘净值均线^"]/df[f"{n}累乘净值均线^"].shift(10)-1
    # df[f"{n}累乘净值均线^^"]=df[f"{n}累乘净值均线^"].rolling(math.floor(n)).mean()
    # df[f"{n}累乘净值均线^^趋势"]=df[f"{n}累乘净值均线^^"]/df[f"{n}累乘净值均线^^"].shift(10)-1
    # df[f"{n}累乘净值黄龙"]=df[f"{n}累乘净值均线"]+2*df[f"累乘净值"].rolling(n+50).std()
    # df[f"{n}累乘净值黄龙趋势"]=df[f"{n}累乘净值黄龙"]/df[f"{n}累乘净值黄龙"].shift(10)-1

# df=df[n:]
df=df[n*2+50:]

df.to_csv("结果.csv")