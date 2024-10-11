import pandas as pd
# pip install alphalens-reloaded
import alphalens as al
import os
import seaborn as sns
import matplotlib.pyplot as plt
basepath=r"C:\Users\13480\Desktop\quant"
path="全部因子分析"
# path="大市值因子分析"
#数据拼接
all_files=os.listdir(f"{basepath}/{path}") #获取文件夹中的所有文件名
# alldf=pd.DataFrame({})
# num=0
for allfilename in all_files:
    if "csv" in allfilename:
        print(allfilename)
        factor_data=pd.read_csv(f"{basepath}/{path}/{allfilename}")
        filename, file_extension = os.path.splitext(allfilename)
        print(filename)

        #对原始数据重新更换索引
        factor_data["date"] = pd.to_datetime(factor_data["date"], utc=True)#存储和读取产生的格式转换问题
        factor_data.set_index(['date',"asset"], inplace=True)
        print(factor_data)

        #因子分位数区间【每一组的样本数】
        factor_quantile_actor_data=factor_data.groupby("factor_quantile").count()
        print(factor_quantile_actor_data)

        #回报分析
        mean_return_by_q_daily,std_err = al.performance.mean_return_by_quantile(factor_data, by_date=True)
        # #设置demeaned=False 计算为绝对收益
        # mean_return_by_q_daily,std_err = al.performance.mean_return_by_quantile(factor_data, by_date=False, demeaned=False)
        print(mean_return_by_q_daily,std_err)#std_err标准差
        # mean_return_by_q_daily.to_csv("回报分析.csv")
        # std_err.to_csv("标准差.csv")
        
        #在回报分析基础上的累积回报率【能输出】
        from alphalens.plotting import plot_cumulative_returns_by_quantile
        plot_cumulative_returns_by_quantile(mean_return_by_q_daily, period='1D')
        plt.rcParams['font.family'] = 'SimHei'  # 设置使用的字体为黑体
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 将黑体设置为默认的无衬线字体
        plt.title(filename)# 添加标题
        plt.legend(loc='upper right') # 设置图例位置为右上角
        plt.savefig(f"{basepath}/{path}/{filename}累积回报.jpg")# 保存为 jpg 格式图片
        plt.clf() # 清空数据

        #在回报分析基础上的日均回报率
        from alphalens.plotting import plot_quantile_returns_bar
        plot_quantile_returns_bar(mean_return_by_q_daily)
        # sns.despine()#边框样式【去除轴线】
        plt.rcParams['font.family'] = 'SimHei'  # 设置使用的字体为黑体
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 将黑体设置为默认的无衬线字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题
        plt.title(filename)# 添加标题
        plt.legend(loc='upper right') # 设置图例位置为右上角
        plt.savefig(f"{basepath}/{path}/{filename}日均回报（逐日计算）.jpg")# 保存为 jpg 格式图片
        plt.clf() # 清空数据

        #分布
        from alphalens.plotting import plot_quantile_returns_violin
        plot_quantile_returns_violin(mean_return_by_q_daily)
        # sns.despine()
        plt.rcParams['font.family'] = 'SimHei'  # 设置使用的字体为黑体
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 将黑体设置为默认的无衬线字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题
        plt.title(filename)# 添加标题
        plt.legend(loc='upper right') # 设置图例位置为右上角
        plt.savefig(f"{basepath}/{path}/{filename}分组分布（不区分日期）.jpg")# 保存为 jpg 格式图片
        plt.clf() # 清空数据

        #利差
        from alphalens.performance import compute_mean_returns_spread
        from alphalens.plotting import plot_mean_quantile_returns_spread_time_series
        qrs, ses = compute_mean_returns_spread(mean_return_by_q_daily,upper_quant=1, lower_quant=9,std_err=std_err)
        plot_mean_quantile_returns_spread_time_series(qrs, ses)
        plt.rcParams['font.family'] = 'SimHei'  # 设置使用的字体为黑体
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 将黑体设置为默认的无衬线字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题
        plt.title(filename)# 添加标题
        plt.legend(loc='upper right') # 设置图例位置为右上角
        plt.savefig(f"{basepath}/{path}/{filename}利差.jpg")# 保存为 jpg 格式图片
        plt.clf() # 清空数据