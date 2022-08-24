from rest_framework.response import Response


class APIResponse(Response):
	def __init__(self, code=100, msg='成功', status=None, headers=None, **kwargs):
		data = {'code': code, 'msg': msg}
		if kwargs:  # 有值，说明传了除上面声明的以外，有其他的，要放到data字典中
			data.update(kwargs)

		# 还要调用父类的init完成初始化
		super().__init__(data=data, status=status, headers=headers)
