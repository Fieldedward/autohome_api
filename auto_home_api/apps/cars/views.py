from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.filters import OrderingFilter

from .models import Car, CarDetail
from .serializer import CarShowSerializer, CarinfosSerializer
from utils.common_filter.fields_filter import Filter
from .serializer_car import CarDetailSerializer
from .throttle_car import CarDetailThrottles
from .page import CommonPageNumberPagination

class CarShowView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
	queryset = Car.objects.all()
	serializer_class = CarShowSerializer
	# 分页
	pagination_class = CommonPageNumberPagination
	filter_backends = [OrderingFilter, Filter]
	# 排序规则：优先级
	# 过滤规则-->到 Filter 中声明
	# filter_fields = ['orders']
	ordering_fields = ['orders', 'price', 'popular']

	def dispatch(self, request, *args, **kwargs):
		if kwargs:
			self.serializer_class = CarinfosSerializer
		return super(CarShowView, self).dispatch(request, *args, **kwargs)


from rest_framework.filters import SearchFilter
from utils.APIRes import APIResponse


class SearchCarsView(GenericViewSet, ListModelMixin):
	queryset = Car.objects.all()
	serializer_class = CarShowSerializer
	filter_backends = [SearchFilter, ]
	search_fields = ['name', 'carFactory__name']

	def list(self, request, *args, **kwargs):
		res = super().list(request, *args, **kwargs)
		if not res:
			return APIResponse(code=901, detail='搜索结果为空')
		return APIResponse(res.data)


class CarDetailView(GenericViewSet, RetrieveModelMixin):
	queryset = CarDetail.objects.all()
	serializer_class = CarDetailSerializer
	throttle_classes = [CarDetailThrottles, ]

	def retrieve(self, request, *args, **kwargs):
		self.get_serializer(data=request.data, context={'request': request})
		return super().retrieve(request, *args, **kwargs)
