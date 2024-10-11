# pip install openai
from openai import OpenAI
import pandas as pd
import requests
import time
import os
key = "sk-KpnJWmRnAql3PzY2VHLlZIGaqCv6xKikYxJxGmNxxPiNn0NX"# kimi
# # client = OpenAI(
# #     base_url="https://llm.loux.cc/v1", 
# #     api_key=key
# # )#原chatgpt的调用方式
client = OpenAI(
    base_url="https://api.moonshot.cn/v1", # <-- 将 base_url 从 https://api.openai.com/v1 替换为 https://api.moonshot.cn/v1
    api_key=key, # <--在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
)#kimi的调用方式
# 【限速说明：并发数1，TPM32000，RPM3，TPDunlimited。一分钟最多调用3次，一天最多1500000token】






# #【语言对话】
# def chat(msg: str, model="moonshot-v1-8k"):#model需要换掉
#     """对话模型"""
#     completion = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": msg},
#         ]
#     )
#     return completion.choices[0].message.content
# # 对话
# print(chat("告诉我如何成为伟大的人"))



# #【文件解读】
# from pathlib import Path
# file_object = client.files.create(file=Path(r"C:\Users\13480\gitee\trade\【应用】\图片去背景\图片去背景.jpg"), purpose="file-extract")
# # 获取结果
# # file_content = client.files.retrieve_content(file_id=file_object.id)
# # 注意，之前 retrieve_content api 在最新版本标记了 warning, 可以用下面这行代替
# # 如果是旧版本，可以用 retrieve_content
# file_content = client.files.content(file_id=file_object.id).text
# print("file_content",file_content)
# # 把它放进请求中
# messages = [
#     {
#         "role": "system",
#         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
#     },
#     {
#         "role": "system",
#         "content": file_content,
#     },
#     {"role": "user", "content": "请提取文字当中的内容"},
# ]
# # 然后调用 chat-completion, 获取 Kimi 的回答
# completion = client.chat.completions.create(
#   model="moonshot-v1-32k",
#   messages=messages,
#   temperature=0.3,
# )
# print(completion.choices[0].message)



# #【单个文件转CSV】
# from pathlib import Path
# # filepath=Path(r"C:\Users\13480\gitee\trade\【应用】\【自动化windows】WeChat\微信自动化【OCR】WeChatOCR\02-1.png")
# filepath=Path(r"C:\Users\13480\gitee\trade\【应用】\【自动化windows】WeChat\微信自动化【机器人】大模型客服\一分一档数据\1.png")
# # filepath=Path(r"C:\Users\13480\gitee\trade\高考志愿填报系统\河北省2024高考一分一档和投档线\20240624195327_41.pdf")
# file_object = client.files.create(file=filepath,purpose="file-extract")
# # 获取文件读取结果
# # file_content = client.files.retrieve_content(file_id=file_object.id)#旧版本retrieve_content
# file_content = client.files.content(file_id=file_object.id).text
# print("file_content",file_content)
# # 将字符串转换为CSV
# row = file_content.strip().split('\n')[0]#格式其实是字符串列表，这里取第一个
# print("row",row)
# cells = row.split('|')[1:-1] # 删掉第一行和最后一行
# print(cells,type(cells))#这个是列表
# #数据处理【逐行拼接df并生成csv文件】
# allrow =[]
# thisrow=[]
# for cell in cells:
#     print("cell",cell)#对列表当中的逐个元素进行处理
#     # cell = cell.strip()#这里是只保留非空数据了【不应该这样变相去掉了空数据】
#     if cell==rf"\n":
#         allrow.append(thisrow)
#         thisrow=[]
#         print("allrow",allrow)
#     else:
#         if cell:# Skip empty cells
#             thisrow.append(cell)
#             print("thisrow",thisrow)
# if len(allrow)==0:#用唯一一行替代
#     allrow=thisrow
# else:#把最后一行填回来
#     allrow.append(thisrow)
# thisdf=pd.DataFrame(allrow)
# thisdf.to_csv("thisdf.csv")
# # 对上传之后的文件进行二次请求处理
# messages = [
#     {
#         "role": "system",
#         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
#     },
#     {
#         "role": "system",
#         "content": file_content,
#     },
#     {"role": "user", "content": "转csv"},#我想要csv文件
# ]
# # 然后调用 chat-completion, 获取 Kimi 的回答
# completion = client.chat.completions.create(
#   model="moonshot-v1-32k",
#   messages=messages,
#   temperature=0.3,
# )
# thismessage=completion.choices[0].message
# print(thismessage,type(thismessage))









# #【批量文件转CSV】有可能识别出来缺一行
alldf=pd.DataFrame({})
import os
from pathlib import Path
# 指定要上传文件的文件夹路径
folder_path = r"C:\Users\13480\gitee\trade\高考志愿填报系统\河北省2024高考一分一档和投档线\一分一档数据"
# folder_path = r"C:\Users\13480\gitee\trade\高考志愿填报系统\河北省2024高考一分一档和投档线"
# 遍历文件夹中的所有PNG文件
for file_name in os.listdir(folder_path):
    time.sleep(20)
    if file_name.endswith(".png"):
        file_path = os.path.join(folder_path, file_name)
        file_object = client.files.create(file=Path(file_path),purpose="file-extract")
        # 获取文件读取结果
        # file_content = client.files.retrieve_content(file_id=file_object.id)#旧版本retrieve_content
        file_content = client.files.content(file_id=file_object.id).text
        print("file_content",file_content)
        # 将字符串转换为CSV
        row = file_content.strip().split('\n')[0]#格式其实是字符串列表，这里取第一个
        print("row",row)
        cells = row.split('|')[1:-1] # 删掉第一行和最后一行
        print(cells,type(cells))#这个是列表
        #数据处理【逐行拼接df并生成csv文件】
        allrow =[]
        thisrow=[]
        for cell in cells:
            # print("cell",cell)#对列表当中的逐个元素进行处理
            # cell = cell.strip()#这里是只保留非空数据了【不应该这样变相去掉了空数据】
            if cell==rf"\n":
                allrow.append(thisrow)
                thisrow=[]
                # print("allrow",allrow)
            else:
                if cell:# Skip empty cells
                    thisrow.append(cell)
                    # print("thisrow",thisrow)
        if len(allrow)==0:#用唯一一行替代
            allrow=thisrow
        else:#把最后一行填回来
            allrow.append(thisrow)
        thisdf=pd.DataFrame(allrow,columns=["分数档次", "物理人数", "物理累计人数", "历史人数", "历史累计人数"])
        thisdf=thisdf.iloc[3:]#去掉前三行【或者以第一行为索引去掉剩下的两行】
        thisdf.to_csv(f"{file_path}处理后.csv")
        print(thisdf)
        alldf=pd.concat([alldf,thisdf])
# # 以“分数档次”列排序并重置索引
# alldf = alldf.sort_values(by="分数档次", ascending=False)#False是降序排列
# alldf = alldf.reset_index(drop=True)
# alldf.to_csv("alldf.csv")