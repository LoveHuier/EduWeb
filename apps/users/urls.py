# _*_coding: utf-8_*_

from django.urls import path, include

from .views import UserInfoView

app_name = "users"
urlpatterns = [
    path("info/", UserInfoView.as_view(), name="user_info"),
]
