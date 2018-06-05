# _*_coding: utf-8_*_

from django.urls import path

from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView

app_name = "organization"
urlpatterns = [
    # 课程机构列表页
    path("list/", OrgView.as_view(), name="org_list"),
    # 用户咨询
    path("add_ask/", AddUserAskView.as_view(), name="add_ask"),
    # 机构首页
    path("home/<int:org_id>/", OrgHomeView.as_view(), name="org_home"),
    # 机构课程列表页
    path("course/<int:org_id>/", OrgCourseView.as_view(), name="org_course"),
    # 机构介绍页
    path("desc/<int:org_id>/", OrgDescView.as_view(), name="org_desc"),
    # 机构讲师页
    path("teacher/<int:org_id>/", OrgTeacherView.as_view(), name="org_teacher"),
]
