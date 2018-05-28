"""EduWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
import xadmin

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    # 调用TemplateView类的as_view方法，会自动转化一个view的函数过来，并在template_name参数指定文件即可，不用自己写一个view类
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),

    # 验证码
    path("captcha/", include('captcha.urls')),
    # 用户激活
    path("active/<str:active_code>/", ActiveUserView.as_view(), name="active"),
    path("forget/", ForgetPwdView.as_view(), name="forget_pwd"),
    # 密码重置链接
    path("reset/<str:reset_code>/", ResetView.as_view(), name="reset_pwd"),
    path("modify_pwd/", ModifyPwdView.as_view(), name="modify_pwd"),
]
