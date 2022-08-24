import os
import sys

# 总路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

# 小的项目路径
API_DIR = os.path.join(BASE_DIR, 'auto_home_api')
sys.path.insert(1, API_DIR)

# apps文件夹路径
APPS_DIR = os.path.join(API_DIR, 'apps')
sys.path.insert(2, APPS_DIR)

SECRET_KEY = 'po2s=e4)$fiqlrc*g5^v#$^=7e%m9@zo)i@(i^k8&c(4ds*%#r'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
	'simpleui',
	'corsheaders',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'home',
	'user',
	'cars',
	'order',
	'approval',
	'coupon',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	# cors 中间件
	'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'auto_home_api.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')]
		,
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'auto_home_api.wsgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'auto_home_api',
		'USER': 'auto_home',
		'PASSWORD': '12345',
		'HOST': '127.0.0.1',
		'PORT': 3306,
		'OPTIONS': {
			"init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
		}
	}
}

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'user.User'

# media的配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(API_DIR, 'media')

# logging 模块配置
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
		},
		'simple': {
			'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
		},
	},
	'filters': {
		'require_debug_true': {
			'()': 'django.utils.log.RequireDebugTrue',
		},
	},
	'handlers': {
		'console': {
			# 实际开发建议使用WARNING
			'level': 'DEBUG',
			'filters': ['require_debug_true'],
			'class': 'logging.StreamHandler',
			'formatter': 'simple'
		},
		'file': {
			# 实际开发建议使用ERROR
			'level': 'WARNING',
			'class': 'logging.handlers.RotatingFileHandler',
			# 日志位置,日志文件名,日志保存目录必须手动创建
			'filename': os.path.join(BASE_DIR, "log", "auto_home.log"),
			# 日志文件的最大值,这里我们设置300M
			'maxBytes': 300 * 1024 * 1024,
			# 日志文件的数量,设置最大日志数量为10
			'backupCount': 10,
			# 日志格式:详细格式
			'formatter': 'verbose',
			# 文件内容编码
			'encoding': 'utf-8'
		},
	},
	# 日志对象
	'loggers': {
		'django': {
			'handlers': ['console', 'file'],
			'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
		},
	}
}

# cors 的配置
from settings.cors_settings import *

# drf 的配置
REST_FRAMEWORK = {

	# 二次封装全局异常处理
	'EXCEPTION_HANDLER': 'utils.exceptions.common_exception_handler',
	# 频率认证类的设置
	"DEFAULT_THROTTLE_RATES": {
		'send_sms': '2/m',
	},

}

import datetime

JWT_AUTH = {
	'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

# cash-redis 缓存配置
CACHES = {
	"default": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": "redis://127.0.0.1:6379",
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
			"CONNECTION_POOL_KWARGS": {"max_connections": 100}  # 默认就有连接池
			# "PASSWORD": "123", # 如果有redis密码需要加上
		}
	}
}

# 其他自定义公共配置
from settings.common_settings import *

# simpleUi配置
from settings.simple_ui_settings import *

# # 大屏展示配置
from settings.full_dispaly_settings import *
