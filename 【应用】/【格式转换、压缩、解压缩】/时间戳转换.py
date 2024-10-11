import pandas as pd
df=pd.DataFrame({"timestamp_column":[20240321141821000]})
# # 将 16 位时间戳列转换为 datetime
# df['timestamp_column'] = pd.to_datetime(df['timestamp_column'].astype(int), unit='ms')
# 如果时间戳是以毫秒为单位的，可以使用以下代码
df['timestamp_column'] = pd.to_datetime((df['timestamp_column']).astype(int), unit='s')
# 确保转换后的列类型为 datetime
print(df)