# 【在必选专业：历史、物理的基础上按照分数排名，物理和化学绑定，历史和政治绑定】志愿号是该考生第多少个志愿，就是指学校录取的所有考生中最大的志愿序号，即该校最低录到了第几志愿
# 这几个文件来自河北省教育考试院
# pip install pandas openpyxl
import pandas as pd
df = pd.read_excel(rf"C:\Users\13480\gitee\trade\高考志愿填报系统\【MBIT性格测试】\MIT测试导入数据.xlsx", engine='openpyxl')
print(df)
df.to_csv("性格试题.csv", index=False)
df = pd.read_excel(rf"C:\Users\13480\gitee\trade\高考志愿填报系统\【MBIT性格测试】\MIT计算结果解释数据导入.xlsx", engine='openpyxl')
print(df)
df.to_csv("性格测试结果.csv", index=False)

