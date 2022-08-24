from django.core.cache import cache
from .celery import app
from home.models import Banner
from django.conf import settings
from home.serializer import BannerSerializer


@app.task
def update_banner():
	# 取出轮播图
	queryset = Banner.objects.all()
	# 序列化之后才能返回给前端
	ser = BannerSerializer(instance=queryset,many=True)
	for item in  ser.data:
		item['image'] = settings.HOST_URL+item['image']
	cache.set("banner_list_cache",ser.data)
