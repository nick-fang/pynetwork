"""djbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import login
from djbank_app import views #估计下面path函数中的路径字符串待修改？？

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'accounts/login/', login, name='login'), #django的login视图函数默认登录的url为r'accounts/login/
    path(r'', views.index_view, name='index'),
    path(r'pay/', views.pay_view, name='pay'),
    path(r'logout/', views.lougout_view),
]
