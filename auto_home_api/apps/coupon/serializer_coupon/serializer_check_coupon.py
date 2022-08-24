from rest_framework import serializers
from coupon.models import Coupon


class CheckCouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = ['coupon_one', 'coupon_two', 'coupon_three']


