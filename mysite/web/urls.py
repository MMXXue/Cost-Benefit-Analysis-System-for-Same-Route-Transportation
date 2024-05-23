#前端管理子路由
from django.contrib import admin
from django.urls import path, include
from web.views import index

urlpatterns = [
    path('', index.index, name="index"),
    path('web/search', index.search, name="web_search"),
    path('web/astar', index.subway_astar, name="web_subway_atar"),
    path('web/bus', index.bus_astar, name="web_bus_atar"),
    path('web/subway', index.astar, name="web_astar"),
    path('web/findway', index.findway, name="web_findway"),

    #path('web/search_form', index.search_form, name="search_form"),

    #前端登录退出的路由
    path('login', index.login, name="web_login"),#加载登录
    path('dologin', index.dologin, name="web_dologin"),#执行登录
    path('logout', index.logout, name="web_logout"),#退出登录
    path('verify', index.verify, name="web_verify"), #验证码

    #账号注册
    path('add', index.add, name="web_user_add"),  # 加载添加表单
    path('insert', index.insert, name="web_user_insert"),  # 执行信息添加

    #为url路由添加请求前缀,凡是带此前缀的地址必须登录后才可访问
    path("web/", include([
        path('', index.webindex, name="web_index"),
    ]))

]
