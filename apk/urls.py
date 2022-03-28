from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path("save_apk_info",views.save_apk_info),
    path("search",views.search),
    path("delete_apk_info",views.delete_apk_info),
    path('basic',views.get_apk_details),
    path("analysis",views.analysis),
    path('apk_pdf',views.apk_pdf),
    path('system_status',views.system_status),
    path('search_by_query',views.search_by_query)
    ,
]