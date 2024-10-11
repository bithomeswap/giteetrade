# CTORATstpETFFileField【ETF清单列表函数】在交易API当中
# CTORATstpETFFileField【ETF成分券详情函数】在交易API当中

# 要求3.7的python环境
# conda create -n my_env3.7 python=3.7

# # market文件是行情API
# # traderapi文件是交易API
# 行情：tcp://210.14.72.21:4402  
# 交易：tcp://210.14.72.21:4400

# 交易、行情fens地址：
# tcp://210.14.72.21:42370
# #首先注册fens信息，RegisterFensUserInfo(&fens_user_info_field)
# 其中：FensEnvID="stock"
# 仿真交易：FensNodeID="sim"
# 仿真行情：FensNodeID="sim_xmd"
# #然后注册fens地址，如：
# RegisterNameServer("tcp://210.14.72.21:42370")

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' 注意: 如果提示找不到_xmdapi.so 且已发布的库文件不一致时,可自行重命名为_xmdapi.so '''

#from asyncio.windows_events import NULL #仅适用于Windows
import sys
import xmdapi

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

if __name__ == "__main__":
    # 打印接口版本号
    print("XMDAPI版本号::"+xmdapi.CTORATstpXMdApi_GetApiVersion())
    print("sys.argv",sys.argv)#系统文件参数，这里就一个，后面的方式应该是同时启动多个文件啥的，或者干脆就是想办法默认获取得到1
    argc=len(sys.argv)#【参数1默认执行TCP访问】
    print("argc",argc)
    if argc==1 : #默认TCP连接仿真环境
        XMD_TCP_FrontAddress ="tcp://210.14.72.21:4402"#行情服务器接口
    elif argc == 3 and sys.argv[1]=="tcp" :   #普通TCP方式
        XMD_TCP_FrontAddress=sys.argv[2]
    elif argc == 4 and sys.argv[1]=="udp" :   #UDP 组播
        XMD_MCAST_FrontAddress=sys.argv[2]	#组播地址
        XMD_MCAST_InterfaceIP=sys.argv[3]	#组播接收地址
    elif argc == 5 and sys.argv[1]=="fens" :  #FENS名字服务器 TCP方式
        XMD_FENS_FrontAddress=sys.argv[2]	#FENS 名字服务器地址
        XDM_FENS_FensEnvID=sys.argv[3]		#注册FENS服务信息必需柜台环境类型，股票现货为"stock"
        XDM_FENS_FensNodeID=sys.argv[4] 	#仿真为“sim_xmd”，7*24小时“24_xmd”,支持FENS的生产环境一般为节点号
    elif argc == 5 and sys.argv[1]=="lob" :   #同时组播订阅普通行情和衍生行情（合成快照），仅适用于生产环境
        XMD_MCAST_FrontAddress=sys.argv[2]	#普通服务组播地址
        XMD_MCAST_DeriveAddress=sys.argv[3]	#衍生服务组播地址
        XMD_MCAST_InterfaceIP=sys.argv[4]	#接收普通行情服务和衍生行情服务的网口地址(托管服务器)
    else:
        print("/*********************************************demo运行说明************************************\n")
        print("* argv[1]: tcp udp fens lob\t\t\t\t=[%s]" % (sys.argv[1]))
        print("* argv[2]: tcp/fens::FrontIP upd/lob::MCAST_IP\t\t=[%s]" % (sys.argv[2] if argc>2 else ""))
        print("* argv[3]: fens::EnvID udp::InterfaceIP lob::DeriveIP\t=[%s]" % (sys.argv[3] if argc>3 else ""))
        print("* argv[4]: fens::FensNodeID\t\t\t\t=[%s]" % (sys.argv[4] if argc>4 else ""))
        print("* Usage:")
        print("* 默认连仿真:		python3 xmddemo.py")
        print("* 指定TCP地址:		python3 xmddemo.py tcp tcp://210.14.72.21:4402")
        print("* 指定FENS地址:		python3 xmddemo fens tcp://210.14.72.21:42370 stock sim_xmd")
        print("* 指定组播地址:		python3 xmddemo udp udp://224.224.1.3:7880 x.x.x.x")
        print("* 实盘实时快照:		python3 xmddemo lob udp://224.224.1.3:7880 udp://224.224.3.3:7888 x.x.x.x")
        print("* 上述x.x.x.x使用托管服务器中接收XMD行情的网口IP地址")
        print("* ******************************************************************************************/")
        exit(-1)

    '''*************************创建实例 注册服务*****************'''
    if argc==1 or sys.argv[1]=="tcp" :   #默认或TCP方式【目前使用的方式】
        print("************* XMD TCP *************")
		#TCP订阅lv1行情，前置Front和FENS方式都用默认构造
        api = xmdapi.CTORATstpXMdApi_CreateTstpXMdApi()
        api.RegisterFront(XMD_TCP_FrontAddress)
        # 注册多个行情前置服务地址，用逗号隔开
        # 例如:api.RegisterFront("tcp://10.0.1.101:6402,tcp://10.0.1.101:16402")
        print("XMD_TCP_FrontAddress[TCP]::%s" % XMD_TCP_FrontAddress)
    elif sys.argv[1]=="udp"  :  #组播普通行情	
        print("************* XMD UDP *************")
        #XMD组播订阅lv1行情
        api = xmdapi.CTORATstpXMdApi_CreateTstpXMdApi(xmdapi.TORA_TSTP_MST_MCAST)
        api.RegisterMulticast(XMD_MCAST_FrontAddress, XMD_MCAST_InterfaceIP, "")
        print("XMD_MCAST_FrontAddress[UDP]::%s" % XMD_MCAST_FrontAddress)
    elif sys.argv[1]=="fens" :  #FENS 名字服务注册
        print("********** XMD FENS MultiCast **********")
        '''********************************************************************************
		 * 注册 fens 地址前还需注册 fens 用户信息,包括环境编号、节点编号、Fens 用户代码等信息
		 * 使用名字服务器的好处是当券商系统部署方式发生调整时外围终端无需做任何前置地址修改
		 * *****************************************************************************'''
        #TCP订阅lv1行情，前置Front和FENS方式都用默认构造
        api = xmdapi.CTORATstpXMdApi_CreateTstpXMdApi()

        fens_user_info_field=xmdapi.CTORATstpFensUserInfoField()
        fens_user_info_field.FensEnvID=XDM_FENS_FensEnvID      #必填项，暂时固定为“stock”表示普通现货柜台
        fens_user_info_field.FensNodeID=XDM_FENS_FensNodeID   #必填项，生产环境需按实际填写,仿真环境为sim_xmd
        api.RegisterFensUserInfo(fens_user_info_field)
		#必须先注册Fens信息再注册Fens
        api.RegisterNameServer(XMD_FENS_FrontAddress)
        # 注册名字服务器地址，支持多服务地址逗号隔开
        # 例如:api.RegisterNameServer('tcp://10.0.1.101:52370,tcp://10.0.1.101:62370')
        print("XMD_FENS_FrontAddress[FENS]::%s" % XMD_FENS_FrontAddress)
    elif sys.argv[1]=="lob" :   #组播普通+组播衍生行情(实时合成快照)
        print("************* XMD UDP+UDP *************")
		#组播订阅lv1行情及组播订阅合成快照
        api = xmdapi.CTORATstpXMdApi_CreateTstpXMdApi(xmdapi.TORA_TSTP_MST_MCAST, xmdapi.TORA_TSTP_MST_MCAST)
        #先注册普通服务，再注册衍生服务
        api.RegisterMulticast(XMD_MCAST_FrontAddress, XMD_MCAST_InterfaceIP, "")
        # 注:合成快照数据量与Lev2基本相当，从性能角度考虑，一般不推荐使用非C++ API进行开发。
        api.RegisterDeriveMulticast(XMD_MCAST_DeriveAddress, XMD_MCAST_InterfaceIP, "")
        print("XMD_MCAST_FrontAddress[lob]::%s", XMD_MCAST_FrontAddress)
        print("XMD_MCAST_DeriveAddress[lob]::%s", XMD_MCAST_DeriveAddress)
    else:
        print("/*********************************************demo运行说明************************************\n")
        print("* argv[1]: tcp udp fens lob\t\t\t\t=[%s]" % (sys.argv[1]))
        print("* argv[2]: tcp/fens::FrontIP upd/lob::MCAST_IP\t\t=[%s]" % (sys.argv[2] if argc>2 else ""))
        print("* argv[3]: fens::EnvID udp::InterfaceIP lob::DeriveIP\t=[%s]" % (sys.argv[3] if argc>3 else ""))
        print("* argv[4]: fens::FensNodeID\t\t\t\t=[%s]" % (sys.argv[4] if argc>4 else ""))
        print("* Usage:")
        print("* 默认连仿真:		python3 xmddemo.py")
        print("* 指定TCP地址:		python3 xmddemo.py tcp tcp://210.14.72.21:4402")
        print("* 指定FENS地址:		python3 xmddemo.py fens tcp://210.14.72.21:42370 stock sim_xmd")
        print("* 指定组播地址:		python3 xmddemo.py udp udp://224.224.1.3:7880 x.x.x.x")
        print("* 实盘实时快照:		python3 xmddemo.py lob udp://224.224.1.3:7880 udp://224.224.3.3:7888 x.x.x.x")
        print("* 上述x.x.x.x使用托管服务器中接收XMD行情的网口IP地址")
        print("* ******************************************************************************************/")
        sys.exit(-2)

    # 创建回调对象
    spi = MdSpi(api)
    # 注册回调接口
    api.RegisterSpi(spi)
    # 启动接口
    api.Init()
    # 等待程序结束
    input()
    # 释放接口对象
    api.Release()