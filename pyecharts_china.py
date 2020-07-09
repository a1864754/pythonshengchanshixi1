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

# 1.2省份及id所在的字典
data_province = data_json["data"]["areaTree"][2]["children"]
info = pd.DataFrame(data_province)[["id", "name"]]

# 1.3转换格式
province_dict = {}
for i in data_province:
    province_dict[i["id"]] = i["name"]

# 获取中国疫情简易信息
# 获取最后更新时间
china_today_data = data_json["data"]["chinaTotal"]["total"]
china_today_time = data_json["data"]["lastUpdateTime"]

# 获取各省份url
# 爬去每个省信息
count = 1
for i in province_dict:
    # print(i)
    try:
        url = "https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=" + i
        data = get_save.url_to_data(url)
        province_data = get_save.get_data(data["data"]["list"], ["date"])
        province_data["name"] = province_dict[i]

        if i == "420000":
            all_province = province_data
            # print(province_dict[i], "成功", province_data.shape)
        else:
            all_province = pd.concat([all_province, province_data])
            # print(province_dict[i], "成功", province_data.shape)
    except:
        print(province_dict[i], "失败", province_data.shape)
# 处理中国各省数据
china_data = all_province
china_data.rename(columns=name_dict, inplace=True)
eg_name_dict = pd.read_csv('./covid_data/county_china_english.csv', encoding='gbk')
china_data['eg_name'] = china_data['名称'].replace(eg_name_dict['中文'].values, eg_name_dict['英文'].values)
heatmap_data_china = china_data[['eg_name', '累计确诊']].values.tolist()

# 处理简易信息
text = "确诊：{0} 疑似：{1} 治愈：{2} 死亡：{3} 输入：{4}".format(china_today_data["confirm"],
                                                   china_today_data["suspect"],
                                                   china_today_data["heal"],
                                                   china_today_data["dead"],
                                                   china_today_data["input"]), "更新时间：" + china_today_time
# 绘图
c = (
    Map()
        .add('中国累计确诊人数', heatmap_data_china, 'china', is_map_symbol_show=False)
        .set_global_opts(title_opts=opts.TitleOpts(title="中国累计确诊人数图", subtitle=text, pos_left='30%'),
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
