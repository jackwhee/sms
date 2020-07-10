'''
数据库查找相关工具
'''
from django.db.models import Q

from users.models import Users, School, Counselor
from course.models import Course


def data_generate(database, condition, list_args):
    '''
    根据 任意查询条件 输出符合json格式的data

    :param database: 数据库名称 ( str )

    :param condition: 查询条件 ( 根据 表字段 选定符合要求的 查询结果集 )
                      必须为 字符串格式 的 完整 ORM 查询语句 如 "username = 'WRhan'"
                      可设置多个查询条件 用逗号隔开 如 "username = 'WRhan', gender='m', id__lt='5'"
                      若外键反查 ( 查询条件是一个obj对象时 ) 不加单引号
                      如"counselor=guwen_name" ( 查询当前学习顾问负责多少学员 )

    :param list_args: list 查询条件 ( 根据 表字段 取出相应的值 )
                 如 'payTime','id','GPA'
                 list_args 最少得传一个

    :return: 当根据 condition 选定的对象只有一个时 ,返回当前对象的数据字典
             e.g: {'username': 'wrhan', 'id': '1', 'GPA': '3.7'}

             当根据 condition 选定的对象有多个时 , 返回由多个对象字典组成的列表
             e.g: [{'username': 'wrhan', 'id': '1', 'GPA': '3.7'}, {'username': 'haha', 'id': '2', 'GPA': '3.7'}]

    e.g: 获取Users表中 状态为'new' 且 id小于3 的所有对象的 username / id / GPA
         data_generate('Users',"isActive='new',id__lt=3",'username','id','GPA')
    '''

    # 根据 condition 获取符合要求的查询结果集
    # print(database + ".objects.filter(" + condition + ")")
    obj_list = eval(database + ".objects.filter(" + condition + ")")
    # print(database + ".objects.filter(" + condition + ")")

    # 判断查询结果集个数
    if len(obj_list) != 1:

        # 有多个obj对象
        data = []
        for obj in obj_list:
            # print(obj)
            # 遍历 obj对象
            dic = {}
            # print(list_args)
            for con in list_args:
                if ('(' or ')') in con:
                    return 'CNM'
                elif 'school' in con:
                    con_list = con.split('_')
                    # print(obj_list)

                    # a = i.school.filter(func='sh')
                    # print(a)
                    results = eval("obj." + con_list[0] + ".filter(func='" + con_list[1] + "')")
                    # print("i." + con_list[0] + ".filter(func='" + con_list[1] + "')")

                    if len(results) != 0:
                        dic[con] = str(results[0])
                    else:
                        dic[con] = ''
                # 遍历查询条件
                else:
                    dic[con] = eval('str(obj.' + con + ')')
            data.append(dic)
        # 返回由多个对象字典组成的列表
        return data
    else:
        # 只有一个obj对象
        if list_args[0] == 'base':
            # 查询参数第一个为 base 所以返回的数据前加上 基础数据
            dic = {
                'username': str(obj_list[0].username),
                'gender': str(obj_list[0].gender),
                'GPA': str(obj_list[0].GPA),
                'birth': str(obj_list[0].birth)[0:10:1],
                'IDCard': str(obj_list[0].IDCard),
                'major': str(obj_list[0].major),
                'domesticTelephone': str(obj_list[0].domesticTelephone),
                'foreignTelephone': str(obj_list[0].foreignTelephone),
                'domesticAddress': str(obj_list[0].domesticAddress),
                'foreignAddress': str(obj_list[0].foreignAddress),
                'ambassador': str(obj_list[0].ambassador),
                'paid': str(obj_list[0].paid),
                'count_wk': str(obj_list[0].count_wk),
                'count_ms': str(obj_list[0].count_ms),
                'balance': str(obj_list[0].balance),
                'firstEmail': str(obj_list[0].firstEmail),
                'secondEmail': str(obj_list[0].secondEmail),
                'grade': str(obj_list[0].grade),
                'wechat': str(obj_list[0].wechat),
                'pinyin':str(obj_list[0].pinyin),
                'study':str(obj_list[0].study),
            }
            # 查询字符串去除第一个 base 参数
            list_args = list_args[1:]
        else:

            # 第一个参数不为base 按需返回数据
            dic = {}
        for con in list_args:
            if ('(' or ')') in con:
                return 'CNM'
            elif 'school' in con:
                con_list = con.split('_')
                results = eval("obj_list[0]." + con_list[0] + ".filter(func='" + con_list[1] + "')")

                if len(results) != 0:
                    dic[con] = str(results[0])
                else:
                    dic[con] = ''


            elif con == 'course_wk':
                results = obj_list[0].course_set.filter(category='wk')
                if len(results) != 0:
                    re_list = set()
                    for i in results:
                        re_list.add(str(i))
                    re_list = list(re_list)
                    dic[con] = re_list
                else:
                    dic[con] = ''

            elif con == 'course_ms':
                results = obj_list[0].course_set.filter(category='ms')
                if len(results) != 0:
                    re_list = set()
                    for i in results:
                        re_list.add(str(i))
                    re_list = list(re_list)
                    dic[con] = re_list
                else:
                    dic[con] = ''




            elif con == 'sub_wk':
                results = obj_list[0].state_set.filter(state='sub')
                if len(results) != 0:
                    re_list = []
                    for i in results:
                        if i.course.category == 'wk':
                            re_list.append({'id': str(i.course_id), 'course': str(i.course)})
                    dic[con] = re_list
                else:
                    dic[con] = ''

            elif con == 'sub_ms':
                results = obj_list[0].state_set.filter(state='sub')
                if len(results) != 0:
                    re_list = []
                    for i in results:
                        if i.course.category == 'ms':
                            re_list.append({'id': str(i.course_id), 'course': str(i.course)})
                    dic[con] = re_list
                else:
                    dic[con] = ''




            elif con == 'pass_wk':
                # results = obj_list[0].state_set.filter(state='sub')[0].course.category
                # print(obj_list[0].state_set.filter(state='sub'))
                # print(obj_list[0].state_set)
                # obj_list[0].course_set.filter(category='ms')[0].state_set.filter(state='sub')
                results = obj_list[0].state_set.filter(state='pass')
                if len(results) != 0:
                    re_list = []
                    for i in results:
                        if i.course.category == 'wk':
                            re_list.append({'id': str(i.course_id), 'course': str(i.course)})
                    dic[con] = re_list
                else:
                    dic[con] = ''

            elif con == 'pass_ms':
                results = obj_list[0].state_set.filter(state='pass')
                if len(results) != 0:
                    re_list = []
                    for i in results:
                        if i.course.category == 'ms':
                            re_list.append({'id': str(i.course_id), 'course': str(i.course)})
                    dic[con] = re_list
                else:
                    dic[con] = ''

            elif con == 'LOP_wk':
                results = obj_list[0].state_set.filter(state='LOP')
                if len(results) != 0:
                    re_list = []
                    for i in results:
                        if i.course.category == 'wk':
                            re_list.append({'id': str(i.course_id), 'course': str(i.course)})
                    dic[con] = re_list
                else:
                    dic[con] = ''

            elif con == 'LOP_ms':
                results = obj_list[0].state_set.filter(state='LOP')
                # print(results)
                if len(results) != 0:
                    re_list = []
                    for i in results:
                        if i.course.category == 'ms':
                            re_list.append({'id': str(i.course_id), 'course': str(i.course)})
                    dic[con] = re_list
                else:
                    dic[con] = ''

            # elif 'course' in con:
            #     con_list = con.split('_')
            #     # print(con,con_list)
            #     # print("obj_list[0]." + con_list[0] + "_set.filter(category='" + con_list[1] + "')")
            #     results = eval("obj_list[0]." + con_list[0] + "_set.filter(category='" + con_list[1] + "')")
            #
            #     if len(results) == 1:
            #         # print(1)
            #         dic[con] = str(results[0])
            #     elif len(results) > 1:
            #         # print(2)
            #         res_list = []
            #         for cou in results:
            #             res_list.append(cou.course)
            #         dic[con] = str(res_list)
            #     else:
            #         # print(3)
            #         dic[con] = ''
            #     # break

            else:
                # print(eval('str(obj_list[0].' + con + ')'))
                try:
                    dic[con] = eval('str(obj_list[0].' + con + ')')
                    # print('str(obj_list[0].' + con + ')')
                except:
                    return 'No data found'

        return dic


def request_data_generate(database, request, condition, key):
    '''
    根据 前端GET请求的查询字符串 输出符合json格式的data

    :param database: 数据库名称 ( str )

    :param request: request

    :param condition: 查询条件 ( 根据 表字段 选定符合要求的 查询结果集 )
                      必须为 字符串格式 的 完整 ORM 查询语句(支持Q F查询) 如 "username = 'WRhan'"
                      可设置多个查询条件 用逗号隔开 如 "username = 'WRhan', gender='m', id__lt='5'"
                      若外键反查 ( 查询条件是一个obj对象时 ) 不加单引号
                      如"counselor=guwen_name" ( 查询当前学习顾问负责多少学员 )

    :param key: request.GET.keys() 中的 key

    :eg:?all_new=id username gender (等号后多条数据空格隔开)

    :return:
    '''

    # 根据key取出 request中查询字符串的 value
    value = request.GET[key].split(' ')

    # 根据 condition 获取符合要求的查询结果集
    obj_list = eval(database + ".objects.filter(" + condition + ")")

    # 判断查询结果集个数
    if len(obj_list) != 1:
        data = []
        # 有多个obj对象
        for obj in obj_list:
            # 遍历 obj对象
            dic = {}
            for con in value:
                # print(value)
                if ('(' or ')') in con:
                    return 'CNM'
                # 根据value遍历查询条件
                else:
                    try:
                        dic[con] = eval('str(obj.' + con + ')')
                        # print('str(obj.' + con + ')')
                    except:
                        # print('str(obj.' + con + ')')
                        return 'No data found'
            data.append(dic)
        # 返回由多个对象字典组成的列表
        return data

    else:
        # 只有一个obj对象
        if value[0] == 'base':
            # 查询参数第一个为 base 所以返回的数据前加上 基础数据
            dic = {
                'username': str(obj_list[0].username),
                'gender': str(obj_list[0].gender),
                'GPA': str(obj_list[0].GPA),
                'birth': str(obj_list[0].birth)[0:10:1],
                'IDCard': str(obj_list[0].IDCard),
                'major': str(obj_list[0].major),
                'domesticTelephone': str(obj_list[0].domesticTelephone),
                'foreignTelephone': str(obj_list[0].foreignTelephone),
                'domesticAddress': str(obj_list[0].domesticAddress),
                'foreignAddress': str(obj_list[0].foreignAddress),
                'ambassador': str(obj_list[0].ambassador),
                'paid': str(obj_list[0].paid),
                'count_wk': str(obj_list[0].count_wk),
                'count_ms': str(obj_list[0].count_ms),
                'balance': str(obj_list[0].balance),
                'firstEmail': str(obj_list[0].firstEmail),
                'secondEmail': str(obj_list[0].secondEmail),
                'grade': str(obj_list[0].grade),
                'wechat': str(obj_list[0].wechat),
                'BZpicker': str(obj_list[0].currency)
            }
            # 查询字符串去除第一个 base 参数
            value = value[1:]
        else:
            # 第一个参数不为base 按需返回数据
            dic = {}
        for con in value:
            if ('(' or ')') in con:
                return 'CNM'
            elif 'school' in con:
                con = con.split('_')
                results = eval("obj_list[0]." + con[0] + ".filter(func='" + con[1] + "')")

                # 19-8-24 修改 课程可能是多个
                if len(results) != 0:
                    re_list = []
                    for i in results:
                        re_list.append(str(i))
                    dic[con] = re_list
                else:
                    dic[con[0]] = ''


            elif 'course' in con:
                con = con.split('_')
                results = eval("obj_list[0]." + con[0] + "_set.filter(category='" + con[1] + "')")
                if len(results) != 0:
                    re_list = []
                    for i in results:
                        re_list.append(str(i))
                    dic[con] = re_list
                else:
                    dic[con[0]] = ''





            else:
                try:
                    dic[con] = eval('str(obj_list[0].' + con + ')')
                except:
                    return 'No data found'

        return dic


# def field_data_qc_generate(database, field):
#     '''
#     根据表字段查询该表字段下的所有数据 ( 去重版本 ) 输出符合json格式的data
#
#     :param database:  数据库名称 ( str )
#     :param field:  表字段名称 ( str )
#     :return:
#     '''
#
#     try:
#         obj_value = eval(database + '.objects.values_list("' + field + '")')
#         id_value = Users.objects.values_list('id')
#         print(id_value)
#     except:
#         return 'No data found'
#
#     field_set = set()
#     for obj in obj_value:
#         field_set.add(obj[0])
#     return list(field_set)


def field_data_generate(database, field, *args):
    '''
    根据表字段查询该表字段下的所有数据  输出带有ID的符合json格式的data

    :param database:  数据库名称 ( str )
    :param field:  表字段名称 ( str )
    :param args: 查询条件
    :return:
    '''
    # print(args)
    # print(database + '.objects.filter('+args[0]+').values_list("id","' + field + '").order_by("'+field +'")')

    if args:
        # 如果有查询条件
        try:
            obj_value = eval(database + '.objects.filter(' + args[
                0] + ').values_list("id","' + field + '").order_by("' + field + '")')
            # print(obj_value)
        except:
            return 'No data found'
    else:
        # 如果没有查询条件

        if field == 'course':
            try:
                obj_value = eval(database + '.objects.values_list("id","' + field + '","category").order_by("' + field + '")')
                # print(obj_value)
                list1 = []
                for i in obj_value:
                    list2 = []
                    if i[2] == 'ms':
                        i2 = i[1] + ' < 面授课 >'
                    else:
                        i2 = i[1] + ' < 网络课 >'

                    # print(i[1])
                    # print(i2)
                    list2.append(i[0])
                    list2.append(i2)
                    list1.append(list2)
                obj_value = list1
            except:
                return 'No data found'
        else:
            try:
                obj_value = eval(database + '.objects.values_list("id","' + field + '").order_by("' + field + '")')
                # print(obj_value)
            except:
                return 'No data found'

    field_set = []
    # print(obj_value)
    for obj in obj_value:
        obj_dic = {}
        obj_dic['id'] = obj[0]
        obj_dic[field] = obj[1]
        field_set.append(obj_dic)

    return list(field_set)


# def search_data_generate(databases, search_msg, conditions):
#     '''
#     根据内容对规定表字段下所有数据进行模糊查询
#
#     :param databases:  数据库名称 ( str )
#     :param search_msg:   模糊查询内容 ( str )
#     :param conditions:   查询字段名称 ( list )
#     :return:   满足条件对象的 姓名 邮箱 身份证 上课学校 网课 面授课
#     :e.g:  search_data_generate('Users', '1', ['domesticTelephone', 'username', 'id'])
#
#     '''
#     if type(conditions) is str:
#         base = databases + ".objects.filter(Q({}__icontains='{}')".format(conditions, search_msg)
#     else:
#         if len(conditions) == 0:
#             return 'No data found'
#         base = databases + ".objects.filter("
#         for num, con in enumerate(conditions):
#             if num == 0:
#                 add = "Q({}__icontains='{}')".format(con, search_msg)
#             else:
#                 add = "|Q({}__icontains='{}')".format(con, search_msg)
#             base += add
#     base += ")"
#     # print(base)
#     try:
#         data = eval(base)
#         # print(data)
#     except:
#         return 'No data found'
#     data_list = []
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
#             sch_sk_list = sch[0]
#
        # data_list.append({'username': obj.username, 'firstEmail': obj.firstEmail, 'secondEmail': obj.secondEmail,
        #                   'IDCard': obj.IDCard, 'school': sch_sk_list,
        #                   'course_wk': cou_wk_list, 'course_ms': cou_ms_list})
#     return data_list


def search_base_generate(databases, search_msg, fuzzy, Precise):
    '''
    根据查询关键词 模糊查询 指定大使 旗下学员的 id username

    :param databases:  数据库名称 ( str )
    :param search_msg:  查询关键词

    :param fuzzy:  模糊查询字段 ( list )
        e.g: [ 'id' , 'username']

    :param Precise:  精准查询大使ID
    :return:  符合条件学员的 id username
        e.g:  search_base_generate('Users', 'WRhan', ['username','id','firstEmail'], '15')
    '''

    base = databases + ".objects.filter("

    for num, con in enumerate(fuzzy):
        if num == 0:
            add = "Q({}__icontains='{}')".format(con, search_msg)
        else:
            add = "|Q({}__icontains='{}')".format(con, search_msg)
        base += add

    base += ",ambassador={},isActive='true')".format(Precise)
    data = eval(base)

    data_list = []
    for obj in data:
        data_list.append({'id': obj.id, 'username': obj.username})

    return data_list


def search_ds_generate(databases, search_msg, fuzzy, Precise):

    base = databases + ".objects.filter("

    for num, con in enumerate(fuzzy):
        if num == 0:
            add = "Q({}__icontains='{}')".format(con, search_msg)
        else:
            add = "|Q({}__icontains='{}')".format(con, search_msg)
        base += add
    base += ",Q(role='ds')|Q(role='scfz')"

    base += ",ambassador={},isActive='true')".format(Precise)
    # print(base)
    data = eval(base)

    data_list = []
    for obj in data:
        data_list.append({'id': obj.id, 'username': obj.username})

    return data_list


def fuzzy_query_generate(search_msg):
    '''
    根据查询关键词判断 从 邮箱 手机号 姓名中进行模糊查询

    邮箱: 当查询关键词中有 @ 时 查询 firstEmail secondEmail 字段
    手机号:  当查询关键词为纯数字时 查询 domesticTelephone foreignTelephone 字段
    姓名:  其他情况 查询 username 字段

    :param search_msg:  查询关键词
    :return:  满足条件对象的 姓名 邮箱 身份证 上课学校 网课 面授课
    '''

    data_list = []
    if '@' in search_msg:
        # 有 @ 符号 查邮箱
        msg_obj_list = Users.objects.filter(Q(firstEmail__contains=search_msg) | Q(secondEmail__contains=search_msg),~Q(isActive='new'))
    else:
        try:
            # 全是数字 查手机号
            int(search_msg)
            msg_obj_list = Users.objects.filter(
                Q(domesticTelephone__contains=search_msg) | Q(foreignTelephone__contains=search_msg),~Q(isActive='new'))
        except:
            # 查姓名
            if len(search_msg) == 0:
                return 'No data found'
            msg_obj_list = Users.objects.filter(
                Q(username__contains=search_msg),~Q(isActive='new'))

    for msg_obj in msg_obj_list:
        # # 多对多查网课名称 ( 可能多个 )
        # cou_wk_list = []
        # cou_wk = msg_obj.course_set.filter(category='wk').values_list('course')
        # for cou in cou_wk:
        #     cou_wk_list.append(cou[0])
        #
        # # 多对多查面授课名称 ( 可能多个 )
        # cou_ms_list = []
        # cou_ms = msg_obj.course_set.filter(category='ms').values_list('course')
        # for cou in cou_ms:
        #     cou_ms_list.append(cou[0])
        #
        # # 多对多查上课学校名称 ( 只能一个 )
        # sch_sk_list = None
        # sch_sk = msg_obj.school.filter(func='sk').values_list('s_name')
        #
        # # 用for循环避免 查不到数据时 out of range
        # for sch in sch_sk:
        #     sch_sk_list = sch[0]

        # data_list.append(
        #     {'id': msg_obj.id, 'username': msg_obj.username, 'firstEmail': msg_obj.firstEmail, 'secondEmail': msg_obj.secondEmail,
        #      'IDCard': msg_obj.IDCard, 'school': sch_sk_list,
        #      'course_wk': cou_wk_list, 'course_ms': cou_ms_list})

        data_list.append({'id': msg_obj.id,'stu_num':msg_obj.stu_num, 'username': msg_obj.username})

    return data_list

def fuzzy_obj(search_msg,xzs_name):
    '''
    根据查询关键词判断 从 邮箱 手机号 姓名中进行模糊查询

    邮箱: 当查询关键词中有 @ 时 查询 firstEmail secondEmail 字段
    手机号:  当查询关键词为纯数字时 查询 domesticTelephone foreignTelephone 字段
    姓名:  其他情况 查询 username 字段

    :param search_msg:  查询关键词
    :return:  满足条件对象的 姓名 邮箱 身份证 上课学校 网课 面授课
    '''

    data_list = []
    if xzs_name == "Paul":
        if '@' in search_msg:
            # 有 @ 符号 查邮箱
            msg_obj_list = Users.objects.filter(
                Q(firstEmail__contains=search_msg) | Q(secondEmail__contains=search_msg), ~Q(isActive='new'),
                ~Q(stu_num=''))
        else:
            try:
                # 全是数字 查手机号
                int(search_msg)
                msg_obj_list = Users.objects.filter(
                    Q(domesticTelephone__contains=search_msg) | Q(foreignTelephone__contains=search_msg),
                    ~Q(isActive='new'), ~Q(stu_num=''))
            except:
                # 查姓名

                if '大学' in search_msg:
                    try:
                        school = School.objects.get(s_name=search_msg, func='zs')
                        msg_obj_list = Users.objects.filter(~Q(isActive='new'), ~Q(stu_num=''), school=school)
                    except:
                        msg_obj_list = ''

                else:
                    if len(search_msg) == 0:
                        return 'No data found'
                    msg_obj_list = Users.objects.filter(
                        Q(username__contains=search_msg), ~Q(isActive='new'), ~Q(stu_num=''))
    else:
        if '@' in search_msg:
            # 有 @ 符号 查邮箱
            msg_obj_list = Users.objects.filter(Q(firstEmail__contains=search_msg) | Q(secondEmail__contains=search_msg),~Q(isActive='new'),~Q(stu_num=''),school__xzs=xzs_name)
        else:
            try:
                # 全是数字 查手机号
                int(search_msg)
                msg_obj_list = Users.objects.filter(
                    Q(domesticTelephone__contains=search_msg) | Q(foreignTelephone__contains=search_msg),~Q(isActive='new'),~Q(stu_num=''),school__xzs=xzs_name)
            except:
                # 查姓名

                if '大学' in search_msg:
                    try:
                        school = School.objects.get(s_name=search_msg,func='zs')
                        msg_obj_list = Users.objects.filter(~Q(isActive='new'),~Q(stu_num=''),school=school,school__xzs=xzs_name)
                    except:
                        msg_obj_list = ''

                else:
                    if len(search_msg) == 0:
                        return 'No data found'
                    msg_obj_list = Users.objects.filter(
                        Q(username__contains=search_msg),~Q(isActive='new'),~Q(stu_num=''),school__xzs=xzs_name)

    for msg_obj in msg_obj_list:
        try:
            school_zs = str(msg_obj.school.get(func='zs'))
            print(school_zs)
        except:
            school_zs = ''
        data_list.append({'id': msg_obj.id,'stu_num':msg_obj.stu_num, 'username': msg_obj.username,'school_zs':school_zs})

    return data_list

def precise_query():
    pass
