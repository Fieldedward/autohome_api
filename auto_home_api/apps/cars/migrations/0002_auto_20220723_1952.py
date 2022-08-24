# Generated by Django 2.2.2 on 2022-07-23 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
	dependencies = [
		('cars', '0001_initial'),
	]

	operations = [
		migrations.RemoveField(
			model_name='distributor',
			name='cars',
		),
		migrations.RemoveField(
			model_name='car',
			name='distributors',
		),
		migrations.AddField(
			model_name='car',
			name='distributors',
			field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL,
			                        to='cars.Distributor', verbose_name='经销商'),
		),
		migrations.AlterField(
			model_name='carsimg',
			name='car',
			field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cars_img',
			                        to='cars.Car', verbose_name='图片所展示的车辆'),
		),
		migrations.DeleteModel(
			name='Car2Distributor',
		),
	]
