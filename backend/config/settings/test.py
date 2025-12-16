"""
테스트 환경 설정
"""
from .base import *

# ====================
# Test Settings
# ====================

# 테스트 모드 활성화
DEBUG = False
TESTING = True

# ====================
# Database (In-Memory)
# ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # 메모리 DB 사용 (빠른 테스트)
    }
}

# ====================
# Password Hashers (Fast for Testing)
# ====================
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# ====================
# Selenium Settings
# ====================
SELENIUM_HEADLESS = True  # 테스트 시 Headless 모드

# ====================
# LLM Settings (Mock 사용 권장)
# ====================
# 테스트에서는 실제 API 호출 대신 Mock 사용을 권장합니다
# pytest-mock을 사용하여 LLM API 호출을 모킹하세요

# ====================
# Logging (Minimal for Testing)
# ====================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',  # 테스트 시 경고만 표시
    },
}

# ====================
# Cache (Dummy Cache for Testing)
# ====================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# ====================
# Email (Console Backend for Testing)
# ====================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ====================
# Static Files
# ====================
STATIC_ROOT = BASE_DIR / 'staticfiles_test'

# ====================
# Security Settings (Relaxed for Testing)
# ====================
SECRET_KEY = 'test-secret-key-not-for-production'
ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True
