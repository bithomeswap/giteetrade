import quandl
quandl.ApiConfig.api_key = '2Yyoynu4pLC_NpyNnFfG'#注册quandl免费账号，获取并配置自己的API_key
#获取美国季度GDP
data = quandl.get('FRED/GDPPOT')
print(data.head())
# #获取固定期限的GDP
# data = quandl.get("FRED/GDP", start_date="2001-12-31", end_date="2005-12-31")
# print(data.head())

# # 获取特定列的数据：
# data = quandl.get(["NSE/OIL.1", "WIKI/AAPL.4"])
# print(data)
# # 获取特定行的数据：
# data = quandl.get("WIKI/AAPL", rows=5) #后5行
# print(data)

#获取整个数据表
data = quandl.get_table('MER/F1', paginate=True)
print(data.head())