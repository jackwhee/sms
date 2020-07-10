import datetime
import time
import jwt
# from rest_framework import response
from django.shortcuts import render

from moodle.models import MoodleUser
from users.models import Users


# ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ 基础设置 ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼

salt = 'cso_canada_summer_w'  #token盐
expire = 6  #token超时时间

# ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ 基础设置 ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲


def make_session_token(m_ac_id,expire_hour=expire):
    '''
    token生成器
    :param m_ac_id: 用户id
    :param m_ac: 用户邮箱
    :param expire_hour: 过期时间(小时)
    :return:
    '''

    playload = {
        "m_ac_id": m_ac_id,
        "iss": 'CsoCanadaSummer',
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=expire_hour),
        'iat': datetime.datetime.utcnow(),
    }

    signature = jwt.encode(playload, salt, algorithm='HS256')

    return signature


def check_session_token(func):
    '''
    token验证装饰器 进行token验证,并将token中用户对应的user_obj加入request中
    :param func: 请求函数(get/post/put/delete......)
    :return:
    '''
    def decorator(self,request,*args,**kwargs):
        try:
            # token = request.META['HTTP_AUTHORIZATION']
            # token = request.session.get('authorization')['token']
            token = request.COOKIES['token']
            res = jwt.decode(token.encode(), salt, algorithms='HS256')
            m_ac_id = res['m_ac_id']
            m_user_obj =MoodleUser.objects.get(id=m_ac_id)
            # m_user_obj = user_obj
            # print(m_user_obj)
            setattr(request,'user_obj',m_user_obj)
            setattr(request,'role',m_user_obj.role)

        except Exception as e:
            # return response.Response({
            #     'code': 40411,
            #     'data':f'{e}'
            # })
            return render(request,'moodle/login.html')

        return func(self,request,*args,**kwargs)

    return decorator