# _*_ encoding:utf-8 _*_
import json
from django.shortcuts import get_object_or_404
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,render_to_response
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
# from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
# Create your views here.
from utils.ajax import ajax_ok_data,ajax_fail_data,ajax_ok
from .forms import *
from .models import UserProfile,EmailVerifyRecord
from utils.email_send import send_email_register

from utils.auth import create_token

def CookieAuth(func):
  def inner(reqeust,*args,**kwargs):
    v = reqeust.COOKIES.get("token")
    if not v:
      return ajax_fail_data(message="请重新登陆")
    return func(reqeust, *args,**kwargs)
  return inner

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):

                return user
        except Exception as e:
            return None
# def index(request):
# if request.method == "GET":

def user_login(request):
    if request.method == "POST":

        login_form = loginform(request.POST)
        if login_form.is_valid():
            print(111)
            email=username = request.POST.get("email","")
            password = request.POST.get("password","")
            user = authenticate(username=username,password=password)
            if user:
                if user.is_staff:
                    # request.session["token"] = user.token
                    # response = render(request)
                    # response.set_cookie()
                    # login(request,user)
                    return ajax_ok(request)

                else:
                    return ajax_fail_data(message="用户未激活")
            else:
                return ajax_fail_data(message="用户名或者密碼錯誤")

        else:
            return ajax_fail_data(message="输入错误")
    # elif request.method == "GET":
    #     course_banner = Couse.objects.filter(is_banner=True)[:3]
    #     return render(request,'login.html',{"course_banner":course_banner})

def user_logout(request):
    if request.method == "GET":
        if request.GET =="o":
            logout(request)

        return HttpResponseRedirect(reverse("index"))


def user_register(request):
 """注册"""
 if request.method == "POST":
     print("开始注册")
     register_form = RegisterForm(request.POST)
     if 1:

         email = request.POST.get("email", "")
         username = request.POST.get("username", "")
         password = request.POST.get("password", "")
         code = request.POST.get("code")
         try:
             user_profile = UserProfile.objects.get(Q(username=username) | Q(email=email))

         except Exception as e:
             user_profile = None
         if user_profile:
             if user_profile.is_staff:
                 return ajax_fail_data(message="用戶已存在")
         code = EmailVerifyRecord.objects.get(code=code,email=email,send_type="register")
         if not code:
             return ajax_fail_data(message="请输入正确验证码")
         token = create_token(email)
         user_profile = UserProfile()
         user_profile.username = username
         user_profile.is_staff = True
         user_profile.email = email
         user_profile.password = make_password(password)
         user_profile.token = token
         user_profile.save()
         return ajax_ok_data()
     else:
         print("fuck")
         data = register_form
         return ajax_ok_data(data)

def active(request,active_code):
    """激活"""
    if request.method =="GET":
        emil_recode = EmailVerifyRecord.objects.filter(code=active_code)
        if emil_recode:
            for cord in emil_recode:
                email = cord.email
                user = UserProfile.objects.get(email=email)
                user.is_staff = True
                user.save()
            return ajax_ok_data()
        else:
            return ajax_fail_data()

def send_regieser_code(request):
    """注册获取验证码"""
    if request.method =="POST":
        email = request.POST.get("email",'')
        status = send_email_register(email,"register")
        if status:
            return ajax_ok_data(message = "邮件发送成功，请注意查收")
        else:
            return ajax_ok_data(message="邮件发送失败")


# def reset(request,reset_code):
#     """验证找回密码链接"""
#     if request.method =="GET":
#         emil_recode = EmailVerifyRecord.objects.filter(code=reset_code)
#         if emil_recode:
#             for cord in emil_recode:
#                 email = cord.email
#                 data = email
#                 return ajax_ok_data(data)
#
#         else:
#             return ajax_fail_data(message="出錯了！！！！！")

def post_reset(request):
    """重置密码"""
    if request.method== "POST":
        repwd_form = resetpwdForm(request.POST)
        if repwd_form.is_valid():
            print("success")
            code = request.POST.get("code",'')
            password = request.POST.get("password",'')
            email = request.POST.get("email",'')
            recoreded = EmailVerifyRecord.objects.get(code=code,send_type="forget")

            user = UserProfile.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return ajax_ok_data(message="修改成功")

        data = repwd_form
        return ajax_ok_data(data)


def user_home(request):
    if request.method == "GET":
        email = request.GET.get("email","")
        page = request.GET.get("p","1") #第几页
        page = int(page)
        search = request.GET.get("search","") #筛选条件
        print(search)
        page = int(page)
        if email:
            user = UserProfile.objects.get(Q(username=email)|Q(email=email))
        else:
            token = request.COOKIES.get("token")
            user = UserProfile.objects.get(token=token)

        page_nums = 9 #一页显示的数据数量
        user_data = user.get_data()
        if user.is_superuser:
            page_last = page * page_nums #本页的最后一条数据
            page_first = page_last - page_nums #本页第一条数据
            if search:
                print(88888)
                search_nums = UserProfile.objects.filter(Q(username__icontains=search)|Q(address__icontains=search)|Q(mobile__icontains=search)|Q(gender__icontains=search)|Q(email__icontains=search)).count()
                data = UserProfile.objects.filter(Q(username__icontains=search)|Q(address__icontains=search)|Q(mobile__icontains=search)|Q(gender__icontains=search)|Q(email__icontains=search))[page_first:page_last]
            else:
                data = UserProfile.objects.all()[page_first:page_last]


            users = []
            for i in data:
                i = i.get_data()
                users.append(i)
            # print (users)
            if not search:
                users.insert(0,user_data)
            if not search:
                nums = user.get_nums()  # 总的数据量
            else:
                nums = search_nums
                print(nums)
            yushu = nums % (page_nums+1)
            pnums = nums / (page_nums+1)  # 页数
            if yushu > 0:
                pnums += 1
            print(pnums)
            return ajax_ok_data(users,nums=pnums)
        data = user.get_data()
        print (type(user))
        # print(user_data)
        return ajax_ok_data(user_data)
    if request.method == "POST":
        print("success12")
        token = request.COOKIES.get("token")
        print(token)
        user = UserProfile.objects.get(token=token)
        print(token)
        user_info_update_form = UserInfoUpdate(request.POST,instance=user)
        if user_info_update_form.is_valid():
            user_info_update_form.save()
            print("success")
            return ajax_ok_data()
        else:
            data = user_info_update_form.errors
            print(data)
            return ajax_fail_data(data)

def upload_image(request):
    '''修改头像'''
    if request.method == "POST":
        uploadfrom = UpLoadImage(request.POST,request.FILES)
        token = request.COOKIES.get("token")
        user = UserProfile.objects.get(token=token)
        if uploadfrom.is_valid():
            image = uploadfrom.cleaned_data['image']
            user.image = image
            user.save()

            return ajax_ok_data()
        else:
            return ajax_fail_data()


def reset(request):
    """找回密码发送验证码"""
    if request.method == "POST":
        email = request.POST.get("email","")
        status = send_email_register(email,"forget")
        if status:
            return ajax_ok_data(message="邮件发送成功")
        else:
            return ajax_fail_data(message="邮件发送失败")

@CookieAuth
def upload_password(request):
    '''个人中心里修改密码'''
    if request.method== "GET":
        # froget_form = forgetForm(request.POST)

        email = request.GET.get("email", '')
        status = send_email_register(email, "forget")
        if status:
            return ajax_ok_data(message="邮件发送成功，请注意查收")
        else:
            return ajax_fail_data(message="邮件发送成功，请注意查收")

    if request.method == "POST":
        repwd_form = resetpwdForm(request.POST)
        if repwd_form.is_valid():
            email = request.POST.get("email", '')
            code = request.POST.get("code","")
            password1 = request.POST.get("password1",'')
            password2 = request.POST.get("password2",'')
            token = request.COOKIES.get("token")
            o = EmailVerifyRecord.objects.get(email=email,code=code,send_type="forget")
            if password1 == password2 and o:
                user = UserProfile.objects.get(token=token)
                user.password = make_password(password1)
                user.save()

                return ajax_ok_data(message="修改成功")
            else:
                return ajax_fail_data(message="兩次輸入的密碼不一致")
        data = repwd_form.errors
        return ajax_ok_data(data)

# @login_required(login_url="/users/login/")
def sendemil_code(request):
    '''更换邮箱时发送邮箱验证码'''
    if request.method == "POST":

        email = request.GET.get("email","")
        if UserProfile.objects.filter(email=email):

            return ajax_ok_data(message="此邮箱已经注册")
        status = send_email_register(email,"update_email")
        if status:
            return ajax_ok_data(message="邮件发送成功")
        else:
            return ajax_fail_data(message="邮件发送失败")

@CookieAuth
def update_email(request):
    '''修改个人邮箱'''
    if request.method=="POST":
        email = request.POST.get("email","")
        code = request.POST.get("code","")
        token = request.COOKIES.get("token",None)
        #获取验证记录
        recoreded = EmailVerifyRecord.objects.filter(code=code,send_type="update_email")
        if recoreded:
            user = UserProfile.objects.get(token=token)
            user.email = email
            user.save()
            return ajax_ok_data()
        else:
            return ajax_ok_data(message="验证码错误")


def page_not_find(request):
    response = render_to_response("404.html",{})
    response.status_code = 404
    return response

def page_error(request):
    response = render_to_response("500.html",{})
    response.status_code = 500
    return response