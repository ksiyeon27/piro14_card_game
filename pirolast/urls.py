
from django.contrib import admin
from django.urls import path, re_path, register_converter, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('main/', include('piro14.urls')),
]

