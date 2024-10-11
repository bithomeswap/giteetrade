from .book import Book
from . import utils
from .utils import *
from .type import *
from .cache import *
import os
import math
import time
import json
import uuid
from datetime import datetime
import logging
logger = logging.getLogger()


# "positions": [
#         {
#         "trading_day" : "20240311",
#         "instrument_id" : '600001',
#         "exchange_id" : 'SSE', 
#         "last_price" : 100,
#         "volume" : 10000,
#         "frozen_total" : 100, 
#         "frozen_yesterday" : 100, 
#         "yesterday_volume" : 100,
#         "purchase_redeemable_qty" :100,
#         "avg_open_price" : 100.0, 
#         "position_cost_price" : 99.0,
#         "profit_price" : 97.0,
#         "pre_close_price" : 91.0,
#         "close_price" : 103.0,
#         "realized_pnl" : 1000,
#         "id" : 12345,
#         "instrument_type" : 1
#         }
#     ]

class BookManager():
    def __init__(self,smart) -> None:
        super().__init__()
        self.smart = smart
        self.name = ""
        self.dbPath = "" #book数据存储根路径
        self.bookMap = {} #book表
        
    def init_books(self,commisionMap):
        try:
            self.name = self.smart.pluginName
            self.dbPath = os.path.join(self.smart.config.get("userPath"),"plugin_data")
            self.parseRate(commisionMap)

            files = []
            if(os.path.exists(self.dbPath)):files = os.listdir(self.dbPath)
            for f in files:
                fPath = os.path.join(self.dbPath,f)
                if(not os.path.isfile(fPath)):continue
                if(os.stat(fPath).st_size<=0):continue #空文件跳过
                if(f.find(".data") == -1):continue
                fname = f.replace("_book.data","")
                names = fname.split("-local_") #demo12345-local_439597 -> demo12345,439597
                # logger.debug("init_books:%s", str(names))
                if len(names)>1:
                    names[0] = names[0]+"-local"
                if(names[0] == self.name): #当前组件的book或子账号book
                    if(len(names) >1):
                        self.add_book(names[1],f,False,False)
                    else:
                        self.add_book(names[0],f,False,True)

            #判断是否第一次初始化
            if(not self.bookMap.get(self.name,None)):
                #组件book
                local_db_path = self.name+"_book.data"
                self.add_book(self.name,local_db_path,True,True)
                #子账户book
                account_id = self.smart.current_account.account_id
                local_account_db_path = self.name+"_"+account_id+"_book.data"
                self.add_book(account_id,local_account_db_path,True,False)

            #设置smart.book数据
            self.smart.book = self.bookMap.get(self.name,None)
            #设置Account.book数据
            account_map = self.smart.account_map
            for account_id in account_map:
                account = account_map.get(account_id,None)
                abook = self.bookMap.get(account_id,None)
                if account and abook:
                    account.book = abook


        except Exception as err:
                logger.error(err,exc_info=True, stack_info=True)

    def parseRate(self,commisionMap):
        #转换费率格式
        def convertRate(rate,exchange):
            tempRate = {
                "fee_rate_buy": rate.get("sh_stock_sx",0) if exchange=='sh' else rate.get("sz_stock_sx",0),
                "fee_min_buy": rate.get("sh_stock_min_sx",0) if exchange=='sh' else rate.get("sz_stock_min_sx",0),
                "fee_addition_buy": rate.get("sh_stock_addition",0) if exchange=='sh' else rate.get("sz_stock_addition",0),
                "fee_rate_sell": rate.get("sh_stock_sx_sell",0) if exchange=='sh' else rate.get("sz_stock_sx_sell",0),
                "fee_min_sell": rate.get("sh_stock_min_sx_sell",0) if exchange=='sh' else rate.get("sz_stock_min_sx_sell",0),
                "fee_addition_sell": rate.get("sh_stock_addition_sell",0) if exchange=='sh' else rate.get("sz_stock_addition_sell",0),
                "fee_rate_etf_buy": rate.get("sh_etf_sx",0) if exchange=='sh' else rate.get("sz_etf_sx",0),
                "fee_min_etf_buy": rate.get("sh_etf_min_sx",0) if exchange=='sh' else rate.get("sz_etf_min_sx",0),
                "fee_addition_etf_buy": rate.get("sh_etf_addition",0) if exchange=='sh' else rate.get("sz_etf_addition",0),
                "fee_rate_etf_sell": rate.get("sh_etf_sx_sell",0) if exchange=='sh' else rate.get("sz_etf_sx_sell",0),
                "fee_min_etf_sell": rate.get("sh_etf_min_sx_sell",0) if exchange=='sh' else rate.get("sz_etf_min_sx_sell",0),
                "fee_addition_etf_sell": rate.get("sh_etf_addition_sell",0) if exchange=='sh' else rate.get("sz_etf_addition_sell",0),
                "fee_rate_gold_etf_buy": rate.get("sh_etf_gold_sx",0) if exchange=='sh' else rate.get("sz_etf_gold_sx",0),
                "fee_rate_reverse_repos_sell": rate.get("sh_repos_sx",0) if exchange=='sh' else rate.get("sz_repos_sx",0),
                "fee_min_reverse_repos_sell": rate.get("sh_repos_min_sx",0) if exchange=='sh' else rate.get("sz_repos_min_sx",0),
                "fee_max_reverse_repos_sell": rate.get("sh_repos_max_sx",0) if exchange=='sh' else rate.get("sz_repos_max_sx",0),
                "fee_rate_bond_buy": rate.get("sh_bond_sx",0) if exchange=='sh' else rate.get("sz_bond_sx",0),
                "fee_min_bond_buy": rate.get("sh_bond_min_sx",0) if exchange=='sh' else rate.get("sz_bond_min_sx",0),
                "fee_addition_bond_buy":rate.get("sh_bond_addition",0) if exchange=='sh' else rate.get("sz_bond_addition",0),
                "fee_rate_bond_sell": rate.get("sh_bond_sx_sell",0) if exchange=='sh' else rate.get("sz_bond_sx_sell",0),
                "fee_min_bond_sell": rate.get("sh_bond_min_sx_sell",0) if exchange=='sh' else rate.get("sz_bond_min_sx_sell",0),
                "fee_addition_bond_sell": rate.get("sh_bond_addition_sell",0) if exchange=='sh' else rate.get("sz_bond_addition_sell",0),
                "fee_rate_etf_creation": rate.get("sh_etf_creation",0) if exchange=='sh' else rate.get("sz_etf_creation",0),
                "fee_rate_etf_redemption": rate.get("sh_etf_redemption",0) if exchange=='sh' else rate.get("sz_etf_redemption",0),
                "fee_min_etf_creation_redemption": rate.get("sh_etf_min_cr",0) if exchange=='sh' else rate.get("sz_etf_min_cr",0),
                "fee_count_rate_etf_creation": rate.get("sz_etf_gh",0) if exchange=='sh' else rate.get("sz_etf_gh",0),
                "fee_count_rate_etf_redemption": rate.get("sh_etf_gh_redemption",0) if exchange=='sh' else rate.get("sz_etf_gh_redemption",0),
                "fee_rate_cross_etf_stock_buy": rate.get("cross_sh_stock_sx",0) if exchange=='sh' else rate.get("cross_sz_stock_sx",0),
                "fee_rate_tax_buy": rate.get("buy_yh",0),
                "fee_rate_tax_sell": rate.get("sell_yh",0.001)
            }
            return  tempRate
        #设置费率
        etfRate = commisionMap.get("etfRate",None)
        etfRateXTP = commisionMap.get("etfRateXTP",None)

        # logger.debug("etfRate:%s",str(etfRate))
        # logger.debug("etfRateXTP:%s",str(etfRateXTP))
        
        if(not etfRate):
            etfRate = {type:0} #默认
        if(not etfRateXTP):
            etfRateXTP = {type:1} #默认
        
        #默认xtp费率
        self.commissions = {
            "XTP":{
                "SSE": {
                    "fee_rate_buy": 0.00304,
                    "fee_min_buy": 6,
                    "fee_addition_buy": 0,
                    "fee_rate_sell": 0.00354,
                    "fee_min_sell": 8,
                    "fee_addition_sell": 0,
                    "fee_rate_etf_buy": 0.003,
                    "fee_min_etf_buy": 6,
                    "fee_addition_etf_buy": 0,
                    "fee_rate_etf_sell": 0.003,
                    "fee_min_etf_sell": 8,
                    "fee_addition_etf_sell": 0,
                    "fee_rate_gold_etf_buy": 0.003,
                    "fee_rate_reverse_repos_sell": 0.0003,
                    "fee_min_reverse_repos_sell": 3,
                    "fee_max_reverse_repos_sell": 0,
                    "fee_rate_bond_buy": 0.00306,
                    "fee_min_bond_buy": 5,
                    "fee_addition_bond_buy": 0,
                    "fee_rate_bond_sell": 0.00306,
                    "fee_min_bond_sell": 5,
                    "fee_addition_bond_sell": 0,
                    "fee_rate_etf_creation": 0.001,
                    "fee_rate_etf_redemption": 0.001,
                    "fee_min_etf_creation_redemption": 0,
                    "fee_count_rate_etf_creation": 0.0005,
                    "fee_count_rate_etf_redemption": 0.0005,
                    "fee_rate_cross_etf_stock_buy": 0.0005,
                    "fee_rate_tax_buy": 0,
                    "fee_rate_tax_sell": 0.0005
                },
                "SZE": {
                    "fee_rate_buy": 0.00304,
                    "fee_min_buy": 6,
                    "fee_addition_buy": 0,
                    "fee_rate_sell": 0.00354,
                    "fee_min_sell": 8,
                    "fee_addition_sell": 0,
                    "fee_rate_etf_buy": 0.003,
                    "fee_min_etf_buy": 6,
                    "fee_addition_etf_buy": 0,
                    "fee_rate_etf_sell": 0.003,
                    "fee_min_etf_sell": 8,
                    "fee_addition_etf_sell": 0,
                    "fee_rate_gold_etf_buy": 0.003,
                    "fee_rate_reverse_repos_sell": 0.0003,
                    "fee_min_reverse_repos_sell": 3,
                    "fee_max_reverse_repos_sell": 0,
                    "fee_rate_bond_buy": 0.00306,
                    "fee_min_bond_buy": 5,
                    "fee_addition_bond_buy": 0,
                    "fee_rate_bond_sell": 0.00306,
                    "fee_min_bond_sell": 5,
                    "fee_addition_bond_sell": 0,
                    "fee_rate_etf_creation": 0.001,
                    "fee_rate_etf_redemption": 0.001,
                    "fee_min_etf_creation_redemption": 0,
                    "fee_count_rate_etf_creation": 0.0005,
                    "fee_count_rate_etf_redemption": 0.0005,
                    "fee_rate_cross_etf_stock_buy": 0.0005,
                    "fee_rate_tax_buy": 0,
                    "fee_rate_tax_sell": 0.0005
                }
            }
        }
        
        username =  etfRate.get("username","")
        self.commissions[username] = {"SSE":convertRate(etfRate,"sh"),"SZE": convertRate(etfRate,"sz")}
        self.commissions[username+"_XTP"] ={"SSE":convertRate(etfRateXTP,"sh"),"SZE": convertRate(etfRateXTP,"sz")}
        
        '''
        TEMP_COMMISSION = {
                    "fee_rate_buy": 0.00304,
                    "fee_min_buy": 6,
                    "fee_addition_buy": 0,
                    "fee_rate_sell": 0.00354,
                    "fee_min_sell": 8,
                    "fee_addition_sell": 0,
                    "fee_rate_etf_buy": 0.003,
                    "fee_min_etf_buy": 6,
                    "fee_addition_etf_buy": 0,
                    "fee_rate_etf_sell": 0.003,
                    "fee_min_etf_sell": 8,
                    "fee_addition_etf_sell": 0,
                    "fee_rate_gold_etf_buy": 0.003,
                    "fee_rate_reverse_repos_sell": 0.0003,
                    "fee_min_reverse_repos_sell": 3,
                    "fee_max_reverse_repos_sell": 0,
                    "fee_rate_bond_buy": 0.00306,
                    "fee_min_bond_buy": 5,
                    "fee_addition_bond_buy": 0,
                    "fee_rate_bond_sell": 0.00306,
                    "fee_min_bond_sell": 5,
                    "fee_addition_bond_sell": 0,
                    "fee_rate_etf_creation": 0.001,
                    "fee_rate_etf_redemption": 0.001,
                    "fee_min_etf_creation_redemption": 0,
                    "fee_count_rate_etf_creation": 0.0005,
                    "fee_count_rate_etf_redemption": 0.0005,
                    "fee_rate_cross_etf_stock_buy": 0.0005,
                    "fee_rate_tax_buy": 0,
                    "fee_rate_tax_sell": 0.0005
                }
        self.commissions[username] = {"SSE":TEMP_COMMISSION,"SZE": TEMP_COMMISSION}
        self.commissions[username+"_XTP"] ={"SSE":TEMP_COMMISSION,"SZE": TEMP_COMMISSION}
        '''



    def add_book(self,key,fileName,isFirst,isRoot):
        try:
            local_db_path = os.path.join(self.dbPath,fileName)
            book = Book()
            book.name = fileName
            book.dbPath = self.dbPath
            book.init_book_tags(1,Source.XTP,"1","1","1")
            book.do_init_commissions(self.commissions)
            
            today=datetime.now()
            todayStr= today.strftime("%Y%m%d")
            if(isFirst or not os.path.exists(local_db_path)):#如果第一次启动
                #按照默认账号初始化book数据
                assets = self.smart.current_account.assets
                positions = []
                position_list = self.smart.current_account.position_list
                for pos in position_list:
                    instrument = self.smart.getInstrument(pos.instrument_id, pos.exchange_id)
                    instrumentType = instrument.instrument_type if instrument else InstrumentType.Unknown # 合约类型
                    positions.append({
                        "avg_open_price" : 0,
                        "close_price" : 0,
                        "direction" : pos.direction,
                        "exchange_id" : pos.exchange_id,
                        "frozen_total" : 0,
                        "frozen_yesterday" : 0,
                        "instrument_id" : pos.instrument_id,
                        "instrument_type" : instrumentType,
                        "last_price" : pos.last_price,
                        "margin" : 0,
                        "market_value" : pos.market_value,
                        "position_cost_price" : pos.position_cost_price,
                        "pre_close_price" : 0,
                        "profit_price" : pos.profit_price,
                        "purchase_redeemable_qty" : pos.purchase_redeemable_qty,
                        "realized_pnl" : 0,
                        "sellable" : pos.sellable_volume,
                        "uname" : "",
                        "unrealized_pnl" : 0,
                        "volume" : pos.volume,
                        "yesterday_volume" : pos.yesterday_volume,
                        "avg_open_price_td":0,
                        "profit_price_td":pos.profit_price
                    })

                paramObj = {
                    "trading_day":todayStr,
                    "initial_equity":assets.buying_power,
                    "static_equity":assets.buying_power,
                    "avail":assets.buying_power,
                    "frozen_cash":0,
                    "frozen_margin":0,
                    "intraday_fee":0,
                    "accumulated_fee":0,
                    "realized_pnl":0,
                    "avail_td":assets.buying_power,
                    "frozen_cash_td":0,
                    "intraday_fee_td":0,
                    "realized_pnl_td":0,
                    "positions": positions
                }
                
                book.do_init(paramObj) #初始化book上场数据
                book.dump() #第一次初始化参数存盘
            else: #继续上次存盘执行.
                def bookFilter(obj):
                    #是否是本策略的数据
                    mine = obj.traffic_sub_id == self.name
                    #是否是策略book还是资金子账号book
                    if(isRoot):
                        return mine
                    else:
                        return mine and obj.account_id==key

                hisOrders = list(filter(bookFilter,self.smart.current_account.order_list))
                hisTrades = list(filter(bookFilter,self.smart.current_account.trade_list))
                book.restore(hisOrders,hisTrades)
            
            #添加到book表
            self.bookMap[key] = book
        except Exception as err:
            logger.error(err,exc_info=True, stack_info=True)

    def dump(self):
        for bookName in self.bookMap:
            self.bookMap[bookName].dump()

    def on_order(self,order:Order):
        for bookName in self.bookMap:
            self.bookMap[bookName].on_order_impl(order)

    def on_trade(self,trade:Trade):
        for bookName in self.bookMap:
            self.bookMap[bookName].on_trade_impl(trade)

    def on_order_input(self,input):
        for bookName in self.bookMap:
            self.bookMap[bookName].on_order_input_impl(input)


    

    
