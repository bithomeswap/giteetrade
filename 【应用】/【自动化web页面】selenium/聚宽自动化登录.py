import time
from datetime import datetime, timedelta
import pandas as pd
import json
import os
import cv2#pip install opencv-python
import time
import random
import requests
import numpy as np
from PIL import Image#pip install pillow
from io import BytesIO
# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver import EdgeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#pip install pyautogui
# import pyautogui
import ddddocr#pip install ddddocr

###【风控识别】###
#1.执行滑块验证码拖动滑块的时候，有些平台会验证拖动轨迹，需要拿随机数停滞距离合成拖动轨迹而不是之间拖动（拖动过程中鼠标仍然需要悬停在滑块上）

alloptions = EdgeOptions()
# alloptions.add_experimental_option("detach", True)        # 引入不关闭浏览器的相关配置项
# alloptions.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])  # 避免终端下执行代码报警告
# alloptions.add_experimental_option("detach", True)        # 不关闭网页
# alloptions.add_extension('插件')                           # 加载拓展插件
# alloptions.add_argument('--headless')                     # 开启无界面模式,如果涉及到与网页的交互（输入内容，点击按钮）那么有些网站就不能使用无头浏览器
# alloptions.add_argument("--disable-gpu")                  # 禁用gpu
# alloptions.add_argument('--user-agent=Mozilla/5.0 HAHA')  # 配置对象添加替换User-Agent的命令
# alloptions.add_argument('--window-size=1366,768')         # 设置浏览器分辨率（窗口大小）
# alloptions.add_argument('--start-maximized')              # 最大化运行（全屏窗口）,不设置，取元素会报错
# alloptions.add_argument('--disable-infobars')             # 禁用浏览器正在被自动化程序控制的提示
# alloptions.add_argument('--incognito')                    # 隐身模式（无痕模式）
# alloptions.add_argument('--disable-javascript')           # 禁用javascript
# alloptions.add_argument(f"--proxy-server=http://115.239.102.149:4214")  # 使用代理
# alloptions.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
# # 加载用户缓存，可以记录使用记录和cookie，如果不指定缓存路径，会自动创建临时文件夹。
# user_dir = r'./browser_cache'
# alloptions.add_argument(f"--user-data-dir={user_dir}")

# 定位元素慢慢来，找不到也不奇怪。iframe和弹窗，定位之前先跳转。
# 动态元素用id/class，不变元素用Xpath。鼠标操作灵活用，实在找不到就用try。

def get_img(driver,targettype,path,classname,picname):
    # 获取浏览器缩放级别
    zoom_level = driver.execute_script("return window.devicePixelRatio;")
    print("浏览器缩放级别",zoom_level)

    if targettype=="path":
        img=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,path)))
    elif targettype=="classname":
        img=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,classname)))
    # print(img)
    time.sleep(1)

    location=img.location#这个location定位不对,rect更准确，location是四舍五入了，但是都不行
    size=img.size
    print(location,size)

    # 滚动到元素位置
    driver.execute_script("arguments[0].scrollIntoView();", img)
    time.sleep(1)
    # 考虑到页面可能存在滚动条，需要减去页面的滚动偏移量
    scroll_x = driver.execute_script("return window.pageXOffset;")
    scroll_y = driver.execute_script("return window.pageYOffset;")

    print("滚动条位置",scroll_x,scroll_y)
    #图片定位
    top=(location['y']-scroll_y)*zoom_level
    bottom=top+size['height']*zoom_level
    left=(location['x']-scroll_x)*zoom_level#这里加数之后会整体右移【也就是左侧的值大了】整体定位不对
    right=left+size['width']*zoom_level
    print('验证码位置',top,bottom,left,right)#截图位置有点偏
    #图片剪裁
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    captcha = screenshot.crop((left,top,right,bottom))#第三个元素是高度，现在改了会向上走
    captcha.save(picname)
    return top,bottom,left,right

# 打开参数【避免模拟的时候被平台识别为机器人】
alloptions.add_experimental_option('excludeSwitches', ['enable-automation']) # 避免终端下执行代码报警告
#账户密码登录推特【selenium模拟登陆过程，自动输入twitter账号和密码，并且获取cookies】
alllist=[
    # {"username":"19511189162","password":"wthWTH00"},
         {"username":"15803281949","password":"wthWTH00"}
         ]
for thislist in alllist:
    # try:
        username=thislist["username"]
        password=thislist["password"]
        print(username,password)
        # driver=webdriver.Edge()#window.navigator.webdriver的值为true
        driver=webdriver.Edge(options=alloptions)#window.navigator.webdriver的值为undefined【避免被平台识别为机器人】
        # 设置浏览器窗口大小（可选）
        driver.set_window_size(1024, 768)#调整窗口大小之后定位变了，但是还有偏离
        # 使用JavaScript执行缩放操作100%【无效操作】
        driver.execute_script("window.scrollTo(0, 0);")  # 滚动到页面顶部，确保元素坐标从顶部开始计算
        driver.execute_script("document.body.style.zoom = '100%';")

        waittime=0.5
        driver.get(r'https://www.joinquant.com/user/login/index?type=login')
        #这里睡几秒，等待页面加载。
        time.sleep(waittime)
        driver.find_element("xpath",r"/html/body/div[2]/div/div/ul[2]/li[1]/div[1]/form/input[1]").send_keys(username)
        time.sleep(waittime)
        driver.find_element("xpath",r"/html/body/div[2]/div/div/ul[2]/li[1]/div[1]/form/input[2]").send_keys(password)
        time.sleep(waittime)
        driver.find_element("xpath",r"/html/body/div[2]/div/div/div[2]/label/input").click()
        time.sleep(waittime)
        driver.find_element("xpath",r"/html/body/div[2]/div/div/ul[2]/li[1]/div[1]/form/button").click()#登录
        time.sleep(waittime)

        # # #鼠标悬停【暂时没有用处】
        # # menu=driver.find_element(By.CLASS_NAME,r"modal-content") # 定位鼠标要悬停的元素
        # # mouse=ActionChains(driver)
        # # mouse.move_to_element(menu).perform() # 鼠标悬停到定位元素上
        # time.sleep(2)#需要等几秒弹窗才能出来

        try:
            # 使用find_element_by_*方法查找元素，这里以find_element_by_id为例
            element = driver.find_element("xpath",r"/html/body/section/div/ul/li[1]/a")
            print("元素存在，无需滑块登录")
        except Exception as e:
            print("元素不存在，需要滑块登录")
            while True:#重复验证避免验证错
                try:
                    #浮动窗口提取元素
                    time.sleep(waittime)
                    # 获取浏览器缩放级别，其实是1.25倍，后面经常算着不对是因为用成了1.5倍去换算了，另外后面位移也可以换成多个随机数逐步移动，每次休息0.01-0.05秒（随机数）
                    zoom_level = driver.execute_script("return window.devicePixelRatio;")
                    print("浏览器缩放级别",zoom_level)

                    # path=r"/html/body/div[7]/div/div/div[2]/div/div/div/div/div[1]"#这个是登录时的路径，在签到时的路径如下r"/html/body/div[7]/div/div[2]/div/div[1]"
                    classname=r"valid-code__div"
                    picname="background.png"#背景图
                    top,bottom,left,right=get_img(driver=driver,
                                                targettype="classname",#参数为classname则根据classname确定元素，参数为path则根据path确定元素
                                                path=False,#根据路径确定位置，一般设置为False
                                                classname=classname,#根据类名确定位置
                                                picname=picname,#背景图路径和名称
                                                )
                    print(top,bottom,left,right)

                    # slidepath=r"/html/body/div[7]/div/div/div[2]/div/div/div/div/div[1]/div[67]"
                    slideclassname=r"valid-code__hq"
                    slidepicname="target.png"#滑块图
                    slidetop,slidebottom,slideleft,slideright=get_img(driver=driver,
                                                targettype="classname",#参数为classname则根据classname确定元素，参数为path则根据path确定元素
                                                path=False,#根据路径确定位置，一般设置为False
                                                classname=slideclassname,#根据类名确定位置
                                                picname=slidepicname,#背景图路径和名称
                                                )
                    print(slidetop,slidebottom,slideleft,slideright)
                    
                    # 裁剪背景图像，裁剪掉最左侧的drop长度
                    drop=(slideright-slideleft)#背景图裁剪长度（在最左侧裁剪掉一个滑块的距离，避免识别成滑块本身）
                    screenshot = Image.open('background.png')
                    print("screenshot",screenshot)
                    captcha = screenshot.crop((drop, 0, screenshot.width, screenshot.height))
                    captcha.save('background.png')

                    # 如果安装速度慢可以换成pip install ddddocr -i https://pypi.tuna.tsinghua.edu.cn/simple/
                    det = ddddocr.DdddOcr(
                        # beta=True,#切换为第二套ORC模型
                        det=False,#det=False 表示不使用图像检测功能，
                        ocr=False,#ocr=False 表示不使用文字识别功能，
                        show_ad=False,#show_ad=False 表示不显示广告，如果不取消的话欢迎使用ddddocr，本项目专注带动行业内卷
                        )
                    with open('target.png', 'rb') as f:
                        target_bytes = f.read()
                    with open('background.png', 'rb') as f:
                        background_bytes = f.read()
                    #这个是只能识别第一个相似点的位置，实际上我需要识别的是第二个，第二个才是目标位置，其横坐标就是滑块位置
                    res = det.slide_match(target_bytes,
                                        background_bytes,
                                        simple_target=True,#进行简单识别，如果小图无过多背景部分，则可以添加simple_target参数，通常为jpg或者bmp格式的图片
                                        # simple_target=False,#不进行简单识别（可能是两图识别），
                                        )#计算出来图片里面的滑块宽度是70
                    target=res.get('target')[2]/zoom_level#这里其实就差了一个1.25的缩放值，本身滑块的偏移和图片计算的偏移有区别，get('target')[0]是左侧位置，get('target')[2]是右侧位置
                    print("网页滑块图片的宽度",drop,"本地滑块图片的宽度",(res.get('target')[2]-res.get('target')[0]),"计算相似点位置",res,"需要滑行的长度",target)
                    if drop==(res.get('target')[2]-res.get('target')[0]):
                        print("网页和本地图片大小一致")#实际上我读取的像素应该还是有区别的这个是1.5倍
                    # 后续可以改成随机多次拖拽法，避免网站风控
                    time.sleep(waittime)
                    #selector定位法
                    slider=driver.find_element(By.CSS_SELECTOR,r"#slideVerifyDragControl > div.valid-code__drag-handle.handler")#聚宽登录界面的滑块位置
                    # slider=driver.find_element(By.CSS_SELECTOR,r"#drag > div.valid-code__drag-handle.handler")#聚宽签到领积分界面的滑块位置
                    # print(slider)
                    action = ActionChains(driver)
                    action.click_and_hold(slider).perform()  # 点击并拖动滑块开始位置  
                    action.move_by_offset(xoffset=target,#横向位移值为x
                                        yoffset=0,#纵向位移值为0
                                        ).perform()  # 移动到目标位置，需要计算偏移量  
                    action.release().perform()  # 松开鼠标，完成拖动操作
                    time.sleep(waittime*3)
                except Exception as e:
                    print("验证成功不再重复拖动滑块")
                    break
        #跳转到固定文章【没收益】
        # driver.get(r'https://www.joinquant.com/view/community/detail/ca92ee7ad8e46ff08a0f05df18429e8a')
        # time.sleep(waittime)

        #浏览社区文章【受限制】
        # driver.find_element("xpath",r"/html/body/section/div/ul/li[4]/a").click()#点击社区
        # time.sleep(waittime)
        # driver.find_element("xpath",r"/html/body/section/main/div/div[2]/div[1]/div[3]/div[1]/div[3]/div").click()#第一篇文章
        # time.sleep(waittime)

        # # 初始化变量以跟踪滚动
        # time.sleep(waittime)
        # last_height=driver.execute_script("return document.body.scrollHeight")
        # driver.execute_script("window.scrollBy(0, {});".format(500))
        # time.sleep(waittime*2)

        #正常签到流程
        driver.find_element("xpath",r"/html/body/section/div/ul/li[1]/a").click()#点击首页
        time.sleep(waittime)
        driver.find_element("xpath",r"/html/body/section/main/div/div[1]/div[2]/div[1]/div[2]").click()#点击积分中心
        #先点击能点到的
        buttonlist=[
            r"/html/body/section/main/div/div[2]/div/div[2]/div[2]/dl/dd[1]/div[2]/div[2]/div[2]/div/button",
            r"/html/body/section/main/div/div[2]/div/div[2]/div[2]/dl/dd[1]/div[1]/div[2]/div[2]/div/button",
            r"/html/body/section/main/div/div[2]/div/div[2]/div[2]/dl/dd[2]/div[1]/div[2]/div[2]/div/button",
            r"/html/body/section/main/div/div[2]/div/div[2]/div[2]/dl/dd[2]/div[3]/div[2]/div[2]/div/button",
            ]
        for button in buttonlist:
            try:#有些按钮在灰色状态的时候XPATH的值不一样
                time.sleep(waittime)
                print(button)
                WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH,button)))
                driver.find_element("xpath",button).click()
                while True:#重复验证避免验证错
                    try:
                        #浮动窗口提取元素
                        time.sleep(waittime)
                        # 获取浏览器缩放级别，其实是1.25倍，后面经常算着不对是因为用成了1.5倍去换算了，另外后面位移也可以换成多个随机数逐步移动，每次休息0.01-0.05秒（随机数）
                        zoom_level = driver.execute_script("return window.devicePixelRatio;")
                        print("浏览器缩放级别",zoom_level)
                        # path=r"/html/body/div[7]/div/div/div[2]/div/div/div/div/div[1]"#这个是登录时的路径，在签到时的路径如下r"/html/body/div[7]/div/div[2]/div/div[1]"
                        classname=r"valid-code__div"
                        picname="background.png"#背景图
                        top,bottom,left,right=get_img(driver=driver,
                                                    targettype="classname",#参数为classname则根据classname确定元素，参数为path则根据path确定元素
                                                    path=False,#根据路径确定位置，一般设置为False
                                                    classname=classname,#根据类名确定位置
                                                    picname=picname,#背景图路径和名称
                                                    )
                        print(top,bottom,left,right)
                        # slidepath=r"/html/body/div[7]/div/div/div[2]/div/div/div/div/div[1]/div[67]"
                        slideclassname=r"valid-code__hq"
                        slidepicname="target.png"#滑块图
                        slidetop,slidebottom,slideleft,slideright=get_img(driver=driver,
                                                    targettype="classname",#参数为classname则根据classname确定元素，参数为path则根据path确定元素
                                                    path=False,#根据路径确定位置，一般设置为False
                                                    classname=slideclassname,#根据类名确定位置
                                                    picname=slidepicname,#背景图路径和名称
                                                    )
                        print(slidetop,slidebottom,slideleft,slideright)
                        
                        # 裁剪背景图像，裁剪掉最左侧的drop长度
                        drop=(slideright-slideleft)#背景图裁剪长度（在最左侧裁剪掉一个滑块的距离，避免识别成滑块本身）
                        screenshot = Image.open('background.png')
                        print("screenshot",screenshot)
                        captcha = screenshot.crop((drop, 0, screenshot.width, screenshot.height))
                        captcha.save('background.png')

                        import ddddocr#pip install ddddocr
                        # 如果安装速度慢可以换成pip install ddddocr -i https://pypi.tuna.tsinghua.edu.cn/simple/
                        det = ddddocr.DdddOcr(
                            # beta=True,#切换为第二套ORC模型
                            det=False,#det=False 表示不使用图像检测功能，
                            ocr=False,#ocr=False 表示不使用文字识别功能，
                            show_ad=False,#show_ad=False 表示不显示广告，如果不取消的话欢迎使用ddddocr，本项目专注带动行业内卷
                            )
                        with open('target.png', 'rb') as f:
                            target_bytes = f.read()
                        with open('background.png', 'rb') as f:
                            background_bytes = f.read()
                        #这个是只能识别第一个相似点的位置，实际上我需要识别的是第二个，第二个才是目标位置，其横坐标就是滑块位置
                        res = det.slide_match(target_bytes,
                                            background_bytes,
                                            simple_target=True,#进行简单识别，如果小图无过多背景部分，则可以添加simple_target参数，通常为jpg或者bmp格式的图片
                                            # simple_target=False,#不进行简单识别（可能是两图识别），
                                            )#计算出来图片里面的滑块宽度是70
                        target=res.get('target')[2]/zoom_level#这里其实就差了一个1.25的缩放值，本身滑块的偏移和图片计算的偏移有区别，get('target')[0]是左侧位置，get('target')[2]是右侧位置
                        print("网页滑块图片的宽度",drop,"本地滑块图片的宽度",(res.get('target')[2]-res.get('target')[0]),"计算相似点位置",res,"需要滑行的长度",target)
                        if drop==(res.get('target')[2]-res.get('target')[0]):
                            print("网页和本地图片大小一致")#实际上我读取的像素应该还是有区别的这个是1.5倍
                        # 后续可以改成随机多次拖拽法，避免网站风控
                        time.sleep(waittime)
                        #selector定位法
                        # slider=driver.find_element(By.CSS_SELECTOR,r"#slideVerifyDragControl > div.valid-code__drag-handle.handler")#聚宽登录界面的滑块位置
                        slider=driver.find_element(By.CSS_SELECTOR,r"#drag > div.valid-code__drag-handle.handler")#聚宽签到领积分界面的滑块位置
                        # print(slider)
                        action = ActionChains(driver)
                        action.click_and_hold(slider).perform()  # 点击并拖动滑块开始位置  
                        action.move_by_offset(xoffset=target,#横向位移值为x
                                            yoffset=0,#纵向位移值为0
                                            ).perform()  # 移动到目标位置，需要计算偏移量  
                        action.release().perform() # 松开鼠标，完成拖动操作
                        time.sleep(waittime*3)
                    except Exception as e:
                        print("验证成功不再重复拖动滑块")
                        break
            except Exception as e:
                print("元素未在指定时间内加载，可能是灰色变化到其他路径了",e)
        time.sleep(waittime*2)
    # except Exception as e:
    #     print(e)

##切换回默认模块
# driver.switch_to.default_content()
##切换到目标iframe
# iframe=driver.find_element(By.CLASS_NAME,r"modal-content")
# driver.switch_to.frame(iframe)
##切换到新tab，假设新tab是第二个窗口句柄
# driver.switch_to.window(driver.window_handles[1])