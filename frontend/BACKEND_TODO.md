# 백엔드 미구현 기능 제안서

프론트엔드 개발 관점에서 백엔드에 반드시 구현되어야 할 기능들을 정리했습니다.

---

## 🚨 필수 구현 사항 (High Priority)

### 1. API 키 관리 시스템

#### 현재 상태
- `apps/api_keys` 앱이 존재하나 views, urls가 모두 비어있음
- models.py도 비어있어 DB 구조 미정의

#### 필요한 API

##### 1.1 API 키 목록 조회
```
GET /api/v1/api-keys/
```

**권한**: IsAuthenticated

**응답**:
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 1,
      "name": "Production Key",
      "key_prefix": "sk_prod_",
      "description": "Production environment key",
      "permissions": ["analyze", "history", "statistics"],
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z",
      "last_used_at": "2024-01-15T10:30:00Z",
      "usage_count": 150
    }
  ]
}
```

##### 1.2 API 키 생성
```
POST /api/v1/api-keys/
```

**권한**: IsAuthenticated

**Request Body**:
```json
{
  "name": "Development Key",
  "description": "Key for development environment",
  "permissions": ["analyze", "history"],
  "rate_limit": 100  // 선택적: 시간당 요청 제한
}
```

**응답**:
```json
{
  "success": true,
  "message": "API key created successfully",
  "data": {
    "id": 2,
    "name": "Development Key",
    "api_key": "sk_dev_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456",  // ⚠️ 최초 1회만 반환
    "key_prefix": "sk_dev_",
    "permissions": ["analyze", "history"],
    "rate_limit": 100,
    "created_at": "2024-01-15T12:00:00Z"
  }
}
```

**보안 고려사항**:
- 생성된 API 키 전체 문자열은 최초 1회만 반환
- DB에는 해시값만 저장 (예: SHA-256)
- 키 형식: `sk_{환경}_{랜덤문자열}`
- 최소 32자 이상 랜덤 문자열

##### 1.3 API 키 수정
```
PUT /api/v1/api-keys/{key_id}/
```

**권한**: IsAuthenticated (소유자만)

**Request Body**:
```json
{
  "name": "Updated Key Name",
  "description": "Updated description",
  "permissions": ["analyze", "history", "statistics"],
  "is_active": false
}
```

##### 1.4 API 키 삭제
```
DELETE /api/v1/api-keys/{key_id}/
```

**권한**: IsAuthenticated (소유자만)

**응답**:
```json
{
  "success": true,
  "message": "API key deleted successfully"
}
```

##### 1.5 API 키 재생성
```
POST /api/v1/api-keys/{key_id}/regenerate/
```

**권한**: IsAuthenticated (소유자만)

**응답**:
```json
{
  "success": true,
  "message": "API key regenerated successfully",
  "data": {
    "api_key": "sk_prod_nEwKeYaBcDeFgHiJkLmNoPqRsTuVwX",  // 새 키
    "regenerated_at": "2024-01-15T15:00:00Z"
  }
}
```

**주의사항**:
- 이전 키는 즉시 무효화됨
- 새 키는 1회만 표시됨

##### 1.6 API 키 사용 통계
```
GET /api/v1/api-keys/{key_id}/usage/?period=30d
```

**권한**: IsAuthenticated (소유자만)

**Query Parameters**:
- `period`: 7d, 30d, 90d, all (기본값: 30d)

**응답**:
```json
{
  "success": true,
  "data": {
    "key_id": 1,
    "period": "30d",
    "total_requests": 500,
    "successful_requests": 480,
    "failed_requests": 20,
    "rate_limit_exceeded": 5,
    "daily_usage": [
      {
        "date": "2024-01-01",
        "requests": 15,
        "success": 14,
        "failed": 1
      }
      // ... 30일치 데이터
    ],
    "endpoint_distribution": {
      "/api/v1/analyze/": 300,
      "/api/v1/history/": 150,
      "/api/v1/statistics/": 50
    },
    "avg_response_time_ms": 450
  }
}
```

#### 데이터베이스 모델 제안

```python
# apps/api_keys/models.py
from django.db import models
from django.contrib.auth.models import User
import secrets
import hashlib

class APIKey(models.Model):
    """API 키 모델"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='api_keys'
    )

    name = models.CharField(max_length=100, verbose_name="키 이름")
    description = models.TextField(blank=True, verbose_name="설명")

    # 보안: 전체 키는 저장하지 않고 해시만 저장
    key_hash = models.CharField(max_length=64, unique=True, verbose_name="키 해시")
    key_prefix = models.CharField(max_length=20, verbose_name="키 prefix (표시용)")

    # 권한
    permissions = models.JSONField(default=list, verbose_name="권한 목록")

    # Rate Limiting
    rate_limit = models.IntegerField(
        default=100,
        verbose_name="시간당 요청 제한"
    )

    # 상태
    is_active = models.BooleanField(default=True, verbose_name="활성 여부")

    # 사용 통계
    usage_count = models.IntegerField(default=0, verbose_name="총 사용 횟수")
    last_used_at = models.DateTimeField(null=True, blank=True, verbose_name="마지막 사용 시각")

    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'api_keys'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['key_hash']),
            models.Index(fields=['user', '-created_at']),
        ]

    @staticmethod
    def generate_key():
        """새 API 키 생성"""
        return f"sk_{''.join(secrets.token_urlsafe(32))}"

    @staticmethod
    def hash_key(key):
        """키 해시 생성"""
        return hashlib.sha256(key.encode()).hexdigest()

    def verify_key(self, key):
        """키 검증"""
        return self.key_hash == self.hash_key(key)


class APIKeyUsage(models.Model):
    """API 키 사용 로그"""

    api_key = models.ForeignKey(
        APIKey,
        on_delete=models.CASCADE,
        related_name='usage_logs'
    )

    endpoint = models.CharField(max_length=200, verbose_name="엔드포인트")
    method = models.CharField(max_length=10, verbose_name="HTTP 메서드")

    status_code = models.IntegerField(verbose_name="응답 상태 코드")
    response_time_ms = models.IntegerField(verbose_name="응답 시간 (ms)")

    ip_address = models.GenericIPAddressField(verbose_name="요청 IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_key_usage'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['api_key', '-created_at']),
            models.Index(fields=['created_at']),
        ]
```

---

### 2. 분석 이력 페이지네이션 개선

#### 현재 상태
```
GET /api/v1/history/?limit=20
```
- 단순 limit 파라미터만 지원
- 오프셋 없어서 페이지 이동 불가능

#### 필요한 개선

##### 2.1 페이지네이션 추가
```
GET /api/v1/history/?page=1&page_size=20
```

**응답**:
```json
{
  "success": true,
  "count": 150,
  "next": "http://localhost:8000/api/v1/history/?page=2&page_size=20",
  "previous": null,
  "results": [
    // 분석 결과 리스트
  ]
}
```

**구현 방법**:
```python
# apps/detection/views.py
from rest_framework.pagination import PageNumberPagination

class AnalysisResultPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class AnalysisHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = AnalysisResultPagination

    def get(self, request):
        queryset = AnalysisResult.objects.filter(user=request.user)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = AnalysisResultListSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
```

---

### 3. 필터링 및 정렬 기능

#### 필요한 API

```
GET /api/v1/history/?risk_level=high&is_safe=false&ordering=-created_at&search=example.com
```

**Query Parameters**:
- `risk_level`: safe, low, medium, high
- `is_safe`: true, false
- `is_clickbait`: true, false
- `is_hate_speech`: true, false
- `is_misinformation`: true, false
- `ordering`: created_at, -created_at, confidence_score, -confidence_score
- `search`: URL 또는 제목 검색

**구현 방법**:
```python
# apps/detection/views.py
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters

class AnalysisResultFilter(filters.FilterSet):
    risk_level = filters.ChoiceFilter(
        field_name='risk_level',
        choices=[('safe', 'Safe'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    )
    is_safe = filters.BooleanFilter(method='filter_is_safe')

    class Meta:
        model = AnalysisResult
        fields = ['is_clickbait', 'is_hate_speech', 'is_misinformation']

    def filter_is_safe(self, queryset, name, value):
        if value:
            return queryset.filter(
                is_clickbait=False,
                is_hate_speech=False,
                is_misinformation=False
            )
        else:
            return queryset.filter(
                models.Q(is_clickbait=True) |
                models.Q(is_hate_speech=True) |
                models.Q(is_misinformation=True)
            )

class AnalysisHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnalysisResultListSerializer
    pagination_class = AnalysisResultPagination
    filter_backends = [
        filters.DjangoFilterBackend,
        drf_filters.OrderingFilter,
        drf_filters.SearchFilter
    ]
    filterset_class = AnalysisResultFilter
    ordering_fields = ['created_at', 'confidence_score']
    search_fields = ['url', 'title']

    def get_queryset(self):
        return AnalysisResult.objects.filter(user=self.request.user)
```

---

### 4. 분석 이력 삭제 기능

#### 필요한 API

##### 4.1 단일 삭제
```
DELETE /api/v1/results/{analysis_id}/
```

**권한**: IsAuthenticated (소유자만)

**응답**:
```json
{
  "success": true,
  "message": "Analysis result deleted successfully"
}
```

##### 4.2 대량 삭제
```
POST /api/v1/results/bulk-delete/
```

**Request Body**:
```json
{
  "ids": [1, 2, 3, 4, 5]
}
```

**응답**:
```json
{
  "success": true,
  "message": "5 results deleted successfully",
  "deleted_count": 5
}
```

**구현 예시**:
```python
# apps/detection/views.py
class AnalysisDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, analysis_id):
        try:
            result = AnalysisResult.objects.get(id=analysis_id, user=request.user)
            result.delete()

            return Response({
                'success': True,
                'message': 'Analysis result deleted successfully'
            })
        except AnalysisResult.DoesNotExist:
            return Response({
                'error': True,
                'message': 'Analysis result not found'
            }, status=404)

class AnalysisBulkDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ids = request.data.get('ids', [])

        if not ids:
            return Response({
                'error': True,
                'message': 'No IDs provided'
            }, status=400)

        deleted_count = AnalysisResult.objects.filter(
            id__in=ids,
            user=request.user
        ).delete()[0]

        return Response({
            'success': True,
            'message': f'{deleted_count} results deleted successfully',
            'deleted_count': deleted_count
        })
```

---

### 5. 개선된 분석 통계

#### 현재 상태
```json
{
  "total_analyses": 100,
  "clickbait_detected": 15,
  "hate_speech_detected": 5,
  "misinformation_detected": 10,
  "safe_content": 70
}
```

#### 필요한 개선

```
GET /api/v1/statistics/?period=30d
```

**응답**:
```json
{
  "success": true,
  "data": {
    "period": "30d",
    "total_analyses": 100,
    "clickbait_detected": 15,
    "hate_speech_detected": 5,
    "misinformation_detected": 10,
    "safe_content": 70,

    "risk_level_distribution": {
      "safe": 70,
      "low": 15,
      "medium": 10,
      "high": 5
    },

    "avg_confidence_score": 0.87,

    "daily_statistics": [
      {
        "date": "2024-01-01",
        "total": 15,
        "safe": 10,
        "dangerous": 5,
        "avg_confidence": 0.85
      }
      // ... 30일치 데이터
    ],

    "most_analyzed_domains": [
      {
        "domain": "example.com",
        "count": 25,
        "safe_count": 20,
        "dangerous_count": 5
      },
      {
        "domain": "news.com",
        "count": 15,
        "safe_count": 12,
        "dangerous_count": 3
      }
    ],

    "hourly_distribution": {
      "00": 2,
      "01": 1,
      // ...
      "23": 3
    }
  }
}
```

**구현 예시**:
```python
# apps/detection/services/statistics_service.py
from django.db.models import Count, Avg, Q
from django.db.models.functions import TruncDate, ExtractHour
from urllib.parse import urlparse
from datetime import timedelta
from django.utils import timezone

class StatisticsService:

    @staticmethod
    def get_user_statistics(user, period='30d'):
        """사용자 통계 조회"""

        # 기간 계산
        days = int(period.rstrip('d')) if period != 'all' else None
        start_date = timezone.now() - timedelta(days=days) if days else None

        queryset = AnalysisResult.objects.filter(user=user)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)

        # 기본 통계
        total = queryset.count()
        clickbait = queryset.filter(is_clickbait=True).count()
        hate_speech = queryset.filter(is_hate_speech=True).count()
        misinformation = queryset.filter(is_misinformation=True).count()
        safe = queryset.filter(
            is_clickbait=False,
            is_hate_speech=False,
            is_misinformation=False
        ).count()

        # 위험도 분포
        risk_distribution = {
            'safe': queryset.filter(confidence_score__lt=0.4).count(),
            'low': queryset.filter(
                confidence_score__gte=0.4,
                confidence_score__lt=0.7
            ).count(),
            'medium': queryset.filter(
                confidence_score__gte=0.7,
                confidence_score__lt=0.9
            ).count(),
            'high': queryset.filter(confidence_score__gte=0.9).count(),
        }

        # 평균 신뢰도
        avg_confidence = queryset.aggregate(
            avg=Avg('confidence_score')
        )['avg'] or 0

        # 일별 통계
        daily_stats = queryset.annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            total=Count('id'),
            safe=Count('id', filter=Q(
                is_clickbait=False,
                is_hate_speech=False,
                is_misinformation=False
            )),
            dangerous=Count('id', filter=Q(
                is_clickbait=True
            ) | Q(
                is_hate_speech=True
            ) | Q(
                is_misinformation=True
            )),
            avg_confidence=Avg('confidence_score')
        ).order_by('date')

        # 도메인별 통계
        domain_stats = []
        for result in queryset:
            domain = urlparse(result.url).netloc
            # 도메인별 집계 로직

        return {
            'period': period,
            'total_analyses': total,
            'clickbait_detected': clickbait,
            'hate_speech_detected': hate_speech,
            'misinformation_detected': misinformation,
            'safe_content': safe,
            'risk_level_distribution': risk_distribution,
            'avg_confidence_score': round(avg_confidence, 2),
            'daily_statistics': list(daily_stats),
            'most_analyzed_domains': domain_stats[:10],
        }
```

---

## ⚠️ 중요 개선 사항 (Medium Priority)

### 6. 에러 응답 상태 코드 개선

#### 현재 문제
- Crawler 실패, LLM 실패 모두 500 에러 반환
- 프론트엔드에서 에러 타입 구분 어려움

#### 개선 방안

**Crawler 실패**:
```
Status: 502 Bad Gateway
```
```json
{
  "error": true,
  "error_type": "CRAWLER_ERROR",
  "error_code": "CRAWLER_FAILED",
  "message": "Failed to crawl URL",
  "details": {
    "reason": "Connection timeout",
    "url": "https://example.com"
  }
}
```

**LLM 실패**:
```
Status: 503 Service Unavailable
```
```json
{
  "error": true,
  "error_type": "LLM_ERROR",
  "error_code": "LLM_SERVICE_UNAVAILABLE",
  "message": "Failed to analyze content",
  "details": {
    "reason": "LLM service unavailable",
    "retry_after": 60
  }
}
```

**구현**:
```python
# apps/detection/views.py
except CrawlerException as e:
    return Response({
        'error': True,
        'error_type': 'CRAWLER_ERROR',
        'error_code': 'CRAWLER_FAILED',
        'message': 'Failed to crawl URL',
        'details': {
            'reason': str(e),
            'url': url
        }
    }, status=status.HTTP_502_BAD_GATEWAY)

except LLMException as e:
    return Response({
        'error': True,
        'error_type': 'LLM_ERROR',
        'error_code': 'LLM_SERVICE_UNAVAILABLE',
        'message': 'Failed to analyze content',
        'details': {
            'reason': str(e),
            'retry_after': 60
        }
    }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
```

---

### 7. Rate Limiting

#### 필요한 기능

**응답 헤더에 Rate Limit 정보 포함**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

**구현**:
```python
# middleware/rate_limit.py
from django.utils import timezone

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Rate limit 체크
        # ...

        response = self.get_response(request)

        # 헤더 추가
        response['X-RateLimit-Limit'] = '100'
        response['X-RateLimit-Remaining'] = '95'
        response['X-RateLimit-Reset'] = int(timezone.now().timestamp()) + 3600

        return response
```

---

### 8. 배치 URL 분석

```
POST /api/v1/analyze/batch/
```

**Request**:
```json
{
  "urls": [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
  ]
}
```

**Response**:
```json
{
  "success": true,
  "message": "Batch analysis completed",
  "data": {
    "total": 3,
    "succeeded": 2,
    "failed": 1,
    "results": [
      {
        "url": "https://example1.com",
        "status": "success",
        "result": { /* 분석 결과 */ }
      },
      {
        "url": "https://example2.com",
        "status": "success",
        "result": { /* 분석 결과 */ }
      },
      {
        "url": "https://example3.com",
        "status": "failed",
        "error": "Failed to crawl URL",
        "error_type": "CRAWLER_ERROR"
      }
    ]
  }
}
```

---

## 📋 기타 개선 사항 (Low Priority)

### 9. JWT 토큰 응답 표준화

**현재**:
```json
{
  "access": "...",
  "refresh": "..."
}
```

**제안**:
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access": "...",
    "refresh": "...",
    "user": {
      "id": 1,
      "username": "user123",
      "email": "user@example.com"
    }
  }
}
```

**장점**: 로그인 시 사용자 정보를 함께 받아 추가 API 호출 불필요

---

### 10. 웹훅 지원 (비동기 분석)

```
POST /api/v1/analyze/
```

**Request**:
```json
{
  "url": "https://example.com",
  "webhook_url": "https://myapp.com/webhook/analysis"
}
```

**즉시 응답**:
```json
{
  "success": true,
  "message": "Analysis started",
  "data": {
    "analysis_id": 123,
    "status": "processing"
  }
}
```

**분석 완료 후 웹훅 호출**:
```
POST https://myapp.com/webhook/analysis
```
```json
{
  "analysis_id": 123,
  "status": "completed",
  "result": { /* 분석 결과 */ }
}
```

---

## 📊 우선순위 요약

### 즉시 구현 필요 (Sprint 1)
1. ✅ API 키 관리 시스템 (전체)
2. ✅ 페이지네이션 개선
3. ✅ 필터링 및 정렬
4. ✅ 에러 응답 상태 코드 개선

### 다음 스프린트 (Sprint 2)
5. ✅ 분석 이력 삭제 기능
6. ✅ 개선된 분석 통계
7. ✅ Rate Limiting

### 장기 개선 (Future)
8. ⏰ 배치 URL 분석
9. ⏰ JWT 토큰 응답 표준화
10. ⏰ 웹훅 지원

---

## 🔧 구현 시 고려사항

### 보안
- API 키는 절대 평문으로 저장하지 않음 (해시 사용)
- Rate Limiting 반드시 구현
- CORS 설정 확인
- SQL Injection 방지

### 성능
- 통계 조회 시 캐싱 고려 (Redis)
- 인덱스 최적화
- N+1 쿼리 방지

### 확장성
- 비동기 작업 큐 고려 (Celery)
- 배치 작업 처리 전략
- 데이터베이스 파티셔닝 고려

---

이 문서는 프론트엔드 개발을 완료하기 위해 백엔드에서 반드시 구현되어야 할 기능들을 정리한 것입니다.
각 기능의 우선순위를 고려하여 순차적으로 구현해주시기 바랍니다.
