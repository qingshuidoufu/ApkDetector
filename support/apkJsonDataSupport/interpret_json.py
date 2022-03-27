

import json

# 将应用报告json数据提取解析成可用于机器学习的形式
import os
import re
import pandas as pd

from apk.models import ApkJson


# 保存json字典内特定内容到数据框

def save2dataframe(pydata, dataframe):
    if (None == pydata):
        print("skip! because json file is empty")
        return
    if ('report' in pydata.keys()):  # 处理没有内容的/无效的json文件
        print("skip! because json file is empty.")
        return

    colunm_name = dataframe.columns.tolist()
    filename = pydata['file_name']  # 获取包名
    print(filename)
    dataframe.loc[filename] = 0  # 添加一行

    # 判断receiver是否在内
    if (None != pydata["receivers"]):
        for i in range(len(pydata["receivers"])):
            if pydata["receivers"][i] in colunm_name:  # 判断数据框是否已经有了这个列索引
                dataframe.loc[filename, pydata["receivers"][i]] = 1  # 表示出现有这个
    # 判断providers是否在内
    if (None != pydata["providers"]):
        for i in range(len(pydata["providers"])):
            if pydata["providers"][i] in colunm_name:  # 判断数据框是否已经有了这个列索引
                dataframe.loc[filename, pydata["providers"][i]] = 1  # 表示出现有这个
    # 判断services是否在内
    if (None != pydata["services"]):
        for i in range(len(pydata["services"])):
            if pydata["services"][i] in colunm_name:  # 判断数据框是否已经有了这个列索引
                dataframe.loc[filename, pydata["services"][i]] = 1  # 表示出现有这个
    # 判断permissions是否在内
    if (None != pydata["permissions"]):
        for i in range(len(pydata["permissions"])):
            d = pydata["permissions"]
            if (None != d):
                for key in d.keys():
                    if key in colunm_name:  # 判断数据框是否已经有了这个列索引
                        dataframe.loc[filename, key] = 1;  # 表示出现有这个
    return dataframe


def get_csv(json_file):

    basedir=os.path.dirname(__file__)
    template_json_dir=os.path.join(basedir, '../sampleTemplate/apkJson.json')
    # 样本模板文件
    with open(template_json_dir, 'r') as f:
        dict_raw=json.load(f)
    # 转换字典成数据框
    my_dataframe = pd.DataFrame(dict_raw, index={"conut"})
    # 解析提取json文件成dict(待测试文件
    json_dict=json.loads(json_file)
    # 批量判断permission等数据是否在数据框中, 给他们赋值
    my_dataframe=save2dataframe(json_dict, my_dataframe)

    # 判断每行的应用是否为恶意应用,在数据框中新建一列, 为恶意应用则标识为1,正常数据标识为-1
    col_name = my_dataframe.columns.tolist()
    col_name.insert(0, "signature")
    my_dataframe = my_dataframe.reindex(columns=col_name)
    for index in my_dataframe.index:
        if re.match("[A-Za-z0-9]{32}\.apk", index, flags=0) != None:
            print("this is a attack app")
            my_dataframe.loc[index, 'signature'] = "1"
        else:
            my_dataframe.loc[index, 'signature'] = '-1'
    print("构建好的样本数据框")
    print(my_dataframe)

    # 转换数据框成csv数据
    my_dataframe.to_csv(os.path.join(basedir, '../sampleCsv/csvReport.csv'))

