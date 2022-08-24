import os
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from libs.qiniu import upload
from django.conf import settings
from django.views import View


class Test(APIView):
	def post(self, request):
		# 拿到文件对象
		file_obj = request.FILES.get("picture")
		# 文件名
		file_name = str(file_obj)
		# 文件存在项目中的那个地方
		file_url = os.path.join(settings.API_DIR, 'media', 'icon', file_name)
		# 把文件保存在本地
		with open(file_url, 'wb') as f:
			f.write(file_obj.read())
		# 文件存在云中的后缀路径
		filename_cloud = 'test/%s' % file_name
		# 保存在云中的名字，文件在本地的完整路径，修改七牛云的配置文件
		res = upload(filename_cloud, file_url)
		if not res:
			return HttpResponse(222)
		# 将文件从本地中删除
		os.remove(file_url)
		return HttpResponse(111)


class FullDisplayView(View):
	def get(self, request):
		return render(request, 'index.html')


from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from rest_framework.response import Response
from . import models, serializer
from django.conf import settings
from django.core.cache import cache


class BannerViewSet(ModelViewSet, mixins.ListModelMixin):
	queryset = models.Banner.objects.all().filter(is_show=1)
	serializer_class = serializer.BannerSerializer

	def list(self, request, *args, **kwargs):
		banner_list = cache.get("banner_list_cache")
		if banner_list:
			return Response(banner_list)
		else:
			res = super().list(request, *args, **kwargs)
			print(res.data)
			cache.set("banner_list_cache", res.data)
			return res
