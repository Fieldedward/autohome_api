from cars.models import CarDetail


class CarDetailThrottles:
	VISIT_RECORD = {}

	def __init__(self):
		self.history = None

	def allow_request(self, request, view):
		path = request.META.get('PATH_INFO')  # 'PATH_INFO': '/cars/car_detail/5/'
		print(path.rsplit('/'))  # ['', 'cars', 'car_detail', '7', '']
		car_id = path.rsplit('/')[-2]
		if not car_id.isdigit():
			return True
		car_id = int(car_id)
		# 取出访问者ip
		ip = request.META.get('REMOTE_ADDR')
		# print(ip)
		import time
		ctime = time.time()
		# 判断当前ip不在访问字典里，添加进去，并且直接返回True,表示第一次访问
		if ip not in self.VISIT_RECORD:
			self.VISIT_RECORD[ip] = [ctime, ]
			return True
		self.history = self.VISIT_RECORD.get(ip)
		# 循环判断当前ip的列表，有值，并且当前时间减去列表的最后一个时间大于3600s，把这种数据pop掉，这样列表中只有一小时以内的访问时间，
		while self.history and ctime - self.history[-1] > 3600:
			self.history.pop()
		if len(self.history) < 5:
			car_detail_obj = CarDetail.objects.filter(pk=car_id).first()
			popular = car_detail_obj.popular
			popular += 200
			# print(popular)
			CarDetail.objects.filter(pk=car_id).update(popular=popular)
			self.history.insert(0, ctime)
		return True

	def wait(self):
		import time
		ctime = time.time()
		return 3600 - (ctime - self.history[-1])
