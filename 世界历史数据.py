import time

import pandas as pd
import save_get

# 获取省份id+name
url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=1593844081982"
data = save_get.re_data(url)
data = data["data"]["areaTree"]
# print(data)
world_id_name_dict = {}
for i in data:
    world_id_name_dict[i["id"]] = i["name"]
print(world_id_name_dict)

count = 1

for i in world_id_name_dict:
    print(i)
    try:
        url = "https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=" + i
        data = save_get.re_data(url)
        world_data = save_get.get_data(data["data"]["list"], ["date"])
        world_data["name"] = world_id_name_dict[i]
        if i == "9577772":
            world_all_data = world_data
            print(world_id_name_dict[i], "成功", world_all_data.shape)
        else:
            world_all_data = pd.concat([world_all_data, world_data])
            print(world_id_name_dict[i], "成功", world_data.shape)
        # time.sleep(1)
    except:
        print(world_id_name_dict[i], "失败", world_data.shape)
save_get.save_data_gbk(world_all_data, "world_all_data")
