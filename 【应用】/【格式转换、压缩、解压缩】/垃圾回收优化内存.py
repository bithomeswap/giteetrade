import sys
import gc

import psutil # 调整内存占用
# 获取当前进程的内存占用情况
# process = psutil.Process()
# memory_info = process.memory_info()
# # 打印内存占用信息
# print("内存占用：")
# print(f"  物理内存占用：{memory_info.rss / (1024**2)} MB")
# print(f"  虚拟内存占用：{memory_info.vms / (1024**2)} MB")

import time
print(f"  物理内存占用：{psutil.Process().memory_info().rss / (1024**2)} MB")
time.sleep(1)
print(f"  物理内存占用：{psutil.Process().memory_info().rss / (1024**2)} MB")
import pandas as pd
df=pd.read_csv("美股train.csv")
print(f"  物理内存占用：{psutil.Process().memory_info().rss / (1024**2)} MB")
del df
unreachable_count = gc.collect()
time.sleep(1)
print(f"  物理内存占用：{psutil.Process().memory_info().rss / (1024**2)} MB")
print(unreachable_count)

# import time
# time.sleep(3)
# print(f"  虚拟内存占用：{psutil.Process().memory_info().vms / (1024**2)} MB")
# import pandas as pd
# df=pd.read_csv("美股train.csv")
# print(f"  虚拟内存占用：{psutil.Process().memory_info().vms / (1024**2)} MB")
# del df
# unreachable_count = gc.collect()
# time.sleep(1)
# print(f"  虚拟内存占用：{psutil.Process().memory_info().vms / (1024**2)} MB")
# print(unreachable_count)
# a = [1]
# b = [2]
# a.append(b)
# b.append(a)
# ####此时a和b之间存在循环引用####
# print(sys.getrefcount(a))   #结果应该是3
# print(sys.getrefcount(b))    #结果应该是3
# del a
# del b
# ####删除了变量名a，b到对象的引用，此时引用计数应该减为1，即只剩下互相引用了####
# try:
#     sys.getrefcount(a)
# except UnboundLocalError:
#      print ('a is invalid')
# ####此时，原来a指向的那个对象引用不为0，python不会自动回收它的内存空间####
# ####但是我们又没办法通过变量名a来引用它了，这就导致了内存泄露####
# unreachable_count = gc.collect()
# ####gc.collect()专门用来处理这些循环引用，返回处理这些循环引用一共释放掉的对象个数。这里返回是2####