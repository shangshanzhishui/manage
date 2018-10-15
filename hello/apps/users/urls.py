# _*_ encoding:utf-8 _*_
from django.conf.urls import url,include


from .views import *


urlpatterns = [

    url(r'^login$',user_login,name='login'),#登陆
    url(r'^logout$',user_logout,name='logout'),#退出
    url(r'^register$',user_register,name='register'),#注册
    url(r'^post_reg_code$',send_regieser_code,name='forgetpwd'),#忘记密码
    url(r'^info$',user_home,name='user_home'),#用户信息
    url(r'^upload/image$',upload_image,name='upload_image'),#用户头像修改
    url(r'^update/pwd$',upload_password,name='upload_password'),#修改用户密码
    url(r'^reset$',reset,name='sendemil_code'),#发送邮箱验证码
    url(r'^post_reset$', post_reset, name="post_reset"),
    url(r'^update_email$',update_email,name='update_email'),#修改邮箱
    url(r'^passwdcode$',sendemil_code),#修改邮箱
    # url(r'^index/$',index),#修改邮箱

    # url(r'^updates/$',update,name='update_email'),#修改邮箱

]
