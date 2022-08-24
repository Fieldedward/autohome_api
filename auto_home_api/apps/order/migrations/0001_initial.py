# Generated by Django 2.2.2 on 2022-07-23 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
	initial = True

	dependencies = [
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
		('cars', '0002_auto_20220723_1952'),
	]

	operations = [
		migrations.CreateModel(
			name='Order',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('subject', models.CharField(default='匿名商品', max_length=150, verbose_name='订单标题')),
				('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='订单总价')),
				('out_trade_no', models.CharField(max_length=64, unique=True, verbose_name='订单号')),
				('trade_no', models.CharField(max_length=64, null=True, verbose_name='流水号')),
				('order_status',
				 models.SmallIntegerField(choices=[(0, '未支付'), (1, '已支付'), (2, '已取消'), (3, '超时取消')], default=0,
				                          verbose_name='订单状态')),
				('pay_type',
				 models.SmallIntegerField(choices=[(1, '支付宝'), (2, '微信支付')], default=1, verbose_name='支付方式')),
				('pay_time', models.DateTimeField(null=True, verbose_name='支付时间')),
				('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='车辆原价')),
				('real_price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='车辆实价')),
				('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
				('car', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING,
				                             related_name='order_car', to='cars.Car', verbose_name='下单关联的车辆')),
				('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING,
				                           related_name='order_user', to=settings.AUTH_USER_MODEL,
				                           verbose_name='下单用户')),
			],
			options={
				'verbose_name': '订单记录',
				'verbose_name_plural': '订单记录',
				'db_table': 'orders',
			},
		),
	]
