
from .account import *
from .type import *
from .algox_strategy_manager import *
from .utils import *

'''
 * 多平台策略管理器，管理所有平台的策略。
 * 各个平台的详细管理逻辑由各自平台的管理器处理，
 * 本类主要为了隐藏各个平台的复杂调用，提供统一接口
'''
class StrategyManager :
    def __init__(self,smart):
        self.managers = {}
        self.managers[StrategyPlatformType.Algo] = AlgoXStrategyManager(self)
        self.context = smart # smart对象
        self.accountManager = None
    

    def getStrategyMap(self,platform_type:str, account:Account,cb) :
        managers = None
        if (platform_type):
            managers = self.managers.get(platform_type)
            if(not managers):
                cb(None)
                return
            else:
                managers = [managers]
        else:
            #all platform
            managers = list(self.managers.values())

        strategyMap = {}
        
        manager = managers.pop()
        def getStrategyMapCallback(tempStrategyMap,err):
            #add strategy
            nonlocal strategyMap
            nonlocal account
            if(tempStrategyMap):assign(strategyMap, tempStrategyMap)
            if(len(managers)>0):
                manager = managers.pop()
                manager.getStrategyMap(account,getStrategyMapCallback)
            else:
                cb(strategyMap)
        manager.getStrategyMap(account,getStrategyMapCallback)

    '''
     * 创建一个权限的策略实例
    '''
    def createInstance(self,account_id:str, platform_type:str, strategy_id:str, config:dict,cb):
        if not account_id:
            account_id = self.context.current_account.account_id
        if not platform_type:
            raise Exception("platform_type required!")
        if not strategy_id:
            raise Exception("strategy_id required!")
        if not config:
            raise Exception("config required!")
        if not cb:
            raise Exception("cb required!")
        manager = self.managers[platform_type]
        if (not manager or not manager.createInstance) :
            cb(None,RspError({"code":RspError.NOT_SUPPORTED}))
            return
        
        def createInstanceCallback(strategy:Strategy,err):
             # 在相关对象中增加绑定关系
            if (strategy):
                account = self.accountManager.getAccountById(account_id)
                strategy.relation_account_map[account_id] = account
                # account.strategy_map[strategy.strategy_id + '_' + platform_type] = strategy
                # self.context.strategy_map[strategy.strategy_id + '_' + platform_type] = strategy
            cb(strategy,err)
        manager.createInstance(account_id, strategy_id, config,createInstanceCallback)

       

    def startStrategy(self,account_id:str, platform_type:str, clent_id:str,cb) :
        if not account_id:
            account_id = self.context.current_account.account_id
        if not platform_type:
            raise Exception("platform_type required!")
        if not clent_id:
            raise Exception("clent_id required")
        if not cb:
            raise Exception("cb required!")
        manager = self.managers[platform_type]
        if (not manager or not manager.startStrategy):
            cb(None,RspError({"code":RspError.NOT_SUPPORTED}))
            return
        manager.startStrategy(account_id, clent_id,cb)


    def initEvent(self):
        # TODO: 魏义 实现如下策略的事件
        # ON_STRATEGY_POSITION_REFRESH_ALL: "on_strategy_position_refresh_all",#某策略持仓变化的全量推送
        # ON_STRATEGY_ASSETS: "on_strategy_assets",#某策略资金的全量推送
        # ON_STRATEGY_UPLOAD_RESULT: "on_strategy_upload_result",#某策略上传结果事件
        # ON_STRATEGY_EXIT_RESULT: "on_strategy_exit_result",#某策略退出结果消息
        # ON_STRATEGY_EXCEPTION: "on_strategy_exception",#某策略运行中的异常消息  如td md断线  程序异常等等
        # ON_STRATEGY_LOG: "on_strategy_log",#某策略log日志发生变化时的增量变化消息
        managers = list(self.managers.values())
        for manager in managers:
            manager.initEvent() 
