from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
router = SimpleRouter()
# http://127.0.0.1:8000/home/
router.register('banners', views.BannerViewSet, 'banners')

urlpatterns = [
	path('test/', views.Test.as_view()),
]

urlpatterns += router.urls
