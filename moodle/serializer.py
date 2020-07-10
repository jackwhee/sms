# from rest_framework import serializers
# from rest_framework import response
# from moodle.models import MoodleUser,MoodleCUS,MoodleCourse,MoodleSubject
#
#
# def UserSerializer(instance=None,many=False,data=None,field=None,allow=(),excludes=('m_ps',)):
#     '''
#     <用户>序列化器
#     :param instance(实例): 查询结果集/查询结果对象
#     :param many: 序列化器many参数
#     :param data: 接收到的json
#     :param field: 需要GET查询的字段名
#     :param excludes: GET排除字段
#     :param allow: PUT/POST允许修改的字段
#     :return: 序列化器对象
#     '''
#
#     class Serializer(serializers.ModelSerializer):
#
#         #       数据编辑
#         #       name --> 返回json键名
#         #       source --> 所绑定数据库字段名
#         #       error_messages --> 自定义错误信息(字典)
#         # m_ac= serializers.EmailField(max_length=50,error_messages={
#         #     'max_length':'字段超长'
#         # })
#
#         #       数据新增
#         #       id_10 --> 新增json键名
#         #       get_id_10 --> 数据编辑方法
#         # id_10 = serializers.SerializerMethodField()
#         # def get_id_10(self,instance):
#         #     return instance.id * 10
#
#         #时间格式化
#         #date = serializers.DateTimeField(format='%Y-%m-%d %X')
#
#         class Meta:
#             '''
#             model: 数据库绑定
#             fields: 查询字段选择
#             exclude: 查询字段筛选
#             '''
#             model = MoodleUser
#
#             # 有指定的查询字段
#             if field:
#                 fields = field
#
#             # 无指定的查询字段
#             else:
#                 #有data参数(POST/PUT) 允许所有字段
#                 if data:
#                     fields = '__all__'
#
#                 #无data参数(GET) 设置排除字段
#                 else:
#                     if excludes:
#                         exclude = excludes
#                     else:
#                         fields = '__all__'
#
#     # POST / PUT
#     if data:
#         allow = set(allow)
#         _data = {}
#
#         #allow存在 且 json键超出allow范围
#         if allow and (not allow.issuperset(set(data.keys()))):
#
#             for key in allow:
#
#                 #取出data中键名与allow对应的数据
#                 if key in data.keys():
#                     _data[key] = data[key]
#
#             return Serializer(data=_data,instance=instance)
#
#         else:
#             return Serializer(data=data,instance=instance)
#
#     # GET
#     else:
#         return Serializer(instance=instance,many=many)
#
#
# def CUSSerializer(instance=None,many=False,data=None,field=None,allow=(),excludes=None):
#     '''
#     <用户-课程关系>序列化器
#     :param instance(实例): 查询结果集/查询结果对象
#     :param many: 序列化器many参数
#     :param data: 接收到的json
#     :param field: 需要GET查询的字段名
#     :param excludes: GET排除字段
#     :param allow: PUT/POST允许修改的字段
#     :return: 序列化器对象
#     '''
#
#     class Serializer(serializers.ModelSerializer):
#
#         class Meta:
#             '''
#             model: 数据库绑定
#             fields: 查询字段选择
#             exclude: 查询字段筛选
#             '''
#             model = MoodleCUS
#
#             # 有指定的查询字段
#             if field:
#                 fields = field
#
#             # 无指定的查询字段
#             else:
#                 #有data参数(POST/PUT) 允许所有字段
#                 if data:
#                     fields = '__all__'
#
#                 #无data参数(GET) 设置排除字段
#                 else:
#                     if excludes:
#                         exclude = excludes
#                     else:
#                         fields = '__all__'
#
#     # POST / PUT
#     if data:
#         allow = set(allow)
#         _data = {}
#
#         #allow存在 且 json键超出allow范围
#         if allow and (not allow.issuperset(set(data.keys()))):
#
#             for key in allow:
#
#                 #取出data中键名与allow对应的数据
#                 if key in data.keys():
#                     _data[key] = data[key]
#
#             return Serializer(data=_data,instance=instance)
#
#         else:
#             return Serializer(data=data,instance=instance)
#
#     # GET
#     else:
#         return Serializer(instance=instance,many=many)
#
#
# def CourseSerializer(instance=None,many=False,data=None,field=None,allow=(),excludes=('m_user',)):
#     '''
#     <课程>序列化器
#     :param instance(实例): 查询结果集/查询结果对象
#     :param many: 序列化器many参数
#     :param data: 接收到的json
#     :param field: 需要GET查询的字段名
#     :param excludes: GET排除字段
#     :param allow: PUT/POST允许修改的字段
#     :return: 序列化器对象
#     '''
#
#     class Serializer(serializers.ModelSerializer):
#
#         class Meta:
#             '''
#             model: 数据库绑定
#             fields: 查询字段选择
#             exclude: 查询字段筛选
#             '''
#             model = MoodleCourse
#
#             # 有指定的查询字段
#             if field:
#                 fields = field
#
#             # 无指定的查询字段
#             else:
#                 #有data参数(POST/PUT) 允许所有字段
#                 if data:
#                     fields = '__all__'
#
#                 #无data参数(GET) 设置排除字段
#                 else:
#                     if excludes:
#                         exclude = excludes
#                     else:
#                         fields = '__all__'
#
#     # POST / PUT
#     if data:
#         allow = set(allow)
#         _data = {}
#
#         #allow存在 且 json键超出allow范围
#         if allow and (not allow.issuperset(set(data.keys()))):
#
#             for key in allow:
#
#                 #取出data中键名与allow对应的数据
#                 if key in data.keys():
#                     _data[key] = data[key]
#
#             return Serializer(data=_data,instance=instance)
#
#         else:
#             return Serializer(data=data,instance=instance)
#
#     # GET
#     else:
#         return Serializer(instance=instance,many=many)
#
#
# def SubjectSerializer(instance=None,many=False,data=None,field=None,allow=(),excludes=None):
#     '''
#     <学科>序列化器
#     :param instance(实例): 查询结果集/查询结果对象
#     :param many: 序列化器many参数
#     :param data: 接收到的json
#     :param field: 需要GET查询的字段名
#     :param excludes: GET排除字段
#     :param allow: PUT/POST允许修改的字段
#     :return: 序列化器对象
#     '''
#
#     class Serializer(serializers.ModelSerializer):
#
#         class Meta:
#             '''
#             model: 数据库绑定
#             fields: 查询字段选择
#             exclude: 查询字段筛选
#             '''
#             model = MoodleSubject
#
#             # 有指定的查询字段
#             if field:
#                 fields = field
#
#             # 无指定的查询字段
#             else:
#                 #有data参数(POST/PUT) 允许所有字段
#                 if data:
#                     fields = '__all__'
#
#                 #无data参数(GET) 设置排除字段
#                 else:
#                     if excludes:
#                         exclude = excludes
#                     else:
#                         fields = '__all__'
#
#     # POST / PUT
#     if data:
#         allow = set(allow)
#         _data = {}
#
#         #allow存在 且 json键超出allow范围
#         if allow and (not allow.issuperset(set(data.keys()))):
#
#             for key in allow:
#
#                 #取出data中键名与allow对应的数据
#                 if key in data.keys():
#                     _data[key] = data[key]
#
#             return Serializer(data=_data,instance=instance)
#
#         else:
#             return Serializer(data=data,instance=instance)
#
#     # GET
#     else:
#         return Serializer(instance=instance,many=many)
