from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from django import forms
from django.shortcuts import render, redirect

##########
    ##       用的form        ###
##########

class UserLoginForm(BootStrapForm):
    name = forms.CharField(label='姓名', widget=forms.TextInput)
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True))
    code = forms.CharField(label='验证码', widget=forms.TextInput)

"""    def clean_password(self):
        return md5(self.cleaned_data["password"])"""


def login_user(request):
    if request.method == "GET":
        form = UserLoginForm()
        return render(request, "login_user.html", {"form": form})

    form = UserLoginForm(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("image_code", "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login_user.html", {"form": form})

        # ✅ 注意这里是 name，不是 username
        user = models.UserInfo.objects.filter(**form.cleaned_data).first()

        if not user:
            form.add_error("password", "用户名或密码错误！")
            return render(request, "login_user.html", {"form": form})

        request.session["info"] = {"id": user.id, "name": user.name, "role": "user"}
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/user/home/")

    return render(request, "login_user.html", {"form": form})

def user_home(request):
    """ 员工登录成功后的首页 """
    return render(request, "user_home.html")
