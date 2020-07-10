from django.http import JsonResponse, HttpResponse
from users.models import Users
from tool.orm_helper import request_data_generate, field_data_generate, data_generate, search_base_generate, \
    fuzzy_query_generate


def test(request):
    if request.GET.keys():
        orm = ''

        for key in request.GET.keys():


# --------------------------------- 测试用 ----------------------------------------------------
            if key == 'dp_search':
                value = request.GET[key]
                print(value)
                data = data_generate('Users', 'id=1', [value])
                result = {'code': 200, 'data': data}
                return JsonResponse(result)
# --------------------------------- 测试用 ----------------------------------------------------




            if key == 'dp_menu':
                value = request.GET[key]

                if value == 'school_sk':
                    data = field_data_generate('School', 's_name', 'func="sk"')
                    # print(data)
                    result = {'code': 200, 'data': data}
                    return JsonResponse(result)

                if value == 'school_sh':
                    data = field_data_generate('School', 's_name', 'func="sh"')
                    # print(data)
                    result = {'code': 200, 'data': data}
                    return JsonResponse(result)

                if value == 'course_wk':
                    data = field_data_generate('Course', 'course', 'category="wk"')
                    result = {'code': 200, 'data': data}
                    return JsonResponse(result)

                if value == 'course_ms':
                    data = field_data_generate('Course', 'course', 'category="ms"')
                    result = {'code': 200, 'data': data}
                    return JsonResponse(result)

                if value == 'counselor':
                    data = field_data_generate('Counselor', 'counselor')
                    result = {'code': 200, 'data': data}
                    return JsonResponse(result)

                # 其他字段均在Users表中
                data = field_data_generate('Users', value)
                result = {'code': 200, 'data': data}
                return JsonResponse(result)

            if key == 'no_gw':
                data = data_generate('Users', "isActive='true',counselor=None", ['id', 'username'])
                result = {'code': 200, 'data': data}
                return JsonResponse(result)

            if key == 'fuzzy_search':
                # 根据查询关键词判断 从 邮箱 手机号 姓名中进行模糊查询
                # 邮箱: 当查询关键词中有 @ 时 查询 firstEmail secondEmail 字段
                # 手机号:  当查询关键词为纯数字时 查询 domesticTelephone foreignTelephone 字段
                # 姓名:  其他情况 查询 username 字段
                # data为满足条件对象的 姓名 邮箱 身份证 上课学校 网课 面授课

                value = request.GET[key]
                # print(value)
                data = fuzzy_query_generate(value)
                result = {'code': 200, 'data': data}
                return JsonResponse(result)

            if key == 'stu_msg':
                # 格式为 ?stu_msg=学号(必须放第一个) base(可有可无 必须放第二个 查询全量数据) 字段1 字段2 字段3 ..... ( 中间用空格隔开 )
                # e.g: ?stu_msg=15 username id GPA

                # 选择课程顾问 =学号 base 获取全量数据即可
                # 已报名学生分配课程 =学号 base counselor allotTime course_ms/wk school_zs/sh/sk count_wk count_ms

                value = request.GET[key]
                value = value.split(' ')
                s_id = value[0]
                value = value[1:]
                data = data_generate('Users', 'id={}'.format(s_id), value)
                result = {'code': 200, 'data': data}
                return JsonResponse(result)

            # try:
            #
            #
            # except:
            #     # 查询字符串也不是id 返回405 权限不足
            #     result = {'code': 405, 'error': 'Not enough permissions'}
            #     return JsonResponse(result)

            print(key, request.GET[key])
            orm += key + "='" + request.GET[key] + "',"

        # print(orm[0:-1:1])
        # data = data_generate('Users', orm, ['id', 'username'])
        # result = {'code': 200, 'data': data}
        # return JsonResponse(result)
        return HttpResponse('OK')


    # 无查询字符串返回 新学生(isActive为true counselor为NULL) 的个数
    else:
        new_stu_num = Users.objects.filter(isActive='true', counselor=None)
        result = {'code': 200, 'data': {'new_stu_num': len(new_stu_num)}}
        return JsonResponse(result)
