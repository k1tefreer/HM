############# 为了方便区分，把用了form的都写到这里 ###############
################ ModelForm 表单 的集合，专门用于表单验证和数据处理 ##############

####### Meta  内嵌类 ######################
# 允许你指定表单的配置，如字段、验证、样式等  ###

from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from app01.utils.bootstrap import BootStrapModelForm
from app01.models import Job

class PrettyModleForm(BootStrapModelForm):
    # 验证：方式1 字段+正则方法
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"
        # exclude = ['level'] 三种形式

    ### ############## 格式化更美观 #############



    # 验证:方式2 钩子方法 只需要Mobile
    # def clean_mobile(self):
    #     txt_mobile = self.cleaned_data["mobile"]
    #
    #     if len(txt_mobile) != 11:
    #     # 验证不通过
    #         raise ValidationError("格式错误")
    #
    #     # 验证通过，用户输入的值返回
    #     return txt_mobile

class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=3,
                           label='用户名',
                           widget=forms.TextInput(attrs = {"class":"form-control"})
                           )

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']

class PrettyEditModleForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True,label='手机号')
    # 正则表达式的校验
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]


    # # 验证:方式2 钩子方法 只需要Mobile
    def clean_mobile(self):

        # 当前编辑的哪一行的id pk就是Primary Key
        print(self.instance.pk)

        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在')

        # 验证通过，用户输入的值返回
        return txt_mobile



from app01.models import Job

class JobModelForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = "__all__"


class JobEditModelForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = "__all__"
