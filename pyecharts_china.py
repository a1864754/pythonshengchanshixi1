import time
from pyecharts import options as opts
from pyecharts.charts import Map
import pandas as pd
import get_save

name_dict = get_save.name_dict

# 1.获取省份id+name
# 1.1爬去数据
url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=1593844081982"
data_json = get_save.url_to_data(url)
data_province = data_json["data"]["areaTree"][2]["children"]
china_today_data = data_json["data"]["chinaTotal"]["total"]
china_today_time = data_json["data"]["lastUpdateTime"]

all_province = get_save.get_data(data_province, ["id", "name", "lastUpdateTime"])

# 处理中国各省数据
china_data = all_province
china_data.rename(columns=name_dict, inplace=True)
confirm_map_data_china = china_data[['名称', '累计确诊']].values.tolist()

# 处理简易信息
subtitle = "确诊：{0} 疑似：{1} 治愈：{2} 死亡：{3} 输入：{4}".format(china_today_data["confirm"],
                                                       china_today_data["suspect"],
                                                       china_today_data["heal"],
                                                       china_today_data["dead"],
                                                       china_today_data["input"])+" 更新时间：" + china_today_time
# 绘图
c = (
    Map()
        .add('中国累计确诊人数', confirm_map_data_china, 'china', is_map_symbol_show=False)
        .set_global_opts(title_opts=opts.TitleOpts(title="中国累计确诊人数图", subtitle=subtitle, pos_left='center'),
                         visualmap_opts=opts.VisualMapOpts(pieces=[
                             {"min": 60000, "color": "#d94e5d"},
                             {"min": 1000, "max": 59999, "color": "#e28b60"},
                             {"min": 500, "max": 999, "color": "#eac763"},
                             {"min": 100, "max": 499, "color": "#9db58f"},
                             {"max": 99, "color": "#60a3ba"}
                         ], is_piecewise=True),

                         legend_opts=opts.LegendOpts(orient='vertical', is_show=False)  # orient='vertical图例位置
                         )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))

)
c.render('中国累计确诊人数.html')
