from django.db import models


class Car(models.Model):
	class Meta:
		db_table = "cars"
		verbose_name = "汽车表"
		verbose_name_plural = "汽车表"

	car_type = (
		(0, '轿车'),
		(1, 'SUV'),
		(2, '跑车')
	)

	seats_choice = (
		(2, '两座'),
		(5, '五座'),
		(7, '七座')
	)

	second_car = (
		(0, "新车"),
		(1, "二手车"),
	)

	manual_trans = (
		(0, "手动档"),
		(1, "自动挡"),
	)

	energy_type = (
		(0, "新能源"),
		(1, "汽油"),
	)

	orders = models.IntegerField(verbose_name='优先级', default=10)
	name = models.CharField(max_length=128, verbose_name="车辆名称")
	car_type = models.SmallIntegerField(choices=car_type, default=0, verbose_name="车辆类型")
	price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='价格', default=0)
	seats_choice = models.SmallIntegerField(choices=seats_choice, default=0, verbose_name="车座数")
	energy_type = models.SmallIntegerField(choices=energy_type, default=0, verbose_name='能源类型')
	manual_trans = models.SmallIntegerField(choices=manual_trans, default=0, verbose_name="变速箱")
	second_car = models.SmallIntegerField(choices=second_car, default=0, verbose_name="是否二手")
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='上市时间')

	# 厂商表
	carFactory = models.ForeignKey(to="CarFactory", on_delete=models.SET_NULL, db_constraint=False,
	                               null=True, blank=True, verbose_name="车厂")
	# 车辆库存
	stock_num = models.SmallIntegerField(default=5, verbose_name='车辆库存')

	# 车辆详情外键字段
	car_info_detail = models.OneToOneField(to="CarDetail", on_delete=models.DO_NOTHING)

	# 经销商表
	distributors = models.ForeignKey(to="Distributor", on_delete=models.SET_NULL, null=True, db_constraint=False,
	                                 verbose_name='经销商')

	def __str__(self):
		return "%s" % self.name

	@property
	def popular(self):
		return self.car_info_detail.popular

	@property
	def car_type_name(self):
		return self.get_car_type_display()

	@property
	def seats_choice_name(self):
		return self.get_seats_choice_display()

	@property
	def second_car_name(self):
		return self.get_second_car_display()

	@property
	def manual_trans_name(self):
		return self.get_manual_trans_display()

	@property
	def energy_type_name(self):
		return self.get_energy_type_display()

	def factory_name(self):
		return self.carFactory.name

	def img_url_list(self):
		img_url_list = []
		for img_url in self.cars_img.all():
			img_url_list.append(img_url.img_url)
		return img_url_list


# 新能源车展示图片表
class CarsImg(models.Model):
	img_url = models.CharField(max_length=256, verbose_name='车辆展示的图片链接后缀')
	car = models.ForeignKey(Car, related_name='cars_img', on_delete=models.DO_NOTHING, verbose_name='图片所展示的车辆')

	class Meta:
		db_table = "cars_img"
		verbose_name = "车辆展示图片链接"
		verbose_name_plural = "车辆展示图片链接"

	def __str__(self):
		return "展示%s的图片" % self.car.name

	@property
	def name(self):
		"""车辆"""
		return self.car.name


# 车辆详情表
class CarDetail(models.Model):
	emission_standard_choice = (
		(0, '无'),
		(1, '国四'),
		(2, '国五'),
		(3, '国六'),
		(4, '国六b'),

	)
	production_mode = (
		(0, '合资'),
		(1, '进口'),
		(2, '国产'),
	)

	car_detail = models.TextField(max_length=1024, null=True, verbose_name='车辆描述')
	# 排量
	displacement = models.CharField(max_length=8, null=True, verbose_name='排量')
	# 车辆颜色
	color = models.CharField(max_length=8, verbose_name='车辆颜色')
	# 国标
	emission_standard = models.SmallIntegerField(choices=emission_standard_choice, default=0, verbose_name="排放国标")
	# 里程
	mileage = models.CharField(max_length=16, verbose_name='车辆里程')
	# 生产方式
	production_mode = models.SmallIntegerField(choices=production_mode, default=0, verbose_name="生产方式")
	# 过户次数
	trans_num = models.IntegerField(verbose_name='过户次数')
	# 车辆人气
	popular = models.BigIntegerField(default=0, verbose_name='车辆人气')

	@property
	def emission_standard_name(self):
		return self.get_emission_standard_display()

	@property
	def production_mode_name(self):
		return self.get_production_mode_display()

	@property
	def car(self):
		return self.car.name

	class Meta:
		db_table = "carDetail"
		verbose_name = "车辆详情表"
		verbose_name_plural = verbose_name


class CarFactory(models.Model):
	"""厂商表,外键一对多车表"""
	name = models.CharField(max_length=64, verbose_name="厂商名称")
	addr = models.CharField(max_length=64, verbose_name="厂商地址")
	tel = models.BigIntegerField(verbose_name="联系方式")

	class Meta:
		db_table = "carFactory"
		verbose_name = "厂商表"
		verbose_name_plural = verbose_name

	def __str__(self):
		return "%s" % self.name


class Distributor(models.Model):
	"""经销商表,二手车经销商为xx二手车市场,新车为xx4S店"""
	name = models.CharField(max_length=64, verbose_name="经销商名称")
	addr = models.CharField(max_length=64, verbose_name="经销商地址")
	tel = models.BigIntegerField(verbose_name="联系方式")

	class Meta:
		db_table = "distributor"
		verbose_name = "经销商表"
		verbose_name_plural = verbose_name

	def __str__(self):
		return "%s对象" % self.name
