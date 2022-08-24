from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.conf import settings

from libs.pay_ali import alipay, GATEWAY
from utils.unique_trade_id import unique_id_redis
from .models import Order
from user.models import User
from cars.models import Car
from coupon.models import Coupon

from celery_package.change_order import change_order_status


class OrderSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField()

    # {"subject":...,'pay_type':...,"price":..,,"car_id":...}
    class Meta:
        model = Order
        fields = ['subject', 'pay_type', 'price', 'car_id', ]

    def _valid_coupon(self, coupon_obj):
        coupon_one = coupon_obj.coupon_one
        coupon_two = coupon_obj.coupon_two
        coupon_three = coupon_obj.coupon_three
        valid_list = []
        # 判断优惠券是否已经使用
        if coupon_one != 1:
            valid_list.append(coupon_one)
        if coupon_two != 1:
            valid_list.append(coupon_two)
        if coupon_three != 1:
            valid_list.append(coupon_three)
        return valid_list

    def _update_coupon_status(self, coupon_obj, discount, user_id):
        # 判断使用了哪张优惠券
        if discount == coupon_obj.coupon_one:
            Coupon.objects.filter(user_id=user_id).update(coupon_one=1)
        elif discount == coupon_obj.coupon_two:
            Coupon.objects.filter(user_id=user_id).update(coupon_two=1)
        else:
            Coupon.objects.filter(user_id=user_id).update(coupon_three=1)

    def _final_price(self, price, discount):
        return price * discount

    def _coupon_exist(self, user_id):
        return Coupon.objects.filter(user_id=user_id).first()

    def _get_coupon(self, user, price):
        """订单支付中优惠券处理逻辑"""
        user_id = user.id
        # 1.判断用户是否领取过优惠券
        coupon_obj = self._coupon_exist(user_id)
        if not coupon_obj:
            return price
        # 2.获取有效的优惠券
        valid_list = self._valid_coupon(coupon_obj)
        # 3.获取最低折扣，使用之后将该优惠券数值改为1，表示已经使用
        if not valid_list:
            return price
        discount = min(valid_list)
        self.context['discount'] = discount
        # 4.更新优惠券状态，使用后折扣值改为1，下次自动剔除
        self._update_coupon_status(coupon_obj, discount, user_id)
        # 5.计算最终价格
        final_price = self._final_price(price, discount)
        return final_price

    def _check_price(self, attrs):
        pre_car_price = attrs.get("price")
        car_id = attrs.get('car_id')
        car_obj = Car.objects.filter(pk=car_id).first()
        real_price = car_obj.price

        if pre_car_price != real_price:
            raise APIException(code=802, detail='汽车价格不合法')
        return real_price

    def _get_out_trade_no(self):
        return unique_id_redis()

    def _get_user(self):
        return self.context.get('request').user

    def _get_pay_url(self, out_trade_no, price, subject):
        # 生成pay_url放到context中
        res = alipay.api_alipay_trade_page_pay(
            out_trade_no=out_trade_no,
            total_amount=float(price * 10000),  # 只有生成支付宝链接时，不能用Decimal
            subject=subject,
            return_url=settings.RETURN_URL,
            notify_url=settings.NOTIFY_URL,
        )
        pay_url = GATEWAY + res
        self.context['pay_url'] = pay_url

    def _before_create(self, attrs, out_trade_no, user):
        # 反序列化需要处理字段类型
        attrs['out_trade_no'] = out_trade_no
        attrs['user'] = user

    def validate(self, attrs):
        # 获取用户
        user = self._get_user()
        if not user.real_user:
            raise APIException(code=902, detail='请先实名认证')
        # 获取原始价格
        price = self._check_price(attrs)
        # 获取优惠券
        final_price = self._get_coupon(user, price)
        # 获取订单号
        out_trade_no = self._get_out_trade_no()
        self._get_pay_url(out_trade_no, final_price, attrs.get('subject'))
        self._before_create(attrs, out_trade_no, user)

        return attrs

    def create(self, validated_data):
        car_id = validated_data.get("car_id")
        car_obj = Car.objects.filter(pk=car_id).first()
        if car_obj.stock_num == 0:
            raise APIException(code=902, detail='库存不足无法购买')
        car_obj.stock_num -= 1
        car_obj.save()
        if not validated_data.get("user").new_user:
            validated_data.get("user").new_user = 1
            validated_data.get("user").save()
        # 启动一个celery 延时任务执行修改数据库中的超时订单状态
        eta_obj = datetime.utcnow() + timedelta(seconds=5)
        change_order_status.apply_async(args=[validated_data.get("out_trade_no")], eta=eta_obj)
        return super().create(validated_data)


class UserOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['orders', ]
