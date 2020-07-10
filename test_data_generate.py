import os, django
import time

from django.db.models import Q
import json

from django.http import JsonResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sms02.settings")  # project_name 项目名称
django.setup()
import random

from users.models import Users, Counselor, School
from financial.models import Market
from course.models import Course

# for i in range(100):
#     print('已创建',i+1,'条Users数据')
#     add = Users()
#     add.username = '蔡徐坤' + str(i) + '号'
#     add.wechat = ''
#     add.GPA = format(random.uniform(2,5),'.1f')
#     add.gender = random.choice(['w','m'])
#     # add.birth = ''
#     add.IDCard = ''
#     add.major = ''
#     add.grade = random.choice(['1','2','3','4','5'])
#     add.domesticTelephone = '1'+str(int(random.uniform(1111111111,9999999999)))
#     add.foreignTelephone = '1'+str(int(random.uniform(1111111111,9999999999)))
#     add.domesticAddress = ''
#     add.foreignAddress = ''
#     add.firstEmail = str(int(random.uniform(2111111111,9999999999)))+'@qq.com'
#     add.secondEmail = ''
#     add.product = ''
#     # add.payTime = ''
#     add.paid = int(random.uniform(250,5000))
#     add.balance = int(random.uniform(5000,20000))
#     # add.payStates = ''
#     add.reason = ''
#     add.isActive = random.choice(['new','true','true','true','true','true','true','true','true','true','true','true'])
#     add.role = random.choice(['xy','xy','xy','xy','xy','xy','xy','xy','xy','xy','xy','xy','cw','scfz','qqfz','jqfz','zs','ds'])
#     # add.counselor = counselor3
#     # add.ambassador = id11
#     # add.datetime = ''
#
#     add.save()
#     time.sleep(0.2)

# b = Users()
# b.openid = 77
# b.save()

# school_list = ['阿尔伯塔大学', '阿萨巴斯卡大学', '卡尔加里大学', '莱斯桥大学', '加拿大皇家大学', '西蒙佛蕾泽大学', '不列颠哥伦比亚大学', '北哥伦比亚大学', '维多利亚大学', '布兰顿大学',
#         '曼尼托巴大学', '温尼伯大学', '艾里森山大学', '圣托玛斯大学', '曼克顿大学', '新布朗斯维克大学', '纽芬兰纪念大学', '阿卡迪亚大学', '戴尔豪斯大学', '圣温森特山大学', '圣安娜大学',
#         '圣法兰西斯-萨维尔大学', '圣玛莉大学', '布兰顿大学学院', '布鲁克大学', '卡尔顿大学', '湖岸大学', '劳伦特大学', '麦克马斯特大学', '尼波星大学', '女王大学', '怀雅逊大学',
#         '特莱特大学', '圭尔夫大学', '渥太华大学', '多伦多大学', '滑铁卢大学', '西安大略大学', '温莎大学', '韦尔福瑞德-劳瑞大学', '约克大学', '爱德华王子岛大学', '主教大学', '协和大学',
#         '拉瓦尔大学', '麦吉尔大学', '蒙特利尔大学', '魁北克大学', '魁北克大学校本部', '魁北克大学蒙特利尔分校', '魁北克大学特瓦河分校', '魁北克大学史库蒂密分校', '魁北克大学瑞姆斯基分校',
#         '施尔布鲁克大学', '里贾纳大学', '萨斯卡彻温大学']
#
#
# for i in school_list:
#         print('已创建', i)
#         market = Market.objects.get(id=3)
#         add = School()
#         add.s_name = i
#         add.func = 'zs'
#         add.market = market
#         add.save()
#         time.sleep(0.2)

add = Users()
add.openid = 3
add.save()