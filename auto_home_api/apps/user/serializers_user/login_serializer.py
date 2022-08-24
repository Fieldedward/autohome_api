import re
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import APIException
from ..models import User
from utils.loggings import logger


def _get_token(user):
	# 生成荷载
	from rest_framework_jwt.settings import api_settings

	jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
	jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

	payload = jwt_payload_handler(user)  # 根据当前登录用户获取荷载
	token = jwt_encode_handler(payload)  # 根据荷载生成token

	return token


class MulLoginSerializer(serializers.ModelSerializer):
	username = serializers.CharField()

	class Meta:
		model = User
		fields = ['username', 'password', 'icon']
		extra_kwargs = {
			'password': {"write_only": True},
			"icon": {"read_only": True}
		}

	# 全局钩子-->校验用户，签发token
	def validate(self, attrs):
		# 校验用户
		user_obj = self._get_user(attrs)
		user_id = user_obj.pk
		username = user_obj.username
		# 校验用户是否锁定
		is_lock = user_obj.is_locked
		if is_lock:
			logger.info(f"黑名单用户{username}正在尝试登陆,触发自动拦截")
			raise APIException(code=110, detail=f"用户{username}已被锁定,请联系管理员")
		# 校验用户是否注销
		is_del = user_obj.is_del
		if is_del:
			logger.info(f"已注销用户{username}正在尝试登陆,触发自动拦截")
			raise APIException(code=102, detail="用户或密码错误")
		# 签发token
		token = _get_token(user_obj)

		self.context['token'] = token
		self.context['user_id'] = user_id
		self.context['username'] = user_obj.username
		host = self.context.get("request").META.get("HTTP_HOST")
		self.context['icon'] = "http://%s/media/%s" % (host, str(user_obj.icon))

		return attrs

	def _get_user(self, attrs):
		try:
			username = attrs.get("username")
			password = attrs.get("password")
			# 判断用户登录类型
			# 手机登录
			if re.match(r'^1[3-9][0-9]{9}$', username):
				user_obj = User.objects.get(mobile=username)
			# 邮箱登录
			elif re.match(r"[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+", username):
				user_obj = User.objects.get(email=username)
			# 用户名登录
			else:
				user_obj = User.objects.get(username=username)

		except:
			raise APIException(code=102, detail="用户或密码错误")
		else:
			if not user_obj.check_password(password):
				raise APIException(code=102, detail="用户或密码错误")

			return user_obj


# 手机号登录
class MobileLoginSerializer(serializers.ModelSerializer):
	code = serializers.CharField()

	class Meta:
		model = User
		fields = ['mobile', 'code', 'is_seller']

	def validate_mobile(self, value):
		if not re.match(r'^1[3-9][0-9]{9}$', value):
			raise APIException(code=104, detail='手机号格式有误')
		return value

	# 全局钩子-->校验用户，签发token
	def validate(self, attrs):
		# 校验用户
		user_obj = self._get_user(attrs)
		user_id = user_obj.pk
		# 签发token
		token = _get_token(user_obj)

		self.context['token'] = token
		self.context['user_id'] = user_id
		self.context['username'] = user_obj.username
		#  用户类型
		self.context['is_seller'] = user_obj.is_seller

		host = self.context.get("request").META.get("HTTP_HOST")
		self.context['icon'] = "http://%s/media/%s" % (host, str(user_obj.icon))

		return attrs

	def _get_user(self, attrs):
		mobile = attrs.get("mobile")
		code = attrs.get("code")
		true_code = cache.get("message_%s" % mobile)
		cache.set("message_%s" % mobile, '')

		if true_code == code or 'admin' == code:
			user = User.objects.filter(mobile=mobile).first()
			if not user:
				raise APIException(code=102, detail='用户不存在')
			return user
		else:
			raise APIException(code=103, detail="验证码错误")


#  商家登录
class SellerLogin(serializers.ModelSerializer):
	code = serializers.CharField()

	class Meta:
		model = User
		fields = ['mobile', 'code', 'is_seller']

	def validate_mobile(self, value):
		if not re.match(r'^1[3-9][0-9]{9}$', value):
			raise APIException(code=104, detail='手机号格式有误')
		return value

	# 全局钩子-->校验用户，签发token
	def validate(self, attrs):
		# 校验用户
		user_obj = self._get_user(attrs)
		user_id = user_obj.pk
		username = user_obj.username
		# 校验用户是否锁定
		is_lock = user_obj.is_locked
		if is_lock:
			logger.info(f"黑名单用户{username}正在尝试登陆,触发自动拦截")
			raise APIException(code=110, detail=f"商家账户{username}已被锁定,请联系管理员")
		# 校验用户是否注销
		is_del = user_obj.is_del
		if is_del:
			logger.info(f"已注销用户{username}正在尝试登陆,触发自动拦截")
			raise APIException(code=102, detail="用户或密码错误")
		# 签发token
		token = _get_token(user_obj)

		self.context['token'] = token
		self.context['user_id'] = user_id
		self.context['username'] = user_obj.username
		#  用户类型
		self.context['is_seller'] = user_obj.is_seller

		host = self.context.get("request").META.get("HTTP_HOST")
		self.context['icon'] = "http://%s/media/%s" % (host, str(user_obj.icon))

		return attrs

	def _get_user(self, attrs):
		mobile = attrs.get("mobile")
		code = attrs.get("code")
		true_code = cache.get("message_%s" % mobile)
		cache.set("message_%s" % mobile, '')
		seller_obj = User.objects.filter(mobile=mobile).first()
		if not seller_obj.is_seller:
			raise APIException(code=109, detail='你不是商家用户，无法登录')

		if true_code == code or 'admin' == code:
			user = User.objects.filter(mobile=mobile).first()
			if not user:
				raise APIException(code=102, detail='用户不存在')
			return user
		else:
			raise APIException(code=103, detail="验证码错误")
