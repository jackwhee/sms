import os
import time,datetime
import uuid

from django.db import models
from users.models import Users

# ▼ --------------------------------------- ▼  user_models  ▼ --------------------------------------- ▼


def avatar_path(instance, filename):
    '''
    用户头像路径
    '''

    user_m_ac = instance.m_ac
    ext = filename.split('.')[-1]
    _filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

    return os.path.join('MOODLE','m_users', user_m_ac,'avater', _filename)



def exam_subject_path(instance, filename):
    '''
    考试题目路径
    '''
    # ext = filename.split('.')[-1]
    # _filename = 'exam_subject.{}'.format(ext)

    course_name = instance.moodle_course.c_name[0:6:1]
    subject_name = instance.moodle_course.subject.s_name

    # try:
    #     # 去重
    #     list_path = os.listdir(os.path.join('media','MOODLE','m_subject',subject_name,'course_msg',course_name,'exam_subject'))
    #     if _filename in list_path:
    #         os.remove(os.path.join('media', 'MOODLE','m_subject',subject_name,'course_msg',course_name,'exam_subject', _filename))
    # except:
    #     pass

    return os.path.join('MOODLE', 'm_subject', subject_name, 'course_msg', course_name, 'exam_subject', filename)


def exam_answer_path(instance, filename):
    '''
    我的答卷路径
    '''

    # ext = filename.split('.')[-1]
    # _filename = 'exam_answer.{}'.format(ext)

    user_m_ac = instance.moodle_user.m_ac
    course_name = instance.moodle_course.c_name[0:6:1]
    exam_name = instance.exam_name

    # try:
    #     # 去重
    #     list_path = os.listdir(os.path.join('media','MOODLE','m_users',user_m_ac,'course',course_name,exam_name))
    #     if _filename in list_path:
    #         os.remove(os.path.join('media','MOODLE','m_users',user_m_ac,'course',course_name,exam_name,_filename))
    # except:
    #     pass

    return os.path.join('MOODLE', 'm_users', user_m_ac, 'course', course_name, exam_name, filename)


def exam_results_path(instance, filename):
    '''
    已批阅试卷
    '''

    # ext = filename.split('.')[-1]
    # _filename = 'exam_results.{}'.format(ext)

    user_m_ac = instance.moodle_user.m_ac
    course_name = instance.moodle_course.c_name[0:6:1]
    exam_name = instance.exam_name

    # try:
    #     # 去重
    #     list_path = os.listdir(os.path.join('media','MOODLE','m_users',user_m_ac,'course',course_name,exam_name))
    #     if _filename in list_path:
    #         os.remove(os.path.join('media','MOODLE','m_users',user_m_ac,'course',course_name,exam_name,_filename))
    # except:
    #     pass

    return os.path.join('MOODLE', 'm_users', user_m_ac, 'course', course_name, exam_name, filename)


# # # # # # # # # # # # # # ▲ 路径方法 ▲ ▼ CRM ▼ # # # # # # # # # # # #


class MoodleUser(models.Model):
    '''
    moodle 用户信息表
    '''

    m_ac = models.EmailField('moodle账号(邮箱格式)', max_length=50, null=True, blank=True)
    m_ps = models.CharField('moodle密码(请勿修改)', max_length=64, null=True, blank=True,default='76d9b3a77dc74acb189f7526b04c9794ced8efc63cf9e0de5ba22ccdd07b0316')
    nick = models.CharField('姓名', max_length=100, default='CSO')
    reg_time = models.DateTimeField('注册时间', auto_now_add=True)
    info = models.TextField("介绍(教授必须填写,学生可以不填)", null=True, blank=True)
    role = models.CharField('身份', choices=(('stu', '学员'), ('prof', '教授')), max_length=7, default='stu')
    avatar = models.ImageField('头像(教授必须上传,学生可以不传)', null=True, blank=True, upload_to=avatar_path)

    users = models.OneToOneField(Users, null=True, on_delete=models.SET_NULL, verbose_name='小程序数据(教授/未注册小程序学员可不填)', blank=True)

    address = models.CharField('寄送地址(教授无需填写)', null=True, blank=True, max_length=255, default="")
    number = models.CharField('订单号(教授无需填写)', null=True, blank=True, max_length=100, default="")
    date = models.CharField('寄送时间(教授无需填写)', null=True, blank=True, max_length=50, default="")

    # active_date = models.CharField('到期时间', null=True, blank=True, max_length=100,default='2000-01-01 00:00:00')

    active_date = models.DateTimeField('到期时间', null=True, blank=True, default=datetime.datetime.strptime('3000-01-01 00:00:00', "%Y-%m-%d %H:%M:%S"))

    def __str__(self):
        return '{} | {} | {}'.format(self.role,self.nick,self.m_ac)

    class Meta:
        db_table = 'moodle_user'
        verbose_name = "01. Moodle用户"
        verbose_name_plural = verbose_name

    # def getAllscore(self, course):
    #     return self.m_exam_stu.filter(moodle_course=course)

    def getAllscore(self):
        return self.m_exam_stu.all()


class EmailCode(models.Model):
    '''
    邮箱验证码表
    '''

    Email = models.EmailField('邮箱', max_length=50)
    E_code = models.CharField('验证码', max_length=6)
    E_time = models.CharField('验证码生成时间', max_length=30, default=time.time())

    def __str__(self):
        return 'M用户 | {}的验证码'.format(self.Email)

    class Meta:
        db_table = 'email_code'
        verbose_name = "验证码信息"
        verbose_name_plural = verbose_name


class MoodleExam(models.Model):
    '''
    考试表
    '''
    exam_name = models.CharField('考试名称', max_length=100)
    moodle_user = models.ForeignKey(MoodleUser, on_delete=models.SET_NULL, null=True, verbose_name='moodle用户', related_name='m_exam')
    moodle_course = models.ForeignKey('MoodleCourse', on_delete=models.SET_NULL, null=True, verbose_name='moodle课程', related_name='m_exam')
    exam_type = models.CharField('考试类型',choices=(('online', '在线'), ('offline', '离线')),default='online',max_length=7)
    exam_subject = models.FileField('考试题目文件', null=True, blank=True, upload_to=exam_subject_path)
    start_time = models.DateTimeField('开始时间（该时间必须小于结束时间）', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    rate = models.IntegerField("考试成绩占比（%）", default=0)

    def __str__(self):
        return '{}的{}课考试'.format(self.moodle_user, self.moodle_course)

    class Meta:
        db_table = 'moodle_exam'
        verbose_name = "07. Moodle考试表"
        verbose_name_plural = verbose_name


class MoodleExamStu(models.Model):
    '''
    学生考试表
    '''
    exam_name = models.CharField('考试名称', max_length=100)
    moodle_user = models.ForeignKey(MoodleUser, on_delete=models.SET_NULL, null=True, verbose_name='moodle用户', related_name='m_exam_stu')
    moodle_course = models.ForeignKey('MoodleCourse', on_delete=models.SET_NULL, null=True, verbose_name='moodle课程', related_name='m_exam_stu')
    exam_answer = models.FileField('我的答卷(旧)/离线考试不变', null=True, blank=True, upload_to=exam_answer_path)
    exam_results = models.FileField('我的已批改试卷', null=True, blank=True, upload_to=exam_results_path)
    content = models.TextField('我的答卷(新)',null=True, blank=True)
    exam_score = models.FloatField('我的分数', null=True, blank=True)

    def __str__(self):
        return '{}的{}课考试'.format(self.moodle_user, self.moodle_course)

    class Meta:
        db_table = 'moodle_exam_stu'
        verbose_name = "08. Moodle学生答卷表"
        verbose_name_plural = verbose_name


class Linshi(models.Model):
    '''
    临时保存考卷
    '''
    exam_name = models.CharField('考试名称', max_length=100)
    moodle_user = models.ForeignKey(MoodleUser, on_delete=models.SET_NULL, null=True, verbose_name='moodle用户', related_name='m_linshi_stu')
    moodle_course = models.ForeignKey('MoodleCourse', on_delete=models.SET_NULL, null=True, verbose_name='moodle课程', related_name='m_linshi_stu')
    content = models.TextField('内容',null=True, blank=True)
    number = models.IntegerField('个数',null=True, blank=True)

    def __str__(self):
        return '{}的{}课考试临时保存'.format(self.moodle_user, self.moodle_course)

    class Meta:
        db_table = 'moodle_exam_linshi'
        verbose_name = '10.Moodle临时保存表'
        verbose_name_plural = verbose_name



# ▲ --------------------------------------- ▲  user_models  ▲ --------------------------------------- ▲
pass


# ▼ --------------------------------------- ▼ course_models ▼ --------------------------------------- ▼


def index_img_path(instance, filename):
    '''
    首页活动图片路径
    '''
    return os.path.join('MOODLE','index', filename)


def file_path(instance, filename):
    '''
    课件文件路径
    '''



    course_name = instance.moodle_course.c_name[0:6:1]
    subject_name = instance.moodle_course.subject.s_name

    # print('--------------------------------------------------',os.path.join('MOODLE','m_subject',subject_name,'course_msg',course_name,'courseware', filename))


    # ext = filename.split('.')[-1]
    # _filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

    return os.path.join('MOODLE','m_subject',subject_name,'course_msg',course_name,'courseware', filename)


def sub_img_path(instance, filename):
    '''
    学科图片路径
    '''
    subject_name = instance.s_name
    ext = filename.split('.')[-1]
    _filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

    return os.path.join('MOODLE','m_subject', subject_name,'subject_img', _filename)


def cour_img_path(instance, filename):
    '''
    课程图片路径
    '''
    course_name = instance.c_name
    subject_name = instance.subject.s_name
    ext = filename.split('.')[-1]
    _filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

    return os.path.join('MOODLE','m_subject', subject_name,'course_msg',course_name,'course_img', _filename)


# # # # # # # # # # # # # # ▲ 路径方法 ▲ ▼ CRM ▼ # # # # # # # # # # # #


class MoodleSubject(models.Model):
    '''
    学科分类表
    '''

    s_name = models.CharField('学科名称', max_length=50)
    sub_img = models.ImageField('学科图片', null=True, blank=True, upload_to=sub_img_path)

    def __str__(self):
        return 'M学科分类 | {}'.format(self.s_name)

    class Meta:
        db_table = 'moodle_subject'
        verbose_name = "03. Moodle学科分类"
        verbose_name_plural = verbose_name


class MoodleCourse(models.Model):
    '''
    课程表
    '''

    c_name = models.CharField('课程名称', max_length=100)
    subject = models.ForeignKey(MoodleSubject, on_delete=models.SET_NULL, null=True, verbose_name='所属学科',
                                related_name='m_course')
    m_user = models.ManyToManyField(MoodleUser, verbose_name='moodle用户', through='MoodleCUS', related_name='m_course')
    cour_img = models.ImageField('课程图片', null=True, blank=True, upload_to=cour_img_path)

    info = models.TextField('课程介绍', null=True, blank=True, default="")

    video_prof = models.CharField('视频录制老师', max_length=100, null=True,blank=True ,default='')

    is_hot = models.CharField('是否为热门课程', choices=(('T', '是'), ('F', '否')), default='F', max_length=1)

    def __str__(self):
        return 'M课程 | {}'.format(self.c_name)

    class Meta:
        db_table = 'moodle_course'
        verbose_name = "04. Moodle课程"
        verbose_name_plural = verbose_name

    def getProfessor(self):
        return self.m_cus.filter(is_teach='T').first()


class MoodleCUS(models.Model):
    '''
    用户/课程中间表
    '''
    moodle_user = models.ForeignKey(MoodleUser, on_delete=models.CASCADE, blank=True, verbose_name='选择用户',
                                    related_name='m_cus')
    moodle_course = models.ForeignKey(MoodleCourse, on_delete=models.CASCADE, blank=True, verbose_name='选择课程',
                                      related_name='m_cus')
    # time = models.FloatField('播放时长', default=0)
    # progress = models.FloatField('课程进度', default=0)
    is_teach = models.CharField('是否为任课老师', choices=(('T', '是'), ('F', '否')), default='F', max_length=1)
    grade = models.FloatField('总成绩', default=0)

    def __str__(self):
        return '{}和{}'.format(self.moodle_user, self.moodle_course)

    class Meta:
        db_table = 'moodle_CUS'
        verbose_name = "02. Moodle用户-课程分配表"
        verbose_name_plural = verbose_name


class MoodleVideo(models.Model):
    '''
    课程视频
    '''
    v_name = models.CharField('视频名称 (如其中有序号请保持两位数格式如：01/02/03)', max_length=100)
    v_index = models.IntegerField('视频顺序(默认以视频名称排序 可不填写)', default=0, null=True, blank=True)
    video_add = models.CharField('视频地址',max_length=500,null=True,blank=True)
    moodle_course = models.ForeignKey(MoodleCourse, on_delete=models.SET_NULL, null=True, verbose_name='所属课程',
                               related_name='m_video')
    # msg = models.TextField('视频简介 (暂时无需填写)', null=True, blank=True, default="")

    def __str__(self):
        return 'M课程视频 | {}'.format(self.v_name)

    class Meta:
        db_table = 'moodle_video'
        verbose_name = "05. Moodle课程视频"
        verbose_name_plural = verbose_name


class MoodleCourseware(models.Model):
    '''
    课件
    '''
    cs_name = models.CharField('课件名称', max_length=50)
    file = models.FileField('课件文件', null=True, blank=True, upload_to=file_path)
    moodle_course = models.ForeignKey(MoodleCourse, on_delete=models.SET_NULL, null=True, verbose_name='所属课程',
                               related_name='m_courseware')

    def __str__(self):
        return 'M课件 | {}'.format(self.cs_name)

    class Meta:
        db_table = 'moodle_courseware'
        verbose_name = "06. Moodle课程课件"
        verbose_name_plural = verbose_name


# ▲ --------------------------------------- ▲ course_models ▲ --------------------------------------- ▲


class MoodleActive(models.Model):
    '''
    首页活动
    '''
    active_img = models.ImageField('活动图片', null=True, blank=True, upload_to=index_img_path)
    title = models.CharField('活动标题', null=True, blank=True, default='', max_length=128)
    info = models.TextField('活动内容', null=True, blank=True, default='')
    url = models.URLField('链接地址',null=True,blank=True)

    def __str__(self):
        return '活动 | {}'.format(self.title)

    class Meta:
        db_table = 'moodle_index_active'
        verbose_name = "11. Moodle首页活动"
        verbose_name_plural = verbose_name


class MoodleNotice(models.Model):
    '''
    通知
    '''
    info = models.TextField('通知内容', null=True, blank=True, default='')

    def __str__(self):
        return '通知 | {}'.format(self.id)

    class Meta:
        db_table = 'moodle_notice'
        verbose_name = "09. Moodle通知"
        verbose_name_plural = verbose_name