#移动端管理子路由
from django.contrib import admin
from django.urls import path, include
from mobile.views import index,member

urlpatterns = [
    path('', index.index, name='mobile_index'),

    #会员注册
    path('register', index.register, name='mobile_register'),

    #执行登录操作
    path('doregister', index.doRegister, name='mobile_doregister'),#执行
    path('verify', index.verify, name="mobile_verify"),  # 验证码

    #寻路
    path('mobile/findway', index.findway, name="mobile_findway"),

    #火车票
    path('mobile/research', index.research, name="mobile_research"),

    #用户中心
    path('mobile/info', index.member, name="mobile_member"),
    path('mobile/info/logout', index.logout, name='mobile_member_logout'),#退出
]