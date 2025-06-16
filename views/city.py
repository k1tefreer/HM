from django.shortcuts import render, redirect
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from django.shortcuts import render, redirect, get_object_or_404
from app01.models import City
from django.core.paginator import Paginator


# 城市列表
def city_list(request):
    cities = City.objects.all()  # 获取所有城市
    paginator = Paginator(cities, 5)  # 每页显示5个城市
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'city_list.html', {
        'page_obj': page_obj
    })


# 添加城市
def city_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        count = request.POST.get('count')
        img = request.FILES.get('img')

        City.objects.create(name=name, count=count, img=img)
        return redirect('city_list')  # 提交后返回城市列表

    return render(request, 'city_add.html')


# 编辑城市
def city_edit(request, city_id):
    city = get_object_or_404(City, id=city_id)

    if request.method == 'POST':
        city.name = request.POST.get('name')
        city.count = request.POST.get('count')

        if 'img' in request.FILES:
            city.img = request.FILES['img']

        city.save()
        return redirect('city_list')

    return render(request, 'city_edit.html', {'city': city})


# 删除城市
def city_delete(request, city_id):
    city = get_object_or_404(City, id=city_id)
    city.delete()
    return redirect('city_list')
