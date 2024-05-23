from django.http import HttpResponse
from django.shortcuts import render
from myadmin.models import Train
from django.core.paginator import Paginator
from django.db.models import Q


def index(request, pIndex=1):
    trainlist = Train.objects.all()
    mywhere = []
    #搜索
    kw = request.GET.get("keyword", None)
    if kw:
        trainlist = trainlist.filter(Q(start_location__contains=kw)|Q(arrival_location__contains=kw))
        mywhere.append('keyword=' + kw)#维持住转页
    #分页
    pIndex = int(pIndex)
    page = Paginator(trainlist,7)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    plist = page.page_range
    content = {"trainlist":list2, 'plist':plist, 'pIndex':pIndex, 'maxpages':maxpages}
    return render(request,'myadmin/train/index.html',content)#加载模板，并存放数据