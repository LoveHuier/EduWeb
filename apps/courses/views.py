from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import Course
from operation.models import UserFavorite, CourseComments


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


class CourseDetailView(View):
    """
    课程详情页
    """

    def get(self, request, course_id):
        current_page = "open_course"
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        # 相关机构与课程是否已收藏
        has_fav_org = False
        has_fav_course = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course.course_org.id):
                has_fav_org = True

        # 相关课程推荐
        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = [course]

        return render(request, "course-detail.html", {
            "course": course,
            "current_page": current_page,
            "has_fav_org": has_fav_org,
            "has_fav_course": has_fav_course,
            "relate_course": relate_course,
        })


class CourseInfoView(View):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        current_page = "open_course"
        course = Course.objects.get(id=int(course_id))
        all_resources = course.courseresource_set.all()
        return render(request, "course-video.html", {
            "course": course,
            "current_page": current_page,
            "all_resources": all_resources,
        })


class CommentsView(View):
    """
    课程评论
    """

    def get(self, request, course_id):
        current_page = "open_course"
        course = Course.objects.get(id=int(course_id))
        all_resources = course.courseresource_set.all()
        all_comments = CourseComments.objects.all()
        return render(request, "course-comment.html", {
            "course": course,
            "current_page": current_page,
            "all_comments": all_comments,
            "all_resources": all_resources,
        })


class AddComentsView(View):
    """
    添加课程评论
    """

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type="application/json")

        course_id = int(request.POST.get("course_id", 0))
        comments = request.POST.get("comments", "")
        if comments and course_id > 0:
            course = Course.objects.get(id=course_id)
            course_comment = CourseComments()
            course_comment.course = course
            course_comment.user = request.user
            course_comment.comments = comments
            course_comment.save()

            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')
