"""
Accounts 앱 URL Configuration
"""

from django.urls import path
from apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    # 회원가입
    path('register/', views.RegisterView.as_view(), name='register'),

    # 프로필 조회
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
