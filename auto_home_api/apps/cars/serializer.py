from rest_framework import serializers
from .models import Car, CarDetail, CarFactory, Distributor


# 车辆展示
class CarShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'name', 'orders', 'price', 'second_car_name', 'energy_type_name', 'stock_num', 'factory_name','popular',
                  'img_url_list'
                  ]
        extra_kwargs = {
            'img_url_list': {
                'read_only': True
            }
        }


# 车辆详情
class CarDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarDetail
        fields = [
            'car_detail', 'displacement', 'color', 'emission_standard_name', 'mileage', 'production_mode_name',
            'trans_num', 'popular',
        ]


# 车厂
class CarFactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarFactory
        fields = [
            'name', 'addr', 'tel'
        ]


class DistributorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = [
            'name', 'addr', 'tel'
        ]


# 车辆所有信息序列化展示
class CarinfosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            'id', 'name', 'orders', 'price', 'second_car_name', 'energy_type_name', 'stock_num', 'img_url_list',
            'car_info_detail',
            'carFactory', 'distributors'
        ]
        extra_kwargs = {
            'img_url_list': {
                'read_only': True
            }
        }

    car_info_detail = CarDetailSerializer()
    carFactory = CarFactorySerializer()
    distributors = DistributorsSerializer()
