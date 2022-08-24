from rest_framework import serializers
from approval.models import CarPendingApproval


class PendingApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPendingApproval
        fields = ['name', 'price', 'seats_choice', 'second_car', 'energy_type', 'stock_num',
                  'displacement', 'color', 'emission_standard', 'is_approval',
                  'mileage', 'production_mode', 'trans_num',
                  'carFactory', 'car_detail_id', 'distributor_id',
                  'img_list',
                  ]
