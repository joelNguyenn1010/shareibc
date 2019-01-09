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
from django.urls import path
from django.conf.urls import url
from .views import ProductAPI, Images, ProductDetailsAPI,ProductCity
urlpatterns = [
    url(r'^city/$', ProductCity.as_view()),
    url(r'^$', ProductAPI.as_view(), name="product_index"),
    url(r'^background/i$', Images.as_view()),
    url(r'^(?P<id>.*)/$', ProductDetailsAPI.as_view(), name="product_details"),

]
