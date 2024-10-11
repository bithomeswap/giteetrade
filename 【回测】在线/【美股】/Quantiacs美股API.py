# #使用anaconda进行安装【仅仅支持linux服务器，windows系统无法执行】
# conda create -n qntdev quantiacs-source::qnt 'python>=3.10,<3.11' conda-forge::ta-lib
# conda activate qntdev
# pip install 'ipywidgets==7.5' 'plotly==4.14' 'matplotlib==3.8.1' 'pandas==1.2.5' 'dash==1.21.0'
# # conda remove -n qntdev quantiacs-source::qnt#删除旧的环境
# conda install -n qntdev quantiacs-source::qnt#安装新的环境


import time
import pandas as pd
import qnt.data as qndata

# ['ADA', 'AUR', 'AVAX', 'BCH', 'BCN', 'BLK', 'BNB', 'BSV', 'BTC', 'BTG',
#  'BTS', 'DASH', 'DGC', 'DGD', 'DOGE', 'DOT', 'EOS', 'ETC', 'ETH', 'FCT',
#  'FRC', 'FTC', 'GNT', 'ICP', 'IFC', 'IXC', 'LINK', 'LSK', 'LTC', 'MAID',
#  'MNC', 'NEO', 'NMC', 'NXT', 'OMNI', 'PPC', 'PTS', 'QRK', 'REP', 'SOL',
#  'STEEM', 'STRAX', 'THETA', 'TRC', 'TRX', 'UNI', 'WAVES', 'WDC', 'XCP',
#  'XEM', 'XLM', 'XMR', 'XPM', 'XPY', 'XRP']

# #获取历史小时K
# alldata = qndata.crypto.load_data(tail=365 * 10,dims=('time','asset',"field"))#dims确定索引层次，从前往后排列
# df=pd.DataFrame({})
# for data in alldata:#根据日期遍历
#     print(data.time)
#     time.sleep(1)
#获取历史日K
alldata = qndata.cryptodaily.load_data(tail=365 * 10,dims=('time','asset',"field"))#dims确定索引层次，从前往后排列
# print(alldata)
df=pd.DataFrame({})
for data in alldata:#根据日期遍历
#     print(data)
    time.sleep(1)
    newdf=pd.DataFrame(data)
    newdf["time"]=newdf.apply(lambda x: x.iloc[0].time.values,axis=1)
#     newdf=newdf.set_index('time')
    newdf["asset"]=newdf.apply(lambda x: x.iloc[0].asset.values,axis=1)
    newdf["open"]=newdf.apply(lambda x: x.iloc[0].values,axis=1)
    newdf["low"]=newdf.apply(lambda x: x.iloc[1].values,axis=1)
    newdf["high"]=newdf.apply(lambda x: x.iloc[2].values,axis=1)
    newdf["close"]=newdf.apply(lambda x: x.iloc[3].values,axis=1)
    newdf["is_liquid"]=newdf.apply(lambda x: x.iloc[4].values,axis=1)
#     newdf.to_csv("数字货币.csv")
    newdf=newdf[["time","asset","open","low","high","close","is_liquid"]]
#     newdf.to_csv("数字货币.csv")
    print(newdf)
    df=pd.concat([df,newdf])
df.to_csv("数字货币历史日K.csv")