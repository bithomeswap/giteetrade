#投资者账户 
import datetime


InvestorID="00030557";   
'''
该默认账号为共用连通测试使用,自有测试账号请到n-sight.com.cn注册并从个人中心获取交易编码,不是网站登录密码,不是手机号
实盘交易时，取客户号，请注意不是资金账号或咨询技术支持
'''
#操作员账户
UserID="00030557";	   #同客户号保持一致即可
#资金账户 
AccountID="00030557";		#以Req(TradingAccount)查询的为准
#登陆密码
Password="17522830";		#N视界注册模拟账号的交易密码，不是登录密码
DepartmentID="0001";		#生产环境默认客户号的前4位
SSE_ShareHolderID='A00030557'   #不同账号的股东代码需要接口ReqQryShareholderAccount去查询
SZ_ShareHolderID='700030557'    #不同账号的股东代码需要接口ReqQryShareholderAccount去查询

# 仿真
# 行情：tcp://210.14.72.21:4402  
# 交易：tcp://210.14.72.21:4400
# 交易、行情fens地址：
# tcp://210.14.72.21:42370
# A套：
# 行情前置地址：tcp://210.14.72.16:9402
# 交易前置地址：tcp://210.14.72.15:4400
# B套：
# 行情前置地址：tcp://210.14.72.16:9402
# 交易前置地址：tcp://210.14.72.16:9500
# #【仿真】
# marketurl="tcp://210.14.72.21:4402"
# tradeurl="tcp://210.14.72.21:4400"
#【A套】
marketurl="tcp://210.14.72.16:9402"
tradeurl="tcp://210.14.72.15:4400"
# #【B套】
# marketurl="tcp://210.14.72.16:9402"
# tradeurl="tcp://210.14.72.16:9500"

#确认当日时间
start_time=datetime.datetime.now().strftime("%Y%m%d")#特殊的时间格式
interval=5#控制请求频率[针对循环型请求]

