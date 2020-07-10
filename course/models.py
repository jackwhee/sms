from django.db import models
from users.models import Users


# Create your models here.

class Course(models.Model):
    '''
    课程表
    '''

    course = models.CharField(max_length=70, default='', verbose_name='课程名称')
    category = models.CharField(max_length=2, choices=(('wk', '网课'), ('ms', '面授')), verbose_name='课程种类',
                                default='ms')

    students = models.ManyToManyField('users.Users', null=True, verbose_name='学生', through='State')

    def __str__(self):
        return self.course

    class Meta:
        db_table = 'course'
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name


class State(models.Model):
    '''
    自定义多对多中间表 添加课程状态字段
    '''
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    users = models.ForeignKey('users.Users', on_delete=models.CASCADE)
    state = models.CharField(max_length=7, choices=(
    ('no_sub', '未提交'), ('sub', '已提交'), ('no_pass', '未通过'), ('pass', '已通过'), ('LOP', 'LOP通过')), verbose_name='课程状态',
                             default='no_sub')

    def __str__(self):
        return self.state

    class Meta:
        db_table = 'state'
        verbose_name = '课程状态'
        verbose_name_plural = verbose_name


class Tuition(models.Model):
    '''
    学费信息表
    '''

    count = models.IntegerField(default=0, verbose_name='课程门数')
    application_fee = models.IntegerField(default=0, verbose_name='申请费')
    course_fee = models.IntegerField(default=0, verbose_name='课程费')
    total_cost = models.IntegerField(default=0, verbose_name='总费用')

    def __str__(self):
        return self.total_cost

    class Meta:
        db_table = 'tuition'
        verbose_name = '学费信息'
        verbose_name_plural = verbose_name