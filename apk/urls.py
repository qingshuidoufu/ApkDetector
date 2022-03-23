from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path("save_apk_info",views.save_apk_info),
    path("search",views.search),
    path("delete_apk_info",views.delete_apk_info),
    path('basic',views.get_apk_details)
    ,
]