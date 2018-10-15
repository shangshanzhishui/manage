# _*_ encoding:utf-8 _*_
from django.shortcuts import render,HttpResponse
import json
from datetime import datetime
from users.models import UserProfile
from django.db.models import Q

def ajax_data(response_code, data=None, error=None, nums=None, message=None):
    """if the response_code is true, then the data is set in 'data',
    if the response_code is false, then the data is set in 'error'
    """
    r = dict(response='ok', data=data, error='', nums='', message='')
    if response_code is True or response_code.lower() in ('ok', 'yes', 'true'):
        r['response'] = 'ok'
    else:
        r['response'] = 'fail'
    if data is not None:
        r['data'] = data
    if error:
        r['error'] = error
    if nums:
        r['nums'] = nums
    if message:
        r['message'] = message
    return r

def ajax_ok_data(data='', nums=None, message=None):
    data = ajax_data('ok', data=data, nums=nums, message=message)
    data = json.dumps(data,cls=DateEncoder)
    r = HttpResponse(data)
    r['Content-Type'] = 'application/json'
    return r

def ajax_fail_data(data='', nums=None, message=None):
    data = ajax_data('fail', data=data, nums=nums, message=message)
    data = json.dumps(data,cls=DateEncoder)
    r = HttpResponse(data)
    r['Content-Type'] = 'application/json'
    return r

def ajax_ok(request,data='', nums=None, message=None):#增加设置cookie
    data = ajax_data('ok', data=data, nums=nums, message=message)
    data = json.dumps(data,cls=DateEncoder)
    r = HttpResponse(data)
    email = request.POST.get("email","")
    print(email)
    token = UserProfile.objects.get(Q(username=email)|Q(email=email)).token
    r.set_cookie("token",token)
    print(token)
    r['Content-Type'] = 'application/json'
    return r

class DateEncoder(json.JSONEncoder ):
  def default(self, obj):
    if isinstance(obj, datetime):
      return obj.__str__()
    return json.JSONEncoder.default(self, obj)