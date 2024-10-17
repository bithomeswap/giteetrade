# 大qmt跟ptrade有些像，但比ptrade复杂一些，速度会慢一点，毕竟QMT终端内置的python3.6.8框架，版本有点旧。



# # coding:gbk
# #非交易时间无法使用
# import datetime
# def init(C):
# 	C.trade=True
# 	pass
	
# def handlebar(C):
# 	while True:
# 		if C.trade==True:
# 			thisnow = datetime.datetime.now().strftime("%Y%m%d")
# 			print("当前时间",thisnow)
# 			print(get_etf_iopv("510050.SH"))
# 			C.trade=False



# coding:gbk
#非交易时间无法使用
import time
import datetime
import pandas as pd
def init(C):
	pass
	
def handlebar(C):
	#realtime=C.get_bar_timetag(C.barpos)
	#print(realtime)
	thisnow = datetime.datetime.now()#.strftime("%Y%m%d")
	print("当前时间",thisnow.time(),type(datetime.timedelta(days=366)),type(thisnow.time()),type(datetime.time()),type(datetime.time(9,55)))
	if((thisnow.time()>datetime.time(9,45)
	)and(thisnow.time()<datetime.time(11,20))
	)or((thisnow.time()>datetime.time(13,5)
	)and(thisnow.time()<datetime.time(14,50))):
		print("选股前先获取持仓信息")
		#获取中小综指成分股
		stocks=C.get_sector('399101.SZ')
		print(type(stocks),stocks)
		startDate = (thisnow-datetime.timedelta(days=366)).strftime("%Y%m%d")
		endDate = thisnow.strftime("%Y%m%d")
		print(startDate,endDate)
		fieldList = [
		'CAPITALSTRUCTURE.total_capital',#总股本
		'ASHAREINCOME.net_profit_incl_min_int_inc',#净利润
		]
		df=C.get_financial_data(fieldList,stocks,startDate,endDate,report_type='report_time')
		#print(df.minor_xs(df.minor_axis[0]))#总股本是空值
		#print(df.minor_xs(df.minor_axis[1]))#净利润是空值
		#thisdf=df.minor_xs(df.minor_axis[1]).dropna()#都是空值
		#print(thisdf)
		