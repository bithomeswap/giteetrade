
from .account import *
from .algox_strategy import *
from .event import *
from .type import *
from . import smartc
from . import utils



'''
 * 算法平台的策略管理器
'''
class AlgoXStrategyManager:
    def __init__(self,rootStrMgr):
        self.rootStrMgr = rootStrMgr
        self.platform_type = StrategyPlatformType.Algo
        self.strategy_map = {}
        self.inited = False
    
    def insertAlgoOrder(self,account_id:str, clent_id:str, config:dict,cb) :
        if not account_id:
            account_id = self.rootStrMgr.context.current_account.account_id
        if not clent_id:
            raise Exception("clent_id required!")
        if not config:
            raise Exception("config required!")
        if not cb:
            raise Exception("cb required!")
        strategy = AlgoXStrategy(self.rootStrMgr.context, clent_id)

        def createCallback(strg,err):
            if(err):
                cb(None,err)
                return
            self.strategy_map[clent_id + "_" + StrategyPlatformType.Algo] = strategy
            smart = self.rootStrMgr.context
            account = smart.account_map.get(account_id)
            account.strategy_map[clent_id + "_" + StrategyPlatformType.Algo] = strategy
            strategy.relation_account_map[account_id] = account

            cb(strategy,None)
        strategy.createStrategy(clent_id, config, createCallback)

    #创建策略，保存到本地
    def createInstance(self,account_id:str, clent_id:str, config:dict,cb) :
        smart = self.rootStrMgr.context
        response = {}
        strategy = AlgoXStrategy(smart, "")
        strategy.clent_id = clent_id
        strategy.status = "XTP_STRATEGY_STATE_CREATED"
        strategy.mxtpStrategyId = ""
        strategy.configdata = config
        if (strategy.configdata) :
            strategy.mclientStrategyId = strategy.configdata.get("clientStrategyId")
            strategy.mstrategyType = strategy.configdata.get("strategyType")
            strategyParam = strategy.configdata.get("strategyParam")
            if strategyParam:
                algoTraDetail = json.loads(strategyParam)
                strategy.data = algoTraDetail
        self.strategy_map[strategy.clent_id + "_" + StrategyPlatformType.Algo] = strategy
        smart = self.rootStrMgr.context
        account = smart.account_map.get(account_id)
        account.strategy_map[strategy.clent_id + "_" + StrategyPlatformType.Algo] = strategy


        response["code"] = 0
        response["data"] = strategy
        smart.emit("createInstanceRes", response)
        cb(strategy,None)


    #启动策略
    def startStrategy(self,account_id:str, clent_id:str,cb) :
        strategy = self.strategy_map.get(clent_id+ "_" + StrategyPlatformType.Algo)
        if (strategy and strategy.createStrategy) :
            def createCallback(stg,err):
                if(err):
                    cb(None,err)
                    return
                smart = self.rootStrMgr.context
                account = smart.account_map.get(account_id)
                strategy.relation_account_map[account_id] = account
                cb(strategy,None)
            strategy.createStrategy(strategy.clent_id, strategy.configdata,createCallback)
        else:
            cb(None,RspError({"code":RspError.NOT_EXIST,"message":"算法单不存在，启动失败"}))
        

    def getStrategyMap(self,account:Account,cb) :
        if(self.inited):
            cb(self.strategy_map,None)
        else:
            def getAlgoStrategiesCallback(rsp:str):
                try:
                    strategyList = decodeRsp(rsp)
                    for it in strategyList :
                        strategy = self._createStrategyFromJson(it)
                        strategy.relation_account_map[account.account_id] = account
                        strategy.account = account
                        self.strategy_map[it.get("mxtpStrategyId") + "_" + StrategyPlatformType.Algo] = strategy
                    self.inited = True
                    cb(self.strategy_map,None)
                except RspError as rspError:
                    logger.error(rspError,exc_info=True, stack_info=True)
                    cb(None,rspError)
            smartc.request("getAlgoStrategies", json.dumps({}), getAlgoStrategiesCallback)

    def _createStrategyFromJson(self,metadata:dict):
        strategy = AlgoXStrategy(self.rootStrMgr.context, metadata.get("mxtpStrategyId") or metadata.get("mclientStrategyId"))
        strategy.status = metadata.get("mstrategyState") or StrategyStatus.Unknown
        strategy.mxtpStrategyId = metadata.get("mxtpStrategyId")
        strategy.mclientStrategyId = metadata.get("mclientStrategyId")
        strategy.mstrategyType = metadata.get("mstrategyType")
        strategy.data = metadata
        return strategy
    

    def initEvent(self):
        #全部推送
        def algoStatusChangeCallback(rsp:str):
            try:
                rsp = json.loads(rsp)
                data = rsp.get("data")
                smart = self.rootStrMgr.context
                mxtpStrategyIdKey = data.get("mxtpStrategyId")+ "_" +  StrategyPlatformType.Algo
                mclientStrategyIdKey =  data.get("mclientStrategyId")+ "_" +  StrategyPlatformType.Algo
                strategy  = self.strategy_map.get(mxtpStrategyIdKey)
                if (data.get("resqtype") == "createStrategyRsp" or data.get("resqtype") == "startStrategyRsp") :
                    if(not strategy):#母单不存在
                        strategy  = self.strategy_map.get(mclientStrategyIdKey)
                        if(strategy):#没有母单编号,根据自定义编号
                            #TODO填充数据
                            self.strategy_map[mxtpStrategyIdKey] = strategy
                            self.strategy_map.pop(mclientStrategyIdKey,"")
                            smart.strategy_map[mxtpStrategyIdKey] = strategy
                            smart.strategy_map.pop(mclientStrategyIdKey,"")
                            #account.strategy_map
                            smart.current_account.strategy_map[mxtpStrategyIdKey] = strategy
                            smart.current_account.strategy_map.pop(mclientStrategyIdKey,"")
                        else:
                            strategy = self._createStrategyFromJson(data)
                            self.strategy_map[mxtpStrategyIdKey] = strategy
                            smart.strategy_map[mxtpStrategyIdKey] = strategy
                            smart.current_account.strategy_map[mxtpStrategyIdKey] = strategy
                        #补充母单编号到strategy_id    
                        strategy.strategy_id = data.get("mxtpStrategyId")

                
                #变更母单状态和数据
                strategy.status = rsp.get("status",StrategyStatus.Unknown )
                strategy.status_name = utils.convertStrategyStatusToChiness(strategy.status)
                #全局派发
                smart.emit(Event.ON_STRATEGY_STATUS_CHANGE, rsp)
                strategy.emit(Event.ON_STRATEGY_STATUS_CHANGE, rsp)
            except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)

        smartc.on("algoStatusChange", algoStatusChangeCallback)