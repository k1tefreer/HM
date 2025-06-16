from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """ 数据统计页面  """
    return render(request, 'chart_list.html')


def chart_bar(request):
    ''' 构造柱状图的数据 '''
    # 数据可以去数据库中获取
    legend = ['黄琮渊', '黄小帅', '黄1', '黄2', '黄3']

    series_list = [
        {
            'name': '黄琮渊',
            'type': 'bar',
            'data': [10, 25, 36, 50, 40, 30, 60, 55, 70, 80, 65, 75]
        },
        {
            'name': '黄小帅',
            'type': 'bar',
            'data': [30, 50, 60, 40, 30, 45, 70, 80, 90, 75, 85, 90]
        },
        {
            'name': '黄1',
            'type': 'bar',
            'data': [15, 35, 45, 50, 60, 55, 45, 35, 30, 40, 50, 60]
        },
        {
            'name': '黄2',
            'type': 'bar',
            'data': [25, 20, 30, 40, 50, 60, 65, 80, 75, 65, 55, 50]
        },
        {
            'name': '黄3',
            'type': 'bar',
            'data': [40, 30, 60, 70, 80, 90, 85, 90, 100, 110, 120, 130]
        }
    ]

    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月','7月','8月','9月','10月','11月','12月']

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def chart_pie(requset):
    """ 构造饼状图 """

    db_data_list = [
        {"value": 1048, "name": 'IT运维部门'},
        {"value": 735, "name": '销售部'},
        {"value": 580, "name": '游戏开发'},
        {"value": 484, "name": '企划部'},
        {"value": 300, "name": '新媒体'}
    ]

    result = {
        "status": True,
        "data": db_data_list,
    }

    return JsonResponse(result)


def chart_line(request):
    """ 构造折线图 """
    legend = ['成都', '重庆分公司', '浙江分公司', '江苏分公司', '上海分公司']

    series_list = [
        {
            'name': '成都',
            'type': 'line',
            'stack': 'Total',
            'data': [120, 132, 101, 134, 90, 230, 210]
        },
        {
            'name': '重庆分公司',
            'type': 'line',
            'stack': 'Total',
            'data': [220, 182, 191, 234, 290,154, 190, 330, 410,100,99, 330, 310]
        },
        {
            'name': '浙江分公司',
            'type': 'line',
            'stack': 'Total',
            'data': [150, 232, 201, 154, 190, 330, 410,100,99,220, 182, 191, 234, 290]
        },
        {
            'name': '江苏分公司',
            'type': 'line',
            'stack': 'Total',
            'data': [320, 332,  334, 390, 330, 320,820, 932, 901, 934, 1290, 1330]
        },
        {
            'name': '上海分公司',
            'type': 'line',
            'stack': 'Total',
            'data': [820, 932, 901, 934, 1290, 1330, 1320,423,654,321,653,623]
        }
    ]

    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月','7月','8月','9月','10月','11月','12月']

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def highcharts(request):

    """ highcharts示例 """

    return render(request,'highcharts.html')