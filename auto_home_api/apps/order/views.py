from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.APIRes import APIResponse
from utils.loggings import logger
from user.models import User
from .models import Order
from .serializer import OrderSerializer, UserOrdersSerializer


class BuyView(GenericViewSet, CreateModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # {"subject":...,'pay_type':...,"price":..,,"car_id":...}
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        pay_url = serializer.context.get("pay_url")
        discount = serializer.context.get('discount')
        if discount:
            return APIResponse(msg=f'成功下单，使用了优惠券{discount}折', pay_url=pay_url)
        return APIResponse(msg='成功下单', pay_url=pay_url)


class PaySuccessView(ViewSet):
    authentication_classes = []
    permission_classes = []

    # 给前端做二次校验用
    def list(self, request):
        out_trade_no = request.query_params.get('out_trade_no')
        order = Order.objects.filter(out_trade_no=out_trade_no).first()
        if order.order_status == 1:
            return APIResponse(msg='订单支付成功')
        elif order.order_status == 0:
            return APIResponse(code=903, msg='尚未收到付款')
        elif order.order_status == 2:
            return APIResponse(code=904, msg='订单已取消')
        elif order.order_status == 3:
            return APIResponse(code=905, msg='订单已超时取消')

    # 给支付宝用的--->必须把项目部署在公网上才能回调成功,修改订单状态
    def create(self, request):
        import json
        try:
            result_data = request.data.dict()
            logger.warning(json.dumps(result_data))
            # 我们的订单号
            out_trade_no = result_data.get('out_trade_no')
            # 支付宝的签名
            signature = result_data.pop('sign')
            from libs.pay_ali import alipay
            result = alipay.verify(result_data, signature)
            if result and result_data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
                # 完成订单修改：订单状态、流水号、支付时间
                Order.objects.filter(out_trade_no=out_trade_no).update(order_status=1)
                # 完成日志记录
                logger.warning('%s订单支付成功' % out_trade_no)
                # 支付宝要的格式就这个格式
                return Response('success')
            else:
                logger.error('%s订单支付失败' % out_trade_no)
        except:
            pass
        return Response('failed')


class GetUserOrders(GenericViewSet, ListModelMixin):
    serializer_class = UserOrdersSerializer
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        queryset = User.objects.filter(pk=user_id).first()
        serializer = self.get_serializer(queryset)

        return Response(serializer.data)
