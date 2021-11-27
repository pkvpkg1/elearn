from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('login/', views.login_user,name='login'),
    path('logout/', views.logout_view,name='logout_view'),
    path('add_new_course/', views.add_new_course,name='add_new_course'),

    path('add_new_course_ajax/', views.add_new_course_ajax,name='add_new_course_ajax'),
    path('add_new_course_video/', views.add_new_course_video,name='add_new_course_video'),
    path('add_new_course_video_ajax/', views.add_new_course_video_ajax,name='add_new_course_video_ajax'),

]

