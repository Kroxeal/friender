from django.contrib import admin
from django.urls import path, re_path

from .views import *



urlpatterns = [
    path('main/', main_page, name="main"),
    path('friends/', all_friends, name="friends"),
    path('establishments/', place_arrangments, name="establishments"),


]