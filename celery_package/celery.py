import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_home_api.settings.dev')
import django
django.setup()

from celery import Celery
backend='redis://127.0.0.1:6379/1'
broker='redis://127.0.0.1:6379/2'
app = Celery(
	'test',
	broker=broker,
	backend=backend,
	include=[
		'celery_package.banner_update',
		'celery_package.send_sms_task',
		'celery_package.change_order',
	],
)

# 获取所有配置,右键执行该文件需要修改文件名
# print(worker.conf)

# 修改时区
app.conf.timezone = 'Asia/Shanghai'
app.conf.enable_utc = False

# 任务的定时配置
from datetime import timedelta
from celery.schedules import crontab

app.conf.beat_schedule = {
	'timed_task_24hours':{
		'task':'celery_package.banner_update.update_banner',  # 任务
		'schedule':timedelta(hours=24),
		# 'schedule':crontab(hours=8, day_of_week=1),  # 每周一早上 8 点
		# 'args':(6,7),  # 任务需要传入的参数
	},
# 	# 可以继续添加
}