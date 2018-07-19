# _*_coding: utf-8_*_
import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ("name", "desc", "detail", "degree", "students", "learn_times", "get_zj_nums", "go_to")
    search_fields = ("name", "desc", "detail", "degree", "students")
    list_filter = ("name", "desc", "detail", "degree", "students", "learn_times")
    ordering = ['-students']
    readonly_fields = ['students', 'learn_times']
    list_editable = ["degree", "desc"]

    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs


class BannerCourseAdmin(object):
    list_display = ("name", "desc", "detail", "degree", "students", "learn_times")
    search_fields = ("name", "desc", "detail", "degree", "students")
    list_filter = ("name", "desc", "detail", "degree", "students", "learn_times")
    ordering = ['-students']
    readonly_fields = ['students', 'learn_times']
    list_editable = ["degree", "desc"]

    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ("course", "name", "add_time")
    search_fields = ("course", "name")
    list_filter = ("course__name", "name", "add_time")


class VideoAdmin(object):
    list_display = ("lesson", "name", "add_time")
    search_fields = ("lesson", "name")
    list_filter = ("lesson", "name", "add_time")


class CourseResourceAdmin(object):
    list_display = ("course", "name", "download", "add_time")
    search_fields = ("course", "name", "download")
    list_filter = ("course", "name", "download", "add_time")


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
