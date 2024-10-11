# pip install matplotlib
import xcsc_tushare as ts
import pandas as pd
import numpy as np
import datetime
import os
if not os.path.exists(f"股票形态"):
    os.makedirs(f"股票形态")
df=pd.read_csv(r"C:\Users\13480\Desktop\quant\【回测】本地\数据文件\全体A股\全体A股小市值.csv")
groupdf=df.groupby("floattoday",group_keys=False)
for index,group in groupdf:
    #设置参数
    # STR_DATE='20231001'
    # END_DATE='20240610'
    STR_DATE=str(index-10000).replace(".0","")
    END_DATE=str(index+20000).replace(".0","")
    print(index,STR_DATE,END_DATE)
    for STOCK in group["代码"].tolist():
        if not os.path.exists(f"股票形态"):
            os.makedirs(f"股票形态")
        MA=[5,10,20]
        pro=ts.pro_api('7ed61c98882a320cadce6481aef04ebf7853807179d45ee7f72089d7',server='http://116.128.206.39:7172')
        df=pro.daily(ts_code=STOCK,start_date=STR_DATE,end_date=END_DATE,adj='qfq')
        df['trade_date']=pd.to_datetime(df['trade_date'])
        df=df.sort_values(by='trade_date')
        print(df)
        df=df.dropna()
        for num in [5,10,20]:
            df[f"ma{num}"]=df["adj_close"].rolling(num).mean()#adj_close是复权价
            df[f"乖离率{num}"]=df["adj_close"]/df[f"ma{num}"]
            df[f"ma_v_{num}"]=df["volume"].rolling(num).mean()#adj_close是复权价
            # df[f"ma{num}"]=df["adj_open"].rolling(num).mean()#adj_open是复权价
            # df[f"乖离率{num}"]=df["adj_open"]/df[f"ma{num}"]
            # df[f"ma_v_{num}"]=df["volume"].rolling(num).mean()#adj_open是复权价
        df=df[20:]
        df.to_csv(f"股票形态/{STOCK}{index}因子值.csv")

        def pricestatus(ma5,ma10,ma20):
            if (ma5>ma10)and(ma10>ma20):
                return 1
            elif  (ma5>ma20)and(ma20>ma10):
                return 2
            elif  (ma10>ma5)and(ma5>ma20):
                return 3
            elif  (ma10>ma20)and(ma20>ma5):
                return 4
            elif  (ma20>ma10)and(ma10>ma5):
                return 5
            else:
                return 6
        def volumestatus(ma5,ma10,ma20):
            if (ma5>ma10)and(ma10>ma20):
                return 1
            elif  (ma5>ma20)and(ma20>ma10):
                return 2
            elif  (ma10>ma5)and(ma5>ma20):
                return 3
            elif  (ma10>ma20)and(ma20>ma5):
                return 4
            elif  (ma20>ma10)and(ma10>ma5):
                return 5
            else:
                return 6
        #多股票判断的时候需要分组
        df['pricestatus']=df.apply(lambda x:pricestatus(x['ma5'],x['ma10'],x['ma20']),axis=1)
        df['volumestatus']=df.apply(lambda x:volumestatus(x['ma_v_5'],x['ma_v_10'],x['ma_v_20']),axis=1)
        #时间转换
        df=df[df["trade_date"]>
                datetime.datetime.strptime(str(STR_DATE).replace(".0",""),'%Y%m%d')
                ].copy()
        print(df)

        ##【买入形态】
        df_buy=df.copy()
        df_buy=df_buy[
            (
            (df_buy[f'乖离率{20}']>1.01)
            &
            (df_buy[f'乖离率{20}']<1.1)
            )
            &
            (
            (df_buy[f'乖离率{10}']>1.01)
            &
            (df_buy[f'乖离率{10}']<1.1)
            )
            &
            (
            (df_buy[f'乖离率{5}']>1.01)
            &
            (df_buy[f'乖离率{5}']<1.1)
            )
            # &
            # (df_buy[f'pricestatus']==1)
            # &
            # (df_buy[f'volumestatus']==5)
            &
            (df_buy[f'pricestatus']==5)#最近的价格比过去低，回调或者探底
            ]
        # print(df_buy)
        # df_buy.to_csv(f"股票形态/{STOCK}{index}买入目标形态.csv")

        ##【卖出形态】
        df_sell=df.copy()
        df_sell=df_sell[
            (
            (df_sell[f'乖离率{20}']<0.99)
            # &
            # (df_sell[f'乖离率{20}']>0.9)
            )
            &
            (
            (df_sell[f'乖离率{10}']<0.99)
            # &
            # (df_sell[f'乖离率{10}']>0.9)
            )
            &
            (
            (df_sell[f'乖离率{5}']<0.99)
            # &
            # (df_sell[f'乖离率{5}']>0.9)
            )
            # &
            # (df_sell[f'pricestatus']==1)
            &
            (df_sell[f'volumestatus']==5)
            ]
        # print(df_sell)
        # df_sell.to_csv(f"股票形态/{STOCK}{index}卖出目标形态.csv")

        import matplotlib.pyplot as plt
        plt.figure(figsize=(8,14),dpi=80)
        df_tu=df[['adj_close','trade_date']]
        df_tu['trade_date']=pd.to_datetime(df_tu['trade_date'])
        df_tu.set_index(['trade_date'],inplace=True)
        import seaborn as sns
        sns.set_style('darkgrid')
        sns.lineplot(x='trade_date',y='adj_close',data=df_tu)
        for year in df_buy["trade_date"].tolist():
            plt.scatter(x=year,y=df_buy[df_buy["trade_date"]==year]["adj_close"].values[0],color='red', alpha=0.8)
            # 假设0是y轴的参考值，可以根据需要调整
        for year in df_sell["trade_date"].tolist():
            plt.scatter(x=year,y=df_sell[df_sell["trade_date"]==year]["adj_close"].values[0],color='blue',alpha=0.8)
        plt.savefig(f'股票形态/{STOCK}{index}.jpg', format='jpg', dpi=300)
