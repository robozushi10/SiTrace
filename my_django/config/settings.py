"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ
from datetime import timedelta  # !!

#---------------------------------------------------------------- 
# 独自にプロジェクトルート用の変数 PROJECT_NAME を定義する(akiyoko basic: P111)
#---------------------------------------------------------------- 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = os.path.basename(BASE_DIR)   # !! my_django

#---------------------------------------------------------------- 
# .env から秘密情報を取り出す(akiyoko basic: P128)
#---------------------------------------------------------------- 
env = environ.Env(); # !!
env.read_env(os.path.join(BASE_DIR, 'config', '.env')) # ./config/.env
SECRET_KEY = env('SECRET_KEY')

#---------------------------------------------------------------- 
# デバッグ機能の ON・OFF 設定
#---------------------------------------------------------------- 
DEBUG = True

MY_DEBUG = { # !!
  'logging': False,  # Django の全ログを出力させたい場合は True にする
  'coreapi': True,   # CoreAPI による APIドキュメント画面を利用する (akiyoko rest2: P178)
  'toolbar': False,  # SQL パネル を使いたい場合は True にする (akiyoko basic: P148)
}

#---------------------------------------------------------------- 
# 全ホストからのアクセスを許可する(akiyoko basic: P124)
#---------------------------------------------------------------- 
ALLOWED_HOSTS = ['*']   # !!

#---------------------------------------------------------------- 
# Application definition
#---------------------------------------------------------------- 
INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'rest_framework',
  'django_filters',     # !! akiyoko rest2: P181
  'sitrace.apps.SitraceConfig',
  'apiv1.apps.Apiv1Config',
  'django_extensions',  # !! python manage.py graph_models -a -g -o graph-model.png
]

#---------------------------------------------------------------- 
# REST_FRAMEWORK の設定 
#---------------------------------------------------------------- 
# DRF 3.12 で CoreAPI が廃止される模様.
REST_FRAMEWORK = {
  'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}


#---------------------------------------------------------------- 
# 
#---------------------------------------------------------------- 
MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

#---------------------------------------------------------------- 
# テンプレート置き場を /.../my_django/templates/ とする (akiyoko basic: P122)
#---------------------------------------------------------------- 
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')], # !! 
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


WSGI_APPLICATION = 'config.wsgi.application'


#---------------------------------------------------------------- 
# 本アプリで使用する Database を指定する (akiyoko basic: P129)
#---------------------------------------------------------------- 
DATABASES = { # !!
  'default': env.db()
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


#---------------------------------------------------------------- 
# ロケーションとタイムゾーン(akiyoko basic: P123)
#---------------------------------------------------------------- 
LANGUAGE_CODE = 'ja'     # !!
TIME_ZONE = 'Asia/Tokyo' # !!
USE_I18N = True          # !!
USE_L10N = True          # !!
USE_TZ = True            # !!


#---------------------------------------------------------------- 
# 静的ファイルの設定 (akiyoko basic: P110)
#---------------------------------------------------------------- 
STATIC_URL = '/static/'
# 静的ファイル置き場を /.../my_django/static/ とする
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]   # !!
# 静的ファイルの配信元. collectstatic コマンドで静的ファイルを集約する際のコピー先でもある.
STATIC_ROOT = '/var/www/{}/static'.format(PROJECT_NAME) # !!


#---------------------------------------------------------------- 
# POST させるデータの上限値
# 無限にしたい場合は validation メソッドを上書きする必要がある
#---------------------------------------------------------------- 
if ('10MB' in MY_DEBUG) and (MY_DEBUG['10MB'] is True): # !! 
  DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240000
elif ('100MB' in MY_DEBUG) and (MY_DEBUG['10MB'] is True):
  DATA_UPLOAD_MAX_NUMBER_FIELDS = 102400000
else:
  DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240000


#---------------------------------------------------------------- 
# ロギング設定 (akiyoko basic: P120)
#---------------------------------------------------------------- 
# 開発時はコンソール出力し、SQLクエリも出力するようにする # !!
if ('logging' in MY_DEBUG) and (MY_DEBUG['logging'] is True):
   LOGGING = {
      # バージョンは「1」固定
      'version': 1,
      # 既存のログ設定を無効化しない
      'disable_existing_loggers': False,
      # ログフォーマット
      'formatters': {
          # 開発用
          'develop': {
              'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d '
                        '%(message)s'
          },
      },
      # ハンドラ
      'handlers': {
          # コンソール出力用ハンドラ
          'console': {
              'level': 'DEBUG',
              'class': 'logging.StreamHandler',
              'formatter': 'develop',
          },
      },
      # ロガー
      'loggers': {
          # 自作アプリケーション全般のログを拾うロガー
          '': {
              'handlers': ['console'],
              'level': 'DEBUG',
              'propagate': False,
          },
          # Django本体が出すログ全般を拾うロガー
          'django': {
              'handlers': ['console'],
              'level': 'INFO',
              'propagate': False,
          },
          # 発行されるSQL文を出力するための設定
          # 'django.db.backends': {
          #     'handlers': ['console'],
          #     'level': 'DEBUG',
          #     'propagate': False,
          # },
      },
  }
