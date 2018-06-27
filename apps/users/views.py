import json, re
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
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.contrib.auth import logout

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
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


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                # 激活账号
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")

            # 检测邮箱是否已被注册
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"msg": "用户该邮箱已注册！", "register_form": register_form})

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 对密码进行加密
            user_profile.password = make_password(pass_word)
            # 表示用户未激活
            user_profile.is_active = False

            user_profile.save()

            # 发送激活邮件
            send_register_email(user_name, "register")

            return render(request, 'login.html')
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    # 一般只用定义get/post这个方法，django会自动判断调用get/post
    def get(self, request):
        redirect_to = request.GET.get("next", "")
        if not redirect_to:
            # 获取上一个页面的url
            http_referer = request.META["HTTP_REFERER"]  # http://127.0.0.1:8000/course/list/
            regex = 'http://.*?(/.*)'
            referer_url = re.findall(regex, http_referer)[0]
            redirect_to = referer_url
        return render(request, "login.html", {
            "redirect_to": redirect_to,
        })

    def post(self, request):
        # 这里LoginForm会对应验证相关的username/password
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    redirect_to = request.POST.get("next", "")
                    # 数据中有next，重定向到redirect_to
                    if redirect_to:
                        return HttpResponseRedirect(redirect_to)
                    else:
                        return HttpResponseRedirect("/")
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
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


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            # 发送邮件
            send_register_email(email, send_type="forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "msg": ""})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    login_url = "/login/"

    def get(self, request):
        return render(request, "usercenter-info.html", {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type="application/json")


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    login_url = "/login/"

    def post(self, request):
        # upload_form = UploadImageForm(request.POST, request.FILES)
        # if upload_form.is_valid():
        #     image = upload_form.cleaned_data['image']
        #     request.user.image = image
        #     request.user.save()
        # 若想upload_form既用model，又有form的功能，则需要传入一个instance，指明当前实例
        upload_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if upload_form.is_valid():
            upload_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail"}', content_type="application/json")


class UpdatePwdView(View):
    """
    个人中心修改密码
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type="application/json")
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type="application/json")


class LogoutView(LoginRequiredMixin, View):
    """
    退出函数
    """
    login_url = "/login/"

    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    login_url = "/login/"

    def get(self, request):
        email = request.GET.get("email", "")
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type="application/json")

        send_register_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type="application/json")


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改邮箱
    """
    login_url = "/login/"

    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update_email")
        if existed_records:
            user = request.user
            user.email = email
            user.save()

            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type="application/json")
