import os

# 应用私钥
APP_PRIVATE_KEY_STRING = open(
	os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pem', 'app_private_key.pem')).read()

# 支付宝公钥
ALIPAY_PUBLIC_KEY_STRING = open(
	os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pem', 'alipay_public_key.pem')).read()

# 应用ID
APP_ID = '2021000121628632'

# 加密方式
SIGN = 'RSA2'

DEBUG = True

# 支付网关
GATEWAY = 'https://openapi.alipaydev.com/gateway.do?' if DEBUG else 'https://openapi.alipay.com/gateway.do?'
