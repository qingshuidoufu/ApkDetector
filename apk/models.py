from django.db import models


# Create your models here.
# apk基础信息
from django.db.models import JSONField


class ApkInfo(models.Model):
    apk_name = models.CharField(max_length=32, verbose_name="应用名称")
    package_name = models.CharField(max_length=64, verbose_name="包名")
    hash_value = models.CharField(max_length=64, verbose_name="HASH", unique=True)
    security_score=models.CharField(max_length=8,verbose_name="安全得分")
    size=models.CharField(max_length=32 ,verbose_name="文件大小")
    user_name=models.CharField(max_length=32,verbose_name="用户名")

# apk详细信息
class ApkDetails(models.Model):
    apk_name = models.CharField(max_length=32, verbose_name="应用名称")
    version=models.CharField(max_length=32,verbose_name="应用版本")
    version_code=models.CharField(max_length=32,verbose_name="安卓版本代号")
    size=models.CharField(max_length=32 ,verbose_name="文件大小")
    md5= models.CharField(max_length=64, verbose_name="HASH值", unique=True)
    sha256=models.CharField(max_length=64,verbose_name="sha256")
    max_sdk=models.CharField(max_length=8,verbose_name="最大SDK")
    min_sdk=models.CharField(max_length=8,verbose_name="最小SDK")
    package_name=models.CharField(max_length=64,verbose_name="安装包名称")
    main_activity=models.CharField(max_length=64,verbose_name="主活动")
    app_type=models.CharField(max_length=8,verbose_name="应用类型")
    security_score=models.CharField(max_length=8,verbose_name="安全得分")
    average_cvss=models.CharField(max_length=8,verbose_name="cvss漏洞评分")
    machine_result=models.CharField(max_length=8,verbose_name="机器学习分类结果")
    user_name = models.CharField(max_length=32, verbose_name="用户名")


# apk超详细信息(json文件)
class ApkJson(models.Model):
    hash_value=models.CharField(max_length=64, verbose_name="md5哈希值")
    user_name = models.CharField(max_length=32, verbose_name="用户名")
    data=JSONField()

# 机器学习分类结果
class ApkLearnResult(models.Model):
    hash_value=models.CharField(max_length=64, verbose_name="md5哈希值")
    user_name = models.CharField(max_length=32, verbose_name="用户名")
    knn_result=models.CharField(max_length=8,verbose_name="knn分析结果")
    native_bayes_result=models.CharField(max_length=8,verbose_name="nativeBayes分析结果")
    decision_tree_result=models.CharField(max_length=8,verbose_name="decisionTree分析结果")
    random_forest_result=models.CharField(max_length=8,verbose_name="randomForest分析结果")


