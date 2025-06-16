import os
from django.shortcuts import render, HttpResponse
from app01 import models
from django.conf import settings



def upload_list(request):
    # 获取所有已上传文件
    uploaded_files = []
    media_path = os.path.join(settings.MEDIA_ROOT)  # 文件存储路径
    for file_name in os.listdir(media_path):
        if os.path.isfile(os.path.join(media_path, file_name)):
            uploaded_files.append(file_name)

    if request.method == 'POST' and request.FILES.get('avatar'):
        file_object = request.FILES['avatar']
        file_path = os.path.join(settings.MEDIA_ROOT, file_object.name)

        # 保存文件
        with open(file_path, 'wb') as f:
            for chunk in file_object.chunks():
                f.write(chunk)

        # 添加新文件到上传的文件列表
        uploaded_files.append(file_object.name)

    return render(request, 'upload_list.html', {'uploaded_files': uploaded_files})

"""def upload_list(request):
    # 获取所有已上传文件
    uploaded_files = []
    media_path = os.path.join(settings.MEDIA_ROOT)  # 文件存储路径
    for file_name in os.listdir(media_path):
        if os.path.isfile(os.path.join(media_path, file_name)):
            uploaded_files.append(file_name)

    if request.method == 'POST' and request.FILES.get('avatar'):
        file_object = request.FILES['avatar']
        file_path = os.path.join(settings.MEDIA_ROOT, file_object.name)

        # 保存文件
        with open(file_path, 'wb') as f:
            for chunk in file_object.chunks():
                f.write(chunk)

        # 添加新文件到上传的文件列表
        uploaded_files.append(file_object.name)

    return render(request, 'upload_list.html', {'uploaded_files': uploaded_files})"""


"""def upload_list(request):
    if request.method == 'GET':
        return render(request, 'upload_list.html')
    # print(request.POST)  # 请求体中数据
    # print(request.FILES)  # 请求发过来的文件

    file_object = request.FILES.get('avatar')
    # print(file_object.name)  # 文件名： WeChat 圖片_20221028155023.jpg

    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()

    return HttpResponse('...')"""


from django import forms
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm


class UpForm(BootStrapForm):
    bootstrap_exclude_field = ['img']
    name = forms.CharField(label='姓名')
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像')


def upload_form(request):
    title = 'Form上传'
    if request.method == 'GET':
        form = UpForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():

        # 1.读取图片内容， 写入到文件夹中并获取文件的路径
        image_object = form.cleaned_data.get('img')
        # file_path = 'app01/static/img/{}'.format(image_object.name)


        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)
        media_path = os.path.join("media", image_object.name)


        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()

        # 2.将图片文件路径写入到数据库
        models.Boss.objects.create(
            name = form.cleaned_data['name'],
            age = form.cleaned_data['age'],
            img = media_path,

        )


        return HttpResponse('...')
    return render(request, 'upload_form.html', {'form': form, 'title': title})


from django import forms
from app01.utils.bootstrap import BootStrapModelForm


class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_field = ['img']
    class Meta:
        model = models.City
        fields = "__all__"


def upload_modal_form(request):
    """" 上传文件和数据 (ModalForm) """
    title = "ModelForm上传文件"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form":form, 'title':title})

    form = UpModelForm(data = request.POST, files = request.FILES)
    if form.is_valid():
        # 对于文件： 自动保存
        # 字段 + 上传的路径到数据库
        form.save()
        return HttpResponse("成功")
    return render(request, 'upload_form.html', {"form":form, 'title':title})
