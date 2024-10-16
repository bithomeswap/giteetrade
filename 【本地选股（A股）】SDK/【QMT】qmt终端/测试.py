# coding:gbk[失灵时不利的]
import datetime
def init(C):
	pass
	
def handlebar(C):
	trade=True
	while True:
		if trade==True:
			thisnow = datetime.datetime.now().strftime("%Y%m%d")
			print("当前时间",thisnow)
			print(get_etf_iopv("510050.SH"))
			trade=False