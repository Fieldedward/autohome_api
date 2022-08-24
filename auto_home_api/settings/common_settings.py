# 后台 url
HOST_URL = 'http://127.0.0.1:8000'
PRE_URL = 'http://127.0.0.1:8080'

# 后台异步回调的地址
NOTIFY_URL = HOST_URL + '/order/success/'
# 前台同步回调的地址，没有 / 结尾的
RETURN_URL = PRE_URL + '/pay/success/'
