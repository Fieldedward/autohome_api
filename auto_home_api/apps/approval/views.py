from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from .models import CarPendingApproval
from .serializer_approval import PendingApprovalSerializer, CarPictureSerializer
from utils.APIRes import APIResponse


# Create your views here.


class ApprovalCarView(GenericViewSet, CreateModelMixin, ListModelMixin):
    queryset = CarPendingApproval.objects.all().filter(is_approval=False)
    serializer_class = PendingApprovalSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        super().create(request, *args, **kwargs)
        return APIResponse(code=100, msg="提交车辆待审核信息成功")

    def list(self, request, *args, **kwargs):
        self.serializer_class = CarPictureSerializer
        ser = self.get_serializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        super().list(request, *args, **kwargs)
        return APIResponse(code=100, msg="提交车辆待审核图片成功")
