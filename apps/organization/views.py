from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg, CityDict
from .forms import UserAskForm


# Create your views here.


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

            return HttpResponse("{'status':'success'}", content_type="application/json")
        else:
            return HttpResponse("{'status':'fail','msg':'{0}'}".format(userask_form.errors),
                                content_type="application/json")


class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
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
        })
