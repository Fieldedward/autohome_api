from rest_framework import serializers
from approval.models import CarPendingApproval


class CarPictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarPendingApproval
        fields = ['id', 'img_list']
