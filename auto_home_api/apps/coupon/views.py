from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from .models import Coupon
from .serializer_coupon import RandomCouponSerializer, CheckCouponSerializer
from utils.APIRes import APIResponse

# Create your views here.


class RandomCouponView(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = Coupon.objects.all()

    def create(self, request, *args, **kwargs):
        self.serializer_class = RandomCouponSerializer
        ser = self.get_serializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        super().create(request, *args, **kwargs)
        return APIResponse(code=117, detail='领取过优惠券成功')

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CheckCouponSerializer
        return super().retrieve(request, *args, **kwargs)
