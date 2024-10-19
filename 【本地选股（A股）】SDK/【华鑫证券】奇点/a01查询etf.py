import time
from traderapi import traderapi#从文件夹当中引入【from 文件夹 引入 文件】
import pandas as pd

from config import *

class TraderSpi(traderapi.CTORATstpTraderSpi):
    def __init__(self,api):
        traderapi.CTORATstpTraderSpi.__init__(self)
        self.__api:traderapi.CTORATstpTraderApi=api
        self.__req_id=0
        self.__front_id=0
        self.__session_id=0
        self.ETFFile=[]#ETFFile初始化为空列表【类当中内创建的变量，在该类的方法当中调用时需要加上self.作为前缀】int是特殊的方法，在非方法中使用时不需要self.作为前缀
        self.ETFBasket=[]#ETFBasket初始化为空列表【类当中内创建的变量，在该类的方法当中调用时需要加上self.作为前缀】int是特殊的方法，在非方法中使用时不需要self.作为前缀
        self.running = 1
        self.etffile=False
        self.etfbasket=False

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
            item = {
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
            }
            item['ETF交易代码']=str(item['ETF交易代码']).zfill(6)
            item['ETF申赎代码']=str(item['ETF申赎代码']).zfill(6)
            # 这里的前一交易日基金单位净值是四舍五入之后的数据，
            # 应该以前一交易日申赎基准单位净值为准计算单笔最小下单金额和单位净值。
            item["前一交易日基金单位净值"]=item["前一交易日申赎基准单位净值"]/item["最小申购赎回单位份数"]
            self.ETFFile.append(item)

        if bIsLast:#这里是查询结束了进行输出
            #【验证ETF清单信息】
            if len(self.ETFFile)>900:#平时900
                print("ETF清单信息输出开始")
                etfinfodf = pd.DataFrame(self.ETFFile)
                etfinfodf.to_csv(f"ETF清单信息{start_time}.csv")
                print("ETF清单信息输出完毕")
                self.etffile = True
            # self.ETFFile=[]
            # time.sleep(self.interval)
            # self.QryETFFileField()#这个是循环执行任务


    def OnRspQryETFBasket(self,pETFBasketField:traderapi.CTORATstpETFBasketField,pRspInfoField:traderapi.CTORATstpRspInfoField,nRequestID:int,bIsLast:bool) -> "void":
        if pETFBasketField:#如果有数据则继续执行【如果不验证则会因为报错中断全部任务】
            item = {
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
            }
            item['ETF交易代码']=str(item['ETF交易代码']).zfill(6)
            item['ETF成份证券代码']=str(item['ETF成份证券代码']).zfill(6)
            self.ETFBasket.append(item)


        if bIsLast:#这里是查询结束了进行输出
            #【验证ETF成分券信息】
            if len(self.ETFBasket)>100000:#平时110000
                etfstocksdf=pd.DataFrame(self.ETFBasket)
                print("ETF成份证券信息输出开始")
                etfstocksdf.to_csv(f"ETF成份证券信息{start_time}.csv")
                print("ETF成份证券信息输出完毕")
                self.etfbasket = True
            # self.ETFBasket=[]
            # time.sleep(self.interval)
            # self.QryETFBasketField()#这个是循环执行任务


    def Wait(self,):
        while self.running:
            time.sleep(1)
            # 两个数据都获取完成则退出
            if self.etffile and self.etfbasket:
                break
        print("数据已经获取成功任务结束")


# 【交易SDK】
# 打印接口版本号
print("thistraderapi Version:::"+traderapi.CTORATstpTraderApi_GetApiVersion())
# 创建接口对象
# pszFlowPath为私有流和公有流文件存储路径，若订阅私有流和公有流且创建多个接口实例，每个接口实例应配置不同的路径
# bEncrypt为网络数据是否加密传输，考虑数据安全性，建议以互联网方式接入的终端设置为加密传输
thistraderapi:traderapi.CTORATstpTraderApi=traderapi.CTORATstpTraderApi.CreateTstpTraderApi('./flow',False)
# 创建回调对象
tradespi=TraderSpi(thistraderapi)
# 注册回调接口
thistraderapi.RegisterSpi(tradespi)
# 注册单个交易前置服务地址
TD_TCP_FrontAddress=tradeurl
# 注册多个交易前置服务地址，用逗号隔开 形如:thistraderapi.RegisterFront("tcp://10.0.1.101:6500,tcp://10.0.1.101:26500")
thistraderapi.RegisterFront(TD_TCP_FrontAddress)
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

thistraderapi.Init()# 启动接口
tradespi.Wait()# 等待任务执行完成
thistraderapi.Release()# 释放接口对象
