#_*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name='昵称',default='')
    token = models.CharField(max_length=50,verbose_name="令牌")
    birday = models.DateTimeField(verbose_name='生日',null=True,blank=True)
    gender = models.CharField(max_length=50,choices=(('male',u'男'),('female',u'女')),default="female")
    address = models.CharField(max_length=100,default=u"")
    mobile = models.CharField(max_length=11,null=True,blank=True)
    image = models.ImageField(upload_to="image/%Y/%m",default=u"image/default.png",max_length=100)

    class Meta:
        verbose_name= "用户信息"
        verbose_name_plural = verbose_name

    def get_data(self):
        '''获得数据'''
        image_url = str(self.image)
        data ={
               "birday":self.birday,
               "gender":self.gender,
               "username":self.username,
               "address":self.address,
               "image":image_url,
               "is_superuser":self.is_superuser,
               "first_name":self.first_name,
               "last_name":self.last_name,
               "mobile":self.mobile,
               "email":self.email}
        return data

    def get_nums(self):
        """获得数据总量"""
        nums = UserProfile.objects.all().count()
        return nums



    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u"验证码")
    email = models.EmailField(max_length=50,verbose_name=u"邮箱")
    send_type = models.CharField(choices=(('register',u'注册'),('forget',u'找回密码'),('update_email',u'更新邮箱')),max_length=30)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证'
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s(%s)" %(self.code,self.email)
