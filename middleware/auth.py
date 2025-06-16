from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect

########## 我的账号和密码 hcy 123###########
class AuthMiddleware(MiddlewareMixin):
    ''' 中间件 1 '''

    # 如果方法中没有返回值 (返回None)， 继续向后走
    # 如果有返回值 HttpResponse、render、redirect，则不再向后执行
    def process_request(self, request):

        # 0. 排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户的URL /login/
        #if request.path_info in ['/login/', "/image/code/"]:
            #return

        if request.path_info in ['/login/', '/login/admin/', '/login/user/', '/image/code/']:
            return

        # 1. 读取当前访问用户的session信息，如果能读到 ，说明已登录过，就可以继续向后走
        info_dict = request.session.get('info')
        # print(info_dict)
        if info_dict:
            return

        # 2. 如果没登录过，回到登录页面
        return redirect('/login/')


