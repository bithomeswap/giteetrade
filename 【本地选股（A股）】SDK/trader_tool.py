from trader_tool.dfcf_etf_data import dfcf_etf_data
api=dfcf_etf_data()
df=api.get_all_etf_data_1()
print(df)