"""stream URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from webcam.views import index,video_feed,AddFace,video_add,requestFaceID,write,requestInsertMySql
from home.views import home
from employees.views import get_employees
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('home/', home),
    path('add/', AddFace),
    path('Department/<int:id>/',get_employees),
    path('video_feed/', video_feed, name="video-feed"),
    path('video_add/', video_add, name="video-add"),
    path('addFaceID',requestFaceID),
    path('addMySql',requestInsertMySql),
    path('write',write)
]
