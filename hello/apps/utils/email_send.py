# _*_ encoding:utf-8 _*_
__author__ = 'shangshanzhishui'
from random import Random
from django.core.mail import send_mail

from hello.settings import EMAIL_FROM
from users.models import EmailVerifyRecord


def send_email_register(email,send_type):
    email_recode = EmailVerifyRecord()
    if send_type == "update_email":
        random_str=generate_random_str(4)
    else:
        random_str = generate_random_str()
    email_recode.code=random_str
    email_recode.email = email
    email_recode.send_type = send_type
    email_recode.save()

    if send_type == "register":
        email_tittle = "hello注册"
        email_body = "验证码：{0}".format(random_str)
        send_status=send_mail(email_tittle,email_body,EMAIL_FROM,[email])
        if send_status:
            print("yes")
    elif send_type == "forget":
        email_tittle = "hello找回密码"
        email_body = "验证码：{0}".format(random_str)
        send_status = send_mail(email_tittle, email_body, EMAIL_FROM, [email])
        if send_status:
            print("yes")
    elif send_type == "update_email":
        email_tittle = "hello邮箱修改验证码"
        email_body = "您的验证码是：{0}".format(random_str)
        send_status = send_mail(email_tittle, email_body, EMAIL_FROM, [email])
        if send_status:
            print("yes")


def generate_random_str(char_length=18):
    str = ''
    chars = "QqWwEeRrTtYyUuIiOoPpAaSsDdFfGgHhJjKkLlZzXxCcVvBbNnMm123456789"
    length=len(chars)-1
    random = Random()
    for i in range(char_length):
        str += chars[random.randint(0,length)]
    return str

