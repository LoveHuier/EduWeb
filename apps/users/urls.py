# _*_coding: utf-8_*_

from django.urls import path, include

from .views import UserInfoView, UploadImageView, UpdatePwdView, LogoutView, SendEmailCodeView, UpdateEmailView
from .views import MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView

app_name = "users"
urlpatterns = [
    # 用户信息
    path("info/", UserInfoView.as_view(), name="user_info"),
    # 用户头像上传
    path("image/upload/", UploadImageView.as_view(), name="image_upload"),
    # 个人中心修改密码
    path("update/pwd/", UpdatePwdView.as_view(), name="update_pwd"),
    # 登出
    path("logout/", LogoutView.as_view(), name="logout"),
    # 发送邮箱验证码
    path("sendemail_code/", SendEmailCodeView.as_view(), name="sendemail_code"),
    # 修改邮箱
    path("update_email/", UpdateEmailView.as_view(), name="update_email"),
    # 我的课程
    path("my_courses/", MyCourseView.as_view(), name="my_courses"),
    # 我的收藏的课程机构
    path("myfav/org/", MyFavOrgView.as_view(), name="myfav_org"),
    # 我的收藏的讲师
    path("myfav/teacher/", MyFavTeacherView.as_view(), name="myfav_teacher"),
    # 我的收藏的课程
    path("myfav/course/", MyFavCourseView.as_view(), name="myfav_course"),
]
