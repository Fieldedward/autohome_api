from rest_framework import serializers
from cars.models import CarDetail


class CarDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = CarDetail
		fields = ['id', 'displacement', 'color', 'emission_standard',
		          'mileage', 'production_mode', 'trans_num', 'popular']
