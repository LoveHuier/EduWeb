# _*_coding: utf-8_*_

from django.urls import path

from .views import OrgView, AddUserAskView

app_name = "organization"
urlpatterns = [
    # 课程机构列表页
    path("list/", OrgView.as_view(), name="org_list"),
    path("add_ask/", AddUserAskView.as_view(), name="add_ask"),
]
