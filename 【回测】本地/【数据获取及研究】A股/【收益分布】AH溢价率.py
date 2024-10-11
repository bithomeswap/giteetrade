import pandas as pd
import numpy as np
import os

##读取历史数据
path=r"/root/test/quant/【回测】本地/数据文件/COIN/"
# path=r"C:/Users/13480/Desktop/【回测】本地/数据文件/COIN/"

df=pd.read_csv(r"C:\Users\13480\gitee\quant\【回测】本地\数据文件\AH股价格对比.csv")

df=df.rename(columns={"a_code":"代码","day":"日期"})
df["代码"] = df["代码"].str.replace("\D","",regex=True).astype(str)
df["日期"]=df["日期"].str.replace("-","",regex=True).astype(float)
print(df)
olddf=pd.read_csv(r"C:\Users\13480\gitee\quant\【回测】本地\数据文件\全体A股\全体A股全部.csv")
olddf["代码"]=olddf["代码"].str.replace("\D","").astype(str)
olddf["日期"]=olddf["floatyesterday"]
df=df.merge(olddf,on=["日期","代码"],how="inner").reset_index(drop=True) # 拼接之前的可转债余额变动表
print(df)
df.to_csv("AH对比.csv")


df=pd.read_csv("AH对比.csv")

sorttype="等密度"#选择间距划分方式
# sorttype="等长度"
# 设置参数
a=50 # 将数据划分成a个等距离的区间
holddays=3 # 观察不同的持仓周期的涨跌分布

basepath="C:/Users/13480/Desktop/【回测】本地/数据文件"
path=r"全体A股" #文件夹路径
# path=r"可转债" #文件夹路径

df=df.sort_values(by="floattoday")#以日期列为索引,避免计算错误
# 删除数据类型不是float或者int的列
non_float_cols = df.select_dtypes(exclude='float').columns.tolist()
non_int_cols = df.select_dtypes(exclude='int').columns.tolist()
intersection = list(set(non_float_cols) & set(non_int_cols))
df = df.drop(intersection,axis=1)
#计算预期收益相关指标
df["target_stock"]=1
for num in range(0,holddays): #持仓2天收益比持仓3天高【貌似持仓两天也比持仓1天收益高，这里确定持仓天数】
    if num<=0:#开盘买入
        df["target_stock"]=df["target_stock"]*(df["target"+str(num)+"_stock_grow"]+1)#第一天早盘卖
        #df["target_stock"]=df["target_stock"]*(df["target"+str(num)+"_stock_quote_rate"]+1)#前一天收盘买
    else:#收盘卖出
        df["target_stock"]=df["target_stock"]*(df["target"+str(num)+"_stock_quote_rate"]+1)
df["target_stock"]=df["target_stock"]-1

df["h_a_comp_rank"]=df.groupby("floattoday")["h_a_comp"].rank(ascending=True)
df=df.groupby("floattoday", group_keys=False).apply(lambda x: x.assign(h_a_comp_rank_rate=(x["h_a_comp_rank"]/len(x))))

#普通类单指标展现
# for mubiao in df.columns:
for mubiao in ["h_a_comp","h_a_comp_rank_rate"]:
    print(mubiao)
    if (not(("target" in mubiao)or("Unnamed" in mubiao)))or(mubiao=="target0_open_rate"):#mubiao.isalpha()是用来验证是否为纯字母数据的
        print("输出概率分布")
        if sorttype=="等密度":
            # 等密度分段
            sorted_data=np.sort(df[f"{mubiao}"])#排序
            indices=np.linspace(0,len(df[f"{mubiao}"]),num=a+1,endpoint=True,dtype=int) #分段
            ranges=[]
            for i in range(len(indices)-1):
                start_idx=indices[i]
                end_idx=indices[i+1] if i !=(len(indices)-2) else len(df[f"{mubiao}"]) # 最后一段需要特殊处理
                upper_bound=sorted_data[end_idx-1] # 注意索引从0开始，因此要减1
                ranges.append((sorted_data[start_idx],upper_bound))
                # print(ranges)
        elif sorttype=="等长度":
            maxnum=df[f"{mubiao}"].max()
            # 等长度分段
            ranges=[]
            for i in range(0,a):
                start_idx=i/a*maxnum
                end_idx=start_idx+1/a*maxnum
                ranges.append([start_idx,end_idx])
                # print(ranges)
        # 生成收益率分布表
        result_df=pd.DataFrame({})
        for rank_range in ranges:
            thisdf=df.copy()
            thisdf=thisdf[(thisdf[f"{mubiao}"]>=rank_range[0])&(thisdf[f"{mubiao}"]<rank_range[1])]
            # thisdf.to_csv(f"from{rank_range[0]}to{rank_range[1]}.csv")
            up_thisdf=thisdf[thisdf[f"target_stock"]>0].copy()
            zero_thisdf=thisdf[thisdf[f"target_stock"]==0].copy()
            down_thisdf=thisdf[thisdf[f"target_stock"]<0].copy()
            thisdf=pd.DataFrame({
                f"{mubiao}": [f"[{rank_range[0]},{rank_range[1]})"],
                f"未来{holddays}日上涨次数": [len(up_thisdf)],
                f"未来{holddays}日横盘次数": [len(zero_thisdf)],
                f"未来{holddays}日下跌次数": [len(down_thisdf)],
                f"未来{holddays}日总次数": [len(thisdf)],
                # f"未来{holddays}日上涨概率": [len(up_thisdf)/len(thisdf)],#用张总的方式有空值
                f"未来{holddays}日平均涨跌幅": [thisdf[f"target_stock"].mean()],
            })
            result_df=pd.concat([result_df,thisdf])
        result_df.round(decimals=6).to_csv(f"{mubiao}持有{holddays}日平均收益分布.csv")
        print(result_df,"任务已经完成")


#排名类多指标组合
ranges=[]
left=0
right=1
step=(right-left)/a
for i in range(a):
    ranges.append((left+i*step,left+(i+1)*step))
# 生成收益率分布表
result_df=pd.DataFrame({})
# 循环处理每个指标和区间
rank_cols=df.filter(like="_rank_rate").columns.tolist()# 筛选出列名中包含"rank"的列
for rank_range in ranges:
    col_result_df=pd.DataFrame()  # 创建一个空的DataFrame，用于存储指标的结果
    for col_name in rank_cols:
        # 根据区间筛选DataFrame
        sub_df=df[(df[col_name]>=rank_range[0])&(df[col_name]<rank_range[1])]
        # 计算收益
        sub_df_mean=sub_df.mean(numeric_only=True)  # 均值法
        # 构造包含指标名和涨跌幅的DataFrame，并添加到列结果DataFrame中
        result_sub_df=pd.DataFrame({col_name:[sub_df_mean[f"target_stock"]]},index=[rank_range])
        col_result_df=pd.concat([col_result_df,result_sub_df],axis=1)
    result_df=pd.concat([result_df,col_result_df])
# 新建涨跌分布文件夹在上级菜单下，并保存结果
result_df.round(decimals=6).to_csv(f"持有{holddays}日平均收益分布.csv")
print("任务已经完成")
# #打印部分标的
# printdf=df.copy()[(df["净总被动买入特大单金额_rank_rate"]>=0.68)&(df["净总被动买入特大单金额_rank_rate"]<=0.70)]
# printdf.to_csv("printdf.csv")
# 固定长度分段