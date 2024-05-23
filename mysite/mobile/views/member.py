from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
def index(request):
    '''个人中心首页'''
    return render(request, 'mobile/member.html')

def detail(request):
    '''个人中心首页'''
    return render(request, 'mobile/member_detail.html')

def logout(request):
    '''账号退出'''
    return render(request, 'mobile/register.html')