# _*_coding: utf-8_*_

from django import forms

from operation.models import UserAsk


class UserAskForm(forms.Form):
    name = forms.CharField(required=True, min_length=2, max_length=20)
    phone = forms.CharField(required=True, min_length=11, max_length=11)
    course_name = forms.CharField(required=True, min_length=5, max_length=50)


class AnotherUserForm(forms.ModelForm):
    # 还可以定义字段
    class Meta:
        # 指明modelform是由哪个model转化的
        model = UserAsk
        # 指明要用到的字段，也可以不指明
        fields = ["name", "mobile", "course_name"]


"""
ModelForm不只是继承简单，而且可以像model一样调用save()保存修改过后的数据，save的时候实际上调用的是model的save。
"""
