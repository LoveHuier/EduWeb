from django.shortcuts import render
from django.contrib.auth import authenticate, login
# 引入原始的认证类
from django.contrib.auth.backends import ModelBackend
# 用Q这个类来完成并集
from django.db.models import Q

from .models import UserProfile


# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 完成username,emali都可以登录
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误！",
                                                  "username":user_name,
                                                  "password":pass_word})
    elif request.method == "GET":
        return render(request, "login.html", {})
