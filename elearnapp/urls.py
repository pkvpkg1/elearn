from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('login/', views.login_user,name='login'),
    path('logout/', views.logout_view,name='logout_view'),

    
    path('new_user/', views.new_user,name='new_user'),
    path('new_user_ajax/', views.new_user_ajax,name='new_user_ajax'),
    
    path('forget_password/', views.forget_password,name='forget_password'),
    path('contact/', views.contact,name='contact'),
    path('courses/', views.courses,name='courses'),

    path('courses_view/', views.courses_view,name='courses_view'),
    
    path('about/', views.about,name='about'),
    path('my_courses/', views.my_courses,name='my_courses'),
    path('course_video_watch/', views.course_video_watch,name='course_video_watch'),
    path('enroll_course/', views.enroll_course,name='enroll_course'),

    path('order_confirm/', views.order_confirm,name='order_confirm'),
    path('paymenthandler/', views.paymenthandler,name='paymenthandler'),

    path('test_template/', views.test_template,name='test_template'),
    path('course_video_watch_first/', views.course_video_watch_first,name='course_video_watch_first'),
    path('courses_search/', views.search,name='search'),


    
]
