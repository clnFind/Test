# -*- coding: utf-8 -*-
from pprint import pprint
import re
import urllib
import requests


def get_weather(city_name):
    city_name = urllib.request.quote("天气 {0}".format(city_name))
    print(city_name)
    url = "http://cn.bing.com/search?q={0}".format(city_name)
    r = requests.get(url=url).text
    pprint(r)

    # 对数据进行过滤
    # 选出天气部分
    # re.S 多行匹配
    weather_arr = re.findall(r"<li class=\"b_ans b_top b_topborder\">(.*?)</li>", r, re.S)

    pprint(weather_arr)

    if len(weather_arr) <= 0:
        return None

    weather = weather_arr[0]
    ret = dict({
        "today": {},
        "weather": []
    })
    # 天气描述
    w_desc = re.findall(r"<div class=\"w2_daysky\">(.*?)</div>", weather, re.S)

    if len(w_desc) > 0:
        ret["today"]["w_desc"] = w_desc[0]

    # 实时温度
    w_temp = re.findall(r"<div class=\"w2_temperature\"><span>(\d+?)</span>", weather, re.S)

    if len(w_temp) > 0:
        ret["today"]["w_temp"] = w_temp[0]

    # 风力
    wind = re.findall(r"<div class=\"w2_dline2\">(.*?)</div>", weather, re.S)

    if len(wind) > 0:
        ret["today"]["wind"] = wind[0]

    # 湿度
    humidity = re.findall(r"<div class=\"w2_dline2\">(\d+?)</div>", weather, re.S)

    print('湿度；', humidity)

    if len(humidity) > 0:
        ret["today"]["humidity"] = humidity[0]

    # PM2.5
    pm25 = re.findall(r"<div class=\"w2_dline2 w2_pm25\">(\d+?)<span", weather, re.S)

    if len(pm25) > 0:
        ret["today"]["pm25"] = pm25[0]

    # 最近5天的温度范围、天气描述、风力(今天、明天、后天、....)
    last_arr = re.findall(r"<div class=\"w2_ftext\">(.*?)</div>", weather, re.S)

    pprint(last_arr)

    if len(last_arr) == 15:
        ret["weather"].append({"w0": last_arr[0:3]})
        ret["weather"].append({"w1": last_arr[3:6]})
        ret["weather"].append({"w2": last_arr[6:9]})
        ret["weather"].append({"w3": last_arr[9:12]})
        ret["weather"].append({"w4": last_arr[12:]})
    return ret


if __name__ == "__main__":
    a = get_weather("杭州")
    pprint(a)
