from .celery import app
from order.models import Order

@app.task
def change_order_status(out_trade_no):
	queryset = Order.objects.filter(out_trade_no=out_trade_no).first()
	if queryset.order_status == 0:
		queryset.order_status = 3
		queryset.save()
		queryset.car.stock_num += 1
		queryset.car.save()
