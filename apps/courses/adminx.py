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

    def save_models(self):
        """
        在保存课程的时候，统计课程机构的课程数
        :return:
        """
        obj = self.new_obj  # 通过new_obj参数可取出当前对象
        obj.save()  # 保存当前添加的课程，防止统计数量出错
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


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
