import akshare as ak
import pandas as pd
import datetime
from pymongo import MongoClient
import time
import pytz

client = MongoClient(
    "mongodb://wth000:wth000@43.159.47.250:27017/dbname?authSource=wth000")
db = client["wth000"]
names = [("000","001","002","600","601","603","605")]

# # 获取当前日期
# start_date = "20190101"
# current_date = datetime.datetime.now()
# end_date = current_date.strftime("%Y%m%d")
# # 从akshare获取A股主板股票的代码和名称
codes = ak.stock_zh_a_spot_em()
# # 过滤掉危险股票
# codes = codes[~codes["名称"].str.contains("S")]
# # 过滤掉退市股票
# codes = codes[~codes["名称"].str.contains("退")]
for name in names:
    try:
        collection = db[f"股票30分钟{name}"]
        df = pd.DataFrame()
        df = codes[codes["代码"].str.startswith(name)][["代码","名称"]].copy()
        # 遍历目标指数代码，获取其分钟K线数据
        for code in df["代码"]:
            # print(code)
            latest = list(collection.find({"代码": float(code)},{"timestamp": 1}).sort("timestamp",-1).limit(1))
            # print(latest)
            if len(latest) == 0:
                upsert_docs = True
                # start_date_query = start_date
            else:
                upsert_docs = False
                latest_timestamp = latest[0]["timestamp"]
            try:
                # 通过 akshare 获取目标指数的日K线数据
                k_data = ak.stock_zh_a_hist_min_em(symbol=code,period="30")
                k_data["代码"] = float(code)
                k_data["成交量"] = k_data["成交量"].apply(lambda x: float(x))
                k_data["日期"] = k_data["时间"]
                # k_data["timestamp"] = k_data["日期"].apply(lambda x: float(datetime.datetime.strptime(x,"%Y-%m-%d").replace(tzinfo=pytz.timezone("Asia/Shanghai")).timestamp()))
                k_data["timestamp"] = k_data["日期"].apply(lambda x: float(datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.timezone("Asia/Shanghai")).timestamp()))
                k_data = k_data.sort_values(by=["代码","日期"])
                docs_to_update = k_data.to_dict("records")
                if upsert_docs:
                    # print(f"{name}({code}) 新增数据")
                    try:
                        collection.insert_many(docs_to_update)
                    except Exception as e:
                        pass
                else:
                    bulk_insert = []
                    for doc in docs_to_update:
                        if doc["timestamp"] > latest_timestamp:
                            # 否则，加入插入列表
                            bulk_insert.append(doc)
                        if doc["timestamp"] == float(latest_timestamp):
                            try:
                                collection.update_many({"代码": doc["代码"],"日期": doc["日期"]},{
                                    "$set": doc},upsert=True)
                            except Exception as e:
                                pass
                    # 执行批量插入操作
                    if bulk_insert:
                        try:
                            collection.insert_many(bulk_insert)
                        except Exception as e:
                            pass
            except Exception as e:
                print(e,f"因为{code}停牌")
        print("任务已经完成")
    except Exception as e:
        print(e)
# limit = 600000
# if collection.count_documents({}) >= limit:
#     oldest_data = collection.find().sort([("日期",1)]).limit(
#         collection.count_documents({})-limit)
#     ids_to_delete = [data["_id"] for data in oldest_data]
#     collection.delete_many({"_id": {"$in": ids_to_delete}})
# print("数据清理成功")