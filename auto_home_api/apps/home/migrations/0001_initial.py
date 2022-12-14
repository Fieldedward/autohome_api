# Generated by Django 2.2.2 on 2022-07-24 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=16, unique=True, verbose_name='名称')),
                ('image', models.ImageField(upload_to='banner', verbose_name='图片')),
                ('link', models.CharField(max_length=64, verbose_name='跳转链接')),
                ('info', models.TextField(verbose_name='详情')),
            ],
            options={
                'verbose_name_plural': '轮播图表',
                'db_table': 'banners',
            },
        ),
    ]
