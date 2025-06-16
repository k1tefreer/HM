from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from app01.models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'salarys', 'job_type', 'dept']  # 字段更新

def job_list(request):
    """招聘信息列表"""
    search_query = request.GET.get('q', '')
    jobs = Job.objects.all()
    if search_query:
        jobs = jobs.filter(title__icontains=search_query)

    return render(request, 'job_list.html', {"jobs": jobs, "search_query": search_query})

def job_add(request):
    """添加招聘信息"""
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/job/list/')
    else:
        form = JobForm()

    return render(request, 'job_add.html', {"form": form})

def job_edit(request, job_id):
    """编辑招聘信息"""
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('/job/list/')
    else:
        form = JobForm(instance=job)

    return render(request, 'job_edit.html', {"form": form})

def job_delete(request, job_id):
    """删除招聘信息"""
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return redirect('/job/list/')
