#pip install akshare
import akshare as ak
import datetime
# df_cbonds=ak.bond_cb_redeem_jsl()#强制赎回信息【实时数据】
# df_cbonds["代码"]=df_cbonds["代码"].str.replace(r'\D','',regex=True).astype(str)
# print(f"去掉强制赎回之前,{len(df_cbonds)}")
# df_cbonds=df_cbonds[~(df_cbonds["强赎状态"]=="已公告强赎")]
# print(f"去掉强制赎回之后,{len(df_cbonds)}")
# df_cbonds["总市值"]=df_cbonds["现价"]*df_cbonds["剩余规模"]        
# df_cbonds["转股溢价率"]=df_cbonds["现价"]/((100/df_cbonds["转股价"])*df_cbonds["正股价"])
# df_cbonds["三低指数"]=df_cbonds["总市值"]*df_cbonds["转股溢价率"]
# df_cbonds["排名"]=df_cbonds["三低指数"].rank(method="max", ascending=True,na_option='bottom')
# # df_cbonds.to_csv("可转债强制赎回信息.csv")

# olddf=ak.bond_zh_cov_info_ths()
# olddf["代码"]=olddf["债券代码"].str.replace(r'\D','',regex=True).astype(str)
# olddf=olddf[olddf["到期时间"]>(datetime.datetime.now()+datetime.timedelta(days=180)).date()]
# print(f"当前展示K线,{len(olddf)}")
# # olddf.to_csv("债券评级同花顺.csv")
# df_cbonds=df_cbonds[df_cbonds["代码"].isin(olddf["代码"].tolist())]
# print(f"去掉到期时间之后,{len(olddf)}")

df=ak.fund_etf_spot_em()#ETF实时行情
print(df)
df=ak.fund_etf_hist_em(
    symbol="159707",
    period= "daily",
    start_date= "19700101",
    end_date= "20500101",
    adjust= "",
    )#ETF历史行情