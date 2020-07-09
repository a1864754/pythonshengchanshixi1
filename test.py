import time
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Map
import pandas as pd
import get_save




# 获取省份id+name
url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=1593844081982"
data_json = get_save.url_to_data(url)
data_province = data_json["data"]["areaTree"][2]["children"]
# print(data_province)
info = pd.DataFrame(data_province)[["id", "name"]]
# print(info)
province_dict = {}
for i in data_province:
    province_dict[i["id"]] = i["name"]
# print(province_dict)

china_today = data_json["data"]["chinaTotal"]["total"]
china_today_data = data_json["data"]["chinaTotal"]["total"]
china_today_time = data_json["data"]["lastUpdateTime"]
print(china_today_time)


