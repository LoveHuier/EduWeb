# _*_coding: utf-8_*_

from django.urls import path

from .views import OrgView

app_name = "organization"
urlpatterns = [
    # 课程机构列表页
    path("list/", OrgView.as_view(), name="org_list"),
]
