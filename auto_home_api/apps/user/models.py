from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	icon = models.ImageField(upload_to='icon', default='icon/default.png', verbose_name='用户头像')
	mobile = models.CharField(max_length=11, verbose_name='手机号')
	is_seller = models.IntegerField(default=0, verbose_name='是否商家')
	is_locked = models.BooleanField(default=0, verbose_name='是否锁定')
	is_del = models.BooleanField(default=0, verbose_name='是否注销')
	real_user = models.BooleanField(default=0, verbose_name='是否实名')
	new_user = models.BooleanField(default=0, verbose_name='是否新用户')

	class Meta:
		db_table = 'auto_home_user'
		verbose_name = '用户表'
		verbose_name_plural = verbose_name

	def __str__(self):  # print User的对象时，会显示它返回的数据
		return self.username

	def orders(self):
		order_obj_list = self.order_user.all()
		order_list=[]
		for order_obj in order_obj_list:
			order_dict={}
			print(order_obj.out_trade_no)

			order_dict['order_id']=order_obj.id
			order_dict['out_trade_no']=order_obj.out_trade_no
			order_dict['pay_type']=order_obj.pay_type_name
			order_dict['order_status']=order_obj.status_choices_name
			order_dict['price']=order_obj.price
			order_dict['created_time']=order_obj.created_time

			order_list.append(order_dict)
		return order_list