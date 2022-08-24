from alipay import AliPay
from . import pay_settings

alipay = AliPay(
	appid=pay_settings.APP_ID,
	app_notify_url=None,  # 默认回调 url
	app_private_key_string=pay_settings.APP_PRIVATE_KEY_STRING,
	# 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
	alipay_public_key_string=pay_settings.ALIPAY_PUBLIC_KEY_STRING,
	sign_type=pay_settings.SIGN,
	debug=pay_settings.DEBUG,
)
