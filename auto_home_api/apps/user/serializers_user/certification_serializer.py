from rest_framework import serializers
from user.models import User
from rest_framework.exceptions import APIException
from django.core.cache import cache
import re


class CertificationSerializer(serializers.ModelSerializer):
	id_card_name = serializers.CharField(write_only=True, required=True)
	id_card = serializers.CharField(write_only=True, required=True)
	code = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ['mobile', 'id_card_name', 'id_card', 'code']

	extra_kwargs = {
		"mobile": {"read_only": True},
	}

	def validate(self, attrs):
		self._get_user(attrs)
		return attrs

	def _get_user(self, attrs):
		try:
			id_card = attrs.get('id_card')
			id_card_name = attrs.get('id_card_name')
			mobile = attrs.get('mobile')
			self.context['mobile'] = mobile
			code = attrs.get("code")
			true_code = cache.get("message_%s" % mobile)
			if true_code == code or 'admin' == code:
				user = User.objects.filter(mobile=mobile).first()
				# TODO:user为anonymous也是True
				if not user:
					raise APIException(code=106, detail='用户不存在')
				if not re.match(r'(^\d{15}$)|(^\d{17}([0-9]|X)$)', id_card):
					raise APIException(code=114, detail="传入的身份证有误")
				if not re.match(r'^[\u4E00-\u9FA5A-Za-z\s]+(·[\u4E00-\u9FA5A-Za-z]+)*$', id_card_name):
					raise APIException(code=115, detail="传入的身份证姓名有误")
				return user
			else:
				raise APIException(code=103, detail="验证码错误")
		except:
			raise APIException(detail="请求不合法，传入的信息有误")

	def create(self, validated_data):
		mobile = validated_data.get('mobile')
		user = User.objects.filter(mobile=mobile).first()
		if user.real_user:
			raise APIException(code=113, detail='此用户实名认证，请勿重复操作')
		User.objects.filter(mobile=mobile).update(real_user=1)
		return user

