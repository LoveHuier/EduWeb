# _*_coding: utf-8_*_

from django.urls import path, include

from .views import UserInfoView, UploadImageView

app_name = "users"
urlpatterns = [
    # 用户信息
    path("info/", UserInfoView.as_view(), name="user_info"),
    # 用户头像上传
    path("image/upload/", UploadImageView.as_view(), name="image_upload"),
]
