from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from app01.models import AttendanceRecord, UserInfo, Department, LeaveRequest, OvertimeRequest
import random
from app01 import models


# ✅ 写死的模拟数据
"""LEAVE_DATA = [
    {"id": 1, "user": "黄琮渊", "leave_type": "年假", "start_time": "2024-03-05 09:00", "end_time": "2024-03-07 18:00", "reason": "家庭出游", "status": "已通过"},
    {"id": 2, "user": "黄小帅", "leave_type": "病假", "start_time": "2024-03-12 09:00", "end_time": "2024-03-13 18:00", "reason": "感冒发烧", "status": "待审批"},
    {"id": 3, "user": "NOIDLECY", "leave_type": "其他", "start_time": "2024-03-20 13:00", "end_time": "2024-03-20 18:00", "reason": "临时事务", "status": "已拒绝"},
    {"id": 4, "user": "小许", "leave_type": "想去外面玩", "start_time": "2024-03-20 13:00", "end_time": "2024-03-20 18:00", "reason": "个人原因", "status": "已拒绝"}
]

OVERTIME_DATA = [
    {"id": 1, "user": "黄琮渊", "start_time": "2024-03-09 19:00", "end_time": "2024-03-09 22:00", "reason": "系统紧急修复", "status": "已通过"},
    {"id": 2, "user": "小张", "start_time": "2024-03-14 18:30", "end_time": "2024-03-14 21:30", "reason": "补齐功能开发", "status": "待审批"}
]
"""

"""# 查询数据库中的真实数据替
LEAVE_DATA = LeaveRequest.objects.select_related("user").order_by("-id")
OVERTIME_DATA = OvertimeRequest.objects.select_related("user").order_by("-id")"""

"""def update_leave_status(request):
    if request.method == "POST":
        leave_id = int(request.POST.get("leave_id"))
        new_status = request.POST.get(f"status_{leave_id}")
        LeaveRequest.objects.filter(id=leave_id).update(status=new_status)
    return redirect("/attendance/report_matrix/")

def update_overtime_status(request):
    if request.method == "POST":
        overtime_id = int(request.POST.get("overtime_id"))
        new_status = request.POST.get(f"status_{overtime_id}")
        OvertimeRequest.objects.filter(id=overtime_id).update(status=new_status)
    return redirect("/attendance/report_matrix/")"""


def update_leave_status(request):
    if request.method == "POST":
        ids = request.POST.getlist("leave_ids[]")
        print("✅ 接收到的 leave_ids:", ids)

        for lid in ids:
            status = request.POST.get(f"status_{lid}")
            print(f"准备更新：请假记录ID={lid}, 新状态={status}")
            if status:
                models.LeaveRequest.objects.filter(id=lid).update(status=status)

    return redirect("/attendance/report_matrix/")


def update_overtime_status(request):
    if request.method == "POST":
        ids = request.POST.getlist("overtime_ids[]")
        print("✅ 接收到的 overtime_ids:", ids)

        for oid in ids:
            status = request.POST.get(f"status_{oid}")
            print(f"准备更新：加班记录ID={oid}, 新状态={status}")
            if status:
                models.OvertimeRequest.objects.filter(id=oid).update(status=status)

    return redirect("/attendance/report_matrix/")



def attendance_report_matrix(request):
    """以部门筛选 + 用户横向考勤视图（模拟√×）"""
    today = timezone.now().date()
    start_date = today - timedelta(days=29)
    date_list = [start_date + timedelta(days=i) for i in range(30)]

    # 获取部门dept
    selected_dept = request.GET.get("dept")
    # 选择就当前 否则所有
    if selected_dept:
        users = UserInfo.objects.filter(depart_id=selected_dept)
    else:
        users = UserInfo.objects.all()

    ## 写入
    attendance_data = []
    for user in users:
        row = {
            "user": user,
            "records": []
        }
        for day in date_list:
            if random.random() < 0.9:
                row["records"].append("√")
            else:
                row["records"].append("×")
        attendance_data.append(row)

    dept_list = Department.objects.all()

    ##### 获取用户端的
    leave_data = LeaveRequest.objects.select_related("user").order_by("-id")
    overtime_data = OvertimeRequest.objects.select_related("user").order_by("-id")

    return render(request, "attendance_matrix.html", {
        "attendance_data": attendance_data,
        "date_list": date_list,
        "dept_list": dept_list,
        "selected_dept": int(selected_dept) if selected_dept else None,
        "leaves": leave_data,
        "overtimes": overtime_data,
    })


"""    return render(request, "attendance_matrix.html", {
        "attendance_data": attendance_data,
        "date_list": date_list,
        "dept_list": dept_list,
        "selected_dept": int(selected_dept) if selected_dept else None,
        "leaves": LEAVE_DATA,
        "overtimes": OVERTIME_DATA,
    })"""

"""def update_leave_status(request):
    """"""
    if request.method == "POST":
        leave_id = int(request.POST.get("leave_id"))
        new_status = request.POST.get(f"status_{leave_id}")
        for item in LEAVE_DATA:
            if item["id"] == leave_id:
                item["status"] = {
                    "pending": "待审批",
                    "approved": "已通过",
                    "rejected": "已拒绝"
                }.get(new_status, "待审批")
    return redirect("/attendance/report_matrix/")


def update_overtime_status(request):
    """"""
    if request.method == "POST":
        overtime_id = int(request.POST.get("overtime_id"))
        new_status = request.POST.get(f"status_{overtime_id}")
        for item in OVERTIME_DATA:
            if item["id"] == overtime_id:
                item["status"] = {
                    "pending": "待审批",
                    "approved": "已通过",
                    "rejected": "已拒绝"
                }.get(new_status, "待审批")
    return redirect("/attendance/report_matrix/")"""
