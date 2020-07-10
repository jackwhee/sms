import hmac
import time
import uuid

from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect
from rest_framework import views
from rest_framework import response
import smtplib
from email.mime.text import MIMEText
from email.header import Header
# from collections import Counter

from .serializer import UserSerializer,CUSSerializer,CourseSerializer,SubjectSerializer
from moodle.models import MoodleUser,EmailCode,MoodleCourse,MoodleSubject
from tool.token import make_token, check_token

# ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ 基础设置 ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼

mail_host = "smtp.exmail.qq.com"  # 设置服务器
mail_user = "ruhan@canadasummer.ca"  # SMTP邮箱用户名
mail_pass = "377137470Tu"  # SMTP邮箱口令
salt = b'cso_canada_summer'  # 密码盐


class Role:
    '''
    权限等级
    现有权限等级(将新增 role 字段放入对应等级列表中):
        普通权限 PermissionsL : 仅可获取自己(token中对应的)obj对象数据
        I级权限 PermissionsI : 可获取任意指定对象数据
    '''

    def __init__(self):
        self.PermissionsL = ['stu']
        self.PermissionsI = ['prof']
        # self.PermissionsII = []
        # self.PermissionsIII = []


# ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ 基础设置 ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲

pass


# ▼ --------------------------------------- ▼  user_views  ▼ --------------------------------------- ▼

class EmailAuth(views.APIView):
    '''
    邮箱验证
    '''

    def get(self, request, m_ac):

        E_code = str(uuid.uuid4())[0:6:1]

        receivers = [f'{m_ac}']  # 接收邮件
        title = 'CSO暑期课程平台验证码'
        email_msg = f'''
            <div>
                <p style="text-align: center;line-height: 45px;border: 3px solid #2c333b;margin: 0;color: white;background-color: #0066b9;">CSO国际暑校</p>
            </div>
            <div style="background-color: #2c333b;height: 100vh;padding: 10px 50px;color: white;">
                <p style="font-size: 30px;">这是您的验证码:</p>
                <p style="color: #0066b9;font-size: 30px;font-weight: 700;">{E_code}</p>
                <p>这个验证码会在<span style="font-weight: 700;"> 10分钟后 </span>过期</p>
                <br>
                <p>您好CSO网课平台用户!</p>
                <p>我们收到一个来自您的注册请求,请将这个验证码输入在<span style="font-weight: 700;"> "CSO课程平台注册" </span>页面的对话栏中</p>
                <p>享受您的自由学习生活!</p>
            </div>
        '''

        message = MIMEText(email_msg, 'html', 'utf-8')
        message['From'] = "CSO<ruhan@canadasummer.ca>"
        message['To'] = "CSO用户<{}>".format(m_ac)

        message['Subject'] = Header(title, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(mail_user, receivers, message.as_string())
            smtpObj.quit()

            try:
                obj = EmailCode.objects.get(Email=m_ac)
                obj.E_code = E_code
                obj.E_time = time.time()
                obj.save()
            except:
                EmailCode.objects.create(Email=m_ac, E_code=E_code)

            return response.Response({
                'code': 200,
                'data': E_code
            })
        except Exception as e:
            print('----------------->邮件发送失败报错:', e)

            return response.Response({
                'code': 40406,
                'data': '验证码发送失败'
            })

    # def post(self,request,m_ac):
    #
    #     print(Role().PermissionsI)


class MoodleUsersMsg(views.APIView):
    '''
    所有用户/注册
    '''

    @check_token
    def get(self, request):
        role = request.role

        # 普通权限
        if role in Role().PermissionsL:
            serializer = UserSerializer(instance=request.user_obj)
            return response.Response({
                'code': 200,
                'data': serializer.data
            })

        # I级权限
        elif role in Role().PermissionsI:
            q_set = MoodleUser.objects.all()
            serializer = UserSerializer(instance=q_set, many=True)
            return response.Response({
                'code': 200,
                'data': serializer.data
            })

    def post(self, request):
        '''
        注册
        :param request:
        :return:
        '''

        # json格式检查
        try:
            account = request.data['m_ac']
            password = request.data['m_ps']
            E_code = request.data['E_code']
        except:
            return response.Response({
                'code': 40407,
                'data': 'json参数有误'
            })

        # 查重
        try:
            MoodleUser.objects.get(m_ac=account)
            return response.Response({
                'code': 40401,
                'data': '该账户已存在,无法注册'
            })
        except:
            pass

        # 验证码验证
        try:
            E_obj = EmailCode.objects.get(Email=account)
            E_time = E_obj.E_time
            interval = float(time.time() - float(E_time))
            # 超时验证 10min
            if interval > 600:
                return response.Response({
                    'code': 40409,
                    'data': '验证码已失效'
                })

            # 验证码相同 进行注册
            if E_code == E_obj.E_code:
                h = hmac.new(salt, password.encode(), digestmod='sha256')
                m_ps_h = h.hexdigest()

                new_data = {
                    'm_ac': account,
                    'm_ps': m_ps_h
                }

                serializer = UserSerializer(data=new_data)
                if serializer.is_valid():
                    q_obj = serializer.save()

                    # 生成token
                    token = make_token(m_ac_id=q_obj.pk)

                    return response.Response({
                        'code': 200,
                        'data': {'token': token.decode()}
                    })
                else:
                    return response.Response({
                        'code': 40402,
                        'data': serializer.errors
                    })

            # 验证码不相同
            else:
                return response.Response({
                    'code': 40410,
                    'data': '验证码错误'
                })

        except:
            # 数据库无当前用户验证码数据
            return response.Response({
                'code': 40408,
                'data': '未获取验证码'
            })


class Login(views.APIView):
    '''
    用户登录
    '''

    def post(self, request):

        # json格式检查
        try:
            password = request.data['m_ps']
            account = request.data['m_ac']
        except:
            return response.Response({
                'code': 40413,
                'data': 'json参数有误'
            })

        # 数据库查询
        try:
            user_obj = MoodleUser.objects.get(m_ac=account)
            h = hmac.new(salt, password.encode(), digestmod='sha256')
            m_ps_h = h.hexdigest()

            # 密码比对
            if user_obj.m_ps == m_ps_h:
                token = make_token(m_ac_id=user_obj.pk)
                return response.Response({
                    'code': 200,
                    'data': {'token': token.decode()}
                })

            else:
                return response.Response({
                    'code': 40414,
                    'data': '密码错误'
                })

        except Exception as e:
            print(e)
            return response.Response({
                'code': 40415,
                'data': '你要登陆的用户不存在'
            })


class MoodleUserMsg(views.APIView):
    '''
    指定用户
    '''

    @check_token
    def get(self, request, pk=None):
        role = request.role

        # 普通权限或无查询字串
        if (role in Role().PermissionsL) or (pk == None):
            serializer = UserSerializer(instance=request.user_obj)
            return response.Response({
                'code': 200,
                'data': serializer.data
            })

        # I级权限
        elif role in Role().PermissionsI:
            try:
                q_obj = MoodleUser.objects.get(id=pk)
            except:
                return response.Response({
                    'code': 40412,
                    'data': '你要查询的用户不存在'
                })
            serializer = UserSerializer(instance=q_obj)
            return response.Response({
                'code': 200,
                'data': serializer.data
            })

    @check_token
    def put(self, request, pk=None):
        role = request.role

        # 普通权限或无查询字串
        if (role in Role().PermissionsL) or (pk == None):
            serializer = UserSerializer(instance=request.user_obj, data=request.data)
            if serializer.is_valid():
                _q_obj = serializer.save()
                return response.Response({
                    'code': 200,
                    'data': _q_obj.pk
                })
            else:
                return response.Response({
                    'code': 40404,
                    'data': serializer.errors
                })

        # I级权限
        elif role in Role().PermissionsI:
            try:
                q_obj = MoodleUser.objects.get(id=pk)
            except:
                return response.Response({
                    'code': 40403,
                    'data': '你要修改的用户不存在'
                })

            serializer = UserSerializer(instance=q_obj, data=request.data)
            if serializer.is_valid():
                _q_obj = serializer.save()
                return response.Response({
                    'code': 200,
                    'data': _q_obj.pk
                })
            else:
                return response.Response({
                    'code': 40404,
                    'data': serializer.errors
                })

    # def delete(self,request,m_ac):
    #     try:
    #         q_obj = Moodle.objects.get(m_account=m_ac)
    #     except:
    #         return response.Response({
    #             'code': 40405,
    #             'data': '你要删除的用户不存在'
    #         })
    #
    #     q_obj.delete()
    #     return response.Response({
    #         'code':200,
    #         'data':'删除成功'
    #     })

# ▲ --------------------------------------- ▲  user_views  ▲ --------------------------------------- ▲
pass


# ▼ --------------------------------------- ▼ course_views ▼ --------------------------------------- ▼

class MoodleLearnData(views.APIView):
    '''
    用户学习数据
    '''

    @check_token
    def put(self,request,judge):

        #获取CUS对象
        try:
            course = int(request.data['course'])
            json_data = request.data['data']
            CUS_obj = request.user_obj.m_cus.get(moodle_course=course)
        except:
            return response.Response({
                'code':40417,
                'data':'json参数有误'
            })

        #修改用户观看视频时长
        if judge == 'time':
            # 重写data
            time = int(json_data) + CUS_obj.time
            data = {
                'time': time
            }

            serializer = CUSSerializer(instance=CUS_obj,data=data)
            if serializer.is_valid():
                serializer.save()
                return response.Response({
                    'code': 200,
                    'data': 'OK'
                })
            else:
                return response.Response({
                    'code': 40416,
                    'data': serializer.errors
                })

        #修改用户观看视频进度
        elif judge == 'progress':

            video_num = len(CUS_obj.moodle_course.m_video.all())
            data_progress = int(json_data) / video_num
            if data_progress > 1:
                return response.Response({
                    'code':40418,
                    'data':'data值不在范围内'
                })
            print(video_num , data_progress)

            if data_progress <= CUS_obj.progress:
                return response.Response({
                    'code':200,
                    'data':'PASS'
                })

            else:
                # 重写data
                data = {
                    'progress': data_progress
                }

                serializer = CUSSerializer(instance=CUS_obj, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return response.Response({
                        'code': 200,
                        'data': 'OK'
                    })
                else:
                    return response.Response({
                        'code': 40416,
                        'data': serializer.errors
                    })

        #API不存在
        else:
            return response.Response({
                'code':404,
                'data':'API不存在'
            })


class MoodleCoursesMsg(views.APIView):
    '''
    所有课程(学科)
    '''

    @check_token
    def get(self, request):

        #获取学科查询结果集
        s_q_set = MoodleSubject.objects.all()
        #新建学科-课程列表
        sub_cou_list = []

        #遍历学科查询结果集
        for s in s_q_set:
            #序列化学科数据
            s_dic = SubjectSerializer(instance=s).data
            #序列化学科旗下课程数据
            c_dic = CourseSerializer(instance=s.m_course.all(),many=True,excludes=['subject','m_user']).data
            #学科数据中添加课程数据
            s_dic['course'] = c_dic
            #学科-课程列表中添加更改后的学科数据
            sub_cou_list.append(s_dic)



        return response.Response({
            'code':200,
            'data':sub_cou_list
        })


class MoodleCourseMsg(views.APIView):
    '''
    我的课程/指定学员的课程
    '''

    @check_token
    def get(self,request,pk=None):
        if not pk:
            user_obj = request.user_obj
            my_course = user_obj.m_course.all()

            serializer = CourseSerializer(instance=my_course,many=True)
            for i in serializer.data:
                cus_obj = user_obj.m_cus.get(moodle_course = i['id'])

                i['time'] = cus_obj.time
                i['progress'] = cus_obj.progress

            return response.Response({
                'code':200,
                'data':serializer.data
            })

        else:
            try:
                user_obj = MoodleUser.objects.get(id=pk)
            except:
                return response.Response({
                    'code': 40412,
                    'data': '你要查询的用户不存在'
                })
            my_course = user_obj.m_course.all()
            serializer = CourseSerializer(instance=my_course,many=True)
            return response.Response({
                'code': 200,
                'data': serializer.data
            })

# ▲ --------------------------------------- ▲ course_views ▲ --------------------------------------- ▲


class SB(views.APIView):
    def get(self,request):


        print(request.META['HTTP_SEC_FETCH_DEST'])

        if request.META['HTTP_SEC_FETCH_DEST'] == 'video':
            return redirect('http://s1.pstatp.com/cdn/expire-1-M/byted-player-videos/1.0.0/xgplayer-demo.mp4')
        else:
            return HttpResponse('404')
