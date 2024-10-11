key="00d24d9fb9c2d1319b62b4e0228c8893"
import requests
import pandas as pd
#行政区划查询
district=requests.request('GET',f"https://restapi.amap.com/v3/config/district?keywords=北京&subdistrict=2&key={key}").json()
print(district)