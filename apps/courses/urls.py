# _*_coding: utf-8_*_
from django.urls import path
from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddComentsView

app_name = "courses"

urlpatterns = [
    # 课程列表页
    path("list/", CourseListView.as_view(), name="course_list"),
    # 课程详情页
    path("detail/<int:course_id>/", CourseDetailView.as_view(), name="course_detail"),
    # 课程章节信息页
    path("info/<int:course_id>/", CourseInfoView.as_view(), name="course_info"),
    # 课程评论
    path("comment/<int:course_id>/", CommentsView.as_view(), name="course_comment"),
    # 发表评论
    path("add_comment/", AddComentsView.as_view(), name="add_comment"),
]
