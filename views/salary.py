from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from app01.models import SalaryRecord, UserInfo
from datetime import date

from django import forms
from app01.models import SalaryRecord

from django import forms
from app01.models import SalaryRecord

class SalaryForm(forms.ModelForm):
    """工资表单"""
    class Meta:
        model = SalaryRecord
        fields = ['base_salary', 'performance_bonus', 'year_end_bonus', 'late_penalty',
                  'pension', 'medical_insurance', 'unemployment_insurance', 'housing_fund',
                  'tax', 'salary_month']
        widgets = {
            'base_salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入基本工资'}),
            'performance_bonus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入绩效奖金'}),
            'year_end_bonus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入年终奖'}),
            'late_penalty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入迟到罚款'}),
            'pension': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入养老保险'}),
            'medical_insurance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入医疗保险'}),
            'unemployment_insurance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入失业保险'}),
            'housing_fund': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入公积金'}),
            'tax': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入个人所得税'}),
            'salary_month': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


def salary_list(request):
    """工资管理列表"""
    queryset = SalaryRecord.objects.all().order_by('-salary_month')
    return render(request, "salary_list.html", {"salaries": queryset})

def salary_add(request):
    """添加工资记录"""
    if request.method == "POST":
        form = SalaryForm(request.POST)
        if form.is_valid():
            salary = form.save(commit=False)
            user_id = request.POST.get("user")  # 获取选中的员工 ID
            salary.user = get_object_or_404(UserInfo, id=user_id)
            salary.save()
            return redirect('/salary/list/')
    else:
        form = SalaryForm()
        users = UserInfo.objects.all()

    return render(request, "salary_add.html", {"form": form, "users": users})

def salary_edit(request, salary_id):
    """编辑工资记录"""
    salary = get_object_or_404(SalaryRecord, id=salary_id)
    if request.method == "POST":
        form = SalaryForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            return redirect('/salary/list/')
    else:
        form = SalaryForm(instance=salary)

    return render(request, "salary_edit.html", {"form": form})

def salary_delete(request, salary_id):
    """删除工资记录"""
    salary = get_object_or_404(SalaryRecord, id=salary_id)
    salary.delete()
    return redirect('/salary/list/')
