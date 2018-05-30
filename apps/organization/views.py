from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict


# Create your views here.


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
        })
