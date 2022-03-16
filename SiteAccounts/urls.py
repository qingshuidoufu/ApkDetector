from django.urls import path,include
from . import views


urlpatterns = [

    path('login/',views.my_login),
    path('register/',views.my_regist),
    path('login_auth/',views.login_auth),
    path('logout/',views.my_logout),
    path('register/do_regist/',views.do_regist),
    path('change_password/',views.change_password),
    path("do_change_password/",views.do_change_password)
    ,
]