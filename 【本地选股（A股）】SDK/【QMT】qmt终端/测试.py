# coding:gbk
#非交易时间无法使用
import datetime
def init(C):
	C.trade=True
	pass
	
def handlebar(C):
	while True:
		if C.trade==True:
			thisnow = datetime.datetime.now().strftime("%Y%m%d")
			print("当前时间",thisnow)
			print(get_etf_iopv("510050.SH"))
			C.trade=False