# _*_coding: utf-8_*_
from random import Random
# django配置发送邮件的模块
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from EduWeb.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(12)

    email_record = EmailVerifyRecord()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "自学网注册激活链接"
        email_body = "请点击下面的链接激活账号：http://127.0.0.1:8000/active/{code}".format(code=code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass
    elif send_type == "forget":
        email_title = "自学网密码重置链接"
        email_body = "请点击下面的链接重置密码：http://127.0.0.1:8000/reset/{code}".format(code=code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass
    elif send_type == "update_email":
        email_title = "自学网邮箱修改验证码"
        email_body = "你的验证码为：{code}".format(code=code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass
