"""
Detection 앱 모델
"""

from django.db import models
from django.contrib.auth.models import User


class AnalysisResult(models.Model):
    """URL 분석 결과"""

    url = models.URLField(max_length=2048, verbose_name="분석 URL")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='analysis_results',
        verbose_name="요청 사용자"
    )

    # 콘텐츠 정보
    title = models.CharField(max_length=500, verbose_name="제목")
    content = models.TextField(verbose_name="본문 요약")

    # 분석 결과
    is_clickbait = models.BooleanField(default=False, verbose_name="클릭베이트 여부")
    is_hate_speech = models.BooleanField(default=False, verbose_name="혐오 표현 포함 여부")
    is_misinformation = models.BooleanField(default=False, verbose_name="허위정보 가능성")

    # 신뢰도
    confidence_score = models.FloatField(default=0.0, verbose_name="전체 신뢰도 (0.0~1.0)")

    # 판단 근거 (Explainability)
    explanation = models.TextField(blank=True, default='', verbose_name="AI 판단 근거 (한 줄 요약)")

    # 상세 분석 결과 (JSON)
    analysis_details = models.JSONField(default=dict, blank=True, verbose_name="상세 분석 결과")

    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        db_table = 'analysis_results'
        verbose_name = 'URL 분석 결과'
        verbose_name_plural = 'URL 분석 결과들'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['url']),
        ]

    def __str__(self):
        return f"{self.url} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @property
    def is_safe(self) -> bool:
        """안전한 콘텐츠 여부"""
        return not (self.is_clickbait or self.is_hate_speech or self.is_misinformation)

    @property
    def risk_level(self) -> str:
        """위험도 레벨"""
        if self.confidence_score >= 0.7:
            return "high"
        elif self.confidence_score >= 0.4:
            return "medium"
        else:
            return "low"
