# 向MOBSF发送请求, 判断MOBSF的api是否可调用
import pymysql
import requests
from django.conf import settings


def is_MOBSF_connected():
    try:
        # 请求头
        url = 'http://127.0.0.1:9000//api/v1/scans'
        # 请求头
        headers = {"Authorization": "3cad2695b8403693647ca66f28f80e4fa679fd0df43aaee6c8f15bc1ce9df8e1"}
        r = requests.post(url, headers=headers)
        MOBSF_status = '未连接'
        if r.status_code.__eq__('200'):
            MOBSF_status = '已连接'
    except BaseException as e:
        MOBSF_status = '未连接'
        return  MOBSF_status
    return  MOBSF_status

def is_database_connected():
    engine=settings.DATABASES.get('default').get('ENGINE')
    name=settings.DATABASES.get('default').get('NAME')
    user=settings.DATABASES.get('default').get('USER')
    password=settings.DATABASES.get('default').get('PASSWORD')
    host=settings.DATABASES.get('default').get('HOST')
    port=int(settings.DATABASES.get('default').get('PORT'))
    database_status = '未连接'
    try:
        db=pymysql.connect(host=host,port=port,user=user,password=password,db=name)
        database_status='已连接'
        return database_status
        print('数据库连接成功')
    except pymysql.Error as e:
        print('数据库连接失败'+str(e))
        return database_status
