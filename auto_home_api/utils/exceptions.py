from rest_framework.views import exception_handler
from django.conf import settings
from utils.loggings import logger
from .APIRes import APIResponse


def common_exception_handler(exc, context):
	# 只要走到这，说明程序出异常了，都需要记录日志，越详细越好
	request = context.get('request')
	view = context.get('view')
	ip = request.META.get('REMOTE_ADDR')
	path = request.path
	logger.error('程序出错了，错误视图类是：%s，用户ip是：%s，请求地址是：%s,错误原因：%s' % (str(view), ip, path, str(exc)))

	res = exception_handler(exc, context)
	# 测试环境
	if settings.DEBUG:
		if res:
			return APIResponse(code=exc.get_codes(), msg=res.data.get('detail'))
		else:
			return APIResponse(code=101, msg=str(exc))
	# 生产环境报错
	else:
		return APIResponse(code=101, msg='系统错误，请联系系统管理员')
