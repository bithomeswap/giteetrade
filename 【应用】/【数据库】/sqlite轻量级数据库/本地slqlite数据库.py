#这个是操作的本地数据库
import sqlite3
conn = sqlite3.connect("First.db")    #连接数据库
cur = conn.cursor()         #创建游标实例
cur.execute("insert into T_fish Values('2018-3-29','鲤鱼',17,10.3,'john')")   #插入一条数据
cur.execute("insert into T_fish Values('2018-3-30','鲢鱼',9,9.2,'tim')")
conn.commit()   #提交数据保存到磁盘
cur.execute("select * from T_fish")    #查找表里的记录
for row in cur.fetchall():
    print(row)
cur.execute("delete from T_fish where nums=10")   #删除数量为10的记录
conn.commit()   #提交结果到硬盘
print('=='*50)
cur.execute("select * from T_fish")    #查找T_fish表里的记录
for row in cur.fetchall():
    print("记录",row)
conn.close()
