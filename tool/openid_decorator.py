'''
openid验证,根据openid换取数据库object对象

'''
import json
from users.models import Users

from django.http import JsonResponse


def openid_check(*methods):
	'''
	:param methods: 请求方法必须是 POST,GET,PUT,DELETE中一个或多个 严格判断参数大小写，统一大写
	:return:
	'''
	
	def _openid_check(func):
		def wrapper(request, *args, **kwargs):
			
			# 判断请求方法
			if not methods:
				# 如果没传methods参数，则直接返回视图
				return func(request, *args, **kwargs)
			# 判断请求方法是否合理
			if not request.method in methods:
				# 如果当前请求的方法不在 methods内，则直接返回视图
				return func(request, *args, **kwargs)
			
			# request校验
			print(request.method)
			print(str(request.method))
			json_str = request.POST
			print(json_str)
			if not json_str:
				# 前端异常提交，没有提交数据
				result = {'code': 401, 'error': 'There is no data'}
				return JsonResponse(result)
			
			# 把json串反序列化成字典
			json_obj = dict(json_str)
			# openid校验
			openid = json_obj.get('openid')
			if not openid or openid == 'null':
				# 前端异常提交，没有提交openid
				result = {'code': 402, 'error': 'You must have an openid'}
				return JsonResponse(result)
			
			# openid数据库校验
			try:
				# 查看此openid是否存在
				openid_obj = Users.objects.get(openid=openid)
				# 存在则取出openid对象
				request.openid = openid_obj
			except:
				result = {'code': 403, 'error': 'Openid unregistered'}
				return JsonResponse(result)

		return wrapper
	
	return _openid_check
