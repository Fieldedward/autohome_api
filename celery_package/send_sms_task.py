from libs.sms_tencent import send_sms
from .celery import app

@app.task
def send_sms_celery(mobile,code):
	send_sms(mobile,code)