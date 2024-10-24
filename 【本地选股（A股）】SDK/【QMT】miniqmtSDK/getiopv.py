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
def getiopv():#有可能错误的参数会导致报错
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
    # print(response.text)
    # print(response)
    df = pd.DataFrame([row["cell"] for row in response.json()["rows"]])#这个里面有iopv数据
    # # 目标网页URL【直接抓实时的iopv数据】
    # url = r'https://www.jisilu.cn/data/etf/etf_list/'#["rows"]这个ETF数据游客就能查看，或者使用针对性链接https://www.jisilu.cn/data/etf/etf_list/?___jsl=LST___t=1729690579460&rp=25&page=1%20%E8%AF%B7%E6%B1%82%E6%96%B9%E6%B3%95:%20GET
    # # "https://app.jisilu.cn/data/cbnew/cb_list_new/"#["data"]这个可转债数据需要开会员才能看【也就是后缀加上东西才行】
    # df.to_csv("etf.csv",index=False)
    return df

# #【上交所】ETF申赎清单【上交所官网有公布各个标的的申赎清单】这个是政府网站，不好直接爬怕有风险，尽量逐个基金去试。【爬取的时候cookie错了不一定拿不到数据】
# https://www.sse.com.cn/disclosure/fund/etflist/detail.shtml?fundid=510010
# 【大机构可以跟基金公司实时保持联系，能够实时沟通确认是否有可以进行交易的额度，有额度才执行交易，没额度有可能无法进行兑换从而实现变相t+0卖掉】
# 爬虫注意事项【通常一个请求包含，网址，查询参数，请求头，请求数据，四个要素。有的直接访问网址是没有用的。】
import requests
def getetflist():#把下面的数据获取挪进来
    pass
# #同一标的当中只有params参数下的"sqlId"不同，headers和url是完全相同的
# #不同标的除了这些不同以外cookies的"JSESSIONID"、"ba17301551dcbaf9_gdp_sequence_ids"字段不同且
# #不同标的除了这些不同以外params的"jsonCallBack"、"FUNDID2":、"_"也不同
# headers = {
#     "Accept": "*/*",
#     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "Connection": "keep-alive",
#     "Referer": "https://www.sse.com.cn/",
#     "Sec-Fetch-Dest": "script",
#     "Sec-Fetch-Mode": "no-cors",
#     "Sec-Fetch-Site": "same-site",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
#     "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\""
# }
# cookies = {
#     "gdp_user_id": "gioenc-338g33c3%2C5dad%2C5b9c%2Cae16%2C40d8da152d19",
#     "ba17301551dcbaf9_gdp_session_id": "8c62574c-45f2-4a1e-9dbb-e8fd1c2fa7d3",
#     "ba17301551dcbaf9_gdp_session_id_sent": "8c62574c-45f2-4a1e-9dbb-e8fd1c2fa7d3",
#     "JSESSIONID": "BB6F9C0D77808A93E4509A4089F665D8",
#     "ba17301551dcbaf9_gdp_sequence_ids": "{%22globalKey%22:83%2C%22VISIT%22:7%2C%22PAGE%22:38%2C%22VIEW_CLICK%22:40}"
# }
# url = "https://query.sse.com.cn/commonQuery.do"

# params = {
#     "jsonCallBack": "jsonpCallback48895506",
#     "isPagination": "false",
#     "FUNDID2": "510010",
#     "sqlId": "COMMON_SSE_CP_JJLB_ETFJJGK_GGSGSHQD_JBXX_C",#这个ID是查询申赎信息的
#     "_": "1729730327153"
# }
# response = requests.get(url, headers=headers, cookies=cookies, params=params)
# print(response.text)
# print(response)

# params = {
#     "jsonCallBack": "jsonpCallback34883042",
#     "isPagination": "false",
#     "FUNDID2": "510010",
#     "sqlId": "COMMON_SSE_CP_JJLB_ETFJJGK_GGSGSHQD_COMPONENT_C",#这个ID是查询申赎清单的
#     "_": "1729730327154"
# }
# response = requests.get(url, headers=headers, cookies=cookies, params=params)
# print(response.text)
# print(response)
# #【查询其他标的】
# cookies = {
#     "gdp_user_id": "gioenc-338g33c3%2C5dad%2C5b9c%2Cae16%2C40d8da152d19",
#     "ba17301551dcbaf9_gdp_session_id": "8c62574c-45f2-4a1e-9dbb-e8fd1c2fa7d3",
#     "ba17301551dcbaf9_gdp_session_id_sent": "8c62574c-45f2-4a1e-9dbb-e8fd1c2fa7d3",
#     "JSESSIONID": "EA863A7651037EA45807287F7126DA6B",
#     "ba17301551dcbaf9_gdp_sequence_ids": "{%22globalKey%22:91%2C%22VISIT%22:7%2C%22PAGE%22:40%2C%22VIEW_CLICK%22:46}"
# }
# url = "https://query.sse.com.cn/commonQuery.do"
# params = {
#     "jsonCallBack": "jsonpCallback69324494",
#     "isPagination": "false",
#     "FUNDID2": "510710",
#     "sqlId": "COMMON_SSE_CP_JJLB_ETFJJGK_GGSGSHQD_JBXX_C",
#     "_": "1729734619942"
# }



# # 【从基金公司获取】这个也需要挂headers、cookie，否则就是非法请求，cookie有错误也能请求成功
# import requests
# import json
# headers = {
#     "Accept": "*/*",
#     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "Connection": "keep-alive",
#     "Content-Type": "application/json; charset=UTF-8",
#     "Origin": "https://e.gtfund.com",
#     "Referer": "https://e.gtfund.com/Etrade/Jijin/view/id/511010",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-origin",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
#     "X-Requested-With": "XMLHttpRequest",
#     "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\""
# }
# cookies = {
#     # "PHPSESSID": "027bed367ea2b56bb62a6a8498712edf",
#     # "clientId": "gtfund-67187f057b19f6.20045771",
#     # "HMF_CI": "8b37b4da167f5a2c6583c61502764e2452dc6fe314c5817e9ad49d7cdf567d63b686e9f802f6019b8e4b02d2171ffd0c2ca37b40adfdad65e678bdc945a5cdbaf7",
#     # "Hm_lvt_c741085096d4baa2cc9aa13db2549f58": "1729658632,1729729535",
#     # "HMACCOUNT": "CF91E0E2B0F6C46C",
#     # "HMY_JC": "c0194280c700f08d5b7f0761a68b51364fba07cf4354afa7ea59fecdaee7078561,",
#     # "HBB_HC": "449f5cb1684215e72ac98add835f9b8f735ce18c94244635a3d4b05a34bf2c91461d4e7c5cd94887d3d5802a1b9a2db0b4",
#     # "C3VK": "d1e5f2",
#     # "Hm_lpvt_c741085096d4baa2cc9aa13db2549f58": "1729731080"
# }
# url = "https://e.gtfund.com/Etrade/Public/cochinBatch"
# data = {
#     "batch": [
#         {
#             "api": "info.fund.detail",
#             "params": {
#                 "fundCode": "511010"
#             }
#         },
#         {
#             "api": "info.fund.growth_plot",
#             "params": {
#                 "start": "2023-10-22T16:00:00.000Z",
#                 "end": "2024-10-22T16:00:00.000Z",
#                 "fundCode": "511010",
#                 "order": "asc"
#             }
#         }
#     ]
# }
# data = json.dumps(data, separators=(',', ':'))
# response = requests.post(url, headers=headers, cookies=cookies, data=data)
# print(response.text)
# print(response)


import requests


headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Origin": "https://www.efunds.com.cn",
    "Referer": "https://www.efunds.com.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
url = "https://api.efunds.com.cn/xcowch/front/etffund/stocklist"
params = {
    "fundCode": "159150",
    "tDate": "2024-10-24"
}
response = requests.get(url, headers=headers, params=params)

print(response.text)
print(response)