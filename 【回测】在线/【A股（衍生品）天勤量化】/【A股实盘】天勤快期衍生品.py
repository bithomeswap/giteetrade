# #!/usr/bin/env python
# #  -*- coding: utf-8 -*-
# #安装对应的python环境【3.10】
# conda create -n my_env python=3.10
# #激活安装的python环境
# conda activate my_env
# #vscode自带的python插件需要删掉并且限制使用否则会干扰代码
# #快期下载地址
# pip install tqsdk -U
# #国内镜像地址
# pip install tqsdk -U -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host=pypi.tuna.tsinghua.edu.cn
import pandas as pd
import time
import datetime
import math
__author__='chengzhi'
from tqsdk import TqApi,TqAuth,TqAccount,TargetPosTask
# 登录账号
api=TqApi(debug="debug.log",auth=TqAuth("19511189162","wth000"))
# newapi=api.copy()#创建该账户的副本在其他线程当中使用【用来做一个账户的多线程处理】


# 【天勤衍生品实盘（真格量化回测）】
# 期期套利、合成期权套利的回测和实盘。
# 天勤在回测的时候没法获取当当时中金所所有标的的详情。
# 实盘可以走天勤掌控度还高一些。
# 回测尽量在真格数据还全乎，选择期货期权回测，init函数里面分别登录期权和期货，初始金额相同，然后根据总金额计算的收益率。


# 【计算期权的卖方保证金】
# 根据输入的ETF期权来查询该期权的交易所规则下的理论卖方保证金，实际情况请以期货公司收取的一手保证金为准
def option_margin(symbol):
    quote_option = api.get_quote(symbol)#quote_option.strike_price表示行权价
    print(quote_option)
    # 判断期权标的是不是ETF
    if quote_option.option_class == "CALL":
        # 认购期权虚值＝Max（行权价-合约标的前收盘价，0）
        call_out_value = max(quote_option.strike_price- quote_option.underlying_quote.pre_close, 0)
        # 认购期权义务仓开仓保证金＝[合约前结算价+Max（12%×合约标的前收盘价-认购期权虚值，7%×合约标的前收盘价）]×合约单位
        call_margin = (quote_option.pre_settlement + max(
            0.12*quote_option.underlying_quote.pre_close-call_out_value,
            0.07*quote_option.underlying_quote.pre_close
            )) * quote_option.volume_multiple
        return round(call_margin, 2)
    elif quote_option.option_class == "PUT":
        # 认沽期权虚值＝Max（合约标的前收盘价-行权价，0）
        put_out_value = max(quote_option.underlying_quote.pre_close- quote_option.strike_price, 0)
        # 认沽期权义务仓开仓保证金＝Min[合约前结算价+Max（12%×合约标的前收盘价-认沽期权虚值，7%×行权价），行权价]×合约单位。
        put_margin = min(quote_option.pre_settlement + max(
            0.12 * quote_option.underlying_quote.pre_close- put_out_value,
            0.07 * quote_option.strike_price),quote_option.strike_price) * quote_option.volume_multiple
        return round(put_margin, 2)
    else:
        print("输入的不是ETF期权合约")
        return None

# #直接手写多合约
# 合约0 = 'SHFE.rb2005'
# 合约1 = 'SHFE.rb2101'
# 合约2 = 'SHFE.rb2002'
# 合约3 = 'SHFE.rb2003'
# 合约4 = 'SHFE.rb2004'
# 合约5 = 'SHFE.rb2005'
# 合约6 = 'SHFE.rb2006'
# 合约7 = 'SHFE.rb2007'
# 合约8 = 'SHFE.rb2008'
# 合约9 = 'SHFE.rb2009'
# 合约10 = 'SHFE.rb2010'
# 合约11 = 'SHFE.rb2011'
# 合约12 = 'SHFE.rb2012'
##选择回测模式还是实盘模式
target="回测"
# target="实盘"
# target="测试"
if target=="回测":#每天只能回测两次【能在回测当中打开的网站上看到收益曲线·】
        #2017年以前的数据是空的
        from datetime import date
        from tqsdk import TqApi,TqAuth,TqBacktest,TargetPosTask,TqSim
        # 在创建 api 实例时传入 TqBacktest 就会进入回测模式,设置web_gui=True开启图形化界面
        from tqsdk import BacktestFinished
        account=TqSim(init_balance=100000)
    # try:
        api=TqApi(account,#在外部设置初始资金
            backtest=TqBacktest(
            start_dt=date(2019,5,2),
            end_dt=date(2019,6,2)),
            # web_gui=True,
            # web_gui="http://192.168.0.123:9876",#固定到本机id端口查看回测记录
            web_gui="http://192.168.10.20:9876",#固定到本机id端口查看回测记录【家庭】
            auth=TqAuth("19511189162","wth000")
            )

        # 多次出现 RuntimeError: Event loop is closed 和 no running event loop 错误。
        # 这通常发生在异步编程中，当事件循环被关闭后，仍有任务尝试执行。
        # 您需要确保在正确的事件循环中执行异步任务。
        ##[价差策略]rb\id等在这里可以通过for循环遍历多个合约



        #另外期货衍生品还有一个涨跌停板制度，回测的时候需要避开涨跌停板，避免无法交易
        #期货期权数据的返回值均为空，尽量在盘前梳理标的情况，然后盘中逐个获取



        qrb_1910 = api.get_quote("SHFE.rb1910")# 订阅近月合约盘口行情（一档）
        rb_1910 = TargetPosTask(api, "SHFE.rb1910")#针对某个合约的自动调仓工具【交易辅助工具】（暂不支持个股）
        qrb_2001 = api.get_quote("SHFE.rb2001")# 订阅远月合约盘口行情（一档）
        rb_2001 = TargetPosTask(api, "SHFE.rb2001")#针对某个合约的自动调仓工具【交易辅助工具】（暂不支持个股）
        
        #账户详情
        account=api.get_account() # 获得资金账户引用，当账户有变化时 account 中的字段会对应更新
        #获取单标的持仓
        position=api.get_position(symbol="CFFEX.IH2402",)
        while True:#下单的单位上这个手尽量换成总资产的金额
            api.wait_update()#可以多设置几次实现多行情序列，一个循环里面只有一次是触发行情更新的，后续的所有的代码都会滞留
            print("资金情况",account,"可用资金",account.available,"账户权益",account.balance)
            print("当前持仓",position)

            #中金所期货信息
            futures=api.query_quotes(ins_class='FUTURE',exchange_id="CFFEX",expired=False)#中金所期货
            while True:
                api.wait_update()
                #前面都没问题了，唯一的就是futures[0]会导致索引越界，这段时间其实是个空数据【不清楚原因】
                print("期货信息",futures,len(futures),type(futures))
                break

            #提取主力合约次主力合约等信息
            targetfutures=[]
            for future in futures:
                match=re.search(r'CFFEX\.(\D+)',future)# 使用正则表达式匹配"CFFEX."之后直到数字之前的部分
                if match:
                    targetfutures.append(match.group(1))# 如果匹配成功，将匹配到的部分添加到结果列表中
            print("去重前",targetfutures)
            targetfutures=set(targetfutures)
            print("去重后",targetfutures)
            alldf=pd.DataFrame({})
            for stock in targetfutures:
                pattern=re.compile(rf'CFFEX\.{stock}\d+')
                thisdf=pd.DataFrame({})
                for future in futures:
                    if pattern.match(future):
                        print(stock,future)
                        klines=api.get_kline_serial(future,60*60*24,data_length=1)#duration_seconds数据周期（1分钟线为60,1小时线为3600,日线为86400，注意: 周期在日线以内时此参数可以任意填写, 在日线以上时只能是日线(86400)的整数倍），data_length数据长度，adj_type是否复权
                        thisdf=pd.concat([thisdf,pd.DataFrame({"品种":[stock],"合约":[future],"成交量":[klines.volume.iloc[-1]]})])
                        print(klines)
                # print("未进行排序",thisdf)
                # 按成交量对合约进行排序
                thisdf=thisdf.sort_values(by='成交量', ascending=False)
                sortedthisdf=thisdf.reset_index(drop=True,inplace=False)
                print(sortedthisdf)
                print(f"成交量第二大的合约是: {sortedthisdf.loc[0].合约}",type(sortedthisdf.loc[0].合约))
                thisdf["成交量最大的合约"]=sortedthisdf.loc[0].合约
                thisdf["成交量第二的合约"]=sortedthisdf.loc[1].合约
                alldf=pd.concat([alldf,thisdf])
            print(alldf)


            #获取期权信息
            indexlist=["SSE.000300",#沪深三百
                    "SSE.000016",#上证50
                    "SSE.000852",#中证1000
                    ]
            for index in indexlist:#可能是收盘之后数据不对
                print(index)
                # 查询行情tick
                quote=api.get_quote(index)
                # print(quote,quote.datetime,
                #       quote.last_price,
                #       quote.ask_price1,
                #       quote.ask_price2,
                #       quote.bid_price1,
                #       quote.bid_price2,
                #       quote.ask_volume1,
                #       quote.ask_volume2,
                #       quote.bid_volume1,
                #       quote.bid_volume2,
                #       )

                #查询对应的期权
                now=datetime.datetime.now()#当前只研究次月合约的机会
                # 交易主力合约
                thisyear=now.year
                thismonth=now.month
                if thismonth==12:
                    thismonth=1
                    thisyear+=1
                else:
                    thismonth+=1
                    pass
                print(thisyear,type(thismonth),thismonth,type(thismonth))
                # 查询符合条件的期权列表，针对ETF和股指期权未下市合约，可按距离最后行权日的距离的远近查询，返回全部的实值、平值、虚值期权
                # option_class (str): [必填] 期权类型
                #*CALL: 看涨期权
                #*PUT: 看跌期权
                # nearbys (int/list of int): [必填] 将所有未下市期权按照最后行权日由近到远排序，参数 0 代表的是当前月/最接近当前月份的未下市期权,1 代表下一个到期的期权，依此类推。
                #*对于 ETF 期权来说 1 代表在参数 0 后的下月，2 代表随后的第一个一个季月，3 代表随后的第二个季月
                #*对于股指期权来说 1 代表在参数 0 后的下月，2 代表下下月，3 代表随后第一个季月，4 代表随后第二个季月，5 代表随后第三个季月
                # has_A (bool): [可选] 是否含有 A，输入 True 代表只含 A 的期权，输入 False 代表不含 A 的期权，默认为 None 不做区分
                # 还有一个query_all_level_options函数，可获取所有期权但是更加复杂
                thisoptions=api.query_all_level_options(underlying_symbol=index,
                                                        underlying_price=quote.last_price,
                                                        option_class="CALL",#卖出期权
                                                        # nearbys=1,#近月期权
                                                        exercise_year=thisyear,
                                                        exercise_month=thismonth,
                                                        # has_A=None,
                                                        )
                while True:
                    api.wait_update()
                    print(thisoptions,"thisoptions",type(thisoptions))
                    thisoption=thisoptions.at_money_options#【这里回测当中取出来的也是空数据】
                    quoteoption=api.get_quote(thisoption[0])#获取指定期权的tick
                    print(thisoption,type(thisoption[0]),quoteoption)
                    thisfuture=re.sub(r"-.*$","-",thisoption[0])#这个是去掉倒数最后一个之后的字符
                    # thisfuture=re.match(r"^(.*)-",thisoption[0]).group(1)#这个是去掉倒数第一个之后的字符
                    thisfuture=thisfuture.replace("-","")
                    thisfuture=thisfuture.replace("IO","IF")#沪深300
                    thisfuture=thisfuture.replace("HO","IH")#上证50
                    thisfuture=thisfuture.replace("MO","IM")#中证1000
                    quotefuture=api.get_quote(thisfuture)#获取指定期货的tick
                    print(thisfuture,type(thisfuture[0]),quotefuture)
                    break
            # print("今日多头持仓手数",position.pos_long_today)
            # print("可用资金",account.available)
            # # if api.is_changing(order,["status","volume_orign","volume_left"]):
            # #     print("单状态: %s,已成交: %d 手" % (order.status,order.volume_orign-order.volume_left))
            # # if api.is_changing(position,"pos_long_today"):
            # #     print("今多头: %d 手" % (position.pos_long_today))
            qrb_2001_vol=math.floor(account.balance*0.5/qrb_2001.last_price)
            qrb_1910_vol=math.floor(account.balance*0.5/qrb_1910.last_price)
            spread = qrb_1910.last_price/qrb_2001.last_price-1
            print("资金余额",account.balance,"远月价格和近月价格",qrb_2001.last_price,qrb_1910.last_price,"当前价差:",spread,"远月数量",qrb_2001_vol,"远月数量",qrb_1910_vol)
            if (spread>0.05):
                print("价差过高: 空近月，多远月")
                rb_1910.set_target_volume(-qrb_1910_vol)#set_target_volume类似于预埋单，会在下一根tick上下单，避免未来函数
                rb_2001.set_target_volume(qrb_2001_vol)
                # #回测的时候使用insertorder的话相当于用到了当前获取的数据的价格去下单了
                # # 下单并返回委托单的引用，当该委托单有变化时 order 中的字段会对应更新
                # order=api.insert_order(symbol="CFFEX.IH2402",direction="BUY",offset="OPEN",volume=5,limit_price=2750)
                # print(f"单状态:{order.status},已成交{order.volume_orign-order.volume_left}手")
                # # 这个函数调用后会立即返回一个指向此委托单的对象引用,使用方法与dict一致,内容如下:
                # # {
                # # "order_id":"", #"123"(委托单ID,对于一个用户的所有委托单，这个ID都是不重复的)
                # # "exchange_order_id":"", #"1928341"(交易所单号)
                # # "exchange_id":"", #"SHFE"(交易所)
                # # "instrument_id":"", #"rb1901"(交易所内的合约代码)
                # # "direction":"", #"BUY"(下单方向,BUY=买,SELL=卖)
                # # "offset":"", #"OPEN"(开平标志,OPEN=开仓,CLOSE=平仓,CLOSETODAY=平今)
                # # "volume_orign":0, #10(总报单手数)
                # # "volume_left":0, #5(未成交手数)
                # # "limit_price":float("nan"), # 4500.0(委托价格,仅当price_type=LIMIT时有效)
                # # "price_type":"", #"LIMIT"(价格类型,ANY=市价,LIMIT=限价)
                # # "volume_condition":"", #"ANY"(手数条件,ANY=任何数量,MIN=最小数量,ALL=全部数量)
                # # "time_condition":"", #"GFD"(时间条件,IOC=立即完成，否则撤销,GFS=本节有效,GFD=当日
                # # 有效,GTC=撤销前有效,GFA=集合竞价有效)
                # # "insert_date_time":0, #1501074872000000000(下单时间(按北京时间)，自unix
                # # →epoch(1970-01-0100:00:00GMT)以来的纳秒数)
                # # "status":"", #"ALIVE"(委托单状态,ALIVE=有效,FINISHED=已完)
                # # "last_msg":"", #"报单成功"(委托单状态信息)
                # # }
                # # 与其它所有数据一样,委托单的信息也会在api.wait_update()时被自动更新
            elif (spread<0.02)and(spread>0):
                print("价差回复: 清空持仓")
                rb_1910.set_target_volume(0)
                rb_2001.set_target_volume(0)
            if (spread<-0.05):
                print("价差过高: 多近月，空远月")
                rb_1910.set_target_volume(qrb_1910_vol)
                rb_2001.set_target_volume(-qrb_2001_vol)
            elif (spread>-0.02)and(spread<0):
                print("价差回复: 清空持仓")
                rb_1910.set_target_volume(0)
                rb_2001.set_target_volume(0)

    # except BacktestFinished as e:
    #     #回测结束时会执行这里的代码
    #     print("任务结束")
    #     print(account.trade_log) #回测的详细信息
    #     print(account.tqsdk_stat) #回测时间内账户交易信息统计结果，其中包含以下字段
    #     #init_balance起始资金
    #     #balance结束资金
    #     #max_drawdown最大回撤
    #     #profit_loss_ratio盈亏额比例
    #     #winning_rate胜率
    #     #ror收益率
    #     #annual_yield年化收益率
    #     #sharpe_ratio年化夏普率
    #     #tqsdk_punchline天勤点评
    

elif target=="实盘":
    # 期权一般在期货前到期【原则上会因为交割日不同导致单腿】
    import re
    while True:
        # # #沪深股票信息
        # # # stocks=api.query_quotes(ins_class='STOCK',expired=False)#获取所有交易所的交易标的
        # # stocks=api.query_quotes(ins_class='STOCK',expired=False)# SSE.10002504 - 上交所沪深300etf期权，SZSE.90000097 - 深交所沪深300etf期权
        # # print("个股信息",stock,len(stock),stock[0],type(stock[0])) 
        # # time.sleep(2)
        # # # #中金所期货信息
        # # # future=api.query_quotes(ins_class='FUTURE',expired=False)#获取所有交易所的交易标的
        # futures=api.query_quotes(ins_class='FUTURE',exchange_id="CFFEX",expired=False)#中金所期货
        # print("期货信息",futures,len(futures),futures[0],type(futures[0]))
        # time.sleep(2)
        

        # #提取主力合约次主力合约等信息
        # targetfutures=[]
        # for future in futures:
        #     match=re.search(r'CFFEX\.(\D+)',future)# 使用正则表达式匹配"CFFEX."之后直到数字之前的部分
        #     if match:
        #         targetfutures.append(match.group(1))# 如果匹配成功，将匹配到的部分添加到结果列表中
        # print("去重前",targetfutures)
        # targetfutures=set(targetfutures)
        # print("去重后",targetfutures)
        # alldf=pd.DataFrame({})
        # for stock in targetfutures:
        #     pattern=re.compile(rf'CFFEX\.{stock}\d+')
        #     thisdf=pd.DataFrame({})
        #     for future in futures:
        #         if pattern.match(future):
        #             print(stock,future)
        #             klines=api.get_kline_serial(future,60*60*24,data_length=1)#duration_seconds数据周期（1分钟线为60,1小时线为3600,日线为86400，注意: 周期在日线以内时此参数可以任意填写, 在日线以上时只能是日线(86400)的整数倍），data_length数据长度，adj_type是否复权
        #             thisdf=pd.concat([thisdf,pd.DataFrame({"品种":[stock],"合约":[future],"成交量":[klines.volume.iloc[-1]]})])
        #             print(klines)
        #     # print("未进行排序",thisdf)
        #     # 按成交量对合约进行排序
        #     thisdf=thisdf.sort_values(by='成交量', ascending=False)
        #     sortedthisdf=thisdf.reset_index(drop=True,inplace=False)
        #     print(sortedthisdf)
        #     print(f"成交量第二大的合约是: {sortedthisdf.loc[0].合约}",type(sortedthisdf.loc[0].合约))
        #     thisdf["成交量最大的合约"]=sortedthisdf.loc[0].合约
        #     thisdf["成交量第二的合约"]=sortedthisdf.loc[1].合约
        #     alldf=pd.concat([alldf,thisdf])
        # print(alldf)
        # alldf.to_csv("alldf.csv")


        # #中金所期权信息
        # # options=api.query_quotes(ins_class='OPTION',expired=False)#获取所有交易所的交易标的
        # options=api.query_quotes(ins_class='OPTION',exchange_id="CFFEX",expired=False)#中金所期权
        # print("期权信息",options,len(options),options[0],type(options[0]))
        # for option in options:
        #     option_margin_money=option_margin(option)#计算期权保证金
        #     print(option,"期权保证金",option_margin_money)
        # time.sleep(2)
        # #中金所指数信息
        # indexlist=api.query_quotes(ins_class='INDEX',exchange_id="CFFEX",expired=False)#中金所指数
        # print("指数信息",indexlist,len(indexlist),indexlist[0],type(indexlist[0]))
        # time.sleep(2)
        # #主力合约信息
        # exchanges=api.query_cont_quotes(exchange_id="CFFEX",has_night=False)
        # print("主力合约",exchanges)
        # time.sleep(2)
        # # 中金所合约对应的期权期货
        # for exchange in exchanges:
        #     # 查询行情tick
        #     quote=api.get_quote(exchange)
        #     print(quote,quote.datetime,
        #           quote.last_price,
        #           quote.ask_price1,
        #           quote.ask_price2,
        #           quote.bid_price1,
        #           quote.bid_price2,
        #           quote.ask_volume1,
        #           quote.ask_volume2,
        #           quote.bid_volume1,
        #           quote.bid_volume2,
        #           )
        #     # while True:
        #     #     api.wait_update()# 调用 wait_update 等待业务信息发生变化，例如: 行情发生变化,委托单状态变化,发生成交等等
        #     #     # 其他合约的行情的更新也会触发业务信息变化，因此下面使用 is_changing 判断 FG209 的行情是否有变化
        #     #     if api.is_changing(quote):# 如果 exchange的任何字段有变化，is_changing就会返回 True
        #     #         print("行情变化",quote)
        #     #     if api.is_changing(quote,["ask_price1","ask_volume1","bid_price1","bid_volume1"]):# 当 exchange 的买1价/买1量/卖1价/卖1量中任何一个有变化，is_changing都会返回 True
        #     #         print("盘口变化",quote.ask_price1,quote.ask_volume1,quote.bid_price1,quote.bid_volume1)
        #     # # 下单
        #     # order=api.insert_order(symbol=exchange,direction="BUY",offset="OPEN",volume=quote.ask_volume1,limit_price=quote.last_price)
        #     # print(order)
        # #撤单
        # cancel_order=api.cancel_order(order_or_order_id: Union[str,Order],account)


        ##【获取中金所期权数据】
        # indexlist=["SSE.510050",#为上交所华夏上证 50 ETF 期权标的
        #             "SSE.510300",#为上交所华泰柏瑞沪深 300 ETF 期权标的
        #             "SZSE.159919" ,#为深交所嘉实沪深 300 ETF 期权标的
        #             "SZSE.159915",#为深交所易方达创业板 ETF 期权标的
        #             "SZSE.159922",#为深交所嘉实中证 500 ETF 期权标的
        #             "SSE.510500",#为上交所南方中证 500 ETF 期权标的
        #             ]#试用账户不支持ETF数据查询
        indexlist=["SSE.000300",#沪深三百
                "SSE.000016",#上证50
                "SSE.000852",#中证1000
                ]
        for index in indexlist:#可能是收盘之后数据不对
            print(index)
            # 查询行情tick
            quote=api.get_quote(index)
            # print(quote,quote.datetime,
            #       quote.last_price,
            #       quote.ask_price1,
            #       quote.ask_price2,
            #       quote.bid_price1,
            #       quote.bid_price2,
            #       quote.ask_volume1,
            #       quote.ask_volume2,
            #       quote.bid_volume1,
            #       quote.bid_volume2,
            #       )


            #查询对应的期权
            now=datetime.datetime.now()#当前只研究次月合约的机会
            # 交易主力合约
            thisyear=now.year
            thismonth=now.month
            if thismonth==12:
                thismonth=1
                thisyear+=1
            else:
                thismonth+=1
                pass
            print(thisyear,type(thismonth),thismonth,type(thismonth))
            # 查询符合条件的期权列表，针对ETF和股指期权未下市合约，可按距离最后行权日的距离的远近查询，返回全部的实值、平值、虚值期权
            # option_class (str): [必填] 期权类型
            #*CALL: 看涨期权
            #*PUT: 看跌期权
            # nearbys (int/list of int): [必填] 将所有未下市期权按照最后行权日由近到远排序，参数 0 代表的是当前月/最接近当前月份的未下市期权,1 代表下一个到期的期权，依此类推。
            #*对于 ETF 期权来说 1 代表在参数 0 后的下月，2 代表随后的第一个一个季月，3 代表随后的第二个季月
            #*对于股指期权来说 1 代表在参数 0 后的下月，2 代表下下月，3 代表随后第一个季月，4 代表随后第二个季月，5 代表随后第三个季月
            # has_A (bool): [可选] 是否含有 A，输入 True 代表只含 A 的期权，输入 False 代表不含 A 的期权，默认为 None 不做区分
            # 还有一个query_all_level_options函数，可获取所有期权但是更加复杂
            thisoptions=api.query_all_level_options(underlying_symbol=index,
                                                    underlying_price=quote.last_price,
                                                    option_class="CALL",#卖出期权
                                                    # nearbys=1,#近月期权
                                                    exercise_year=thisyear,
                                                    exercise_month=thismonth,
                                                    # has_A=None,
                                                    )
            # print(thisoptions,"thisoptions",type(thisoptions))
            thisoption=thisoptions.at_money_options
            quoteoption=api.get_quote(thisoption[0])#获取指定期权的tick
            print(thisoption,type(thisoption[0]),quoteoption)
            thisfuture=re.sub(r"-.*$","-",thisoption[0])#这个是去掉倒数最后一个之后的字符
            # thisfuture=re.match(r"^(.*)-",thisoption[0]).group(1)#这个是去掉倒数第一个之后的字符
            thisfuture=thisfuture.replace("-","")
            thisfuture=thisfuture.replace("IO","IF")#沪深300
            thisfuture=thisfuture.replace("HO","IH")#上证50
            thisfuture=thisfuture.replace("MO","IM")#中证1000
            quotefuture=api.get_quote(thisfuture)#获取指定期货的tick
            print(thisfuture,type(thisfuture[0]),quotefuture)

        time.sleep(1000)
        break

    #【策略类：主要是交易记录的打印和订单的验证都逻辑，逻辑有提高的空间】
    # #样板【重点观察订单状态，这块是之前的代码所没有的】
    # #!/usr/bin/env python
    # # -*- coding: utf-8 -*-
    # from tqsdk import TqApi,TqAuth,TargetPosTask,TqKq,TqAccount
    # import pandas as pd
    # import numpy as np
    # from datetime import datetime
    # import yaml#pip install PyYAML
    # from typing import Union,List,Any,Optional
    # import time
    # import os
    # import pickle
    # class Strategy(object):
    #     def __init__(self,configfile):
    #         self.configfile=configfile
    #         dict_cfg=self.load_config(self.configfile)
    #         self.params=dict_cfg['Params']
    #         self.get_params()
    #         self.get_data()
    #         print(self.stra_name+' __init__  {}的总仓位:{} pos:{} MarketPosition:{}  Quote_symbol:{} Trade_symbol:{} acc_name:{} is_testing:{}'.format(self.Trade_symbol.split('.')[1],self.position.pos,self.pos,self.MarketPosition,self.Quote_symbol,self.Trade_symbol,self.acc_name,self.is_testing))
    #     def get_params(self):
    #         self.Quote_symbol=self.params['Quote_symbol']#'KQ.m@'+symbol#KQ.m@CFFEX.IF - 中金所IF品种主连合约
    #         self.Trade_symbol=self.params['Trade_symbol']

    #         self.ID=self.params['ID']
    #         self.stra_name=self.params['stra_name']
    #         self.port=self.params['port']
    #         self.acc_number=self.params['acc_number']
    #         self.acc_name=self.params['acc_name']
    #         self.pwd=self.params['pwd']
    #         self.is_testing=self.params['is_testing']
    #         if self.is_testing==1:
    #             self.api=TqApi(TqKq(),auth=',',web_gui=':'+self.port,disable_print=True)
    #         if self.is_testing==0:
    #             self.api=TqApi(TqAccount(self.acc_name,self.acc_number,self.pwd),auth=',',web_gui=':'+self.port,disable_print=True)
    #         self.position=self.api.get_position(self.Trade_symbol)
    #         self.account=self.api.get_account()
    #         self.target_pos=TargetPosTask(self.api,self.Trade_symbol)
    #         self.lots=self.params['lots']
    #         self.pos=self.params['pos']
    #         self.Interval=self.params['Interval']
    #         self.path_in=self.params['path_in']
    #         self.path_out=self.params['path_out']
    #         self.MarketPosition=self.params['MarketPosition']
    #         self.entryprice=self.params['entryprice']
    #         self.entrydate=self.params['entrydate']
    #         self.exitprice=self.params['exitprice']
    #         self.exitdate=self.params['exitdate']
    #     def closeapi(self):
    #         self.api.close()
    #     def __getstate__(self):
    #         return self.__dict__
    #     def get_data(self):
    #         self.klines=self.api.get_kline_serial(self.Quote_symbol,self.Interval,data_length=8964)
    #     def write_trade_log(self,item):
    #         if not os.path.exists(self.path_out+self.stra_name+'\\' ):
    #             os.mkdir(self.path_out+self.stra_name+'\\')
    #             df_trade_log=pd.DataFrame([])
    #             #df_trade_log.columns=['stra_name','symbol','datetime','buyorsell','price','lots']
    #             df_trade_log.to_csv(self.path_out+self.stra_name+'\\'+self.stra_name+'_trade_log.csv')
    #         if not os.path.isfile(self.path_out+self.stra_name+'\\'+self.stra_name+'_trade_log.csv'):
    #             df_trade_log=pd.DataFrame([])
    #             df_trade_log.to_csv(self.path_out+self.stra_name+'\\'+self.stra_name+'_trade_log.csv')
    #         df_trade_log=pd.read_csv(self.path_out+self.stra_name+'\\'+self.stra_name+'_trade_log.csv',index_col=0)
    #         if len(df_trade_log.values.tolist())!=0:
    #             df_trade_log.columns=['stra_name','symbol','datetime','buyorsell','price','lots']
    #         trade_log=df_trade_log.values.tolist()
    #         trade_log.append(item)
    #         df_trade_log=pd.DataFrame(trade_log)
    #         df_trade_log.columns=['stra_name','symbol','datetime','buyorsell','price','lots']
    #         df_trade_log.to_csv(self.path_out+self.stra_name+'\\'+self.stra_name+'_trade_log.csv')
    #         print(self.stra_name+' '+self.Trade_symbol+' one log write to trade_log ')
    #     def buy(self):
    #         info_dict={'position': self.position.pos,'pos': self.pos,'acc_name': self.acc_name,'stra_name': self.stra_name}
    #         self.PRINT('before buy',info_dict)
    #         if self.MarketPosition<0:
    #             self.buytocover()
    #         quote=self.api.get_quote(self.Trade_symbol)
    #         order=self.api.insert_order(symbol=self.Trade_symbol,direction="BUY",offset="OPEN",volume=self.lots,
    #                                     limit_price=quote.last_price)
    #         while True:
    #             self.api.wait_update()
    #             # print("单状态: %s,已成交: %d 手" % (order.status,order.volume_orign - order.volume_left))
    #             if order.status == "FINISHED":
    #                 self.MarketPosition=1
    #                 self.pos=self.lots
    #                 # trade_log
    #                 date_str=time.strftime("%Y%m%d %H:%M:%S",time.localtime())
    #                 item=[self.stra_name,self.Trade_symbol,date_str,'buy',order.trade_price,self.lots]
    #                 self.write_trade_log(item)
    #                 self.entrydate=date_str
    #                 self.entryprice=order.trade_price#可以更改
    #                 params=self.load_config(self.configfile)
    #                 params['Params']['entryprice']=self.entryprice
    #                 params['Params']['entrydate']=self.entrydate
    #                 self.update_cfg_yml(params)
    #                 break
    #         info_dict={'position': self.position.pos,'pos': self.pos,'acc_name': self.acc_name,
    #                         'stra_name': self.stra_name}
    #         self.PRINT('after buy',info_dict)
    #     def sell(self):
    #         if self.MarketPosition>0:
    #             info_dict={'position': self.position.pos,'pos': self.pos,'acc_name': self.acc_name,
    #                             'stra_name': self.stra_name}
    #             self.PRINT('before sell',info_dict)
    #             quote=self.api.get_quote(self.Trade_symbol)
    #             exchange=self.Trade_symbol.split('.')[0]
    #             today=time.strftime("%Y-%m-%d",time.localtime())
    #             if (exchange == 'SHFE' and today == self.entrydate[:10]) or (
    #                     self.Trade_symbol[:6].upper() == 'INE.SC' and today == self.entrydate[:10]):
    #                 order=self.api.insert_order(symbol=self.Trade_symbol,direction="SELL",offset="CLOSETODAY",volume=self.lots,
    #                                             limit_price=quote.last_price)
    #             else:
    #                 order=self.api.insert_order(symbol=self.Trade_symbol,direction="SELL",offset="CLOSE",volume=self.lots,
    #                                             limit_price=quote.last_price)
    #             while True:
    #                 self.api.wait_update()
    #                 # print("单状态: %s,已成交: %d 手" % (order.status,order.volume_orign - order.volume_left))
    #                 if order.status == "FINISHED":
    #                     self.MarketPosition=0
    #                     self.pos=0
    #                     # trade_log
    #                     #date_str=time.strftime("%Y-%m-%d %H:%M:%S",
    #                     #                         time.localtime(self.klines.datetime.iloc[-1]/1000000000))
    #                     date_str=time.strftime("%Y%m%d %H:%M:%S",time.localtime())
    #                     item=[self.stra_name,self.Trade_symbol,date_str,'sell',order.trade_price,self.lots]
    #                     self.write_trade_log(item)
    #                     self.exitdate=date_str
    #                     self.exitprice=order.trade_price
    #                     params=self.load_config(self.configfile)
    #                     params['Params']['exitprice']=self.exitprice
    #                     params['Params']['exitdate']=self.exitdate
    #                     self.update_cfg_yml(params)
    #                     break
    #             info_dict={'position': self.position.pos,'pos': self.pos,'acc_name': self.acc_name,
    #                             'stra_name': self.stra_name}
    #             self.PRINT('after sell',info_dict)
    #     def sellshort(self):
    #         info_dict={'position': self.position.pos,'pos': self.pos,'acc_name': self.acc_name,
    #                         'stra_name': self.stra_name}
    #         self.PRINT('before sellshort',info_dict)
    #         if self.MarketPosition>0:
    #             self.sell()
    #         quote=self.api.get_quote(self.Trade_symbol)
    #         order=self.api.insert_order(symbol=self.Trade_symbol,direction="SELL",offset="OPEN",volume=self.lots,
    #                                     limit_price=quote.last_price)
    #         while True:
    #             self.api.wait_update()
    #             # print("单状态: %s,已成交: %d 手" % (order.status,order.volume_orign - order.volume_left))
    #             if order.status == "FINISHED":
    #                 self.MarketPosition=-1
    #                 self.pos=-self.lots
    #                 # trade_log
    #                 # date_str=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.klines.datetime.iloc[-1]/1000000000))
    #                 date_str=time.strftime("%Y%m%d %H:%M:%S",time.localtime())
    #                 item=[self.stra_name,self.Trade_symbol,date_str,'sellshort',order.trade_price,self.lots]
    #                 self.write_trade_log(item)
    #                 self.entrydate=date_str
    #                 self.entryprice=order.trade_price
    #                 params=self.load_config(self.configfile)
    #                 params['Params']['entryprice']=self.entryprice
    #                 params['Params']['entrydate']=self.entrydate
    #                 self.update_cfg_yml(params)
    #                 break
    #         info_dict={'position': self.position.pos,'pos': self.pos,'acc_name': self.acc_name,
    #                         'stra_name': self.stra_name}
    #         self.PRINT('after sellshort',info_dict)
    #     def buytocover(self):
    #         if self.MarketPosition<0:
    #             info_dict={'position': self.position.pos,'pos': self.pos,'acc_name': self.acc_name,
    #                             'stra_name': self.stra_name}
    #             self.PRINT('before buytocover',info_dict)
    #             quote=self.api.get_quote(self.Trade_symbol)
    #             exchange=self.Trade_symbol.split('.')[0]
    #             today=time.strftime("%Y-%m-%d",time.localtime())
    #             if (exchange == 'SHFE' and today == self.entrydate[:10]) or (
    #                     self.Trade_symbol[:6].upper() == 'INE.SC' and today == self.entrydate[:10]):
    #                 order=self.api.insert_order(symbol=self.Trade_symbol,direction="BUY",offset="CLOSETODAY",volume=self.lots,
    #                                             limit_price=quote.last_price)
    #             else:
    #                 order=self.api.insert_order(symbol=self.Trade_symbol,direction="BUY",offset="CLOSE",volume=self.lots,
    #                                             limit_price=quote.last_price)
    #             while True:
    #                 self.api.wait_update()
    #                 # print("单状态: %s,已成交: %d 手" % (order.status,order.volume_orign - order.volume_left))
    #                 if order.status == "FINISHED":
    #                     self.MarketPosition=0
    #                     self.pos=0
    #                     # trade_log
    #                     # date_str=time.strftime("%Y-%m-%d %H:%M:%S",
    #                     #                         time.localtime(self.klines.datetime.iloc[-1]/1000000000))
    #                     date_str=time.strftime("%Y%m%d %H:%M:%S",time.localtime())
    #                     item=[self.stra_name,self.Trade_symbol,date_str,'buytocover',order.trade_price,
    #                             self.lots]
    #                     self.write_trade_log(item)
    #                     self.exitdate=date_str
    #                     self.exitprice=order.trade_price
    #                     params=self.load_config(self.configfile)
    #                     params['Params']['exitprice']=self.exitprice
    #                     params['Params']['exitdate']=self.exitdate
    #                     self.update_cfg_yml(params)
    #                     break
    #             info_dict={'position': self.position.pos,'pos': self.pos,'acc_name': self.acc_name,
    #                             'stra_name': self.stra_name}
    #             self.PRINT('after buytocover',info_dict)
    #     def stra(self):
    #         '''
    #         while True:
    #             self.api.wait_update()
    #             if self.api.is_changing(self.klines.iloc[-1],"datetime"):
    #                 # datetime: 自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数
    #                 print("新K线",datetime.fromtimestamp(self.klines.iloc[-1]["datetime"]/1e9))
    #                 # 判断最后一根K线的收盘价是否有变化
    #             if self.api.is_changing(self.klines.iloc[-1],"close"):
    #                 # klines.close返回收盘价序列
    #                 print("K线变化",datetime.fromtimestamp(self.klines.iloc[-1]["datetime"]/1e9),self.klines.close.iloc[-1])
    #         self.api.close()
    #         '''
    #     def load_config(self,path_filename):
    #         with open(path_filename,encoding='utf-8') as stra_cfg_json_file:
    #             dict_cfg=yaml.load(stra_cfg_json_file,Loader=yaml.FullLoader)
    #         return dict_cfg
    #     def dump_config(self,path_filename,params):
    #         with open(path_filename,"w",encoding="utf-8") as f:
    #             yaml.dump(params,f,Dumper=yaml.Dumper,default_flow_style=False,encoding='utf-8',allow_unicode=True)
    #     def update_cfg_yml(self,params):
    #         #params=self.load_config(self.configfile)
    #         params['Params']['MarketPosition']=self.MarketPosition
    #         params['Params']['pos']=self.pos
    #         self.dump_config(self.configfile,params)
    #     def PRINT(self,beforeorafter,info_dict):
    #         position=info_dict['position']
    #         stra_name=info_dict['stra_name']
    #         pos=info_dict['pos']
    #         acc_name=info_dict['acc_name']
    #         print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),
    #               f'策略名称{stra_name}',
    #               beforeorafter,
    #               f'acc_name:{acc_name}总仓位:{position}pos:{pos}')

elif target=="测试":
    #下载本账号当日订单记录
    import csv
    import os
    from datetime import datetime
    from tqsdk import TqApi, TqAuth, TqKq
    """
    本示例用于下载账户当前交易日到目前位置的全部委托单、成交记录分别到 orders.csv、trades.csv 文件。
    如果文件已经存在，会将记录追加到文件末尾。
    用户可以在交易日结束之后，运行本示例，可以将当日的委托单、成交记录保存到本地。
    """
    order_cols = ["order_id", "exchange_order_id", "exchange_id", "instrument_id",
                "direction", "offset", "status", "volume_orign", "volume_left", "limit_price",
                "price_type", "volume_condition", "time_condition", "insert_date_time", "last_msg"]
    trade_cols = ["trade_id", "order_id", "exchange_trade_id", "exchange_id", "instrument_id", 
                "direction", "offset", "price", "volume", "trade_date_time"]
    def write_csv(file_name, cols, datas):
        file_exists = os.path.exists(file_name) and os.path.getsize(file_name) > 0
        print("file_exists",file_exists)
        with open(file_name, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, dialect='excel')
        print("csv_writer",csv_writer)
        if not file_exists:
            print("datas",datas)
            if len(datas)==0:#空值处理
                print("当日数据为空")
                pass
            else:
                csv_writer.writerow(['datetime'] + cols)
                print("新建文件")
        for item in datas.values():
            if 'insert_date_time' in cols:
                dt = datetime.fromtimestamp(item['insert_date_time'] / 1e9).strftime('%Y-%m-%d %H:%M:%S.%f')
            elif 'trade_date_time' in cols:
                dt = datetime.fromtimestamp(item['trade_date_time'] / 1e9).strftime('%Y-%m-%d %H:%M:%S.%f')
            else:
                dt = None
                row = [dt] + [item[k] for k in cols]
                csv_writer.writerow(row)
    with TqApi(TqKq(), auth=TqAuth("19511189162","wth000")) as api:
        # 将当前账户下全部委托单、成交信息写入 csv 文件中
        write_csv("orders.csv", order_cols,api.get_order())
        write_csv("trades.csv", trade_cols,api.get_trade())



    # #获取近期数据【时间太久的行情数据无法直接下载（直接下载需要开通专业版）】
    # from datetime import date,datetime,timedelta
    # import pandas as pd
    # import time
    # import copy
    # klines_a60=api.get_kline_serial('KQ.i@DCE.jd',60,10000)
    # klines=copy.deepcopy(klines_a60)
    # rr=[]
    # for i in range(len(klines['datetime'])):
    #     rr.append(datetime.fromtimestamp(klines['datetime'].iloc[i]/1e9))
    # aaaa=pd.DataFrame(rr)
    # aaaa.columns=['datetime']
    # klines.drop('datetime',axis=1,inplace=True)
    # klines.drop('id',axis=1,inplace=True)
    # klines.drop('symbol',axis=1,inplace=True)
    # klines.drop('duration',axis=1,inplace=True)
    # klines=pd.concat([klines,aaaa],axis=1)
    # klines.index=klines["datetime"]
    # klines.drop('datetime',axis=1,inplace=True)
    # rr=[]
    # for x in klines.columns:
    #     rr.append('KQ.i@DCE.jd'+"."+x)
    # klines.columns=rr
    # print(klines)






# ****【附录】****
# #从天勤获取所有期货合约代码
#*FUTURE: 期货
#*CONT: 主连
#*COMBINE: 组合
#*INDEX: 指数
#*OPTION: 期权
#*STOCK: 股票

# #品种信息
# SHFE.cu1901  -  上期所 cu1901 期货合约
# DCE.m1901    -  大商所 m1901 期货合约
# CZCE.SR901   -  郑商所 SR901 期货合约
# CFFEX.IF1901 -  中金所 IF1901 期货合约
# INE.sc2109   -  上期能源 sc2109 期货合约
# GFEX.si2301  -  广期所 si2301 期货合约
# KQD.m@CBOT.ZS - 美黄豆主连

# CZCE.SPD SR901&SR903  - 郑商所 SR901&SR903 跨期合约
# DCE.SP a1709&a1801    - 大商所 a1709&a1801 跨期合约
# GFEX.SP si2308&si2309 - 广期所 si2308&si2309 跨期组合

# DCE.m1807-C-2450    - 大商所豆粕期权
# CZCE.CF003C11000    - 郑商所棉花期权
# SHFE.au2004C308     - 上期所黄金期权
# CFFEX.IO2002-C-3550 - 中金所沪深300股指期权
# INE.sc2109C450      - 上期能源原油期权
# GFEX.si2308-C-5800  - 广期所硅期权

# KQ.m@CFFEX.IF - 中金所IF品种主连合约
# KQ.i@SHFE.bu - 上期所bu品种指数

# SSWE.CUH - 上期所仓单铜现货数据

# SSE.600000 - 上交所浦发银行股票编码
# SZSE.000001 - 深交所平安银行股票编码
# SSE.000016 - 上证50指数
# SSE.000300 - 沪深300指数
# SSE.000905 - 中证500指数
# SSE.000852 - 中证1000指数
# SSE.510050 - 上交所上证50ETF
# SSE.510300 - 上交所沪深300ETF
# SZSE.159919 - 深交所沪深300ETF
# SSE.10002513 - 上交所上证50ETF期权
# SSE.10002504 - 上交所沪深300ETF期权
# SZSE.90000097 - 深交所沪深300ETF期权
# SZSE.159915 - 易方达创业板ETF
# SZSE.90001277 - 创业板ETF期权
# SZSE.159922 - 深交所中证500ETF
# SZSE.90001355 - 深交所中证500ETF期权
# SSE.510500 - 上交所中证500ETF
# SSE.10004497 - 上交所中证500ETF期权
# SZSE.159901 - 深交所100ETF

# DCE.m1807-C-2450 - 大商所豆粕期权
# CZCE.CF003C11000 - 郑商所棉花期权
# SHFE.au2004C308 - 上期所黄金期权
# CFFEX.IO2002-C-3550 - 中金所沪深300股指期权
# SSE.10002513 - 上交所上证50etf期权
# SSE.10002504 - 上交所沪深300etf期权
# SZSE.90000097 - 深交所沪深300etf期权
# CZCE.SPD SR901&SR903 - 郑商所 SR901&SR903 跨期合约
# DCE.SP a1709&a1801 - 大商所 a1709&a1801 跨期合约


# 账户get_account
# #: 币种
# self.currency: str = ""
# #: 昨日账户权益(不包含期权)
# self.pre_balance: float = float("nan")
# #: 静态权益 （静态权益 = 昨日结算的权益 + 今日入金 - 今日出金, 以服务器查询ctp后返回的金额为准）(不包含期权)
# self.static_balance: float = float("nan")
# #: 账户权益 （账户权益 = 动态权益 = 静态权益 + 平仓盈亏 + 持仓盈亏 - 手续费 + 权利金 + 期权市值）
# self.balance: float = float("nan")
# #: 可用资金（可用资金 = 账户权益 - 冻结保证金 - 保证金 - 冻结权利金 - 冻结手续费 - 期权市值）
# self.available: float = float("nan")
# #: 期货公司返回的balance（ctp_balance = 静态权益 + 平仓盈亏 + 持仓盈亏 - 手续费 + 权利金）
# self.ctp_balance: float = float("nan")
# #: 期货公司返回的available（ctp_available = ctp_balance - 保证金 - 冻结保证金 - 冻结手续费 - 冻结权利金）
# self.ctp_available: float = float("nan")
# #: 浮动盈亏
# self.float_profit: float = float("nan")
# #: 持仓盈亏
# self.position_profit: float = float("nan")
# #: 本交易日内平仓盈亏
# self.close_profit: float = float("nan")
# #: 冻结保证金
# self.frozen_margin: float = float("nan")
# #: 保证金占用
# self.margin: float = float("nan")
# #: 冻结手续费
# self.frozen_commission: float = float("nan")
# #: 本交易日内交纳的手续费
# self.commission: float = float("nan")
# #: 冻结权利金
# self.frozen_premium: float = float("nan")
# #: 本交易日内收入-交纳的权利金
# self.premium: float = float("nan")
# #: 本交易日内的入金金额
# self.deposit: float = float("nan")
# #: 本交易日内的出金金额
# self.withdraw: float = float("nan")
# #: 风险度（风险度 = 保证金 / 账户权益）
# self.risk_ratio: float = float("nan")
# #: 期权市值
# self.market_value: float = float("nan")


#持仓Position 是一个持仓对象 
# #: 交易所
# self.exchange_id: str = ""
# #: 交易所内的合约代码
# self.instrument_id: str = ""
# #: 多头老仓手数
# self.pos_long_his: int = 0
# #: 多头今仓手数
# self.pos_long_today: int = 0
# #: 空头老仓手数
# self.pos_short_his: int = 0
# #: 空头今仓手数
# self.pos_short_today: int = 0
# #: 期货公司查询的多头今仓手数 (不推荐, 推荐使用pos_long_today)
# self.volume_long_today: int = 0
# #: 期货公司查询的多头老仓手数 (不推荐, 推荐使用pos_long_his)
# self.volume_long_his: int = 0
# #: 期货公司查询的多头手数 (不推荐, 推荐使用pos_long)
# self.volume_long: int = 0
# #: 期货公司查询的多头今仓冻结 (不推荐)
# self.volume_long_frozen_today: int = 0
# #: 期货公司查询的多头老仓冻结 (不推荐)
# self.volume_long_frozen_his: int = 0
# #: 期货公司查询的多头持仓冻结 (不推荐)
# self.volume_long_frozen: int = 0
# #: 期货公司查询的空头今仓手数 (不推荐, 推荐使用pos_short_today)
# self.volume_short_today: int = 0
# #: 期货公司查询的空头老仓手数 (不推荐, 推荐使用pos_short_his)
# self.volume_short_his: int = 0
# #: 期货公司查询的空头手数 (不推荐, 推荐使用pos_short)
# self.volume_short: int = 0
# #: 期货公司查询的空头今仓冻结 (不推荐)
# self.volume_short_frozen_today: int = 0
# #: 期货公司查询的空头老仓冻结 (不推荐)
# self.volume_short_frozen_his: int = 0
# #: 期货公司查询的空头持仓冻结 (不推荐)
# self.volume_short_frozen: int = 0
# #: 多头开仓均价,以开仓价来统计
# self.open_price_long: float = float("nan")
# #: 空头开仓均价,以开仓价来统计
# self.open_price_short: float = float("nan")
# #: 多头开仓成本,为开仓价乘以手数
# self.open_cost_long: float = float("nan")
# #: 空头开仓成本,为开仓价乘以手数
# self.open_cost_short: float = float("nan")
# #: 多头持仓均价,为多头持仓成本除以多头数量
# self.position_price_long: float = float("nan")
# #: 空头持仓均价,为空头持仓成本除以空头数量
# self.position_price_short: float = float("nan")
# #: 多头持仓成本,为今仓的开仓价乘以手数加上昨仓的昨结算价乘以手数的和
# self.position_cost_long: float = float("nan")
# #: 空头持仓成本,为今仓的开仓价乘以手数加上昨仓的昨结算价乘以手数的和
# self.position_cost_short: float = float("nan")
# #: 多头浮动盈亏
# self.float_profit_long: float = float("nan")
# #: 空头浮动盈亏
# self.float_profit_short: float = float("nan")
# #: 浮动盈亏 （浮动盈亏: 相对于开仓价的盈亏）
# self.float_profit: float = float("nan")
# #: 多头持仓盈亏
# self.position_profit_long: float = float("nan")
# #: 空头持仓盈亏
# self.position_profit_short: float = float("nan")
# #: 持仓盈亏 （持仓盈亏: 相对于上一交易日结算价的盈亏），期权持仓盈亏为 0
# self.position_profit: float = float("nan")
# #: 多头占用保证金
# self.margin_long: float = float("nan")
# #: 空头占用保证金
# self.margin_short: float = float("nan")
# #: 占用保证金
# self.margin: float = float("nan")
# #: 期权权利方市值(始终 >= 0)
# self.market_value_long: float = float("nan")
# #: 期权义务方市值(始终 <= 0)
# self.market_value_short: float = float("nan")
# #: 期权市值
# self.market_value: float = float("nan")
# #: 净持仓手数, ==0表示无持仓或多空持仓手数相等. <0表示空头持仓大于多头持仓, >0表示多头持仓大于空头持仓
# self.pos: int = 0
# #: 多头持仓手数, ==0表示无多头持仓. >0表示多头持仓手数
# self.pos_long: int = 0
# #: 空头持仓手数, ==0表示无空头持仓. >0表示空头持仓手数
# self.pos_short: int = 0


#订单order
# #: 委托单ID, 对于一个用户的所有委托单，这个ID都是不重复的
# self.order_id: str = ""
# #: 交易所单号
# self.exchange_order_id: str = ""
# #: 交易所
# self.exchange_id: str = ""
# #: 交易所内的合约代码
# self.instrument_id: str = ""
# #: 下单方向, BUY=买, SELL=卖
# self.direction: str = ""
# #: 开平标志, OPEN=开仓, CLOSE=平仓, CLOSETODAY=平今
# self.offset: str = ""
# #: 总报单手数
# self.volume_orign: int = 0
# #: 未成交手数
# self.volume_left: int = 0
# #: 委托价格, 仅当 price_type = LIMIT 时有效
# self.limit_price: float = float("nan")
# #: 价格类型, ANY=市价, LIMIT=限价
# self.price_type: str = ""
# #: 手数条件, ANY=任何数量, MIN=最小数量, ALL=全部数量
# self.volume_condition: str = ""
# #: 时间条件, IOC=立即完成，否则撤销, GFS=本节有效, GFD=当日有效, GTC=撤销前有效, GFA=集合竞价有效
# self.time_condition: str = ""
# #: 下单时间，自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数.
# self.insert_date_time: int = 0
# #: 委托单状态信息
# self.last_msg: str = ""
# #: 委托单状态, ALIVE=有效, FINISHED=已完
# self.status: str = ""
# #: 委托单是否确定已死亡（以后一定不会再产生成交）(注意，False 不代表委托单还存活，有可能交易所回来的信息还在路上或者丢掉了)
# self.is_dead: bool = None
# #: 委托单是否确定已报入交易所并等待成交 (注意，返回 False 不代表确定未报入交易所，有可能交易所回来的信息还在路上或者丢掉了)
# self.is_online: bool = None
# #: 委托单是否确定是错单（即下单失败，一定不会有成交）(注意，返回 False 不代表确定不是错单，有可能交易所回来的信息还在路上或者丢掉了)
# self.is_error: bool = None
# #: 平均成交价
# self.trade_price: float = float('nan')