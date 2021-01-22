from .import views
from django.contrib import admin
from django.urls import path, re_path, register_converter, include
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

app_name = 'piro14'

urlpatterns = [
    path('', views.main_before, name='main_before'), #로그인 전 메인화면
    path('login/', views.main_after, name='main_after'), #로그인 후 메인화면
    path('google/', TemplateView.as_view(template_name='piro14/index.html'), name='googlelogin'), #?
    path('accounts/', include('allauth.urls')), #?
    path('list/', views.game_list, name='game_list'), #게임 list
    path('detail/<int:pk>/', views.game_detail, name='game_detail'), #게임 디테일
    path('attack/', views.game_attack, name='game_attack'), #공격하기
    path('ranking/', views.game_ranking, name='game_ranking'), #랭킹보기
    path('delete/<int:pk>/', view=views.game_delete, name = 'game_delete'),
    path('logout/', auth_views.LogoutView.as_view(template_name='piro14/main_bflog.html'), name='logout'),
    path('counterattack/<int:pk>/', views.game_counter_attack, name='game_counter_attack'), #반격하기
]
