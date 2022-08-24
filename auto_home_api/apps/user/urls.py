from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
# http://127.0.0.1:8000/user/
router.register('normal', views.UserView, 'normal')
router.register('seller', views.SellerUserView, 'seller')
router.register('sms', views.MobileView, 'sms')
router.register('service', views.CloseAccountView, 'service')
router.register('display', views.DisplayUserInfoView, 'display')
router.register('auth', views.CertificationView, 'auth')
router.register('icon', views.UpdateUserIconView, 'icon')

urlpatterns = [
	# path('', include(router.urls)),
]
urlpatterns += router.urls
