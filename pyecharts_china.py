import time
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Map
import pandas as pd
import save_get

# 获取省份id+name
url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=1593844081982"
data_json = save_get.re_data(url)
data_province = data_json["data"]["areaTree"][2]["children"]
# print(data_province)
info = pd.DataFrame(data_province)[["id", "name"]]
# print(info)
province_dict = {}
for i in data_province:
    province_dict[i["id"]] = i["name"]
# print(province_dict)

china_today_data = data_json["data"]["chinaTotal"]["total"]
china_today_time = data_json["data"]["lastUpdateTime"]
print(china_today_data)
print(china_today_data["confirm"])

# 获取各省份url
count = 1
for i in province_dict:
    # print(i)
    try:
        url = "https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=" + i
        data = save_get.re_data(url)
        province_data = save_get.get_data(data["data"]["list"], ["date"])
        province_data["name"] = province_dict[i]

        if i == "420000":
            all_province = province_data
            # print(province_dict[i], "成功", province_data.shape)
        else:
            all_province = pd.concat([all_province, province_data])
            # print(province_dict[i], "成功", province_data.shape)
    except:
        pass
# all_province.to_csv('./covid_data/all_province.csv',encoding='utf-8-sig')

china_data = all_province
name_dict = {'date': '日期', 'id': "编号", 'name': '名称', 'lastUpdateTime': '更新时间', 'total_confirm': '累计确诊',
             'total_suspect': '累计疑似',
             'total_heal': '累计治愈', 'total_dead': '累计死亡', 'total_severe': '累计重症', 'total_input': '累计输入',
             'total_newConfirm': '累计新增确诊', 'total_newDead': '累计新增死亡', 'total_newHeal': '累计新增治愈',
             'today_confirm': '当日新增确诊',
             'today_suspect': '当日新增疑似', 'today_heal': '当日新增治愈', 'today_dead': '当日新增死亡', 'today_severe': '当日新增重症',
             'today_storeConfirm': '当日现存确诊', 'today_input': '当日新增输入'}
china_data.rename(columns=name_dict, inplace=True)
eg_name_dict = pd.read_csv('./covid_data/county_china_english.csv', encoding='gbk')
china_data['eg_name'] = china_data['名称'].replace(eg_name_dict['中文'].values, eg_name_dict['英文'].values)
heatmap_data_china = china_data[['eg_name', '累计确诊']].values.tolist()

text = "确诊：{0} 疑似：{1} 治愈：{2} 死亡：{3} 输入：{4}".format(china_today_data["confirm"],
                                                   china_today_data["suspect"],
                                                   china_today_data["heal"],
                                                   china_today_data["dead"],
                                                   china_today_data["input"]), "更新时间：" + china_today_time
c = (
    Map()
        .add('中国累计确诊人数', heatmap_data_china, 'china', is_map_symbol_show=False)
        .set_global_opts(title_opts=opts.TitleOpQts(title="中国累计确诊人数图", pos_left='30%'),
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
