import requests

url = "http://124.221.229.164:18011"

def sign_tc3(*args,**kwargs):
    signature = ""
    try:
        data = {
            "method":"sign_tc3",
            "args":args,
            "kwargs":kwargs,
        }
        response = requests.post(url=url,json=data)
        signature = response.json()
    except Exception as e:
        print(e)
    return signature
