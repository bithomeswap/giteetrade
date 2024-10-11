
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
                # UID_4HGW0dvl7EA7zaZLYe8bjegTSZFS # 姨父畅海东UID
    # # 发送消息
    # # WxPusher.send_message('<content>',
    # #                       uids=['<uids>'],
    # #                       topic_ids=['<topic_ids>'],
    # #                       token='<appToken>')      
    message=WxPusher.send_message(
        "【用户注册】\n"+
        str(text),
        uids=["UID_qkmjMTBknX0I5ZZoVY3IBFv7WVV1"],#本人UID
        # uids=uidslist,
        topic_ids=["12417"],
        token="AT_tFRZgjToc6XnG5dzR2MGyv1DzECNYOIU",
    )
    messageId=message["data"][0]["messageId"]
    print(message,messageId)
    # # 查询消息是否发送成功【其实是发送错误】
    # query_message=WxPusher.query_message(f"{messageId}")
    # print(query_message)



# pip install wmi
import wmi
m_wmi = wmi.WMI()
print("m_wmi",m_wmi)


#【软件运行的时候提示用户将这个信息传给我以获取激活码实现完整功能】
#【加上试用超过一次强制用户升级的功能】
#【针对有实力的志愿填报机构也可以做定制化开发（如北清教育）】


# 获取 CPU 序列号
cpu_info = m_wmi.Win32_Processor()
if len(cpu_info) > 0:
    cpu_number = cpu_info[0].ProcessorId
    print("cpu_number",cpu_number)
# 获取 MAC 地址
mac_address=""
for network in m_wmi.Win32_NetworkAdapterConfiguration():
    this_mac_address = network.MacAddress
    if this_mac_address != None:
        mac_address+=this_mac_address
        print("this_mac_address",this_mac_address)
print("mac_address",mac_address)
# 获取硬盘序列号
disk_info = m_wmi.Win32_PhysicalMedia()
if len(disk_info) > 0:
    disk_serial = disk_info[0].SerialNumber.strip()
    print("disk_serial",disk_serial)
# 获取主板序列号
board_info = m_wmi.Win32_BaseBoard()
if len(board_info) > 0:
    board_id = board_info[0].SerialNumber.strip().strip('.')
    print("board_id",disk_serial)
# 将获取到的机器的 CPU序列号、Mac地址、硬盘序列号、主板序列号的硬件数据字符串拼接【在基础数据之上+195增加破解难度】
combine_str = cpu_number + mac_address + disk_serial + board_id + "195"#这个195是单独加上的
combine_byte = combine_str.encode("utf-8")
# 进行 MD5 编码【加密】
import hashlib
machine_code = hashlib.md5(combine_byte).hexdigest().upper()#生成激活码
print(machine_code)
#激活码详情推送到微信
postmessage(f"cpu_number:{cpu_number},mac_address:{mac_address},disk_serial:{disk_serial},board_id:{board_id}"+
            f"设备激活码:{machine_code}"
            )
#需要验证输入的激活码和推送的激活码是否一致






# # # 【】【测试】【】# # # 
    # #【计算设备激活码】（除非版本升级需要将全部会员作废否则激活码的计算方式不能轻易改变）
    # m_wmi = wmi.WMI()
    # print("m_wmi",m_wmi)
    # #【软件运行的时候提示用户将这个信息传给我以获取激活码实现完整功能】
    # #【加上试用超过一次强制用户升级的功能】
    # #【针对有实力的志愿填报机构也可以做定制化开发（如北清教育）】
    # # 获取 CPU 序列号
    # # cpu_info = m_wmi.Win32_Processor()
    # # if len(cpu_info) > 0:
    # #     self.cpu_number = cpu_info[0].ProcessorId
    # #     print("cpu_number",self.cpu_number)
    # # # 获取 MAC 地址
    # # self.mac_address=""
    # # for network in m_wmi.Win32_NetworkAdapterConfiguration():
    # #     this_mac_address = network.MacAddress
    # #     if this_mac_address != None:
    # #         self.mac_address+=this_mac_address
    # #         print("this_mac_address",this_mac_address)
    # # print("mac_address",self.mac_address)
    # # 获取硬盘序列号
    # disk_info = m_wmi.Win32_PhysicalMedia()
    # if len(disk_info) > 0:
    #     self.disk_serial = disk_info[0].SerialNumber.strip()
    #     print("disk_serial",self.disk_serial)
    # # 获取主板序列号
    # board_info = m_wmi.Win32_BaseBoard()
    # if len(board_info) > 0:
    #     self.board_id = board_info[0].SerialNumber.strip().strip('.')
    #     print("board_id",self.board_id)
    # # 将获取到的机器的 CPU序列号、Mac地址、硬盘序列号、主板序列号的硬件数据字符串拼接【在基础数据之上+195增加破解难度】
    # # self.combine_str = self.cpu_number + self.mac_address + self.disk_serial + self.board_id + "195"#这个195是单独加上的
    # self.combine_str = self.disk_serial + self.board_id + "195"#这个195是单独加上的
    # self.combine_byte = self.combine_str.encode("utf-8")
    # # 进行 MD5 编码【加密】
    # self.machine_code = hashlib.md5(self.combine_byte).hexdigest().upper()#生成激活码
    # print(self.machine_code)

# def getkey(self):
#     has_this_machine_code=False
#     #环境配置里面需要找到这个key
#     try:
#         data=pd.read_json('./setting.json')
#         print(data)
#         # 我的电脑当中需要添加到json文件的内容是
#         # "machine_code":{"0":"83D679A6D4FDF6A664B5977A743C0537"},
#         if ("machine_code" in data.columns):
#             print(data["machine_code"].values[0],"+",str(self.machine_code))
#             if (data["machine_code"].values[0]==str(self.machine_code)):
#                 has_this_machine_code=True
#             else:
#                 print("setting.json文件错误，请联系管理员获取")
#         else:
#             print("setting.json文件错误，请联系管理员获取")
#     except Exception as e:
#         print("本地没有setting.json，请联系管理员获取",e)
#     if has_this_machine_code==False:
#         #激活码详情推送到微信
#         postmessage(
#             # cpu_number:{self.cpu_number},\n
#             # mac_address:{self.mac_address},\n
#             f"""
#             disk_serial:{self.disk_serial},\n
#             board_id:{self.board_id},\n
#             machine_code[设备激活码]:{self.machine_code},\n
#             """)
#         jsondf=pd.DataFrame({
#             # "cpu_number":[self.cpu_number],
#             # "mac_address":[self.mac_address],
#             "disk_serial":[self.disk_serial],
#             "board_id":[self.board_id]})
#         thisjson=jsondf.to_json()
#         with open('./setting.json','w') as json_file:
#             json_file.write(thisjson)

#         str_update = f"""
#                     您是新设备\n
#                     请联系管理员获取设备激活码\n
#                     【微信号】：bithomeAI
#                     """
#         message = QMessageBox.question(
#             self, "检查更新", str_update,
#             QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

#     return has_this_machine_code
