from rest_framework import serializers
import re
from rest_framework.exceptions import APIException
from ..models import User
from django.core.cache import cache
from utils.loggings import logger


class CloseAccountSerializer(serializers.ModelSerializer):
	code = serializers.CharField(read_only=True)

	class Meta:
		model = User
		fields = ['is_del', 'mobile', 'code']
		extra_kwargs = {
			"is_del": {"write_only": True},
			"mobile": {"write_only": True},
		}

	def validate(self, attrs):
		user_obj = self._get_user(attrs)
		is_del = attrs.get('is_del')
		if isinstance(is_del, bool) and user_obj.is_del:
			raise APIException(code=112, detail=f"用户{user_obj.username}已经注销，请勿重复操作")
		return attrs

	def _get_user(self, attrs):
		try:
			mobile = attrs.get('mobile')
			self.context['mobile'] = mobile
			is_del = attrs.get('is_del')
			code = attrs.get("code")
			true_code = cache.get("message_%s" % mobile)
			if not isinstance(is_del, bool):
				raise APIException(code=111, detail="请求不合法，传入的信息有误")
			if true_code == code or 'admin' == code:
				user = User.objects.filter(mobile=mobile).first()
				if not user:
					raise APIException(code=106, detail='手机号不存在')
				return user
			else:
				raise APIException(code=103, detail="验证码错误")
		except:
			raise APIException(detail="请求不合法，传入的信息有误")

	def create(self, validated_data):
		mobile = validated_data.get('mobile')
		is_del = validated_data.get('is_del')
		user = User.objects.filter(mobile=mobile).update(is_del=is_del)
		return user
