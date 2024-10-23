# pip install wxauto#安装
# pip install --upgrade wxauto#更新
# pip install -r requirements.txt#环境配置

# #需要登陆微信后才能使用
# from wxauto import FixVersionError
# FixVersionError()#如果提示微信版本低无法登录，使用这段代码可以跳过更新

#打开微信主页
from wxauto import WeChat
wx = WeChat()#WeChat().nickname属性能够读取当前对话框当中，自己的微信用户名，但是在多开情况下，如何使不同线程匹配不同的用户名是个问题

import math

###【风控识别】###
# 1.机器人回复消息需要增加500-3000ms的随机数延时，不然容易被风控，因为真人操作的过程不可能每两条消息的间隔都刚好一样的时间。
# 第一条间隔可能1100MS，第二条可能1500MS。毫秒级别人基本感觉不对，但是人家服务器能知道你每次间隔的时间都一样就会触发风控。
# 2.个人微信好友上限是5000人，企业微信免费好友2000人（政府、学校、医院、非盈利组织免费好友50000人）。
# 腾讯客服表示，微信好友数量上限约 1 万个，每日添加好友和被添加没有次数限制，但短时间内频繁添加好友，可能会出现异常提示。


# GetSessionAmont#获取聊天对象名和新消息条数
# GetSessionList#获取当前聊天列表中的所有聊天对象的名字
# CurrentChat#获取当前聊天对象名
# GetFriendDetails#获取所有好友详情信息
# GetListenMessage#获取监听对象的新消息
# SwitchToContact#切换到通讯录页面
# SwitchToChat#切换到聊天页面





#需要先打开群，才能进行好友添加
# who="文件传输助手"
# who="量化策略交流学习"#已经加完好友
# who="QMT交易实战33群"#跑到第280个群友了
who="聚宽策略PTrade实盘"
# who="国金吃肉聊天交流群"
# who="wxauto三群"
wx.ChatWith(who)#【默认点击左键{左键右键功能置换时使用下方代码}】打开群指定的聊天窗口{返回值为字符串}

# 判断对话框是否是群聊{也可以使用获取群成员昵称的函数来判断【如果报错说明不是群聊】}
from wxauto.uiautomation import PaneControl
def IsGroup(chatBox:PaneControl):
    groupName = chatBox.TextControl()
    return True if groupName.GetSiblingControl(lambda x:x.Name in groupName.Name) else False
is_group = IsGroup(wx.ChatBox)
print("是否是群聊",is_group)

import akshare
akshare.bond_cb_index_jsl
#自动化加好友【这个是添加群好友不是根据联系方式自动加好友】
import random#添加随机数
import time
# pip install uiautomation
import uiautomation as auto
wechatWindow = auto.WindowControl(searchDepth=1, Name="微信", ClassName='WeChatMainWndForPC')
num=0
while True:
    num+=1
    if num>=62:#这里尽量把前二十人跳过去【另外还有一个索引越界{UI当中无法展示该名片}的问题】
        button = wechatWindow.ButtonControl(Name='收起')
        if button.Exists():
            print("有收起按钮无需重新打开")
            pass
        else:
            button = wechatWindow.ButtonControl(Name='聊天信息')
            button.Click()#默认左键
            time.sleep(0.5+random.random())
            button = wechatWindow.ButtonControl(Name='查看更多')
            button.Click()#默认左键
            time.sleep(0.5+random.random())
            buttonlist = wechatWindow.ListControl(Name='聊天成员')
            childrenlist=buttonlist.GetChildren()#默认左键
            time.sleep(0.5+random.random())
        # print(childrenlist)
        children=childrenlist[num]
        print(children)#Rect的最后一个是高度9384-9298=86[60x86]一行的高度是86，4行是344
        print("元素的位置信息",children.BoundingRectangle)#元素的位置信息Rect信息
        print("元素的位置信息",
              children.BoundingRectangle.left,
              children.BoundingRectangle.top,
              children.BoundingRectangle.right,
              children.BoundingRectangle.bottom,
              )#元素的位置信息
        # #【一行四个人】
        # ControlType: ListItemControl    ClassName:     AutomationId:     Rect: (1192,9212,1252,9298)[60x86]    Name: '陌年微凉'    Handle: 0x0(0)ControlType: ListItemControl    ClassName:     AutomationId:     Rect: (988,9298,1048,9384)[60x86]    Name: '棉花糖🤗'    Handle: 0x0(0)
        # ControlType: ListItemControl    ClassName:     AutomationId:     Rect: (1056,9298,1116,9384)[60x86]    Name: 'GreenSun'    Handle: 0x0(0)ControlType: ListItemControl    ClassName:     AutomationId:     Rect: (1124,9298,1184,9384)[60x86]    Name: 'LYON.'    Handle: 0x0(0)   
        # ControlType: ListItemControl    ClassName:     AutomationId:     Rect: (1192,9298,1252,9384)[60x86]    Name: '星河'    Handle: 0x0(0)    
        
        #将窗口滚动到目标位置
        m=num%4#列数
        n=(num-m)/4#行数
        print(f"目前为为第{n}行{m}列")#每行四个用户，需要计算向下滚动的距离
        if num<200:
            button.WheelDown(wheelTimes=int(math.floor(n*6/13)),#7次13行多一点，6次13行少一点
                                    interval=0.1,#滚动间隔
                                    waitTime=0.1,#等待时间【任务完成后的等待时间】
                                    )#模拟鼠标向下滚动
        else:
            button.WheelDown(wheelTimes=int(math.floor(n*7/13)),#7次13行多一点，6次13行少一点
                                    interval=0.1,#滚动间隔
                                    waitTime=0.2,#等待时间【任务完成后的等待时间】
                                    )#模拟鼠标向下滚动
        #执行加好友操作
        children.Click()#点开具体某个群成员的信息对话框
        button = wechatWindow.ButtonControl(Name='添加到通讯录')
        if button.Exists():
            button.Click()#默认点击左键
            time.sleep(0.5+random.random())
            #针对隐私设置用户进行处理
            warn = wechatWindow.ButtonControl(Name='取消')
            if not warn.Exists():
                #验证是否能够直接添加
                friendcard = wechatWindow.ButtonControl(Name='更多')
                time.sleep(1)
                if friendcard.Exists():
                    print("对方直接通过好友验证无需确认")#需要取消窗口
                    #点开具体某个群成员的信息对话框释放对话框
                    button = wechatWindow.ButtonControl(Name='聊天信息')
                    button.RightClick()
                else:
                    print("有隐私设置无法添加好友确认已进行下一步")
                    wechatWindow.ButtonControl(Name='确定').Click(simulateMove=False)
            else:#只申请非隐私设置的用户
                addmsg=who#群聊名称（申请信息）
                remark=f"{who}{children.Name}"#备注名
                tags=[f"{who}标签"]# 标签名列表
                #修改好友申请信息
                NewFriendsWnd=wechatWindow.WindowControl(ClassName='WeUIDialog')
                #【设置好友申请信息】
                # if addmsg:
                #     msgedit = NewFriendsWnd.TextControl(Name="发送添加朋友申请").GetParentControl().EditControl()
                #     msgedit.Click(simulateMove=False)
                #     msgedit.SendKeys('{Ctrl}a', waitTime=0)
                #     msgedit.SendKeys(addmsg)
                #【设置备注名】
                if remark:
                    remarkedit = NewFriendsWnd.TextControl(Name='备注名').GetParentControl().EditControl()
                    remarkedit.Click(simulateMove=False)
                    remarkedit.SendKeys('{Ctrl}a', waitTime=0)
                    remarkedit.SendKeys(remark)
                #【设置标签名】
                # if tags:#标签这不太对
                #     tagedit = NewFriendsWnd.TextControl(Name='标签').GetParentControl().EditControl()
                #     for tag in tags:
                #         tagedit.Click(simulateMove=False)
                #         tagedit.SendKeys(tag)
                #         NewFriendsWnd.PaneControl(ClassName='DropdownWindow').TextControl().Click(simulateMove=False)
                NewFriendsWnd.ButtonControl(Name='确定').Click(simulateMove=False)#确认添加好友
                #跳过无法添加好友情况的
                time.sleep(1)
                text = wechatWindow.TextControl(Name='对方账号违反了《微信个人账号使用规范》，无法添加朋友，可引导对方查看微信团队消息了解详情。')#TextControl
                if text.Exists():
                    print("对方违规无法添加好友点击确定跳过")
                    wechatWindow.ButtonControl(Name='确定').Click(simulateMove=False)
        else:
            print("不存在该按钮")
            # children.MiddleClick()#点击鼠标中键
            # children.MiddlePressMouse()#按下鼠标中键
            # children.MiddleReleaseMouse()#松开鼠标中键
            children.RightClick()#默认点击右键
            # children.Click()#默认点击左键
            time.sleep(0.5+random.random())


# #获取当前对话窗口的聊天记录【可以执行】
# messages = wechatWindow.ListControl(Name='消息')
# for message in messages.GetChildren():
#     content = message.Name
#     print(content)


# timeout=5#五秒钟超时
# wx.UiaAPI.SendKeys('{Ctrl}f', waitTime=1)
# wx.B_Search.SendKeys(who, waitTime=1.5)
# target_control = wx.SessionBox.TextControl(Name=f"<em>{who}</em>")
# if target_control.Exists(timeout):
#     print('选择完全匹配项')
#     target_control.Click(simulateMove=False)
# else:
#     search_result_control = wx.SessionBox.GetChildren()[1].GetChildren()[1].GetFirstChildControl()
#     if not search_result_control.PaneControl(searchDepth=1).TextControl(RegexName='联系人|群聊').Exists(0.1):
#         print(f'未找到搜索结果: {who}')
#         wx._refresh()
#     print('选择搜索结果第一个')
#     target_control = search_result_control.Control(RegexName=f'.*{who}.*')
#     chatname = target_control.Name
#     target_control.Click(simulateMove=False)


# #获取所有好友列表【拿不到微信号，还是要用AutoHotkey热键精灵】
# AllFriends=wx.GetAllFriends()#该方法运行时间取决于好友数量，约每秒6~8个好友的速度，该方法未经过大量测试，可能存在未知问题，如有问题请微信群内反馈
# # 可选参数Args:
# #     keywords (str, optional): 搜索关键词，只返回包含关键词的好友列表
# print(AllFriends,len(AllFriends))


# #获取当前群的所有成员的昵称
# GroupMembers=wx.GetGroupMembers()
# print(GroupMembers)


# # @所有人
# who = '自动化测试'#群名称
# msg = '测试着玩（请忽略）'
# wx.AtAll(msg=msg,who=who)


# # #设置消息发送对象
# # who = '文件传输助手'#好友名称
# who = '王腾鹤'#好友名称
# # who = '🧊烫手'#好友名称【注意是微信名，而不是微信号】
# print(wx,wx.nickname)
# # 现在用的是消息队列式需要在线程内通过WeChat().nickname取用户，后面前后台设计模式的话就不用区分用户了，把消息取出来在后台做对话处理即可，对话存放数据格式难住了
# #微信消息发送
# wx.SendMsg(f'wxauto测试',who)
# # #SendMsg函数后面加上这句话能够，实现语音聊天功能（执行的时候不能乱动鼠标不然容易点错）
# # editbox.SendKeys('{Enter}')#editbox只包括聊天框，不包含上方的按钮部分
# # self.ChatBox.ButtonControl(Name='语音聊天').Click(simulateMove=True)#self.ChatBox包含整个聊天界面
# # # 微信发送文件
# # files = [
# #     r'C:\Users\Admin\Desktop\wxauto-WeChat3.9.8\wxauto-WeChat3.9.8\doc.md',
# #     r'C:\Users\Admin\Desktop\wxauto-WeChat3.9.8\wxauto-WeChat3.9.8\LICENSE',
# #     r'C:\Users\Admin\Desktop\wxauto-WeChat3.9.8\wxauto-WeChat3.9.8\demo\README.md'
# # ]
# # wx.SendFiles(filepath=files, who=who)


# # 获取当前聊天页面（文件传输助手）消息，并自动保存聊天图片
# msgs = wx.GetAllMessage(savepic=True)
# print(msgs)
# for msg in msgs:
#     print(f"{msg[0]}: {msg[1]}")
# print('wxauto测试完成')


# #自动接受好友申请
# new = wx.GetNewFriends()#获取新的好友申请对象列表
# print(new)
# for thisnew in new:
#     print(thisnew)# 获取可接受的新好友对象
#     print(thisnew.name)# 获取好友申请昵称
#     print(thisnew.msg)# 获取好友申请信息
#     # 接受好友请求，并且添加备注“备注张三”、添加标签wxauto
#     thisnew.Accept(remark=thisnew.msg,#备注
#                    tags=['wxauto'],#分组
#                    )
# # 切换回聊天页面
# wx.SwitchToChat()


# #自动化加好友【这个是根据联系方式添加新的好友不是群好友】
# # AddNewFriend(self, keywords, addmsg=None, remark=None, tags=None):#自动添加好友的函数
# """添加新的好友
# Args:
#     keywords (str): 搜索关键词，微信号、手机号、QQ号
#     addmsg (str, optional): 添加好友的消息
#     remark (str, optional): 备注名
#     tags (list, optional): 标签列表
# Example:
#     >>> wx = WeChat()
#     >>> keywords = '13800000000'      # 微信号、手机号、QQ号
#     >>> addmsg = '你好，我是xxxx'      # 添加好友的消息
#     >>> remark = '备注名字'            # 备注名
#     >>> tags = ['朋友', '同事']        # 标签列表
#     >>> wx.AddNewFriend(keywords, addmsg=addmsg, remark=remark, tags=tags)
# """
# #使用gbk方式打开文件并自动化加好友
# import pandas as pd
# df=pd.read_csv(r"C:\Users\13480\gitee\trade\【应用】\【自动化windows】AutoHotkey微信好友导出\微信好友记录\20240808105501.csv",encoding="GBK",encoding_errors='ignore')
# print(df,df["微信号"].tolist())
# for index,thisdf in df.iterrows():
#     print(thisdf)
#     # 备注,昵称,微信号,地区,标签,个性签名,元数据
#     account=thisdf["微信号"]
#     remarkname=thisdf["备注"]
#     try:
#         wx.AddNewFriend(keywords=account,#对方微信号、手机号、QQ号等
#                         addmsg="",#添加好友申请信息
#                         remark=remarkname,#备注
#                         tags=["客户"],#标签列表
#                         )
#     except Exception as e:
#         print(e,"添加失败",account,remarkname,"可能是已经有好友了")


# # #打开朋友圈【尚未完善】
# button = wechatWindow.ButtonControl(Name='朋友圈')
# button.Click()
# friendWindow = auto.WindowControl(
#     searchDepth=1, Name="朋友圈", ClassName='SnsWnd')
# friendWindow.SetFocus()
# listControls = friendWindow.ListControl(Name='朋友圈')
# for item in listControls.GetChildren():
#     if item.ControlTypeName != "ListItemControl":
#         continue
#     print(item.Name)
#     panes = item.GetChildren()[0].GetChildren()[
#         0].GetChildren()[1].GetChildren()
#     if len(panes) >= 5:
#         print("评论：")
#         comments = panes[4].ListControl(Name='评论')
#         for comment in comments.GetChildren():
#             print(comment.Name)
#     print("------------------")


# #输入文字【好像不能执行】
# edit = wechatWindow.EditControl(Name='输入')
# edit.SendKeys('你好')
# sendButton = wechatWindow.ButtonControl(Name='发送(S)')
# sendButton.Click()


# #【消息监控】
# import time
# import uiautomation as auto
# import re
# from plyer import notification#pip install plyer
# notification_history = {}  # 历史消息
# def check_wechat_messages():
#     # 获取微信窗口
#     wechat_win = auto.WindowControl(Name="微信", ClassName="WeChatMainWndForPC")
#     shoukuanWin = wechat_win.ListControl(Name="会话")
#     bbb = shoukuanWin.GetChildren()
#     for chatMsg in bbb:
#         if "条新消息" in chatMsg.Name:
#             # 计算消息条数
#             match = re.match(r'([a-zA-Z0-9]+)(\d+)条新消息', chatMsg.Name)
#             if match:
#                 nickname = match.group(1)
#                 message_count = int(match.group(2))
#                 printInfo = f"{nickname} 给你发送了 {message_count} 条消息"
#                 print(printInfo)
#                 print("------------")
#                 # 获取消息列表控件
#                 xiaoxis = wechat_win.ListControl(Name="消息")
#                 # 获取消息列表控件的子控件
#                 xiaoxi_children = xiaoxis.GetChildren()
#                 # 获取最后一个子控件
#                 last_xiaoxi = xiaoxi_children[-1]
#                 # 打印最后一条消息的内容
#                 print(last_xiaoxi.Name)
#                 # 在指定时间内不重发
#                 last_notification_time = notification_history.get((nickname, message_count), 0)
#                 current_time = time.time()
#                 if current_time - last_notification_time > 15:
#                     # 依次发送
#                     notification_title = f"来自 {nickname} 的 {message_count} 条消息"
#                     notification_message = f"{last_xiaoxi.Name}"
#                     notification.notify(
#                         title=notification_title,
#                         message=notification_message,
#                         app_name="WeChat"
#                     )
#                     # 更新日志
#                     notification_history[(nickname, message_count)] = current_time
# if __name__ == "__main__":
#     try:
#         while True:
#             check_wechat_messages()
#             time.sleep(2)  #2秒检测一次UI组件
#     except KeyboardInterrupt:
#         print("程序退出~")
#     except Exception as e:
#         print(f"程序执行出现了问题: {str(e)}")



# #【收款助手】未完成
# import uiautomation as auto
# import re
# import time
# def get_children_at_depth(control, target_depth, current_depth=0):
#     children = control.GetChildren()
#     result = []
#     for child in children:
#         if current_depth == target_depth:
#             result.append(child)
#         else:
#             result.extend(get_children_at_depth(child, target_depth, current_depth + 1))
#     return result
# def process_last_child_information(previous_info):
#     weixin = auto.WindowControl(Name="微信收款助手", ClassName="ChatWnd")
#     xiaoxi = weixin.ListControl(Name="消息")
#     target_depth = 5
#     depth_5_children = get_children_at_depth(xiaoxi, target_depth)
#     # 正则表达式模式
#     pattern = r'收款到账通知(\d+月\d+日 \d+:\d+)收款金额￥([0-9.]+)汇总'
#     last_child = None
#     for child in depth_5_children:
#         match = re.search(pattern, child.Name)
#         if match:
#             last_child = child  # 保存最后一条子控件的引用
#     # 在循环结束后，提取最后一条子控件的信息
#     if last_child:
#         match = re.search(pattern, last_child.Name)
#         if match:
#             date_time = match.group(1)
#             amount = match.group(2)
#             # 监听下一笔
#             if (date_time, amount) != previous_info:
#                 print("收款回调：")
#                 print(date_time)
#                 print("金额:", amount)
#                 print("正在等待下一笔...")
#                 print("----------")
#                 previous_info = (date_time, amount)
#     return previous_info
# # 循环
# previous_info = None
# while True:
#     previous_info = process_last_child_information(previous_info)
#     # 每2秒执行一次循环
#     time.sleep(2)



#【案例：使用微信自动化复制粘贴】
# # 打开微信窗口
# pyautogui.hotkey('ctrl', 'alt', 'w')
# time.sleep(2)
# # 清空剪切板并将目标写入到剪切板
# pyperclip.copy("")
# pyperclip.copy('#发送对象')
# # 使用快捷键 ctrl+f 定位到微信搜索栏
# pyautogui.hotkey('ctrl', 'f')
# time.sleep(1)
# # 使用快捷键 ctrl+v 将目标粘贴到微信搜索栏，微信将自动搜索
# pyautogui.hotkey('ctrl', 'v')
# time.sleep(1)
# # 按回车键打开搜索出的目标
# pyautogui.press('enter')
# time.sleep(2)



# #通讯录里面拉群聊
# def quote(self, msg):
#     """引用该消息
#     Args:
#         msg (str): 引用的消息内容
#     Returns:
#         bool: 是否成功引用
#     """
#     wxlog.debug(f'发送引用消息：{msg}  --> {self.sender} | {self.content}')
#     self._winobj._show()
#     headcontrol = [i for i in self.control.GetFirstChildControl().GetChildren() if i.ControlTypeName == 'ButtonControl'][0]
#     RollIntoView(self.chatbox.ListControl(), headcontrol, equal=True)
#     xbias = int(headcontrol.BoundingRectangle.width() * 2)
#     ybias = int(headcontrol.BoundingRectangle.height() * 0.12)  # 添加 ybias 计算
#     headcontrol.RightClick(x=xbias, y=-ybias, simulateMove=False)  # 传入 y 参数
#     menu = self._winobj.UiaAPI.MenuControl(ClassName='CMenuWnd')
#     quote_option = menu.MenuItemControl(Name="引用")
#     if not quote_option.Exists(maxSearchSeconds=0.1):
#         wxlog.debug('该消息当前状态无法引用')
#         return False
#     quote_option.Click(simulateMove=False)
#     editbox = self.chatbox.EditControl(searchDepth=15)
#     t0 = time.time()
#     while True:
#         if time.time() - t0 > 10:
#             raise TimeoutError(f'发送消息超时 --> {msg}')
#         SetClipboardText(msg)
#         editbox.SendKeys('{Ctrl}v')
#         if editbox.GetValuePattern().Value.replace('\r ', ''):
#             break
#     editbox.SendKeys('{Enter}')
#     return True