from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
# http://127.0.0.1:8000/order/
router.register('buy', views.BuyView, 'buy')
router.register('success', views.PaySuccessView, 'success')
router.register('getorders', views.GetUserOrders, 'getorders')

urlpatterns = [
	# path('', include(router.urls)),
]
urlpatterns += router.urls
