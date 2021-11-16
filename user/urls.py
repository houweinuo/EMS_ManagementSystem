# -*- coding: utf-8 -*-
# @Time    : 2021/11/12 16:08
# @Author  : HWN
# @File    : urls.py
# @Software: PyCharm
from django.urls import path

from user.views import LoginView, RegisterView, AddView, UpdateView, IndexView, DeleteView, LogoutView, login_handle, \
    register_handle,ImageCodeView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('add/', AddView.as_view(), name='add'),
    path('update/', UpdateView.as_view(), name='update'),
    path('index/', IndexView.as_view(), name='index'),
    path('delete/', DeleteView.as_view(), name='delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login_handle/', login_handle, name='login_handle'),
    path('register_handle/', register_handle, name='register_handle'),
    path('image/', ImageCodeView.as_view(), name='image')
]
