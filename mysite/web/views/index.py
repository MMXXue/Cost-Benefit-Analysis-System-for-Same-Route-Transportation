from django.shortcuts import render
from urllib.parse import quote
from lxml import etree
import time
from django.http import HttpResponse
import requests
from django.shortcuts import redirect
from django.urls import reverse
from myadmin.models import User
import xml.etree.ElementTree as ET
import networkx as nx
import math
import requests
from queue import PriorityQueue
import csv
import random
from datetime import datetime
from django.db.models import Q



# Create your views here.
def index(request):
    '''系统前台首页'''
    return redirect(reverse('web_index'))

def webindex(request):
    '''系统前台首页'''
    return render(request, 'web/index.html')

# 查询火车票内容_接收请求数据
def search(request):
    request.encoding = 'utf-8'
    location1 = request.GET.get("start", None)
    location2 = request.GET.get("arrival", None)
    print(location1)
    print(location2)
    keywords1 = quote(location1)
    keywords2 = quote(location2)
    date = time.strftime("%Y-%m-%d", time.localtime())
    url = 'https://trains.ctrip.com/webapp/newtrain/list?'
    headers = {
        "User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    para = {
        'ticketType': '0',
        'dStation': keywords1,
        'aStation': keywords2,
        'dDate': date,
        'rDate': '',
        'trainsType': '',
        'hubCityName': '',
        'highSpeedOnly': '0',
    }
    page_data = requests.get(url=url, headers=headers, params=para).text
    tree = etree.HTML(page_data)
    num = tree.xpath('//section/div[@class="card-white list-item"]')
    train_sum = []
    train_train_from_time = []
    train_train_to_time = []
    train_from_station = []
    train_to_station = []
    train_train_haoshi = []
    train_train_checi = []
    train_train_price = []
    train_train_site_sum = []
    new_list = []
    for i in num:
        train = []
        train_from_time = i.xpath('.//div[@class="from"]/div[@class="time"]/text()')
        train_to_time = i.xpath('.//div[@class="to"]/div[@class="time"]/text()')
        del train_to_time[1]
        train.extend(train_from_time)
        train.extend(train_to_time)
        train_train_from_time.extend(train_from_time)
        train_train_to_time.extend(train_to_time)
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
        elif str1.startswith('T'):
            train_site_level = i.xpath('.//ul[@class ="surplus-list"]//text()')
            sum = ""
            for a in train_site_level:
                sum += a
            train_site_sum.append(sum)
        elif str1.startswith('L'):
            train_site_level = i.xpath('.//ul[@class ="surplus-list"]//text()')
            sum = ""
            for a in train_site_level:
                sum += a
            train_site_sum.append(sum)
        elif str1.startswith('A'):
            train_site_level = i.xpath('.//ul[@class ="surplus-list"]//text()')
            sum = ""
            for a in train_site_level:
                sum += a
            train_site_sum.append(sum)
        from_station = i.xpath('.//div[@class="from"]/div[2]/text()')
        to_station = i.xpath('.//div[@class="to"]/div[2]/text()')
        train_from_station.extend(from_station)
        train_to_station.extend(to_station)
        train_train_haoshi.extend(train_haoshi)
        train_train_checi.extend(train_checi)
        train_train_price.extend(train_price)
        train_train_site_sum.extend(train_site_sum)

        train.extend(from_station)
        train.extend(to_station)
        train.extend(train_haoshi)
        train.extend(train_checi)
        train.extend(train_price)
        train.extend(train_site_sum)
        train_sum.append(train)
        name_list = ['train_train_from_time',
                     'train_train_to_time',
                     'train_from_station',
                     'train_to_station',
                     'train_train_haoshi',
                     'train_train_checi',
                     'train_train_price',
                     'train_train_site_sum']
        final = dict(zip(name_list, train))
        print(final)
        new_list.append(final)
    print(new_list)
    count = str(7)
    xianzhi = str(1)
    return render(request, 'web/search_info.html', {'new_list':new_list,})

# 机动车寻径
def astar(request):
    request.encoding = 'utf-8'
    site1 = request.GET.get("web_start_location", None)
    site2 = request.GET.get("web_arrival_location", None)
    print(site1)
    print(site2)
    dom = ET.parse("./static/web/shanghai_interpreter.xml")
    root = dom.getroot()
    pos_location = {}  # 放进图里的所有节点 id 和经纬度数据
    loc = []  # 节点的经度和纬度
    Map = nx.Graph()
    EARTH_RADIUS = 6.371229 * 1e6
    length = []
    length2 = []
    length3 = []
    length4 = []
    start_jiedian_num = []
    end_jiedian_num = []
    juli_sum_dict = {}
    juli_sum_list = []
    search_range = 10
    car_add_time = 20

    for node in root.iter('node'):
        id = node.attrib['id']
        lat = float(node.attrib['lat'])
        lon = float(node.attrib['lon'])
        Map.add_node(id
                     , ID=id
                     , lat=lat
                     , lon=lon
                     )
        pos_location[id] = (lon, lat)
        loc.append([lon, lat])

    for way in root.findall('way'):
        list_node = []
        for node in way.iter('nd'):
            list_node.append(node)
        previous_node = list_node[0].attrib['ref']
        start_node_id = way[0].attrib['ref']
        end_node_id = list_node[-1].attrib['ref']

        for sub_node in way.iter('nd'):
            current_node_id = sub_node.attrib['ref']
            if (current_node_id != start_node_id):
                lon1 = pos_location[current_node_id][0]
                lat1 = pos_location[current_node_id][1]
                lon2 = pos_location[previous_node][0]
                lat2 = pos_location[previous_node][1]
                x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(((lat1 + lat2) / 2) * math.pi / 180) / 180)
                y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                weight = math.hypot(x, y)  # 返回米
                Map.add_edge(previous_node, current_node_id
                             , weight=weight
                             )
                previous_node = current_node_id

    url = 'https://restapi.amap.com/v3/geocode/geo?'

    param = {
        "address": site1,
        "key": "0a6cbf6d3afccaad7b50479fdb949b06"
    }
    num = requests.get(url=url, params=param).json()
    num_location = num['geocodes'][0]['location']
    oringin_list = num_location.split(',')
    start_lon = float(oringin_list[0])
    start_lat = float(oringin_list[1])

    param2 = {
        "address": site2,
        "key": "0a6cbf6d3afccaad7b50479fdb949b06"
    }
    num2 = requests.get(url=url, params=param2).json()
    num_location2 = num2['geocodes'][0]['location']
    oringin_list2 = num_location2.split(',')
    end_lon = float(oringin_list2[0])
    end_lat = float(oringin_list2[1])

    for i in pos_location:
        start_jiedian_num.append(i)
        tup_location = pos_location[i]
        node_lon = tup_location[0]
        node_lat = tup_location[1]
        x = float((start_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
            ((start_lat + node_lat) / 2) * math.pi / 180) / 180)
        y = float((start_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
        weight = math.hypot(x, y)  # 返回米
        length.append(weight)

    for i in range(len(length)):
        if length[i] <= search_range:
            length3.append(start_jiedian_num[i])
    print("起点", search_range, "米附近有", len(length3), "个节点")

    for i in pos_location:
        end_jiedian_num.append(i)
        tup_location = pos_location[i]
        node_lon = tup_location[0]
        node_lat = tup_location[1]
        x = float((end_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
            ((end_lat + node_lat) / 2) * math.pi / 180) / 180)
        y = float((end_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
        weight = math.hypot(x, y)  # 返回米
        length2.append(weight)

    for i in range(len(length2)):
        if length2[i] <= search_range:
            length4.append(end_jiedian_num[i])
    print("终点", search_range, "米附近有", len(length4), "个节点")

    if len(length3) == 0 or len(length4) == 0:
        print(search_range, '米内没有找到附近节点')
    else:
        for start_node in length3:
            for end_node in length4:
                frontier = PriorityQueue()
                frontier.put((0, start_node))
                came_from = {}
                cost_so_far = {}
                came_from[start_node] = None
                cost_so_far[start_node] = 0
                final = 'nice'
                message1 = 'error'

                while not frontier.empty():
                    current = frontier.get()
                    current = current[1]
                    if current == end_node:
                        break

                    for next in list(Map.neighbors(current)):
                        next = str(next)
                        current = str(current)

                        lon1 = pos_location[current][0]
                        lat1 = pos_location[current][1]
                        lon2 = pos_location[next][0]
                        lat2 = pos_location[next][1]
                        x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                            ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                        y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                        weight = math.hypot(x, y)  # 返回米

                        new_cost = cost_so_far[current] + weight
                        if next not in cost_so_far or new_cost < cost_so_far[next]:
                            cost_so_far[next] = new_cost

                            lon1 = pos_location[end_node][0]
                            lat1 = pos_location[end_node][1]
                            lon2 = pos_location[next][0]
                            lat2 = pos_location[next][1]
                            x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                                ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                            y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                            weight = math.hypot(x, y)  # 返回米

                            for_juli = weight
                            priority = new_cost + for_juli
                            frontier.put((priority, next))
                            came_from[next] = current
                    if frontier.empty():
                        final = message1

                if final == 'error':
                    pass
                else:
                    road = []
                    a_road = came_from
                    huisu_jiedian = a_road[end_node]

                    print('huisu_jiedian', huisu_jiedian)
                    print('end_node', end_node)

                    road.append(end_node)
                    road.append(huisu_jiedian)
                    for k in range(len(a_road)):
                        if huisu_jiedian != start_node:
                            huisu_jiedian = a_road[huisu_jiedian]
                            road.append(huisu_jiedian)
                        else:
                            break
                    road.reverse()
                    juli = cost_so_far[end_node]
                    juli_sum_list.append(juli)
                    juli_sum_dict[juli] = (start_node, end_node)

    while len(juli_sum_list) == 0:
        print(search_range, '米内没有找到路径，正在扩大节点附近搜索范围----')
        length = []
        length2 = []
        length3 = []
        length4 = []
        start_jiedian_num = []
        end_jiedian_num = []
        juli_sum_dict = {}
        juli_sum_list = []
        search_range = search_range + 10

        for i in pos_location:
            start_jiedian_num.append(i)
            tup_location = pos_location[i]
            node_lon = tup_location[0]
            node_lat = tup_location[1]
            x = float((start_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                ((start_lat + node_lat) / 2) * math.pi / 180) / 180)
            y = float((start_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            length.append(weight)

        for i in range(len(length)):
            if length[i] <= search_range:
                length3.append(start_jiedian_num[i])
        print("起点", search_range, "米附近有", len(length3), "个节点")

        for i in pos_location:
            end_jiedian_num.append(i)
            tup_location = pos_location[i]
            node_lon = tup_location[0]
            node_lat = tup_location[1]
            x = float((end_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                ((end_lat + node_lat) / 2) * math.pi / 180) / 180)
            y = float((end_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            length2.append(weight)

        for i in range(len(length2)):
            if length2[i] <= search_range:
                length4.append(end_jiedian_num[i])
        print("终点", search_range, "米附近有", len(length4), "个节点")

        for start_node in length3:
            for end_node in length4:
                frontier = PriorityQueue()
                frontier.put((0, start_node))
                came_from = {}
                cost_so_far = {}
                came_from[start_node] = None
                cost_so_far[start_node] = 0
                # index = 1
                message1 = 'error'
                final = 'nice'

                while not frontier.empty():
                    current = frontier.get()
                    current = current[1]

                    if current == end_node:
                        break

                    for next in list(Map.neighbors(current)):
                        next = str(next)
                        current = str(current)

                        lon1 = pos_location[current][0]
                        lat1 = pos_location[current][1]
                        lon2 = pos_location[next][0]
                        lat2 = pos_location[next][1]
                        x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                            ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                        y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                        weight = math.hypot(x, y)  # 返回米

                        new_cost = cost_so_far[current] + weight

                        if next not in cost_so_far or new_cost < cost_so_far[next]:
                            cost_so_far[next] = new_cost
                            lon1 = pos_location[end_node][0]
                            lat1 = pos_location[end_node][1]
                            lon2 = pos_location[next][0]
                            lat2 = pos_location[next][1]
                            x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                                ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                            y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                            weight = math.hypot(x, y)  # 返回米

                            for_juli = weight
                            priority = new_cost + for_juli
                            frontier.put((priority, next))
                            came_from[next] = current
                    if frontier.empty():
                        final = message1
                if final == 'error':
                    pass
                else:
                    road = []
                    a_road = came_from
                    huisu_jiedian = a_road[end_node]
                    road.append(end_node)
                    road.append(huisu_jiedian)
                    for k in range(len(a_road)):
                        if huisu_jiedian != start_node:
                            huisu_jiedian = a_road[huisu_jiedian]
                            road.append(huisu_jiedian)
                        else:
                            break
                    road.reverse()
                    juli = cost_so_far[end_node]
                    juli_sum_list.append(juli)
                    juli_sum_dict[juli] = (start_node, end_node)

    else:
        print("在", search_range, "米内已找到路径----")
        juli_min = min(juli_sum_list)
        print("在", search_range, "米内已找到最短路径----")
        print("正在地理信息格式化----")
        for i in juli_sum_dict:
            if i == juli_min:
                node_result = juli_sum_dict[i]
                final_start_node = node_result[0]
                final_end_node = node_result[1]

                # 人性化输出
                url = 'https://restapi.amap.com/v3/geocode/regeo?parameters'
                road_list = []
                frontier = PriorityQueue()
                frontier.put((0, final_start_node))
                came_from = {}
                cost_so_far = {}
                came_from[final_start_node] = None
                cost_so_far[final_start_node] = 0

                while not frontier.empty():
                    current = frontier.get()
                    current = current[1]
                    if current == final_end_node:
                        break

                    for next in list(Map.neighbors(current)):
                        next = str(next)
                        current = str(current)

                        lon1 = pos_location[current][0]
                        lat1 = pos_location[current][1]
                        lon2 = pos_location[next][0]
                        lat2 = pos_location[next][1]
                        x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                            ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                        y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                        weight = math.hypot(x, y)  # 返回米
                        new_cost = cost_so_far[current] + weight
                        if next not in cost_so_far or new_cost < cost_so_far[next]:
                            cost_so_far[next] = new_cost

                            lon1 = pos_location[final_end_node][0]
                            lat1 = pos_location[final_end_node][1]
                            lon2 = pos_location[next][0]
                            lat2 = pos_location[next][1]
                            x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                                ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                            y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                            weight = math.hypot(x, y)
                            for_juli = weight
                            priority = new_cost + for_juli
                            frontier.put((priority, next))
                            came_from[next] = current

                reroad = []
                a_road = came_from

                huisu_jiedian = a_road[final_end_node]

                print('最终的回溯节点 huisu_jiedian', huisu_jiedian)
                print('最终的目标节点 final_end_node', final_end_node)

                reroad.append(final_end_node)
                reroad.append(huisu_jiedian)
                for k in range(len(a_road)):
                    if huisu_jiedian != final_start_node:
                        huisu_jiedian = a_road[huisu_jiedian]
                        reroad.append(huisu_jiedian)
                    else:
                        break
                reroad.reverse()

                for i in reroad:
                    site = pos_location[i]
                    str1 = str(site)
                    location = str1[1:-1]
                    param = {
                        'location': location,
                        "key": '0a6cbf6d3afccaad7b50479fdb949b06',
                        'extensions': 'base',
                        'roadlevel': '1',
                    }
                    num = requests.get(url=url, params=param).json()
                    num_location = num['regeocode']['addressComponent']['streetNumber']['street']
                    road_list.append(num_location)
                print('地理格式化完成----')

                road_list.append(0)
                re_road_list = []
                for i in range(len(road_list) - 1):
                    if road_list[i] != road_list[i + 1]:
                        re_road_list.append(road_list[i])
                #print('re_road_list:',re_road_list)

                new_tidai_list = []
                for u in range(len(re_road_list)):
                    if re_road_list[u] != []:
                        new_tidai_list.append(re_road_list[u])

                masum = []
                for i in range(1000000):
                    masum.append(new_tidai_list[0])
                    num = -1
                    list3 = []
                    if len(new_tidai_list) == 0:
                        break
                    for k in range(1000000):
                        if new_tidai_list[num] == new_tidai_list[0]:
                            break
                        else:
                            list3.insert(0, new_tidai_list[num])
                            num = num - 1
                    if len(list3) == 0:
                        break
                    else:
                        new_tidai_list = list3
                print("路径规划为：",masum)
                print(str(site1),"到",str(site2),"之间最优路径的距离为",str(juli_min),"米")
                #print("节点ID",str(final_start_node),"和",str(final_end_node),"之间最短路径的距离：",str(juli_min))
                time = float(juli_min)/50000*60
                time = car_add_time+int(time)
                print("该路径规划方案[纯汽车]需要耗费", str(time), "分钟")
                car_dic = {
                    're_road_list':masum,
                    'juli_min':str(juli_min),
                    'time':str(time),
                }
                return render(request, 'web/astar.html', {'car_dic':car_dic})


def findway(request):
    request.encoding = 'utf-8'
    site1 = request.GET.get("web_start_location", None)
    site2 = request.GET.get("web_arrival_location", None)
    tool = request.GET.get("web_tool", None)
    print(site1)
    print(site2)
    if tool == '地铁':
        pos_location = {}  # 放进图里的所有节点 id 和经纬度数据
        loc = []  # 节点的经度和纬度
        Map = nx.Graph()
        EARTH_RADIUS = 6.371229 * 1e6
        length = []
        length2 = []
        length3 = []
        length4 = []
        start_jiedian_num = []
        end_jiedian_num = []
        juli_sum_dict = {}
        juli_sum_list = []
        car_add_time = 20
        gonggongjiaotong_add_time = 15
        search_range = 100
        add_range = 50
        re_bus_line_name_sum = []

        # 加入地铁线路
        url = 'http://map.amap.com/service/subway?_1639285523673&srhdata=3100_drw_shanghai.json'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43"
        }
        data = requests.get(url=url, headers=headers).json()
        for k in data['l']:  # 每条线
            site_name_list = []  # 站名列表
            site_zuobiao_list = []
            subway_line_name = k['kn']
            for i in k['st']:
                stop_name = i['n']
                stop_zuobiao = i['sl']
                site_name_list.append(stop_name)
                line_name_sum = subway_line_name + str('(') + stop_name + str(')')
                site_zuobiao_list.append(stop_zuobiao)
                Map.add_node(stop_zuobiao, line_name_sum=line_name_sum)
                pos_location[stop_zuobiao] = line_name_sum
            for z in range(len(site_zuobiao_list) - 1):
                subway_zuobiao_first = site_zuobiao_list[z].split(',', 1)
                subway_zuobiao_later = site_zuobiao_list[z + 1].split(',', 1)
                lon1 = float(subway_zuobiao_first[0])
                lat1 = float(subway_zuobiao_first[1])
                lon2 = float(subway_zuobiao_later[0])
                lat2 = float(subway_zuobiao_later[1])
                x = float(
                    (lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(((lat1 + lat2) / 2) * math.pi / 180) / 180)
                y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                weight = math.hypot(x, y)  # 返回米
                Map.add_edge(site_zuobiao_list[z], site_zuobiao_list[z + 1], weight=weight)
        # print(pos_location)

        url = 'https://restapi.amap.com/v3/geocode/geo?'
        param = {
            "address": site1,
            "key": "0a6cbf6d3afccaad7b50479fdb949b06",
            "city": "上海",
        }
        num = requests.get(url=url, params=param).json()
        num_location = num['geocodes'][0]['location']
        oringin_list = num_location.split(',')
        start_lon = float(oringin_list[0])
        start_lat = float(oringin_list[1])

        param2 = {
            "address": site2,
            "key": "0a6cbf6d3afccaad7b50479fdb949b06",
            "city": "上海",
        }
        num2 = requests.get(url=url, params=param2).json()
        num_location2 = num2['geocodes'][0]['location']
        oringin_list2 = num_location2.split(',')
        end_lon = float(oringin_list2[0])
        end_lat = float(oringin_list2[1])

        for i in pos_location:
            # pos_location[i]     地铁5号线
            start_jiedian_num.append(i)
            tup_location = i.split(',')
            node_lon = float(tup_location[0])
            node_lat = float(tup_location[1])
            x = float((start_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                ((start_lat + node_lat) / 2) * math.pi / 180) / 180)
            y = float((start_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            length.append(weight)

        for i in range(len(length)):
            if length[i] <= search_range:
                length3.append(start_jiedian_num[i])
        print("起点", search_range, "米附近有", len(length3), "个节点")

        for i in pos_location:
            end_jiedian_num.append(i)
            tup_location = i.split(',')
            node_lon = float(tup_location[0])
            node_lat = float(tup_location[1])
            x = float((end_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                ((end_lat + node_lat) / 2) * math.pi / 180) / 180)
            y = float((end_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            length2.append(weight)

        for i in range(len(length2)):
            if length2[i] <= search_range:
                length4.append(end_jiedian_num[i])
        print("终点", search_range, "米附近有", len(length4), "个节点")

        if len(length3) == 0 or len(length4) == 0:
            print(search_range, '米内没有找到附近节点')
        else:
            for start_node in length3:
                for end_node in length4:
                    try:
                        path = nx.astar_path(Map, start_node, end_node)
                        juli = nx.astar_path_length(Map, start_node, end_node)
                        juli_sum_list.append(juli)
                        juli_sum_dict[juli] = (start_node, end_node)
                    except:
                        pass

        while len(juli_sum_list) == 0:
            print(search_range, '米内没有找到路径，正在扩大节点附近搜索范围----')
            length = []
            length2 = []
            length3 = []
            length4 = []
            start_jiedian_num = []
            end_jiedian_num = []
            juli_sum_dict = {}
            juli_sum_list = []
            search_range = search_range + add_range

            for i in pos_location:
                # pos_location[i]     地铁5号线
                start_jiedian_num.append(i)
                tup_location = i.split(',')
                node_lon = float(tup_location[0])
                node_lat = float(tup_location[1])
                x = float((start_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                    ((start_lat + node_lat) / 2) * math.pi / 180) / 180)
                y = float((start_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
                weight = math.hypot(x, y)  # 返回米
                length.append(weight)

            for i in range(len(length)):
                if length[i] <= search_range:
                    length3.append(start_jiedian_num[i])
            print("起点", search_range, "米附近有", len(length3), "个节点")

            for i in pos_location:
                end_jiedian_num.append(i)
                tup_location = i.split(',')
                node_lon = float(tup_location[0])
                node_lat = float(tup_location[1])
                x = float((end_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                    ((end_lat + node_lat) / 2) * math.pi / 180) / 180)
                y = float((end_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
                weight = math.hypot(x, y)  # 返回米
                length2.append(weight)

            for i in range(len(length2)):
                if length2[i] <= search_range:
                    length4.append(end_jiedian_num[i])
            print("终点", search_range, "米附近有", len(length4), "个节点")

            for start_node in length3:
                for end_node in length4:
                    try:
                        path = nx.astar_path(Map, start_node, end_node)
                        juli = nx.astar_path_length(Map, start_node, end_node)
                        juli_sum_list.append(juli)
                        juli_sum_dict[juli] = (start_node, end_node)
                    except:
                        pass

        else:
            print("在", search_range, "米内已找到路径----")
            juli_min = min(juli_sum_list)
            print("在", search_range, "米内已找到最短路径----")
            print("正在地理信息格式化----")
            for i in juli_sum_dict:
                if i == juli_min:
                    road_list = []
                    node_result = juli_sum_dict[i]
                    final_start_node = node_result[0]
                    final_end_node = node_result[1]

                    reroad = nx.astar_path(Map, final_start_node, final_end_node)
                    subway_road_name = []
                    for i in reroad:
                        subway_road_name.append(pos_location[i])

                    print("纯地铁路径规划为：", subway_road_name)
                    print(str(site1), "到", str(site2), "之间[纯地铁]最优路径的距离为", str(juli_min), "米")
                    time = float(juli_min) / 50000 * 60
                    time = gonggongjiaotong_add_time + int(time)
                    print("该路径规划方案[纯地铁]需要耗费", str(time), "分钟")
                    subway_dic = {
                        're_road_list': subway_road_name,
                        'juli_min': str(juli_min),
                        'time': str(time),
                    }
                    return render(request, 'web/subway.html', {'subway_dic': subway_dic})
    elif tool == '公交车':
        pos_location = {}  # 放进图里的所有节点 id 和经纬度数据
        loc = []  # 节点的经度和纬度
        Map = nx.Graph()
        EARTH_RADIUS = 6.371229 * 1e6
        length = []
        length2 = []
        length3 = []
        length4 = []
        start_jiedian_num = []
        end_jiedian_num = []
        juli_sum_dict = {}
        juli_sum_list = []
        car_add_time = 20
        gonggongjiaotong_add_time = 15
        search_range = 100
        add_range = 10
        re_bus_line_name_sum = []

        total = len(open('./static/web/上海市公交车基本信息.csv', encoding='utf-8').readlines())

        # 加入公交车线路
        with open('./static/web/上海市公交车基本信息.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for i, rows in enumerate(reader):
                if i != 0:
                    node = []
                    route_name = rows[0]
                    row = rows[1]
                    location = row.split('],[')
                    sum = len(location) - 1
                    for num in range(len(location)):
                        if num == 0:
                            one = location[num]
                            true_one = one[1:]
                            node.append(true_one)
                        elif num == sum:
                            last = location[num]
                            true_last = last[:-1]
                            node.append(true_last)
                        else:
                            node.append(location[num])
                    for z in range(len(node)):
                        Map.add_node(node[z], Route_name=route_name)
                        pos_location[node[z]] = route_name

                    node_last = node[-1]
                    node.append(node_last)
                    for q in range(len(node) - 1):
                        bus_zuobiao_first = node[q].split(',', 1)
                        bus_zuobiao_later = node[q + 1].split(',', 1)
                        lon1 = float(bus_zuobiao_first[0])
                        lat1 = float(bus_zuobiao_first[1])
                        lon2 = float(bus_zuobiao_later[0])
                        lat2 = float(bus_zuobiao_later[1])
                        x = float(
                            (lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                                ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                        y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                        weight = math.hypot(x, y)  # 返回米
                        Map.add_edge(node[q], node[q + 1], weight=weight)

            # print(pos_location)

        url = 'https://restapi.amap.com/v3/geocode/geo?'
        param = {
            "address": site1,
            "key": "0a6cbf6d3afccaad7b50479fdb949b06",
            "city": "上海",
        }
        num = requests.get(url=url, params=param).json()
        num_location = num['geocodes'][0]['location']
        oringin_list = num_location.split(',')
        start_lon = float(oringin_list[0])
        start_lat = float(oringin_list[1])

        param2 = {
            "address": site2,
            "key": "0a6cbf6d3afccaad7b50479fdb949b06",
            "city": "上海",
        }
        num2 = requests.get(url=url, params=param2).json()
        num_location2 = num2['geocodes'][0]['location']
        oringin_list2 = num_location2.split(',')
        end_lon = float(oringin_list2[0])
        end_lat = float(oringin_list2[1])

        for i in pos_location:
            # pos_location[i]     地铁5号线
            start_jiedian_num.append(i)
            tup_location = i.split(',')
            node_lon = float(tup_location[0])
            node_lat = float(tup_location[1])
            x = float((start_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                ((start_lat + node_lat) / 2) * math.pi / 180) / 180)
            y = float((start_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            length.append(weight)

        for i in range(len(length)):
            if length[i] <= search_range:
                length3.append(start_jiedian_num[i])
        print("起点", search_range, "米附近有", len(length3), "个节点")

        for i in pos_location:
            end_jiedian_num.append(i)
            tup_location = i.split(',')
            node_lon = float(tup_location[0])
            node_lat = float(tup_location[1])
            x = float((end_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                ((end_lat + node_lat) / 2) * math.pi / 180) / 180)
            y = float((end_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            length2.append(weight)

        for i in range(len(length2)):
            if length2[i] <= search_range:
                length4.append(end_jiedian_num[i])
        print("终点", search_range, "米附近有", len(length4), "个节点")

        if len(length3) == 0 or len(length4) == 0:
            print(search_range, '米内没有找到附近节点')
        else:
            for start_node in length3:
                for end_node in length4:
                    try:
                        path = nx.astar_path(Map, start_node, end_node)
                        juli = nx.astar_path_length(Map, start_node, end_node)
                        juli_sum_list.append(juli)
                        juli_sum_dict[juli] = (start_node, end_node)
                    except:
                        pass

        while len(juli_sum_list) == 0:
            print(search_range, '米内没有找到路径，正在扩大节点附近搜索范围----')
            length = []
            length2 = []
            length3 = []
            length4 = []
            start_jiedian_num = []
            end_jiedian_num = []
            juli_sum_dict = {}
            juli_sum_list = []
            search_range = search_range + add_range

            for i in pos_location:
                # pos_location[i]     地铁5号线
                start_jiedian_num.append(i)
                tup_location = i.split(',')
                node_lon = float(tup_location[0])
                node_lat = float(tup_location[1])
                x = float((start_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                    ((start_lat + node_lat) / 2) * math.pi / 180) / 180)
                y = float((start_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
                weight = math.hypot(x, y)  # 返回米
                length.append(weight)

            for i in range(len(length)):
                if length[i] <= search_range:
                    length3.append(start_jiedian_num[i])
            print("起点", search_range, "米附近有", len(length3), "个节点")

            for i in pos_location:
                end_jiedian_num.append(i)
                tup_location = i.split(',')
                node_lon = float(tup_location[0])
                node_lat = float(tup_location[1])
                x = float((end_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                    ((end_lat + node_lat) / 2) * math.pi / 180) / 180)
                y = float((end_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
                weight = math.hypot(x, y)  # 返回米
                length2.append(weight)

            for i in range(len(length2)):
                if length2[i] <= search_range:
                    length4.append(end_jiedian_num[i])
            print("终点", search_range, "米附近有", len(length4), "个节点")

            for start_node in length3:
                for end_node in length4:
                    try:
                        path = nx.astar_path(Map, start_node, end_node)
                        juli = nx.astar_path_length(Map, start_node, end_node)
                        juli_sum_list.append(juli)
                        juli_sum_dict[juli] = (start_node, end_node)
                    except:
                        pass

        else:
            print("在", search_range, "米内已找到路径----")
            juli_min = min(juli_sum_list)
            print("在", search_range, "米内已找到最短路径----")
            print("正在地理信息格式化----")
            for i in juli_sum_dict:
                if i == juli_min:
                    road_list = []
                    node_result = juli_sum_dict[i]
                    final_start_node = node_result[0]
                    final_end_node = node_result[1]

                    reroad = nx.astar_path(Map, final_start_node, final_end_node)
                    subway_road_name = []
                    for k in reroad:
                        subway_road_name.append(pos_location[k])

                    bus_name_same_num = 1
                    final_bus_road_guihua = []
                    bus_list = []

                    for q in range(10000000000000000):
                        # 存放后续list的
                        list2 = []
                        for i in range(1, len(subway_road_name)):
                            if subway_road_name[0] != subway_road_name[-i]:
                                list2.insert(0, subway_road_name[-i])
                            else:
                                bus_list.append(subway_road_name[0])
                                break
                        subway_road_name = []
                        for w in list2:
                            subway_road_name.append(w)
                        # print('-----------------!!!!')
                        # print('re_bus_line_name_sum:', re_bus_line_name_sum)
                        # print('list2:', list2)
                        if len(list2) == 0:
                            break

                    print("纯公交车路径规划为：", bus_list)
                    print(str(site1), "到", str(site2), "之间[纯公交车]最优路径的距离为", str(juli_min), "米")
                    time = float(juli_min) / 50000 * 60
                    time = gonggongjiaotong_add_time + int(time)
                    print("该路径规划方案[纯公交车]需要耗费", str(time), "分钟")
                    bus_dic = {
                        're_road_list': bus_list,
                        'juli_min': str(juli_min),
                        'time': str(time),
                    }
                    return render(request, 'web/bus.html', {'bus_dic': bus_dic})
    elif tool == '汽车':
        dom = ET.parse("./static/web/shanghai_interpreter.xml")
        root = dom.getroot()
        pos_location = {}  # 放进图里的所有节点 id 和经纬度数据
        loc = []  # 节点的经度和纬度
        Map = nx.Graph()
        EARTH_RADIUS = 6.371229 * 1e6
        length = []
        length2 = []
        length3 = []
        length4 = []
        start_jiedian_num = []
        end_jiedian_num = []
        juli_sum_dict = {}
        juli_sum_list = []
        search_range = 10
        car_add_time = 20

        for node in root.iter('node'):
            id = node.attrib['id']
            lat = float(node.attrib['lat'])
            lon = float(node.attrib['lon'])
            Map.add_node(id
                         , ID=id
                         , lat=lat
                         , lon=lon
                         )
            pos_location[id] = (lon, lat)
            loc.append([lon, lat])

        for way in root.findall('way'):
            list_node = []
            for node in way.iter('nd'):
                list_node.append(node)
            previous_node = list_node[0].attrib['ref']
            start_node_id = way[0].attrib['ref']
            end_node_id = list_node[-1].attrib['ref']

            for sub_node in way.iter('nd'):
                current_node_id = sub_node.attrib['ref']
                if (current_node_id != start_node_id):
                    lon1 = pos_location[current_node_id][0]
                    lat1 = pos_location[current_node_id][1]
                    lon2 = pos_location[previous_node][0]
                    lat2 = pos_location[previous_node][1]
                    x = float(
                        (lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(((lat1 + lat2) / 2) * math.pi / 180) / 180)
                    y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                    weight = math.hypot(x, y)  # 返回米
                    Map.add_edge(previous_node, current_node_id
                                 , weight=weight
                                 )
                    previous_node = current_node_id

        url = 'https://restapi.amap.com/v3/geocode/geo?'

        param = {
            "address": site1,
            "key": "0a6cbf6d3afccaad7b50479fdb949b06",
            "city": "上海",
        }
        num = requests.get(url=url, params=param).json()
        num_location = num['geocodes'][0]['location']
        oringin_list = num_location.split(',')
        start_lon = float(oringin_list[0])
        start_lat = float(oringin_list[1])

        param2 = {
            "address": site2,
            "key": "0a6cbf6d3afccaad7b50479fdb949b06",
            "city": "上海",
        }
        num2 = requests.get(url=url, params=param2).json()
        num_location2 = num2['geocodes'][0]['location']
        oringin_list2 = num_location2.split(',')
        end_lon = float(oringin_list2[0])
        end_lat = float(oringin_list2[1])

        for i in pos_location:
            start_jiedian_num.append(i)
            tup_location = pos_location[i]
            node_lon = tup_location[0]
            node_lat = tup_location[1]
            x = float((start_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                ((start_lat + node_lat) / 2) * math.pi / 180) / 180)
            y = float((start_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            length.append(weight)

        for i in range(len(length)):
            if length[i] <= search_range:
                length3.append(start_jiedian_num[i])
        print("起点", search_range, "米附近有", len(length3), "个节点")

        for i in pos_location:
            end_jiedian_num.append(i)
            tup_location = pos_location[i]
            node_lon = tup_location[0]
            node_lat = tup_location[1]
            x = float((end_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                ((end_lat + node_lat) / 2) * math.pi / 180) / 180)
            y = float((end_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            length2.append(weight)

        for i in range(len(length2)):
            if length2[i] <= search_range:
                length4.append(end_jiedian_num[i])
        print("终点", search_range, "米附近有", len(length4), "个节点")

        if len(length3) == 0 or len(length4) == 0:
            print(search_range, '米内没有找到附近节点')
        else:
            for start_node in length3:
                for end_node in length4:
                    frontier = PriorityQueue()
                    frontier.put((0, start_node))
                    came_from = {}
                    cost_so_far = {}
                    came_from[start_node] = None
                    cost_so_far[start_node] = 0
                    final = 'nice'
                    message1 = 'error'

                    while not frontier.empty():
                        current = frontier.get()
                        current = current[1]
                        if current == end_node:
                            break

                        for next in list(Map.neighbors(current)):
                            next = str(next)
                            current = str(current)

                            lon1 = pos_location[current][0]
                            lat1 = pos_location[current][1]
                            lon2 = pos_location[next][0]
                            lat2 = pos_location[next][1]
                            x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                                ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                            y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                            weight = math.hypot(x, y)  # 返回米

                            new_cost = cost_so_far[current] + weight
                            if next not in cost_so_far or new_cost < cost_so_far[next]:
                                cost_so_far[next] = new_cost

                                lon1 = pos_location[end_node][0]
                                lat1 = pos_location[end_node][1]
                                lon2 = pos_location[next][0]
                                lat2 = pos_location[next][1]
                                x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                                    ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                                y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                                weight = math.hypot(x, y)  # 返回米

                                for_juli = weight
                                priority = new_cost + for_juli
                                frontier.put((priority, next))
                                came_from[next] = current
                        if frontier.empty():
                            final = message1

                    if final == 'error':
                        pass
                    else:
                        road = []
                        a_road = came_from
                        huisu_jiedian = a_road[end_node]

                        print('huisu_jiedian', huisu_jiedian)
                        print('end_node', end_node)

                        road.append(end_node)
                        road.append(huisu_jiedian)
                        for k in range(len(a_road)):
                            if huisu_jiedian != start_node:
                                huisu_jiedian = a_road[huisu_jiedian]
                                road.append(huisu_jiedian)
                            else:
                                break
                        road.reverse()
                        juli = cost_so_far[end_node]
                        juli_sum_list.append(juli)
                        juli_sum_dict[juli] = (start_node, end_node)

        while len(juli_sum_list) == 0:
            print(search_range, '米内没有找到路径，正在扩大节点附近搜索范围----')
            length = []
            length2 = []
            length3 = []
            length4 = []
            start_jiedian_num = []
            end_jiedian_num = []
            juli_sum_dict = {}
            juli_sum_list = []
            search_range = search_range + 10

            for i in pos_location:
                start_jiedian_num.append(i)
                tup_location = pos_location[i]
                node_lon = tup_location[0]
                node_lat = tup_location[1]
                x = float((start_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                    ((start_lat + node_lat) / 2) * math.pi / 180) / 180)
                y = float((start_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
                weight = math.hypot(x, y)  # 返回米
                length.append(weight)

            for i in range(len(length)):
                if length[i] <= search_range:
                    length3.append(start_jiedian_num[i])
            print("起点", search_range, "米附近有", len(length3), "个节点")

            for i in pos_location:
                end_jiedian_num.append(i)
                tup_location = pos_location[i]
                node_lon = tup_location[0]
                node_lat = tup_location[1]
                x = float((end_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                    ((end_lat + node_lat) / 2) * math.pi / 180) / 180)
                y = float((end_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
                weight = math.hypot(x, y)  # 返回米
                length2.append(weight)

            for i in range(len(length2)):
                if length2[i] <= search_range:
                    length4.append(end_jiedian_num[i])
            print("终点", search_range, "米附近有", len(length4), "个节点")

            for start_node in length3:
                for end_node in length4:
                    frontier = PriorityQueue()
                    frontier.put((0, start_node))
                    came_from = {}
                    cost_so_far = {}
                    came_from[start_node] = None
                    cost_so_far[start_node] = 0
                    # index = 1
                    message1 = 'error'
                    final = 'nice'

                    while not frontier.empty():
                        current = frontier.get()
                        current = current[1]

                        if current == end_node:
                            break

                        for next in list(Map.neighbors(current)):
                            next = str(next)
                            current = str(current)

                            lon1 = pos_location[current][0]
                            lat1 = pos_location[current][1]
                            lon2 = pos_location[next][0]
                            lat2 = pos_location[next][1]
                            x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                                ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                            y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                            weight = math.hypot(x, y)  # 返回米

                            new_cost = cost_so_far[current] + weight

                            if next not in cost_so_far or new_cost < cost_so_far[next]:
                                cost_so_far[next] = new_cost
                                lon1 = pos_location[end_node][0]
                                lat1 = pos_location[end_node][1]
                                lon2 = pos_location[next][0]
                                lat2 = pos_location[next][1]
                                x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                                    ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                                y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                                weight = math.hypot(x, y)  # 返回米

                                for_juli = weight
                                priority = new_cost + for_juli
                                frontier.put((priority, next))
                                came_from[next] = current
                        if frontier.empty():
                            final = message1
                    if final == 'error':
                        pass
                    else:
                        road = []
                        a_road = came_from
                        huisu_jiedian = a_road[end_node]
                        road.append(end_node)
                        road.append(huisu_jiedian)
                        for k in range(len(a_road)):
                            if huisu_jiedian != start_node:
                                huisu_jiedian = a_road[huisu_jiedian]
                                road.append(huisu_jiedian)
                            else:
                                break
                        road.reverse()
                        juli = cost_so_far[end_node]
                        juli_sum_list.append(juli)
                        juli_sum_dict[juli] = (start_node, end_node)

        else:
            print("在", search_range, "米内已找到路径----")
            juli_min = min(juli_sum_list)
            print("在", search_range, "米内已找到最短路径----")
            print("正在地理信息格式化----")
            for i in juli_sum_dict:
                if i == juli_min:
                    node_result = juli_sum_dict[i]
                    final_start_node = node_result[0]
                    final_end_node = node_result[1]

                    # 人性化输出
                    url = 'https://restapi.amap.com/v3/geocode/regeo?parameters'
                    road_list = []
                    frontier = PriorityQueue()
                    frontier.put((0, final_start_node))
                    came_from = {}
                    cost_so_far = {}
                    came_from[final_start_node] = None
                    cost_so_far[final_start_node] = 0

                    while not frontier.empty():
                        current = frontier.get()
                        current = current[1]
                        if current == final_end_node:
                            break

                        for next in list(Map.neighbors(current)):
                            next = str(next)
                            current = str(current)

                            lon1 = pos_location[current][0]
                            lat1 = pos_location[current][1]
                            lon2 = pos_location[next][0]
                            lat2 = pos_location[next][1]
                            x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                                ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                            y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                            weight = math.hypot(x, y)  # 返回米
                            new_cost = cost_so_far[current] + weight
                            if next not in cost_so_far or new_cost < cost_so_far[next]:
                                cost_so_far[next] = new_cost

                                lon1 = pos_location[final_end_node][0]
                                lat1 = pos_location[final_end_node][1]
                                lon2 = pos_location[next][0]
                                lat2 = pos_location[next][1]
                                x = float((lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(
                                    ((lat1 + lat2) / 2) * math.pi / 180) / 180)
                                y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                                weight = math.hypot(x, y)
                                for_juli = weight
                                priority = new_cost + for_juli
                                frontier.put((priority, next))
                                came_from[next] = current

                    reroad = []
                    a_road = came_from

                    huisu_jiedian = a_road[final_end_node]

                    print('最终的回溯节点 huisu_jiedian', huisu_jiedian)
                    print('最终的目标节点 final_end_node', final_end_node)

                    reroad.append(final_end_node)
                    reroad.append(huisu_jiedian)
                    for k in range(len(a_road)):
                        if huisu_jiedian != final_start_node:
                            huisu_jiedian = a_road[huisu_jiedian]
                            reroad.append(huisu_jiedian)
                        else:
                            break
                    reroad.reverse()

                    for i in reroad:
                        site = pos_location[i]
                        str1 = str(site)
                        location = str1[1:-1]
                        param = {
                            'location': location,
                            "key": '0a6cbf6d3afccaad7b50479fdb949b06',
                            'extensions': 'base',
                            'roadlevel': '1',
                        }
                        num = requests.get(url=url, params=param).json()
                        num_location = num['regeocode']['addressComponent']['streetNumber']['street']
                        road_list.append(num_location)
                    print('地理格式化完成----')

                    road_list.append(0)
                    re_road_list = []
                    for i in range(len(road_list) - 1):
                        if road_list[i] != road_list[i + 1]:
                            re_road_list.append(road_list[i])
                    # print('re_road_list:',re_road_list)

                    new_tidai_list = []
                    for u in range(len(re_road_list)):
                        if re_road_list[u] != []:
                            new_tidai_list.append(re_road_list[u])

                    masum = []
                    for i in range(1000000):
                        masum.append(new_tidai_list[0])
                        num = -1
                        list3 = []
                        if len(new_tidai_list) == 0:
                            break
                        for k in range(1000000):
                            if new_tidai_list[num] == new_tidai_list[0]:
                                break
                            else:
                                list3.insert(0, new_tidai_list[num])
                                num = num - 1
                        if len(list3) == 0:
                            break
                        else:
                            new_tidai_list = list3
                    print("纯汽车路径规划为：", masum)
                    print(str(site1), "到", str(site2), "之间[纯汽车]最优路径的距离为", str(juli_min), "米")
                    # print("节点ID",str(final_start_node),"和",str(final_end_node),"之间最短路径的距离：",str(juli_min))
                    time = float(juli_min) / 50000 * 60
                    time = car_add_time + int(time)
                    print("该路径规划方案[纯汽车]需要耗费", str(time), "分钟")
                    car_dic = {
                        're_road_list': masum,
                        'juli_min': str(juli_min),
                        'time': str(time),
                    }
                    return render(request, 'web/astar.html', {'car_dic': car_dic})
    else:
        context = {"info": "交通工具名称输入错误，请重新输入！"}
        return render(request, 'web/info.html',context)


#地铁寻径
def subway_astar(request):
    request.encoding = 'utf-8'
    site1 = request.GET.get("web_start_location", None)
    site2 = request.GET.get("web_arrival_location", None)
    print(site1)
    print(site2)
    pos_location = {}  # 放进图里的所有节点 id 和经纬度数据
    loc = []   # 节点的经度和纬度
    Map = nx.Graph()
    EARTH_RADIUS = 6.371229 * 1e6
    length = []
    length2 = []
    length3 = []
    length4 = []
    start_jiedian_num = []
    end_jiedian_num = []
    juli_sum_dict ={}
    juli_sum_list = []
    car_add_time = 20
    gonggongjiaotong_add_time = 15
    search_range = 100
    add_range = 50
    re_bus_line_name_sum = []

    #加入地铁线路
    url = 'http://map.amap.com/service/subway?_1639285523673&srhdata=3100_drw_shanghai.json'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43"
    }
    data = requests.get(url=url, headers=headers).json()
    for k in data['l']:  # 每条线
        site_name_list = []  # 站名列表
        site_zuobiao_list = []
        subway_line_name = k['kn']
        for i in k['st']:
            stop_name = i['n']
            stop_zuobiao = i['sl']
            site_name_list.append(stop_name)
            line_name_sum = subway_line_name + str('(') + stop_name + str(')')
            site_zuobiao_list.append(stop_zuobiao)
            Map.add_node(stop_zuobiao, line_name_sum=line_name_sum)
            pos_location[stop_zuobiao] = line_name_sum
        for z in range(len(site_zuobiao_list) - 1):
            subway_zuobiao_first = site_zuobiao_list[z].split(',', 1)
            subway_zuobiao_later = site_zuobiao_list[z + 1].split(',', 1)
            lon1 = float(subway_zuobiao_first[0])
            lat1 = float(subway_zuobiao_first[1])
            lon2 = float(subway_zuobiao_later[0])
            lat2 = float(subway_zuobiao_later[1])
            x = float(
                (lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(((lat1 + lat2) / 2) * math.pi / 180) / 180)
            y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            Map.add_edge(site_zuobiao_list[z], site_zuobiao_list[z + 1], weight=weight)
    #print(pos_location)

    url = 'https://restapi.amap.com/v3/geocode/geo?'
    param = {
        "address": site1,
        "key": "0a6cbf6d3afccaad7b50479fdb949b06",
        "city": "上海",
    }
    num = requests.get(url=url, params=param).json()
    num_location = num['geocodes'][0]['location']
    oringin_list = num_location.split(',')
    start_lon = float(oringin_list[0])
    start_lat = float(oringin_list[1])

    param2 = {
        "address": site2,
        "key": "0a6cbf6d3afccaad7b50479fdb949b06",
        "city": "上海",
    }
    num2 = requests.get(url=url, params=param2).json()
    num_location2 = num2['geocodes'][0]['location']
    oringin_list2 = num_location2.split(',')
    end_lon = float(oringin_list2[0])
    end_lat = float(oringin_list2[1])

    for i in pos_location:
        #pos_location[i]     地铁5号线
        start_jiedian_num.append(i)
        tup_location = i.split(',')
        node_lon = float(tup_location[0])
        node_lat = float(tup_location[1])
        x = float((start_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(((start_lat + node_lat) / 2) * math.pi / 180) / 180)
        y = float((start_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
        weight = math.hypot(x, y)  # 返回米
        length.append(weight)

    for i in range(len(length)):
        if length[i] <= search_range:
            length3.append(start_jiedian_num[i])
    print("起点", search_range, "米附近有", len(length3), "个节点")

    for i in pos_location:
        end_jiedian_num.append(i)
        tup_location = i.split(',')
        node_lon = float(tup_location[0])
        node_lat = float(tup_location[1])
        x = float((end_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
            ((end_lat + node_lat) / 2) * math.pi / 180) / 180)
        y = float((end_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
        weight = math.hypot(x, y)  # 返回米
        length2.append(weight)

    for i in range(len(length2)):
        if length2[i] <= search_range:
            length4.append(end_jiedian_num[i])
    print("终点", search_range, "米附近有", len(length4), "个节点")

    if len(length3) == 0 or len(length4) == 0:
        print(search_range, '米内没有找到附近节点')
    else:
        for start_node in length3:
            for end_node in length4:
                try:
                    path = nx.astar_path(Map,start_node,end_node)
                    juli = nx.astar_path_length(Map,start_node,end_node)
                    juli_sum_list.append(juli)
                    juli_sum_dict[juli] = (start_node, end_node)
                except:
                    pass

    while len(juli_sum_list) == 0:
        print(search_range, '米内没有找到路径，正在扩大节点附近搜索范围----')
        length = []
        length2 = []
        length3 = []
        length4 = []
        start_jiedian_num = []
        end_jiedian_num = []
        juli_sum_dict = {}
        juli_sum_list = []
        search_range = search_range + add_range

        for i in pos_location:
            # pos_location[i]     地铁5号线
            start_jiedian_num.append(i)
            tup_location = i.split(',')
            node_lon = float(tup_location[0])
            node_lat = float(tup_location[1])
            x = float((start_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                ((start_lat + node_lat) / 2) * math.pi / 180) / 180)
            y = float((start_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            length.append(weight)

        for i in range(len(length)):
            if length[i] <= search_range:
                length3.append(start_jiedian_num[i])
        print("起点", search_range, "米附近有", len(length3), "个节点")

        for i in pos_location:
            end_jiedian_num.append(i)
            tup_location = i.split(',')
            node_lon = float(tup_location[0])
            node_lat = float(tup_location[1])
            x = float((end_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                ((end_lat + node_lat) / 2) * math.pi / 180) / 180)
            y = float((end_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            length2.append(weight)

        for i in range(len(length2)):
            if length2[i] <= search_range:
                length4.append(end_jiedian_num[i])
        print("终点", search_range, "米附近有", len(length4), "个节点")

        for start_node in length3:
            for end_node in length4:
                try:
                    path = nx.astar_path(Map,start_node,end_node)
                    juli = nx.astar_path_length(Map,start_node,end_node)
                    juli_sum_list.append(juli)
                    juli_sum_dict[juli] = (start_node, end_node)
                except:
                    pass

    else:
        print("在", search_range, "米内已找到路径----")
        juli_min = min(juli_sum_list)
        print("在", search_range, "米内已找到最短路径----")
        print("正在地理信息格式化----")
        for i in juli_sum_dict:
            if i == juli_min:
                road_list =[]
                node_result = juli_sum_dict[i]
                final_start_node = node_result[0]
                final_end_node = node_result[1]

                reroad = nx.astar_path(Map,final_start_node,final_end_node)
                subway_road_name = []
                for i in reroad:
                    subway_road_name.append(pos_location[i])

                print("纯地铁路径规划为：", subway_road_name)
                print(str(site1), "到", str(site2), "之间[纯地铁]最优路径的距离为", str(juli_min), "米")
                time = float(juli_min) / 50000 * 60
                time = gonggongjiaotong_add_time + int(time)
                print("该路径规划方案[纯地铁]需要耗费", str(time), "分钟")
                subway_dic = {
                    're_road_list': subway_road_name,
                    'juli_min': str(juli_min),
                    'time': str(time),
                }
                return render(request, 'web/subway.html', {'subway_dic': subway_dic})

#公交车寻径
def bus_astar(request):
    request.encoding = 'utf-8'
    site1 = request.GET.get("web_start_location", None)
    site2 = request.GET.get("web_arrival_location", None)
    print(site1)
    print(site2)
    pos_location = {}  # 放进图里的所有节点 id 和经纬度数据
    loc = []  # 节点的经度和纬度
    Map = nx.Graph()
    EARTH_RADIUS = 6.371229 * 1e6
    length = []
    length2 = []
    length3 = []
    length4 = []
    start_jiedian_num = []
    end_jiedian_num = []
    juli_sum_dict = {}
    juli_sum_list = []
    car_add_time = 20
    gonggongjiaotong_add_time = 15
    search_range = 100
    add_range = 10
    re_bus_line_name_sum = []

    total = len(open('./static/web/上海市公交车基本信息.csv', encoding='utf-8').readlines())

    # 加入公交车线路
    with open('./static/web/上海市公交车基本信息.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for i, rows in enumerate(reader):
            if i != 0:
                node = []
                route_name = rows[0]
                row = rows[1]
                location = row.split('],[')
                sum = len(location) - 1
                for num in range(len(location)):
                    if num == 0:
                        one = location[num]
                        true_one = one[1:]
                        node.append(true_one)
                    elif num == sum:
                        last = location[num]
                        true_last = last[:-1]
                        node.append(true_last)
                    else:
                        node.append(location[num])
                for z in range(len(node)):
                    Map.add_node(node[z], Route_name=route_name)
                    pos_location[node[z]] = route_name

                node_last = node[-1]
                node.append(node_last)
                for q in range(len(node) - 1):
                    bus_zuobiao_first = node[q].split(',', 1)
                    bus_zuobiao_later = node[q + 1].split(',', 1)
                    lon1 = float(bus_zuobiao_first[0])
                    lat1 = float(bus_zuobiao_first[1])
                    lon2 = float(bus_zuobiao_later[0])
                    lat2 = float(bus_zuobiao_later[1])
                    x = float(
                        (lon2 - lon1) * math.pi * EARTH_RADIUS * math.cos(((lat1 + lat2) / 2) * math.pi / 180) / 180)
                    y = float((lat1 - lat2) * math.pi * EARTH_RADIUS / 180)
                    weight = math.hypot(x, y)  # 返回米
                    Map.add_edge(node[q], node[q + 1], weight=weight)

        # print(pos_location)

    url = 'https://restapi.amap.com/v3/geocode/geo?'
    param = {
        "address": site1,
        "key": "0a6cbf6d3afccaad7b50479fdb949b06",
        "city": "上海",
    }
    num = requests.get(url=url, params=param).json()
    num_location = num['geocodes'][0]['location']
    oringin_list = num_location.split(',')
    start_lon = float(oringin_list[0])
    start_lat = float(oringin_list[1])

    param2 = {
        "address": site2,
        "key": "0a6cbf6d3afccaad7b50479fdb949b06",
        "city": "上海",
    }
    num2 = requests.get(url=url, params=param2).json()
    num_location2 = num2['geocodes'][0]['location']
    oringin_list2 = num_location2.split(',')
    end_lon = float(oringin_list2[0])
    end_lat = float(oringin_list2[1])

    for i in pos_location:
        # pos_location[i]     地铁5号线
        start_jiedian_num.append(i)
        tup_location = i.split(',')
        node_lon = float(tup_location[0])
        node_lat = float(tup_location[1])
        x = float((start_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
            ((start_lat + node_lat) / 2) * math.pi / 180) / 180)
        y = float((start_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
        weight = math.hypot(x, y)  # 返回米
        length.append(weight)

    for i in range(len(length)):
        if length[i] <= search_range:
            length3.append(start_jiedian_num[i])
    print("起点", search_range, "米附近有", len(length3), "个节点")

    for i in pos_location:
        end_jiedian_num.append(i)
        tup_location = i.split(',')
        node_lon = float(tup_location[0])
        node_lat = float(tup_location[1])
        x = float((end_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
            ((end_lat + node_lat) / 2) * math.pi / 180) / 180)
        y = float((end_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
        weight = math.hypot(x, y)  # 返回米
        length2.append(weight)

    for i in range(len(length2)):
        if length2[i] <= search_range:
            length4.append(end_jiedian_num[i])
    print("终点", search_range, "米附近有", len(length4), "个节点")

    if len(length3) == 0 or len(length4) == 0:
        print(search_range, '米内没有找到附近节点')
    else:
        for start_node in length3:
            for end_node in length4:
                try:
                    path = nx.astar_path(Map, start_node, end_node)
                    juli = nx.astar_path_length(Map, start_node, end_node)
                    juli_sum_list.append(juli)
                    juli_sum_dict[juli] = (start_node, end_node)
                except:
                    pass

    while len(juli_sum_list) == 0:
        print(search_range, '米内没有找到路径，正在扩大节点附近搜索范围----')
        length = []
        length2 = []
        length3 = []
        length4 = []
        start_jiedian_num = []
        end_jiedian_num = []
        juli_sum_dict = {}
        juli_sum_list = []
        search_range = search_range + add_range

        for i in pos_location:
            # pos_location[i]     地铁5号线
            start_jiedian_num.append(i)
            tup_location = i.split(',')
            node_lon = float(tup_location[0])
            node_lat = float(tup_location[1])
            x = float((start_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                ((start_lat + node_lat) / 2) * math.pi / 180) / 180)
            y = float((start_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            length.append(weight)

        for i in range(len(length)):
            if length[i] <= search_range:
                length3.append(start_jiedian_num[i])
        print("起点", search_range, "米附近有", len(length3), "个节点")

        for i in pos_location:
            end_jiedian_num.append(i)
            tup_location = i.split(',')
            node_lon = float(tup_location[0])
            node_lat = float(tup_location[1])
            x = float((end_lon - node_lon) * math.pi * EARTH_RADIUS * math.cos(
                ((end_lat + node_lat) / 2) * math.pi / 180) / 180)
            y = float((end_lat - node_lat) * math.pi * EARTH_RADIUS / 180)
            weight = math.hypot(x, y)  # 返回米
            length2.append(weight)

        for i in range(len(length2)):
            if length2[i] <= search_range:
                length4.append(end_jiedian_num[i])
        print("终点", search_range, "米附近有", len(length4), "个节点")

        for start_node in length3:
            for end_node in length4:
                try:
                    path = nx.astar_path(Map, start_node, end_node)
                    juli = nx.astar_path_length(Map, start_node, end_node)
                    juli_sum_list.append(juli)
                    juli_sum_dict[juli] = (start_node, end_node)
                except:
                    pass

    else:
        print("在", search_range, "米内已找到路径----")
        juli_min = min(juli_sum_list)
        print("在", search_range, "米内已找到最短路径----")
        print("正在地理信息格式化----")
        for i in juli_sum_dict:
            if i == juli_min:
                road_list = []
                node_result = juli_sum_dict[i]
                final_start_node = node_result[0]
                final_end_node = node_result[1]

                reroad = nx.astar_path(Map, final_start_node, final_end_node)
                subway_road_name = []
                for k in reroad:
                    subway_road_name.append(pos_location[k])

                bus_name_same_num = 1
                final_bus_road_guihua = []
                bus_list = []

                for q in range(10000000000000000):
                    # 存放后续list的
                    list2 = []
                    for i in range(1, len(subway_road_name)):
                        if subway_road_name[0] != subway_road_name[-i]:
                            list2.insert(0, subway_road_name[-i])
                        else:
                            bus_list.append(subway_road_name[0])
                            break
                    subway_road_name = []
                    for w in list2:
                        subway_road_name.append(w)
                    # print('-----------------!!!!')
                    # print('re_bus_line_name_sum:', re_bus_line_name_sum)
                    # print('list2:', list2)
                    if len(list2) == 0:
                        break

                print("纯公交车路径规划为：", bus_list)
                print(str(site1), "到", str(site2), "之间[纯公交车]最优路径的距离为", str(juli_min), "米")
                time = float(juli_min) / 50000 * 60
                time = gonggongjiaotong_add_time + int(time)
                print("该路径规划方案[纯公交车]需要耗费", str(time), "分钟")
                bus_dic = {
                    're_road_list': bus_list,
                    'juli_min': str(juli_min),
                    'time': str(time),
                }
                return render(request, 'web/bus.html', {'bus_dic': bus_dic})

def login(request):
    '''加载登录页面'''
    return render(request,'web/login.html')

def dologin(request):
    '''执行登录操作'''
    try:
        # 执行验证码的校验
        if request.POST['code'] != request.session['verifycode']:
            return redirect(reverse('web_login')+"?errinfo=2")

        # 根据登录账号获取用户信息
        user = User.objects.get(username=request.POST['username'])
        # 校验当前用户状态是否正常或管理员
        if user.status == 1 or user.status == 6 :
            # 获取密码并md5
            import hashlib
            md5 = hashlib.md5()
            n = user.password_salt
            s = request.POST['pass'] + str(n)
            md5.update(s.encode('utf-8'))
            # 校验密码是否正确
            if user.password_hash == md5.hexdigest():
                # 将当前登录成功用户信息以webuser这个key放入到session中
                request.session['webuser'] = user.toDict()
                return redirect(reverse('web_index'))
            else:
                return redirect(reverse('web_login') + "?errinfo=5")
        else:
            return redirect(reverse('web_login') + "?errinfo=4")
    except Exception as err:
        print(err)
        return redirect(reverse('web_login') + "?errinfo=3")

def logout(request):
    '''执行推出操作'''
    del request.session['webuser']
    return redirect(reverse('web_login'))

def verify(request):
    '''验证码'''
    import random
    from PIL import Image, ImageDraw, ImageFont
    # 定义变量，用于画面的背景色、宽、高
    # bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242, 164, 247)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    # str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/arial.ttf', 21)
    # font = ImageFont.load_default().font
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

#账号注册
def add(request):
    return render(request, "web/register.html")

def insert(request):
    try:
        ob = User()
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        # 获取密码并md5
        import hashlib
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password'] + str(n)
        md5.update(s.encode('utf-8'))
        ob.password_hash = md5.hexdigest()
        ob.password_salt = n
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"新账号已经注册成功，请返回登录界面"}
    except Exception as err:
        print(err)
        context = {'info': "账号注册失败"}
    return render(request, "web/info.html",context)





