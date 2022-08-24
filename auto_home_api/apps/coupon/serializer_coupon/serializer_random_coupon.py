from rest_framework import serializers
from coupon.models import Coupon
from user.models import User
from rest_framework.exceptions import APIException
import random


class RandomCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['user_id']

    def _user_status(self, attrs):
        # 确认id是否存在
        user_id = attrs.get('user_id')
        is_user = User.objects.filter(id=user_id).first()
        if not is_user:
            raise APIException(code=111, detail='请求不合法，传入的信息有误')
        # 确认id是不是当前登陆用户(postman测试，先注释)
        # request = self.context.get('request')
        # user = request.user
        # if user_id != user.id:
        #     raise APIException(code=111, detail='请求不合法，传入的信息有误')
        return True

    def _get_coupon(self, attrs, res):
        coupon_one = random.uniform(0.88, 0.99)
        coupon_one = round(coupon_one, 2)
        coupon_two = random.uniform(0.88, 0.99)
        coupon_two = round(coupon_two, 2)
        coupon_three = random.uniform(0.88, 0.99)
        coupon_three = round(coupon_three, 2)
        attrs['coupon_one'] = coupon_one
        attrs['coupon_two'] = coupon_two
        attrs['coupon_three'] = coupon_three
        attrs['is_generate'] = 1
        user_id = attrs.get('user_id')
        if not res:
            Coupon.objects.filter(user_id=user_id).update(coupon_one=coupon_one, coupon_two=coupon_two,
                                                          coupon_three=coupon_three)

    def validate(self, attrs):
        # 第一步，判断user_id是否存在和user_id是不是当前登陆用户
        self._user_status(attrs)
        # 第二步，判断是否领取过优惠券
        res = self._coupon_status(attrs)
        # 第三步，产生优惠券
        self._get_coupon(attrs, res)
        return attrs

    def _coupon_status(self, attrs):
        user_id = attrs.get('user_id')
        coupon_obj = Coupon.objects.filter(user_id=user_id).first()
        if coupon_obj:
            return False
        return True

    def create(self, validated_data):
        coupon_one = validated_data.get('coupon_one')
        coupon_two = validated_data.get('coupon_two')
        coupon_three = validated_data.get('coupon_three')
        user_id = validated_data.get('user_id')
        validated_data['id'] = user_id
        coupon_obj = Coupon.objects.filter(user_id=user_id).first()
        if coupon_obj:
            if coupon_obj.is_generate:
                raise APIException(code=116, detail='已经领取过优惠券，不能重复领取')
            Coupon.objects.filter(user_id=user_id).update(is_generate=1)
            raise APIException(code=117, detail=f'重新领取优惠券成功,分别为{coupon_one}折,{coupon_two}折,{coupon_three}折')
        coupon = Coupon.objects.create(**validated_data)
        return coupon
