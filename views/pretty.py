from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm,PrettyEditModleForm,PrettyModleForm

# views可以拆分 models.py 一定不能拆分

def pretty_list(request):
    ''' 靓号列表 '''

 # 防止分页 + 搜索 冲突 实现共同兼容条件
# '''    from django.http.request import QueryDict
#     import copy
#     quert_dict = copy.deepcopy(request.GET)
#     quert_dict._mutable = True
#     quert_dict.setlist('page',[11])
#     print(quert_dict.urlencode())'''


    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile="18881888118",price=20,level=1,status=1)

    ############## 搜索框 ###############
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict = {"mobile__contains": search_data}
        # 写法2
        # data_dict["mobile__contains"] = search_data
    # 在url尾部写 ?q=xxx

    # select * from 表 order by level desc;  ## 下面-level 表示倒叙排 级别高的在上面
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request,queryset)  #### 主要加这一句 就可以实现分页

    page_queryset = page_object.page_queryset

    page_string = page_object.html()

    context = {
        "search_data": search_data,
        "queryset": page_queryset, # 分完页的数据
        "page_string":page_string, # 生成页码
    }
    return render(request,'pretty_list.html', context)

    # # 1.根据用户想要访问的页码，计算出起止位置
    # page = int(request.GET.get('page', 1))
    # page_size = 10  # 每页显示20条数据
    # start = (page - 1) * page_size
    # end = page * page_size
    #
    # # select * from 表 order by level desc;  ## 下面-level 表示倒叙排 级别高的在上面
    # queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")[page_object.start:page_object.end]
    #
    # # 数据总条数
    # total_count = models.PrettyNum.objects.filter(**data_dict).order_by("-level").count()
    #
    # # 总页码
    # total_page_count, div = divmod(total_count, page_size)  # divmod是取余运算
    # if div:
    #     total_page_count += 1

    # # 计算出，显示当前页的前5页、后5页
    # plus = 5
    # if total_page_count <= 2 * plus + 1:
    #     # 数据库中的数据比较少，没有达到11页
    #     start_page = 1
    #     end_page = total_page_count
    # else:
    #     start_page = page - plus
    #     end_page = page + plus
    #
    #     # 数据库中的数据比较多 >11页
    #
    #     # 当前页 <5时 (小极值)
    #     if page <= plus:
    #         start_page = 1
    #         end_page = 2 * plus + 1
    #     else:
    #         # 当前页 > 5
    #         # 当前页+5 > 总页面
    #         if (page + plus) > total_page_count:
    #             start_page = total_page_count - 2 * plus
    #             end_page = total_page_count
    #         else:
    #             start_page = page - plus
    #             end_page = page + plus
    #
    # # 页码
    # page_str_list = []
    #
    # # 首页
    # page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    #
    # # 上一页
    # if page > 1:
    #     prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    # else:
    #     prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    # page_str_list.append(prev)
    #
    # # 页面
    # for i in range(start_page, end_page + 1):
    #     if i == page:
    #         ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
    #     else:
    #         ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
    #     page_str_list.append(ele)
    #
    # # 下一页
    # if page < total_page_count:
    #     prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    # else:
    #     prev = '<li><a href="?page={}">下一页</a></li>'.format(total_page_count)
    # page_str_list.append(prev)
    #
    # # 尾页
    # page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page_count))
    #
    #
    #
    # search_string = '''
    # <li>
    #     <form style="float: left; margin-left: -1px" method="get">
    #         <input name="page"
    #                style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;"
    #                type="text" class="form-control" placeholder="页码">
    #         <button style="border-radius: 0" class="btn btn-group-default" type="submit">跳转</button>
    #     </form>
    # </li>
    #
    # '''
    #
    # page_str_list.append(search_string)
    #
    # page_string = mark_safe("".join(page_str_list))

    # return render(request, 'pretty_list.html',
    #               {"queryset": page_queryset, "search_data": search_data, "page_string": page_string})
# # 搜索手机号是否存在Num: PrettyNum object (6)>]>
# q1 = models.PrettyNum.objects.filter(mobile='17784057456', id = 6)
# print(q1)
#
# data_dict = {"mobile":"17784057456", "id":6}
# q2 = models.PrettyNum.objects.filter(**data_dict)
# print(q2)
#
# # 大于__gt 大于等于__gte 小于__lt 小于等于 __lte
# # 筛选出：mobile__startwith 以什么开头 __endwith 以什么结尾 __contains 包含什么
# models.PrettyNum.objects.filter(id = 6)
# models.PrettyNum.objects.filter(id__gt = 6)
# models.PrettyNum.objects.filter(id__gte = 6)
# models.PrettyNum.objects.filter(id__lt = 6)
# models.PrettyNum.objects.filter(id__lte = 6)
# models.PrettyNum.objects.filter(mobile__startswith="177")
# models.PrettyNum.objects.filter(mobile__endswith="456")
# models.PrettyNum.objects.filter(mobile__contains="456")

def pretty_add(request):
    ''' 添加靓号 '''

    # form = PrettyModleForm()
    # return render(request, 'pretty_add.html', {"form": form})
    if request.method == 'GET':
        form = PrettyModleForm()
        return render(request, 'pretty_add.html', {"form": form})

    # 用户POST提交数据，数据校验
    form = PrettyModleForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    # 校验失败 （在页面上显示错误信息）

    return render(request, 'pretty_list.html', {"form": form})


def pretty_edit(request, nid):
    ''' 编辑靓号 '''
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PrettyEditModleForm(instance=row_object)
        return render(request, 'pretty_edit.html', {"form": form})

    form = PrettyEditModleForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'pretty_edit.html', {"form": form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')