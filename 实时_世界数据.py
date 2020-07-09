

import requests
import chardet
import json
import pandas as pd
import get_save

# 爬取信息
url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=318749413808"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/83.0.4103.116 Safari/537.36"}
req = requests.get(url, headers=headers)
req.encoding = chardet.detect(req.content)["encoding"]
data_json = json.loads(req.text)
world_data = data_json["data"]["areaTree"]
# print(world_data)

name_id = pd.DataFrame(world_data)[["id", "name", "lastUpdateTime"]]
world_today_data = pd.DataFrame(i["today"] for i in world_data)
world_total_data = pd.DataFrame(i["total"]for i in world_data)
world_today_data.columns = ["today_"+i for i in world_today_data.columns]
world_total_data.columns = ["total_"+i for i in world_total_data.columns]

world_data = pd.concat([name_id, world_total_data, world_today_data], axis=1)
print(world_data.head(5))
get_save.save_data(world_data, 'word_data')


