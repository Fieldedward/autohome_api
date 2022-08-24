from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
# http://127.0.0.1:8000/approval/approval_car/
router.register('approval_car', views.ApprovalCarView, 'approval_car')


urlpatterns = [
]
urlpatterns += router.urls
