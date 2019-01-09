"""shareibc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls.py/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls.py import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls.py'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
#...
from .views import AuthView, RegisterAPIView, UserSupport, UpdateUser, AuthVerify, UserAPI

urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url('auth/create', RegisterAPIView.as_view()),
    url(r'^api-token-verify/', verify_jwt_token),
    url('refresh-token/', refresh_jwt_token),
    url('support/', UserSupport.as_view()),
    url('update/', UpdateUser.as_view()),
    url('verify/', AuthVerify.as_view()),
    url('retrieve/',UserAPI.as_view())
]

