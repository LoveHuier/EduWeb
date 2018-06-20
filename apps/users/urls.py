# _*_coding: utf-8_*_

from django.urls import path, include

from .views import UserInfoView, UploadImageView, UpdatePwdView

app_name = "users"
urlpatterns = [
    # 用户信息
    path("info/", UserInfoView.as_view(), name="user_info"),
    # 用户头像上传
    path("image/upload/", UploadImageView.as_view(), name="image_upload"),
    # 个人中心修改密码
    path("update/pwd/", UpdatePwdView.as_view(), name="update_pwd"),
]