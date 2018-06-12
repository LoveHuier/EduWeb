from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite


# Create your views here.

class OrgTeacherView(View):
    """
    机构讲师页
    """

    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html', {
            "course_org": course_org,
            "all_teachers": all_teachers,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgDescView(View):
    """
    机构介绍列表页
    """

    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """

    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html', {
            "course_org": course_org,
            "all_courses": all_courses,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:3]

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-homepage.html', {
            "course_org": course_org,
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class AddUserAskView(View):
    """
    添加用户咨询
    """

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            mobile = request.POST.get("mobile", "")
            # modelform调用save方法后，返回一个model类
            # 设置commit=True,调用save之后，保存到数据库；若不设置或设置为False，不提交到数据库。
            userask = userask_form.save(commit=True)

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        current_page = "org"
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()

        # 热门机构(top3),order_by django的orm功能
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 城市筛选功能
        city_id = request.GET.get("city", "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 机构类别筛选功能
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 机构排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
            "current_page": current_page,
        })


class AddFavView(View):
    """
    用户收藏与取消收藏
    """

    def post(self, request):
        fav_id = int(request.POST.get("fav_id", 0))
        fav_type = int(request.POST.get("fav_type", 0))

        # request.user取出request中的user,若用户未登录，会取出一个匿名的user
        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if exist_records:
            # 若用户已收藏，则取消收藏，调用delete方法
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if fav_id > 0 and fav_type > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错！"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        current_page = "teachers"
        all_teachers = Teacher.objects.all()

        teacher_nums = all_teachers.count()

        hot_teachers = all_teachers.order_by("-click_nums")[:3]

        sort = request.GET.get("sort", "")
        if sort == "hot":
            all_teachers = all_teachers.order_by("-click_nums")

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 4, request=request)  # 一定要加上每页个数。
        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "current_page": current_page,
            "all_teachers": teachers,
            "teacher_nums": teacher_nums,
            "hot_teachers": hot_teachers,
            "sort": sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        current_page = "teachers"
        teacher = Teacher.objects.get(id=int(teacher_id))

        all_teachers = Teacher.objects.all()
        hot_teachers = all_teachers.order_by("-click_nums")[:3]

        all_courses = teacher.course_set.all()
        if not all_courses:
            all_courses = []

        return render(request, "teacher-detail.html", {
            "current_page": current_page,
            "teacher": teacher,
            "hot_teachers": hot_teachers,
            "all_courses": all_courses,
        })
