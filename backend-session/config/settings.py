import os,json

# 시간을 저장하는 객체를 만드는 라이브러리
from datetime import timedelta
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, 'secrets.json') # secrets.json 파일 위치를 명시

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = []


# Application definition
# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 소셜로그인 site 설정
    'django.contrib.sites',
]

PROJECT_APPS = [
    'posts', 
    'accounts',
]

# pip install을 통해 제3자 라이브러리를 다운로드를 받았을 때는 꼭 추가해주자
THIRD_PARTY_APPS = [
    "corsheaders", #  Cross-Origin Resource Sharing (CORS)를 지원하기 위한 라이브러리, 다른 도메인으로부터 온 리소스의 접근을 제한
    "rest_framework", # drf
    "rest_framework_simplejwt", # jwt 토큰

    # 소셜로그인 라이브러리
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # allauth.socialaccount.providers.{소셜로그인제공업체}
    # {소셜로그인제공업체} 부분에는 구글 외에도 카카오,네이버 추가 가능
    'allauth.socialaccount.providers.google',
    #s3
    'storages',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

# 사이트는 1개만 사용할 것이라고 명시
SITE_ID = 1

# AUTH_USER_MODEL = 'users.Member'
AUTH_USER_MODEL = 'users.Users'

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username' # username 필드 사용 x
ACCOUNT_EMAIL_REQUIRED = True            # email 필드 사용 o
ACCOUNT_USERNAME_REQUIRED = False        # username 필드 사용 x
ACCOUNT_AUTHENTICATION_METHOD = 'email'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

#CORS 설정
# Adding CORS headers allows your resources to be accessed on other domains. 
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [ 
    "http://localhost:3000", # 리액트 포트 (클리이언트)
    "http://127.0.0.1:3000",
    # "프론트 도메인 주소"
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False # DB에 반영되기 위해 False로 변경


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.Member' # accounts App의 Member 모델을 사용한다. 적지 않으면 기본유저모델을 사용.

# EC2
# 모든 호스트에게 허용
ALLOWED_HOSTS = [
    '*',
] 

# JWT

# 여러 REST_FRAMEWORK를 추가할 수 있음
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES' : (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

REST_USE_JWT = True

SIMPLE_JWT = {
    # 액세스 토큰 유효기간을 3시간으로 설정
    'ACCESS_TOKEN_LIFETIME' : timedelta(hours=3),

    # 리프레시 토큰 유혀기간을 1주일로 설정
    'REFRESH_TOKEN_LIFETIME' : timedelta(days = 7),

    # 새로운 엑세스 토큰과 리프레시 토큰 반환
    'ROTATE_REFRESH_TOKENS': False,

    # 같은 리프레시 토큰이 반환되지 않도록 하는 옵션
    'BLACKLIST_AFTER_ROTATION': False, 

    # JWT 인증에 사용할 사용자 클래스를 연결
    'TOKEN_USER_CLASS' : 'accounts.Member',
}

# MySQL 연결
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'mydatabase', # RDS 
		'USER': get_secret("DB_USER"), # RDS Username
		'PASSWORD': get_secret("DB_SECRET"),
		'HOST': get_secret("DB_HOST"), # localhost -> RDS 엔드포인트
        # secrets.json에 쓰기
		'PORT': '3306', # mysql은 3306 포트를 사용합니다
	}
}

# AWS 권한 설정
AWS_ACCESS_KEY_ID = get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_secret('AWS_SECRET_ACCESS_KEY')
AWS_REGION = 'ap-northeast-2'

# AWS S3 버킷 이름
AWS_STORAGE_BUCKET_NAME = 'likelion-11'

# AWS S3 버킷의 URL
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME,AWS_REGION)

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

