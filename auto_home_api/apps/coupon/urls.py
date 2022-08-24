from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
# http://127.0.0.1:8000/coupon/random/  post携带{"user_id":2} 领取优惠券
# http://127.0.0.1:8000/coupon/random/2/  查看优惠券
router.register('random', views.RandomCouponView, 'random')


urlpatterns = [
]
urlpatterns += router.urls
