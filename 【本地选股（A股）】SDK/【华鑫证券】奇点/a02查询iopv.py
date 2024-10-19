import time

import pandas as pd
from xmdapi import xmdapi#从文件夹当中引入【from 文件夹 引入 文件】
from config import *

from a01查询etf import tradespi

# [能够获取到IOPV数据,就是任务无法主动结束]
import sys

class MdSpi(xmdapi.CTORATstpXMdSpi):
    def __init__(self,api):
        xmdapi.CTORATstpXMdSpi.__init__(self)
        self.__api:xmdapi.CTORATstpXMdApi=api
        self.running = 1
        self.iopv = {} #初始化iopv存储字典
        self.etfinfos = []
        self.etfstocks = []
        self.start_time = time.time()
        self.count = 0
        self.last_change_time = time.time()
        

    def OnFrontConnected(self):#不进行登录和订阅的话就会报错链接错误
        print("OnFrontConnected")
        #请求登录，目前未校验登录用户，请求域置空即可
        login_req=xmdapi.CTORATstpReqUserLoginField()
        self.__api.ReqUserLogin(login_req,1)
        
    def OnRspUserLogin(self,pRspUserLoginField,pRspInfoField,nRequestID):#用户登录并且订阅600621华鑫股份
        if pRspInfoField.ErrorID==0:
            print('Login success! [%d]' % nRequestID)#登录成功
            '''
            订阅行情
            当sub_arr中只有一个"00000000"的合约且ExchangeID填TORA_TSTP_EXD_SSE或TORA_TSTP_EXD_SZSE时，订阅单市场所有合约行情
			当sub_arr中只有一个"00000000"的合约且ExchangeID填TORA_TSTP_EXD_COMM时，订阅全市场所有合约行情
			其它情况,订阅sub_arr集合中的合约行情
            '''

            上交所订阅列表 = []
            深交所订阅列表 = []

            for i in self.etfinfos:
                symbol = i["ETF交易代码"]
                if symbol.startswith("5"):
                    上交所订阅列表.append(symbol)
                elif symbol.startswith("1"):
                    深交所订阅列表.append(symbol)

            for i in self.etfstocks:
                symbol = i["ETF成份证券代码"]
                if symbol.startswith("5"):
                    上交所订阅列表.append(symbol)
                elif symbol.startswith("1"):
                    深交所订阅列表.append(symbol)

            上交所订阅列表 = list(set([str(i).encode() for i in 上交所订阅列表]))
            深交所订阅列表 = list(set([str(i).encode() for i in 深交所订阅列表]))

            print('上交所订阅列表',len(上交所订阅列表))
            print('深交所订阅列表',len(深交所订阅列表))
            
            # 订阅所有数据
            # 上交所订阅列表 = [b'00000000']
            # 深交所订阅列表 = [b'00000000']

            ret = self.__api.SubscribeMarketData(上交所订阅列表,xmdapi.TORA_TSTP_EXD_SSE)#TORA_TSTP_EXD_SSE上交所
            ret = self.__api.SubscribeMarketData(深交所订阅列表,xmdapi.TORA_TSTP_EXD_SZSE)#TORA_TSTP_EXD_SSE上交所
        else:
            print('Login fail!!! [%d] [%d] [%s]'
                %(nRequestID,pRspInfoField.ErrorID,pRspInfoField.ErrorMsg))#登录失败
            

    def OnRtnMarketData(self,pMarketDataField):#返回市场数据详情
        if pMarketDataField:#如果有数据则继续执行【如果不验证则会因为报错中断全部任务】
            if str(pMarketDataField.SecurityID).zfill(6).startswith(("1","5")):#验证是否以1或者5开头
                try:               
                    item={
                        "TradingDay":pMarketDataField.TradingDay,#交易时间
                        "SecurityID":pMarketDataField.SecurityID,
                        "ExchangeID":pMarketDataField.ExchangeID,
                        "SecurityName":pMarketDataField.SecurityName,#中文名
                        "PreClosePrice":pMarketDataField.PreClosePrice,
                        "OpenPrice":pMarketDataField.OpenPrice,
                        "Volume":pMarketDataField.Volume,
                        "Turnover":pMarketDataField.Turnover,
                        "TradingCount":pMarketDataField.TradingCount,
                        "LastPrice":pMarketDataField.LastPrice,
                        "BidPrice1":pMarketDataField.BidPrice1,
                        "BidVolume1":pMarketDataField.BidVolume1,
                        "AskPrice1":pMarketDataField.AskPrice1,
                        "AskVolume1":pMarketDataField.AskVolume1,
                        "UpperLimitPrice":pMarketDataField.UpperLimitPrice,#涨停价
                        "LowerLimitPrice":pMarketDataField.LowerLimitPrice,#跌停价
                        "PreCloseIOPV":pMarketDataField.PreCloseIOPV,
                        "IOPV":pMarketDataField.IOPV,#盘前IOPV数据为0
                    }
                    self.iopv[item['SecurityID']] = item
                    current_time = time.time()
                    self.last_change_time = current_time
                    self.count += 1
                    if self.count%1000==0:
                        print(f'接收={self.count}  iopv数据={len(self.iopv)} 处理速度={round(self.count/(current_time-self.start_time),2)}个/秒')
                except Exception as e:
                    print(e)
        else:
            print('pMarketDataField',pMarketDataField)


    def Wait(self,):
        while self.running:
            time.sleep(1)
            # 有数据且数据中断超过2秒则写入文件并退出
            if self.iopv and time.time() - self.last_change_time>2:
                # ipov字典数据取values
                iopvdf=pd.DataFrame(self.iopv.values())
                iopvdf.to_csv('iopv数据.csv')
                break


# 打印接口版本号
print("XMDAPI版本号::"+xmdapi.CTORATstpXMdApi_GetApiVersion())
print("sys.argv",sys.argv)#系统文件参数，这里就一个，后面的方式应该是同时启动多个文件啥的，或者干脆就是想办法默认获取得到1
argc=len(sys.argv)#【参数1默认执行TCP访问】
print("argc",argc)
XMD_TCP_FrontAddress=marketurl

'''*************************创建实例 注册服务*****************'''
print("************* XMD TCP *************")

#TCP订阅lv1行情，前置Front和FENS方式都用默认构造
thisxmdapi:xmdapi.CTORATstpXMdApi=xmdapi.CTORATstpXMdApi_CreateTstpXMdApi()
# 注册多个行情前置服务地址，用逗号隔开
# 例如:thisxmdapi.RegisterFront("tcp://10.0.1.101:6402,tcp://10.0.1.101:16402")
thisxmdapi.RegisterFront(XMD_TCP_FrontAddress)
print("XMD_TCP_FrontAddress[TCP]::%s" % XMD_TCP_FrontAddress)
# 创建回调对象
spi = MdSpi(thisxmdapi)

# 设置前面获取的etf数据
spi.etfinfos = tradespi.ETFFile
spi.etfstocks = tradespi.ETFBasket

thisxmdapi.RegisterSpi(spi)# 注册回调接口
thisxmdapi.Init()# 启动接口
spi.Wait()# 等待任务执行完成
thisxmdapi.Release()# 释放接口对象

