from django.shortcuts import render, redirect
from app01 import models
from app01.models import ResignRequest


# 查看所有离职申请
def admin_resign_list(request):
    resign_requests = models.ResignRequest.objects.all().order_by('-submit_date')
    return render(request, "account_resign.html", {"resign_requests": resign_requests})

# 查看所有出差报销申请
def admin_expense_list(request):
    expense_claims = models.ExpenseClaim.objects.all().order_by('-submit_time')
    return render(request, "account_expense.html", {"expense_claims": expense_claims})

# 审批离职申请
def approve_resign(request, resign_id):
    """if request.method == 'POST':
        status = request.POST.get('status')  # 获取提交的状态
        resign_request = models.ResignRequest.objects.get(id=resign_id)
        resign_request.status = status
        resign_request.save()
    return redirect('admin_resign_list')  # 重定向到管理员的离职申请页面"""

    if request.method == "POST":
        status = request.POST.get("status")
        reject_reason = request.POST.get("reject_reason")

        resign_request = ResignRequest.objects.get(id=resign_id)

        if status == "approved":
            resign_request.status = "approved"
        elif status == "rejected":
            resign_request.status = "rejected"
            resign_request.reject_reason = reject_reason  # 保存拒绝理由

        resign_request.save()

        return redirect("/admin/resign/list/")
    return redirect("/admin/resign/list/")

# 审批出差报销申请
def approve_expense(request, expense_id):
    if request.method == 'POST':
        status = request.POST.get('status')  # 获取提交的状态
        expense_claim = models.ExpenseClaim.objects.get(id=expense_id)
        expense_claim.status = status
        expense_claim.save()
    return redirect('admin_expense_list')  # 重定向到管理员的出差报销页面
