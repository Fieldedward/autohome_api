from rest_framework import serializers
from user.models import User


class DisplayUserInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'mobile', 'icon', 'email', 'real_user']
		extra_kwargs = {
			'mobile': {"read_only": True},
			'real_user': {"read_only": True},
		}

	def validate(self, attrs):
		attrs.get("icon").name = self.context.get("request").user.username + '.jpg'
		return attrs




class UpdateUserIconSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['icon']

