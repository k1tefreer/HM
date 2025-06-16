from django.shortcuts import render, redirect
from django import forms
from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.models import ExpenseClaim,UserInfo
from django.utils import timezone


def view_profile(request):
    # 获取当前登录的用户
    user_id = request.session.get("info", {}).get("id")
    if not user_id:
        return redirect("/login/user/")

    user = UserInfo.objects.get(id=user_id)

    return render(request, "user_profile.html", {
        'user': user,
    })


# 请假/加班共用 Form
class LeaveOvertimeForm(BootStrapForm):
    start_time = forms.DateTimeField(
        label="开始时间",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    end_time = forms.DateTimeField(
        label="结束时间",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    reason = forms.CharField(label="原因", widget=forms.Textarea)
    type_choice = forms.ChoiceField(label="类型", choices=[("leave", "请假"), ("overtime", "加班")])


def leave_overtime(request):
    user_id = request.session.get("info", {}).get("id")


    if request.method == "GET":
        form = LeaveOvertimeForm()
        success = request.GET.get("success") == "1"

        # ✅ 获取当前用户的历史请假 & 加班记录
        leave_records = models.LeaveRequest.objects.filter(user_id=user_id).order_by("-id")
        overtime_records = models.OvertimeRequest.objects.filter(user_id=user_id).order_by("-id")

        return render(request, "leave_overtime.html", {
            "form": form,
            "success": success,
            "leave_records": leave_records,
            "overtime_records": overtime_records
        })

    form = LeaveOvertimeForm(data=request.POST)
    if form.is_valid():
        if not user_id:
            return redirect("/login/user/")
        ###### form 手动定义字段 然后写入数据库 ######
        if form.cleaned_data["type_choice"] == "leave":
            models.LeaveRequest.objects.create(
                user_id=user_id,
                leave_type="other",
                start_time=form.cleaned_data["start_time"],
                end_time=form.cleaned_data["end_time"],
                reason=form.cleaned_data["reason"],
                status="pending"
            )
        else:
            models.OvertimeRequest.objects.create(
                user_id=user_id,
                start_time=form.cleaned_data["start_time"],
                end_time=form.cleaned_data["end_time"],
                reason=form.cleaned_data["reason"],
                status="pending"
            )
        return redirect("/leave_overtime/?success=1")

    return render(request, "leave_overtime.html", {"form": form})

####################### 如果用modelform ###################
"""
class LeaveRequestModelForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_time', 'end_time', 'reason']

class OvertimeRequestModelForm(forms.ModelForm):
    class Meta:
        model = OvertimeRequest
        fields = ['start_time', 'end_time', 'reason']
"""
############################################################


"""def leave_overtime(request):
    if request.method == "GET":
        form = LeaveOvertimeForm()
        success = request.GET.get("success") == "1"
        return render(request, "leave_overtime.html", {"form": form, "success": success})

    form = LeaveOvertimeForm(data=request.POST)
    if form.is_valid():
        user_id = request.session.get("info", {}).get("id")
        if not user_id:
            return redirect("/login/user/")

        if form.cleaned_data["type_choice"] == "leave":
            models.LeaveRequest.objects.create(
                user_id=user_id,
                leave_type="other",
                start_time=form.cleaned_data["start_time"],
                end_time=form.cleaned_data["end_time"],
                reason=form.cleaned_data["reason"],
                status="pending"
            )
        else:
            models.OvertimeRequest.objects.create(
                user_id=user_id,
                start_time=form.cleaned_data["start_time"],
                end_time=form.cleaned_data["end_time"],
                reason=form.cleaned_data["reason"],
                status="pending"
            )

        return redirect("/leave_overtime/?success=1")

    return render(request, "leave_overtime.html", {"form": form})"""

"""# 离职申请
class ResignForm(BootStrapForm):
    reason = forms.CharField(label="离职原因", widget=forms.Textarea)


def resign(request):
    if request.method == "GET":
        form = ResignForm()
        return render(request, "resign.html", {"form": form})

    form = ResignForm(data=request.POST)
    if form.is_valid():
        # 可选方案：作为任务记录
        models.Task.objects.create(
            title="离职申请",
            detail=form.cleaned_data["reason"],
            level=2,
            user_id=1  # 默认管理员ID，或后期可设为 session['info']['id']
        )
        return redirect("/user/home/")

    return render(request, "resign.html", {"form": form})"""


class ResignForm(BootStrapForm):
    reason = forms.CharField(label="离职原因", widget=forms.Textarea)
    file = forms.FileField(label="上传附件（可选）", required=False)  # ✅ 添加这一行


def resign(request):
    user_id = request.session.get("info", {}).get("id")
    if request.method == "GET":
        form = ResignForm()
        # ✅ 获取用户自己的历史离职记录
        records = models.ResignRequest.objects.filter(user_id=user_id).order_by("-id")
        return render(request, "resign.html", {"form": form, "records": records})

    form = ResignForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        models.ResignRequest.objects.create(
            user_id=user_id,
            reason=form.cleaned_data["reason"],
            file=form.cleaned_data["file"],  # ✅ 保存上传文件
            status="pending"
        )
        return redirect("/resign/")
    # POST失败也传 records，避免报错
    records = models.ResignRequest.objects.filter(user_id=user_id).order_by("-id")
    return render(request, "resign.html", {"form": form, "records": records})


# 出差费用报销
class ExpenseForm(BootStrapForm):
    title = forms.CharField(label="报销事项")
    amount = forms.DecimalField(label="金额", max_digits=10, decimal_places=2)
    description = forms.CharField(label="详情说明", widget=forms.Textarea)
    # file = forms.FileField(label="上传附件", required=False)  # 添加附件上传字段


def expense(request):
    user_id = request.session.get("info", {}).get("id")
    if not user_id:
        return redirect("/login/user/")

    if request.method == "GET":
        form = ExpenseForm()
        # 获取当前用户的出差报销记录
        records = ExpenseClaim.objects.filter(user_id=user_id).order_by('-submit_time')
        return render(request, "expense.html", {"form": form, "records": records})

    form = ExpenseForm(data=request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        desc = form.cleaned_data["description"]
        amount = form.cleaned_data["amount"]
        # 创建出差报销申请
        ExpenseClaim.objects.create(
            user_id=user_id,
            amount=amount,
            description=desc,
            status="pending"  # 默认状态为待审批
        )
        return redirect("/expense/?success=1")

    return render(request, "expense.html", {"form": form})
