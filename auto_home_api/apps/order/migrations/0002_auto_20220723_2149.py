# Generated by Django 2.2.2 on 2022-07-23 21:49

from django.db import migrations


class Migration(migrations.Migration):
	dependencies = [
		('order', '0001_initial'),
	]

	operations = [
		migrations.RemoveField(
			model_name='order',
			name='real_price',
		),
		migrations.RemoveField(
			model_name='order',
			name='total_amount',
		),
	]