import time
from datetime import datetime, timedelta
import pandas as pd
import json
from selenium import webdriver


#账户密码登录推特【selenium模拟登陆过程，自动输入twitter账号和密码，并且获取cookies】
twi_username="1348006516@qq.com"
twi_password="wthWTH00"
# driver=webdriver.Chrome()#谷歌浏览器使用该方法方法.find_element("xpath","//*[@id=\"layers\"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input").send_keys(twi_username)
# # driver=webdriver.Edge()
# # driver=webdriver.Firefox()#火狐浏览器有单独的方法【这个方法谷歌浏览器没用】.find_element_by_xpath("//input[@data-testid='SearchBox_Search_Input']")

# driver.get(r'https://twitter.com/i/flow/login')
# print("初始化浏览器",driver)
# #这里睡几秒，等待页面加载。
# time.sleep(5)
# driver.find_element("xpath","//*[@id=\"layers\"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input").send_keys(twi_username)
# # print(driver)
# time.sleep(3)
# driver.find_element("xpath","//*[@id=\"layers\"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div").click()
# # print(driver)
# time.sleep(2)
# driver.find_element("xpath","//*[@id=\"layers\"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input").send_keys(twi_password)
# driver.find_element("xpath","//*[@id=\"layers\"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span").click()
# # print(driver)
# time.sleep(2)
# #使用这个函数可以导出driver的cookies
# savedCookies=driver.get_cookies()
# print("获取cookies",savedCookies)
# # DevTools listening on ws://127.0.0.1:53682/devtools/driver/4f0d7369-2d2d-4d33-8fdc-8e439f5ce6ac
# # [18300:504:0422/183303.327:ERROR:network_service_instance_impl.cc(599)] Network service crashed, restarting service.


# #直接使用Cookies登录推特
# driver=webdriver.Chrome()
# driver.get(r'https://twitter.com/i/flow/login')
# time.sleep(1)
# driver.delete_all_cookies()
savedCookies=[{'domain': '.twitter.com', 'expiry': 1748341850, 'httpOnly': True, 'name': 'auth_token', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'ceb0472cdf45245ee6d4bccde991c8a399ed4906'}, {'domain': '.twitter.com', 'expiry': 1713803450, 'httpOnly': False, 'name': 'ct0', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '2acc41ae50107238b4a2121fb9d34c27'}, {'domain': '.twitter.com', 'expiry': 1748341850, 'httpOnly': False, 'name': 'twid', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '"u=773393572724899840"'}, {'domain': '.twitter.com', 'expiry': 1748341826, 'httpOnly': False, 'name': 'guest_id_marketing', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'v1%3A171378182504694079'}, {'domain': '.twitter.com', 'expiry': 1748341836, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.2.602020201.1713781837'}, {'domain': '.twitter.com', 'expiry': 1748341850, 'httpOnly': True, 'name': 'kdt', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'u3NI0CFmeS6AxqZBPNRuANtkYJ5PJw1LOWdvH8yK'}, {'domain': '.twitter.com', 'expiry': 1748341825, 'httpOnly': False, 'name': 'guest_id', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'v1%3A171378182504694079'}, {'domain': '.twitter.com', 'expiry': 1713790826, 'httpOnly': False, 'name': 'gt', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1782356274484846800'}, {'domain': '.twitter.com', 'expiry': 1748341826, 'httpOnly': False, 'name': 'personalization_id', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '"v1_99mDmaxhO3YQatPBf53UbQ=="'}, {'domain': '.twitter.com', 'expiry': 1713868236, 'httpOnly': False, 'name': '_gid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.2.74225981.1713781837'}, {'domain': '.twitter.com', 'httpOnly': True, 'name': '_twitter_sess', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDmCWwWPAToMY3NyZl9p%250AZCIlYzRlZDE1NDk3MWIwYjNjM2VlNzE5ODYzZDg1Yjc3ZDc6B2lkIiUwYzM2%250AZGJmMDIzNGQxZDcwYWNhZDlhNmFlZTNlYmUxZQ%253D%253D--055d223dbaa256ad7b4929906050cd0a352cf780'}, {'domain': '.twitter.com', 'expiry': 1748341826, 'httpOnly': False, 'name': 'guest_id_ads', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'v1%3A171378182504694079'}]
# for cookie in savedCookies:
#     for k in {'name', 'value', 'domain', 'path', 'expiry'}:
#         # cookie.keys()属于'dict_keys'类，通过list将它转化为列表
#         if k not in list(cookie.keys()):
#             # saveCookies中的第一个元素，由于记录的是登录前的状态，所以它没有'expiry'的键名，我们给它增加
#             if k=='expiry':
#                 t=time.time()
#                 cookie[k]=int(t)  # 时间戳s
#     driver.add_cookie({k: cookie[k] for k in {'name', 'value', 'domain', 'path', 'expiry'}})
#     savedCookies=driver.get_cookies()
#     print("获取cookies",savedCookies)


cookies=savedCookies[0]
#将爬取的时间转换为国区时间
def Standardization_time(publish_date):
    # 将日期转换为标准格式
    from datetime import datetime, timedelta
    # 将字符串转换为datetime对象
    utc_dt=datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    # 由于中国是UTC+8，我们将UTC时间加上8小时得到中国时间
    # 注意：这里简单地加上时差，如果需要考虑夏令时等复杂情况，使用pytz库会更准确
    china_dt=utc_dt+ timedelta(hours=8)
    # 将日期格式化为所需格式
    formatted_date=china_dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date
#将获取的评论数，点赞数等转换为数字格式，使可以符合mysql里表格的字段要求
def Standardization_cout(str):
    try:
        # 移除逗号
        views_str_cleaned=str.replace(',', '')
        # 将清理后的字符串转换为整数
        views_int=int(views_str_cleaned)
        return views_int
    except:
        pass
#【推特搜索数据本地化】
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# pip install webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
def crawl_daily_tweets(cookies,keywords,start_date, days):
    # 将关键词字符串分割成列表
    keyword_list=keywords.split(',')
    # 转换字符串日期为datetime对象
    start=datetime.strptime(start_date, "%Y-%m-%d")
    for keyword in keyword_list:#遍历每一个索引词
        for i in range(days):#遍历每一天
            day=start+ timedelta(days=i)
            # 对于每一天，构建一个网址
            day_str=day.strftime("%Y-%m-%d") # 转换回字符串格式
            next_day_str=(day+ timedelta(days=1)).strftime("%Y-%m-%d")
            # 在这里调用你的爬取函数，传入构建的网址
            target_url=f"https://twitter.com/search?q={keyword.strip()}%20until%3A{next_day_str}%20since%3A{day_str}&src=typed_query"
            # 根据传入的cookie创建一个ChromeOptions实例
            options=Options()
            # 设置为无头模式
            options.add_argument('--headless')
            # 创建浏览器实例
            driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            # 首先访问Twitter的主页以设置域
            driver.get("https://twitter.com")
            # 休息
            time.sleep(2)
            # 添加Cookie
            for k in {'name', 'value', 'domain', 'path', 'expiry'}:
                # cookies.keys()属于'dict_keys'类，通过list将它转化为列表
                if k not in list(cookies.keys()):
                    # saveCookies中的第一个元素，由于记录的是登录前的状态，所以它没有'expiry'的键名，我们给它增加
                    if k=='expiry':
                        t=time.time()
                        cookies[k]=int(t)  # 时间戳s
            driver.add_cookie({k: cookies[k] for k in {'name', 'value', 'domain', 'path', 'expiry'}})
            savedCookies=driver.get_cookies()
            print("添加cookies",savedCookies)
            # 休息
            time.sleep(2)
            # 重新加载或访问目标网页
            driver.get(target_url)
            print("使用cookie搜索")
            # 休息
            time.sleep(2)
            # import pymysql
            # # 数据库连接配置
            # config={
            #     'host': 'localhost',
            #     'user': 'root',
            #     'password': 'root',
            #     'database': 'weibo',
            #     'charset': 'utf8mb4',
            # }
            # # 建立数据库连接
            # mysql_db=pymysql.connect(**config)
            # # 创建游标对象
            # cursor=mysql_db.cursor()
            # # 创建表的SQL语句（如果还没有创建）
            # create_table_sql="""
            #                         CREATE TABLE IF NOT EXISTS tweets (
            #                             tweet_url VARCHAR(255) NOT NULL PRIMARY KEY,
            #                             username VARCHAR(100) NOT NULL,
            #                             tweet_content TEXT NOT NULL,
            #                             publish_date DATETIME,
            #                             comments INT DEFAULT 0,
            #                             retweets INT DEFAULT 0,
            #                             likes INT DEFAULT 0,
            #                             views INT DEFAULT 0,
            #                             get_time DATETIME NOT NULL,
            #                             keyword VARCHAR(100)
            #                         );
            #                         """
            # # 执行创建表的SQL语句
            # try:
            #     cursor.execute(create_table_sql)
            #     mysql_db.commit()
            #     print("Table created successfully.")
            # except Exception as e:
            #     mysql_db.rollback()
            #     print(f"Failed to create table: {e}")
            # finally:
            #     cursor.close()
            # 获取数据
            import random
            crawled_tweets_urls=[]
            # 初始化变量以跟踪滚动
            last_height=driver.execute_script("return document.body.scrollHeight")
            max_retries=5  # 允许的最大重试次数
            retries=0  # 当前重试次数
            while retries < max_retries:
                driver.execute_script("window.scrollBy(0, {});".format(random.randint(200, 800)))
                time.sleep(random.uniform(2, 4.5))
                # 这里设置最长等待时间为10秒
                article_content=WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='cellInnerDiv']/div/div/article")))
                for article in article_content:
                    try:
                        # 获取推文的网址
                        tweet_url=article.find_element(By.XPATH, ".//time/..").get_attribute("href")
                        if tweet_url not in crawled_tweets_urls:
                            crawled_tweets_urls.append(tweet_url)
                            try:
                                # 获取用户名
                                username=article.find_element(By.XPATH, ".//div[@data-testid='User-Name']//span").text
                                # 获取推文内容
                                tweet_content=article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                                # 获取发布日期
                                publish_date=article.find_element(By.XPATH, ".//time").get_attribute('datetime')
                                publish_date=Standardization_time(publish_date)
                                # 获取评论数
                                comments=article.find_element(By.XPATH,
                                                                ".//div[@data-testid='reply']//span").text if article.find_elements(
                                    By.XPATH, ".//div[@data-testid='reply']//span") else "0"
                                comments=Standardization_cout(comments)
                                # 获取转发数
                                retweets=article.find_element(By.XPATH,
                                                                ".//div[@data-testid='retweet']//span").text if article.find_elements(
                                    By.XPATH, ".//div[@data-testid='retweet']//span") else "0"
                                retweets=Standardization_cout(retweets)
                                # 获取点赞数
                                likes=article.find_element(By.XPATH,
                                                            ".//div[@data-testid='like']//span").text if article.find_elements(
                                    By.XPATH, ".//div[@data-testid='like']//span") else "0"
                                likes=Standardization_cout(likes)
                                # 获取查看次数（如果可用）
                                views=article.find_element(By.XPATH,
                                                            ".//a[contains(@href,'analytics')]//span").text if article.find_elements(
                                    By.XPATH, ".//a[contains(@href,'analytics')]//span") else "0"
                                views=Standardization_cout(views)
                                #关键词
                                keyword=keyword
                                #爬取时间
                                get_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                # 抓取数据并存储到字典
                                tweet_data={
                                    "tweet_url": tweet_url,
                                    "username": username,
                                    "tweet_content": tweet_content,
                                    "publish_date": publish_date,
                                    "comments": comments if comments else "0",
                                    "retweets": retweets if retweets else "0",
                                    "likes": likes if likes else "0",
                                    "views": views if views else "0",
                                    "get_time": get_time,
                                    "keyword": keyword,
                                }
                                # # 数据库连接配置
                                # config={
                                #     'host': 'localhost',
                                #     'user': 'root',
                                #     'password': 'root',
                                #     'database': 'weibo',
                                #     'charset': 'utf8mb4',
                                # }
                                # # 建立数据库连接
                                # mysql_db=pymysql.connect(**config)
                                # # 创建游标对象
                                # cursor=mysql_db.cursor()
                                # # 插入或更新数据的SQL语句模板
                                # insert_or_update_sql="""
                                # INSERT INTO tweets (
                                #     tweet_url, username, tweet_content, publish_date, 
                                #     comments, retweets, likes, views, get_time, keyword
                                # ) VALUES (%(tweet_url)s, %(username)s, %(tweet_content)s, %(publish_date)s, 
                                # %(comments)s, %(retweets)s, %(likes)s, %(views)s, %(get_time)s, %(keyword)s)
                                # ON DUPLICATE KEY UPDATE 
                                #     username=VALUES(username),
                                #     tweet_content=VALUES(tweet_content),
                                #     publish_date=VALUES(publish_date),
                                #     comments=VALUES(comments),
                                #     retweets=VALUES(retweets),
                                #     likes=VALUES(likes),
                                #     views=VALUES(views),
                                #     get_time=VALUES(get_time),
                                #     keyword=VALUES(keyword);
                                # """
                                # # 执行插入或更新数据的SQL语句
                                # try:
                                #     cursor.execute(insert_or_update_sql, tweet_data)
                                #     mysql_db.commit()
                                #     print("Data inserted or updated successfully.")
                                # except Exception as e:
                                #     mysql_db.rollback()
                                #     print(f"Insert or update data error: {e}")
                                # finally:
                                #     cursor.close()
                                print(f"Tweet URL: {tweet_url}, Username: {username}, Tweet_content: {tweet_content}, Date: {publish_date}, Comments: {comments}, Retweets: {retweets}, Likes: {likes}, Views: {views}, Get_time: {get_time}, Keyword: {keyword}")
                                print('-----------')
                                # tweet_data_df=pd.DataFrame({"tweet_data":[tweet_data]})
                                tweet_data=pd.Series(tweet_data,name=str(get_time))#生成序列并命名为tweet_data的值
                                tweet_data_df=pd.DataFrame(tweet_data)#报错信息：If using all scalar values, you must pass an index
                                tweet_data_df.to_csv(f"推文关键词_{keyword}_{str(tweet_content)}.csv")
                            except Exception as e:
                                print(f'提取信息时出错: {e}')
                        else:
                            continue
                    except Exception as e:
                        print(f'提取信息时出错: {e}')
                # 检查页面滚动高度是否有变化
                new_height=driver.execute_script("return document.body.scrollHeight")
                if new_height==last_height:
                    retries+=1
                    print(f"第{retries}次重试...")
                else:
                    last_height=new_height
                    retries=0 # 重置重试次数
                    print("检测到新内容，继续爬取...")
            # input("已到达页面底部或重试次数已达上限，按Enter键继续...")#让用户主动继续，在终端输出这一行，当用户按Enter键之后才继续执行
# # 此代码一共可以爬取包括推文网址，推文作者，推文内容，推文点赞数，转发数，浏览数，评论数，爬取时间，推文发布时间还有关键词等10个字段。
# crawl_daily_tweets(cookies=cookies,keywords="马斯克,推文",start_date="2024-04-22",days=2)#拿到的是start_date日期之后days天的数据



# #【自动发表推文】
# options=Options()
# # 设置为无头模式
# options.add_argument('--headless')
# # 创建浏览器实例
# driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# # 首先访问Twitter的主页以设置域
# driver.get("https://twitter.com")
# # 休息
# time.sleep(2)
# # 添加Cookie
# for k in {'name', 'value', 'domain', 'path', 'expiry'}:
#     # cookie.keys()属于'dict_keys'类，通过list将它转化为列表
#     if k not in list(cookies.keys()):
#         # saveCookies中的第一个元素，由于记录的是登录前的状态，所以它没有'expiry'的键名，我们给它增加
#         if k=='expiry':
#             t=time.time()
#             cookies[k]=int(t)  # 时间戳s
# driver.add_cookie({k: cookies[k] for k in {'name', 'value', 'domain', 'path', 'expiry'}})
# savedCookies=driver.get_cookies()
# print("添加cookies",savedCookies)
# time.sleep(2)
# # 重新加载或访问目标网页【跳转到发推文页面】
# driver.get("https://twitter.com/compose/post")
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# print("等待登录完毕")
# # 等待登录完成
# driver.implicitly_wait(2)  # 等待10秒
# tweet_box = driver.find_element(By.XPATH, ".//div[@data-testid='tweetTextarea_0']") # 【这个位置输出是文字信息】使用 By.XPATH 来定位推文输入框
# print("获取推文输入框",tweet_box,type(tweet_box),tweet_box.text)
# tweet_box.send_keys("大家好,这是我通过自动化工具发表的推文!")
# #发送推文
# tweet_box_return = driver.find_element(By.XPATH, ".//div[@data-testid='tweetButton']") # 【这个位置输出是文字信息】使用 By.XPATH 来定位推文输入框
# # print(tweet_box_return)
# tweet_box_return.send_keys(Keys.RETURN)# 模拟按下回车键发布推文tweetButtonInline



# #【推特转评赞】
# options=Options()
# # 设置为无头模式
# options.add_argument('--headless')
# # 创建浏览器实例
# driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# # 首先访问Twitter的主页以设置域
# driver.get("https://twitter.com")
# # 休息
# time.sleep(2)
# # 添加Cookie
# for k in {'name', 'value', 'domain', 'path', 'expiry'}:
#     # cookie.keys()属于'dict_keys'类，通过list将它转化为列表
#     if k not in list(cookies.keys()):
#         # saveCookies中的第一个元素，由于记录的是登录前的状态，所以它没有'expiry'的键名，我们给它增加
#         if k=='expiry':
#             t=time.time()
#             cookies[k]=int(t)  # 时间戳s
# driver.add_cookie({k: cookies[k] for k in {'name', 'value', 'domain', 'path', 'expiry'}})
# savedCookies=driver.get_cookies()
# print("添加cookies",savedCookies)
# time.sleep(2)
# # 重新加载或访问目标网页【跳转到需要转评赞的推文页面】
# taegeturl="https://twitter.com/BithomeSwap/status/1781657704358109353"
# driver.get(taegeturl)
# # 等待登录完成
# driver.implicitly_wait(2)  # 等待10秒
# from selenium.webdriver.common.keys import Keys
# # 自动点赞
# likes=driver.find_element(By.XPATH,".//div[@data-testid='like']")
# likes.send_keys(Keys.RETURN)
# time.sleep(2)
# print("点赞成功")
# # 自动转发
# retweets=driver.find_element(By.XPATH,".//div[@data-testid='retweet']").click()
# retweets=driver.find_element(By.XPATH,".//div[@data-testid='retweetConfirm']").click()
# print("转发成功")
# time.sleep(2)
# # 自动评论
# comments=driver.find_element(By.XPATH,".//div[@data-testid='reply']")
# comments=driver.find_element(By.XPATH,".//div[@data-testid='tweetTextarea_0']")
# comments.send_keys("大家好,这是我通过自动化工具发表的推文!详情联系：")
# comments=driver.find_element(By.XPATH,".//div[@data-testid='tweetButtonInline']")
# comments.send_keys(Keys.RETURN)
# print("评论成功")
# time.sleep(2)



#【推特自动注册】【需要使用不同IP注册】【正在完善】
# 创建浏览器实例
driver=webdriver.Edge()
# 首先访问Twitter的主页以设置域
driver.get("https://twitter.com")
# driver.find_element(By.XPATH,".//div[@data-testid='tweetButtonInline']")
print(driver)
time.sleep(20000)


