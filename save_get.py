import time
import pandas as pd


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
