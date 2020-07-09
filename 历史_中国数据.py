import requests
import chardet
import json
import pandas as pd
import save_get

# 爬取信息
url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=318749413808"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.116 Safari/537.36"}
req = requests.get(url, headers=headers)
req.encoding = chardet.detect(req.content)["encoding"]
data_json = json.loads(req.text)
china_history_data = data_json["data"]["chinaDayList"]
# print(china_history_data)
# 获取当天日期
china_date = pd.DataFrame(china_history_data)["date"]
# print(info)
# 获取每天总计数据
# 获取每天总计数据（浓缩）
china_total_data = pd.DataFrame([i["total"] for i in china_history_data])
# print(china_total_data.head())
# 获取每天实时数据（浓缩）
china_today_data = pd.DataFrame([i["today"] for i in china_history_data])
# print(china_today_data)

# 更改列名
china_total_data.columns = ["total_" + i for i in china_today_data.columns]
china_today_data.columns = ["today_" + i for i in china_today_data.columns]
# print(china_total_data)
# 合并
china_data = pd.concat([china_date, china_total_data, china_today_data], axis=1)
save_get.save_data(china_data, "china_data")
