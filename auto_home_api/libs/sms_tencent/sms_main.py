import ssl
import random
from qcloudsms_py import SmsSingleSender, SmsMultiSender
from qcloudsms_py.httpclient import HTTPError
from .sms_settings import appkey, appid, template_id, sms_sign
from auto_home_api.utils.loggings import logger

ssl._create_default_https_context = ssl._create_unverified_context


def make_code():
	res = ''
	for i in range(6):
		# 随机取得一个大写字母
		# s1 = chr(random.randint(65, 90))
		# 将 0-9 之间的数字随机取一个，并且输出成 str 类型
		s2 = str(random.randint(0, 9))
		# 在数字或者大写字母中随机取一个，总共需要 n 个字符，再拼接起来
		res += random.choice([s2, ])
	return res


def send_sms(mobile, code):
	ssender = SmsSingleSender(appid, appkey)
	# ssender = SmsMultiSender(appid, appkey)
	params = [code, ]  # 当模板没有参数时，`params = []`
	try:
		result = ssender.send_with_param(86, mobile, template_id, params, sign=sms_sign, extend="", ext="")
		if result.get("result") == 0:
			return True
		else:
			logger.error('手机号为:%s,发送短信失败' % mobile)
			return False
	except Exception:
		logger.error('发送短信异常，手机号为:%s' % mobile)
		return False
