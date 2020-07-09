import json
import time

import chardet
import pandas as pd
import requests


def url_to_data(url):
    url = url
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/83.0.4103.116 Safari/537.36"}
    req = requests.get(url, headers=headers)
    req.encoding = chardet.detect(req.content)["encoding"]
    # print(req.status_code)
    # print(req.text)
    # 转换为json格式
    data_json = json.loads(req.text)
    return data_json

# 给一个json数据，和一个需要列的名字，返回一个
def get_data(data, info_list):

    info = pd.DataFrame(data)[info_list]

    today_data = pd.DataFrame(i["today"] for i in data)
    today_data.columns = ["today_" + i for i in today_data.columns]

    total_data = pd.DataFrame(i["total"] for i in data)
    total_data.columns = ["total_" + i for i in total_data.columns]

    return pd.concat([info, total_data, today_data], axis=1)


# 数据保存
def save_data(data, name):
    file_name = './covid_data/' + name + '_' + time.strftime('%Y_%m_%d', time.localtime(time.time())) + '.csv'
    data.to_csv(file_name, index=None, encoding='utf-8-sig')
    print(file_name, '数据已成功保存')


def save_data_gbk(data, name):
    file_name = './covid_data/' + name + '_' + time.strftime('%Y_%m_%d', time.localtime(time.time())) + '.csv'
    data.to_csv(file_name, index=None, encoding='gbk')
    print(file_name, '数据已成功保存')


name_dict = {'date': '日期', 'id': "编号", 'name': '名称', 'lastUpdateTime': '更新时间', 'total_confirm': '累计确诊',
             'total_suspect': '累计疑似',
             'total_heal': '累计治愈', 'total_dead': '累计死亡', 'total_severe': '累计重症', 'total_input': '累计输入',
             'total_newConfirm': '累计新增确诊', 'total_newDead': '累计新增死亡', 'total_newHeal': '累计新增治愈',
             'today_confirm': '当日新增确诊',
             'today_suspect': '当日新增疑似', 'today_heal': '当日新增治愈', 'today_dead': '当日新增死亡', 'today_severe': '当日新增重症',
             'today_storeConfirm': '当日现存确诊', 'today_input': '当日新增输入'}
