import os

import pandas as pd
from sklearn.preprocessing import StandardScaler
from joblib import load

# 数据预处理
from support.apkJsonDataSupport.interpret_json import get_csv


def pre_process(static_path):
    print('loading static csv....')
    static_data = pd.read_csv(static_path)

    # 取出静态数据目标值
    static_y = static_data.iloc[:, 1:2]
    static_y.drop([0], inplace=True)

    # 取出静态数据特征值
    # 删除统计数据
    static_x = static_data.drop([0])
    # 删除静态数据目标值
    static_x = static_x.drop(['signature'], axis=1)
    # 删除静态数据文件名
    static_x.drop(static_x.columns[0], inplace=True, axis=1)
    print(static_x)
    print(static_y)

    return static_x


# 标准化
def standarize(static):
    # 实例化一个转换器
    transfer = StandardScaler()
    # 训练集调用fit_transform进行标准化操作
    test = transfer.fit_transform(static)
    return test


# 调用分类器获取分类结果
def mechine_analyse(json_data):
    # 将样本转换为csv中间文件
    get_csv(json_data)

    basedir = os.path.dirname(__file__)
    csv_path = os.path.join(basedir, '../sampleCsv/csvReport.csv')
    knn_model_path = os.path.join(basedir, 'knn.joblib')
    native_bayes_model_path = os.path.join(basedir, 'bayes.joblib')
    decision_tree_model_path = os.path.join(basedir, 'dc.joblib')
    random_forest_model_path = os.path.join(basedir, 'rf.joblib')

    # 数据预处理
    sample_data = pre_process(csv_path)
    # 分类器
    knn_classifier = load(knn_model_path)
    native_bayes_classifier = load(native_bayes_model_path)
    decision_tree_classifier = load(decision_tree_model_path)
    random_forest_classifier = load(random_forest_model_path)

    r1 = knn_classifier.predict(sample_data)
    r2 = native_bayes_classifier.predict(sample_data)
    r3 = decision_tree_classifier.predict(sample_data)
    r4 = random_forest_classifier.predict(sample_data)


    print(r1)
    print(r2)
    print(r3)
    print(r4)

    return {'knn': str(r1[0]) , 'nb':str(r2[0]) , 'dc': str(r3[0]) , 'rf': str(r4[0]) }
