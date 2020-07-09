import pandas as pd
import get_save

# 获取省份id+name
url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=1593844081982"
data = get_save.url_to_data(url)
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
        data = get_save.url_to_data(url)
        world_data = get_save.get_data(data["data"]["list"], ["date"])
        world_data["name"] = world_id_name_dict[i]
        if i == "9577772":
            world_all_data = world_data
            print(world_id_name_dict[i], '\033[0;32m 成功 \033[0m', world_all_data.shape)
        else:
            world_all_data = pd.concat([world_all_data, world_data])
            print(world_id_name_dict[i], '\033[0;32m 成功 \033[0m', world_data.shape)
        # time.sleep(1)
    except:
        print(world_id_name_dict[i], '\033[0;31m 成功 \033[0m', world_data.shape)
get_save.save_data_gbk(world_all_data, "world_all_data")
