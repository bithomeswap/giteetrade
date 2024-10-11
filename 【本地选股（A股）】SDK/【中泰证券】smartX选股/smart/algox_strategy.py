from .strategy import *
from .type import *
from . import smartc
from . import utils
from .utils import *
from .event import *
import json
import logging
logger = logging.getLogger()

class AlgoXStrategy(Strategy):
    def __init__(self,context, strategy_id:str):
        super().__init__(context,StrategyPlatformType.Algo, strategy_id)
        self.orderMap = {}
        self.tradeMap = {}
        self.account = self.smart.current_account
        self.configdata = {}
        self.mstrategyType = None
        self.mclientStrategyId = ""
        self.mxtpStrategyId = ""
        self.started = False

    def loadData(self) :
        self.strategy_order_list = []
        for item in self.account.order_list:
            if(item.parent_order_id == self.strategy_id):
                self.strategy_order_list.append(item)

        self.strategy_trade_list = []
        for item in self.account.trade_list:
            if(item.parent_order_id == self.strategy_id):
                self.strategy_trade_list.append(item)


    #生成母单
    def createStrategy(self,clent_id:str=None, config:dict=None,cb=None) :
        if not clent_id:
            raise Exception("clent_id required!")
        if not config:
            raise Exception("config required!")
        if not cb:
            raise Exception("cb required!")
        order = {
            "strategyType": config.get("strategyType"),
            "clientStrategyId": clent_id,
            "strategyParam": config.get("strategyParam"),
        }
        def createStrategyCallback(rsp:str):
            try:
                data = decodeRsp(rsp)
                cb(self,None)
            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
                cb(None,rspError)
        smartc.request("algocreateStrategy", json.dumps(order), createStrategyCallback if cb else None)

    #停止母单
    def stopStrategy(self,cb=None):
        if not cb:
            raise Exception("cb required!")
        def stopStrategyCallback(rsp:str):
            try:
                data = decodeRsp(rsp)
                cb(data,None)
            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
                cb(None,rspError)
        smartc.request("algostopStrategy", json.dumps({"strategy_id":self.strategy_id}), stopStrategyCallback)
        
    
    #强制停止母单
    def forceStopStrategy(self,cb=None) :
        if not cb:
            raise Exception("cb required!")
        def forceStopStrategyCallback(rsp:str):
            try:
                data = decodeRsp(rsp)
                cb(data,None)
            except RspError as rspError:
                logger.error(rspError,exc_info=True, stack_info=True)
                cb(None,rspError)
        smartc.request("algoforceStopStrategy", json.dumps({"strategy_id":self.strategy_id}), forceStopStrategyCallback)
    
    def _addOrderInfo(self,orderInfo:Order):
        oldOrderInfo = self.orderMap.get(orderInfo.order_id) #todo：这里判断可能条件不足 特别是多账号下可能冲突
        if (not oldOrderInfo):
            self.orderMap[orderInfo.order_id] = orderInfo
            self.strategy_order_list.append(orderInfo)
        else:
            assign(oldOrderInfo, orderInfo)
        self.emit(Event.ON_ORDER, orderInfo)

    def _addTradeReport(self,report:Trade):
        oldReport = self.tradeMap.get(report.trade_id)
        if (not oldReport):
            self.tradeMap[report.trade_id] = report
            self.strategy_trade_list.append(report)
            self.emit(Event.ON_TRADE, report)


