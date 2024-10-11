# pip install wxauto
from wxauto import WeChat
import time
import random
# pip install zhipuai
from zhipuai import ZhipuAI
client = ZhipuAI(api_key="ff79b8184df39ff7cc9b5a4f94d9e437.z7fwnYYUgqQToiZ6") # 请填写您自己的APIKey
def AIchat(content):
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": "你是一名非常优秀的计算机工程师，请用一段完整的话告诉我答案。"+content},
        ],
        stream=False,#是否启动流式回答
        temperature=0.8,
        # temperature: 这个参数用于控制生成文本的创造性或者说是随机性。temperature 的值范围通常是0到1。当 temperature 值较高时，生成的文本会更加多样和不可预测；当 temperature 值较低时，生成的文本会更加稳定和可预测。在这个例子中，temperature 设置为0.8，意味着生成的文本会相对多样，但不会完全随机。
        seed=random.randint(0, 1000),
        # seed: 这个参数用于设置随机数生成器的初始值。在文本生成中，使用 seed 可以确保在相同的输入下，每次生成的文本是一致的。这对于调试和复现结果非常有用。在这个例子中，seed 是通过 random.randint(0, 1000) 随机生成的一个介于0到1000之间的整数。
        )
    print(response.choices[0].message.content,type(response.choices[0].message.content))
    reply=response.choices[0].message.content
    return reply

wx = WeChat()
# 指定监听目标
listen_list = [
    '自动化测试',
    '王腾鹤',
]
for i in listen_list:
    wx.AddListenChat(who=i)  # 添加监听对象
    
# 持续监听消息，有消息则对接大模型进行回复
wait = 1  # 设置1秒查看一次是否有新消息
while True:
    msgs = wx.GetListenMessage()
    print(msgs)
    for chat in msgs:#遍历每一个聊天对话框
        msg = msgs.get(chat)# 获取消息内容
        print("沟通对象",chat,"聊天信息",msg,type(msgs))
        #msg[-1]这个是怕消息过多只选择最后一条进行回复
        if (msg[-1][0] == 'Self') and(
            "本人消息" not in msg[-1][1]#避免回复本人消息
            ):
            # ===================================================
            # 处理消息逻辑
            reply = AIchat(msg[-1][1])
            # ===================================================
            # 回复消息
            chat.SendMsg("本人消息【无需回复】"+reply)
        if (msg[-1][0] == 'friend'):
            # ===================================================
            # 处理消息逻辑
            reply = AIchat(msg[-1][1])
            # ===================================================
            # 回复消息
            chat.SendMsg(reply)
    time.sleep(wait)
