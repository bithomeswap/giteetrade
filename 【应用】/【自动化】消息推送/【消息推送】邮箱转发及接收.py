# conda install pandas
import pandas as pd
# 发布到邮箱机器人
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
def postmessage(text,smtp_server_host,smtp_server_port,email_address,email_password,receiver_address):# 发送带附件的文件
    # 创建多部分邮件对象
    message = MIMEMultipart()
    message['From'] = email_address#设置发件人名称（邮件内部）
    message['To'] = Header('收件人名称', 'utf-8')#设置收件人名称（邮件内部）
    message['Subject'] = Header('邮件主题', 'utf-8')#设置邮件主题
    message.attach(MIMEText('测试邮件', 'plain', 'utf-8'))#添加文本消息到邮件
    # 创建 MIMEApplication对象
    csv_attachment=MIMEApplication(text.encode('utf-8'), 'csv')
    csv_attachment.add_header('Content-Disposition', 'attachment', filename='测试.csv')
    message.attach(csv_attachment)#添加附件到邮件
    #发送邮件
    try:
        # 连接SMTP服务器
        server = smtplib.SMTP(smtp_server_host, smtp_server_port)
        server.starttls()
        # 登录邮箱
        server.login(email_address, email_password)
        # 发送邮件
        server.sendmail(email_address, receiver_address, message.as_string())
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败:', str(e))
    finally:
        # 关闭连接
        server.quit()
# 邮箱服务器地址和端口（不同的端口执行不同的任务）
smtp_server_host = 'smtp.qq.com'
smtp_server_port = 587
email_address = "1348006516@qq.com"# 本人邮箱
email_password = "tfspjbixhevlihfi"# 本人邮箱授权码

#生成内容并发送邮件
receiver_address = "1348006516@qq.com"# 收件人邮箱
text=pd.DataFrame({'代码': [1, 2, 3], '列名': ['a', 'b', 'c']}).to_csv(index=False)
# postmessage(text,smtp_server_host,smtp_server_port,email_address,email_password,receiver_address)


import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
# 此函数通过使用poplib实现接收邮件
def recv_email_by_pop3(pop_server_host,pop_server_port,email_address,email_password):
    try:
        # 连接pop服务器。如果没有使用SSL，将POP3_SSL()改成POP3()即可其他都不需要做改动
        email_server = poplib.POP3_SSL(host=pop_server_host, port=pop_server_port, timeout=10)
        print("pop3----connect server success, now will check username")
    except:
        print("pop3----sorry the given email server address connect time out")
        exit(1)
    try:
        # 验证邮箱是否存在
        email_server.user(email_address)
        print("pop3----username exist, now will check password")
    except:
        print("pop3----sorry the given email address seem do not exist")
        exit(1)
    try:
        # 验证邮箱密码是否正确
        email_server.pass_(email_password)
        print("pop3----password correct,now will list email")
    except:
        print("pop3----sorry the given username seem do not correct")
        exit(1)
    # 邮箱中其收到的邮件的数量
    email_count = len(email_server.list()[1])
    # list()返回所有邮件的编号:
    resp, mails, octets = email_server.list()
    # 遍历所有的邮件
    for i in range(1, len(mails) + 1):
        # 通过retr(index)读取第index封邮件的内容；这里读取最后一封，也即最新收到的那一封邮件
        resp, lines, octets = email_server.retr(i)
        # lines是邮件内容，列表形式使用join拼成一个byte变量
        email_content = b'\r\n'.join(lines)
        try:
            # 再将邮件内容由byte转成str类型
            email_content = email_content.decode('utf-8')
        except Exception as e:
            print(str(e))
            continue
        # # 将str类型转换成<class 'email.message.Message'>
        # msg = email.message_from_string(email_content)
        msg = Parser().parsestr(email_content)
        print('------------------------------  华丽分隔符  ------------------------------')
        # 写入邮件内容到文件
        parse_email(msg, 0)
    # 关闭连接
    email_server.close()
# indent用于缩进显示:
def parse_email(msg, indent):
    if indent == 0:
        # 邮件的From, To, Subject存在于根对象上:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    # 需要解码Subject字符串:
                    value = decode_str(value)
                else:
                    # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        # 如果邮件对象是一个MIMEMultipart,
        # get_payload()返回list，包含所有的子对象:
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            # 递归打印每一个子对象:
            return parse_email(part, indent + 1)
    else:
        # 邮件对象不是一个MIMEMultipart,
        # 就根据content_type判断:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            # 纯文本或HTML内容:
            content = msg.get_payload(decode=True)
            # 要检测文本编码:
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content))
        else:
            # 不是文本，作为附件处理:
            print('%sAttachment: %s' % ('  ' * indent, content_type))
# 解码
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
# 猜测字符编码
def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        for item in content_type.split(';'):
            item = item.strip()
            if item.startswith('charset'):
                charset = item.split('=')[1]
                break
    return charset
# 邮箱对应的pop服务器，也可以直接是IP地址
# 改成自己邮箱的pop服务器；qq邮箱不需要修改此值
pop_server_host = "pop.qq.com"
# 邮箱对应的pop服务器的监听端口。改成自己邮箱的pop服务器的端口；qq邮箱不需要修改此值
pop_server_port = 995
recv_email_by_pop3(pop_server_host,pop_server_port,email_address,email_password)