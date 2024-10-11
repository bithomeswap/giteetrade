
import os
import sys
import getopt
import logging
from logging import handlers
import json

config ={
        "plugin_id": "",
        "logPath": "",
        "isBacktest": False,
        "btconfig":{}
    }
er = None
try:
    opts, args = getopt.getopt(sys.argv[1:], ":d:f:c:", ["ddebug=","ffile=", "cconfig="])
    print("opts:",opts)
except getopt.GetoptError as err:
    er = err

for opt, arg in opts:
    if opt in ("-c", "--cconfig"):
        config = json.loads(arg)
        break

isBacktest = config.get("isBacktest",False)
closeLog = config.get("btconfig",{}).get("enginConfig",{}).get("close_log",False) if isBacktest else False
p = config.get("logPath","")
plugin_id =  config.get("plugin_id","")
logPath = os.path.join(p,plugin_id)+"py.log" #if not isBacktest else os.path.join(p,plugin_id)+"py_bt.log"

# 创建logger对象
logger = logging.getLogger()

# 设置日志等级
logger.setLevel(logging.DEBUG)

# 向文件输出的日志信息格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(process)d - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')

# 追加写入文件a ，设置utf-8编码防止中文写入乱码
defaultHandler = handlers.TimedRotatingFileHandler(filename=logPath, when='D', backupCount=3, encoding='utf-8')
defaultHandler.setLevel(logging.DEBUG)  # 向文件输出的日志级别
defaultHandler.setFormatter(formatter)

consoleHandler = logging.StreamHandler()  # 往屏幕上输出
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(formatter)

# 加载文件到logger对象中
if not closeLog:
    logger.addHandler(defaultHandler)

#logger.addHandler(defaultHandler)
# logger.addHandler(consoleHandler)
######################LOGGER Core################################
userLogPath = os.path.join(p,plugin_id)+"user_py.log"
# 创建logger对象
userLogger = logging.getLogger("user")

# 设置日志等级
userLogger.setLevel(logging.DEBUG)

# 追加写入文件a ，设置utf-8编码防止中文写入乱码
userHandler = handlers.TimedRotatingFileHandler(filename=userLogPath, when='D', backupCount=3, encoding='utf-8')
userHandler.setLevel(logging.DEBUG)  # 向文件输出的日志级别
userHandler.setFormatter(formatter)

# 加载文件到userLogger对象中
userLogger.addHandler(userHandler)
# userLogger.addHandler(consoleHandler)


logger.debug("initial logging: %s",logPath)
if er:
    logger.error(er,exc_info=True, stack_info=True)