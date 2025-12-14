"""
Detection 앱 URL Configuration
"""

from django.urls import path
from apps.detection import views

app_name = 'detection'

urlpatterns = [
    # URL 분석
    path('analyze/', views.URLAnalysisView.as_view(), name='analyze'),

    # 분석 이력
    path('history/', views.AnalysisHistoryView.as_view(), name='history'),

    # 분석 결과 상세
    path('results/<int:analysis_id>/', views.AnalysisDetailView.as_view(), name='detail'),

    # 통계
    path('statistics/', views.AnalysisStatisticsView.as_view(), name='statistics'),
]
