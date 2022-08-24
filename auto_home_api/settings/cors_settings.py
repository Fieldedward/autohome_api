# cors 跨域请求相关配置
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
	'DELETE',
	'GET',
	'OPTIONS',
	'PATCH',
	'POST',
	'PUT',
	'VIEW',
)

# 请求头中带有的字段
CORS_ALLOW_HEADERS = (
	'XMLHttpRequest',
	'X_FILENAME',
	'accept-encoding',
	'authorization',
	'content-type',
	'dnt',
	'origin',
	'user-agent',
	'x-csrftoken',
	'x-requested-with',
	'Pragma',
	'token',
	'Authorization',
	'csrftoken',
)
