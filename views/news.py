import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01 import models  # 如果需要访问模型，这里是导入的方式

@csrf_exempt
def news_list(request):
    if request.method == 'GET' and 'HTTP_X_REQUESTED_WITH' in request.headers and request.headers['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
        # 豆瓣电影排行榜页面 URL
        url = 'https://movie.douban.com/chart'

        try:
            # 发送 GET 请求
            response = requests.get(url, timeout=10)  # 设置超时
            response.raise_for_status()  # 如果响应状态码不是 200，将引发异常

            # 解析 HTML 内容
            soup = BeautifulSoup(response.content, 'html.parser')

            # 获取电影列表
            movies = soup.select('.chart .list .item')  # 根据实际页面结构调整选择器

            # 提取前十部电影的信息
            top_10_movies = []
            for idx, movie in enumerate(movies[:10]):
                title = movie.select_one('.title').get_text(strip=True) if movie.select_one('.title') else '未知'
                link = movie.select_one('a')['href'] if movie.select_one('a') else '#'
                top_10_movies.append({"rank": idx + 1, "title": title, "link": link})

            # 返回电影信息作为 JSON 响应
            return JsonResponse({'movies': top_10_movies})
        except requests.exceptions.RequestException as e:
            # 请求失败时返回错误信息
            return JsonResponse({'error': f'Error fetching data: {str(e)}'}, status=500)
    else:
        # 非有效请求返回错误信息
        return JsonResponse({'error': 'Invalid request'}, status=400)

