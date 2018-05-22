# _*_coding: utf-8_*_
import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ("name", "desc", "add_time")
    search_fields = ("name", "desc")
    list_filter = ("name", "desc", "add_time")


class CourseOrgAdmin(object):
    list_display = ("city", "name", "desc", "click_nums", "fav_nums", "add_time")
    search_fields = ("city", "name", "desc", "click_nums", "fav_nums")
    list_filter = ("city", "name", "desc", "click_nums", "fav_nums", "add_time")


class TeacherAdmin(object):
    list_display = ("org", "name", "work_years", "work_company", "points", "add_time")
    search_fields = ("org", "name", "work_years", "work_company", "points")
    list_filter = ("org", "name", "work_years", "work_company", "points", "add_time")


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CityDictAdmin)
xadmin.site.register(Teacher, CityDictAdmin)
