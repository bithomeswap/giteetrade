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
TD_TCP_FrontAddress="tcp://210.14.72.21:4400" #仿真交易环境
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

# 启动接口
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
            for index in etfinfodf["ETF交易代码"].tolist():
                symbol=str(index).zfill(6)
                print(symbol,type(symbol))
                if str(symbol).startswith("5"):#上交所
                    sub_arr=[str(symbol).encode()]#
                    ret=self.__api.SubscribeMarketData(sub_arr,xmdapi.TORA_TSTP_EXD_SSE)#TORA_TSTP_EXD_SSE上交所
                elif str(symbol).startswith("1"):#深交所
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
            if len(self.iopv)<=5000:#ETF的IOPV数据少于5000条时直接添加
                self.iopv.append(thisiopv)
            else:
                self.iopv=self.iopv[1:]#去掉第一行
                self.iopv.append(thisiopv)
            # print(self.iopv)
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
XMD_TCP_FrontAddress="tcp://210.14.72.21:4402"#行情服务器接口
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
# 启动接口
thisxmdapi.Init()
while True:
    time.sleep(10)
    iopvdf=pd.DataFrame(spi.iopv)#spi里面的数据可以传输出来
    print(iopvdf)
    iopvdf.to_csv('iopvdf.csv')



# 计算每一个标的的成分股组合之后的价格和实际价格的换算关系，还有涨停板处理和必选股
        #             etffile=True
        # #【验证ETF成分券信息】
        # etfstocksdf=pd.read_csv(f"ETF成份证券信息{start_time}.csv")
        # etfstocksdf=etfstocksdf.iloc[:, 1:]#这样一样可以去掉第一行避免空数据干扰
        # # etfstocksdf=etfstocksdf.drop('Unnamed: 0',axis=1)#去掉空白行【:不能错，不能多空格】
        # if len(etfstocksdf)>100000:#平时110000
        #     print(etfstocksdf.columns.tolist(),type(etfstocksdf.columns.tolist()))
        #     if etfstocksdf.columns.tolist()==['交易日','交易所代码','ETF交易代码','ETF成份证券代码',
        #                     '成分证券名称','成分证券数量','现金替代标志','溢价比例',
        #                     '申购替代金额','赎回替代金额','挂牌市场','ETF申赎类型']:
        #         etfbasket=True






# thistraderapi.Join()# 加入任务
# input()# 等待程序结束[不确定几分钟结束]一直没结束
thisxmdapi.Release()# 释放接口对象

