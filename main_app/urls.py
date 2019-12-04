from django.conf.urls import url
from django.urls import path
from django.template.defaulttags import url
from main_app import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('realtime/', views.realtime, name='realtime'),
    path('login/', views.login, name='login'),
    path('form_login/',views.form_login, name='form_login/'),
    path('register/',views.register),
    path('form_register/',views.form_register),
    path('contact/',views.contact),
    path('form_contact/',views.form_contact),
    path('street_events/',views.street_events),
    path('livelihood_analysis/', views.livelihood_analysis),
    path('hot_community/',views.hot_community),
    path('done/',views.done),
    path('abnormal_events/',views.abnormal_events),
    path('scroll_display/',views.scroll_display),
    path('feedback/',views.feedback),
    # path('read_feedback/',views.read_feedback),
    path('store_feedback/',views.store_feedback),
    path('user_profile/',views.profile),
    path('account_info_change/',views.account_info_change),
    path('logout/',views.logout),
    path('',views.goto_index),# 用于从根目录直接转到/index
    path('delete_feedback/',views.delete_feedback),
]
