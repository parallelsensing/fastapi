import os
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import re
def generate_unique_filename(original_filename):
    # 获取文件扩展名
    extension = os.path.splitext(original_filename)[1]
    # 生成唯一的UUID
    unique_id = uuid.uuid4()
    # 组合唯一标识符和扩展名
    unique_filename = f"{unique_id}{extension}"
    return unique_filename
def is_valid_email(email):
    # 正则表达式模式用于匹配常见的电子邮件格式
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


async def send_email(type:str, to_email:str, code:str,effective_time:int):
    
    # 设置邮件的发送者信息
    from_email = "dawnplatform1999@gmail.com"
    app_password = "jmvvpdtpvspvnhzu"

    # 根据邮件类型设置主题和邮件内容
    if type == "register":
        subject = "注册验证码"
        body = f"您好！感谢您注册我们的平台。您的验证码是：{code}。请在{effective_time}分钟内完成注册。"
    elif type == "reset_password":
        subject = "密码重置验证码"
        body = f"您好！您正在尝试重置密码。您的验证码是：{code}。请在{effective_time}分钟内完成密码重置。"
    else:
        print("无效的邮件类型")
        return

    # 创建MIMEMultipart邮件对象
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # 邮件内容
    msg.attach(MIMEText(body, 'plain'))

    # 连接到 Gmail 的 SMTP 服务器
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # 启动 TLS 加密
        server.login(from_email, app_password)  # 登录 Gmail
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)  # 发送邮件
        server.quit()
        print(f"邮件已成功发送到 {to_email}")
        return 1
    except Exception as e:
        print(f"发送邮件失败: {e}")
        return -1
# 发送带链接的邮件
async def send_link_email(type: str, to_email: str, link: str, effective_time: int):
    # 设置邮件的发送者信息
    from_email = "dawnplatform1999@gmail.com"
    app_password = "jmvvpdtpvspvnhzu"

    # 根据邮件类型设置主题和邮件内容
    if type == "reset_password":
        subject = "重置密码"
        body = f"""
        <html>
        <body>
            <p>您好！您正在尝试重置密码。</p>
            <p>请点击下面的链接修改密码：</p>
            <p><a href="{link}">重置链接</a></p>
            <p>请在{effective_time}分钟内完成密码重置。</p>
        </body>
        </html>
        """
    else:
        print("无效的邮件类型")
        return
    
    # 创建MIMEMultipart邮件对象
    msg = MIMEMultipart("alternative")
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # 将HTML邮件正文添加到消息中
    msg.attach(MIMEText(body, 'html'))
     
    # 连接到 Gmail 的 SMTP 服务器
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # 启动 TLS 加密
        server.login(from_email, app_password)  # 登录 Gmail
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)  # 发送邮件
        server.quit()
        print(f"邮件已成功发送到 {to_email}")
        return 1
    except Exception as e:
        print(f"发送邮件失败: {e}")
        return -1