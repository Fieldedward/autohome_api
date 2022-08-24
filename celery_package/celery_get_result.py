from .celery import app
from celery.result import AsyncResult


def task_result_celery(id):
	a = AsyncResult(id=id, app=app)

	if a.successful():
		result = a.get()
		return 1, result
	elif a.failed():
		return 0, 'a任务失败'
	elif a.status == 'PENDING':
		return 2, 'a任务等待中被执行'
	elif a.status == 'RETRY':
		return 3, 'a任务异常后正在重试'
	elif a.status == 'STARTED':
		return 4, 'a任务已经开始被执行'
