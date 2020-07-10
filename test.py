import os, django
from django.db.models import Q
import json

from django.http import JsonResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sms02.settings")  # project_name 项目名称
django.setup()
import random

from users.models import Users, Counselor, School
from course.models import Course, State

# from tool.orm_helper import objs_finder

# 外键自关联反向查询测试
# dashi1 = Users.objects.get(id = 1)
# guwen1 = Counselor.objects.get(id=1)
# user = Users()
#
# user.username = 'ceshi8'
# user.GPA = 3.2
# user.gender = 'm'
# user.role = 'xy'
# user.counselor = guwen1
# user.save()

# guwen = Counselor()
# guwen.counselor = 'zhangsan'
# guwen.telephone = '14243534352'
# guwen.save()

# user = Users.objects.get(id = 5)
# user.counselor = Counselor.objects.get(id=1)
# user.save()

# guwen_name = Counselor.objects.get(id = 1)
# all = Users.objects.filter(counselor=guwen_name , id__gt=3)
# for i in all:
# 	print(i.username,i.id)

# from django.db.models import Count
# result = Users.objects.aggregate(mycnt=Count('id'))
# print("数据记录总个数是:", result['mycnt'])
# print("result=", result)  # {"mycnt": 10}

# a1 = Users.objects.filter(isActive='new')
# print(len(a1))


# def obj_finder(fields,msg):
# 	state_obj = eval('Users.objects.filter('+fields+'=\''+msg+'\''+')')
# 	return state_obj
# print(obj_finder('id','1'))


# guwen_name = Counselor.objects.get(id=1)


#
#
# def json_data_generate(*args, **kwargs):
# 	# 遍历查询条件并拼接
# 	conditions = ''
# 	print(args[0])
# 	for con in args:
# 		# print(con)
# 		conditions += con
# 		conditions += ','
#
# 	# 遍历data结构并拼接成字典
# 	key = ''
# 	value = ''
# 	for data in kwargs:
# 		if kwargs[data] == 0:
# 			# 值为0 放入key
# 			key += '+str(stu_obj.{})'.format(data)
# 			key += '+\' \''
# 			print(key)
# 		if kwargs[data] == 1:
# 			# 值为1 放入value
# 			value += '+str(stu_obj.{})'.format(data)
# 			value += '+\' \''
# 			print(value)


# data = {}
# obj_list = eval('Users.objects.filter(' + conditions + ')')
# for stu_obj in obj_list:
# 	eval('data.update({' + key[1:] + ':' + value[1:] + '})')
# return data

# json_data_generate("isActive='new',id='1'", username=0, school=0, payTime=1)


# print(json_data_generate("isActive='new',id='1'", username=0, school=0, payTime=1))


# school = School.objects.get(id=1)
#
# wrhan = Users.objects.get(id=1)
# wrhan.school = school
# wrhan.save()


# def data_generate(condition, *args):
# 	'''
# 	根据 任意查询条件 输出data
#
# 	:param condition: 查询条件 ( 根据 表字段 选定符合要求的 数据对象 )
# 				      必须为 字符串格式 的 完整 ORM 查询语句 如 "username = 'WRhan'"
# 				      可设置多个查询条件 用逗号隔开 如 "username = 'WRhan', gender='m', id__lt='5'"
# 				      若外键反查 ( 查询条件是一个obj对象时 ) 不加单引号
# 				      如"counselor=guwen_name" ( 查询当前学习顾问负责多少学员 )
#
# 	:param args: 查询条件 ( 根据 表字段 取出相应的值 )
# 				 如 'payTime','id','GPA'
# 				 args 最少得传一个
#
# 	:return: 当根据 condition 选定的对象只有一个时 ,返回当前对象的数据字典
# 			 e.g: {'username': 'wrhan', 'id': '1', 'GPA': '3.7'}
#
# 			 当根据 condition 选定的对象有多个时 , 返回一个由多个对象字典组成的列表
# 			 e.g: [{'username': 'wrhan', 'id': '1', 'GPA': '3.7'}, {'username': 'haha', 'id': '2', 'GPA': '3.7'}]
# 	'''
# 	obj_list = eval("Users.objects.filter("+condition+")")
# 	if len(obj_list) !=1:
# 		data = []
#
# 		for stu_obj in obj_list:
# 			dic = {}
# 			for con in args:
# 				dic[con] = eval('str(stu_obj.'+con+')')
# 			data.append(dic)
#
# 		return data
# 	else:
# 		dic = {}
# 		for con in args:
# 			dic[con] = eval('str(obj_list[0].' + con+')')
# 			# dic[con] = str(obj_list[0].payTime)
# 		# print(obj_list[0].payTime)
# 		return dic
#
#
# print(data_generate("isActive='new',id__lt=3",'username','id','GPA'))

# a = {'data':[{'name':'xxx','age':12},{'name':'xdf','age':14},{'name':'wwx','age':11},{'name':'aa','age':16}]}
#
# print(json.dumps(a))


# def request_data_generate(request, condition, key):
# 	value = request.GET[key].split(' ')
# 	obj_list = eval("Users.objects.filter(" + condition + ")")
# 	if len(obj_list) != 1:
# 		data = []
#
# 		for stu_obj in obj_list:
# 			dic = {}
# 			for con in value:
# 				dic[con] = eval('str(stu_obj.' + con + ')')
# 			data.append(dic)
#
# 		return data
# 	else:
# 		if value[0] == 'base':
# 			dic = {
# 				'username': obj_list[0].username,
# 				'gender': obj_list[0].gender,
# 				'GPA': obj_list[0].GPA,
# 				'birth': obj_list[0].birth,
# 				'IDCard': obj_list[0].IDCard,
# 				'major': obj_list[0].major,
# 				'domesticTelephone': obj_list[0].domesticTelephone,
# 				'foreignTelephone': obj_list[0].foreignTelephone,
# 				'domesticAddress': obj_list[0].domesticAddress,
# 				'foreignAddress': obj_list[0].foreignAddress,
# 				'ambassador': obj_list[0].ambassador,
# 				'paid': obj_list[0].paid,
# 				'count': obj_list[0].count,
# 				'balance': obj_list[0].balance,
# 			}
# 			value = value[1:]
# 		else:
# 			dic = {}
#
# 		for con in value:
# 			dic[con] = eval('str(obj_list[0].' + con + ')')
# 		return dic

# 添加数据 ------------------------------------------------------------------------------------------------

# id11 = Users.objects.get(id=11)
# school1 = School.objects.get(id=1)
# school2 = School.objects.get(id=2)
# counselor3 = Counselor.objects.get(id=3)
# id20 = Users.objects.get(id=20)


# id20.school.add(school2)
# print(id20.school.all())

# --------------------------------------------------------------
# print(Users.objects.filter( isActive='true',counselor = None ))
# test = objs_finder("id = 4.9 ")
# print(test)


# ----------------------------搜索------------------------------
# a = 2
# b = 5
# c = '3'
# d = '2.5'
# e = 3.8
# f = 'sds'

# print(type(c))

# users = Users.objects.filter(Q(username__icontains='c') | Q(domesticTelephone__icontains=687))


# print(users)


# def search_data_generate(databases, search_msg, conditions):
#     if type(conditions) is str:
#         base = databases + ".objects.filter(Q({}__icontains={})".format(conditions, search_msg)
#     else:
#         base = databases + ".objects.filter("
#         for num, con in enumerate(conditions):
#             if num == 0:
#                 add = "Q({}__icontains={})".format(con, search_msg)
#             else:
#                 add = "|Q({}__icontains={})".format(con, search_msg)
#             base += add
#     base += ")"
#     data = eval(base)
#     data_list = []
#     # print(data)
#     for obj in data:
#         cou_wk_list = []
#         cou_wk = obj.course_set.filter(category='wk').values_list('course')
#         for cou in cou_wk:
#             cou_wk_list.append(cou[0])
#
#         cou_ms_list = []
#         cou_ms = obj.course_set.filter(category='ms').values_list('course')
#         for cou in cou_ms:
#             cou_ms_list.append(cou[0])
#
#         sch_sk_list = None
#         sch_sk = obj.school.filter(func='sk').values_list('s_name')
#         for sch in sch_sk:
#             sch_sk_list=sch[0]
#
#         data_list.append({'username': obj.username, 'firstEmail': obj.firstEmail, 'secondEmail': obj.secondEmail,
#                           'IDCard': obj.IDCard, 'school': sch_sk_list,
#                           'course_wk': cou_wk_list,'course_ms': cou_ms_list})
#     return data_list
#
#
# print(search_data_generate('Users', '1', ['domesticTelephone', 'username', 'id']))

# ------------------------------------多对多-------------------------------------------

# id1 = Users.objects.get(id=11)
# print(id1.course_set.all())
# print(id1.school.filter(func='sk'))
# # id1.school.create(s_name='武汉大学',func='sk')
#
#
# # course1 = id1.course_set.create(course='地理',category='ms')
#
#
# test = Users.objects.order_by('username')
# print(test)

# a01 = Users.objects.filter(Q(firstEmail__contains='a')|Q(secondEmail__contains='a'))
# for i in a01:
#     print(i.secondEmail,i.firstEmail)

# a = Users.objects.filter(school='2')
# print(a)

# a = School.objects.filter(func='sh').values_list("id","s_name").order_by("s_name")
# print(a)

# b = School.objects.filter(id__in=[1,2])

# a = Users.objects.filter(school=2,course=2,counselor=1).filter(school=1)
# print(a)
#
# b = State.objects.filter(Q(users__allotTime__contains='2019-08-20') & Q(users__subTime__contains='2019-08-20') & Q(
#     users__passTime__contains='2019-08-20'), state='no_sub', users__school=1, users__course=4).filter(users__school=2,
#                                                                                                       state='sub')




# res = Users.objects.get(id=1).course_set.filter(category='ms')
#
# for i in res:
#     print(i.id)

# res = Users.objects.get(id=1).state_set.filter(state='LOP')
# print(res)
# for i in res:
#     if i.course.category == 'wk':
#         print(i.course)
#
#
# a = '123214'
# print(a[0:3:1])

# id1 = Users.objects.get(id=1)
# # print(id1.feedbackTime)
# id1.feedbackTime = '2019-08-24'
# id1.save()

search = Users.objects.filter(feedbackTime__range=('2019-08-22','2019-08-29'))
# print(search)

# b = State.objects.filter(users__feedbackTime__range=('2019-08-22','2019-08-29'))
# b = State.objects.filter(users__feedbackTime='2019-08-24')
# c = Users.objects.filter(school=1,course=2,feedbackTime__range=('2019-08-22','2019-08-29'),passTime__range=('2019-08-19','2019-08-21'),LOPTime__range=('2019-08-19','2019-08-29')).filter(school__id=2)
# print(c)

# d = Users.objects.filter(Q(username__contains='sb'),Q(payTime__contains='2019-09'),payStates='sq',)
# print(d)


# for i in b:
#     print(i.users)

e = Users.objects.get(id=1)
for i in e.course_set.filter(category='ms'):
    print(i.course)