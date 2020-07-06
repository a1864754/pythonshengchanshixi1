mport time

import requests
import chardet
import json
import pandas as pd

# 爬取信息
url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=318749413808"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
req = requests.get(url, headers=headers)
req.encoding = chardet.detect(req.content)["encoding"]
# print(req.status_code)
# print(req.text)
# 转换为json格式
data_json = json.loads(req.text)
# print("格式: ", type(data_json))
# print("字典键: ", data_json.keys())
# print("信息头: ", data_json["data"]["areaTree"][2]["total"])
# print("信息: ", data_json["data"]["areaTree"][2]["today"])
# print(data_json["data"]["areaTree"][2]["name"])

data_provience = data_json["data"]["areaTree"][2]["children"]
infos = []

infos_today = []
for i in data_provience:
    # name,id,lastupdata=i["name"], i["id"], i["lastUpdateTime"]
    info = pd.DataFrame(data_provience)[["id", "name", "lastUpdateTime"]]
    # print(i["today"])
    # print(i["total"]["confirm"],i["total"]["heal"],i["total"]["dead"])
    confirm, heal, dead = i["total"]["confirm"], i["total"]["heal"], i["total"]["dead"]
    # 信息添加到列表
    infos.append(i["total"])
    infos_today.append(i["today"])
# 列表转DataFrame

total_data2 = pd.DataFrame(infos)
today_data = pd.DataFrame(infos_today)
# 修改total_data2中的列名
total_data2.columns = ["total_" + i for i in total_data2.columns]
# total_data2.head()
# today_data.head()
# 保存为CSV文件

total_data2.to_csv("1184.csv", index=None, encoding="utf-8-sig")
today_data.to_csv("1183.csv", index=None, encoding="utf-8-sig")

provience_data = pd.concat([info, total_data2, today_data], axis=1)
provience_data.to_csv("provience2.csv", index=None, encoding="utf-8-sig")


# 封装函数
def get_data(data, info_list):
    info = pd.DataFrame(data)[info_list]

    today_data = pd.DataFrame(i["today"] for i in data)
    today_data.columns = ["today_" + i for i in today_data.columns]

    total_data = pd.DataFrame(i["total"] for i in data)
    total_data.columns = ["total_" + i for i in total_data.columns]

    return pd.concat([info, total_data, today_data], axis=1)

# 数据保存
def save_data(data,name):
    file_name = './covid_data/'+name+'_'+time.strftime('%Y_%m_%d',time.localtime(time.time()))+'.csv'
    data.to_csv(file_name,index=None,encoding='utf-8-sig')
    print(file_name,'数据已成功保存')
# 测试函数
# 1.数据获取
today_provience = get_data(data_provience, ["id", "name", "lastUpdateTime"])
#today_provience.head()
#today_provience.to_csv("today_provience_gbk.csv", index=None, encoding="gbk")
# 2.
save_data(today_provience,'today_provience')
