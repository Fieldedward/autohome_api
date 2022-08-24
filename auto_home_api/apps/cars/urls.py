from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
# http://127.0.0.1:8000/cars/  {"user_id":3}
router.register('show', views.CarShowView, 'show')
router.register('search', views.SearchCarsView, 'search')
router.register('car_detail', views.CarDetailView, 'car_detail')

urlpatterns = [
]
urlpatterns += router.urls
