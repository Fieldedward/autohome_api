from rest_framework.throttling import SimpleRateThrottle


class SendSmsThrottle(SimpleRateThrottle):
	scope = "send_sms"

	def get_cache_key(self, request, view):
		return request.query_params.get("mobile")
