import time
import pymysql#pip install pymysql

# #首次使用：2024-01-29，需要在mysql端建立合适的表格。

# 配置参数
HOST = 'mysql.sqlpub.com'#或者82.103.129.94【这个地址链接不到，域名可以连接到】
PORT = 3306
USER = 'bithome'
PASSWORD = 'ethrazgCcSHkrsKE'
DATABASE = 'bithome'

#有可能需要多链接几次(while True:)
connection = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE,
                        charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
print("链接成功",connection)
cursor=connection.cursor()#创建链接



# csvname="jqdata"#表名称



# # SQL 查询，检查表是否存在
# sql_check_table = f"SHOW TABLES LIKE '{csvname}'"#"INSERT INTO {} (data) VALUES (%s)".format(csvname)效果一样
# cursor.execute(sql_check_table)
# result = cursor.fetchone()
# if result:
#     print("表 'jqdata' 已存在,数据清空")
#     # 如果表存在，清空表中的数据
#     sql_truncate_table = f"TRUNCATE TABLE {csvname}"
#     cursor.execute(sql_truncate_table)
#     connection.commit()
# else:
#     print("表 'jqdata' 不存在,正在创建")
#     # 如果表不存在，创建表
#     sql_create_table =f"""
#     CREATE TABLE {csvname} (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         data VARCHAR(255) NOT NULL
#     )
#     """
#     cursor.execute(sql_create_table)
#     connection.commit()
#     print("表 'jqdata' 创建成功。")



# # SQL 插入语句【多行数据转成json】
# data_to_insert = {
#     'signal': ['SIGNAL_1', 'SIGNAL_2', 'SIGNAL_3'],
#     'created_at': ['2024-01-29 12:00:00', '2024-01-30 12:00:00', '2024-01-31 12:00:00']
# }
# import json# 将字典转换为 JSON 字符串
# data_to_insert = json.dumps(data_to_insert)
# sql_insert = f"INSERT INTO {csvname} (data) VALUES (%s)"#%s是sql为了防止注入攻击的占位符
# cursor.execute(sql_insert,data_to_insert)#插入单行数据
# cursor.execute(sql_insert,data_to_insert)#插入单行数据



# # # SQL 插入语句【多索引】
# # data_to_insert = {
# #     'signal': ['SIGNAL_1', 'SIGNAL_2', 'SIGNAL_3'],
# #     'created_at': ['2024-01-29 12:00:00', '2024-01-30 12:00:00', '2024-01-31 12:00:00']
# # }
# # sql_insert = """INSERT INTO jqdata (signal, created_at) VALUES (%s, %s)"""#%s是sql为了防止注入攻击的占位符
# # # 准备数据
# # data_to_insert = list(zip(data_to_insert['signal'], data_to_insert['created_at']))
# # # 插入多行数据
# # cursor.executemany(sql_insert,data_to_insert)#插入一个字典



# # SQL 查询语句
# sql_select = "SELECT data FROM jqdata"
# cursor.execute(sql_select)# 执行查询
# results = cursor.fetchall()# 获取所有查询结果
# print(results)
# # # 将 JSON 字符串转换回字典
# # for result in results:
# #     data = json.loads(result[0])
# #     print(data)  # 打印数据或进行其他处理


import pandas as pd
try:
    with connection.cursor() as cursor:
        # 查询数据库中所有表的名称
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        # 遍历所有表
        for table_name in tables:
            print(table_name)
            table_name = table_name['Tables_in_bithome']
            print(f"Exporting data from table {table_name}...")
            # 查询表中的数据
            cursor.execute(f"SELECT * FROM `{table_name}`")
            rows = cursor.fetchall()
            # print("rows",rows)
            # # 获取列名
            # column_names = [desc[0] for desc in cursor.description]
            # print("column_names",column_names)
            # # 将数据写入 CSV 文件
            df=pd.DataFrame(rows)
            df.to_csv(f"{table_name}.csv")
finally:
    # 关闭数据库连接
    connection.close()



# # 要删除的数据条件
# data_to_delete = 'SIGNAL_1'  # 根据你的表结构调整条件
# try:
#     with connection.cursor() as cursor:
#         # SQL 删除语句
#         sql_delete = "DELETE FROM jqdata WHERE %s data"
#         cursor.execute(sql_delete, data_to_delete)
#         connection.commit()
#         print("数据删除成功，删除的行数：", cursor.rowcount)
# finally:
#     # 关闭数据库连接
#     connection.close()



# ABSOLUTE_QUANTITY = True  # 绝对数量下单：True；相对比例下单：False

# # 初始化
# def initialize(context):
#     g.__connection = None  # 数据库连接
#     g.dealt_signals = {}  # 今日已执行指令
#     g.rongzi=[]

#     # 早上9:24打开数据库连接
#     run_daily(context, open_mysql_connection, time='9:24')
#     run_daily(context, get_rongzi, time='9:23')
#     # 每3秒查询一次交易指令
#     run_interval(context, interval_handle, seconds=3)
    
#     # 下午15:01关闭数据库连接
#     run_daily(context, close_mysql_connection, time='15:01')

# def get_rongzi(context):
#     g.rongzi=get_margincash_stocks()
    
# def get_trade_limit_price(stock):
    
#     df = get_snapshot(stock)
#     last_price = df[stock]['last_px']
#     high_limit = df[stock]['up_px']
#     low_limit = df[stock]['down_px']
    
#     buy_limit = min(round(max(last_price*1.015-0.01,last_price+0.1),2),high_limit)
#     sell_limit= max(round(min(last_price*0.985+0.01,last_price-0.1),2),low_limit)
    
#     return buy_limit,sell_limit    

# def handle_data(context, data):
#     pass

# def open_mysql_connection(context):
#     g.dealt_signals = {}  # 今日已执行指令，重置为空
#     g.__connection = get_db_connection()


# def get_db_connection():
#     attempts = 5  # 重试5次
#     while attempts:
#         try:
#             conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE,
#                                    charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
#             return conn
#         except Exception as e:
#             attempts -= 1
#             log.info("连接MySQL数据库失败，错误信息: %s" % repr(e))
#             time.sleep(1)
#     #
#     log.info("连接MySQL数据库失败，已达到最大尝试次数")
#     return None


# def get_trade_signals(context):
#     # type: (Context) -> Optional[List[dict]]
#     """查询交易信号"""
#     today = context.blotter.current_dt.date()
    
#     sql = "SELECT * FROM jddata WHERE DATE(time)='{}'".format(today)
#     #log.info(sql)
#     attempts = 3  # 重试3次
#     data = None
#     while attempts:
#         try:
#             conn = g.__connection  # type: pymysql.Connection
#             cursor = conn.cursor()
#             cursor.execute(sql)
#             data = cursor.fetchall()
#             cursor.close()
#             break
#         except Exception as e:
#             g.__connection = get_db_connection()
#             attempts -= 1
#     #
#     #log.info(data)
#     return data


# def del_trade_signal(pk_id):
#     """删除交易信号"""
#     sql = "DELETE FROM jddata WHERE id={id}".format(id=pk_id)
#     attempts = 3  # 重试3次
#     while attempts:
#         try:
#             conn = g.__connection  # type: pymysql.Connection
#             cursor = conn.cursor()
#             cursor.execute(sql)
#             cursor.close()
#             break
#         except Exception as e:
#             g.__connection = get_db_connection()
#             attempts -= 1


# def close_mysql_connection(context):
#     # log并删除今日未执行成功的指令单
#     data = get_trade_signals(context)
#     if (data is not None) and len(data) > 0:
#         for row in data:
#             pk_id = row['id']
#             log.info('今日未执行订单：方向：%s, 标的: %s, 数量: %d, 比例: %.4f, 策略: %s' % (
#                 row['action'], row['code'], row['quantity'], row['pct'], row['strategy']
#             ))
#             del_trade_signal(pk_id)
#     # 断开连接
#     if g.__connection is not None:
#         g.__connection.close()
#         g.__connection = None


# def interval_handle(context):
#     #log.info('程序正常运行，暂时没有交易')
#     # type: (Context) -> None
#     """
#     每3秒查询一次交易指令, 如有指令，则下单
#     """
#     now = context.blotter.current_dt
#     now_time = now.hour * 100 + now.minute
#     if not (925 < now_time < 1500):  # 非交易时间
#         return
#     data = get_trade_signals(context)
#     if data is None or len(data) == 0:
#         return

#     # 分离买单和卖单
#     sell_orders, buy_orders = [], []
#     for row in data:
#         if row['action'] == 'SELL':
#             sell_orders.append(row)
#         else:
#             buy_orders.append(row)

#     # 如果有卖单，则只执行卖单；否则，只执行买单
#     if len(sell_orders) > 0:
#         for row in sell_orders:
#             if row['id'] in g.dealt_signals:  # 该指令已经执行
#                 continue
            
#             security = row['code'].replace('XSHG', 'SS').replace('XSHE', 'SZ')
#             if ABSOLUTE_QUANTITY:
#                 quantity = row['quantity']
#             else:
#                 quantity = min(context.portfolio.positions[security].amount,
#                                int(context.portfolio.positions[security].amount * row['pct']))
#             # 卖单
#             buy_limit,sell_limit=get_trade_limit_price(security)
#             order_id = margin_trade(security, -quantity, market_type=4, limit_price=sell_limit)  # 负数表示卖出
#             if order_id is not None:  # 下单成功
#                 g.dealt_signals[row['id']] = order_id  # 记录订单id
#                 log.info('策略:%s, 卖出下单：%s, 数量：%d' % (row['strategy'], security, quantity))
#         # 很重要：暂时不再执行买单 #
#         return
#     else:  # 现在只有买单了
#         for row in buy_orders:
#             if row['id'] in g.dealt_signals:  # 该指令已经执行
#                 continue
#             security = row['code'].replace('XSHG', 'SS').replace('XSHE', 'SZ')
#             buy_limit,sell_limit=get_trade_limit_price(security)
#             if ABSOLUTE_QUANTITY:
#                 quantity = row['quantity']
#                 if security in g.rongzi:
#                     order_id = margincash_open(security, quantity, market_type=4, limit_price=buy_limit)  # 正数表示买入
#                 else:
#                     order_id = margin_trade(security, quantity, market_type=4, limit_price=buy_limit)  # 正数表示买入                
#                 tips = '数量: %d' % quantity
#             else:  # 按总资产百分比计算出的金额买入
#                 money = min(context.portfolio.cash,
#                             round(context.portfolio.portfolio_value * row['pct'], 2))
#                 order_id = order_value(security, money)  # 按金额买入
#                 tips = '金额: %.2f' % money
#             # 记录已经处理的指令
#             if order_id is not None:  # 下单成功
#                 g.dealt_signals[row['id']] = order_id  # 记录订单id
#                 log.info('策略:%s, 买入下单：%s, %s' % (row['strategy'], security, tips))

#     return


# def on_trade_response(context, trade_list):
#     for trade in trade_list:
#         if not trade['order_id']:      
#             continue
#         order_id = trade['order_id']
#         # 根据订单号找到数据表的主键id
#         pk_id = 0
#         for sig_id in g.dealt_signals:
#             if order_id == g.dealt_signals[sig_id]:
#                 pk_id = sig_id
#                 break
#         # 删除数据库中的指令
#         if pk_id:
#             del_trade_signal(pk_id)