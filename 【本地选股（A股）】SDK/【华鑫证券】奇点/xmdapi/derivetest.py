#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xmdapi

class MdSpi(xmdapi.CTORATstpXMdSpi):
    def __init__(self, api):
        xmdapi.CTORATstpXMdSpi.__init__(self)
        self.__api = api

    def OnFrontConnected(self):
        print("OnFrontConnected")
        
        #请求登录，目前未校验登录用户，请求域置空即可
        login_req = xmdapi.CTORATstpReqUserLoginField()
        self.__api.ReqUserLogin(login_req, 1)

    def OnRspUserLogin(self, pRspUserLoginField, pRspInfoField, nRequestID):
        if pRspInfoField.ErrorID == 0:
            print('Login success! [%d]' % nRequestID)

            '''
            订阅行情
            当sub_arr中只有一个"00000000"的合约且ExchangeID填TORA_TSTP_EXD_SSE或TORA_TSTP_EXD_SZSE时，订阅单市场所有合约行情
			其它情况，订阅sub_arr集合中的合约行情
            '''
            sub_arr = [b'000002']
            ret = self.__api.SubscribeRapidMarketData(sub_arr, xmdapi.TORA_TSTP_EXD_SZSE)
            if ret != 0:
                print('SubscribeRapidMarketData fail, ret[%d]' % ret)
            else:
                print('SubscribeRapidMarketData success, ret[%d]' % ret)

            sub_arr = [b'00000000']
            ret = self.__api.SubscribeRapidMarketData(sub_arr, xmdapi.TORA_TSTP_EXD_SSE)
            if ret != 0:
                print('SubscribeRapidMarketData fail, ret[%d]' % ret)
            else:
                print('SubscribeRapidMarketData success, ret[%d]' % ret)

            if 0:
                sub_arr = [b'000002']
                ret = self.__api.UnSubscribeRapidMarketData(sub_arr, xmdapi.TORA_TSTP_EXD_SZSE)
                if ret != 0:
                    print('UnSubscribeRapidMarketData fail, ret[%d]' % ret)
                else:
                    print('SubscribeRapidMarketData success, ret[%d]' % ret)

            if 0:
                sub_arr = [b'00000000']
                ret = self.__api.UnSubscribeRapidMarketData(sub_arr, xmdapi.TORA_TSTP_EXD_SSE)
                if ret != 0:
                    print('UnSubscribeRapidMarketData fail, ret[%d]' % ret)
                else:
                    print('SubscribeRapidMarketData success, ret[%d]' % ret)
                    
        else:
            print('Login fail!!! [%d] [%d] [%s]'
                %(nRequestID, pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))


    def OnRspSubRapidMarketData(self, pSpecificSecurityField, pRspInfoField):
        if pRspInfoField.ErrorID == 0:
            print('OnRspSubRapidMarketData: OK!')
        else:
            print('OnRspSubRapidMarketData: Error! [%d] [%s]'
                %(pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))


    def OnRspUnSubRapidMarketData(self, pSpecificSecurityField, pRspInfoField):
        if pRspInfoField.ErrorID == 0:
            print('OnRspUnSubRapidMarketData: OK!')
        else:
            print('OnRspUnSubRapidMarketData: Error! [%d] [%s]'
                %(pRspInfoField.ErrorID, pRspInfoField.ErrorMsg))

    def OnRtnRapidMarketData(self, pRapidMarketDataField):
        print("SecurityID[%s] LastPrice[%.2f] TotalVolumeTrade[%d] TotalValueTrade[%.2f] BidPrice1[%.2f] BidVolume1[%d] BidCount1[%d] AskPrice1[%.2f] AskVolume1[%d] AskCount1[%d] UpperLimitPrice[%.2f] LowerLimitPrice[%.2f]"
            % (pRapidMarketDataField.SecurityID, pRapidMarketDataField.LastPrice, pRapidMarketDataField.TotalVolumeTrade,
               pRapidMarketDataField.TotalValueTrade, pRapidMarketDataField.BidPrice1, pRapidMarketDataField.BidVolume1, pRapidMarketDataField.BidCount1, pRapidMarketDataField.AskPrice1,
               pRapidMarketDataField.AskVolume1, pRapidMarketDataField.AskCount1, pRapidMarketDataField.UpperLimitPrice, pRapidMarketDataField.LowerLimitPrice))


if __name__ == "__main__":
    # 打印接口版本号
    print(xmdapi.CTORATstpXMdApi_GetApiVersion())

    # 创建接口对象，第一个参数对应行情前置地址模式（RegisterMulticast），第二个参数对应衍生服务地址模式（RegisterDeriveMulticast）
    api = xmdapi.CTORATstpXMdApi_CreateTstpXMdApi(xmdapi.TORA_TSTP_MST_MCAST, xmdapi.TORA_TSTP_MST_MCAST)

    # 创建回调对象
    spi = MdSpi(api)

    # 注册回调接口
    api.RegisterSpi(spi)

    # 注册单个行情前置服务地址及衍生服务地址。只订阅合成快照时前置地址也可用衍生服务地址替代。
    # 注：合成快照数据量与Lev2基本相当，从性能角度考虑，一般不推荐使用非C++ API进行开发。
    api.RegisterMulticast("udp://224.224.3.3:7888", "10.168.9.1", "")
    api.RegisterDeriveMulticast("udp://224.224.3.3:7888", "10.168.9.1", "")

    # 启动接口
    api.Init()

    # 等待程序结束
    input()

    # 释放接口对象
    api.Release()
