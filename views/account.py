from django.shortcuts import render, HttpResponse, redirect
from django import forms
from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from app01.utils.code import check_code


def login_select(request):
    """登录身份选择页（我是管理员 / 我是员工）"""
    return render(request, 'login_select.html')

class LoginForm(BootStrapForm):
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput,
                               required=True
                               )
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(render_value=True),  # 密码输错了也不会清空
                               required=True
                               )

    code = forms.CharField(label='验证码',
                           widget=forms.TextInput,
                           required=True
                           )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login_admin(request):
    ''' 登录 '''


    if request.session.get("info", {}).get("role") == "admin":
        return redirect("/admin/list/")  # 管理员主界面

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login_admin.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功, 获取到的用户名和密码
        print(form.cleaned_data)
        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', '')
        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login_admin.html', {'form': form})

        # 去数据库校验用户名和密码是否正确, 获取用户对象、None
        # admin_object = models.Admin.objects.filter(username=form.cleaned_data['username'],password=form.cleaned_data['password']).first()
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('password', '用户名或密码错误！')
            return render(request, 'login_admin.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串； 写到用户浏览器的cookie中； 再写入到session中；
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username, 'role': 'admin'}  # 把当前用户名存储到session中
        # 7天免登录，session信息可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect('/admin/list/')

    return render(request, 'login_admin.html', {'form': form})


from io import BytesIO


def image_code(request):
    ''' 生成图片验证码 '''

    # 调用 pillow函数 生成图片
    img, code_string = check_code()
    print(code_string)

    # 写入到自己的session中 (以便于后续获取验证码再进行校验)
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()  # 创建
    img.save(stream,'png')  # 写入
    return HttpResponse(stream.getvalue(), content_type='image/png')  # 获取
    # content_type='image/png' 浏览器会将其当作图片处理并显示


def logout(request):
    ''' 注销 '''

    request.session.clear()

    return redirect('/login/')
