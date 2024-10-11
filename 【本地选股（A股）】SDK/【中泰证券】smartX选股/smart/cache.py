from .type import *
from . import smartc
import json
import logging
logger = logging.getLogger()

'''
 smart提供的账号对象  代表一个资金账号及资产、持仓信息
'''

CMD_SET = "CMD_SET"
CMD_DEL = "CMD_DEL"
CMD_PUSH = "CMD_PUSH"


class Cache(dict):
    def __init__(self):
        super().__init__()

    def set(self,key:str, value, tpl=None):
        cmd = {
            "type": CMD_SET,
            "key": key,
            "value": value
        }
        self.__processCMD(cmd)
        smartc.request("cacheSet", json.dumps(cmd),None)
    
    def delete(self,key:str):
        cmd = {
            "type": CMD_DEL,
            "key": key
        }
        self.__processCMD(cmd)
        smartc.request("cacheDel", json.dumps(cmd),None)

    def push(self,key:str, value):
        cmd = {
            "type": CMD_PUSH,
            "key": key,
            "value": value
        }
        self.__processCMD(cmd)
        smartc.request("cachePush", json.dumps(cmd),None)

    def __processCMD(self,cmd:dict) :
        try:
            topKey = None
            if (cmd.get("type") == CMD_SET) :
                obj = self
                keys = cmd.get("key").split(".")
                size = len(keys)
                topKey = keys[0]
                for i in range(size) :
                    #只有一级属性
                    if (size <= 1) :
                        obj[keys[i]] = cmd.get("value")
                        break
                    elif (i + 2 >= size) : #找到最终一个属性
                        #如果数据结构中不存在则默认创建一个
                        if (not keys[i] in obj) :
                            obj[keys[i]] = {}
                        
                        obj = obj.get(keys[i])
                        obj[keys[i + 1]] = cmd.get("value")
                        break
                    else:
                        #如果数据结构中不存在则默认创建一个
                        if (not keys[i] in obj) :
                            obj[keys[i]] = {}
                        
                        obj = obj.get(keys[i])

                
            elif (cmd.get("type") == CMD_DEL) :
                obj = self
                keys = cmd.get("key").split(".")
                size = len(keys)
                topKey = keys[0]
                for i in range(size) :
                    #只有一级属性
                    if (size <= 1) :
                        obj.pop(keys[i],"")
                        break
                    elif (i + 2 >= size) : #找到最终一个属性
                        obj = obj.get(keys[i])
                        if (obj) :
                            obj.pop(keys[i + 1],"")
                        break
                    else:
                        if (not keys[i] in obj) :
                            break
                        
                    
            elif (cmd.get("type") == CMD_PUSH):
                obj = self
                keys = cmd.get("key").split(".")
                size = len(keys)
                topKey = keys[0]
                for i in range(size) :
                    #只有一级属性
                    if (size <= 1) :
                        target = obj.get(keys[i])
                        if (not target) :
                            target = []
                            obj[keys[i]] = target

                        if (type(target) == list) :
                            target.append(cmd.get("value"))

                        break
                    elif (i + 2 >= size) : #找到最终一个属性
                        #如果数据结构中不存在则默认创建一个
                        if (not keys[i] in obj) :
                            parent = {}
                            obj[keys[i]] = parent
                            parent[keys[i + 1]] = []
                        
                        obj = obj.get(keys[i])
                        target = obj.get(keys[i + 1])
                        if (not target) :
                            target = []
                            obj[keys[i + 1]] = target
                        
                        if (type(target) == list) :
                            target.append(cmd.get("value"))
                        
                        break
                    else:
                        #如果数据结构中不存在则默认创建一个
                        if (not keys[i] in obj) :
                            obj[keys[i]] = {}
                        
                        obj = obj.get(keys[i])
                    
                
            return topKey
        except Exception as err:
            logger.error(err,exc_info=True, stack_info=True)
