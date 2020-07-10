from django.db import models
from django.utils import timezone
# from financial.models import Market
import uuid
import os


# Create your models here.


class Counselor(models.Model):
    '''
    课程顾问表
    '''
    counselor = models.CharField(max_length=30, default='', verbose_name='顾问姓名')
    telephone = models.CharField(max_length=11, default='', verbose_name='顾问电话')

    def __str__(self):
        return self.counselor

    class Meta:
        db_table = 'Counselor'
        verbose_name = '课程顾问信息'
        verbose_name_plural = verbose_name


class School(models.Model):
    '''
    大学信息表
    '''
    s_name = models.CharField(max_length=60, default='', verbose_name='学校名称')
    market = models.ForeignKey('financial.Market', null=True, on_delete=models.SET_NULL, verbose_name='市场')
    func = models.CharField(max_length=2, choices=(('zs', '招生'), ('sh', '审核'), ('sk', '上课')), verbose_name='学校功能',
                            default='zs')
    qyfz = models.CharField(max_length=21, default='', verbose_name='区域负责人姓名')
    xzs = models.CharField(max_length=21, default='', verbose_name='小助手姓名')
    city = models.CharField(max_length=10, default='',null=True,blank=True, verbose_name='国家')

    def __str__(self):
        return self.s_name

    class Meta:
        db_table = 'school'
        verbose_name = "学校信息"
        verbose_name_plural = verbose_name


# 凭证图片上传动态路径
def voucher_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

    # pic_path = os.path.abspath('../media/{}/{}'.format(instance.id,filename))
    # print(pic_path)
    # if 'voucher.jpg' in os.listdir('./media/{}/voucher'.format(instance.id)):
    #     os.remove('./media/{}/voucher/voucher.jpg'.format(instance.id))
    # else:
    #     pass
    # return the whole path to the file
    return os.path.join(str(instance.id), "voucher", filename)


# 身份证图片上传动态路径
def card_path(instance, filename):
    # print(instance)
    # print(filename)
    try:
        # print(2.1)
        list_path = os.listdir('./media/{}/card_img'.format(instance.id))
        # print(list_path)
        if not list_path:
            filename = 'face.jpg'
        elif list_path == ['face.jpg']:
            filename = 'reverse.jpg'
        elif list_path == ['reverse.jpg']:
            filename = 'face.jpg'
        else:
            return
    except:
        # print(2.2)
        filename = 'face.jpg'
    # return the whole path to the file

    return os.path.join(str(instance.id), "card_img", filename)

# LOP凭证上传动态路径
def LOP_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file

    return os.path.join(str(instance.id), "LOP_img", filename)
# def LOP_path(instance, filename):
#     list_path = os.listdir('./media/{}/LOP_img'.format(instance.id))
#     print(list_path)
#     if not list_path:
#         filename = 'face.jpg'
#     elif list_path == ['face.jpg']:
#         filename = 'reverse.jpg'
#     elif list_path == ['reverse.jpg']:
#         filename = 'face.jpg'
#     else:
#         return
#     # return the whole path to the file
#
#     return os.path.join(str(instance.id), "LOP_img", filename)

# GPA凭证上传动态路径
def GPA_path(instance, filename):
    # try:
    #     list_path = os.listdir('./media/{}/GPA_img'.format(instance.id))
    #     # print(list_path)
    #     if not list_path:
    #         filename = 'GPA.jpg'
    #     else:
    #         return
    # except:
    #     filename = 'GPA.jpg'
    # return the whole path to the file

    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file

    return os.path.join(str(instance.id), "GPA_img", filename)

    # return os.path.join(str(instance.id), "GPA_img", filename)





class Users(models.Model):
    '''
    学员/大使/财务/小助手 用户信息
    '''

    # 必填 openid 权限认证的依据
    openid = models.CharField(max_length=128,default='', verbose_name='openid')
    webopenid = models.CharField(max_length=128,default='', verbose_name='webopenid')
    stu_num = models.CharField(max_length=7, default='',verbose_name='学号')

    # 学员提交信息
    username = models.CharField(max_length=21, default='', verbose_name='姓名')
    pinyin = models.CharField(max_length=50, default='', verbose_name='姓名拼音')
    wechat = models.CharField(max_length=50, default='', verbose_name='微信号')
    GPA = models.CharField(max_length=5,default='', verbose_name='GPA')
    gender = models.CharField(max_length=1, choices=(('w', '女'), ('m', '男')), default='w', verbose_name='性别')
    birth = models.DateField(default=timezone.now, verbose_name='出生年月')
    IDCard = models.CharField(max_length=20, default='', verbose_name='身份证号')
    major = models.CharField(max_length=90, default='', verbose_name='专业')
    grade = models.CharField(max_length=30, default='', verbose_name='年级')
    domesticTelephone = models.CharField(max_length=11, default='', verbose_name='电话（国内）')
    foreignTelephone = models.CharField(max_length=30, default='', verbose_name='电话（国外）')
    domesticAddress = models.CharField(max_length=120, default='', verbose_name='地址（国内）')
    foreignAddress = models.CharField(max_length=120, default='', verbose_name='地址（国外）')
    firstEmail = models.EmailField(default='', verbose_name='邮件一')
    secondEmail = models.EmailField(default='', verbose_name='邮件二')
    product = models.CharField(max_length=30, default='', verbose_name='选择产品')

    # 财务提交信息
    count_wk = models.CharField(max_length=1,
                                choices=(('0', '0门'), ('1', '1门'), ('2', '2门'), ('3', '3门'), ('4', '4门'), ('5', '5门')),
                                default='0', verbose_name='网课门数')

    count_ms = models.CharField(max_length=1,
                                choices=(('0', '0门'), ('1', '1门'), ('2', '2门'), ('3', '3门'), ('4', '4门'), ('5', '5门')),
                                default='0', verbose_name='面授门数')

    paid = models.FloatField(default=0, verbose_name='已缴金额')
    balance = models.FloatField(default=0, verbose_name='剩余金额')
    currency = models.CharField(max_length=3, choices=(('人民币', '人民币'), ('加币', '加币')), default='加币', verbose_name='币种')

    payStates = models.CharField(
        max_length=2, choices=(('sq', '缴申请费'), ('bq', '补齐缴费'), ('qe', '全额缴费'), ('yt', '已退费')),
        default='', verbose_name='缴费状态')
    reason = models.TextField(verbose_name='处理消息', default='')
    isActive = models.CharField(max_length=6,
                                choices=(('new', '新学员'), ('update', '更新'), ('true', '已认证'), ('nds', '新大使申请'), ('refund', '申请退费'),
                                         ('false', '注销/驳回')), null=True, verbose_name='账户状态')
    role = models.CharField(max_length=4,
                            choices=(
                                ('xy', '学员'), ('ds', '大使'), ('scfz', '市场负责人'), ('qqfz', '全职区域负责人'), ('jqfz', '兼职区域负责人'),
                                ('cw', '财务'), ('zs', '小助手')), null=True, verbose_name='用户权限')
    counselor = models.ForeignKey(Counselor, null=True, verbose_name='课程顾问', on_delete=models.SET_NULL)
    ambassador = models.ForeignKey('self', null=True, verbose_name='大使', on_delete=models.SET_NULL , related_name='qxxy')
    school = models.ManyToManyField(School, null=True, verbose_name='学校')
    positive = models.CharField(max_length=1,choices=(('1','已转正'),('0','未转正')),default='0',verbose_name='是否转正')

    # 时间
    pay_sq_time = models.DateField(null=True,default=None, verbose_name='缴费申请费日期')
    pay_bq_time = models.DateField(null=True,default=None, verbose_name='补齐学费日期')
    pay_qe_time = models.DateField(null=True,default=None, verbose_name='缴费全款日期')
    refund_time = models.DateField(null=True,default=None, verbose_name='退费日期')
    allotTime = models.DateField(null=True,default=None, verbose_name='分配时间')  # 分配顾问的时间
    feedbackTime = models.DateField(null=True,default=None, verbose_name='反馈时间')  # 顾问反馈需要选哪些课的时间
    subTime = models.DateField(null=True,default=None, verbose_name='提交时间')  # 选完课提交的时间
    passTime = models.DateField(null=True,default=None, verbose_name='通过时间')  # 通过时间
    LOPTime = models.DateField(null=True,default=None, verbose_name='LOP通过时间')  # LOP通过时间
    study = models.DateField(null=True,default=None, verbose_name='签证到期时间')  # 签证到期时间
    tb_time = models.DateField(null=True,default=None,verbose_name='学生填表时间')

    single = models.CharField(max_length=1,choices=((1,'以获得'),(0,'未获得')),default=0,verbose_name='一次性奖金50刀')


    # 图片
    voucher = models.ImageField(default='', upload_to=voucher_path, verbose_name='凭证图片')
    card_img = models.ImageField(default='', upload_to=card_path, verbose_name='身份证图片')
    LOP_img = models.ImageField(default='', upload_to=LOP_path, verbose_name='LOP凭证图片')
    GPA_img = models.ImageField(default='', upload_to=GPA_path, verbose_name='GPA凭证图片')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


class Assistant(models.Model):
    # primary_key 默认为不可修改
    ast_name = models.CharField('用户名', max_length=30)
    password = models.CharField('密码', max_length=40)

    def __str__(self):
        return self.ast_name

    class Meta:
        db_table = 'assistant'
        verbose_name = "小助手"
        verbose_name_plural = verbose_name
