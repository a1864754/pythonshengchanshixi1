import time

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


# 获取各省份url
count = 1
for i in province_dict:
    print(i)
    try:
        url = "https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=" + i
        data = save_get.re_data(url)
        province_data = save_get.get_data(data["data"]["list"], ["date"])
        province_data["name"] = province_dict[i]

        if i == "420000":
            all_province = province_data
            print(province_dict[i], "成功", province_data.shape)
        else:
            all_province = pd.concat([all_province, province_data])
            print(province_dict[i], "成功", province_data.shape)
        time.sleep(1)
    except:
        print()

save_get.save_data_gbk(all_province,"all_province")



