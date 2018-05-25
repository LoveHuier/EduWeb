from django.shortcuts import render
from django.contrib.auth import authenticate, login
# 引入原始的认证类
from django.contrib.auth.backends import ModelBackend
# 用Q这个类来完成并集
from django.db.models import Q
# 引进django中的一个基础的View,完成定制功能
from django.views.generic.base import View
# 对密码进行加密
from django.contrib.auth.hashers import make_password

from .models import UserProfile
from .forms import LoginForm, RegisterForm
from utils.email_send import send_register_email


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


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 对密码进行加密
            user_profile.password = make_password(pass_word)

            user_profile.save()

            # 发送激活邮件
            send_register_email(user_name, "register")
            pass


class LoginView(View):
    # 一般只用定义get/post这个方法，django会自动判断调用get/post
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        # 这里LoginForm会对应验证相关的username/password
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return render(request, "index.html", {"msg": "用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form": login_form})


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
                                                  "username": user_name,
                                                  "password": pass_word})
    elif request.method == "GET":
        return render(request, "login.html", {})
