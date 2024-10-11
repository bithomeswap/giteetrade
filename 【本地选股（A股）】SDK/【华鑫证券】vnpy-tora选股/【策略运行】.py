# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
# app = QApplication(sys.argv)
# w = QWidget()
# w.setWindowTitle('Simple')
# btn = QPushButton('Hello PyQt6!', w)
# btn.move(50, 50)
# w.show()
# sys.exit(app.exec())

# pip install --upgrade pip 
# pip install PyQt6 
# # 备份PyQt6目录到其他处：c:\users\kevinqq\.virtualenvs\pyqt6-demo\Lib\site-packages\PyQt6\ 
# pip install pyqt6-tools # 恢复PyQt6到原始目录
# # 如果是使用PySide6，则比较简单：
# pip install pyside6
# # 安装Qt for Python插件，文件栏右键Creat Qt UI File(Designer)创建PYQT的ui文件和py文件
# # 安装依赖sip
# pip3 install sip
# # UI打包库
# pip install pyinstaller auto-py-to-exe 
# # 打包PYQT生成exe文件
# pyinstaller -F -w -i xxx.ico main.py --noconsole



##在windows当中c++版本需要更新到最新版本，也就是在下面这个链接当中【但是还是需要装很多东西因而放弃使用它】
#https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/

#conda remove -n my_env --all #删除没用的版本【base是根目录不可以删除】
#conda remove -n env3.8 --all #删除没用的版本【base是根目录不可以删除】
#conda create -n env3.8 python=3.8 #安装目标版本
#conda activate env3.8 #激活目标版本
#conda deactivate #退出当前环境
#pip install python-dateutil
#pip install vnpy-tora
##conda install -c conda-forge ta-lib #这个包只能在本地下载在服务器下载会报错
#pip install vnpy

# import vnpy
# print(vnpy.__file__)#打印所引用包的位置
# import time
# time.sleep(10)
# # engine包含各种事件函数如下单查询等信息
# # object包含各种对象如各自函数的参数

import dateutil.parser

from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp
from vnpy_tora import (ToraOptionGateway,ToraStockGateway)

from vnpy_tora.gateway.tora_stock_gateway import *

import pandas as pd
import math
import time
import datetime
basepath=r"C:/Users/13480/Desktop/vnpy_tora_华鑫证券/"
#basepath=r"C:/Users/Admin/Desktop/vnpy_tora_华鑫证券/"
def main():
    ##参数设置
    #ACCOUNT_USERID: str="用户代码"
    #ACCOUNT_ACCOUNTID: str="资金账号"
    #ADDRESS_FRONT: str="前置地址"
    #ADDRESS_FENS: str="FENS地址"
    TRADE_TYPE: str="TORASTOCK"
    event_engine=EventEngine()
    main_engine=MainEngine(event_engine)
    main_engine.add_gateway(ToraOptionGateway)
    main_engine.add_gateway(ToraStockGateway)
    
    # qapp=create_qapp() #打开UI界面【pyqt6报错很多没有这个函数好像是因为PYQT库当中把这个用法删掉了但是vnpy框架没有修改】
    # main_window=MainWindow(main_engine,event_engine)
    # main_window.showMaximized()
    # # qapp.exec() #关闭UI界面

    # # 选择是否启动测试网
    # test=False
    test=True
    if test==True:#7*24小时仿真
        marketcil="tcp://210.14.72.16:9402"
        tradecil="tcp://210.14.72.16:9500"
        #tradecil="tcp://210.14.72.15:4400"
    else:#真实仿真
        marketcil="tcp://210.14.72.21:4402"
        tradecil="tcp://210.14.72.21:4400"

    # 选择需要登陆的账号
    # accountid="00043342"
    accountid="00043330"
    # accountid="00041048"
    if accountid=="00043342":
        password="95366378"
    elif accountid=="00043330":
        password="47362325"
    elif accountid=="00041048":
        password="37532450"
        
    # # 是否仅仅执行卖出任务以达到清理仓位的目的而不买入股票【正常应该是Fasle】
    # onlysell=True
    onlysell=False

    maxmoney=2000000#设置最大总下单金额用来计算单股持仓金额的【当前账号余额超过该金额时才会触发】
    targetordernum=50#设置满足交易targetordernum轮次之后如果一直没持仓数据说明确实没有持仓转入买入线程
    main_engine.connect({
            "账号": accountid,
            "密码": password,
            "行情服务器": marketcil,
            "交易服务器": tradecil,
            ##衍生服务器配置【账号密码需要重新申请】
            #"衍生账号": "00041072",
            #"衍生密码": "89925233",
            #"衍生服务器": "101.230.90.99",
            #"衍生端口": 25556,
            "产品标识": "",
            "账号类型": ACCOUNT_USERID,
            "地址类型": ADDRESS_FRONT,
            "UserProductInfo": "HXDQADFEN9",
            "HD": "57PHLV6MS",
        },gateway_name=TRADE_TYPE)

    # 生成日志文件夹
    import os
    now=datetime.datetime.now()
    # now=datetime.datetime.now()-datetime.timedelta(days=1)
    start_date=now.strftime("%Y-%m-%d")#测试当天的数据
    # 验证证券文件夹下是否有日志文件夹
    log_path = f"{basepath}{start_date}"
    if not os.path.exists(log_path):
        # 如果日志文件夹不存在，则创建一个
        os.makedirs(log_path)
        print("已创建日志文件夹")
    else:
        print("日志文件夹已存在")
    # 配置日志
    from loguru import logger # pip install loguru # 这个框架可以解决中文不显示的问题
    logger.add(
        sink=f"{basepath}{start_date}/{accountid}{test}log.log",#sink: 创建日志文件的路径。
        level="INFO",#level: 记录日志的等级，低于这个等级的日志不会被记录。等级顺序为 debug < info < warning < error。设置 INFO 会让 logger.debug 的输出信息不被写入磁盘。
        rotation="00:00",#rotation: 轮换策略，此处代表每天凌晨创建新的日志文件进行日志 IO；也可以通过设置 "2 MB" 来指定 日志文件达到 2 MB 时进行轮换。   
        retention="7 days",#retention: 只保留 7 天。 
        compression="zip",#compression: 日志文件较大时会采用 zip 进行压缩。
        encoding="utf-8",#encoding: 编码方式
        enqueue=True,#enqueue: 队列 IO 模式，此模式下日志 IO 不会影响 python 主进程，建议开启。
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"#format: 定义日志字符串的样式，这个应该都能看懂。
    )
    # logger.remove(handler_id=None)#只输出到磁盘不输出到控制台
    logger.info(f"当前账号{accountid},是否启用测试网{test},main_engine{main_engine}")

    # time.sleep(60)#等待策略引擎彻底启动大概60秒附近
    # allcontracts=pd.DataFrame(main_engine.get_all_contracts())
    # allcontracts.to_csv(f"{basepath}数据备份/allcontracts.csv")

    time.sleep(20)#等待交易引擎启动
    allcontracts=pd.read_csv(f"{basepath}数据备份/allcontracts.csv")
    allcontracts["symbol"]=allcontracts["symbol"].astype(str).str.zfill(6)
    #确认买卖计划
    buydf=pd.read_csv(f"{basepath}数据备份/{start_date}中小板（同花顺）买入.csv")
    buydf["symbol"]=buydf["代码"].astype(str).str.zfill(6)
    selldf=pd.read_csv(f"{basepath}数据备份/{start_date}中小板（同花顺）卖出.csv")
    selldf["symbol"]=selldf["代码"].astype(str).str.zfill(6)
    logger.info(f"{buydf},{selldf}")
    #订阅需要买入的标的
    for thissymbol in buydf["symbol"]:
        logger.info(thissymbol)
        exchange=allcontracts.loc[allcontracts["symbol"]==str(thissymbol),"exchange"].values.tolist()[0].split(".")[1]
        gateway_name=allcontracts.loc[allcontracts["symbol"]==str(thissymbol),"gateway_name"].values.tolist()[0]
        logger.info(f"exchange,{exchange},gateway_name,{gateway_name}")
        main_engine.subscribe(
            req=SubscribeRequest(symbol=str(thissymbol),exchange=Exchange(exchange)),
            gateway_name=str(gateway_name),
        )
    targetnum=5#设置持仓数量
    bidrate=0.003#设置盘口价差为0.003
    timecancellwait=60#设置超过timecancellwait秒自动撤单
    timetickwait=60#设置每次下单时确认是否是最新tick的确认时间
    targetmoney=20000#设置下单时对手盘需要达到的厚度（即单笔目标下单金额，因为手数需要向下取整，所以实际金额比这个值低）
    traderate=2#设置单次挂单金额是targetmoney的traderate倍
    
    cancellorder=True#设置一分钟不成交或者已成交金额达到目标值自动撤单
    # cancellorder=False#设置一分钟不成交或者已成交金额达到目标值自动撤单

    # tradeway="maker"#执行maker方式下单
    tradeway="taker"#执行taker方式下单

    buyorderroad=False#买入进程默认关闭，只有卖出计划结束时才重启
    sellorderroad=False#卖出进程默认关闭，只有卖出计划结束时才重启

    ordernum=0#初始化当前交易轮次为0
    dfaccount=pd.DataFrame({"账号余额":[0],"持仓金额":[0]})#初始化持仓金额【只初始化一次，不要重置】
    dfordercancelled=pd.DataFrame({})#初始化存储已经撤销订单的列表【只初始化一次，不要重置】
    while True:
        time.sleep(1)#休息一秒，避免空转
        dfordersall=pd.DataFrame({})#初始化存储全部订单的列表【每一轮都可以重置】
        logger.info(f"******,订单管理（标准时间）,{datetime.datetime.utcnow()},订单管理（东八区）,{datetime.datetime.utcnow()+datetime.timedelta(hours=8)},当前交易轮次,{ordernum}")
        ordernum+=1
        #撤单管理【尚未完成】
        if ordernum%10==0:
            logger.info(f"交易轮次达标{ordernum}，执行撤单任务")
            #获取所有订单对未完成订单进行处理
            allorderalls=main_engine.get_all_orders()
            for thisorder in allorderalls:
                #logger.info(f"thisorder,{thisorder}")
                thissymbol=str(thisorder.symbol)
                exchange=allcontracts.loc[allcontracts["symbol"]==str(thissymbol),"exchange"].values.tolist()[0].split(".")[1]
                try:
                    if (type(thisorder.datetime)!=str)and((thisorder.datetime)!=None):#只处理既不是空值又不是字符串的情况
                        thisorder.datetime=str(thisorder.datetime.strftime("%Y-%m-%d %H:%M:%S,%f %Z%z"))
                except Exception as e:
                    logger.info(f"******订单时间标准化报错，报错信息{e},thisorder详情{thisorder}")
                thisorderdf=pd.DataFrame([thisorder])
                dfordersall=pd.concat([dfordersall,thisorderdf])
                orderstatus=thisorder.status#获取订单状态
                vt_orderid=thisorder.vt_orderid#获取订单id
                orderprice=thisorder.price#获取下单价格
                ordertraded=thisorder.traded#获取已成交数量
                ordervolume=thisorder.volume#获取总下单数量
                if cancellorder:#如果cancellorder设置为true则执行以下撤单流程【最低撤单金额一万元】
                    ##针对未完全成交的订单进行处理
                    #Status.PARTTRADED：部分成交，Status.ALLTRADED：全部成交  
                    #Status.CANCELLED：已经撤销，拒绝订单
                    if (orderstatus!=Status.ALLTRADED):
                        if (orderstatus!=Status.CANCELLED)and(orderstatus!=Status.REJECTED):
                            logger.info(f"******,不是已成交订单、撤销订单和被拒绝订单,{vt_orderid}")
                            #60秒内不成交就撤单【这个是要小于当前时间，否则就一直无法执行】
                            thisordertime=dateutil.parser.parse(thisorder.datetime).replace(tzinfo=datetime.datetime.utcnow().tzinfo)
                            logger.info(thisordertime)
                            now=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
                            logger.info(f"thisordertime,{thisordertime},{now}处理开始")
                            if thisordertime+datetime.timedelta(seconds=timecancellwait)<now:
                                logger.info(f"******,超时撤单,{vt_orderid},{thissymbol},{ordervolume},{ordertraded}")
                                if (ordertraded*orderprice>targetmoney):
                                    try:
                                        main_engine.cancel_order(thisorder.create_cancel_request(),thisorder.gateway_name)
                                        logger.info(f"******,已成交金额达标执行撤单,{vt_orderid}")
                                    except Exception as e:
                                        logger.info(f"******报错信息{e},已完成或取消中的条件单不允许取消")
                                elif ordertraded==0:#未成交撤单
                                    try:#如果该委托已成交或者已撤单则会报错
                                        main_engine.cancel_order(thisorder.create_cancel_request(),thisorder.gateway_name)
                                        logger.info(f"******,下单后一直未成交执行撤单,{vt_orderid}")
                                    except Exception as e:
                                        logger.info(f"******报错信息{e},已完成或取消中的条件单不允许取消")
                    direction=thisorder.direction
                    if buyorderroad==True:#只在买入线程当中进行撤销订单的余额回补
                        #这里只计算BUY方向的订单
                        if ((direction)==Direction.LONG):
                            if (orderstatus==Status.CANCELLED):
                                cancel_amount=ordervolume-ordertraded
                                logger.info(f"******,撤单成功,{vt_orderid},{thissymbol},{ordervolume},{ordertraded}")
                                if dfordercancelled.empty:#dfordercancelled一开始是个空值，这里主要是确认一下之前有没有数据，有数据才需要检验之前是否撤销过
                                    dfordercancelled=pd.concat([dfordercancelled,thisorderdf],ignore_index=True)
                                    cancel_money=cancel_amount*orderprice#然后就是计算撤销了的订单的未完成金额，加给下单金额当中
                                    moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]+=cancel_money
                                else:
                                    if thisorder.orderid not in dfordercancelled["orderid"].tolist():
                                        dfordercancelled=pd.concat([dfordercancelled,thisorderdf],ignore_index=True)
                                        cancel_money=cancel_amount*orderprice#然后就是计算撤销了的订单的未完成金额，加给下单金额当中
                                        moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]+=cancel_money
                            elif (orderstatus==Status.REJECTED):
                                cancel_amount=ordervolume
                                #logger.info(f"******,废单处理",vt_orderid,thissymbol,ordervolume,ordertraded)
                                if dfordercancelled.empty:#dfordercancelled一开始是个空值，这里主要是确认一下之前有没有数据，有数据才需要检验之前是否撤销过
                                    dfordercancelled=pd.concat([dfordercancelled,thisorderdf],ignore_index=True)
                                    cancel_money=cancel_amount*orderprice#然后就是计算撤销了的订单的未完成金额，加给下单金额当中
                                    moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]+=cancel_money
                                if thisorder.orderid not in dfordercancelled["orderid"].tolist():
                                    dfordercancelled=pd.concat([dfordercancelled,thisorderdf],ignore_index=True)
                                    cancel_money=cancel_amount*orderprice#然后就是计算撤销了的订单的未完成金额，加给下单金额当中
                                    moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]+=cancel_money
            dfordersall.to_csv(f"{basepath}{start_date}/{accountid}{test}___dfordersall.csv")#输出所有未全部成交的订单【针对所有订单】
            dfordercancelled.to_csv(f"{basepath}{start_date}/{accountid}{test}___dfordercancelled.csv")#输出已经撤销或者作废的订单【只针对的买入订单】
        #获取账号详情
        account=main_engine.get_account(f"{TRADE_TYPE}.{accountid}")
        logger.info(f"account,{account}")
        if not hasattr(account, "balance"):
            logger.info(f"等待账户数据") 
        else:#只有引擎已经启动并且account对象具有balance属性的时候才执行下一步
            accountbalance=account.balance
            logger.info(f"资金余额,{accountbalance}")
            dfaccount["账号余额"]=accountbalance
            #获取所有订阅标的的tick
            dfallticks=pd.DataFrame({})
            allticks=main_engine.get_all_ticks()
            for tick in allticks: #五档买入参数准备
                thissymbol=str(tick.symbol)
                exchange=allcontracts.loc[allcontracts["symbol"]==str(thissymbol),"exchange"].values.tolist()[0].split(".")[1]
                if (type(tick.datetime)!=str):#将时间类型不是字符串的tcik数据进行处理
                    tick.datetime=tick.datetime.strftime("%Y-%m-%d %H:%M:%S,%f %Z%z")
                thistickdf=pd.DataFrame([tick])
                dfallticks=pd.concat([dfallticks,thistickdf])
            if dfallticks.empty:
                logger.info(f"等待tick数据")
            else:#只针对dfallticks不为空的情况进行处理
                dfallticks["wap_price"]=(dfallticks["bid_price_1"]*dfallticks["bid_volume_1"]+dfallticks["ask_price_1"]*dfallticks["ask_volume_1"])/(dfallticks["bid_volume_1"] + dfallticks["ask_volume_1"])
                #获取持仓详情
                dfallpositions=pd.DataFrame({})
                allpositions=pd.DataFrame(main_engine.get_all_positions())
                sellsymbol=[]
                nostocks=0#验证是否有持仓标的的tick没有获取成功
                if (allpositions.empty):
                    logger.info(f"allpositions为空值等待数据获取{allpositions}")
                    if(ordernum>targetordernum):
                        sellorderroad=True
                        logger.info(f"持仓为空值,但是交易轮次达到{ordernum}轮{sellorderroad}")
                else:#只有引擎已经启动并且有返回值的时候才执行
                    logger.info(f"allpositions不为空值执行卖出确认{allpositions}")
                    for thisposition in allpositions.iterrows():
                        thisposition=thisposition[1]
                        thissymbol=thisposition.symbol
                        exchange=allcontracts.loc[allcontracts["symbol"]==str(thissymbol),"exchange"].values.tolist()[0].split(".")[1]
                        gateway_name=allcontracts.loc[allcontracts["symbol"]==str(thissymbol),"gateway_name"].values.tolist()[0]
                        #订阅已经持仓的标的
                        main_engine.subscribe(
                            req=SubscribeRequest(symbol=str(thissymbol),exchange=Exchange(exchange)),
                            gateway_name=str(gateway_name),
                        )
                        if (thissymbol not in dfallticks["symbol"].tolist()):
                            nostocks+=1
                        if (thissymbol in dfallticks["symbol"].tolist()):#需要订阅这个标的成功并且返回tick之后才能执行
                            logger.info(f"{thissymbol}已经订阅可以执行")
                            #拼接持仓详情
                            positionprice=dfallticks[dfallticks["symbol"]==str(thissymbol)]["wap_price"].values[0]
                            thispositiondf=pd.DataFrame(thisposition).T
                            thispositiondf["wap_price"]=positionprice
                            logger.info(f"thispositiondf,{thispositiondf},volume,{thisposition.volume}")
                            if thisposition.volume>0:#持仓数量大于0
                                dfallpositions=pd.concat([dfallpositions,thispositiondf])
                                dfallpositions["positionmoney"]=dfallpositions["volume"]*dfallpositions["wap_price"]
                                allpositionmoney=dfallpositions["positionmoney"].sum()
                                dfaccount["持仓金额"]=allpositionmoney
                                logger.info(f"{thissymbol}持仓数量大于0")
                                if (buyorderroad==False):#只在非买入线程执行卖出计划
                                    logger.info(f"{thissymbol}正在执行卖出线程")
                                    if (thissymbol not in selldf["symbol"].tolist()):#确认是否有应卖出未卖出标的
                                        sellsymbol.append(thissymbol)
                                        logger.info(f"待卖出标的,{thissymbol},所有待卖出标的,{sellsymbol}")
                                        #volume总数量frozen冻结数量yd_volume昨日持仓数量
                                        available_amount=thisposition.yd_volume-thisposition.frozen
                                        if available_amount>0:#【可卖出数量大于0】昨日持仓数量减去当前冻结数量大于0
                                            logger.info(f"{thissymbol}昨日持仓数量减去当前冻结数量大于0")
                                            if thissymbol in dfallticks["symbol"].tolist():
                                                selltick=dfallticks[dfallticks["symbol"]==str(thissymbol)]
                                                logger.info(f"{thissymbol}已经订阅可以进行处理{selltick}")
                                                ask_price_1=selltick["ask_price_1"].values[0]
                                                ask_volume_1=selltick["ask_volume_1"].values[0]
                                                bid_price_1=selltick["bid_price_1"].values[0]
                                                bid_volume_1=selltick["bid_volume_1"].values[0]
                                                logger.info(f"卖出准备,{exchange},{gateway_name},{ask_price_1},{ask_volume_1},{bid_price_1},{bid_volume_1}")
                                                #对ticktime的时区进行处理
                                                ticktime=dateutil.parser.parse(selltick["datetime"].values[0]).replace(tzinfo=datetime.datetime.utcnow().tzinfo)
                                                now=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
                                                logger.info(f"ticktime,{ticktime}{type(ticktime)},{now}处理开始")
                                                if ticktime+datetime.timedelta(seconds=timetickwait)>now:
                                                    logger.info(f"ticktime较近适宜下单")
                                                    if ((thissymbol.startswith("12")) or (thissymbol.startswith("11"))):#针对11开头或者12开头的转债单独处理
                                                        logger.info(f"******,可转债策略")
                                                        if (ask_price_1-bid_price_1)<=(((ask_price_1+bid_price_1)/2)*bidrate):#盘口价差
                                                            logger.info(f"******,盘口价差适宜，适合执行交易")
                                                            if tradeway=="maker":
                                                                if (available_amount*ask_price_1)<(traderate*targetmoney):
                                                                    logger.info(f"******,剩余全部卖出")
                                                                    sellvolume=(math.floor(available_amount/10))*10
                                                                    sellorder=main_engine.send_order(req=OrderRequest(
                                                                            symbol=thissymbol,
                                                                            exchange=Exchange(exchange),
                                                                            direction=Direction.SHORT, #卖出
                                                                            type=OrderType.LIMIT, #限价单
                                                                            volume=sellvolume,
                                                                            price=ask_price_1,
                                                                            #reference=f"strategy_测试"
                                                                            ),
                                                                            gateway_name=str(gateway_name))#下单
                                                                    logger.info(sellorder)
                                                                else:#限价卖出最小下单金额
                                                                    logger.info(f"******,卖出目标金额")
                                                                    sellvolume=(math.floor(((targetmoney/ask_price_1))/10))*10
                                                                    if (available_amount*ask_price_1)>500000:#针对余额高于500000的标的单独扩大下单数量
                                                                        sellvolume*=10
                                                                    sellorder=main_engine.send_order(req=OrderRequest(
                                                                            symbol=thissymbol,
                                                                            exchange=Exchange(exchange),
                                                                            direction=Direction.SHORT, #卖出
                                                                            type=OrderType.LIMIT, #限价单
                                                                            volume=sellvolume,
                                                                            price=ask_price_1,
                                                                            #reference=f"strategy_测试"
                                                                            ),
                                                                            gateway_name=str(gateway_name))#下单
                                                                    logger.info(sellorder)
                                                            if tradeway=="taker":
                                                                if (bid_price_1*bid_volume_1)>targetmoney:#盘口深度【对手盘一档买入】                                            
                                                                    if (available_amount*bid_price_1)<(traderate*targetmoney):
                                                                        logger.info(f"******,剩余全部卖出")
                                                                        sellvolume=(math.floor(available_amount/10))*10
                                                                        sellorder=main_engine.send_order(req=OrderRequest(
                                                                            symbol=thissymbol,
                                                                            exchange=Exchange(exchange),
                                                                            direction=Direction.SHORT, #卖出
                                                                            type=OrderType.LIMIT, #限价单
                                                                            volume=sellvolume,
                                                                            price=bid_price_1,
                                                                            #reference=f"strategy_测试"#这个是区分具体使用的哪个策略
                                                                            ),
                                                                            gateway_name=str(gateway_name))#下单
                                                                        logger.info(sellorder)
                                                                    else:#限价卖出最小下单金额
                                                                        logger.info(f"******,卖出目标金额")
                                                                        sellvolume=(math.floor((targetmoney/bid_price_1)/10))*10
                                                                        if (available_amount*bid_price_1)>500000:#针对余额高于500000的标的单独扩大下单数量
                                                                            sellvolume*=10
                                                                        sellorder=main_engine.send_order(req=OrderRequest(
                                                                            symbol=thissymbol,
                                                                            exchange=Exchange(exchange),
                                                                            direction=Direction.SHORT, #卖出
                                                                            type=OrderType.LIMIT, #限价单
                                                                            volume=sellvolume,
                                                                            price=bid_price_1,
                                                                            #reference=f"strategy_测试"#这个是区分具体使用的哪个策略
                                                                            ),
                                                                            gateway_name=str(gateway_name))#下单
                                                                        logger.info(f"{sellorder}")
                                                    else:
                                                        logger.info(f"******,个股策略")
                                                        if (ask_price_1-bid_price_1)<=(((ask_price_1+bid_price_1)/2)*bidrate):#盘口价差
                                                            logger.info(f"******,盘口价差适宜，适合执行交易")
                                                            if tradeway=="maker":
                                                                if (available_amount*ask_price_1)<(traderate*targetmoney):
                                                                    logger.info(f"******,剩余全部卖出")
                                                                    sellvolume=(math.floor(available_amount/100))*100
                                                                    sellorder=main_engine.send_order(req=OrderRequest(
                                                                            symbol=thissymbol,
                                                                            exchange=Exchange(exchange),
                                                                            direction=Direction.SHORT, #卖出
                                                                            type=OrderType.LIMIT, #限价单
                                                                            volume=sellvolume,
                                                                            price=ask_price_1,
                                                                            #reference=f"strategy_测试"
                                                                            ),
                                                                            gateway_name=str(gateway_name))#下单
                                                                    logger.info(sellorder)
                                                                else:#限价卖出最小下单金额
                                                                    logger.info(f"******,卖出目标金额")
                                                                    sellvolume=(math.floor(((targetmoney/ask_price_1))/100))*100
                                                                    if (available_amount*ask_price_1)>500000:#针对余额高于500000的标的单独扩大下单数量
                                                                        sellvolume*=10
                                                                    sellorder=main_engine.send_order(req=OrderRequest(
                                                                            symbol=thissymbol,
                                                                            exchange=Exchange(exchange),
                                                                            direction=Direction.SHORT, #卖出
                                                                            type=OrderType.LIMIT, #限价单
                                                                            volume=sellvolume,
                                                                            price=ask_price_1,
                                                                            #reference=f"strategy_测试"
                                                                            ),
                                                                            gateway_name=str(gateway_name))#下单
                                                                    logger.info(sellorder)
                                                            if tradeway=="taker":
                                                                if (bid_price_1*bid_volume_1)>targetmoney:#盘口深度【对手盘一档买入】                                            
                                                                    if (available_amount*bid_price_1)<(traderate*targetmoney):
                                                                        logger.info(f"******,剩余全部卖出")
                                                                        sellvolume=(math.floor(available_amount/100))*100
                                                                        sellorder=main_engine.send_order(req=OrderRequest(
                                                                            symbol=thissymbol,
                                                                            exchange=Exchange(exchange),
                                                                            direction=Direction.SHORT, #卖出
                                                                            type=OrderType.LIMIT, #限价单
                                                                            volume=sellvolume,
                                                                            price=bid_price_1,
                                                                            #reference=f"strategy_测试"#这个是区分具体使用的哪个策略
                                                                            ),
                                                                            gateway_name=str(gateway_name))#下单
                                                                        logger.info(sellorder)
                                                                    else:#限价卖出最小下单金额
                                                                        logger.info(f"******,卖出目标金额")
                                                                        sellvolume=(math.floor((targetmoney/bid_price_1)/100))*100
                                                                        if (available_amount*bid_price_1)>500000:#针对余额高于500000的标的单独扩大下单数量
                                                                            sellvolume*=10
                                                                        sellorder=main_engine.send_order(req=OrderRequest(
                                                                            symbol=thissymbol,
                                                                            exchange=Exchange(exchange),
                                                                            direction=Direction.SHORT, #卖出
                                                                            type=OrderType.LIMIT, #限价单
                                                                            volume=sellvolume,
                                                                            price=bid_price_1,
                                                                            #reference=f"strategy_测试"#这个是区分具体使用的哪个策略
                                                                            ),
                                                                            gateway_name=str(gateway_name))#下单
                                                                        logger.info(f"{sellorder}")
                        sellorderroad=True
                        logger.info(f"持仓不为空值,等待应卖出持仓卖出{ordernum}轮{sellorderroad}")
                if sellorderroad==True:#交易轮次数ordernum大于200才进行金额重置
                    dfallpositions.to_csv(f"{basepath}{start_date}/{accountid}{test}___dfallpositions.csv")
                    dfallticks.to_csv(f"{basepath}{start_date}/{accountid}{test}___dfallticks.csv")
                    dfaccount.to_csv(f"{basepath}{start_date}/{accountid}{test}___dfaccount.csv")
                    if (len(sellsymbol)==0) and (buyorderroad==False):#没有需要卖出的标的才执行，并且只能在刚刚由卖出线程转换成买入线程的时候使用
                        logger.info(f"没有需要卖出的标的计算交易金额")
                        if nostocks==0:
                            logger.info(f"所有持仓标的均已经订阅")
                            buyorderroad=True#启动买入计划
                            initmoney=dfaccount["账号余额"].values[0]+dfaccount["持仓金额"].values[0] #设置主账号初始仓位（一百万）
                            if initmoney>maxmoney:
                                initmoney=maxmoney
                                logger.info(f"initmoney金额过高重置为{initmoney}")
                            premoney=initmoney/targetnum
                            buydf["moneymanage"]=premoney
                            moneymanage=buydf[["symbol", "moneymanage"]]
                            if dfallpositions.empty:
                                logger.info(f"第一次建仓无需重置金额")
                            else:
                                logger.info(f"已有持仓需调整下单金额")
                                if (targetnum-len(dfallpositions)>=0):
                                    moneymanage=moneymanage[~moneymanage["symbol"].isin(dfallpositions["symbol"].tolist())] #重置之前需要把在卖出selldf中的标的在moneymanage当中去掉
                                    moneymanage=moneymanage[:(targetnum-len(dfallpositions))] #这里减去的是持仓股票数量，然后在持仓标的中选择金额不足的向上拼接                                    
                                    logger.info(f"卖出计划结束，已根据持仓情况调整下单计划,{moneymanage}")
                                    for thispostion in dfallpositions.iterrows():
                                        thispostion=thispostion[1]
                                        thissymbol=thispostion.symbol
                                        logger.info(f"针对持仓状态对下单金额进行调整{thispostion.symbol},thisposition,{thisposition},thisposition.volume{thisposition.volume},{type(thisposition.volume)}")
                                        if float(thisposition.volume)>0:
                                            positionmoney=dfallpositions[dfallpositions["symbol"]==str(thissymbol)]["positionmoney"].iloc[0]
                                            logger.info(f"有持仓需要调整,{thissymbol},thisposition,{thisposition},positionmoney,{positionmoney}")
                                            if thissymbol not in moneymanage["symbol"].tolist():
                                                newdata=pd.DataFrame([{"symbol":str(thissymbol),"moneymanage":(premoney-positionmoney)}])
                                                moneymanage=pd.concat([moneymanage,newdata],ignore_index=True)
                                                logger.info(f"******,拼接上之前应买入未买全的股票，之后最新的下单金额计划,{moneymanage}")
                                            elif thissymbol in moneymanage["symbol"].tolist():
                                                moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]=(premoney-positionmoney)
                                                logger.info(f"******,更新完之前应买入未买全的股票，之后最新的下单金额计划,{moneymanage}")
                                else:#持仓数量大于等于目标数量【直接对持仓标的当中金额不足的进行处理】
                                    logger.info(f"******,持仓数量超过目标数量无法重置金额请尽快处理")
                            moneymanage["目标金额"]=moneymanage["moneymanage"].copy()
                            logger.info(f"moneymanage,{moneymanage}")
                            ##根据可用资金比例，重新设置单股下单金额【目的是想把剩余资金利用起来】
                            #available_cash=dfaccount["账号余额"].values[0]
                            #turnrate=available_cash/(moneymanage["moneymanage"].sum())
                            #logger.info(available_cash,moneymanage["moneymanage"].sum())
                            #moneymanage["moneymanage"]=moneymanage["moneymanage"]*turnrate
                            #logger.info(f"调整比例,{turnrate},处理后,{moneymanage}")
                if (buyorderroad):#如果持仓真的是空值的话就直接下单【不过需要小心引擎刚启动数据还没过来的情况】
                    if onlysell==True:
                        logger.info(f"清理仓位任务已经完成")
                        break
                    moneymanage.to_csv(f"{basepath}{start_date}/{accountid}{test}___moneymanage.csv")
                    logger.info(f"买入准备,buyorderroad,{buyorderroad}")
                    for thissymbol in moneymanage["symbol"].tolist():#如果恰好是三十只以上股票，且没有需要卖出的股票时，moneymanage为空会导致报错
                        logger.info(f"待买入标的,{thissymbol}")
                        buymoney=moneymanage[moneymanage["symbol"]==str(thissymbol)]["moneymanage"].iloc[0]
                        if buymoney>targetmoney:#只针对待买入金额超过targetmoney的标的进行买入，否则直接掠过
                            #重置并获取资产信息
                            account=main_engine.get_account(f"{TRADE_TYPE}.{accountid}")
                            logger.info(f"account,{account}")
                            if hasattr(account, "balance"):#只有引擎已经启动并且有返回值的时候才执行
                                portfolio_available_cash=account.balance
                                logger.info(f"当前余额,{portfolio_available_cash},{type(portfolio_available_cash)}")
                                if portfolio_available_cash>targetmoney:#余额大于targetmoney才执行下单
                                    if buymoney>targetmoney:#应买入金额大于单笔交易金额时执行买入计划
                                        exchange=allcontracts.loc[allcontracts["symbol"]==str(thissymbol),"exchange"].values.tolist()[0].split(".")[1]
                                        gateway_name=allcontracts.loc[allcontracts["symbol"]==str(thissymbol),"gateway_name"].values.tolist()[0]
                                        buytick=dfallticks[dfallticks["symbol"]==str(thissymbol)]
                                        ask_price_1=buytick["ask_price_1"].values[0]
                                        ask_volume_1=buytick["ask_volume_1"].values[0]
                                        bid_price_1=buytick["bid_price_1"].values[0]
                                        bid_volume_1=buytick["bid_volume_1"].values[0]
                                        logger.info(f"买入准备,{exchange},{gateway_name},{ask_price_1},{ask_volume_1},{bid_price_1},{bid_volume_1}")
                                        ticktime=dateutil.parser.parse(buytick["datetime"].values[0]).replace(tzinfo=datetime.datetime.utcnow().tzinfo)
                                        now=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
                                        logger.info(f"ticktime,{ticktime}{type(ticktime)},{now}处理开始")
                                        if ticktime+datetime.timedelta(seconds=timetickwait)>now:
                                            logger.info(f"ticktime较近适宜下单")
                                            if ((thissymbol.startswith("12")) or (thissymbol.startswith("11"))):#针对11开头或者12开头的转债单独处理
                                                logger.info(f"******,可转债策略")
                                                if (ask_price_1-bid_price_1)<=(((ask_price_1+bid_price_1)/2)*bidrate):#盘口价差
                                                    logger.info(f"******,盘口价差适宜，适合执行交易")
                                                    if tradeway=="maker":#maker下单【不需要考虑深度问题】
                                                        if buymoney<(traderate*targetmoney):
                                                            logger.info(f"******,剩余全部买入")
                                                            buyvolume=(math.floor((buymoney/bid_price_1)/10))*10
                                                            buyorder=main_engine.send_order(req=OrderRequest(
                                                                symbol=thissymbol,
                                                                exchange=Exchange(exchange),
                                                                direction=Direction.LONG, #多头
                                                                type=OrderType.LIMIT, #限价单
                                                                volume=buyvolume,
                                                                price=bid_price_1,
                                                                #reference=f"strategy_测试"#这个是区分具体使用的哪个策略
                                                                ),
                                                                gateway_name=str(gateway_name))#下单
                                                            logger.info(buyorder)
                                                            bidmoney=float(bid_price_1)*buyvolume
                                                            moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]-=bidmoney
                                                        else:
                                                            logger.info(f"******,买入目标金额")
                                                            buyvolume=(math.floor((targetmoney/bid_price_1)/10))*10
                                                            if buymoney>500000:#针对总下单余额高于500000的标的单独扩大下单数量
                                                                buyvolume*=10
                                                            buyorder=main_engine.send_order(req=OrderRequest(
                                                                symbol=thissymbol,
                                                                exchange=Exchange(exchange),
                                                                direction=Direction.LONG, #多头
                                                                type=OrderType.LIMIT, #限价单
                                                                volume=buyvolume,
                                                                price=bid_price_1,
                                                                # reference=f"strategy_测试"#这个是区分具体使用的哪个策略
                                                                ),
                                                                gateway_name=str(gateway_name))#下单
                                                            logger.info(buyorder)
                                                            bidmoney=float(bid_price_1)*buyvolume
                                                            moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]-=bidmoney
                                                    if tradeway=="taker":#taker下单【跟其他地方一样需要考虑深度】
                                                        if (ask_price_1*ask_volume_1)>targetmoney:#盘口深度【对手盘一档买入】
                                                            if buymoney<(traderate*targetmoney):
                                                                logger.info(f"******,剩余全部买入")
                                                                buyvolume=(math.floor((buymoney/ask_price_1)/10))*10
                                                                buyorder=main_engine.send_order(req=OrderRequest(
                                                                    symbol=thissymbol,
                                                                    exchange=Exchange(exchange),
                                                                    direction=Direction.LONG, #多头
                                                                    type=OrderType.LIMIT, #限价单
                                                                    volume=buyvolume,
                                                                    price=ask_price_1,
                                                                    # reference=f"strategy_测试"#这个是区分具体使用的哪个策略
                                                                    ),
                                                                    gateway_name=str(gateway_name))#下单
                                                                logger.info(buyorder)
                                                                bidmoney=float(ask_price_1)*buyvolume
                                                                moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]-=bidmoney
                                                            else:
                                                                logger.info(f"******,买入目标金额")
                                                                buyvolume=(math.floor((targetmoney/ask_price_1)/10))*10
                                                                if buymoney>500000:#针对总下单余额高于500000的标的单独扩大下单数量
                                                                    buyvolume*=10
                                                                buyorder=main_engine.send_order(req=OrderRequest(
                                                                    symbol=thissymbol,
                                                                    exchange=Exchange(exchange),
                                                                    direction=Direction.LONG, #多头
                                                                    type=OrderType.LIMIT, #限价单
                                                                    volume=buyvolume,
                                                                    price=ask_price_1,
                                                                    # reference=f"strategy_测试"#这个是区分具体使用的哪个策略
                                                                    ),
                                                                    gateway_name=str(gateway_name))#下单
                                                                logger.info(buyorder)
                                                                bidmoney=float(ask_price_1)*buyvolume
                                                                moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]-=bidmoney
                                            else:
                                                logger.info(f"******,个股策略")
                                                if (ask_price_1-bid_price_1)<=(((ask_price_1+bid_price_1)/2)*bidrate):#盘口价差
                                                    logger.info(f"******,盘口价差适宜，适合执行交易")
                                                    if tradeway=="maker":#maker下单【不需要考虑深度问题】
                                                        if buymoney<(traderate*targetmoney):
                                                            logger.info(f"******,剩余全部买入")
                                                            buyvolume=(math.floor((buymoney/bid_price_1)/100))*100
                                                            buyorder=main_engine.send_order(req=OrderRequest(
                                                                symbol=thissymbol,
                                                                exchange=Exchange(exchange),
                                                                direction=Direction.LONG, #多头
                                                                type=OrderType.LIMIT, #限价单
                                                                volume=buyvolume,
                                                                price=bid_price_1,
                                                                #reference=f"strategy_测试"#这个是区分具体使用的哪个策略
                                                                ),
                                                                gateway_name=str(gateway_name))#下单
                                                            logger.info(buyorder)
                                                            bidmoney=float(bid_price_1)*buyvolume
                                                            moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]-=bidmoney
                                                        else:
                                                            logger.info(f"******,买入目标金额")
                                                            buyvolume=(math.floor((targetmoney/bid_price_1)/100))*100
                                                            if buymoney>500000:#针对总下单余额高于500000的标的单独扩大下单数量
                                                                buyvolume*=10
                                                            buyorder=main_engine.send_order(req=OrderRequest(
                                                                symbol=thissymbol,
                                                                exchange=Exchange(exchange),
                                                                direction=Direction.LONG, #多头
                                                                type=OrderType.LIMIT, #限价单
                                                                volume=buyvolume,
                                                                price=bid_price_1,
                                                                # reference=f"strategy_测试"#这个是区分具体使用的哪个策略
                                                                ),
                                                                gateway_name=str(gateway_name))#下单
                                                            logger.info(buyorder)
                                                            bidmoney=float(bid_price_1)*buyvolume
                                                            moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]-=bidmoney
                                                    if tradeway=="taker":#taker下单【跟其他地方一样需要考虑深度】
                                                        if (ask_price_1*ask_volume_1)>targetmoney:#盘口深度【对手盘一档买入】
                                                            if buymoney<(traderate*targetmoney):
                                                                logger.info(f"******,剩余全部买入")
                                                                buyvolume=(math.floor((buymoney/ask_price_1)/100))*100
                                                                buyorder=main_engine.send_order(req=OrderRequest(
                                                                    symbol=thissymbol,
                                                                    exchange=Exchange(exchange),
                                                                    direction=Direction.LONG, #多头
                                                                    type=OrderType.LIMIT, #限价单
                                                                    volume=buyvolume,
                                                                    price=ask_price_1,
                                                                    # reference=f"strategy_测试"#这个是区分具体使用的哪个策略
                                                                    ),
                                                                    gateway_name=str(gateway_name))#下单
                                                                logger.info(buyorder)
                                                                bidmoney=float(ask_price_1)*buyvolume
                                                                moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]-=bidmoney
                                                            else:
                                                                logger.info(f"******,买入目标金额")
                                                                buyvolume=(math.floor((targetmoney/ask_price_1)/100))*100
                                                                if buymoney>500000:#针对总下单余额高于500000的标的单独扩大下单数量
                                                                    buyvolume*=10
                                                                buyorder=main_engine.send_order(req=OrderRequest(
                                                                    symbol=thissymbol,
                                                                    exchange=Exchange(exchange),
                                                                    direction=Direction.LONG, #多头
                                                                    type=OrderType.LIMIT, #限价单
                                                                    volume=buyvolume,
                                                                    price=ask_price_1,
                                                                    # reference=f"strategy_测试"#这个是区分具体使用的哪个策略
                                                                    ),
                                                                    gateway_name=str(gateway_name))#下单
                                                                logger.info(buyorder)
                                                                bidmoney=float(ask_price_1)*buyvolume
                                                                moneymanage.loc[moneymanage["symbol"]==str(thissymbol),"moneymanage"]-=bidmoney
                #打印当前的持仓状态
                if not dfallpositions.empty:
                    positionsymbols=dfallpositions["symbol"].tolist()
                    selldflist=selldf["symbol"].tolist()
                    buydflist=buydf["symbol"].tolist()
                    falsesymbol=[x for x in positionsymbols if x not in selldflist]
                    truesymbol=[x for x in positionsymbols if x in selldflist]
                    havesymbol=[x for x in buydflist if x in positionsymbols]
                    nohavesymbol=[x for x in buydflist if x not in positionsymbols]
                    logger.info(f"******,应卖出标的,{falsesymbol},应买入标的,{nohavesymbol},持仓标的,{positionsymbols}")
if __name__=="__main__":
    main()