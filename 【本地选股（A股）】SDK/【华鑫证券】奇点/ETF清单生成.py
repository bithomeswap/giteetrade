#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from pathlib import Path
import datetime
from traderapi import traderapi#从文件夹当中引入【from 文件夹 引入 文件】
from xmdapi import xmdapi#从文件夹当中引入【from 文件夹 引入 文件】
''' 注意: 如果提示找不到_tradeapi 且与已发布的库文件不一致时,可自行重命名为_tradeapi.so (windows下为_tradeapi.pyd)'''

import pandas as pd

#投资者账户 
InvestorID = "00030557";   
'''
该默认账号为共用连通测试使用,自有测试账号请到n-sight.com.cn注册并从个人中心获取交易编码,不是网站登录密码,不是手机号
实盘交易时，取客户号，请注意不是资金账号或咨询技术支持
'''
#操作员账户
UserID = "00030557";	   #同客户号保持一致即可
#资金账户 
AccountID = "00030557";		#以Req(TradingAccount)查询的为准
#登陆密码
Password = "17522830";		#N视界注册模拟账号的交易密码，不是登录密码
DepartmentID = "0001";		#生产环境默认客户号的前4位
SSE_ShareHolderID='A00030557'   #不同账号的股东代码需要接口ReqQryShareholderAccount去查询
SZ_ShareHolderID='700030557'    #不同账号的股东代码需要接口ReqQryShareholderAccount去查询

class TraderSpi(traderapi.CTORATstpTraderSpi):
    def __init__(self, api):
        traderapi.CTORATstpTraderSpi.__init__(self)
        self.__api:traderapi.CTORATstpTraderApi = api
        self.__req_id = 0
        self.__front_id = 0
        self.__session_id = 0

    def OnFrontConnected(self) -> "void":
        print('OnFrontConnected')

        # 获取终端信息
        self.__req_id += 1
        ret = self.__api.ReqGetConnectionInfo(self.__req_id)
        if ret != 0:
            print('ReqGetConnectionInfo fail, ret[%d]' % ret)

    def OnFrontDisconnected(self, nReason: "int") -> "void":
        print('OnFrontDisconnected: [%d]' % nReason)

    def OnRspGetConnectionInfo(self, pConnectionInfoField: "CTORATstpConnectionInfoField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int") -> "void":
        if pRspInfoField.ErrorID == 0:
            print('inner_ip_address[%s]' % pConnectionInfoField.InnerIPAddress)
            print('inner_port[%d]' % pConnectionInfoField.InnerPort)
            print('outer_ip_address[%s]' % pConnectionInfoField.OuterIPAddress)
            print('outer_port[%d]' % pConnectionInfoField.OuterPort)
            print('mac_address[%s]' % pConnectionInfoField.MacAddress)

            #请求登录
            login_req = traderapi.CTORATstpReqUserLoginField()

            # 支持以用户代码、资金账号和股东账号方式登录
		    # （1）以用户代码方式登录
            login_req.LogInAccount = UserID
            login_req.LogInAccountType = traderapi.TORA_TSTP_LACT_UserID
		    # （2）以资金账号方式登录
            #login_req.DepartmentID = DepartmentID
            #login_req.LogInAccount = AccountID
            #login_req.LogInAccountType = traderapi.TORA_TSTP_LACT_AccountID
		    # （3）以上海股东账号方式登录
            #login_req.LogInAccount = SSE_ShareHolderID
            #login_req.LogInAccountType = traderapi.TORA_TSTP_LACT_SHAStock
		    # （4）以深圳股东账号方式登录
            #login_req.LogInAccount = SZSE_ShareHolderID
            #login_req.LogInAccountType = traderapi.TORA_TSTP_LACT_SZAStock

		    # 支持以密码和指纹(移动设备)方式认证
		    # （1）密码认证
		    # 密码认证时AuthMode可不填
            #login_req.AuthMode = traderapi.TORA_TSTP_AM_Password
            login_req.Password = Password
		    # （2）指纹认证
		    # 非密码认证时AuthMode必填
            #login_req.AuthMode = traderapi.TORA_TSTP_AM_FingerPrint
            #login_req.DeviceID = '03873902'
            #login_req.CertSerial = '9FAC09383D3920CAEFF039'
		
		    # 终端信息采集
		    # UserProductInfo填写终端名称
            login_req.UserProductInfo = 'pyapidemo'
		    # 按照监管要求填写终端信息
            login_req.TerminalInfo = 'PC;IIP=000.000.000.000;IPORT=00000;LIP=x.xx.xxx.xxx;MAC=123ABC456DEF;HD=XXXXXXXXXX'
		    # 以下内外网IP地址若不填则柜台系统自动采集，若填写则以终端填值为准报送
            #login_req.MacAddress = '5C-87-9C-96-F3-E3'
            #login_req.InnerIPAddress = '10.0.1.102'
            #login_req.OuterIPAddress = '58.246.43.50'

            self.__req_id += 1
            ret = self.__api.ReqUserLogin(login_req, self.__req_id)
            if ret != 0:
                print('ReqUserLogin fail, ret[%d]' % ret)
        else:
            print('GetConnectionInfo fail, [%d] [%d] [%s]!!!' % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))

    ETFFile = []
    ETFBasket = []
    start_time = datetime.datetime.now().strftime("%Y%m%d")#特殊的时间格式
    interval = 5#控制请求频率

    def QueryEtf(self,):#这里取出来的数据跟同花顺实盘的数据不完全一致
        self.QryETFFileField()
        self.QryETFBasketField()

    def QryETFFileField(self,):
        # 查询ETF清单信息
        req_field = traderapi.CTORATstpQryETFFileField()
        # 以下字段不填表示不设过滤条件，即查询所有etf
        # req_field.ExchangeID = traderapi.TORA_TSTP_EXD_SSE
        print("查询 QryETFFileField")
        self.__req_id += 1
        ret = self.__api.ReqQryETFFile(req_field, self.__req_id)
        if ret != 0:
            print('ReqQryETFFile fail, ret[%d]' % ret)

    def QryETFBasketField(self,):
        # 查询ETF成份证券信息
        print("查询 QryETFBasketField")
        req_field = traderapi.CTORATstpQryETFBasketField()
        # 以下字段不填表示不设过滤条件，即查询所有etf
        # req_field.ExchangeID = traderapi.TORA_TSTP_EXD_SSE
        self.__req_id += 1
        ret = self.__api.ReqQryETFBasket(req_field, self.__req_id)
        if ret != 0:
            print('ReqQryETFFile fail, ret[%d]' % ret)

    def OnRspQryETFFile(self, pETFFileField: traderapi.CTORATstpETFFileField, pRspInfoField: traderapi.CTORATstpRspInfoField, nRequestID: int, bIsLast: bool) -> "void":
        if pETFFileField:#如果有数据则继续执行【如果不验证则会因为报错中断全部任务】
            self.ETFFile.append(pETFFileField.dict())
        if bIsLast:#这里是查询结束了进行输出
            self.write_to_csv(self.ETFFile,f"ETFFile{self.start_time}.csv")
            # self.ETFFile = []
            # time.sleep(self.interval)
            # self.QryETFFileField()#这个是循环执行任务
            api.Release()

    def OnRspQryETFBasket(self, pETFBasketField: traderapi.CTORATstpETFBasketField, pRspInfoField: traderapi.CTORATstpRspInfoField, nRequestID: int, bIsLast: bool) -> "void":
        if pETFBasketField:#如果有数据则继续执行【如果不验证则会因为报错中断全部任务】
            self.ETFBasket.append(pETFBasketField.dict())
        if bIsLast:#这里是查询结束了进行输出
            self.write_to_csv(self.ETFBasket,f"ETFBasket{self.start_time}.csv")
            # self.ETFBasket = []
            # time.sleep(self.interval)
            # self.QryETFBasketField()#这个是循环执行任务
            api.Release()

    def write_to_csv(self,data,path):
        print(f'[write_to_csv] {path}')
        df = pd.DataFrame(data)
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path.as_posix())

    def OnRspUserLogin(self, pRspUserLoginField: "traderapi.CTORATstpRspUserLoginField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int") -> "void":
        if pRspInfoField.ErrorID == 0:
            print('Login success! [%d]' % nRequestID)

            self.__front_id = pRspUserLoginField.FrontID
            self.__session_id = pRspUserLoginField.SessionID

            self.QueryEtf()

            # if 0:
            #     # 修改密码
            #     req_field = traderapi.CTORATstpUserPasswordUpdateField()
            #     req_field.UserID = UserID
            #     req_field.OldPassword = Password
            #     req_field.NewPassword = '123456'

            #     self.__req_id += 1
            #     ret = self.__api.ReqUserPasswordUpdate(req_field, self.__req_id)
            #     if ret != 0:
            #         print('ReqUserPasswordUpdate fail, ret[%d]' % ret)
            #     return


            # if 0:
            #     # 查询合约
            #     req_field = traderapi.CTORATstpQrySecurityField()
                
            #     #以下字段不填表示不设过滤条件，即查询全部合约
            #     #req_field.ExchangeID = traderapi.TORA_TSTP_EXD_SSE
            #     #req_field.SecurityID = '600000'

            #     self.__req_id += 1
            #     ret = self.__api.ReqQrySecurity(req_field, self.__req_id)
            #     if ret != 0:
            #         print('ReqQrySecurity fail, ret[%d]' % ret)

            # if 0:
            #     # 查询投资者
            #     req_field = traderapi.CTORATstpQryInvestorField()

            #     # 以下字段不填表示不设过滤条件
            #     #req_field.InvestorID = InvestorID

            #     self.__req_id += 1
            #     ret = self.__api.ReqQryInvestor(req_field, self.__req_id)
            #     if ret != 0:
            #         print('ReqQryInvestor fail, ret[%d]' % ret)

            # if 0:
            #     # 查询股东账号
            #     req_field = traderapi.CTORATstpQryShareholderAccountField()

            #     # 以下字段不填表示不设过滤条件，即查询所有股东账号
            #     #req_field.ExchangeID = traderapi.TORA_TSTP_EXD_SSE

            #     self.__req_id += 1
            #     ret = self.__api.ReqQryShareholderAccount(req_field, self.__req_id)
            #     if ret != 0:
            #         print('ReqQryShareholderAccount fail, ret[%d]' % ret)

            # if 0:
            #     # 查询资金账号
            #     req_field = traderapi.CTORATstpQryTradingAccountField()

            #     # 以下字段不填表示不设过滤条件，即查询所有资金账号
            #     req_field.InvestorID = InvestorID
            #     req_field.DepartmentID = DepartmentID
            #     req_field.AccountID = AccountID

            #     self.__req_id += 1
            #     ret = self.__api.ReqQryTradingAccount(req_field, self.__req_id)
            #     if ret != 0:
            #         print('ReqQryTradingAccount fail, ret[%d]' % ret)


            # if 0:
            #     # 查询报单
            #     req_field = traderapi.CTORATstpQryOrderField()

            #     # 以下字段不填表示不设过滤条件，即查询所有报单
            #     #req_field.SecurityID = '600000'
            #     #req_field.InsertTimeStart = '09:35:00'
            #     #req_field.InsertTimeEnd = '10:00:00'

            #     # IsCancel字段填1表示只查询可撤报单
            #     #req_field.IsCancel = 1

            #     self.__req_id += 1
            #     ret = self.__api.ReqQryOrder(req_field, self.__req_id)
            #     if ret != 0:
            #         print('ReqQryOrder fail, ret[%d]' % ret)


            # if 0:
            #     # 查询持仓
            #     req_field = traderapi.CTORATstpQryPositionField()

            #     # 以下字段不填表示不设过滤条件，即查询所有持仓
            #     #req_field.SecurityID = '600000'

            #     self.__req_id += 1
            #     ret = self.__api.ReqQryPosition(req_field, self.__req_id)
            #     if ret != 0:
            #         print('ReqQryPosition fail, ret[%d]' % ret)


            # if 0:
            #     # 请求报单
            #     req_field = traderapi.CTORATstpInputOrderField()

            #     req_field.ExchangeID = traderapi.TORA_TSTP_EXD_SSE
            #     req_field.ShareholderID = SSE_ShareHolderID
            #     req_field.SecurityID = '600000'
            #     req_field.Direction = traderapi.TORA_TSTP_D_Buy
            #     req_field.VolumeTotalOriginal = 100

            #     '''
            #     上交所支持限价指令和最优五档剩撤、最优五档剩转限两种市价指令，对于科创板额外支持本方最优和对手方最优两种市价指令和盘后固定价格申报指令
            #     深交所支持限价指令和立即成交剩余撤销、全额成交或撤销、本方最优、对手方最优和最优五档剩撤五种市价指令
            #     限价指令和上交所科创板盘后固定价格申报指令需填写报单价格，其它市价指令无需填写报单价格
            #     以下以上交所限价指令为例，其它指令参考开发指南相关说明填写OrderPriceType、TimeCondition和VolumeCondition三个字段:
            #     '''
            #     req_field.LimitPrice = 7.29
            #     req_field.OrderPriceType = traderapi.TORA_TSTP_OPT_LimitPrice
            #     req_field.TimeCondition = traderapi.TORA_TSTP_TC_GFD
            #     req_field.VolumeCondition = traderapi.TORA_TSTP_VC_AV


            #     '''
            #     OrderRef为报单引用，类型为整型，该字段报单时为选填
            #     若不填写，则系统会为每笔报单自动分配一个报单引用
            #     若填写，则需保证同一个TCP会话下报单引用严格单调递增，不要求连续递增，至少需从1开始编号
            #     '''
            #     #req_field.OrderRef = 1

            #     '''
            #     InvestorID为选填，若填写则需保证填写正确
            #     Operway为委托方式，根据券商要求填写，无特殊说明置空即可
            #     终端自定义字段，终端可根据需要填写如下字段的值，该字段值不会被柜台系统修改，在报单回报和查询报单时返回给终端
            #     '''
            #     #req_field.SInfo = 'sinfo'
            #     #req_field.IInfo = 123

            #     '''
            #     其它字段置空
            #     '''

            #     self.__req_id += 1
            #     ret = self.__api.ReqOrderInsert(req_field, self.__req_id)
            #     if ret != 0:
            #         print('ReqOrderInsert fail, ret[%d]' % ret)

            
            # if 0:
            #     # 请求撤单
            #     req_field = traderapi.CTORATstpInputOrderActionField()

            #     req_field.ExchangeID = traderapi.TORA_TSTP_EXD_SSE
            #     req_field.ActionFlag = traderapi.TORA_TSTP_AF_Delete

    
            #     # 撤单支持以下两种方式定位原始报单：
            #     # （1）报单引用方式
            #     #req_field.FrontID = self.__front_id
            #     #req_field.SessionID = self.__session_id
            #     #req_field.OrderRef = 1
            #     # （2）系统报单编号方式
            #     req_field.OrderSysID = '110019400000005'


            #     # OrderActionRef报单操作引用，用法同报单引用，可根据需要选填

            #     '''
            #     终端自定义字段，终端可根据需要填写如下字段的值，该字段值不会被柜台系统修改，在查询撤单时返回给终端
            #     '''
            #     #req_field.SInfo = 'sinfo'
            #     #req_field.IInfo = 123

            #     '''
            #     委托方式字段根据券商要求填写，无特殊说明置空即可
            #     其它字段置空
            #     '''

            #     self.__req_id += 1
            #     ret = self.__api.ReqOrderAction(req_field, self.__req_id)
            #     if ret != 0:
            #         print('ReqOrderAction fail, ret[%d]' % ret)


            # if 0:
            #     # 查询集中交易资金
            #     req_field = traderapi.CTORATstpReqInquiryJZFundField()

            #     req_field.DepartmentID = DepartmentID
            #     req_field.AccountID = AccountID
            #     req_field.CurrencyID = traderapi.TORA_TSTP_CID_CNY

            #     self.__req_id += 1
            #     ret = self.__api.ReqInquiryJZFund(req_field, self.__req_id)
            #     if ret != 0:
            #         print('ReqInquiryJZFund fail, ret[%d]' % ret)


            # if 0:
            #     # 资金转移(包括资金调拨和银证转账)
            #     req_field = traderapi.CTORATstpInputTransferFundField()

            #     req_field.DepartmentID = DepartmentID
            #     req_field.AccountID = AccountID
            #     req_field.CurrencyID = traderapi.TORA_TSTP_CID_CNY
            #     req_field.Amount = 100000.0

            #     '''
            #     转移方向：
            #     TORA_TSTP_TRNSD_MoveIn表示资金从集中交易柜台调拨至快速交易柜台
            #     TORA_TSTP_TRNSD_MoveOut表示资金从快速交易柜台调拨至集中交易柜台
            #     TORA_TSTP_TRNSD_StockToBank表示证券快速交易系统资金转入银行，即出金
            #     TORA_TSTP_TRNSD_BankToStock表示银行资金转入证券快速交易系统，即入金
            #     以下说明各场景下字段填值：
            #     '''
            #     # （1）资金从集中交易柜台调拨至快速交易柜台
            #     req_field.TransferDirection = traderapi.TORA_TSTP_TRNSD_MoveIn
            #     # （2）资金从快速交易柜台调拨至集中交易柜台
            #     #req_field.TransferDirection = traderapi.TORA_TSTP_TRNSD_MoveOut
            #     # （3）证券快速交易系统资金转入银行，需填写银行代码和资金密码
            #     #req_field.TransferDirection = traderapi.TORA_TSTP_TRNSD_StockToBank
            #     #req_field.BankID = traderapi.TORA_TSTP_BKID_CCB
            #     #req_field.AccountPassword = '123456'
            #     # （4）银行资金转入证券快速交易系统，需填写银行代码和银行卡密码
            #     #req_field.TransferDirection = traderapi.TORA_TSTP_TRNSD_BankToStock
            #     #req_field.BankID = traderapi.TORA_TSTP_BKID_CCB
            #     #req_field.BankPassword = '123456'

            #     '''
            #     申请流水号ApplySerial字段为选填字段
            #     若不填写则柜台系统会自动生成一个申请流水号
            #     若填写则需保证同一个TCP会话下申请流水号不重复
            #     '''
            #     #req_field.ApplySerial = 1

            #     self.__req_id += 1
            #     ret = self.__api.ReqTransferFund(req_field, self.__req_id)
            #     if ret != 0:
            #         print('ReqTransferFund fail, ret[%d]', ret)

            # if 0:
            #     '''登出,目前登出成功连接会立即被柜台系统断开，终端不会收到OnRspUserLogout应答
            #     连接断开后接口内部会触发重新连接，为不使连接成功后又触发重新登录，需终端做好逻辑控制
            #     一般情况下若希望登出，直接调用Release接口即可，释放成功连接将被终端强制关闭，Release接口调用注意事项见下文说明
            #     '''
            #     req_field = traderapi.CTORATstpUserLogoutField()

            #     self.__req_id += 1
            #     ret = self.__api.ReqUserLogout(req_field, self.__req_id)
            #     if ret != 0:
            #         print('ReqUserLogout fail, ret[%d]' % ret)
        else:
            print('Login fail!!! [%d] [%d] [%s]'
                % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))
        return

    # def OnRspUserPasswordUpdate(self, pUserPasswordUpdateField: "CTORATstpUserPasswordUpdateField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int") -> "void":
    #     if pRspInfoField.ErrorID == 0:
    #         print('OnRspUserPasswordUpdate: OK! [%d]' % nRequestID)
    #     else:
    #         print('OnRspUserPasswordUpdate: Error! [%d] [%d] [%s]' 
    #             % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))


    # def OnRspOrderInsert(self, pInputOrderField: "CTORATstpInputOrderField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int") -> "void":
    #     if pRspInfoField.ErrorID == 0:
    #         print('OnRspOrderInsert: OK! [%d]' % nRequestID)
    #     else:
    #         print('OnRspOrderInsert: Error! [%d] [%d] [%s]'
    #             % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))


    # def OnRspOrderAction(self, pInputOrderActionField: "CTORATstpInputOrderActionField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int") -> "void":
    #     if pRspInfoField.ErrorID == 0:
    #         print('OnRspOrderAction: OK! [%d]' % nRequestID)
    #     else:
    #         print('OnRspOrderAction: Error! [%d] [%d] [%s]'
    #             % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))


    # def OnRspInquiryJZFund(self, pRspInquiryJZFundField: "CTORATstpRspInquiryJZFundField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int") -> "void":
    #     if pRspInfoField.ErrorID == 0:
    #         print('OnRspInquiryJZFund: OK! [%d] [%.2f] [%.2f]'
    #             % (nRequestID, pRspInquiryJZFundField.UsefulMoney, pRspInquiryJZFundField.FetchLimit))
    #     else:
    #         print('OnRspInquiryJZFund: Error! [%d] [%d] [%s]'
    #             % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))


    # def OnRspTransferFund(self, pInputTransferFundField: "CTORATstpInputTransferFundField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int") -> "void":
    #     if pRspInfoField.ErrorID == 0:
    #         print('OnRspTransferFund: OK! [%d]' % nRequestID)
    #     else:
    #         print('OnRspTransferFund: Error! [%d] [%d] [%s]'
    #             % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))


    # def OnRtnOrder(self, pOrderField: "CTORATstpOrderField") -> "void":
    #     print('OnRtnOrder: InvestorID[%s] SecurityID[%s] OrderRef[%d] OrderLocalID[%s] LimitPrice[%.2f] VolumeTotalOriginal[%d] OrderSysID[%s] OrderStatus[%s]'
    #         % (pOrderField.InvestorID, pOrderField.SecurityID, pOrderField.OrderRef, pOrderField.OrderLocalID, 
    #         pOrderField.LimitPrice, pOrderField.VolumeTotalOriginal, pOrderField.OrderSysID, pOrderField.OrderStatus))


    # def OnRtnTrade(self, pTradeField: "CTORATstpTradeField") -> "void":
    #     print('OnRtnTrade: TradeID[%s] InvestorID[%s] SecurityID[%s] OrderRef[%d] OrderLocalID[%s] Price[%.2f] Volume[%d]'
    #         % (pTradeField.TradeID, pTradeField.InvestorID, pTradeField.SecurityID,
    #         pTradeField.OrderRef, pTradeField.OrderLocalID, pTradeField.Price, pTradeField.Volume))


    # def OnRtnMarketStatus(self, pMarketStatusField: "CTORATstpMarketStatusField") -> "void":
    #     print('OnRtnMarketStatus: MarketID[%s] MarketStatus[%s]'
    #         % (pMarketStatusField.MarketID, pMarketStatusField.MarketStatus))


    # def OnRspQrySecurity(self, pSecurityField: "CTORATstpSecurityField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int", bIsLast: "bool") -> "void":
    #     if bIsLast != 1:
    #         print('OnRspQrySecurity[%d]: SecurityID[%s] SecurityName[%s] MarketID[%s] OrderUnit[%s] OpenDate[%s] UpperLimitPrice[%.2f] LowerLimitPrice[%.2f]'
    #             % (nRequestID, pSecurityField.SecurityID, pSecurityField.SecurityName, pSecurityField.MarketID,
    #             pSecurityField.OrderUnit, pSecurityField.OpenDate, pSecurityField.UpperLimitPrice, pSecurityField.LowerLimitPrice))
    #     else:
    #         print('查询合约结束[%d] ErrorID[%d] ErrorMsg[%s]'
    #         % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))


    # def OnRspQryInvestor(self, pInvestorField: "CTORATstpInvestorField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int", bIsLast: "bool") -> "void":
    #     if bIsLast != 1:
    #         print('OnRspQryInvestor[%d]: InvestorID[%s]  Operways[%s]'
    #             %(nRequestID, pInvestorField.InvestorID, 
    #             pInvestorField.Operways))
    #     else:
    #         print('查询投资者结束[%d] ErrorID[%d] ErrorMsg[%s]'
    #             % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))


    # def OnRspQryShareholderAccount(self, pShareholderAccountField: "CTORATstpShareholderAccountField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int", bIsLast: "bool") -> "void":
    #     if bIsLast != 1:
    #         print('OnRspQryShareholderAccount[%d]: InvestorID[%s] ExchangeID[%s] ShareholderID[%s]'
    #             %(nRequestID, pShareholderAccountField.InvestorID, pShareholderAccountField.ExchangeID, pShareholderAccountField.ShareholderID))
    #     else:
    #         print('查询股东账户结束[%d] ErrorID[%d] ErrorMsg[%s]'
    #             % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))


    # def OnRspQryTradingAccount(self, pTradingAccountField: "CTORATstpTradingAccountField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int", bIsLast: "bool") -> "void":
    #     if bIsLast != 1:
    #         print('OnRspQryTradingAccount[%d]: DepartmentID[%s] InvestorID[%s] AccountID[%s] CurrencyID[%s] UsefulMoney[%.2f] FetchLimit[%.2f]'
    #             % (nRequestID, pTradingAccountField.DepartmentID, pTradingAccountField.InvestorID, pTradingAccountField.AccountID, pTradingAccountField.CurrencyID,
    #             pTradingAccountField.UsefulMoney, pTradingAccountField.FetchLimit))
    #     else:
    #         print('查询资金账号结束[%d] ErrorID[%d] ErrorMsg[%s]'
    #             % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))


    # def OnRspQryOrder(self, pOrderField: "CTORATstpOrderField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int", bIsLast: "bool") -> "void":
    #     if bIsLast != 1:
    #         print('OnRspQryOrder[%d]: SecurityID[%s] OrderLocalID[%s] OrderRef[%d] OrderSysID[%s] VolumeTraded[%d] OrderStatus[%s] OrderSubmitStatus[%s], StatusMsg[%s]'
    #             % (nRequestID, pOrderField.SecurityID, pOrderField.OrderLocalID, pOrderField.OrderRef, pOrderField.OrderSysID, 
    #             pOrderField.VolumeTraded, pOrderField.OrderStatus, pOrderField.OrderSubmitStatus, pOrderField.StatusMsg))
    #     else:
    #         print('查询报单结束[%d] ErrorID[%d] ErrorMsg[%s]'
    #             % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))

    # def OnRspQryPosition(self, pPositionField: "CTORATstpPositionField", pRspInfoField: "CTORATstpRspInfoField", nRequestID: "int", bIsLast: "bool") -> "void":
    #     if bIsLast != 1:
    #         print('OnRspQryPosition[%d]: InvestorID[%s] SecurityID[%s] HistoryPos[%d] TodayBSPos[%d] TodayPRPos[%d]'
    #             % (nRequestID, pPositionField.InvestorID, pPositionField.SecurityID, pPositionField.HistoryPos, 
    #             pPositionField.TodayBSPos, pPositionField.TodayPRPos))
    #     else:
    #         print('查询持仓结束[%d] ErrorID[%d] ErrorMsg[%s]'
    #             % (nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))

import sys

class MdSpi(xmdapi.CTORATstpXMdSpi):
    def __init__(self, api):
        xmdapi.CTORATstpXMdSpi.__init__(self)
        self.__api = api
    def OnFrontConnected(self):#不进行登录和订阅的话就会报错链接错误
        print("OnFrontConnected")
        #请求登录，目前未校验登录用户，请求域置空即可
        login_req = xmdapi.CTORATstpReqUserLoginField()
        self.__api.ReqUserLogin(login_req, 1)
    def OnRspUserLogin(self, pRspUserLoginField, pRspInfoField, nRequestID):#用户登录并且订阅600621华鑫股份
        # pass
        if pRspInfoField.ErrorID == 0:
            print('Login success! [%d]' % nRequestID)#登录成功
            '''
            订阅行情
            当sub_arr中只有一个"00000000"的合约且ExchangeID填TORA_TSTP_EXD_SSE或TORA_TSTP_EXD_SZSE时，订阅单市场所有合约行情
			当sub_arr中只有一个"00000000"的合约且ExchangeID填TORA_TSTP_EXD_COMM时，订阅全市场所有合约行情
			其它情况,订阅sub_arr集合中的合约行情
            '''
            sub_arr = [b'600621']
            ret = self.__api.SubscribeMarketData(sub_arr, xmdapi.TORA_TSTP_EXD_SSE)
            if ret != 0:
                print('SubscribeMarketData fail, ret[%d]' % ret)
            else:
                print('SubscribeMarketData success, ret[%d]' % ret)
            sub_arr = [b'000001']
            ret = self.__api.SubscribeRapidMarketData(sub_arr, xmdapi.TORA_TSTP_EXD_SZSE)
            if ret != 0:
                print('SubscribeRapidMarketData fail, ret[%d]' % ret)#订阅市场数据失败
            else:
                print('SubscribeRapidMarketData success, ret[%d]' % ret)#订阅市场数据成功
        else:
            print('Login fail!!! [%d] [%d] [%s]'
                %(nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))#登录失败
    def OnRspSubMarketData(self, pSpecificSecurityField, pRspInfoField):#接收已订阅市场数据
        if pRspInfoField.ErrorID == 0:
            print('OnRspSubMarketData: OK!')#接收已订阅市场数据成功
        else:
            print('OnRspSubMarketData: Error! [%d] [%s]'
                %(pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))
    def OnRspUnSubMarketData(self, pSpecificSecurityField, pRspInfoField):#接收未订阅市场数据
        if pRspInfoField.ErrorID == 0:
            print('OnRspUnSubMarketData: OK!')#接收未订阅市场数据成功
        else:
            print('OnRspUnSubMarketData: Error! [%d] [%s]'
                %(pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))
    def OnRspSubRapidMarketData(self, pSpecificSecurityField, pRspInfoField):
        if pRspInfoField.ErrorID == 0:
            print('OnRspSubRapidMarketData: OK!')
        else:
            print('OnRspSubRapidMarketData: Error! [%d] [%s]'
                %(pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))
    def OnRtnMarketData(self, pMarketDataField):#返回市场数据详情
        print("OnRtnMarketData::SecurityID[%s] SecurityName[%s] LastPrice[%.2f] Volume[%d] Turnover[%.2f] BidPrice1[%.2f] BidVolume1[%d] AskPrice1[%.2f] AskVolume1[%d] UpperLimitPrice[%.2f] LowerLimitPrice[%.2f]" 
            % (pMarketDataField.SecurityID, pMarketDataField.SecurityName, pMarketDataField.LastPrice, pMarketDataField.Volume,pMarketDataField.Turnover, pMarketDataField.BidPrice1, 
            pMarketDataField.BidVolume1, pMarketDataField.AskPrice1,pMarketDataField.AskVolume1, pMarketDataField.UpperLimitPrice, pMarketDataField.LowerLimitPrice))
    def OnRtnRapidMarketData(self, pRapidMarketDataField):
        print("SecurityID[%s] LastPrice[%.2f] TotalVolumeTrade[%d] TotalValueTrade[%.2f] BidPrice1[%.2f] BidVolume1[%d] BidCount1[%d] AskPrice1[%.2f] AskVolume1[%d] AskCount1[%d] UpperLimitPrice[%.2f] LowerLimitPrice[%.2f]"
            % (pRapidMarketDataField.SecurityID, pRapidMarketDataField.LastPrice, pRapidMarketDataField.TotalVolumeTrade,
               pRapidMarketDataField.TotalValueTrade, pRapidMarketDataField.BidPrice1, pRapidMarketDataField.BidVolume1, pRapidMarketDataField.BidCount1, pRapidMarketDataField.AskPrice1,
               pRapidMarketDataField.AskVolume1, pRapidMarketDataField.AskCount1, pRapidMarketDataField.UpperLimitPrice, pRapidMarketDataField.LowerLimitPrice))

CTORATstpMarketDataField#行情数据IOPV

# PreCloseIOPV = property(_xmdapi.CTORATstpMarketDataField_PreCloseIOPV_get, _xmdapi.CTORATstpMarketDataField_PreCloseIOPV_set)
# IOPV = property(_xmdapi.CTORATstpMarketDataField_IOPV_get, _xmdapi.CTORATstpMarketDataField_IOPV_set)

# if __name__ == "__main__":
#     # 打印接口版本号
#     print("XMDAPI版本号::"+xmdapi.CTORATstpXMdApi_GetApiVersion())
#     print("sys.argv",sys.argv)#系统文件参数，这里就一个，后面的方式应该是同时启动多个文件啥的，或者干脆就是想办法默认获取得到1
#     argc=len(sys.argv)#【参数1默认执行TCP访问】
#     print("argc",argc)
#     if argc==1 : #默认TCP连接仿真环境
#         XMD_TCP_FrontAddress ="tcp://210.14.72.21:4402"#行情服务器接口
#     elif argc == 3 and sys.argv[1]=="tcp": #普通TCP方式
#         XMD_TCP_FrontAddress=sys.argv[2]
#     elif argc == 4 and sys.argv[1]=="udp": #UDP 组播
#         XMD_MCAST_FrontAddress=sys.argv[2] #组播地址
#         XMD_MCAST_InterfaceIP=sys.argv[3]	#组播接收地址
#     elif argc == 5 and sys.argv[1]=="fens":  #FENS名字服务器 TCP方式
#         XMD_FENS_FrontAddress=sys.argv[2]	#FENS 名字服务器地址
#         XDM_FENS_FensEnvID=sys.argv[3] #注册FENS服务信息必需柜台环境类型，股票现货为"stock"
#         XDM_FENS_FensNodeID=sys.argv[4] #仿真为“sim_xmd”，7*24小时“24_xmd”,支持FENS的生产环境一般为节点号
#     elif argc == 5 and sys.argv[1]=="lob": #同时组播订阅普通行情和衍生行情（合成快照），仅适用于生产环境
#         XMD_MCAST_FrontAddress=sys.argv[2] #普通服务组播地址
#         XMD_MCAST_DeriveAddress=sys.argv[3]	#衍生服务组播地址
#         XMD_MCAST_InterfaceIP=sys.argv[4]	#接收普通行情服务和衍生行情服务的网口地址(托管服务器)
#     else:
#         print("/*********************************************demo运行说明************************************\n")
#         print("* argv[1]: tcp udp fens lob\t\t\t\t=[%s]" % (sys.argv[1]))
#         print("* argv[2]: tcp/fens::FrontIP upd/lob::MCAST_IP\t\t=[%s]" % (sys.argv[2] if argc>2 else ""))
#         print("* argv[3]: fens::EnvID udp::InterfaceIP lob::DeriveIP\t=[%s]" % (sys.argv[3] if argc>3 else ""))
#         print("* argv[4]: fens::FensNodeID\t\t\t\t=[%s]" % (sys.argv[4] if argc>4 else ""))
#         print("* Usage:")
#         print("* 默认连仿真:		python3 xmddemo.py")
#         print("* 指定TCP地址:		python3 xmddemo.py tcp tcp://210.14.72.21:4402")
#         print("* 指定FENS地址:		python3 xmddemo fens tcp://210.14.72.21:42370 stock sim_xmd")
#         print("* 指定组播地址:		python3 xmddemo udp udp://224.224.1.3:7880 x.x.x.x")
#         print("* 实盘实时快照:		python3 xmddemo lob udp://224.224.1.3:7880 udp://224.224.3.3:7888 x.x.x.x")
#         print("* 上述x.x.x.x使用托管服务器中接收XMD行情的网口IP地址")
#         print("* ******************************************************************************************/")
#         exit(-1)

#     '''*************************创建实例 注册服务*****************'''
#     if argc==1 or sys.argv[1]=="tcp" :   #默认或TCP方式【目前使用的方式】
#         print("************* XMD TCP *************")
# 		#TCP订阅lv1行情，前置Front和FENS方式都用默认构造
#         api = xmdapi.CTORATstpXMdApi_CreateTstpXMdApi()
#         api.RegisterFront(XMD_TCP_FrontAddress)
#         # 注册多个行情前置服务地址，用逗号隔开
#         # 例如:api.RegisterFront("tcp://10.0.1.101:6402,tcp://10.0.1.101:16402")
#         print("XMD_TCP_FrontAddress[TCP]::%s" % XMD_TCP_FrontAddress)
#     elif sys.argv[1]=="udp"  :  #组播普通行情	
#         print("************* XMD UDP *************")
#         #XMD组播订阅lv1行情
#         api = xmdapi.CTORATstpXMdApi_CreateTstpXMdApi(xmdapi.TORA_TSTP_MST_MCAST)
#         api.RegisterMulticast(XMD_MCAST_FrontAddress, XMD_MCAST_InterfaceIP, "")
#         print("XMD_MCAST_FrontAddress[UDP]::%s" % XMD_MCAST_FrontAddress)
#     elif sys.argv[1]=="fens" :  #FENS 名字服务注册
#         print("********** XMD FENS MultiCast **********")
#         '''********************************************************************************
# 		 * 注册 fens 地址前还需注册 fens 用户信息,包括环境编号、节点编号、Fens 用户代码等信息
# 		 * 使用名字服务器的好处是当券商系统部署方式发生调整时外围终端无需做任何前置地址修改
# 		 * *****************************************************************************'''
#         #TCP订阅lv1行情，前置Front和FENS方式都用默认构造
#         api = xmdapi.CTORATstpXMdApi_CreateTstpXMdApi()

#         fens_user_info_field=xmdapi.CTORATstpFensUserInfoField()
#         fens_user_info_field.FensEnvID=XDM_FENS_FensEnvID      #必填项，暂时固定为“stock”表示普通现货柜台
#         fens_user_info_field.FensNodeID=XDM_FENS_FensNodeID   #必填项，生产环境需按实际填写,仿真环境为sim_xmd
#         api.RegisterFensUserInfo(fens_user_info_field)
# 		#必须先注册Fens信息再注册Fens
#         api.RegisterNameServer(XMD_FENS_FrontAddress)
#         # 注册名字服务器地址，支持多服务地址逗号隔开
#         # 例如:api.RegisterNameServer('tcp://10.0.1.101:52370,tcp://10.0.1.101:62370')
#         print("XMD_FENS_FrontAddress[FENS]::%s" % XMD_FENS_FrontAddress)
#     elif sys.argv[1]=="lob" :   #组播普通+组播衍生行情(实时合成快照)
#         print("************* XMD UDP+UDP *************")
# 		#组播订阅lv1行情及组播订阅合成快照
#         api = xmdapi.CTORATstpXMdApi_CreateTstpXMdApi(xmdapi.TORA_TSTP_MST_MCAST, xmdapi.TORA_TSTP_MST_MCAST)
#         #先注册普通服务，再注册衍生服务
#         api.RegisterMulticast(XMD_MCAST_FrontAddress, XMD_MCAST_InterfaceIP, "")
#         # 注:合成快照数据量与Lev2基本相当，从性能角度考虑，一般不推荐使用非C++ API进行开发。
#         api.RegisterDeriveMulticast(XMD_MCAST_DeriveAddress, XMD_MCAST_InterfaceIP, "")
#         print("XMD_MCAST_FrontAddress[lob]::%s", XMD_MCAST_FrontAddress)
#         print("XMD_MCAST_DeriveAddress[lob]::%s", XMD_MCAST_DeriveAddress)
#     else:
#         print("/*********************************************demo运行说明************************************\n")
#         print("* argv[1]: tcp udp fens lob\t\t\t\t=[%s]" % (sys.argv[1]))
#         print("* argv[2]: tcp/fens::FrontIP upd/lob::MCAST_IP\t\t=[%s]" % (sys.argv[2] if argc>2 else ""))
#         print("* argv[3]: fens::EnvID udp::InterfaceIP lob::DeriveIP\t=[%s]" % (sys.argv[3] if argc>3 else ""))
#         print("* argv[4]: fens::FensNodeID\t\t\t\t=[%s]" % (sys.argv[4] if argc>4 else ""))
#         print("* Usage:")
#         print("* 默认连仿真:		python3 xmddemo.py")
#         print("* 指定TCP地址:		python3 xmddemo.py tcp tcp://210.14.72.21:4402")
#         print("* 指定FENS地址:		python3 xmddemo.py fens tcp://210.14.72.21:42370 stock sim_xmd")
#         print("* 指定组播地址:		python3 xmddemo.py udp udp://224.224.1.3:7880 x.x.x.x")
#         print("* 实盘实时快照:		python3 xmddemo.py lob udp://224.224.1.3:7880 udp://224.224.3.3:7888 x.x.x.x")
#         print("* 上述x.x.x.x使用托管服务器中接收XMD行情的网口IP地址")
#         print("* ******************************************************************************************/")
#         sys.exit(-2)

#     # 创建回调对象
#     spi = MdSpi(api)
#     # 注册回调接口
#     api.RegisterSpi(spi)
#     # 启动接口
#     api.Init()
#     # 等待程序结束
#     input()
#     # 释放接口对象
#     api.Release()

#明天根据159302计算ETF溢价率，最大现金替代比例是1，也就是可以全现金申赎
if __name__ == '__main__':
    # 打印接口版本号
    print("TradeAPI Version:::"+traderapi.CTORATstpTraderApi_GetApiVersion())
    # 创建接口对象
    # pszFlowPath为私有流和公有流文件存储路径，若订阅私有流和公有流且创建多个接口实例，每个接口实例应配置不同的路径
    # bEncrypt为网络数据是否加密传输，考虑数据安全性，建议以互联网方式接入的终端设置为加密传输
    api:traderapi.CTORATstpTraderApi = traderapi.CTORATstpTraderApi.CreateTstpTraderApi('./flow', False)
    # 创建回调对象
    spi = TraderSpi(api)
    # 注册回调接口
    api.RegisterSpi(spi)
    if 1:   #模拟环境，TCP 直连Front方式
        # 注册单个交易前置服务地址
        TD_TCP_FrontAddress="tcp://210.14.72.21:4400" #仿真交易环境
        # TD_TCP_FrontAddress="tcp://210.14.72.15:4400" #24小时环境A套
        # TD_TCP_FrontAddress="tcp://210.14.72.16:9500" #24小时环境B套
        api.RegisterFront(TD_TCP_FrontAddress)
        # 注册多个交易前置服务地址，用逗号隔开 形如: api.RegisterFront("tcp://10.0.1.101:6500,tcp://10.0.1.101:26500")
        print("TD_TCP_FensAddress[sim or 24H]::%s\n"%TD_TCP_FrontAddress)
    else:	#模拟环境，FENS名字服务器方式
        TD_TCP_FensAddress ="tcp://210.14.72.21:42370"; #模拟环境通用fens地址
        '''********************************************************************************
        * 注册 fens 地址前还需注册 fens 用户信息，包括环境编号、节点编号、Fens 用户代码等信息
        * 使用名字服务器的好处是当券商系统部署方式发生调整时外围终端无需做任何前置地址修改
        * *****************************************************************************'''
        fens_user_info_field = traderapi.CTORATstpFensUserInfoField()
        fens_user_info_field.FensEnvID="stock" #必填项，暂时固定为“stock”表示普通现货柜台
        fens_user_info_field.FensNodeID="sim"  #必填项，生产环境需按实际填写,仿真环境为sim
        fens_user_info_field.FensNodeID,="24a" #必填项，生产环境需按实际填写,24小时A套环境为24a
        # fens_user_info_field.FensNodeID="24b" #必填项，生产环境需按实际填写,24小时B套环境为24b
        api.RegisterFensUserInfo(fens_user_info_field)
        api.RegisterNameServer(TD_TCP_FensAddress)
        # 注册名字服务器地址，支持多服务地址逗号隔开 形如:api.RegisterNameServer('tcp://10.0.1.101:52370,tcp://10.0.1.101:62370')
        print("TD_TCP_FensAddress[%s]::%s\n"%(fens_user_info_field.FensNodeID,TD_TCP_FensAddress))
    #订阅私有流
    api.SubscribePrivateTopic(traderapi.TORA_TERT_QUICK)
    #订阅公有流
    api.SubscribePublicTopic(traderapi.TORA_TERT_QUICK)
    '''**********************************
	*	TORA_TERT_RESTART, 从日初开始
	*	TORA_TERT_RESUME, 从断开时候开始
	*	TORA_TERT_QUICK, 从最新时刻开始
	*************************************'''
    # 启动接口
    api.Init()
    api.Join()
	# 等待程序结束
    input()
    # 释放接口对象
    api.Release()
