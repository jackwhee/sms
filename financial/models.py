from django.db import models
from django.utils import timezone
from users.models import Users


# Create your models here.

class Base_commission(models.Model):
    month = models.CharField(max_length=2, default='', verbose_name='月份')
    application_fee = models.IntegerField(default=0, verbose_name='申请费提成')
    month_target = models.IntegerField(default=0, verbose_name='月目标人数')
    month_complete = models.IntegerField(default=0, verbose_name='月目标完成后提成因素')
    month_unfinished = models.IntegerField(default=0, verbose_name='月目标完成前提成因素')
    quarter_target = models.IntegerField(default=0, verbose_name='季目标人数')
    quarter_complete = models.IntegerField(default=0, verbose_name='季目标完成后提成金额')

    def __str__(self):
        return self.month

    class Meta:
        db_table = 'base_commission'
        verbose_name = "基础提成信息"
        verbose_name_plural = verbose_name


class Ambassador_annual(models.Model):
    floor = models.IntegerField(default=0, verbose_name='人数范围下限')
    ceiling = models.IntegerField(default=0, verbose_name='人数范围上限')
    annual_bonus = models.IntegerField(default=0, verbose_name='年度奖金')
    discount = models.IntegerField(default=0, choices=((0, '无资格'), (1, '有资格')), verbose_name='学费减免机会')

    def __str__(self):
        return self.ceiling

    class Meta:
        db_table = 'Ambassador_annual'
        verbose_name = "大使年度奖金"
        verbose_name_plural = verbose_name


class Head_salary(models.Model):
    level = models.CharField(max_length=4, choices=(('scfz', '市场负责人'), ('qqfz', '全职区域负责人'), ('jqfz', '兼职区域负责人')),
                             default='scfz', verbose_name='负责人等级')
    base_salary = models.IntegerField(default=0, verbose_name='底薪')
    commission = models.IntegerField(default=0, verbose_name='下属分成')


    def __str__(self):
        return self.level

    class Meta:
        db_table = 'head_salary'
        verbose_name = "负责人薪资"
        verbose_name_plural = verbose_name

class Market(models.Model):
    type = models.CharField(max_length=6,choices=(('big','大市场'),('middle','中市场'),('small','小市场')),default='small',verbose_name='市场大小')
    low =  models.IntegerField(default=0, verbose_name='最低奖')
    middle = models.IntegerField(default=0, verbose_name='中档奖')
    high = models.IntegerField(default=0, verbose_name='高档奖')


    def __str__(self):
        return self.type

    class Meta:
        db_table = 'Market'
        verbose_name = "市场"
        verbose_name_plural = verbose_name

class Head_annual(models.Model):
    market = models.ForeignKey(Market,null=True,on_delete=models.SET_NULL,verbose_name='市场')
    floor = models.IntegerField(default=0, verbose_name='人数范围下限')
    ceiling = models.IntegerField(default=0, verbose_name='人数范围上限')
    Annual_bonus = models.IntegerField(default=0, verbose_name='年度奖金')


    def __str__(self):
        return self.ceiling

    class Meta:
        db_table = 'Head_annual'
        verbose_name = "负责人年度奖金"
        verbose_name_plural = verbose_name


class Salary(models.Model):
    # head = models.ForeignKey('users.Users',null=True,on_delete=models.SET_NULL,verbose_name='用户')
    ds_name = models.CharField(max_length=21, default='', verbose_name='大使姓名')
    month = models.DateField(default=timezone.now, verbose_name='提成计算时间')
    base_salary = models.IntegerField(default=0, verbose_name='底薪')
    apply_commission = models.IntegerField(default=0, verbose_name='申请费提成')
    supplement_commission = models.IntegerField(default=0, verbose_name='补缴费提成')
    all_commission = models.IntegerField(default=0, verbose_name='全款提成')
    quarter_commission = models.IntegerField(default=0, verbose_name='季度提成')
    ds_year_commission = models.IntegerField(default=0, verbose_name='大使年度提成')
    fz_year_commission = models.IntegerField(default=0, verbose_name='负责人年度奖金')
    discount = models.IntegerField(default=0,verbose_name='学费减免资格')
    underling_commission = models.IntegerField(default=0, verbose_name='下属提成')
    deduct = models.IntegerField(default=0, verbose_name='学员退款金额')

    #0则表示未完成 其他数字表示总人数与目标的差值
    task = models.IntegerField(default=0,verbose_name='当月任务是否完成')


    def __str__(self):
        return self.ds_name

    class Meta:
        db_table = 'Salary'
        verbose_name = "工资信息表"
        verbose_name_plural = verbose_name
