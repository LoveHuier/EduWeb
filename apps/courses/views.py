from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course


# Create your views here.


class CourseListView(View):
    def get(self, request):
        current_page = "open_course"
        all_courses = Course.objects.all().order_by("-add_time")

        # 热门课程
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 排序
        sort = request.GET.get("sort", "")
        if sort == "hot":
            all_courses = all_courses.order_by("-click_nums")
        elif sort == "students":
            all_courses = all_courses.order_by("-students")

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 9, request=request)  # 一定要加上每页个数。
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "current_page": current_page,
            "sort": sort,
            "hot_courses": hot_courses,
        })
