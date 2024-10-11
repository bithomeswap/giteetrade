# 创作者微信：lianghuajiaoyi123456
# pip install pytdx
import pandas as pd

#微盘股拥挤度因子
from pytdx.exhq import *
from pytdx.hq import TdxHq_API
import pandas as pd
from datetime import datetime
#通达信api地址：https://gitee.com/better319/pytdx/#5--%E8%8E%B7%E5%8F%96%E6%8C%87%E6%95%B0k%E7%BA%BF
ip="119.147.212.81"
api = TdxHq_API()
api.connect(ip,7709)
all_data=pd.DataFrame()
#每次只能取800组数据，循环取数
for i in [4,3,2,1,0]:
    num=800*i
    #获取微盘股指数，指数get_index_bars，个股get_security_bars
    # wp_data = api.to_df(api.get_security_bars(4, 1, '000004',num, 800))
    # wp_data['date'] = wp_data['datetime']
    # wp_data = api.to_df(api.get_index_bars(4, 1, '880823',num, 800))#微盘股指数
    # wp_data = api.to_df(api.get_index_bars(4, 1, '000001',num, 800))#上证股指数
    wp_data = api.to_df(api.get_index_bars(4, 1, '000300',num, 800))#沪深三百
    wp_data['datetime'] = pd.to_datetime(wp_data['datetime'])
    wp_data['date'] = wp_data['datetime'].dt.strftime('%Y-%m-%d')
    print(wp_data)
    #获取上证指数成交量
    wp_data['szzs_amount'] = api.to_df(api.get_index_bars(4, 1, '000001',num, 800))['amount']
    #获取深圳成指成交量
    wp_data['szcz_amount'] = api.to_df(api.get_index_bars(4, 0, '399001',num, 800))['amount']
    #获取创业板指成交量
    wp_data['cybz_amount'] = api.to_df(api.get_index_bars(4, 0, '399006',num, 800))['amount']
    wp_data['全市场总成交额']=wp_data['szzs_amount']+wp_data['szcz_amount']+wp_data['cybz_amount']
    all_data = pd.concat([all_data, wp_data], ignore_index=True)

all_data['target'] = all_data['open'].shift(-2)/all_data['open'].shift(-1)
all_data['微盘股成交额'] = all_data['amount']
all_data['微盘股成交量'] = all_data['vol']
all_data['微盘股成交额均值'] = all_data['微盘股成交额'].rolling(10).mean()
all_data['微盘股成交额极大值'] = all_data['微盘股成交额'].rolling(10).max()
all_data['微盘股成交额极小值'] = all_data['微盘股成交额'].rolling(10).min()
all_data['微盘股成交额乖离率'] = all_data['微盘股成交额']/all_data['微盘股成交额均值']
all_data['微盘股成交额极大乖离率'] = all_data['微盘股成交额']/all_data['微盘股成交额极大值']
all_data['微盘股成交额极小乖离率'] = all_data['微盘股成交额']/all_data['微盘股成交额极小值']
all_data['微盘股成交额变动'] = all_data['微盘股成交额']/all_data['微盘股成交额'].shift(1)

all_data['微盘股成交额占比'] = all_data['微盘股成交额']/all_data['全市场总成交额']#微盘股成交额除以总成交额
all_data['微盘股成交额占比均值'] = all_data['微盘股成交额占比'].rolling(10).mean()
all_data['微盘股成交额占比极大值'] = all_data['微盘股成交额占比'].rolling(10).max()
all_data['微盘股成交额占比极小值'] = all_data['微盘股成交额占比'].rolling(10).min()
all_data['微盘股成交额占比乖离率'] = all_data['微盘股成交额占比']/all_data['微盘股成交额占比均值']
all_data['微盘股成交额占比极大乖离率'] = all_data['微盘股成交额占比']/all_data['微盘股成交额占比极大值']
all_data['微盘股成交额占比极小乖离率'] = all_data['微盘股成交额占比']/all_data['微盘股成交额占比极小值']
all_data['微盘股成交额占比变动'] = all_data['微盘股成交额占比']/all_data['微盘股成交额占比'].shift(1)

all_data['微盘股指数均值'] = all_data['close'].rolling(10).mean()
all_data['微盘股指数极大值'] = all_data['close'].rolling(10).max()
all_data['微盘股指数极小值'] = all_data['close'].rolling(10).min()
all_data['微盘股指数乖离率'] = all_data['close']/all_data['微盘股指数均值']
all_data['微盘股指数极大乖离率'] = all_data['close']/all_data['微盘股指数极大值']
all_data['微盘股指数极小乖离率'] = all_data['close']/all_data['微盘股指数极小值']
all_data['微盘股指数变动'] = all_data['close']/all_data['close'].shift(1)

# all_data=all_data[all_data["微盘股成交额占比变动"]>0.9]
# all_data=all_data[all_data["微盘股成交额占比乖离率"]>0.85]
# all_data=all_data[all_data["微盘股成交额占比极大乖离率"]>0.7]

# all_data=all_data[all_data["微盘股指数变动"]<1.08]
# all_data=all_data[all_data["微盘股指数乖离率"]>0.85]
# all_data=all_data[all_data["微盘股指数极大乖离率"]>0.7]

# all_data=all_data[all_data["微盘股成交额占比极小乖离率"]>=1]
# all_data=all_data[all_data["微盘股成交额占比极小乖离率"]>1]#在当前成交额占比处于十日最低点的时候空仓
all_data=all_data[all_data["微盘股成交额极小乖离率"]>1]#在当前成交额占比处于十日最低点的时候空仓
# all_data=all_data[all_data["微盘股指数极小乖离率"]>=1]
all_data=all_data[all_data["微盘股指数极小乖离率"]>1]#在当前指数处于十日最低点的时候空仓
all_data['微盘股指数涨幅']=all_data['close']/all_data['close'].values[0]
all_data['value'] = all_data['target'].cumprod()
all_data.to_csv("微盘股.csv")
print(all_data)
# #设置date列为index，方便画图
# all_data = all_data.set_index('date')
# import matplotlib.pyplot as plt
# from matplotlib import ticker
# plt.rcParams['font.family'] = 'SimHei'  # 设置使用的字体为黑体
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 将黑体设置为默认的无衬线字体
# all_data[['tiny_to_all_ratio']].plot(figsize=(16,9), color=['SteelBlue'],title='小市值拥挤度')
# #蓝线为拥挤度。
# plt.show()