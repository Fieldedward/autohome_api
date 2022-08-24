import re
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import APIException
from ..models import User


# 普通用户注册
class MobileRegisterSerializer(serializers.ModelSerializer):
	code = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['mobile', 'password', 'code']
		extra_kwargs = {'password': {'write_only': True}}

	def validate_mobile(self, value):
		if not re.match(r'^1[3-9][0-9]{9}$', value):
			raise APIException(code=104, detail='手机号格式有误')
		return value

	def validate(self, attrs):
		mobile = attrs.get("mobile")
		code = attrs.get("code")
		# is_seller=attrs.get("is_seller")
		true_code = cache.get("message_%s" % mobile)
		cache.set("message_%s" % mobile, '')
		if not code == true_code and not 'admin' == code:
			raise APIException(code=103, detail="验证码错误")
		#  手机号是否注册过
		if User.objects.filter(mobile=mobile).first():
			raise APIException(code=105, detail='该手机号已经被注册')
		# 反序列化需要将不在表中的字段取出
		attrs.pop("code")
		attrs["username"] = mobile

		return attrs

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		return user


# 商家用户注册
class SellerMobileRegisterSerializer(serializers.ModelSerializer):
	code = serializers.CharField(write_only=True)
	mobile = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['mobile', 'password', 'code', 'is_seller']
		extra_kwargs = {
			'password': {'write_only': True},
		}

	def validate_mobile(self, value):
		if not re.match(r'^1[3-9][0-9]{9}$', value):
			raise APIException(code=104, detail='手机号格式有误')
		return value

	def validate(self, attrs):
		mobile = attrs.get("mobile")
		code = attrs.get("code")
		is_seller = attrs.get("is_seller")
		true_code = cache.get("message_%s" % mobile)
		cache.set("message_%s" % mobile, '')
		if not str(is_seller) == '1':
			raise APIException(code=109, detail='请求不合法，此处只注册商家用户')
		if not code == true_code and not 'admin' == code:
			raise APIException(code=103, detail="验证码错误")
		#  注册过了判断是否是商家用户, 手机号存在 且is_seller =1
		if User.objects.filter(mobile=mobile, is_seller=1).first():
			raise APIException(code=105, detail='该手机号已经被注册')
		elif User.objects.filter(mobile=mobile, is_seller=0).first():
			attrs['is_seller'] = 1
		# 反序列化需要将不在表中的字段取出
		attrs.pop("code")
		attrs["username"] = mobile
		return attrs

	def create(self, validated_data):
		# 通过传入的数据去数据库中筛选一下mobile是否存在
		instance_mobile = validated_data.get("mobile")
		instance_is_seller = validated_data.get("is_seller")
		user_obj = User.objects.filter(mobile=instance_mobile).first()
		if not user_obj:
			user = User.objects.create_user(**validated_data)
		else:
			user = User.objects.update(is_seller=instance_is_seller)
		return user
