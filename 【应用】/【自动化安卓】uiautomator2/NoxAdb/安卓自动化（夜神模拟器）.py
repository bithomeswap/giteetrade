#【具体元素的定位需要和uiautomator2结合】模拟器太卡安卓自动化必须在物理机上进行
# pip install -U uiautomator2
import os
import re
import time
import random
# 运行时间 0.5 - 1 小时
print('Starting......')
r_time = 60 * random.randint(30, 60)
print("任务总时间：{} 分钟".format(int(r_time / 60)))
# global devices
devices=[]#获取设备端口列表
# 获取设备总数
def get_all_devices(devices):
    try:
        for device in os.popen("adb devices"):
            if "\t" in device:
                devices.append(device.split("\t")[0])
    except Exception as e:
        print(e)
        # _ = e
        pass
    print("设备: {} \t数量: {}台".format(devices, len(devices)))
get_all_devices(devices)
# print(devices)

# 获取设备屏幕 宽 高
def get_screen_params(devices):
    screen_w_h = {}
    for device in devices:
        print(device)

        # 获取分辨率
        f = os.popen("adb -s " + device + " shell wm size")
        w, h = re.search(r"(\d{3,4})x(\d{3,4})", f.read()).groups()
        screen_w_h[device] = [int(w), int(h)]
    return screen_w_h
screen_params = get_screen_params(devices)
print('屏幕参数: {}'.format(screen_params))

# 打开应用 com.kuaishou.nebula/com.yxcorp.gifshow.HomeActivity
for device in devices:#链接快手极速版【或者其他指定应用】
    # os.system("adb -s {} shell am start -n com.kuaishou.nebula/com.yxcorp.gifshow.HomeActivity".format(device))
    os.system("adb -s {} shell am start -n com.tencent.mm/.ui.LauncherUI".format(device))#打开微信
# 等待软件打开
time.sleep(7)



# #启动adb【无效可能是未开启USB调试】需要配置JAVA环境好麻烦换成影刀可能比较好
# # adb start-server
# # adb devices
# # python -m uiautomator2 init
# #【如果无法使用ui2连接，可能是没激活，也可能是abd没在环境变量当中】
# # adb shell dumpsys activity activities | findstr Run
# import uiautomator2 as u2#可能这样链接才稳定
# #这个框架不受javahome环境变量影响，不过adb命令还需要有，只是不需要借用java的adb了（用夜神模拟器原生的adb就行），
# # 但是再之前对夜神模拟器安装的时候需要安卓studio的原生的几个包里面的windows版本的apksigner.jar对夜神模拟器安装uiautomator2的包
# for device in devices:
#     print(device,type(device))
#     d =u2.connect(device)#'127.0.0.1:62001'
#     # d =u2.connect_usb(device)#'127.0.0.1:62001'
#     #得到设备的基本信息
#     print(d.info)
#     #启动app
#     d.app_start('com.tencent.mm/.ui.LauncherUI')
#     #上面的代码可以直接启动成功微信【无需过于冗杂java环境配置】
