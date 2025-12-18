# URL Analysis Service - API Documentation

## 목차
1. [인증 방법](#인증-방법)
2. [사용 가능한 API](#사용-가능한-api)
3. [API 키 관리](#api-키-관리)
4. [URL 분석 API](#url-분석-api)
5. [Rate Limiting](#rate-limiting)
6. [에러 처리](#에러-처리)

---

## 인증 방법

본 서비스는 두 가지 인증 방법을 지원합니다:

### 1. JWT 인증 (웹 애플리케이션용)

**토큰 발급:**
```bash
POST /api/v1/auth/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**응답:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**API 호출 시 사용:**
```bash
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### 2. API Key 인증 (외부 개발자용)

**API 키 발급 후 사용:**

방법 1: Authorization 헤더
```bash
Authorization: Bearer sk_live_xxxxxxxxxxxxx
```

방법 2: X-API-Key 헤더
```bash
X-API-Key: sk_live_xxxxxxxxxxxxx
```

---

## 사용 가능한 API

### URL 분석 서비스

#### 1. URL 분석 요청
피싱/스미싱 URL을 분석합니다.

```bash
POST /api/v1/analyze/
```

**요청 예시:**
```bash
curl -X POST https://your-domain.com/api/v1/analyze/ \
  -H "Authorization: Bearer sk_live_xxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://suspicious-website.com"
  }'
```

**요청 Body:**
```json
{
  "url": "https://suspicious-website.com"
}
```

**응답 예시:**
```json
{
  "success": true,
  "message": "Analysis completed successfully",
  "data": {
    "id": 123,
    "url": "https://suspicious-website.com",
    "is_malicious": true,
    "risk_score": 85,
    "analysis_summary": "이 사이트는 피싱 사이트로 의심됩니다...",
    "detected_threats": [
      "Phishing",
      "Fake Login Form"
    ],
    "created_at": "2025-12-18T15:30:00Z"
  }
}
```

#### 2. 분석 이력 조회
사용자의 분석 이력을 조회합니다.

```bash
GET /api/v1/history/?limit=20
```

**요청 예시:**
```bash
curl -X GET "https://your-domain.com/api/v1/history/?limit=20" \
  -H "Authorization: Bearer sk_live_xxxxxxxxxxxxx"
```

**응답 예시:**
```json
{
  "success": true,
  "count": 20,
  "data": [
    {
      "id": 123,
      "url": "https://suspicious-website.com",
      "is_malicious": true,
      "risk_score": 85,
      "created_at": "2025-12-18T15:30:00Z"
    }
  ]
}
```

#### 3. 분석 결과 상세 조회
특정 분석 결과의 상세 정보를 조회합니다.

```bash
GET /api/v1/results/{analysis_id}/
```

**요청 예시:**
```bash
curl -X GET https://your-domain.com/api/v1/results/123/ \
  -H "Authorization: Bearer api 키"
```

**응답 예시:**
```json
{
  "success": true,
  "data": {
    "id": 123,
    "url": "https://suspicious-website.com",
    "is_malicious": true,
    "risk_score": 85,
    "analysis_summary": "상세 분석 내용...",
    "detected_threats": ["Phishing", "Fake Login Form"],
    "technical_details": {
      "html_content": "...",
      "suspicious_keywords": ["login", "password"],
      "similar_phishing_cases": [...]
    },
    "created_at": "2025-12-18T15:30:00Z"
  }
}
```

#### 4. 통계 조회
사용자의 분석 통계를 조회합니다.

```bash
GET /api/v1/statistics/
```

**요청 예시:**
```bash
curl -X GET https://your-domain.com/api/v1/statistics/ \
  -H "Authorization: Bearer sk_live_xxxxxxxxxxxxx"
```

**응답 예시:**
```json
{
  "success": true,
  "data": {
    "total_analyses": 150,
    "malicious_count": 45,
    "safe_count": 105,
    "malicious_rate": 30.0
  }
}
```

---

## API 키 관리

### 1. API 키 목록 조회

```bash
GET /api/v1/api-keys/
```

**요청 예시 (JWT 인증 필요):**
```bash
curl -X GET https://your-domain.com/api/v1/api-keys/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**응답:**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 1,
      "name": "Production API Key",
      "key_prefix": "sk_live_",
      "masked_key": "sk_live_...****",
      "is_active": true,
      "total_requests": 1250,
      "usage_today": 45,
      "last_used_at": "2025-12-18T15:30:00Z",
      "rate_limit_per_minute": 60,
      "rate_limit_per_day": 10000,
      "created_at": "2025-12-01T10:00:00Z"
    }
  ]
}
```

### 2. API 키 생성

```bash
POST /api/v1/api-keys/
```

**요청 예시:**
```bash
curl -X POST https://your-domain.com/api/v1/api-keys/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Production Key",
    "rate_limit_per_minute": 60,
    "rate_limit_per_day": 10000
  }'
```

**요청 Body:**
```json
{
  "name": "My Production Key",
  "rate_limit_per_minute": 60,
  "rate_limit_per_day": 10000
}
```

**응답 (⚠️ 평문 키는 이 시점에만 반환됩니다!):**
```json
{
  "success": true,
  "message": "API key created successfully. Please save the key, it will not be shown again.",
  "data": {
    "id": 1,
    "name": "My Production Key",
    "raw_key": "api 키",
    "key_prefix": "sk_live_",
    "is_active": true,
    "rate_limit_per_minute": 60,
    "rate_limit_per_day": 10000,
    "created_at": "2025-12-18T15:30:00Z"
  }
}
```

**⚠️ 중요: API 키는 생성 시 1회만 반환되며, 이후 다시 조회할 수 없습니다. 반드시 안전한 곳에 저장하세요!**

### 3. API 키 수정

```bash
PUT /api/v1/api-keys/{api_key_id}/
```

**요청 예시:**
```bash
curl -X PUT https://your-domain.com/api/v1/api-keys/1/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Key Name",
    "is_active": true,
    "rate_limit_per_minute": 100
  }'
```

### 4. API 키 삭제

```bash
DELETE /api/v1/api-keys/{api_key_id}/
```

**요청 예시:**
```bash
curl -X DELETE https://your-domain.com/api/v1/api-keys/1/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### 5. API 키 재생성

기존 키를 무효화하고 새로운 키를 생성합니다.

```bash
POST /api/v1/api-keys/{api_key_id}/regenerate/
```

**요청 예시:**
```bash
curl -X POST https://your-domain.com/api/v1/api-keys/1/regenerate/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**응답:**
```json
{
  "success": true,
  "message": "API key regenerated successfully. Please save the new key, it will not be shown again.",
  "data": {
    "id": 2,
    "name": "My Production Key",
    "raw_key": "api 키",
    "key_prefix": "sk_live_",
    "is_active": true,
    "rate_limit_per_minute": 60,
    "rate_limit_per_day": 10000,
    "created_at": "2025-12-18T16:00:00Z"
  }
}
```

### 6. API 키 사용 통계

```bash
GET /api/v1/api-keys/{api_key_id}/usage/?days=7
```

**요청 예시:**
```bash
curl -X GET "https://your-domain.com/api/v1/api-keys/1/usage/?days=7" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**응답:**
```json
{
  "success": true,
  "data": {
    "total_requests": 1250,
    "requests_today": 45,
    "requests_this_week": 320,
    "requests_this_month": 1250,
    "last_used_at": "2025-12-18T15:30:00Z",
    "endpoint_stats": {
      "/api/v1/analyze/": 800,
      "/api/v1/history/": 300,
      "/api/v1/results/": 150
    },
    "daily_stats": [
      {
        "date": "2025-12-12",
        "count": 50
      },
      {
        "date": "2025-12-13",
        "count": 45
      }
    ],
    "recent_logs": [
      {
        "id": 1,
        "endpoint": "/api/v1/analyze/",
        "method": "POST",
        "status_code": 200,
        "ip_address": "192.168.1.1",
        "created_at": "2025-12-18T15:30:00Z"
      }
    ]
  }
}
```

---

## Rate Limiting

### 기본 제한

- **분당 요청 제한**: 60회 (기본값, API 키별 설정 가능)
- **일당 요청 제한**: 10,000회 (기본값, API 키별 설정 가능)

### Rate Limit 초과 시 응답

```json
{
  "error": true,
  "message": "Rate limit exceeded: 60 requests per minute",
  "wait": 60
}
```

HTTP Status: `429 Too Many Requests`

---

## 에러 처리

### 일반 에러 응답 형식

```json
{
  "error": true,
  "message": "에러 메시지",
  "details": "상세 에러 정보"
}
```

### HTTP Status Codes

- `200 OK`: 요청 성공
- `201 Created`: 리소스 생성 성공
- `400 Bad Request`: 잘못된 요청
- `401 Unauthorized`: 인증 실패
- `403 Forbidden`: 권한 없음
- `404 Not Found`: 리소스를 찾을 수 없음
- `429 Too Many Requests`: Rate limit 초과
- `500 Internal Server Error`: 서버 에러

### 일반적인 에러 예시

**인증 실패:**
```json
{
  "error": true,
  "message": "Invalid API key"
}
```

**Rate Limit 초과:**
```json
{
  "error": true,
  "message": "Rate limit exceeded: 60 requests per minute",
  "wait": 60
}
```

**잘못된 요청:**
```json
{
  "error": true,
  "message": "Invalid request data",
  "details": {
    "url": ["This field is required."]
  }
}
```

---

## 예제 코드

### Python

```python
import requests

API_KEY = "sk_live_your_api_key_here"
BASE_URL = "https://your-domain.com/api/v1"

# URL 분석
def analyze_url(url):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"url": url}

    response = requests.post(
        f"{BASE_URL}/analyze/",
        headers=headers,
        json=data
    )

    return response.json()

# 사용
result = analyze_url("https://suspicious-website.com")
print(result)
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

const API_KEY = 'sk_live_your_api_key_here';
const BASE_URL = 'https://your-domain.com/api/v1';

// URL 분석
async function analyzeUrl(url) {
  try {
    const response = await axios.post(
      `${BASE_URL}/analyze/`,
      { url },
      {
        headers: {
          'Authorization': `Bearer ${API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data;
  } catch (error) {
    console.error('Error:', error.response.data);
    throw error;
  }
}

// 사용
analyzeUrl('https://suspicious-website.com')
  .then(result => console.log(result))
  .catch(err => console.error(err));
```

### cURL

```bash
# URL 분석
curl -X POST https://your-domain.com/api/v1/analyze/ \
  -H "Authorization: Bearer sk_live_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious-website.com"}'

# 분석 이력 조회
curl -X GET "https://your-domain.com/api/v1/history/?limit=10" \
  -H "Authorization: Bearer sk_live_your_api_key_here"

# API 키 생성 (JWT 토큰 필요)
curl -X POST https://your-domain.com/api/v1/api-keys/ \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My API Key",
    "rate_limit_per_minute": 60,
    "rate_limit_per_day": 10000
  }'
```

---

## 보안 모범 사례

1. **API 키 보안**
   - API 키는 절대 공개 저장소에 커밋하지 마세요
   - 환경 변수로 관리하세요
   - 정기적으로 키를 재생성하세요

2. **HTTPS 사용**
   - 모든 API 요청은 HTTPS를 통해 이루어져야 합니다

3. **Rate Limiting 준수**
   - Rate limit을 초과하지 않도록 요청 속도를 조절하세요
   - 필요시 더 높은 한도를 요청하세요

4. **에러 처리**
   - 모든 API 호출에 적절한 에러 처리를 구현하세요
   - 429 에러 시 재시도 로직을 구현하세요

---

## 지원

문의사항이나 도움이 필요하신 경우:
- 이메일: support@your-domain.com
- GitHub Issues: https://github.com/your-repo/issues
