# _*_coding: utf-8_*_

import re
from django import forms

from operation.models import UserAsk


# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=5, max_length=50)


class UserAskForm(forms.ModelForm):
    # 还可以定义字段
    class Meta:
        # 指明modelform是由哪个model转化的
        model = UserAsk
        # 指明要用到的字段，也可以不指明
        fields = ["name", "mobile", "course_name"]

    # 对字段做自定义验证，方法名必须以clean开头;初始化form的时候，自动调用clean_mobile方法
    def clean_mobile(self):
        # 利用form的内置变量cleaned_data(它是字典类型)，取出form中的数据
        mobile = self.cleaned_data["mobile"]

        REGEX_MOBILE = '^1[3578]\d{9}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            # 用raise抛出异常
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")
