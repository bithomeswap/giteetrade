import time
import sched
import subprocess
# 创建scheduler对象
schedule = sched.scheduler(time.time,time.sleep)
print(schedule)
# 计算执行时间
waittime=3600
# waittime=2
print(time.time())#返回一个浮点数，表示当前时间的时间戳
# 安排合并后的任务
schedule.enterabs(time.time()+waittime,1,subprocess.call([
    "python", r"C:\Users\13480\Desktop\quant\【回测】本地\【收益分布】指标收益分布（股票）.py"]),())#schedule.enterabs()方法接受4个参数：time（时间）、priority（优先级）、action（要执行的函数）、argument（函数的参数）
# schedule.enterabs(time.time(),1,subprocess.call([
    # "python", r"C:\Users\13480\Desktop\quant\【回测】本地\【收益分布】指标及rank后收益分布.py"]),())#schedule.enterabs()方法接受4个参数：time（时间）、priority（优先级）、action（要执行的函数）、argument（函数的参数）
