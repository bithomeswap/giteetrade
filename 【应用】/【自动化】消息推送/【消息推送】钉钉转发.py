import pandas as pd
import requests
def postmessage(title,df):
    message = df.to_markdown()
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=f5a623f7af0ae156047ef0be361a70de58aff83b7f6935f4a5671a626cf42165"
    test=requests.post(
        webhook,
        json={
            "msgtype": "markdown",
            "markdown": {"title": title, "text": message},
        },
        ##可能是文件大小受限制无法发送
        # json={
        #     "msgtype": "file",
        #     "file": {
        #         "media_id": "",
        #         "file_name": "data.csv",
        #         "file_type": "csv",
        #         "content": df.to_csv(index=False)
        #     }
        # },
    )
    print(test)
postmessage("测试",pd.DataFrame({"代码":[000000],"内容":["内存"]}))