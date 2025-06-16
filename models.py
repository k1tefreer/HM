from django.db import models


# Create your models here.
class Admin(models.Model):
    ''' 管理员 '''
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    ''' 部门表 '''
    title = models.CharField(verbose_name='标题', max_length=32)

    # verbase_name 就相当于注释

    def __str__(self):
        return self.title
    #   <!-- 获取字段名 -->


class UserInfo(models.Model):
    ''' 员工表 '''
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name='入职时间') 没有时分秒了
    create_time = models.DateField(verbose_name='入职时间') # 如果要改 把DateField改为 Datetimefield
    # salary = models.DecimalField(verbose_name='薪水', max_digits=10, decimal_places=2, default=0)

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name='部门ID' )

    # 1.有约束
    # - to, 与那张表关联 - to_field, 与表中的哪一列关联
    # 2.django自动
    # - 写的depart - 生成数据列 depart_id
    # 3.部门表呗删除
    # #### 3.1 级联删除
    depart = models.ForeignKey(verbose_name='部门', to='Department', to_field='id', on_delete=models.CASCADE)
    # #### 3.2 置空
    # depart = models.ForeignKey(to='Department', to_fields='id',null = True,blank= True,on_delete=models.CASCADE)

    # 在django中做的约束
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)


class PrettyNum(models.Model):
    ''' 靓号表 '''
    mobile = models.CharField(verbose_name='手机号', max_length=32)
    # <!-- 手机号不用int max_length不用11 是因为会搜索 故把这个设置成字符串形式-->
    # 想要允许为空 null=True black=True
    price = models.IntegerField(verbose_name='价格', default=0)  # 整形长度不用加

    level_choices = (
        (1, '1级'),
        (2, '2级'),
        (3, '3级'),
        (4, '4级'),
    )

    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)

    status_choice = (
        (1, "已占用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choice, default=2)


class Task(models.Model):
    ''' 任务 '''
    level_choice = (
        (1, '紧急'),
        (2, '重要'),
        (3, '临时')
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choice, default=1)
    title = models.CharField(verbose_name='标题', max_length=64)
    detail = models.TextField(verbose_name='详细信息')
    # user_id
    user = models.ForeignKey(verbose_name='负责人', to='Admin', on_delete=models.CASCADE)


class Order(models.Model):
    ''' 订单 '''
    oid = models.CharField(verbose_name='订单号', max_length=64)
    title = models.CharField(verbose_name='名称', max_length=32)
    price = models.IntegerField(verbose_name='价格 ')
    status_choice = (
        (1, "待支付"),
        (2, "已支付"),
    )

    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice, default=1)  # default=1 表示默认为1 待支付
    # admin_id
    admin = models.ForeignKey(verbose_name='管理员', to='admin', on_delete=models.CASCADE)


class Boss(models.Model):
    ''' 老板 '''
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    img = models.CharField(verbose_name='头像', max_length=120)


class City(models.Model):
    ''' 城市 '''
    name = models.CharField(verbose_name='名称', max_length=32)
    count = models.IntegerField(verbose_name='人口')

    # 本质上数据库也是CharField, 自动保存数据。
    img = models.FileField(verbose_name='Logo', max_length=120, upload_to='city/')


from django.db import models


class Job(models.Model):
    """ 职位表 """
    title = models.CharField(verbose_name='职位名称', max_length=64)
    company = models.CharField(verbose_name='公司名称', max_length=64)
    salarys = models.DecimalField(verbose_name='薪资', max_digits=10, decimal_places=2, default=0)  # 修改字段名

    create_time = models.DateField(verbose_name='发布时间', auto_now_add=True)

    JOB_TYPE_CHOICES = (
        (1, '全职'),
        (2, '兼职'),
        (3, '实习'),
    )
    job_type = models.SmallIntegerField(verbose_name='职位类型', choices=JOB_TYPE_CHOICES)

    dept = models.ForeignKey(
        'app01.Department',  # 关联到 Department 表
        on_delete=models.CASCADE,
        verbose_name='所属部门'
    )  # 修改 department 为 dept

    def __str__(self):
        return self.title

    class Meta:
        db_table = "app01_job"


from django.db import models
from django.contrib.auth.models import User


class AttendanceRecord(models.Model):
    """"""
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="员工")  # ✅ 关联 UserInfo
    check_in_time = models.DateTimeField(null=True, blank=True, verbose_name="上班打卡")
    check_out_time = models.DateTimeField(null=True, blank=True, verbose_name="下班打卡")
    date = models.DateField(auto_now_add=True, verbose_name="日期")

class LeaveRequest(models.Model):
    """"""
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="申请人")  # ✅ 关联 UserInfo
    leave_type = models.CharField(max_length=20, choices=[
        ('annual', '年假'),
        ('sick', '病假'),
        ('other', '其他')
    ])
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='pending')  # pending / approved / rejected

class OvertimeRequest(models.Model):
    """"""
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="申请人")  # ✅ 关联 UserInfo
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='pending')


class SalaryRecord(models.Model):
    """工资管理"""
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="员工")
    base_salary = models.DecimalField(verbose_name="基本工资", max_digits=10, decimal_places=2)
    performance_bonus = models.DecimalField(verbose_name="绩效奖金", max_digits=10, decimal_places=2, default=0)
    year_end_bonus = models.DecimalField(verbose_name="年终奖", max_digits=10, decimal_places=2, default=0)
    late_penalty = models.DecimalField(verbose_name="迟到罚款", max_digits=10, decimal_places=2, default=0)

    # 五险一金
    pension = models.DecimalField(verbose_name="养老保险", max_digits=10, decimal_places=2, default=0)
    medical_insurance = models.DecimalField(verbose_name="医疗保险", max_digits=10, decimal_places=2, default=0)
    unemployment_insurance = models.DecimalField(verbose_name="失业保险", max_digits=10, decimal_places=2, default=0)
    housing_fund = models.DecimalField(verbose_name="公积金", max_digits=10, decimal_places=2, default=0)

    # 个人所得税
    tax = models.DecimalField(verbose_name="个人所得税", max_digits=10, decimal_places=2, default=0)
    final_salary = models.DecimalField(verbose_name="实发工资", max_digits=10, decimal_places=2, default=0)

    salary_month = models.DateField(verbose_name="工资月份")

    def save(self, *args, **kwargs):
        """自动计算工资"""
        total_deductions = self.late_penalty + self.pension + self.medical_insurance + self.unemployment_insurance + self.housing_fund + self.tax
        total_earnings = self.base_salary + self.performance_bonus + self.year_end_bonus
        self.final_salary = total_earnings - total_deductions
        super().save(*args, **kwargs)

    class Meta:
        db_table = "app01_salary"
        verbose_name = "工资记录"
        verbose_name_plural = "工资记录"


"""class ResignRequest(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="申请人")
    reason = models.TextField(verbose_name="离职原因")
    submit_date = models.DateField(auto_now_add=True, verbose_name="提交日期")
    status = models.CharField(max_length=20, default='pending', verbose_name='状态')"""


class ResignRequest(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="申请人")
    reason = models.TextField(verbose_name="离职原因")
    file = models.FileField(upload_to="resign/", null=True, blank=True, verbose_name="附件")  # ✅ 新增字段
    submit_date = models.DateField(auto_now_add=True, verbose_name="提交日期")
    status = models.CharField(max_length=20, default='pending', verbose_name='状态')

    reject_reason = models.TextField(null=True, blank=True, verbose_name='拒绝理由')  # 添加拒绝理由字段

    def __str__(self):
        return f"{self.user.name} - {self.submit_date}"

class ExpenseClaim(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="申请人")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="报销金额")
    description = models.TextField(verbose_name="用途说明")
    submit_time = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")
    status = models.CharField(max_length=20, default='pending', verbose_name='状态')
    file = models.FileField(upload_to='expense_files/', blank=True, null=True, verbose_name="附件")

    def __str__(self):
        return f"{self.user.name} - {self.submit_time}"

"""class ExpenseClaim(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="申请人")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="报销金额")
    description = models.TextField(verbose_name="用途说明")
    submit_time = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")
    status = models.CharField(max_length=20, default='pending', verbose_name='状态')"""


"""此外，如果要实现各个功能板块都能成功运行，需要完成以下步骤。
具体搭建步骤：1、需要先定义数据模型（在models.py中定义相应的数据模型），
2、然后在视图函数中编写每个模块的相应视图函数进行逐步编写。
比如管理员账户管理模块实现了登录、注册、密码修改等功能；任务管理模块实现了任务的创建、编辑和删除功能。
3、开始设计html页面，前端需要给用户好的页面体验，故每个页面都extend 4.2所写的layout布局的，
导入了跑马灯和磁吸小球后页面更美观。且每个功能模块都对应了一个或多个 HTML 页面，
如 admin_list.html、job_add.html 等，这些页面通过模板继承来共享统一的布局结构。
通过 {% extends 'layout.html' %}，每个模块页面的结构都统一，避免了重复的代码，提升了开发效率和维护性。
4、路由配置url.py，就是找到相应的url路径，确保能够各个板块有效访问，
如通过 path('task/list/', views.task_list) 来访问任务列表。
5、最后就是mysql数据库迁移，迁移后终端输入python manage.py runserver
启动本地服务器后点击系统默认地址进入系统。"""