import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')

# # 获取沪深300指数收盘价
import akshare as ak
import os

stock="指数"
indexlist=['000016','000300','000001','000985','399005','399101','399011','399015']
target="指数"

# stock="个股"
# # indexlist=['300829.SZ','300215.SZ','300709.SZ','603610.SH','300439.SZ','300867.SZ',
# #  '300423.SZ','000910.SZ','300177.SZ','300590.SZ','300740.SZ','002975.SZ',
# #  '300255.SZ','603313.SH','603960.SH','300326.SZ','603018.SH','300815.SZ',
# #  '300842.SZ','002614.SZ','000601.SZ','000507.SZ','603959.SH','300219.SZ',
# #  '300149.SZ','300184.SZ','300127.SZ','000823.SZ','300205.SZ','600590.SH',
# #  '002251.SZ','002611.SZ','600105.SH','002215.SZ','600308.SH','002344.SZ',
# #  '002449.SZ','300303.SZ','300477.SZ','603429.SH','300485.SZ','603601.SH',
# #  '600449.SH','000036.SZ','300872.SZ']
# # target="小市值"
# indexlist=['601328.SH','601398.SH','601939.SH','601998.SH','600028.SH','601166.SH',
#  '600016.SH','601088.SH','600000.SH','600036.SH']
# target="大市值"
# alldata=pd.read_csv(r"C:\Users\13480\Desktop\【回测】本地\数据文件\全体A股\全体A股.csv")

# stock="COIN"
# indexlist=["BTCUSDT","ETHUSDT","BNBUSDT","TRXUSDT","DOTUSDT"]
# target="COIN"
# alldata=pd.read_csv("/root/test/quant/【回测】本地/数据文件/COIN/__binance合约日K.csv")
# # alldata=pd.read_csv("/root/test/quant/【回测】本地/数据文件/COIN/__binance合约小时K.csv")
# # alldata=pd.read_csv("/root/test/quant/【回测】本地/数据文件/COIN/__binance合约2小时K.csv")

#设置均线长度【不能是偶数，主要是取中间数那个均值点】
klen = 21#个股21天合适，指数5天合适
for index in indexlist:
    if stock=="指数":
        data = ak.index_zh_a_hist(symbol=index, period='daily', start_date='20200104', end_date='20240106')
    elif stock=="COIN":
        data=alldata.copy()
        data=data[data["代码"]==index]
    elif stock=="个股":
        data=alldata.copy()
        data=data[data["代码"]==index]
        data.rename(columns={"yesterday_prev_close":"前收",
        "yesterday_high": "最高",
        "yesterday_low": "最低",
        "yesterday_close": "收盘",
        "yesterday_open": "开盘",
        "yesterday_turnover": "成交额",
        "yesterday_volume":"成交量",
        # "yesterday_总股本":"总股本",
        "yesterday_流通股本":"总股本",
        "yesterday_归母净利润":"归母净利润",
        "floattoday":"日期",
        },inplace=True)

    data= data[['日期','收盘']].rename(columns={'日期':'date', '收盘':'close'})
    if stock!="个股":
        data['date'] = pd.to_datetime(data['date'])
    data['pct'] = data['close'].pct_change()#计算涨跌幅
    data.set_index('date', drop=True, inplace=True)
    # data.tail(10)#获取最后10行数据
    print(len(data))

    # #log预测法
    # import math
    # def get_score(df):
    #     y = np.log(df)
    #     x = np.arange(y.size)
    #     slope, intercept = np.polyfit(x, y, 1)
    #     annualized_returns = math.pow(math.exp(slope), 250) - 1
    #     r_squared=1-(sum((y-(slope * x + intercept))**2) / ((len(y) - 1) * np.var(y, ddof=1)))
    #     score = annualized_returns * r_squared
    #     return score
    # # klen日均线
    # data['icu'] = data["close"].rolling(klen).apply(get_score,raw=True)
    # # 当价格上穿短期ICU均线则买入
    # data.loc[(data['icu']>0),'signal'] = 1
    # # 当价格从上往下穿均线时卖出平仓
    # data.loc[(data['icu']<0),'signal'] = 0

    #均值回归法
    from scipy.stats import siegelslopes
    # 计算ICU均线
    def get_icu(df):
        n = df.shape[0]#宽度等同于len(df)(0位置那个元素代表的1，这里也就是总元素数量)
        m = round((n-1)/2)#(n-1)/2，上面是5下面是2
        # print(np.arange(-m,m+1))
        # print(df)
        beta,mu = siegelslopes(df,np.arange(-m,m+1),method='hierarchical')#这样回归的均线的残差的绝对值最小
        # print(beta,mu)
        # y = mu
        # y = mu + beta * m
        y = mu + beta * n
        return y
    # klen日均线
    data['ma'] = data['close'].rolling(klen).mean()
    data['icu'] = data['close'].rolling(klen).apply(get_icu,raw=True)
    # 当价格上穿短期ICU均线则买入
    data.loc[(data['close']>data['icu']) & (data['close'].shift(1)<=data['icu'].shift(1)), 'signal'] = 1
    # 当价格从上往下穿均线时卖出平仓
    data.loc[(data['close']<data['icu']) & (data['close'].shift(1)>=data['icu'].shift(1)), 'signal'] = 0



    data['signal'] = data['signal'].fillna(method='ffill').fillna(value=0) 
    # 收盘交易，下一日才会有持仓
    data['position'] = data['signal'].shift(1).fillna(value=0)
    # ICU策略的净值计算
    data['strategy_pct'] = data['pct'] * data['position']
    data['基准净值'] = (1.0 + data['pct']).cumprod()#计算基准净值
    data['策略净值'] = (1.0 + data['strategy_pct']).cumprod() 
    data['基准收益率'] = data['基准净值']-1.0#计算基准收益率
    data['策略收益率'] = data['策略净值'] - 1.0
    # print(data[['策略收益率','基准收益率']])
    newpath=os.path.join(os.path.abspath("."),target)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    data.to_csv(f"{newpath}/{stock}{index}的ICU均线{klen}.csv")


##多参数测试
# import warnings
# import numpy as np
# import pandas as pd
# import akshare as ak
# from scipy.stats import siegelslopes
# warnings.filterwarnings('ignore')
# # 计算ICU均线
# def get_icu(srs):
#     n = srs.shape[0]
#     m = round((n-1) / 2)
#     beta, mu = siegelslopes(srs, np.arange(-m,m+1), method='hierarchical')
#     y = mu + beta * m
#     return y
# def icu_backttest(data0, m):
#     # 防止原始数据被修改
#     data = data0.copy()
#     # 计算ICU均线
#     data['icu'] = data['close'].rolling(2*m+1).apply(get_icu, raw=True)
#     # 生成交易信号和持仓
#     data.loc[(data['close']>data['icu']) & (data['close'].shift(1)<=data['icu'].shift(1)), 'signal'] = 1
#     data.loc[(data['close']<data['icu']) & (data['close'].shift(1)>=data['icu'].shift(1)), 'signal'] = 0
#     data['signal'] = data['signal'].fillna(method='ffill').fillna(value=0) 
#     data['position'] = data['signal'].shift(1).fillna(value=0)  
#     # 择时策略净值
#     data['strategy_pct'] = data['pct'] * data['position']
#     data['strategy'] = (1.0 + data['strategy_pct']).cumprod() 
#     # 最终的累计收益率
#     cum_return = data['strategy'].iloc[-1] - 1.0
#     return cum_return
# # 获取数据
# data = ak.index_zh_a_hist(symbol='000300', period='daily', start_date='20050104', end_date='20230406')
# data= data[['日期','收盘']].rename(columns={'日期':'date', '收盘':'close'})
# data['date'] = pd.to_datetime(data['date'])
# data['pct'] = data['close'].pct_change() #涨跌幅
# data.set_index('date', drop=True, inplace=True)
# # 待选参数列表
# m_list = list(range(2, 101))
# # 参数结果
# result = pd.DataFrame(np.nan, index=range(len(m_list)), columns=['m', 'n', 'cum_return'])
# # 循环回测不同参数下的ICU策略
# for i, m in enumerate(m_list):
#     cum_return = icu_backttest(data, m)
#     result.loc[i] = [m, 2*m+1, cum_return]
#     print('%d/%d. 参数 [%d] 对应的ICU策略累计收益率是 %.2f %%' %(i+1, len(m_list), m, 100*cum_return))
# result = result.sort_values('cum_return', ascending=False)
# result[result.cum_return>8.5]