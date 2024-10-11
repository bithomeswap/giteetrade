import time
import os
import math
import requests
filename=r"C:\Users\13480\gitee\trade\高考志愿填报系统\软件强制更新\version.txt"
with open(filename,'r',encoding='utf-8') as file:
    up=True
    for line in file:
        print("本地版本",line,type(line))
        district=requests.request('GET',f"https://gitee.com/bithomeAI/exe/raw/master/version.txt").json()#验证本地版本号和在线版本号
        print("district",district,type(district))
        # if str(line)==str(district):#跟github页面对比
        if str(line)==str(district)+"1":#跟github页面对比【测试使得故意不相等】
            print("版本正确")
            up=False
        else:
            print("版本错误")

if up==True:#执行更新程序【下载最新版本、更新版本文件、删除当前程序】
    #【弹窗提示版本更新】
    import tkinter.messagebox as msgbox
    msgbox.showwarning(title="警告", message="请更新软件版本，享受最新功能")
    msgbox.showinfo(title="最新版软件下载地址（软件下载完成之前请勿关闭此按钮）", message="https://gitee.com/bithomeAI/exe")

    # from PIL import Image, ImageTk
    # import tkinter as tk
    # root = tk.Tk()# 创建主窗口
    # # root.withdraw()# 隐藏主窗口【隐藏就看不到了】

    # #【超链接】
    # root.title("软件更新")
    # root.geometry("90x60")
    # link_label = tk.Label(root, text="软件更新", fg="blue", underline=True)
    # link_label.pack(pady=20)
    # from webbrowser import open as webopen
    # link_label.bind("<Button-1>", lambda event: webopen('https://gitee.com/bithomeAI/exe'))

    # #【二维码】
    # a=tk.Frame(root)
    # a.pack()
    # image_path = r'C:\Users\13480\gitee\trade\高考志愿填报系统\软件强制更新\xq.png'  # 替换为你的图片路径
    # b=Image.open(image_path)
    # # print("b",b,b.size,type(b.size))
    # weight=float(b.size[0])
    # height=float(b.size[1])
    # # print(b.size[0],b.size[1])
    # # 获取屏幕的宽度和高度
    # screen_width = float(root.winfo_screenwidth())
    # screen_height = float(root.winfo_screenheight())
    # little=2#设置宽或者高占屏幕宽或者高的最大比例
    # rate=min(screen_width/weight/little,screen_height/height/little)#屏幕是图片的倍数再除以一堆的倍数
    # b=b.resize(size=(math.floor(weight*rate),math.floor(height*rate)))#设置图片大小
    # b=ImageTk.PhotoImage(b)
    # link=tk.Label(a,image=b).pack()

    # #【保持主窗口】
    # root.attributes('-topmost', True)# 使窗口保持在最前方
    # root.overrideredirect(True)# 禁用窗口的关闭按钮
    # root.mainloop()# 保持窗口打开，直到用户关闭【需要保持打开】

    #直接下载最新版本【实际不是这个地址】
    from webbrowser import open as webopen
    webopen("https://gitee.com/bithomeAI/exe/releases/download/2025/gaokao.exe", new=0, autoraise=True)

    #重写本地的版本文件
    with open(filename,'w',encoding='utf-8') as file:
        file.write(str(district))

    # # 更新版本之后删除原来的文件
    # # Python可以删除自身文件，但打包成.exe文件之后exe本身在执行时文件是被占用的状态无法删除自身，因而需要额外的bat文件参与
    # import sys
    # import subprocess 
    # def WriteRestartCmd():
    #     b=open("upgrade.bat",'w')
    #     TempList="@echo off\n";# 关闭bat脚本的输出
    #     TempList+="ping -n 5 127.0.0.1>nul \n"# 有的电脑没有sleep命令，因而使用ping替代，ping一次默认一秒左右
    #     TempList+="del "+os.path.realpath(sys.argv[0])+"\n"# 删除当前文件【sys.argv[0]获取文件路径，在exe文件当中更加准确】
    #     TempList+="ping -n 10 127.0.0.1>nul \n"# 有的电脑没有sleep命令，因而使用ping替代，ping一次默认一秒左右
    #     b.write(TempList)
    #     b.close()
    #     subprocess.Popen("upgrade.bat")# 执行版本升级命令
    #     sys.exit()# 退出此程序
    # # 新程序启动时，删除旧程序制造的脚本
    # if os.path.isfile("upgrade.bat"):
    #     os.remove("upgrade.bat")
    # WriteRestartCmd()#删除当前运行的文件
else:
    # pip install pyside6
    # pyside6-designer#CMD命令行启动pyside6
    # 使用pyqt执行志愿填报任务
    pass