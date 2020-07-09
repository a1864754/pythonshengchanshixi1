# 爬取信息
# 城市ID：https://static.ws.126.net/163/f2e/news/virus_province/static/shaanxi.json
# 西安历史：https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=
import pandas as pd
import get_save
from xpinyin import Pinyin
import time

pin = Pinyin()
# 省份id+name
url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=1593844081982"
data_json = get_save.url_to_data(url)
data_province = data_json["data"]["areaTree"][2]["children"]
# print(data_province)
info = pd.DataFrame(data_province)[["id", "name"]]
# print(info)
province_dict_en = {}
for i in data_province:
    if i["name"] == '陕西':
        province_dict_en[610000] = "shaanxi"
    elif i["name"] == '重庆':
        pass
    else:
        city_pinyin = pin.get_pinyin(i["name"], "")
        province_dict_en[i["id"]] = city_pinyin

province_dict = {}
for i in data_province:
    province_dict[i["id"]] = i["name"]
print(province_dict_en)
print(province_dict)

# 获取城市id+name
for i in province_dict_en:
    print("开始爬取:", i, province_dict[i], province_dict_en[i])
    url = "https://static.ws.126.net/163/f2e/news/virus_province/static/"+province_dict_en[i]+".json"
    # time.sleep(3)
    data = get_save.url_to_data(url)
    print(data)
# data = data["features"][""]
# print(data)
