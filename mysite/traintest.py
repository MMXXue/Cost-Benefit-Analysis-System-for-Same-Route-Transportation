import pandas as pd
from django.shortcuts import render
import requests
from lxml import etree


def index(request):
        url = 'https://trains.ctrip.com/webapp/newtrain/list?ticketType=0&dStation=%25E4%25B8%258A%25E6%25B5%25B7&aStation=%25E6%25AD%25A6%25E6%25B1%2589&dDate=2021-12-06&rDate=&trainsType=&hubCityName=&highSpeedOnly=0'
        headers = {
            "User-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        page_data = requests.get(url=url,headers=headers).text
        tree = etree.HTML(page_data)
        num = tree.xpath('//section/div[@class="card-white list-item"]')
        trainlist_sum = []
        for i in num:
            trainlist = []
            train_from_time = i.xpath('.//div[@class="from"]/div[@class="time"]/text()')
            train_to_time = i.xpath('.//div[@class="to"]/div[@class="time"]/text()')
            del train_to_time[1]
            trainlist.extend(train_from_time)
            trainlist.extend(train_to_time)
            train_haoshi = i.xpath('.//div[@class="haoshi"]/text()')
            train_checi = i.xpath('.//div[@class="checi"]/text()')
            train_price = i.xpath('.//div[@class="price"]/text()')
            #train_site_level = i.xpath('.//ul[@class ="surplus-list"]//text()')
            train_site_sum = []

            train_checi1 = i.xpath('.//div[@class="checi"]/text()')
            str1 = ''.join(train_checi1)
            if str1.startswith('D'):
                train_site_level = i.xpath('.//ul[@class ="surplus-list"]//text()')
                sum = ""
                for a in train_site_level:
                    sum += a
                train_site_sum.append(sum)
            elif str1.startswith('G'):
                train_site_level = i.xpath('.//ul[@class ="surplus-list"]//text()')
                sum = ""
                for a in train_site_level:
                    sum += a
                train_site_sum.append(sum)
            elif str1.startswith('Z'):
                train_site_level = i.xpath('.//ul[@class ="surplus-list"]//text()')
                sum = ""
                for a in train_site_level:
                    sum += a
                train_site_sum.append(sum)
            elif str1.startswith('K'):
                train_site_level = i.xpath('.//ul[@class ="surplus-list"]//text()')
                sum = ""
                for a in train_site_level:
                    sum += a
                train_site_sum.append(sum)
            from_station = i.xpath('.//div[@class="from"]/div[2]/text()')
            to_station = i.xpath('.//div[@class="to"]/div[2]/text()')
            trainlist.extend(from_station)
            trainlist.extend(to_station)
            trainlist.extend(train_haoshi)
            trainlist.extend(train_checi)
            trainlist.extend(train_price)
            trainlist.extend(train_site_sum)
            trainlist_sum.append(trainlist)
        return render(request, 'myadmin/train/index.html', {'trainlist_sum': trainlist_sum})