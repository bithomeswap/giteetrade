# pip install PyX matplotlib scapy#总共安装了3个包
# pip install scapy#简易版
# pip install --pre scapy basic#基础版
# pip install --pre scapy complete#完全体



# IP地址可以确定唯一的一台主机，端口可以确定一个进程，所以一个ip地址+一个端口就可以唯一确定是哪一台主机上的哪个进程在发送信息
from scapy.all import *
# print(conf)#查看配置
# lsc()#查看命令



#[使用本机IP进行发包测试]
# target = '172.22.0.1'#使用本机IP进行测试
# # 这里我们使用sr()函数对192.168.2.11(即S1)做端口22，80，123的TCP SYN扫描（注意flags = "S"）, timeout设为5秒。
# ans,unans = sr(IP(dst = target) / TCP(sport = RandShort(), dport = [22, 80, 123], flags = "S"), timeout = 5)
# # sr()函数返回的是一个元组，该元组下面有两个元素，一个是Results，一个是Unanswered，
# print(ans,unans)# 我们用ans来表示Results，也就是被响应的包，用unans来表示Unanswered，表示没有被响应的包。
# # ans和unans各自又含两个包，一个是发出去的包，一个是接收到的包，
# # 以ans[0][0]和ans[0][1]为例，
# # 第一个[0]表示抓到的第一个包，
# # 第二个[0]和[1]分别表示第一个包里发出的包和接收到的包。
# for sent, received in ans:
#     # 举例如下：
#     # >>> ans[0][0] （第一个包里发出的包）
#     # <IP frag=0 proto=tcp dst=192.168.2.11 |<TCP dport=sunrpc flags=A |>>
#     # >>> ans[0][1] （第一个包里接收到的包）
#     # <IP version=4 ihl=5 tos=0x0 len=40 id=10338 flags= frag=0 ttl=255 proto=tcp chksum=0xe11 src=192.168.2.11 dst=192.168.2.1 options=[] |<TCP sport=sunrpc dport=ftp_data seq=0 ack=0 dataofs=5 reserved=0 flags=R window=0 chksum=0x2a01 urgptr=0 |<Padding load='\x00\x00\x00\x00\x00\x00' |>>>
#     # 正因如此，所以下面for loop里的sent, received分别代表的是
#     # ans[0][0]、ans[0][1](抓到的第一个端口为22的包)，
#     # ans[1][0]、ans[1][1](抓到的第二个端口为80的包),
#     # ans[2][0]、ans[2][1](抓到的第三个端口为123的包)里的内容
#     # haslayer()函数返回的是布尔值，用来判断从接收端返回的包(received)里所含协议的类型，
#     if received.haslayer(TCP) and str(received[TCP].flags) == "SA":
#         # 判断该received包是否包含TCP协议，并且该包里TCP的flag位是否为SA(, )SA代表SYN/ACK)则说明该端口在接收端是打开的(Open)
#         print("Port " + str(sent[TCP].dport) + " of " + target + " is OPEN!")
#     elif received.haslayer(TCP) and str(received[TCP].flags) == "RA":
#         # 如果返回的包是TCP包，并且该TCP包的flag位为RA（RA表示Reset+），则说明该端口在接收端已经被关闭(closed)
#         print("Port " + str(sent[TCP].dport) + " of " + target + " is closed!")
#     elif received.haslayer(ICMP) and str(received[ICMP].type) == "3":
#         # 如果返回的包是ICMP包，并且该ICMP包的类型为3，则说明该端口被路由器或者防火墙过滤了(filtered)
#         print("Port " + str(sent[TCP].dport) + " of " + target + " is filtered!")
# for sent in unans:#如果发送端没有收到任何回复(no response)，我们同样可以判断该端口被路由器或者防火墙过滤了(filtered)，将该信息打印出来。
#     print(str(sent[TCP].dport) + " is filtered!")



# # [端口扫描]执行代码时需要在后缀上加port
# # python 【应用】\监听WIFI\监听.py 192.168.1.1
# import socket
# import argparse
# import sys
# import time
# parser = argparse.ArgumentParser()
# parser.add_argument('host')
# args = parser.parse_args()
# start = time.time()
# try:
#     for port in range(1, 65536):
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.settimeout(1)
#         result = sock.connect_ex((args.host, port))
#         print("Port:",port,result)
#         if result == 0:
#             print("Port: {} Open".format(port))
#         sock.close()
# except KeyboardInterrupt:
#     sys.exit()
# end = time.time()
# print(f"Scanning completed in: {end-start:.3f}s")




# # 读取Pcap文件【读包】
# # Pcap是一些工具如Wireshark，Aircrack-ng抓到的数据包
# a = rdpcap("test.cap")
# print(a)
# #<test.cap: UDP:518 TCP:231 ICMP:0 Other:0>