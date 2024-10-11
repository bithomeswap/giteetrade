import time
from datetime import datetime, timedelta
import pandas as pd
import json
#关闭了2FA验证之后，直接监控最新邮件判断验证码
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver import EdgeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image

# import pyautogui#pip install pyautogui

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

# 打开参数【避免模拟的时候被平台识别为机器人】
alloptions.add_experimental_option('excludeSwitches', ['enable-automation']) # 避免终端下执行代码报警告
# driver=webdriver.Edge()#window.navigator.webdriver的值为true
driver=webdriver.Edge(options=alloptions)#window.navigator.webdriver的值为undefined【避免被平台识别为机器人】
# 设置浏览器窗口大小（可选）
driver.set_window_size(1024, 768)#调整窗口大小之后定位变了，但是还有偏离
# 使用JavaScript执行缩放操作100%【无效操作】
driver.execute_script("window.scrollTo(0, 0);")  # 滚动到页面顶部，确保元素坐标从顶部开始计算
driver.execute_script("document.body.style.zoom = '100%';")
# 首先访问Twitter的主页以设置域
driver.get('https://www.zoho.com/mail/lp/logout-review.html')
#每个步骤的等待时间
waittime=0.5

try:
    print("存在cookie，使用cookie登录")
    # 从文件加载 cookies
    with open("cookies.json", "r") as file:
        cookies = json.load(file)
    # for cookie in cookies:
    #     thisindex=cookies.index(cookie)
    #     print(thisindex)
    #     if 'expiry' in list(cookie.keys()):
    #         # 获取当前时间的时间戳
    #         current_time_stamp = int(time.time())
    #         # 将 expiry 的值设置为当前时间的时间戳
    #         cookies[thisindex]['expiry'] = current_time_stamp
    # print(cookies)
    # driver.delete_all_cookies()
    driver.add_cookie(cookies)
except Exception as e:
    print(e,"cookie登录失败重新模拟登录")
    driver.find_element(By.CSS_SELECTOR,r"#header > div.zgh-utilities > div.zgh-accounts > a.zgh-login").click()#登录
    time.sleep(waittime)
    username="1348006516@bithome.top"
    driver.find_element(By.CSS_SELECTOR,r"#login_id").send_keys(username)
    driver.find_element(By.CSS_SELECTOR,r"#nextbtn > span").click()#登录
    time.sleep(waittime)
    password="wthWTH00"
    driver.find_element(By.CSS_SELECTOR,r"#password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR,r"#nextbtn > span").click()#登录
    time.sleep(waittime)
    button=rf"#\37 217268000000008014 > div > div"
    WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,button)))
    driver.find_element(By.CSS_SELECTOR,button).click()
    time.sleep(waittime)
    # 加载 cookies 文件【这里的cookies不可以用于登录，应该是有另外的token】
    cookies=driver.get_cookies()
    print("获取cookies",type(cookies),cookies)
    with open("cookies.json", "w") as file:
        json.dump(cookies, file)
    # #获取token值,实际为null
    # sessionStoragesessionid = driver.execute_script('window.sessionStorage.getItem("sessionId");')
    # with open("sessionStoragesessionid.json", "w") as file:
    #     json.dump(sessionStoragesessionid, file)
    # sessionStoragetoken = driver.execute_script('window.sessionStorage.getItem("token");')
    # with open("sessionStoragetoken.json", "w") as file:
    #     json.dump(sessionStoragetoken, file)
    # localStoragetoken = driver.execute_script('window.localStorage.getItem("token");')
    # with open("localStoragetoken.json", "w") as file:
    #     json.dump(localStoragetoken, file)
    # windowlocalStoragetoken = driver.execute_script('window.localStorage.getItem("token")')
    # with open("windowlocalStoragetoken.json", "w") as file:
    #     json.dump(windowlocalStoragetoken, file)
    # #获取token
    # token=browser.execute_script('window.localStorage.getItem("token")')
    # print(token)
    # # js设置添加Token
    # browser.execute_script('window.localStorage.setItem("token", "token值")')

time.sleep(waittime)
# 定位到父元素
try:
    print("xpath定位成功")
    parent_element_name = r"/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div"
    parent_element = driver.find_element("xpath",parent_element_name)
except Exception as e:
    print("xpath定位失败")
    parent_element = driver.find_element(By.CSS_SELECTOR,"#zm_centerHolder > div.SCmWra > div > div > div.zmAppContent > div")

# 使用 XPath 获取所有直接子元素
child_elements = parent_element.find_elements("xpath",f".//div")#获取所有div后代标签
print("child_elements",child_elements)
for child in child_elements:# 打印每个子元素的标签名
    # child_xpath = child.get_attribute('xpath')
    # print(child,child_xpath)
    data_ty = child.get_attribute('data-ty')#只有一级标签有
    print("data-ty",data_ty)
    if data_ty=="lt":
    # child_class = child.get_attribute('class')
    # print("class",child_class)
    # dataaction = child.get_attribute('data-action')
    # print("dataaction",dataaction)
    # if dataaction=="pFolder":
        
        thisid = child.get_attribute('id')#只有一级标签有
        print("thisid",thisid)
        driver.find_element(By.ID,thisid).click()
        time.sleep(waittime)

        
        # 获取浏览器缩放级别
        zoom_level = driver.execute_script("return window.devicePixelRatio;")
        print("浏览器缩放级别",zoom_level)
        #定位元素
        #x_108899445elm_1618463748842 > table > tbody > tr > td【主文本】
        img=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#zm_centerHolder > div.SCmWra > div:nth-child(1) > div > div.SC_pv.shw.zmSMail > div.zmPV > div.zmPVContent > div.zmPVMailWrapper > div > div.zmMailWrapper")))
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
        # 保存并且识别图像
        picname="images.jpg"
        captcha.save(picname)
        # 实在不行这里直接截图然后AI识字（来判断是否有验证码）
        images = (picname)
        # # pip install easyocr
        import easyocr
        #设置识别中英文两种语言
        reader = easyocr.Reader(['ch_sim','en'], gpu =  False) # need to run only once to load model into memory
        result = reader.readtext((images), detail = 0)
        print(result)
        # 点击退出
        driver.find_element(By.CSS_SELECTOR,"#close").click()
        time.sleep(waittime)


        # 看完之后需要删除，不然会重复观看【跳到子元素里面的删除按钮】


# time.sleep(waittime)
#\31 721037241374116300
time.sleep(2000)
