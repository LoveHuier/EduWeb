# _*_coding: utf-8_*_
from django.urls import path
from .views import CourseListView

app_name = "courses"

urlpatterns = [
    # 课程列表页
    path("list/", CourseListView.as_view(), name="course_list"),
]
