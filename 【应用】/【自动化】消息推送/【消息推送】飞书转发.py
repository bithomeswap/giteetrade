import pandas as pd
import requests
def postmessage(title,df):
    message = df.to_markdown()
    webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/04d50505-1300-4b90-b8cd-d583ca31ffb0"
    test=requests.post(
        webhook,

        headers = {
            "Authorization": "Bearer YOUR_ACCESS_TOKEN",
            "Content-Type": "application/json"
        },
        json={"msg_type": "text",
              "content": {"text": message}
        },

        ##请求体大小不能超过 20 K因而下面的文件无法发送
        # headers = {
        #     "Authorization": "Bearer {ACCESS_TOKEN}",
        #     "Content-Type": "multipart/form-data"
        # },
        # files={
        #     "chat_id": "{CHAT_ID}",
        #     "file": ("data.csv", df.to_csv(index=False).encode('utf-8'))
        # },
    )
    print(test)
    
postmessage("测试",pd.DataFrame({"代码":[000000],"内容":["内存"]}))
