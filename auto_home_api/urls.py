from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from home.views import FullDisplayView

urlpatterns = [
	path('admin/', admin.site.urls),
	path('index/', FullDisplayView.as_view()),
	path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
	path('user/', include('user.urls')),
	path('cars/', include('cars.urls')),
	path('home/', include('home.urls')),
	path('order/', include('order.urls')),
	path('approval/', include('approval.urls')),
	path('coupon/', include('coupon.urls'))
]
