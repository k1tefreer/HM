"""
# app01/views/llg.py

from django.shortcuts import render, redirect
import time
import jwt
import requests


# ask_glm 函数
def ask_glm(key, model, max_tokens, temperature, content):
    url = "https://openai.api2d.net/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key
    }

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": content
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


# 视图函数
def llg_connect(request):
    # 从 session 中获取 API Token，如果没有则为空
    key = request.session.get('API_TOKEN', '')

    # 如果没有 Token，则检查 POST 请求中的 token 参数
    if not key and 'token' in request.POST:
        key = request.POST.get('token')
        request.session['API_TOKEN'] = key  # 保存 token 到 session

    # 如果仍然没有 Token，返回错误信息
    if not key:
        return render(request, 'llg_connect.html', {
            'error': 'API Token is required!',  # 提示用户 Token 缺失
        })

    # 初始化对话历史（如果尚未初始化）
    if 'messages' not in request.session:
        request.session['messages'] = [{"role": "assistant", "content": "你好，我是ChatGLM，有什么可以帮你？"}]

    if request.method == 'POST':
        model = request.POST.get('model', 'glm-3-turbo')
        max_tokens = int(request.POST.get('max_tokens', 512))
        temperature = float(request.POST.get('temperature', 0.8))

        # 获取用户输入的 prompt
        if 'prompt' in request.POST:
            prompt = request.POST.get('prompt')
            request.session["messages"].append({"role": "user", "content": prompt})

            # 调用 API 获取响应
            response_json = ask_glm(key, model, max_tokens, temperature, request.session["messages"])

            if "choices" in response_json and len(response_json["choices"]) > 0:
                full_response = response_json['choices'][0]['message']['content']
                request.session["messages"].append({"role": "assistant", "content": full_response})
            else:
                request.session["messages"].append({"role": "assistant", "content": "抱歉，没有收到有效的回复。"})

    # 渲染模板
    return render(request, 'llg_connect.html', {
        'messages': request.session.get("messages", []),
        'token': key,
    })

"""