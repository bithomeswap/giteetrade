# #【同花顺APP上有申赎清单信息，但是没接口拿到】
# #【iopv数据据说软件上的计算方式有延迟，而且抢的人多肯定要高频低延迟才能抢到】
# # 集思录的ETF净值数据比问财出来的速度快【估值就是iopv，现价除以估值就是溢价率】
# # 爬虫循环获取网页信息比较可靠【每一个基金也可以单独获取申赎额度等信息】
# # 集思录ETF净值数据地址：https://www.jisilu.cn/data/etf/#index
# # 景顺长城申赎详情：https://www.igwfmc.com/main/jjcp/product/513980/detail.html
# # 国联安申赎详情：https://www.cpicfunds.com/product/516480/index.shtml
import requests
import pandas as pd
import time
def getiopv():
    #cookie和headers加一下，不然他们知道你用的python
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.jisilu.cn/data/etf/",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }
    cookies = {
        "kbzw__Session": "j5stpa4friur6i24dqae5dnnp1",
        "kbz_newcookie": "1"
    }
    url = "https://www.jisilu.cn/data/etf/etf_list/"#查调出来的数据库链接
    params = {
        "___jsl": "LST___t=1729680229839",
        "volume": "",
        "unit_total": "",
        "rp": "25"
    }
    params["___jsl"] = f"LST___t={int(time.time()*1000)}"
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    print(response.text)
    print(response)
    df = pd.DataFrame([row["cell"] for row in response.json()["rows"]])#这个里面有iopv数据
    # # 目标网页URL【直接抓实时的iopv数据】
    # url = r'https://www.jisilu.cn/data/etf/etf_list/'#["rows"]这个ETF数据游客就能查看，或者使用针对性链接https://www.jisilu.cn/data/etf/etf_list/?___jsl=LST___t=1729690579460&rp=25&page=1%20%E8%AF%B7%E6%B1%82%E6%96%B9%E6%B3%95:%20GET
    # # "https://app.jisilu.cn/data/cbnew/cb_list_new/"#["data"]这个可转债数据需要开会员才能看【也就是后缀加上东西才行】
    # df.to_csv("etf.csv",index=False)
    return df