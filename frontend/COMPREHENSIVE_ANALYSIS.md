# 프론트엔드-백엔드 연동 종합 분석 문서

이 문서는 백엔드 API 구조를 분석하고, 프론트엔드 코드를 작성하며, 디버깅 전략과 백엔드 개선 사항을 제안한 종합 문서입니다.

---

## 📋 목차

1. [백엔드 분석 요약](#백엔드-분석-요약)
2. [프론트엔드 코드](#프론트엔드-코드)
3. [에러 처리 및 디버깅 전략](#에러-처리-및-디버깅-전략)
4. [백엔드 미구현 로직 제안](#백엔드-미구현-로직-제안)

---

## 🎯 백엔드 분석 요약

### 기술 스택
- **프레임워크**: Django + Django REST Framework
- **인증**: JWT (django-rest-framework-simplejwt)
- **데이터베이스**: PostgreSQL/SQLite
- **LLM**: Google Gemini
- **크롤러**: Selenium
- **RAG**: 커스텀 RAG 서비스

### API 구조

#### ✅ 구현 완료된 API

##### 1. 인증 시스템
```
POST   /api/v1/auth/token/          # 로그인 (토큰 발급)
POST   /api/v1/auth/token/refresh/  # 토큰 갱신
```

**특징**:
- Access Token + Refresh Token 방식
- Simple JWT 라이브러리 사용
- 프론트엔드에서 자동 갱신 인터셉터 구현됨

##### 2. 계정 관리
```
POST   /api/v1/accounts/register/   # 회원가입
GET    /api/v1/accounts/profile/    # 프로필 조회
PUT    /api/v1/accounts/profile/    # 프로필 수정
```

**모델**: Django 기본 User 모델 사용

##### 3. URL 분석 시스템 (핵심 기능)
```
POST   /api/v1/analyze/             # URL 분석 실행
GET    /api/v1/history/             # 분석 이력 조회
GET    /api/v1/results/{id}/        # 분석 상세 조회
GET    /api/v1/statistics/          # 분석 통계
```

**분석 파이프라인**:
1. Selenium으로 URL 크롤링
2. RAG 서비스로 컨텍스트 가져오기 (선택적)
3. Gemini LLM으로 콘텐츠 분석
4. DB에 결과 저장

**분석 항목**:
- `is_clickbait`: 클릭베이트 여부
- `is_hate_speech`: 혐오 표현 포함 여부
- `is_misinformation`: 허위정보 가능성
- `confidence_score`: 전체 신뢰도 (0.0~1.0)
- `risk_level`: 위험도 레벨 (safe, low, medium, high)

#### ❌ 미구현 API

##### 4. API 키 관리
```
/api/v1/api-keys/                   # ❌ 미구현
```
- `apps/api_keys` 디렉토리 존재
- views.py, urls.py 모두 비어있음
- models.py도 비어있음

##### 5. Analytics
```
/api/v1/analytics/                  # ❌ 미구현
```
- `apps/analytics` 디렉토리 존재
- views.py, urls.py 모두 비어있음
- models.py도 비어있음

### 데이터베이스 모델

#### AnalysisResult (detection 앱)
```python
class AnalysisResult(models.Model):
    url = models.URLField(max_length=2048)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # 콘텐츠
    title = models.CharField(max_length=500)
    content = models.TextField()

    # 분석 결과
    is_clickbait = models.BooleanField(default=False)
    is_hate_speech = models.BooleanField(default=False)
    is_misinformation = models.BooleanField(default=False)
    confidence_score = models.FloatField(default=0.0)

    # 상세 정보
    analysis_details = models.JSONField(default=dict)

    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### User (accounts 앱)
- Django 기본 User 모델 사용
- 향후 확장 가능하도록 구조화됨

---

## 💻 프론트엔드 코드

### 디렉토리 구조
```
frontend/
├── src/
│   ├── api/                    # API 클라이언트
│   │   ├── client.js           # ✅ Axios 설정 및 인터셉터
│   │   ├── auth.js             # ✅ 인증 API
│   │   ├── analysis.js         # ✅ 분석 API
│   │   └── apiKeys.js          # 🆕 API 키 관리 (백엔드 구현 필요)
│   ├── utils/                  # 유틸리티
│   │   ├── storage.js          # ✅ 로컬 스토리지 관리
│   │   ├── logger.js           # ✅ 로깅 유틸리티
│   │   └── errorHandler.js    # 🆕 고급 에러 처리
│   ├── components/             # 재사용 컴포넌트
│   ├── pages/                  # 페이지 컴포넌트
│   └── App.jsx
├── .env                        # 환경 변수
└── package.json
```

### 주요 기능 및 구현 상태

#### 1. API 클라이언트 (client.js) ✅
**기능**:
- Axios 인스턴스 설정 (Base URL, Timeout 30초)
- Request Interceptor: Access Token 자동 추가
- Response Interceptor:
  - 401 에러 시 자동 토큰 갱신
  - 토큰 갱신 실패 시 자동 로그아웃
  - 중복 갱신 방지 (큐 메커니즘)
- 에러 표준화

**코드 품질**: ⭐⭐⭐⭐⭐ (매우 우수)

#### 2. 인증 API (auth.js) ✅
**제공 함수**:
- `login(username, password)`: 로그인 + 프로필 자동 조회
- `register(userData)`: 회원가입 + 필드별 에러 처리
- `getProfile()`: 프로필 조회
- `updateProfile(profileData)`: 프로필 수정
- `logout()`: 로그아웃 (로컬 스토리지 정리)

**코드 품질**: ⭐⭐⭐⭐⭐ (매우 우수)

#### 3. 분석 API (analysis.js) ✅
**제공 함수**:
- `analyzeUrl(url)`: URL 분석
- `getAnalysisHistory(limit)`: 분석 이력
- `getAnalysisDetail(analysisId)`: 분석 상세
- `getAnalysisStatistics()`: 분석 통계
- `getRiskLevelText(riskLevel)`: 위험도 한글 변환
- `getRiskLevelColor(riskLevel)`: 위험도 색상

**에러 처리**:
- 400: URL 유효성 검증 에러
- 500 (crawl): 크롤링 실패
- 500 (analyze): LLM 분석 실패

**코드 품질**: ⭐⭐⭐⭐⭐ (매우 우수)

#### 4. API 키 관리 (apiKeys.js) 🆕
**제공 함수** (백엔드 구현 필요):
- `getApiKeys()`: API 키 목록
- `createApiKey(keyData)`: API 키 생성
- `updateApiKey(keyId, updateData)`: API 키 수정
- `deleteApiKey(keyId)`: API 키 삭제
- `regenerateApiKey(keyId)`: API 키 재생성
- `getApiKeyUsage(keyId, period)`: 사용 통계

**상태**: ⚠️ 백엔드 미구현

#### 5. 스토리지 유틸리티 (storage.js) ✅
**제공 함수**:
- `setAccessToken(token)` / `getAccessToken()`
- `setRefreshToken(token)` / `getRefreshToken()`
- `setUserInfo(userInfo)` / `getUserInfo()`
- `clearAuth()`: 모든 인증 정보 삭제
- `isAuthenticated()`: 인증 상태 확인

**코드 품질**: ⭐⭐⭐⭐⭐ (매우 우수)

#### 6. 로깅 유틸리티 (logger.js) ✅
**제공 함수**:
- `logDebug()`, `logInfo()`: 개발 환경만
- `logWarn()`, `logError()`: 모든 환경
- `logApiRequest()`, `logApiResponse()`, `logApiError()`: API 전용

**특징**:
- 타임스탬프 자동 추가
- 카테고리별 분류
- 환경별 로그 레벨 제어

**코드 품질**: ⭐⭐⭐⭐⭐ (매우 우수)

#### 7. 고급 에러 처리 (errorHandler.js) 🆕
**제공 기능**:
- 에러 타입 자동 분류 (NETWORK, AUTHENTICATION, CRAWLER, LLM 등)
- 사용자 친화적 메시지 자동 생성
- 재시도 가능 여부 판단
- Exponential Backoff 재시도 로직
- 필드 에러 포맷팅
- 에러 복구 제안 생성

**사용 예시**:
```javascript
import { handleError, retryWithBackoff } from './utils/errorHandler';

// 에러 처리
try {
  await analyzeUrl(url);
} catch (error) {
  const processed = handleError(error, { context: 'Analysis' });
  alert(processed.userMessage);

  if (processed.retryable) {
    // 재시도 가능한 에러
  }
}

// 자동 재시도
const result = await retryWithBackoff(
  () => analyzeUrl(url),
  { maxRetries: 3 }
);
```

---

## 🛠 에러 처리 및 디버깅 전략

### 에러 처리 구조

#### 1. 에러 표준화

모든 API 에러는 다음 형식으로 표준화됩니다:

```javascript
{
  status: 400,                      // HTTP 상태 코드
  statusText: 'Bad Request',        // 상태 텍스트
  message: '기본 에러 메시지',       // 원본 메시지
  userMessage: '사용자 표시용 메시지', // UI 표시용
  details: { ... },                 // 상세 정보
  fieldErrors: { ... },             // 필드별 에러
  isError: true                     // 에러 플래그
}
```

#### 2. 에러 타입별 처리 전략

| 에러 타입 | 상태 코드 | 처리 방법 | 재시도 가능 |
|----------|----------|---------|-----------|
| 네트워크 에러 | - | 연결 확인 안내 | ✅ |
| 인증 에러 | 401 | 자동 토큰 갱신 → 실패 시 로그인 페이지 | ❌ |
| 권한 에러 | 403 | 권한 없음 안내 | ❌ |
| 유효성 에러 | 400 | 필드별 에러 표시 | ❌ |
| 크롤러 에러 | 502* | URL 확인 안내 | ✅ |
| LLM 에러 | 503* | 서비스 일시 중단 안내 | ✅ |
| 서버 에러 | 500 | 서버 문제 안내 | ✅ |
| 타임아웃 | 408, 504 | 재시도 안내 | ✅ |

*현재는 500으로 반환되지만, 백엔드 개선 필요

#### 3. 자동 재시도 전략

```javascript
const result = await retryWithBackoff(
  () => analyzeUrl(url),
  {
    maxRetries: 3,           // 최대 3회 재시도
    initialDelay: 1000,      // 첫 재시도: 1초 대기
    maxDelay: 10000,         // 최대 대기: 10초
    // 지연 시간: 1초 → 2초 → 4초 → 8초 (Exponential Backoff)
  }
);
```

### 디버깅 전략

#### 1. 로깅 포인트

##### API 레벨 (자동)
```
[2024-01-01T00:00:00.000Z] [DEBUG] [API] POST /api/v1/analyze/ { url: "..." }
[2024-01-01T00:00:00.500Z] [DEBUG] [API] POST /api/v1/analyze/ - 200 { success: true }
```

##### 컴포넌트 레벨
```javascript
import { logDebug, logError } from './utils/logger';

useEffect(() => {
  logDebug('Component', 'Analysis page mounted');
}, []);

useEffect(() => {
  logDebug('State', 'Analysis result updated', result);
}, [result]);
```

#### 2. 디버깅 체크리스트

**API 호출 문제**:
1. ✅ Network 탭에서 요청 확인
2. ✅ Console에서 `logApiRequest` 로그 확인
3. ✅ Access Token 확인: `localStorage.getItem('access_token')`
4. ✅ Authorization 헤더 형식 확인: `Bearer <token>`

**인증 문제**:
1. ✅ 토큰 존재 여부: `isAuthenticated()`
2. ✅ 토큰 만료 확인
3. ✅ 토큰 갱신 로직 동작 확인

**데이터 문제**:
1. ✅ API 응답 데이터 구조 확인 (Network 탭)
2. ✅ Serializer 필드명 확인
3. ✅ 컴포넌트 상태 확인 (React DevTools)

#### 3. 일반적인 문제 해결

**문제**: 로그인 후 토큰이 저장되지 않음
```javascript
// 확인:
// 1. login 함수에서 setAccessToken 호출 확인
// 2. 브라우저 로컬 스토리지 권한 확인
// 3. 프라이빗 모드가 아닌지 확인
```

**문제**: API 요청 시 401 에러 계속 발생
```javascript
// 확인:
// 1. Access Token이 있는지: localStorage.getItem('access_token')
// 2. Refresh Token이 있는지: localStorage.getItem('refresh_token')
// 3. 토큰 갱신 인터셉터 로직 확인
```

**문제**: 토큰 갱신이 작동하지 않음
```javascript
// 확인:
// 1. Refresh Token이 유효한지
// 2. /api/v1/auth/token/refresh/ 엔드포인트 응답 확인
// 3. 인터셉터의 isRefreshing 플래그 확인
```

---

## 🚀 백엔드 미구현 로직 제안

상세 내용은 `BACKEND_TODO.md` 파일을 참조하세요.

### 우선순위별 구현 사항

#### 🔴 높음 (즉시 구현 필요)

##### 1. API 키 관리 시스템 ⭐⭐⭐⭐⭐
- **상태**: 앱은 존재하나 완전히 비어있음
- **필요 API**:
  - `GET /api/v1/api-keys/` - 키 목록
  - `POST /api/v1/api-keys/` - 키 생성
  - `PUT /api/v1/api-keys/{id}/` - 키 수정
  - `DELETE /api/v1/api-keys/{id}/` - 키 삭제
  - `POST /api/v1/api-keys/{id}/regenerate/` - 키 재생성
  - `GET /api/v1/api-keys/{id}/usage/` - 사용 통계
- **보안 요구사항**:
  - API 키는 평문 저장 금지 (SHA-256 해시 사용)
  - 생성 시 1회만 전체 키 반환
  - Rate Limiting 필수
- **프론트엔드**: 이미 준비됨 (`apiKeys.js`)

##### 2. 페이지네이션 개선 ⭐⭐⭐⭐
- **현재**: `?limit=20` (오프셋 없음)
- **필요**: `?page=1&page_size=20`
- **이유**: 무한 스크롤, 페이지 내비게이션 구현 불가

##### 3. 에러 응답 상태 코드 개선 ⭐⭐⭐⭐
- **현재**: Crawler, LLM 실패 모두 500
- **필요**:
  - Crawler 실패: 502 Bad Gateway
  - LLM 실패: 503 Service Unavailable
  - 에러 타입 필드 추가: `error_type`, `error_code`
- **이유**: 프론트엔드에서 에러 타입별 처리 가능

##### 4. 필터링 및 정렬 ⭐⭐⭐
- **필요 파라미터**:
  - `risk_level=high`
  - `is_safe=false`
  - `is_clickbait=true`
  - `ordering=-created_at`
  - `search=example.com`
- **구현**: DjangoFilterBackend 사용

#### 🟡 중간 (다음 스프린트)

##### 5. 분석 이력 삭제 ⭐⭐⭐
- `DELETE /api/v1/results/{id}/` - 단일 삭제
- `POST /api/v1/results/bulk-delete/` - 대량 삭제

##### 6. 개선된 분석 통계 ⭐⭐⭐
- 기간별 통계 (`?period=30d`)
- 위험도 분포
- 일별 통계
- 도메인별 통계
- 시간대별 분포

##### 7. Rate Limiting 정보 ⭐⭐
- 응답 헤더: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

#### 🟢 낮음 (장기 개선)

##### 8. 배치 URL 분석 ⭐
- 여러 URL 동시 분석
- CSV 업로드 지원

##### 9. JWT 토큰 응답 표준화 ⭐
- 로그인 시 사용자 정보 함께 반환
- 추가 API 호출 불필요

##### 10. 웹훅 지원 ⭐
- 비동기 분석 처리
- 완료 시 콜백

---

## 📊 코드 품질 평가

### 기존 프론트엔드 코드

| 모듈 | 완성도 | 코드 품질 | 개선 필요 사항 |
|-----|-------|---------|--------------|
| api/client.js | 100% | ⭐⭐⭐⭐⭐ | 없음 |
| api/auth.js | 100% | ⭐⭐⭐⭐⭐ | 없음 |
| api/analysis.js | 100% | ⭐⭐⭐⭐⭐ | 없음 |
| utils/storage.js | 100% | ⭐⭐⭐⭐⭐ | 없음 |
| utils/logger.js | 100% | ⭐⭐⭐⭐⭐ | 없음 |

**총평**: 기존 프론트엔드 코드는 매우 잘 작성되어 있으며, 산업 표준을 충족합니다.

### 추가 작성된 코드

| 파일 | 용도 | 백엔드 의존성 |
|-----|------|-------------|
| api/apiKeys.js | API 키 관리 | ⚠️ 백엔드 구현 필요 |
| utils/errorHandler.js | 고급 에러 처리 | ✅ 독립적 |

---

## 🎯 다음 단계

### 프론트엔드 팀
1. ✅ 기존 API 연동 코드 검토 완료
2. ✅ 에러 처리 유틸리티 통합
3. ⏳ UI 컴포넌트 개발
4. ⏳ API 키 관리 페이지 개발 (백엔드 완료 후)

### 백엔드 팀
1. ⚠️ API 키 관리 시스템 구현 (최우선)
2. ⚠️ 에러 응답 상태 코드 개선
3. ⚠️ 페이지네이션 개선
4. ⏳ 필터링 및 정렬 기능
5. ⏳ 개선된 통계 API

---

## 📚 참고 문서

- `FRONTEND_DEVELOPMENT_GUIDE.md`: 프론트엔드 개발 가이드 (이미 존재)
- `BACKEND_TODO.md`: 백엔드 미구현 기능 상세 스펙
- `src/api/`: API 클라이언트 코드
- `src/utils/`: 유틸리티 함수

---

## ✅ 체크리스트

### 프론트엔드
- [x] API 클라이언트 설정
- [x] 인증 API 구현
- [x] 분석 API 구현
- [x] 자동 토큰 갱신
- [x] 에러 처리
- [x] 로깅 시스템
- [x] 스토리지 관리
- [x] 고급 에러 처리 유틸리티
- [x] API 키 관리 클라이언트 (백엔드 대기)
- [ ] UI 컴포넌트
- [ ] 페이지 구현

### 백엔드
- [x] JWT 인증
- [x] 회원가입/로그인
- [x] 프로필 관리
- [x] URL 분석 파이프라인
- [x] 분석 이력 조회
- [x] 기본 통계
- [ ] API 키 관리 시스템
- [ ] 페이지네이션
- [ ] 필터링/정렬
- [ ] 개선된 통계
- [ ] 에러 코드 표준화

---

**작성일**: 2024
**작성자**: 프론트엔드-백엔드 연동 분석팀
**버전**: 1.0
