# pip install wxpusher
from wxpusher import WxPusher
# 发布到微信机器人
def postmessage(text):
    # # 查询用户
    # # query_user=WxPusher.query_user("<page>","<page_size>","<appToken>")
    # for pagenum in range(1,5):
    #     uidslist=[]
    #     query_user=WxPusher.query_user(str(pagenum),"50","AT_tFRZgjToc6XnG5dzR2MGyv1DzECNYOIU")
    #     # print(query_user["data"]["records"])
    #     if len(query_user["data"]["records"])>0:
    #         for query in query_user["data"]["records"]:
    #             print(query["uid"])
    #             uidslist.append(query["uid"])
    #             # UID_4HGW0dvl7EA7zaZLYe8bjegTSZFS # 姨父畅海东UID
    # # 发送消息
    # # WxPusher.send_message('<content>',
    # #                       uids=['<uids>'],
    # #                       topic_ids=['<topic_ids>'],
    # #                       token='<appToken>')      
    message=WxPusher.send_message(
        "【风险提示】本消息仅作为策略演示及研究使用，严禁任何个人或组织以此作为投资依据，因为使用或者传播本订阅信息而产生的任何风险由使用者自行承担。\n"+
        "【策略说明】状态列为初始建仓说明标的低估适合建仓，如果某持仓股票不在状态列为持仓观察的标的当中，说明风险加大不宜继续持有。\n"+
        str(text),
        uids=["UID_qkmjMTBknX0I5ZZoVY3IBFv7WVV1"],
        # uids=uidslist,
        topic_ids=["12417"],
        token="AT_tFRZgjToc6XnG5dzR2MGyv1DzECNYOIU",
    )
    messageId=message["data"][0]["messageId"]
    print(message,messageId)
    # # 查询消息是否发送成功【其实是发送错误】
    # query_message=WxPusher.query_message(f"{messageId}")
    # print(query_message)
postmessage("测试")