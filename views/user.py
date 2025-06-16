from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, PrettyEditModleForm, PrettyModleForm


# views可以拆分 models.py 一定不能拆分


def user_list(request):
    ''' 用户管理 '''

    # 获取所有用户列表 [obj,obj,obj]
    queryset = models.UserInfo.objects.all()

    '''

    # 用Python的语法获取数据
    for obj in queryset:
        print(obj.id,obj.name,obj.account,obj.create_time.strftime("%Y-%m-%d"),obj.get_gender_display(),obj.depart_id,obj.depart.title)

        # obj.get_gender_display() 就是查询1 2 对应的性别
        # get_字段名称_display()
        # obj.depart.title (这里不用depart_id)
        # 即根据id自动去关联的表中获取哪一行数据的depart对象。
        # {{xxxxxxx}} 模板语法中不能加括号
        # {{ obj.get_gender_display }} display后面的括号省略了
    '''

    page_object = Pagination(request, queryset, page_size=5)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, 'user_list.html', context)

# form
def user_add(request):
    ''' 添加用户 （原始方式） '''
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    # 获取提交用户  （POST请求）
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')
    # salary = request.POST.get('slr')

    # 数据将手动添加到数据库中
    models.UserInfo.objects.create(name=user, password=pwd, age=age,
                                   account=account, create_time=ctime,
                                   gender=gender, depart_id=depart_id
                                   )

    # 返回到用户列表（添加成功后重定向）
    return redirect('/user/list/')


# modelform
def user_model_form_add(request):
    ''' 添加用户 (ModelForm版本) '''
    if request.method == 'GET':
        ### 初始化表单对象 ###
        form = UserModelForm()

        #### 渲染表单模板 #####
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法 保存到数据库
        # {'name': 'IDLECY NO', 'password': '311', 'age': 20, 'account': Decimal('778564'), 'create_time': datetime.datetime(2013, 4, 13, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'gender': 1, 'depart': <Department: IT运维部门>}
        print(form.cleaned_data)
        # models.UserInfo.objects.create() 方法1
        form.save()
        return redirect('/user/list/')

    # 校验失败 （在页面上显示错误信息）

    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    ''' 编辑用户 '''
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        # 根据ID去数据库获取要编辑的哪一行数据 (对象)
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {"form": form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据
        # 不需要输入的数据也想要保存 form.instance.字段名 = 值
        form.save()
        return redirect('/user/list')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')