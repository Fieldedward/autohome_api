from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from libs import sms_tencent
from utils.APIRes import APIResponse
from utils.loggings import logger
from utils.common_throttle.sms_throttle import SendSmsThrottle
from .models import User
from .serializers_user import MulLoginSerializer, MobileLoginSerializer, MobileRegisterSerializer, SellerLogin, \
    SellerMobileRegisterSerializer, CloseAccountSerializer, DisplayUserInfoSerializer, CertificationSerializer, \
    UpdateUserIconSerializer

from celery_package.send_sms_task import send_sms_celery
from celery_package.celery_get_result import task_result_celery


# 验证手机号
class MobileView(ViewSet):
    """该视图类只有发送短信有频率认证"""

    @action(methods=['POST'], detail=False)
    def mobile_check(self, request):
        try:
            mobile = request.query_params.get("mobile")
            User.objects.get(mobile=mobile)
            return APIResponse()
        except:
            raise APIException(code=106, detail='手机号不存在')

    @action(methods=["POST"], detail=False, throttle_classes=[SendSmsThrottle, ])
    def send_message(self, request):
        mobile = request.data.get("mobile")
        if mobile:
            # 发送短信
            code = sms_tencent.make_code()
            # celery 异步发送短信
            task_id = send_sms_celery.delay(mobile, code)
            # 查看运行结果
            # task_status,msg = task_result_celery(task_id)
            logger.info("验证码为：%s" % code)
            cache.set("message_%s" % mobile, code)
            return APIResponse(msg="短信发送成功")

        else:
            raise APIException(code=108, detail='手机号不能为空')

    # 发送短信频率的报错封装
    def throttled(self, request, wait):
        wait = '距离下次可以发送短信还剩%s秒' % int(wait)
        raise APIException(code=801, detail=wait)


# 普通用户
class UserView(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()

    def _login_main(self, request):
        ser = self.get_serializer(data=request.data, context={"request": request})

        ser.is_valid(raise_exception=True)
        token = ser.context.get("token")
        username = ser.context.get("username")
        icon = ser.context.get("icon")
        user_id = ser.context.get('user_id')

        return APIResponse(user_id=user_id, token=token, username=username, icon=icon)

    @action(methods=["POST"], detail=False, url_path='login', serializer_class=MulLoginSerializer)
    def mul_login(self, request):
        return self._login_main(request)

    @action(methods=["POST"], detail=False, url_path='login2', serializer_class=MobileLoginSerializer)
    def mobile_login(self, request):
        return self._login_main(request)

    @action(methods=["POST"], detail=False, url_path='register', serializer_class=MobileRegisterSerializer)
    def mobile_register(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return APIResponse(msg="注册成功")


# 商家用户
class SellerUserView(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()

    def _login_main(self, request):
        ser = self.get_serializer(data=request.data, context={"request": request})

        ser.is_valid(raise_exception=True)
        token = ser.context.get("token")
        username = ser.context.get("username")
        icon = ser.context.get("icon")
        user_id = ser.context.get('user_id')

        return APIResponse(user_id=user_id, token=token, username=username, icon=icon)

    @action(methods=["POST"], detail=False, url_path='sellerlogin', serializer_class=MulLoginSerializer)
    def mul_login(self, request):
        return self._login_main(request)

    @action(methods=["POST"], detail=False, url_path='sellerlogin2', serializer_class=SellerLogin)
    def mobile_login(self, request):
        return self._login_main(request)

    # {“mobile”:"","password":"","code":'admin',"is_seller":"1"}
    @action(methods=["POST"], detail=False, url_path='register', serializer_class=SellerMobileRegisterSerializer)
    def mobile_register(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return APIResponse(msg="注册成功")


# 用户注销
class CloseAccountView(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()

    # permission_classes = [IsAuthenticated, ]

    def _close_user(self, request):
        ser = self.get_serializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        mobile = ser.context.get("mobile")
        return APIResponse(code=100, msg=f"{mobile}注销账户成功, 本网站不再保留您的信息")

    @action(methods=["POST"], detail=False, url_path='close', serializer_class=CloseAccountSerializer)
    def close_account(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return self._close_user(request)


# 展示个人信息
# http://127.0.0.1:8000/user/display/user_id/
class DisplayUserInfoView(GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = DisplayUserInfoSerializer
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]


# 修改头像
class UpdateUserIconView(GenericViewSet, RetrieveModelMixin, UpdateModelMixin,):
    queryset = User.objects.all()
    serializer_class = UpdateUserIconSerializer
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print(serializer.data)
        return APIResponse(code=100, msg='修改成功')
        # print(request.data)
        # data = {'icon': request.data.get('icon')}
        # print(data)
        # pk = request.data.get('id')
        # user = self.queryset.filter(pk=pk).first()
        # src = self.get_serializer(instance=user, data=data)
        # src.is_valid()
        # if src.is_valid():
        #     src.save()
        #     icon = user.objects.get('icon')
        #     return APIResponse(code=100, msg='修改成功', icon=icon)
        # else:
        #     return APIResponse(code=101, msg='修改失败')



# 实名认证接口
class CertificationView(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()

    def _certification_user(self, request):
        ser = self.get_serializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        username = ser.context.get("username")
        return APIResponse(code=100, msg=f"{username}实名认证成功, 恭喜您！")

    @action(methods=["POST"], detail=False, url_path='certification', serializer_class=CertificationSerializer)
    def close_account(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return self._certification_user(request)
