import get_save

url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=1593844081982"
data_json = get_save.url_to_data(url)
data_province = data_json["data"]["areaTree"][2]["children"]

all_province = get_save.get_data(data_province, ["id", "name", "lastUpdateTime"])


print(all_province)