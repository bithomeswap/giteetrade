import pandas as pd
timetarget="floattoday"
df=pd.read_csv(rf"C:\Users\13480\Desktop\quant\printdf.csv")
# 日期截取
datelist=df[timetarget].unique().tolist() # 获取观察周期的所有日期数据
testdays=20#只要最后testdays日期的数据
# testdays=len(datelist)#截取全部数据
print("日期截取前",len(df))
dateprediction=datelist[len(datelist)-testdays]
print("截取日期",dateprediction)
df=df[df[timetarget]>=dateprediction]
print("日期截取后",len(df))
df.to_csv("printdf截取后.csv")