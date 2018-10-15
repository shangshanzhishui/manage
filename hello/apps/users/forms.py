# _*_ encoding:utf-8 _*_
__author__ = 'shangshanzhishui'

from django import forms
# from captcha.fields import CaptchaField
from .models import UserProfile,EmailVerifyRecord

class loginform(forms.Form):

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6)


class RegisterForm(forms.Form):
    email  = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6)


class forgetForm(forms.Form):
    email = forms.EmailField(required=True)
    # captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class resetpwdForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6)


class UpLoadImage(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]


class UserInfoUpdate(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["username","first_name","last_name","gender","address","mobile"]