# Generated by Django 2.2.2 on 2022-07-25 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='is_generate',
            field=models.BooleanField(default=0, verbose_name='是否领取过优惠券'),
        ),
    ]