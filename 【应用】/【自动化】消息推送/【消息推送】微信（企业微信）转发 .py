import pandas as pd
import requests
def postmessage(title,df):
    key="4c5b0199-f549-4f63-b70f-bbaa823d3fcb"
    postwebhook=f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file"
    # 上传文件
    file_path=r"C:\Users\13480\gitee\quant\【本地选股（A股）】SDK\【行业】聚宽一级行业对照表.csv"
    response = requests.post(postwebhook, files={'media': open(file_path, 'rb')})
    print(response.json()["media_id"])
    id=response.json()["media_id"]

    webhook = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    test=requests.post(
        webhook,

        # json={
        #     "msgtype": "text",
        #     "text": {
        #         "content": "广州今日天气：29度，大部分多云，降雨概率：60%",
        #         "mentioned_list":["wangqing","@all"],
        #         "mentioned_mobile_list":["13800001111","@all"]
        #     }
        # },
        
        json={
            "msgtype": "file",
            "file": {
                "media_id": id
            }
        },
    )
    print(test.json())
postmessage("测试",pd.DataFrame({"代码":[000000],"内容":["内存"]}))