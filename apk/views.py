import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

from apk.models import ApkInfo, ApkDetails, ApkJson, ApkLearnResult

# 添加apk信息(info为基础信息, details为详细信息
from support.predict import mechine_analyse


@login_required
def save_apk_info(request):
    if request.method == "POST":  # 判断Post请求提交表单
        # 基础信息保存
        apk_info = ApkInfo()  # 创建一个apkInfo实例
        apk_info.apk_name = request.POST.get("apk_name")
        apk_info.package_name = request.POST.get("package_name")
        apk_info.hash_value = request.POST.get("hash_value")
        apk_info.security_score = request.POST.get("security_score")
        apk_info.size = request.POST.get("size")
        apk_info.user_name = request.user.username
        apk_info.save()

        # 详细信息保存
        apk_details = ApkDetails()  # 保存应用详细
        apk_details.apk_name = request.POST.get("apk_name")
        apk_details.version = request.POST.get("version")
        apk_details.version_code = request.POST.get("version_code")
        apk_details.size = request.POST.get("size")
        apk_details.md5 = request.POST.get("md5")
        apk_details.sha256 = request.POST.get("sha256")
        apk_details.max_sdk = request.POST.get("max_sdk")
        apk_details.min_sdk = request.POST.get("min_sdk")
        apk_details.package_name = request.POST.get("package_name")
        apk_details.main_activity = request.POST.get("main_activity")
        apk_details.app_type = request.POST.get("app_type")
        apk_details.security_score = request.POST.get("security_score")
        apk_details.average_cvss = request.POST.get("average_cvss")
        apk_details.user_name = request.user.username
        apk_details.save()

        #  保存json数据
        apk_json = ApkJson()
        apk_json.hash_value = request.POST.get("md5")
        apk_json.user_name = request.user.username
        apk_json.data = request.POST.get("apk_json")
        apk_json.save()

        #  运行机器学习代码,获取机器学习分类结果

        # 新建一个model
        apk_learn_result = ApkLearnResult()
        # 获取分类结果
        result = mechine_analyse(apk_json.data)

        apk_learn_result.hash_value = request.POST.get("md5")
        apk_learn_result.user_name = request.user.username

        apk_learn_result.knn_result= result.get('knn')
        apk_learn_result.native_bayes_result = result.get('nb')
        apk_learn_result.decision_tree_result = result.get('dc')
        apk_learn_result.random_forest_result = result.get('rf')
        apk_learn_result.save()

        return HttpResponse(json.dumps({'msg': 'success'}), content_type='application/json')


@login_required()
def search(request):
    apk_info_list = ApkInfo.objects.all().filter(user_name=request.user.username).order_by('-id')

    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(apk_info_list, 10)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            apk_infos = paginator.page(page)
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            apk_infos = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            apk_infos = paginator.page(paginator.num_pages)
        return render(request, "search.html", {'apk_infos': apk_infos})


# 删除info信息
@login_required()
def delete_apk_info(request):
    apk_info = ApkInfo.objects.get(hash_value=request.POST.get("hash"))
    apk_info.delete()

    #  连带删除apk_details信息
    apk_details = ApkDetails.objects.get(md5=request.POST.get("hash"))
    apk_details.delete()

    #  连带删除apk_json数据
    apk_json = ApkJson.objects.get(hash_value=request.POST.get("hash"))
    apk_json.delete()

    # 连带删除机器学习分类结果
    apk_learn_result = ApkLearnResult.objects.get(hash_value=request.POST.get("hash"))
    apk_learn_result.delete()

    return HttpResponse(json.dumps({'msg': '本地数据库删除成功'}), content_type='application/json')


# 查看详情
@login_required()
def get_apk_details(request):
    hash_value = request.GET.get("hash")
    if hash_value is None:
        return render(request, "basic.html", {'context': '未指定apk文件, 请使用查询功能选择一个应用后查看'})
    else:
        try:
            apk_details = ApkDetails.objects.get(md5=hash_value)
            apk_learn_result = ApkLearnResult.objects.get(hash_value=hash_value)
            class_string_dict={}
            if apk_learn_result.knn_result.__eq__('1'):
                class_string_dict['knn']='恶意应用'
            else:
                class_string_dict['knn']='正常应用'
            if apk_learn_result.native_bayes_result.__eq__('1'):
                class_string_dict['nb']='恶意应用'
            else:
                class_string_dict['nb']='正常应用'
            if apk_learn_result.decision_tree_result.__eq__('1'):
                class_string_dict['dc'] = '恶意应用'
            else:
                class_string_dict['dc'] = '正常应用'
            if apk_learn_result.random_forest_result.__eq__('1'):
                class_string_dict['rf'] = '恶意应用'
            else:
                class_string_dict['rf'] = '正常应用'
        except:
            return render(request, "basic.html")
        return render(request, "basic.html",
                      {'apk_details': apk_details, 'class_string_dict' : class_string_dict,'context': '此为应用的基本信息和基本分析情况, 请点击查看详细分析报告查看详细信息'})


# 分析结果展示
@login_required()
def analysis(request):
    hash_value = request.GET.get("hash")
    if hash_value is None:
        return render(request, "analysis.html", {'context': '未指定apk文件, 请使用查询功能选择一个应用后查看'})
    else:
        try:
            apk_json = ApkJson.objects.get(hash_value=hash_value)

        except:
            return render(request, "analysis.html")
    return render(request, "analysis.html",
                  {'apk_json': apk_json.data,  'hash': hash_value,
                   'context': '分析结果以json数据展示'})
