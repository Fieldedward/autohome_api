from django.db import models
from user.models import User
from cars.models import Car


class Order(models.Model):
	"""订单模型"""
	status_choices = (
		(0, '未支付'),
		(1, '已支付'),
		(2, '已取消'),
		(3, '超时取消'),
	)
	pay_choices = (
		(1, '支付宝支付'),
		(2, '微信支付'),
	)
	subject = models.CharField(max_length=150, verbose_name="订单标题", default='匿名商品')

	# 咱们生成的订单号，唯一，后期改订单状态需要使用这个号
	out_trade_no = models.CharField(max_length=64, verbose_name="订单号", unique=True)
	# 支付宝有个流水号
	trade_no = models.CharField(max_length=64, null=True, verbose_name="流水号")
	# 订单状态
	order_status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="订单状态")
	pay_type = models.SmallIntegerField(choices=pay_choices, default=1, verbose_name="支付方式")
	pay_time = models.DateTimeField(null=True, verbose_name="支付时间")

	price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="车辆原价")

	# real_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="车辆实价")

	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

	user = models.ForeignKey(User, related_name='order_user', on_delete=models.DO_NOTHING, db_constraint=False,
	                         verbose_name="下单用户")

	car = models.ForeignKey(Car, related_name='order_car', on_delete=models.DO_NOTHING, db_constraint=False,
	                        verbose_name="下单关联的车辆")

	@property
	def status_choices_name(self):
		return self.get_order_status_display()

	@property
	def pay_type_name(self):
		return self.get_pay_type_display()


	@property
	def car_detail(self):
		img_list = []

		for img in self.car.cars_img.all():
			img_list.append(img.img_url)

		data_dict = {
			"car_name": self.car.name,
			"car_img_url": img_list[0],
		}
		return data_dict

	def __str__(self):
		return "%s - ￥%s" % (self.subject, self.price)

	class Meta:
		db_table = "orders"
		verbose_name = "订单记录"
		verbose_name_plural = "订单记录"
