import json
import os
from .account import *
from . import smartc
from .utils import *
from . import utils
import logging
logger = logging.getLogger()

'''
多平台账户管理器，管理所有平台的账户
'''


class AccountManager:
    def __init__(self,context):
        self.accountMap = {}
        self.smart = context

    def getAccountMap(self):
        return self.accountMap

    def getAccountById(self, id:str):
        return self.accountMap[id]

    '''
     * 初始化用户数据/切换用户
    '''
    def initUserData(self, configPath:str, user:dict, accCallback):
        # 如果用户存在，不需要加载数据，只需要
        if user is not None:
            return
        account = None

        def strategyCallback(strategyMap:dict):
            try:
                #将多用户的策略列表归集到smart.strategy_map下
                account.strategy_map = strategyMap
                assign(self.smart.strategy_map,strategyMap)
                accCallback()
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)

        ''' 读取历史委托和成交 '''
        def getOrdersAndTradesCallback(rsp:str):
            try:
                data = decodeRsp(rsp)
                orderList = data["order_list"]
                tradeList = data["trade_list"]
                #初始化委托列表
                for item in orderList:
                    order = Order()
                    assign(order,item)
                    order.code = order.instrument_id + "." + getExchangeStrFromExchangeId(order.exchange_id)
                    order.instrument_type = InstrumentType.__dict__.get(order.instrument_type,0)
                    account.order_list.append(order)
                    account.order_map[order.order_id] = order
                #初始化成交列表
                for item in tradeList:
                    trade = Trade()
                    assign(trade,item)
                    trade.code = trade.instrument_id + "." + getExchangeStrFromExchangeId(trade.exchange_id)
                    trade.instrument_type = InstrumentType.__dict__.get(trade.instrument_type,0)
                    account.trade_list.append(trade)
                    account.trade_map[trade.trade_id] = trade

                self.smart.strategyManager.getStrategyMap(None, account,strategyCallback)
            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)

        ''' 读取持仓 '''
        def positionCallback(rsp:str):
            try:
                pList = decodeRsp(rsp)
                positionList = []
                for item in pList:
                    position = None
                    position = convertPositionFromSmartToPlugin(item)
                    positionList.append(position)
                account.refreshPositionList(positionList) # 该账号的实时持仓信息
                
                smartc.request("getOrdersAndTrades", json.dumps({"account_id":account.account_id}),getOrdersAndTradesCallback)
            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
       
       #读取信用融券负债合约  
        def creditDebtSecurityCallback(data:str):
            try:
                debtSecurityMap = decodeRsp(data)
                securityList = []
                securityMap = {}
                for k2 in debtSecurityMap:
                    item = debtSecurityMap[k2]
                    tempDebt = convertCreditDebtSecurityFromSmartToPlugin(item)
                    securityList.append(tempDebt)
                    securityMap[tempDebt.debt_id] = tempDebt
            
                account.credit_debt_security_list = securityList
                account.credit_debt_security_map = securityMap
                smartc.request("getPositionList", "{}",positionCallback)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        
        #读取信用融资负债合约
        def creditDebtFinanceCallback(data:str):
            try:
                debtFinanceMap = decodeRsp(data)
                financeList = []
                financeMap = {}
                for k1 in debtFinanceMap:
                    item = debtFinanceMap[k1]
                    tempDebt = convertCreditDebtFinanceFromSmartToPlugin(item)
                    financeList.append(tempDebt)
                    financeMap[tempDebt.debt_id] = tempDebt
                account.credit_debt_finance_list = financeList
                account.credit_debt_finance_map = financeMap

                smartc.request("getCreditDebtSecurity", "{}",creditDebtSecurityCallback)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
        
        #读取信用可融券头寸
        def creditTickerAssignListCallback(data:str):
            try:
                assignList = decodeRsp(data)
                results = []
                assignMap = {}
                for item in assignList:
                    creditTickerAssignInfo = convertCreditTickerAssignInfoFromSmartToPlugin(item)
                    results.append(creditTickerAssignInfo)
                    assignMap[creditTickerAssignInfo.instrument_id + "_" + creditTickerAssignInfo.exchange_id] = creditTickerAssignInfo
                account.credit_ticker_assign_list = results
                account.credit_ticker_assign_map = assignMap
                smartc.request("getCreditDebtFinance", "{}",creditDebtFinanceCallback)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)

        #资产信息
        def creditAssetsCallback(data:str):
            try:
                creditAssets = decodeRsp(data)
                utils.assign(account.assets, convertCreditAssetsFromSmartToPlugin(creditAssets))          
                smartc.request("getCreditTickerAssignList", "{}",creditTickerAssignListCallback)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)
       

        ''' 读取资产信息 '''
        def assetCallback(rsp:str):
            try:
                assets = decodeRsp(rsp)
                account.xtp_account_type = assets['accountType']
                if account.xtp_account_type == 'XTP_ACCOUNT_NORMAL':
                    account.account_type = AccountType.Stock # 账户类型 AccountType
                elif (account.xtp_account_type == 'XTP_ACCOUNT_CREDIT'): 
                    account.account_type = AccountType.Credit
                elif (account.xtp_account_type == 'XTP_ACCOUNT_DERIVE'): 
                    account.account_type = AccountType.Future
                account.source = Source.XTP
                account.assets = convertAssetsFromSmartToPlugin(assets)

                if (account.account_type == AccountType.Credit):
                    smartc.request("queryCreditAssets", "{}",creditAssetsCallback)
                else:
                    smartc.request("getPositionList", "{}",positionCallback)

            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
        

        ''' 读取用户信息 '''
        def getUserCallback(rsp:str):
            try:
                user = decodeRsp(rsp)
                if not user['username']:
                    return
                nonlocal account #声明非本地变量
                account = Account(self.smart)
                account.account_id = user['username'] # 当前登录的资金账号
                account.nick_name = user['nickname'] # 资金账号的昵称
                account.exchange_right = user['exchange_right'] # 沪深交易权限  shsz上海深圳   sh上海  sz深圳  双中心用户登录一个节点只有一个市场的权限# #todo ???这个该怎么处理
                if user['quoteLevel'] == "L1":
                    account.isLevel2 = False
                else:
                    account.isLevel2 = True
                username = user['username'] 
                self.smart.account_map[username] = account
                self.accountMap[username] = account
                self.smart.current_account = account
                
                if self.smart.config.get("isBacktest"):
                    account.xtp_account_type = 'XTP_ACCOUNT_NORMAL'
                    account.account_type = AccountType.Stock # 账户类型 AccountType
                    accCallback()
                else:   
                    smartc.request("getAssets","{}",assetCallback)

            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
        smartc.request("getUser","{}",getUserCallback)