"""
URL configuration for thalos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from . import views, auth_views

urlpatterns = [
    # path('', include(router.urls)),
    path('keep/', auth_views.KeepAv.as_view()),
    path('access/', auth_views.CustomAuthToken.as_view()),
    path('validate2FA/', auth_views.Validate2FA.as_view()),
    path('get_token/', auth_views.RecoverPass.as_view()),
    path('generate_password/', auth_views.GeneratePass.as_view(), name='generate-password'),

    path('', views.index, name="index"),
    path('roles/list/', views.RolesList.as_view()),
    path('user/list/', views.UserList.as_view()),
    path('user/get/<slug:pk>', views.UserDetail.as_view()),
    path('user/create/', views.UserCreate.as_view()),
    path('user/update/status/<slug:pk>', views.UserUpdateStatus.as_view()),
    path('user/update/<slug:pk>', views.UserUpdate.as_view()),
]
