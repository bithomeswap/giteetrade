#!/usr/bin/python3
# -*- coding:UTF-8 -*-

# conda create -n my_env7 python=3.7#创建环境
# conda env remove -n my_env7#删除环境
# conda activate my_env7#激活环境
#pip install pandas
import pandas as pd
from pathlib import Path
import datetime
from traderapi import traderapi#从文件夹当中引入【from 文件夹 引入 文件】
from xmdapi import xmdapi#从文件夹当中引入【from 文件夹 引入 文件】
''' 注意:如果提示找不到_tradeapi 且与已发布的库文件不一致时,可自行重命名为_tradeapi.so (windows下为_tradeapi.pyd)'''

#投资者账户 
InvestorID="00030557";   
'''
该默认账号为共用连通测试使用,自有测试账号请到n-sight.com.cn注册并从个人中心获取交易编码,不是网站登录密码,不是手机号
实盘交易时，取客户号，请注意不是资金账号或咨询技术支持
'''
#操作员账户
UserID="00030557";	   #同客户号保持一致即可
#资金账户 
AccountID="00030557";		#以Req(TradingAccount)查询的为准
#登陆密码
Password="17522830";		#N视界注册模拟账号的交易密码，不是登录密码
DepartmentID="0001";		#生产环境默认客户号的前4位
SSE_ShareHolderID='A00030557'   #不同账号的股东代码需要接口ReqQryShareholderAccount去查询
SZ_ShareHolderID='700030557'    #不同账号的股东代码需要接口ReqQryShareholderAccount去查询



# 仿真
# 行情：tcp://210.14.72.21:4402  
# 交易：tcp://210.14.72.21:4400
# 交易、行情fens地址：
# tcp://210.14.72.21:42370
# A套：
# 行情前置地址：tcp://210.14.72.16:9402
# 交易前置地址：tcp://210.14.72.15:4400
# B套：
# 行情前置地址：tcp://210.14.72.16:9402
# 交易前置地址：tcp://210.14.72.16:9500
# #【仿真】
# marketurl="tcp://210.14.72.21:4402"
# tradeurl="tcp://210.14.72.21:4400"
#【A套】
marketurl="tcp://210.14.72.16:9402"
tradeurl="tcp://210.14.72.15:4400"
# #【B套】
# marketurl="tcp://210.14.72.16:9402"
# tradeurl="tcp://210.14.72.16:9500"



class TraderSpi(traderapi.CTORATstpTraderSpi):
    def __init__(self,api):
        traderapi.CTORATstpTraderSpi.__init__(self)
        self.__api:traderapi.CTORATstpTraderApi=api
        self.__req_id=0
        self.__front_id=0
        self.__session_id=0
        self.ETFFile=[]#ETFFile初始化为空列表【类当中内创建的变量，在该类的方法当中调用时需要加上self.作为前缀】int是特殊的方法，在非方法中使用时不需要self.作为前缀
        self.ETFBasket=[]#ETFBasket初始化为空列表【类当中内创建的变量，在该类的方法当中调用时需要加上self.作为前缀】int是特殊的方法，在非方法中使用时不需要self.作为前缀

    def OnFrontConnected(self) -> "void":
        print('OnFrontConnected')
        # 获取终端信息
        self.__req_id+=1
        ret=self.__api.ReqGetConnectionInfo(self.__req_id)
        if ret!=0:
            print('ReqGetConnectionInfo fail,ret[%d]' % ret)
    def OnFrontDisconnected(self,nReason:"int") -> "void":
        print('OnFrontDisconnected:[%d]' % nReason)
    def OnRspGetConnectionInfo(self,pConnectionInfoField:"CTORATstpConnectionInfoField",pRspInfoField:"CTORATstpRspInfoField",nRequestID:"int") -> "void":
        if pRspInfoField.ErrorID==0:
            print('inner_ip_address[%s]' % pConnectionInfoField.InnerIPAddress)
            print('inner_port[%d]' % pConnectionInfoField.InnerPort)
            print('outer_ip_address[%s]' % pConnectionInfoField.OuterIPAddress)
            print('outer_port[%d]' % pConnectionInfoField.OuterPort)
            print('mac_address[%s]' % pConnectionInfoField.MacAddress)
            #请求登录
            login_req=traderapi.CTORATstpReqUserLoginField()
            # 支持以用户代码、资金账号和股东账号方式登录
		    # （1）以用户代码方式登录
            login_req.LogInAccount=UserID
            login_req.LogInAccountType=traderapi.TORA_TSTP_LACT_UserID
		    # （2）以资金账号方式登录
            #login_req.DepartmentID=DepartmentID
            #login_req.LogInAccount=AccountID
            #login_req.LogInAccountType=traderapi.TORA_TSTP_LACT_AccountID
		    # （3）以上海股东账号方式登录
            #login_req.LogInAccount=SSE_ShareHolderID
            #login_req.LogInAccountType=traderapi.TORA_TSTP_LACT_SHAStock
		    # （4）以深圳股东账号方式登录
            #login_req.LogInAccount=SZSE_ShareHolderID
            #login_req.LogInAccountType=traderapi.TORA_TSTP_LACT_SZAStock

		    # 支持以密码和指纹(移动设备)方式认证
		    # （1）密码认证
		    # 密码认证时AuthMode可不填
            #login_req.AuthMode=traderapi.TORA_TSTP_AM_Password
            login_req.Password=Password
		    # （2）指纹认证
		    # 非密码认证时AuthMode必填
            #login_req.AuthMode=traderapi.TORA_TSTP_AM_FingerPrint
            #login_req.DeviceID='03873902'
            #login_req.CertSerial='9FAC09383D3920CAEFF039'
		
		    # 终端信息采集
		    # UserProductInfo填写终端名称
            login_req.UserProductInfo='pyapidemo'
		    # 按照监管要求填写终端信息
            login_req.TerminalInfo='PC;IIP=000.000.000.000;IPORT=00000;LIP=x.xx.xxx.xxx;MAC=123ABC456DEF;HD=XXXXXXXXXX'
		    # 以下内外网IP地址若不填则柜台系统自动采集，若填写则以终端填值为准报送
            #login_req.MacAddress='5C-87-9C-96-F3-E3'
            #login_req.InnerIPAddress='10.0.1.102'
            #login_req.OuterIPAddress='58.246.43.50'

            self.__req_id+=1
            ret=self.__api.ReqUserLogin(login_req,self.__req_id)
            if ret!=0:
                print('ReqUserLogin fail,ret[%d]' % ret)
        else:
            print('GetConnectionInfo fail,[%d] [%d] [%s]!!!' % (nRequestID,pRspInfoField.ErrorID,pRspInfoField.ErrorMsg))


    def QueryEtf(self,):#这里取出来的数据跟同花顺实盘的数据不完全一致
        self.QryETFFileField()
        self.QryETFBasketField()

    def QryETFFileField(self,):
        # 查询ETF清单信息
        req_field=traderapi.CTORATstpQryETFFileField()
        # 以下字段不填表示不设过滤条件，即查询所有etf
        # req_field.ExchangeID=traderapi.TORA_TSTP_EXD_SSE
        print("查询 QryETFFileField")
        self.__req_id+=1
        ret=self.__api.ReqQryETFFile(req_field,self.__req_id)
        if ret!=0:
            print('ReqQryETFFile fail,ret[%d]' % ret)

    def QryETFBasketField(self,):
        # 查询ETF成份证券信息
        print("查询 QryETFBasketField")
        req_field=traderapi.CTORATstpQryETFBasketField()
        # 以下字段不填表示不设过滤条件，即查询所有etf
        # req_field.ExchangeID=traderapi.TORA_TSTP_EXD_SSE
        self.__req_id+=1
        ret=self.__api.ReqQryETFBasket(req_field,self.__req_id)
        if ret!=0:
            print('ReqQryETFFile fail,ret[%d]' % ret)

    def OnRspQryETFFile(self,pETFFileField:traderapi.CTORATstpETFFileField,pRspInfoField:traderapi.CTORATstpRspInfoField,nRequestID:int,bIsLast:bool) -> "void":
        if pETFFileField:#如果有数据则继续执行【如果不验证则会因为报错中断全部任务】
            self.ETFFile.append({
                "交易日":pETFFileField.TradingDay,
                "交易所代码":pETFFileField.ExchangeID,
                "ETF交易代码":pETFFileField.ETFSecurityID,
                "ETF申赎代码":pETFFileField.ETFCreRedSecurityID,
                "最小申购赎回单位份数":pETFFileField.CreationRedemptionUnit,
                "最大现金替代比例":pETFFileField.Maxcashratio,
                "预估现金差额":pETFFileField.EstimateCashComponent,
                "前一交易日现金差额":pETFFileField.CashComponent,
                "前一交易日基金单位净值":pETFFileField.NAV,
                "前一交易日申赎基准单位净值":pETFFileField.NAVperCU,
                "当日申购赎回基准单位的红利金额":pETFFileField.DividendPerCU,
                "ETF申赎类型":pETFFileField.ETFCreRedType,
                "ETF证券名称":pETFFileField.ETFSecurityName,
            })
        if bIsLast:#这里是查询结束了进行输出
            df=pd.DataFrame(self.ETFFile)
            print("ETF清单信息输出开始")
            df.to_csv(f"ETF清单信息{start_time}.csv")
            print("ETF清单信息输出完毕")
            # time.sleep(self.interval)
            # self.ETFFile=[]
            # self.QryETFFileField()#这个是循环执行任务

    def OnRspQryETFBasket(self,pETFBasketField:traderapi.CTORATstpETFBasketField,pRspInfoField:traderapi.CTORATstpRspInfoField,nRequestID:int,bIsLast:bool) -> "void":
        if pETFBasketField:#如果有数据则继续执行【如果不验证则会因为报错中断全部任务】
            self.ETFBasket.append({
                "交易日":pETFBasketField.TradingDay,
                "交易所代码":pETFBasketField.ExchangeID,
                "ETF交易代码":pETFBasketField.ETFSecurityID,
                "ETF成份证券代码":pETFBasketField.SecurityID,
                "成分证券名称":pETFBasketField.SecurityName,
                "成分证券数量":pETFBasketField.Volume,
                "现金替代标志":pETFBasketField.ETFCurrenceReplaceStatus,
                "溢价比例":pETFBasketField.Premium,
                "申购替代金额":pETFBasketField.CreationReplaceAmount,
                "赎回替代金额":pETFBasketField.RedemptionReplaceAmount,
                "挂牌市场":pETFBasketField.MarketID,
                "ETF申赎类型":pETFBasketField.ETFCreRedType
            })
        if bIsLast:#这里是查询结束了进行输出
            df=pd.DataFrame(self.ETFBasket)
            print("ETF成份证券信息输出开始")
            df.to_csv(f"ETF成份证券信息{start_time}.csv")
            print("ETF成份证券信息输出完毕")
            # time.sleep(self.interval)
            # self.ETFBasket=[]
            # self.QryETFBasketField()#这个是循环执行任务

    def OnRspUserLogin(self,pRspUserLoginField:"traderapi.CTORATstpRspUserLoginField",pRspInfoField:"CTORATstpRspInfoField",nRequestID:"int") -> "void":
        if pRspInfoField.ErrorID==0:
            print('Login success! [%d]' % nRequestID)
            self.__front_id=pRspUserLoginField.FrontID
            self.__session_id=pRspUserLoginField.SessionID
            self.QueryEtf()
        else:
            print('Login fail!!! [%d] [%d] [%s]'
                % (nRequestID,pRspInfoField.ErrorID,pRspInfoField.ErrorMsg))
        return

#确认当日时间
start_time=datetime.datetime.now().strftime("%Y%m%d")#特殊的时间格式
old_time=(datetime.datetime.now()-datetime.timedelta(days=90)).strftime("%Y%m%d")#特殊的时间格式
print("start_time",start_time,"old_time",old_time)
interval=5#控制请求频率[针对循环型请求]

# 【交易SDK】
# 打印接口版本号
print("thistraderapi Version:::"+traderapi.CTORATstpTraderApi_GetApiVersion())
# 创建接口对象
# pszFlowPath为私有流和公有流文件存储路径，若订阅私有流和公有流且创建多个接口实例，每个接口实例应配置不同的路径
# bEncrypt为网络数据是否加密传输，考虑数据安全性，建议以互联网方式接入的终端设置为加密传输
thistraderapi:traderapi.CTORATstpTraderApi=traderapi.CTORATstpTraderApi.CreateTstpTraderApi('./flow',False)
# 创建回调对象
spi=TraderSpi(thistraderapi)
# 注册回调接口
thistraderapi.RegisterSpi(spi)
# 注册单个交易前置服务地址
TD_TCP_FrontAddress=tradeurl
# "tcp://210.14.72.21:4400" #仿真交易环境
# TD_TCP_FrontAddress="tcp://210.14.72.15:4400" #24小时环境A套
# TD_TCP_FrontAddress="tcp://210.14.72.16:9500" #24小时环境B套

thistraderapi.RegisterFront(TD_TCP_FrontAddress)
# 注册多个交易前置服务地址，用逗号隔开 形如:thistraderapi.RegisterFront("tcp://10.0.1.101:6500,tcp://10.0.1.101:26500")
print("TD_TCP_FensAddress[sim or 24H]::%s\n"%TD_TCP_FrontAddress)

#订阅私有流
thistraderapi.SubscribePrivateTopic(traderapi.TORA_TERT_QUICK)
#订阅公有流
thistraderapi.SubscribePublicTopic(traderapi.TORA_TERT_QUICK)
'''**********************************
*	TORA_TERT_RESTART,从日初开始
*	TORA_TERT_RESUME,从断开时候开始
*	TORA_TERT_QUICK,从最新时刻开始
*************************************'''

# 启动接口【启动了单独的线程】
thistraderapi.Init()

#[根据时间结束任务]
# import time
# time.sleep(60)# 等待程序结束[其中的一个文件在收盘之后就失效了]

#[根据生成文件是否达标结束任务]
etffile=False
etfbasket=False
import time
while True:
    time.sleep(2)
    try:
        #【验证ETF清单信息】
        etfinfodf=pd.read_csv(f"ETF清单信息{start_time}.csv")
        etfinfodf['ETF交易代码']=etfinfodf['ETF交易代码'].apply(lambda x:str(x).zfill(6))
        etfinfodf['ETF申赎代码']=etfinfodf['ETF交易代码'].apply(lambda x:str(x).zfill(6))
        print(etfinfodf)
        etfinfodf=etfinfodf.iloc[:, 1:]#这样一样可以去掉第一行避免空数据干扰
        # etfinfodf=etfinfodf.drop('Unnamed: 0',axis=1)#去掉空白行【:不能错，不能多空格】
        # 这里的前一交易日基金单位净值是四舍五入之后的数据，
        # 应该以前一交易日申赎基准单位净值为准计算单笔最小下单金额和单位净值。
        etfinfodf["前一交易日基金单位净值"]=etfinfodf["前一交易日申赎基准单位净值"]/etfinfodf["最小申购赎回单位份数"]
        if len(etfinfodf)>900:#平时900
            print(etfinfodf.columns.tolist(),type(etfinfodf.columns.tolist()))
            if etfinfodf.columns.tolist()==['交易日','交易所代码','ETF交易代码','ETF申赎代码',
                            '最小申购赎回单位份数','最大现金替代比例','预估现金差额',
                            '前一交易日现金差额','前一交易日基金单位净值','前一交易日申赎基准单位净值',
                            '当日申购赎回基准单位的红利金额','ETF申赎类型','ETF证券名称']:
                etffile=True
        #【验证ETF成分券信息】
        etfstocksdf=pd.read_csv(f"ETF成份证券信息{start_time}.csv")
        etfstocksdf['ETF交易代码']=etfstocksdf['ETF交易代码'].apply(lambda x:str(x).zfill(6))
        etfstocksdf['ETF成份证券代码']=etfstocksdf['ETF成份证券代码'].apply(lambda x:str(x).zfill(6))
        etfstocksdf=etfstocksdf.iloc[:, 1:]#这样一样可以去掉第一行避免空数据干扰
        # etfstocksdf=etfstocksdf.drop('Unnamed: 0',axis=1)#去掉空白行【:不能错，不能多空格】
        if len(etfstocksdf)>100000:#平时110000
            print(etfstocksdf.columns.tolist(),type(etfstocksdf.columns.tolist()))
            if etfstocksdf.columns.tolist()==['交易日','交易所代码','ETF交易代码','ETF成份证券代码',
                            '成分证券名称','成分证券数量','现金替代标志','溢价比例',
                            '申购替代金额','赎回替代金额','挂牌市场','ETF申赎类型']:
                etfbasket=True
    except Exception as e:
        print("数据不匹配",e)
    if (etffile==True)and(etfbasket==True):
        print("数据已经获取成功任务结束")
        break

# thistraderapi.Join()# 加入任务
# input()# 等待程序结束[不确定几分钟结束]一直没结束
thistraderapi.Release()# 释放接口对象



# [能够获取到IOPV数据,就是任务无法主动结束]
import sys
class MdSpi(xmdapi.CTORATstpXMdSpi):
    def __init__(self,api):
        xmdapi.CTORATstpXMdSpi.__init__(self)
        self.__api=api
    def OnFrontConnected(self):#不进行登录和订阅的话就会报错链接错误
        print("OnFrontConnected")
        #请求登录，目前未校验登录用户，请求域置空即可
        login_req=xmdapi.CTORATstpReqUserLoginField()
        self.__api.ReqUserLogin(login_req,1)
        self.iopv=[]#初始化iopv存储字典
        self.stocks=[]#初始化stocks存储字典
    def OnRspUserLogin(self,pRspUserLoginField,pRspInfoField,nRequestID):#用户登录并且订阅600621华鑫股份
        if pRspInfoField.ErrorID==0:
            print('Login success! [%d]' % nRequestID)#登录成功
            '''
            订阅行情
            当sub_arr中只有一个"00000000"的合约且ExchangeID填TORA_TSTP_EXD_SSE或TORA_TSTP_EXD_SZSE时，订阅单市场所有合约行情
			当sub_arr中只有一个"00000000"的合约且ExchangeID填TORA_TSTP_EXD_COMM时，订阅全市场所有合约行情
			其它情况,订阅sub_arr集合中的合约行情
            '''
            # 【订阅列表】
            for symbol in etfinfodf["ETF交易代码"].tolist():
                # symbol=str(index).zfill(6)#前面已经处理了
                # print(symbol,type(symbol))
                if str(symbol).startswith("5"):#上交所ETF
                    sub_arr=[str(symbol).encode()]#
                    ret=self.__api.SubscribeMarketData(sub_arr,xmdapi.TORA_TSTP_EXD_SSE)#TORA_TSTP_EXD_SSE上交所
                elif str(symbol).startswith("159"):#深交所ETF
                    sub_arr=[str(symbol).encode()]#
                    ret=self.__api.SubscribeMarketData(sub_arr,xmdapi.TORA_TSTP_EXD_SZSE)#TORA_TSTP_EXD_SZSE深交所
                    
            for symbol in etfstocksdf["ETF成份证券代码"].tolist():
                # symbol=str(index).zfill(6)#前面已经处理了
                # print(symbol,type(symbol))
                if str(symbol).startswith(("60","68","11")):#上交所"60","68","11"分别是上交所主板、上交所科创板、上交所可转债
                    sub_arr=[str(symbol).encode()]#
                    ret=self.__api.SubscribeMarketData(sub_arr,xmdapi.TORA_TSTP_EXD_SSE)#TORA_TSTP_EXD_SSE上交所
                elif str(symbol).startswith(("00","30","12")):#深交所"00","30","12"分别是深交所主板、深交所创业板、深交所可转债
                    sub_arr=[str(symbol).encode()]#
                    ret=self.__api.SubscribeMarketData(sub_arr,xmdapi.TORA_TSTP_EXD_SZSE)#TORA_TSTP_EXD_SZSE深交所
            # 【订阅单个标的】
            # sub_arr=[b'159302']#b""前缀表示这是一个字节字符串（bytes literal）
            # ret=self.__api.SubscribeMarketData(sub_arr,xmdapi.TORA_TSTP_EXD_SZSE)#TORA_TSTP_EXD_SZSE深交所，TORA_TSTP_EXD_SSE上交所
            # if ret!=0:
            #     print('SubscribeMarketData fail,ret[%d]' % ret)
            # else:
            #     print('SubscribeMarketData success,ret[%d]' % ret)       
        else:
            print('Login fail!!! [%d] [%d] [%s]'
                %(nRequestID,pRspInfoField.ErrorID,pRspInfoField.ErrorMsg))#登录失败
    def OnRspSubMarketData(self,pSpecificSecurityField,pRspInfoField):#接收已订阅市场数据
        if pRspInfoField.ErrorID==0:
            # print('OnRspSubMarketData:OK!')#接收已订阅市场数据成功
            pass
        else:
            print('OnRspSubMarketData:Error! [%d] [%s]'
                %(pRspInfoField.ErrorID,pRspInfoField.ErrorMsg))
    def OnRspUnSubMarketData(self,pSpecificSecurityField,pRspInfoField):#接收未订阅市场数据
        if pRspInfoField.ErrorID==0:
            print('OnRspUnSubMarketData:OK!')#接收未订阅市场数据成功
        else:
            print('OnRspUnSubMarketData:Error! [%d] [%s]'
                %(pRspInfoField.ErrorID,pRspInfoField.ErrorMsg))
    def OnRspSubRapidMarketData(self,pSpecificSecurityField,pRspInfoField):
        if pRspInfoField.ErrorID==0:
            print('OnRspSubRapidMarketData:OK!')
        else:
            print('OnRspSubRapidMarketData:Error! [%d] [%s]'
                %(pRspInfoField.ErrorID,pRspInfoField.ErrorMsg))
    def OnRtnMarketData(self,pMarketDataField):#返回市场数据详情
        if pMarketDataField:#如果有数据则继续执行【如果不验证则会因为报错中断全部任务】
            # print(pMarketDataField.SecurityID,type(pMarketDataField.SecurityID))
            if str(pMarketDataField.SecurityID).zfill(6).startswith(("159","5")):#验证是否以159{深证基金}或者5{上证基金}开头
                # print(pMarketDataField.SecurityID,type(pMarketDataField.SecurityID))
                thisiopv={
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
                    # TradingDay = property(_xmdapi.CTORATstpMarketDataField_TradingDay_get, _xmdapi.CTORATstpMarketDataField_TradingDay_set)
                    # SecurityID = property(_xmdapi.CTORATstpMarketDataField_SecurityID_get, _xmdapi.CTORATstpMarketDataField_SecurityID_set)
                    # ExchangeID = property(_xmdapi.CTORATstpMarketDataField_ExchangeID_get, _xmdapi.CTORATstpMarketDataField_ExchangeID_set)
                    # SecurityName = property(_xmdapi.CTORATstpMarketDataField_SecurityName_get, _xmdapi.CTORATstpMarketDataField_SecurityName_set)
                    # PreClosePrice = property(_xmdapi.CTORATstpMarketDataField_PreClosePrice_get, _xmdapi.CTORATstpMarketDataField_PreClosePrice_set)
                    # OpenPrice = property(_xmdapi.CTORATstpMarketDataField_OpenPrice_get, _xmdapi.CTORATstpMarketDataField_OpenPrice_set)
                    # Volume = property(_xmdapi.CTORATstpMarketDataField_Volume_get, _xmdapi.CTORATstpMarketDataField_Volume_set)
                    # Turnover = property(_xmdapi.CTORATstpMarketDataField_Turnover_get, _xmdapi.CTORATstpMarketDataField_Turnover_set)
                    # TradingCount = property(_xmdapi.CTORATstpMarketDataField_TradingCount_get, _xmdapi.CTORATstpMarketDataField_TradingCount_set)
                    # LastPrice = property(_xmdapi.CTORATstpMarketDataField_LastPrice_get, _xmdapi.CTORATstpMarketDataField_LastPrice_set)
                    # HighestPrice = property(_xmdapi.CTORATstpMarketDataField_HighestPrice_get, _xmdapi.CTORATstpMarketDataField_HighestPrice_set)
                    # LowestPrice = property(_xmdapi.CTORATstpMarketDataField_LowestPrice_get, _xmdapi.CTORATstpMarketDataField_LowestPrice_set)
                    # BidPrice1 = property(_xmdapi.CTORATstpMarketDataField_BidPrice1_get, _xmdapi.CTORATstpMarketDataField_BidPrice1_set)
                    # AskPrice1 = property(_xmdapi.CTORATstpMarketDataField_AskPrice1_get, _xmdapi.CTORATstpMarketDataField_AskPrice1_set)
                    # UpperLimitPrice = property(_xmdapi.CTORATstpMarketDataField_UpperLimitPrice_get, _xmdapi.CTORATstpMarketDataField_UpperLimitPrice_set)
                    # LowerLimitPrice = property(_xmdapi.CTORATstpMarketDataField_LowerLimitPrice_get, _xmdapi.CTORATstpMarketDataField_LowerLimitPrice_set)
                    # PERatio1 = property(_xmdapi.CTORATstpMarketDataField_PERatio1_get, _xmdapi.CTORATstpMarketDataField_PERatio1_set)
                    # PERatio2 = property(_xmdapi.CTORATstpMarketDataField_PERatio2_get, _xmdapi.CTORATstpMarketDataField_PERatio2_set)
                    # PriceUpDown1 = property(_xmdapi.CTORATstpMarketDataField_PriceUpDown1_get, _xmdapi.CTORATstpMarketDataField_PriceUpDown1_set)
                    # PriceUpDown2 = property(_xmdapi.CTORATstpMarketDataField_PriceUpDown2_get, _xmdapi.CTORATstpMarketDataField_PriceUpDown2_set)
                    # OpenInterest = property(_xmdapi.CTORATstpMarketDataField_OpenInterest_get, _xmdapi.CTORATstpMarketDataField_OpenInterest_set)
                    # BidVolume1 = property(_xmdapi.CTORATstpMarketDataField_BidVolume1_get, _xmdapi.CTORATstpMarketDataField_BidVolume1_set)
                    # AskVolume1 = property(_xmdapi.CTORATstpMarketDataField_AskVolume1_get, _xmdapi.CTORATstpMarketDataField_AskVolume1_set)
                    # BidPrice2 = property(_xmdapi.CTORATstpMarketDataField_BidPrice2_get, _xmdapi.CTORATstpMarketDataField_BidPrice2_set)
                    # BidVolume2 = property(_xmdapi.CTORATstpMarketDataField_BidVolume2_get, _xmdapi.CTORATstpMarketDataField_BidVolume2_set)
                    # AskPrice2 = property(_xmdapi.CTORATstpMarketDataField_AskPrice2_get, _xmdapi.CTORATstpMarketDataField_AskPrice2_set)
                    # AskVolume2 = property(_xmdapi.CTORATstpMarketDataField_AskVolume2_get, _xmdapi.CTORATstpMarketDataField_AskVolume2_set)
                    # BidPrice3 = property(_xmdapi.CTORATstpMarketDataField_BidPrice3_get, _xmdapi.CTORATstpMarketDataField_BidPrice3_set)
                    # BidVolume3 = property(_xmdapi.CTORATstpMarketDataField_BidVolume3_get, _xmdapi.CTORATstpMarketDataField_BidVolume3_set)
                    # AskPrice3 = property(_xmdapi.CTORATstpMarketDataField_AskPrice3_get, _xmdapi.CTORATstpMarketDataField_AskPrice3_set)
                    # AskVolume3 = property(_xmdapi.CTORATstpMarketDataField_AskVolume3_get, _xmdapi.CTORATstpMarketDataField_AskVolume3_set)
                    # BidPrice4 = property(_xmdapi.CTORATstpMarketDataField_BidPrice4_get, _xmdapi.CTORATstpMarketDataField_BidPrice4_set)
                    # BidVolume4 = property(_xmdapi.CTORATstpMarketDataField_BidVolume4_get, _xmdapi.CTORATstpMarketDataField_BidVolume4_set)
                    # AskPrice4 = property(_xmdapi.CTORATstpMarketDataField_AskPrice4_get, _xmdapi.CTORATstpMarketDataField_AskPrice4_set)
                    # AskVolume4 = property(_xmdapi.CTORATstpMarketDataField_AskVolume4_get, _xmdapi.CTORATstpMarketDataField_AskVolume4_set)
                    # BidPrice5 = property(_xmdapi.CTORATstpMarketDataField_BidPrice5_get, _xmdapi.CTORATstpMarketDataField_BidPrice5_set)
                    # BidVolume5 = property(_xmdapi.CTORATstpMarketDataField_BidVolume5_get, _xmdapi.CTORATstpMarketDataField_BidVolume5_set)
                    # AskPrice5 = property(_xmdapi.CTORATstpMarketDataField_AskPrice5_get, _xmdapi.CTORATstpMarketDataField_AskPrice5_set)
                    # AskVolume5 = property(_xmdapi.CTORATstpMarketDataField_AskVolume5_get, _xmdapi.CTORATstpMarketDataField_AskVolume5_set)
                    # UpdateTime = property(_xmdapi.CTORATstpMarketDataField_UpdateTime_get, _xmdapi.CTORATstpMarketDataField_UpdateTime_set)
                    # UpdateMillisec = property(_xmdapi.CTORATstpMarketDataField_UpdateMillisec_get, _xmdapi.CTORATstpMarketDataField_UpdateMillisec_set)
                    # ClosePrice = property(_xmdapi.CTORATstpMarketDataField_ClosePrice_get, _xmdapi.CTORATstpMarketDataField_ClosePrice_set)
                    # SettlementPrice = property(_xmdapi.CTORATstpMarketDataField_SettlementPrice_get, _xmdapi.CTORATstpMarketDataField_SettlementPrice_set)
                    # MDSecurityStat = property(_xmdapi.CTORATstpMarketDataField_MDSecurityStat_get, _xmdapi.CTORATstpMarketDataField_MDSecurityStat_set)
                    # HWLevel = property(_xmdapi.CTORATstpMarketDataField_HWLevel_get, _xmdapi.CTORATstpMarketDataField_HWLevel_set)
                    # PreCloseIOPV = property(_xmdapi.CTORATstpMarketDataField_PreCloseIOPV_get, _xmdapi.CTORATstpMarketDataField_PreCloseIOPV_set)
                    # IOPV = property(_xmdapi.CTORATstpMarketDataField_IOPV_get, _xmdapi.CTORATstpMarketDataField_IOPV_set)
                }
                if len(self.iopv)==0:#【第一行不需要验证是否有旧数据】ETF的IOPV数据少于5000条时直接添加【超过6000条会因为内存原因导致任务终止】
                    pass
                else:
                    self.iopv = [item for item in self.iopv if item['SecurityID'] != pMarketDataField.SecurityID]#只去掉已有的行
                self.iopv.append(thisiopv)
            else:
                # print(pMarketDataField.SecurityID,type(pMarketDataField.SecurityID))
                thisstocks={
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
                if len(self.stocks)==0:#【第一行不需要验证是否有旧数据】ETF的IOPV数据少于5000条时直接添加【超过6000条会因为内存原因导致任务终止】
                    pass
                else:
                    self.stocks = [item for item in self.stocks if item['SecurityID'] != pMarketDataField.SecurityID]#只去掉已有的行
                self.stocks.append(thisstocks)
                # input()#验证是否会阻塞住【验证结果是会阻塞】input() 函数用于获取用户输入。当你调用 input() 函数时，程序会暂停执行，等待用户在控制台输入文本。用户输入的文本在按下回车键后会被 input() 函数接收，并返回一个字符串类型的值。
    def OnRtnRapidMarketData(self,pRapidMarketDataField):
        print("SecurityID[%s] LastPrice[%.2f] TotalVolumeTrade[%d] TotalValueTrade[%.2f] BidPrice1[%.2f] BidVolume1[%d] BidCount1[%d] AskPrice1[%.2f] AskVolume1[%d] AskCount1[%d] UpperLimitPrice[%.2f] LowerLimitPrice[%.2f]"
            % (pRapidMarketDataField.SecurityID,pRapidMarketDataField.LastPrice,pRapidMarketDataField.TotalVolumeTrade,
               pRapidMarketDataField.TotalValueTrade,pRapidMarketDataField.BidPrice1,pRapidMarketDataField.BidVolume1,pRapidMarketDataField.BidCount1,pRapidMarketDataField.AskPrice1,
               pRapidMarketDataField.AskVolume1,pRapidMarketDataField.AskCount1,pRapidMarketDataField.UpperLimitPrice,pRapidMarketDataField.LowerLimitPrice))

# 打印接口版本号
print("XMDAPI版本号::"+xmdapi.CTORATstpXMdApi_GetApiVersion())
print("sys.argv",sys.argv)#系统文件参数，这里就一个，后面的方式应该是同时启动多个文件啥的，或者干脆就是想办法默认获取得到1
argc=len(sys.argv)#【参数1默认执行TCP访问】
print("argc",argc)
XMD_TCP_FrontAddress=marketurl

'''*************************创建实例 注册服务*****************'''
print("************* XMD TCP *************")

#TCP订阅lv1行情，前置Front和FENS方式都用默认构造
thisxmdapi=xmdapi.CTORATstpXMdApi_CreateTstpXMdApi()
thisxmdapi.RegisterFront(XMD_TCP_FrontAddress)
# 注册多个行情前置服务地址，用逗号隔开
# 例如:thisxmdapi.RegisterFront("tcp://10.0.1.101:6402,tcp://10.0.1.101:16402")
print("XMD_TCP_FrontAddress[TCP]::%s" % XMD_TCP_FrontAddress)
#【初始化iopvdf】
iopvdf=pd.DataFrame({})#用来拼接iopv数据的列表
# 创建回调对象
spi=MdSpi(thisxmdapi)
# 注册回调接口
thisxmdapi.RegisterSpi(spi)
# 启动接口【启动了单独的线程】
thisxmdapi.Init()



def symbol_convert(stock):#股票代码加后缀
    #北交所的股票8字开头，包括82、83、87、88，其中82开头的股票表示优先股；83和87开头的股票表示普通股票、88开头的股票表示公开发行的。
    if (stock.startswith("60"))or(#上交所主板
        stock.startswith("68"))or(#上交所科创板
        stock.startswith("11"))or(#上交所可转债
        (stock.startswith("5"))):#上交所ETF：51、52、56、58都是
        return str(str(stock)+".SH")
        # return str(str(stock)+".SS")
    elif (stock.startswith("00"))or(#深交所主板
        stock.startswith("30"))or(#深交所创业板
        stock.startswith("12"))or(#深交所可转债
        (stock.startswith("159"))):#深交所ETF：暂时只有159的是深交所ETF
        return str(str(stock)+".SZ")
    else:
        print("不在后缀转换名录",str(stock))
        return str(str(stock))
# 【ETF申赎套利前一天成交额低于5000万的都不要看（大概300多只将近400只ETF符合日成交额5000w的标准）】使用akshre或者tushare验证最近10天的平均成交额，至少要近10天平均交易额大于100倍单份申购额，要不大概率是亏损的
lastETFdf=etfinfodf.copy()
try:
    lastETFdf=pd.read_csv(f"ETF清单信息成交额过滤后{start_time}.csv")
    lastETFdf['ETF交易代码']=lastETFdf['ETF交易代码'].apply(lambda x:str(x).zfill(6))
    lastETFdf['ETF申赎代码']=lastETFdf['ETF交易代码'].apply(lambda x:str(x).zfill(6))
    print(lastETFdf)
    lastETFdf=lastETFdf.iloc[:, 1:]#这样一样可以去掉第一行避免空数据干扰
    print("当日已经处理ETF成交额过滤")#这里应该还有一个格式处理
except Exception as e:
    print("当日尚未处理ETF成交额过滤")#这种一条条的筛选可能不太好，因为毕竟有1000条呢，速度和限频都不好处理
    # pip install xcsc-tushare
    import xcsc_tushare as ts
    # ts.set_token('7ed61c98882a320cadce6481aef04ebf7853807179d45ee7f72089d7')
    # ts.pro_api(server='http://116.128.206.39:7172')   #指定tocken对应的环境变量，此处以生产为例
    pro = ts.pro_api('7ed61c98882a320cadce6481aef04ebf7853807179d45ee7f72089d7',server='http://116.128.206.39:7172')
    #获取交易日数据
    daydf = pro.trade_cal(exchange='SZSE', start_date=old_time, end_date=start_time)#获取深证的交易日交易所 SZN-深股通,SHN-沪股通,SSE-上海证券交易所,SZSE-深圳证券交易所
    print(daydf)
    old_day=daydf["trade_date"].values[-10]#取最近10个交易日
    print(old_day)
    # lastETFdf["ETF交易代码"]=lastETFdf["ETF交易代码"].apply(lambda x:symbol_convert(x)).astype(str) # 需要指定类型为字符串
    for symbol in lastETFdf["ETF交易代码"].tolist():
        print(symbol)
        thisdf = pro.fund_daily(ts_code=symbol_convert(symbol),
                                start_date=old_day,
                                end_date=start_time,
                                field='ts_code,trade_date,pre_close,open,high,low,close,amount')
        money=thisdf["amount"].mean()#amount成交额(单位是千元)
        lastETFdf.loc[lastETFdf["ETF交易代码"]==symbol,"15日平均成交额"]=money
        time.sleep(0.21)#每分钟最多访问300次否则限频
        # print(symbol,thisdf)

    # #pip install akshare【差多了会报错】
    # import akshare as ak
    # for symbol in lastETFdf["ETF交易代码"].tolist():
    #     print(symbol)
    #     thisdf=ak.fund_etf_hist_em(
    #                 symbol=symbol,
    #                 period= "daily",
    #                 start_date= old_time,
    #                 end_date= start_time,
    #                 adjust= "",#默认返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据
    #                 )#ETF历史行情
    #     thisdf=thisdf[-15:]#只要后15行
    #     money=thisdf["成交额"].mean()
    #     lastETFdf.loc[lastETFdf["ETF交易代码"]==symbol,"15日平均成交额"]=money
    #     #print(symbol,thisdf)
    # print(len(lastETFdf))

    lastETFdf.to_csv(f"ETF清单信息成交额过滤后{start_time}.csv")

lastETFdf=lastETFdf[(lastETFdf["15日平均成交额"]*1000)>(1000*(10**4))]#至少大于1000w{600多个}（实际上应该大于5000w{394个}）
lastETFdf=lastETFdf[lastETFdf["前一交易日申赎基准单位净值"]<(lastETFdf["15日平均成交额"]*1000*0.01)]#单份申赎金额小于平均成交额的百分之一
print("处理后",len(lastETFdf))#剩下300多个ETF符合要求
holdETFlist=lastETFdf["ETF交易代码"].tolist()
etfinfodf=etfinfodf[etfinfodf["ETF交易代码"].isin(holdETFlist)]
etfstocksdf=etfstocksdf[etfstocksdf["ETF交易代码"].isin(holdETFlist)]
print("处理后",len(etfinfodf))



while True:
    time.sleep(5)#得等几秒任务启动之后才能获取其中的数据
    
    iopvdf=pd.DataFrame(spi.iopv)#spi里面的数据可以传输出来【SecurityID是股票代码】
    iopvdf.to_csv('iopvdf.csv')
    # nowdf=iopvdf.copy().groupby('SecurityID').apply(lambda x:x[-1:])#每一组只保留最后一行【下面另外两种方式也可以】
    # nowdf=iopvdf.copy().groupby('SecurityID').last().reset_index()
    # nowdf=iopvdf.copy().drop_duplicates(subset='SecurityID',keep='last')#怼到10000条之后数据就出来的快了
    # print(nowdf)
    # nowdf.to_csv('iopvdf处理后.csv')#前面验证过这里就不需要处理了

    stocksdf=pd.DataFrame(spi.stocks)#spi里面的数据可以传输出来【SecurityID是股票代码】
    stocksdf.to_csv('stocksdf.csv')

    #【】【策略执行细节说明】【】
    # ETF套利策略会受基金公司限额问题，所以有时间不能全额实现策略，需要提前跟基金公司沟通好。
    # 有一些规模大的ETF是T+2交易的需要融券还券，都是那些保险、证券公司自营盘在套。
    # 一般来讲不做外盘ETF套利（外盘需要纯现金申赎），一个是汇率损失（申购赎回各有固定2%的汇率损失）一个是额度问题（高利润的标的开盘秒清散户基本抢不到），无法完全实现T+0，风险敞口极大。

    # #【ETF申赎详情】
    # 0预估现金差额：在ETF套利中，"预估现金差额"是一个重要的概念，它指的是在ETF申购赎回过程中，由于一篮子股票的市值与ETF净值之间的差异，需要用现金来补足的部分。这个差额可能为正、为负或为零，具体取决于ETF净值与一篮子股票市值的比较。
    etfinfodf=etfinfodf[(etfinfodf["前一交易日申赎基准单位净值"]<(100*(10**4)))]#只要单笔下单金额小于100w的标的
    etfinfodf=etfinfodf[(etfinfodf["最大现金替代比例"]<1)&(etfinfodf["最大现金替代比例"]>0)]#只要最大现金替代比例在（0，1）之间的标的
    # etfinfodf=etfinfodf[(etfinfodf["ETF申赎类型"]==0)]#0普通申赎，1实物申赎（0应该是不强制申赎类型了就，1可能是强制实物申赎{暂时没遇到}）
    # #【ETF成分券详情】
    # print(len(etfstocksdf["ETF交易代码"].unique().tolist()))#996
    #【eq("7").any()|x.eq('a').any()，因为输出成csv再读出来是字符串7了】
    etfstocksdf['是否特殊ETF'] = etfstocksdf.groupby('ETF交易代码')['挂牌市场'].transform(lambda x: 
                                                                              x.eq("7").any()
                                                                            #   |
                                                                            #   x.eq('a').any()#x.eq('a').any()#暂时不单独去北交所标的
                                                                              )
    etfstocksdf=etfstocksdf[etfstocksdf["是否特殊ETF"]!=True]
    print(len(etfstocksdf["ETF交易代码"].unique().tolist()))#单独去a的北交所剩下953（去掉了50多个），单独去7的外盘剩下808（去掉了188左右）
    # 0现金替代标志：目前没碰到有禁止现金替代的标的，大部分都是1选项，3、4选项大部分是外盘或者可能是支持港股通（深股通、沪股通）的部分
    # TORA_TSTP_ETFCTSTAT_Forbidden(0):禁止现金替代
    # TORA_TSTP_ETFCTSTAT_Allow(1):可以现金替代
    # TORA_TSTP_ETFCTSTAT_Force(2):必须现金替代
    # TORA_TSTP_ETFCTSTAT_CBAllow(3):跨市退补现金替代
    # TORA_TSTP_ETFCTSTAT_CBForce(4):跨市必须现金替代
    # 1挂牌市场：挂牌市场不是1上交所A股、2深交所的部分A股，如7是境外市场，a是北交所主板【只保留不含北交所的】
    # etfstocksdf[etfstocksdf["现金替代标志"]==0]#不能现金替代的需要单独处理【但是没找到这个】

    stocksdf["ETF成份证券代码"]=stocksdf["SecurityID"]
    etfstocksdf=etfstocksdf.merge(stocksdf,on="ETF成份证券代码",how="left")#左连接意味着结果DataFrame将包含etfstocksdf中的所有行，如果stocksdf中有匹配的行，则会添加相应的列；如果没有匹配的行，则对应的列会用NaN（即“非数字”值）填充。
    etfstocksdf["申购金额"]=etfstocksdf["AskPrice1"]*etfstocksdf["成分证券数量"]
    etfstocksdf["赎回金额"]=etfstocksdf["BidPrice1"]*etfstocksdf["成分证券数量"]

    # etfstocksdf["ETF成份证券代码"]#根据成分券代码拼接买一卖一，计算申赎金额
    
    time.sleep(1000)

    # 【后续任务】如果无法计算三档深度，可以对手盘+滑点的模式计算冲击成本
    # 0.【【券商推送的iopv的延迟好像是3秒一次，理论上应该自己算更快一些】】有人实盘半自动{手动点}试过大概十几秒能完成一次套利
    # 1.根据订阅的股票价格和ETF价格，通过成分股换算IOPV价格，计算实际折价率【bidiopv和askiopv】
    # 2.ETF成分股涨停板处理和必选股处理【部分标的不允许现金替代】
    # 3.全市场限购额度、单账户最大申赎金额吗【这俩函数是用来解决ETF限额问题的，在外盘尤其要注意，内盘也经常会遇到】



# 72.查询ETF清单信息响应(RspQryETFFile)：
# 域字段	描述	类型	取值
# TradingDay	交易日	char(8)	
# ExchangeID	交易所代码	char(1)	
# TORA_TSTP_EXD_COMM(0):通用(内部使用)
# TORA_TSTP_EXD_SSE(1):上海交易所
# TORA_TSTP_EXD_SZSE(2):深圳交易所
# TORA_TSTP_EXD_HK(3):香港交易所
# TORA_TSTP_EXD_BSE(4):北京证券交易所
# ETFSecurityID	ETF交易代码	char(30)	
# ETFCreRedSecurityID	ETF申赎代码	char(30)	
# CreationRedemptionUnit	最小申购赎回单位份数	int	
# Maxcashratio	最大现金替代比例	double	
# EstimateCashComponent	预估现金差额	double	
# CashComponent	前一交易日现金差额	double	
# NAV	前一交易日基金单位净值	double	
# NAVperCU	前一交易日申赎基准单位净值	double	
# DividendPerCU	当日申购赎回基准单位的红利金额	double	
# ETFCreRedType	ETF申赎类型	char(1)	
# TORA_TSTP_CRT_IS(0):普通申赎
# TORA_TSTP_CRT_OS(1):实物申赎
# ETFSecurityName	ETF证券名称	char(80)	


# 73.查询ETF成份证券信息响应(RspQryETFBasket)：
# 域字段	描述	类型	取值
# TradingDay	交易日	char(8)	
# ExchangeID	交易所代码	char(1)	
# TORA_TSTP_EXD_COMM(0):通用(内部使用)
# TORA_TSTP_EXD_SSE(1):上海交易所
# TORA_TSTP_EXD_SZSE(2):深圳交易所
# TORA_TSTP_EXD_HK(3):香港交易所
# TORA_TSTP_EXD_BSE(4):北京证券交易所
# ETFSecurityID	ETF交易代码	char(30)	
# SecurityID	ETF成份证券代码	char(30)	
# SecurityName	成分证券名称	char(80)	
# Volume	成分证券数量	int	
# ETFCurrenceReplaceStatus	现金替代标志	char(1)	
# TORA_TSTP_ETFCTSTAT_Forbidden(0):禁止现金替代
# TORA_TSTP_ETFCTSTAT_Allow(1):可以现金替代
# TORA_TSTP_ETFCTSTAT_Force(2):必须现金替代
# TORA_TSTP_ETFCTSTAT_CBAllow(3):跨市退补现金替代
# TORA_TSTP_ETFCTSTAT_CBForce(4):跨市必须现金替代
# Premium	溢价比例	double	
# CreationReplaceAmount	申购替代金额	double	
# RedemptionReplaceAmount	赎回替代金额	double	
# MarketID	挂牌市场	char(1)	
# TORA_TSTP_MKD_COMMON(0):通用(内部使用)
# TORA_TSTP_MKD_SHA(1):上海A股
# TORA_TSTP_MKD_SZA(2):深圳A股
# TORA_TSTP_MKD_SHB(3):上海B股
# TORA_TSTP_MKD_SZB(4):深圳B股
# TORA_TSTP_MKD_SZThreeA(5):深圳三版A股
# TORA_TSTP_MKD_SZThreeB(6):深圳三版B股
# TORA_TSTP_MKD_Foreign(7):境外市场
# TORA_TSTP_MKD_SZHK(8):深圳港股通市场
# TORA_TSTP_MKD_SHHK(9):上海港股通市场
# TORA_TSTP_MKD_BJMain(a):北京主板
# ETFCreRedType	ETF申赎类型	char(1)	
# TORA_TSTP_CRT_IS(0):普通申赎
# TORA_TSTP_CRT_OS(1):实物申赎



# thistraderapi.Join()# 加入任务
# input()# 等待程序结束[不确定几分钟结束]一直没结束
thisxmdapi.Release()# 释放接口对象

