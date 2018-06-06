# _*_coding: utf-8_*_
from django.urls import path
from .views import CourseListView, CourseDetailView

app_name = "courses"

urlpatterns = [
    # 课程列表页
    path("list/", CourseListView.as_view(), name="course_list"),
    # 课程详情页
    path("detail/<int:course_id>/", CourseDetailView.as_view(), name="course_detail"),
]
