from rest_framework.filters import BaseFilterBackend
from django.db.models import Q


class Filter(BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		if not request.GET.dict():
			return queryset

		filter_fields_items = request.GET.dict()
		filter_fields = ['carFactory', 'carFactory_id', 'car_info_detail', 'car_info_detail_id', 'car_type', 'cars_img',
		                 'created_time', 'distributors', 'distributors_id', 'energy_type', 'id', 'manual_trans', 'name',
		                 'order_car', 'orders', 'price', 'seats_choice', 'second_car', 'stock_num']

		for key in list(filter_fields_items.keys()):
			if key in filter_fields:
				continue
			filter_fields_items.pop(key)

		if 'price' in filter_fields_items:
			start_num, end_num = request.GET.get("price").split('-')
			start_num = float(start_num)
			end_num = float(end_num)
			queryset = queryset.filter(price__range=[start_num, end_num])
			filter_fields_items.pop('price')

		if not filter_fields_items:
			return queryset
		q = Q()
		for key, value in filter_fields_items.items():
			q.children.append((key, value))
		queryset = queryset.filter(q)

		return queryset
