from django.urls import path, include, re_path
from . import views


urlpatterns = [

    path('login',views.my_login),
    path('register/',views.my_regist),
    path('login_auth',views.login_auth),
    path('logout/',views.my_logout),
    path('register/do_regist/',views.do_regist),
    path('change_password/',views.change_password),
    path("do_change_password/",views.do_change_password),
    path('password/change/',views.change_password),
    # path('send_email/',views.send_email),
    path('',include('allauth.urls')),
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^profile/update/$', views.profile_update, name='profile_update'),
    re_path(r'^profile/do_update/$', views.do_profile_update)
    ,
]