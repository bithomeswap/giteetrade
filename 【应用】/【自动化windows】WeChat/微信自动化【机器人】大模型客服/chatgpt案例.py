# pip install openai
from openai import OpenAI
import requests
import time
import os

# org-GFzJAgVTUGEraoeQAXWsIyNa
# sk-aCtm9Srvha9t3xgyE3Ad66241eA94eA1Ad714c870a635330#他人的API
key = "sk-aCtm9Srvha9t3xgyE3Ad66241eA94eA1Ad714c870a635330"# $10

client = OpenAI(
    base_url="https://llm.loux.cc/v1", 
    api_key=key
)

def chat(msg: str, model="gpt-4o"):
    """对话模型"""
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": msg},
        ]
    )
    return completion.choices[0].message.content

def draw(prompt: str):
    """文生图模型"""
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    if response.data:
        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt
        print(revised_prompt)
    elif response.error:
        raise Exception(response.error['message'])
    
    # 下载图片
    response = requests.get(image_url)
    image = response.content
    
    # 保存图片
    if not os.path.exists("image"):
        os.makedirs("image")
    imagepath = os.path.realpath(f"image/image_{time.strftime('%Y%m%d%H%M%S')}.jpg")
    with open(imagepath, "wb") as f:
        f.write(image)
    
    return imagepath

def balance(key):
    """查询余额"""
    response = requests.get(f'https://llm.loux.cc/balance?key={key}')
    return response.json()

if __name__ == '__main__':#最近有IP限制了
    # 对话
    print(chat("告诉我如何成为伟大的人"))
    # 画图
    print(draw("漂亮的女生"))
