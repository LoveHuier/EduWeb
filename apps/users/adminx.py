# _*_coding: utf-8_*_

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


class BaseSetting(object):
    # 主题修改
    enable_themes = True
    use_bootswatch = True


class EmailVerifyRecordAdmin(object):
    # 显示样式
    list_display = ("code", "email", "send_type", "send_time")
    # 搜索功能
    search_fields = ("code", "email", "send_type")
    # 数据筛选功能
    list_filter = ("code", "email", "send_type", "send_time")


class BannerAdmin(object):
    list_display = ("title", "image", "url", "index", "add_time")
    search_fields = ("title", "image", "url", "index")
    list_filter = ("title", "image", "url", "index", "add_time")


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
