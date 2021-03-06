# _*_ encoding:utf-8 _*_
"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from users.views import active,reset,post_reset
from hello.settings import MEDIA_ROOT#,STATIC_ROOT
from django.views.static import serve

urlpatterns = [
    url(r'^$',TemplateView.as_view(template_name="index.html")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/',include("users.urls",namespace="user")),#users app
    url(r'^active/(?P<active_code>.*)/$', active),#激活账号
    url(r'^reset/(?P<reset_code>.*)/$', reset),

    # url(r'^login$', index, name="post_reset"),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
