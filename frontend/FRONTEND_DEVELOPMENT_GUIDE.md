# 프론트엔드 개발 가이드

## 📋 목차

1. [백엔드 API 구조 분석](#백엔드-api-구조-분석)
2. [프론트엔드 코드 구조](#프론트엔드-코드-구조)
3. [에러 처리 및 디버깅 전략](#에러-처리-및-디버깅-전략)
4. [백엔드 개선 사항](#백엔드-개선-사항)

---

## 백엔드 API 구조 분석

### API Base URL
- **개발 환경**: `http://localhost:8000`
- **운영 환경**: 환경 변수 `VITE_API_BASE_URL` 설정 필요

### 인증 방식
- **JWT (JSON Web Token)** 기반 인증
- Access Token + Refresh Token 방식
- Access Token: 요청 헤더에 `Authorization: Bearer <token>` 형식으로 전송
- Refresh Token: Access Token 만료 시 자동 갱신

### API 엔드포인트

#### 1. 인증 (Authentication)

##### 로그인
```
POST /api/v1/auth/token/
```
**Request Body:**
```json
{
  "username": "user123",
  "password": "password123"
}
```
**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

##### 토큰 갱신
```
POST /api/v1/auth/token/refresh/
```
**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 2. 계정 관리 (Accounts)

##### 회원가입
```
POST /api/v1/accounts/register/
```
**권한**: AllowAny (인증 불필요)

**Request Body:**
```json
{
  "username": "user123",         // 필수
  "email": "user@example.com",   // 선택
  "password": "password123",     // 필수
  "password_check": "password123", // 필수
  "first_name": "홍",            // 선택
  "last_name": "길동"            // 선택
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com"
  }
}
```

**Error Response (400):**
```json
{
  "error": true,
  "message": "Invalid registration data",
  "details": {
    "password": ["Passwords do not match"],
    "username": ["This field is required."]
  }
}
```

##### 프로필 조회
```
GET /api/v1/accounts/profile/
```
**권한**: IsAuthenticated

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "first_name": "홍",
    "last_name": "길동",
    "date_joined": "2024-01-01T00:00:00Z"
  }
}
```

##### 프로필 수정
```
PUT /api/v1/accounts/profile/
```
**권한**: IsAuthenticated

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "first_name": "김",
  "last_name": "철수"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "id": 1,
    "username": "user123",
    "email": "newemail@example.com",
    "first_name": "김",
    "last_name": "철수",
    "date_joined": "2024-01-01T00:00:00Z"
  }
}
```

#### 3. URL 분석 (Detection)

##### URL 분석
```
POST /api/v1/analyze/
```
**권한**: IsAuthenticated

**Request Body:**
```json
{
  "url": "https://example.com/article"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Analysis completed successfully",
  "data": {
    "id": 1,
    "url": "https://example.com/article",
    "user_email": "user@example.com",
    "title": "기사 제목",
    "content": "기사 내용...",
    "is_clickbait": false,
    "is_hate_speech": false,
    "is_misinformation": false,
    "is_safe": true,
    "confidence_score": 0.95,
    "risk_level": "safe",
    "analysis_details": {
      "clickbait_reason": "...",
      "hate_speech_reason": "...",
      "misinformation_reason": "..."
    },
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

**Error Responses:**

- **400 Bad Request**: 잘못된 URL
```json
{
  "error": true,
  "message": "Invalid request data",
  "details": {
    "url": ["Enter a valid URL."]
  }
}
```

- **500 Internal Server Error (Crawler)**: 크롤링 실패
```json
{
  "error": true,
  "message": "Failed to crawl URL",
  "details": "Connection timeout"
}
```

- **500 Internal Server Error (LLM)**: 분석 실패
```json
{
  "error": true,
  "message": "Failed to analyze content",
  "details": "LLM service unavailable"
}
```

##### 분석 이력 조회
```
GET /api/v1/history/?limit=20
```
**권한**: IsAuthenticated

**Query Parameters:**
- `limit`: 조회 개수 (기본값: 20, 최대: 100)

**Success Response (200):**
```json
{
  "success": true,
  "count": 15,
  "data": [
    {
      "id": 1,
      "url": "https://example.com/article",
      "title": "기사 제목",
      "is_clickbait": false,
      "is_hate_speech": false,
      "is_misinformation": false,
      "is_safe": true,
      "confidence_score": 0.95,
      "risk_level": "safe",
      "created_at": "2024-01-01T00:00:00Z"
    }
    // ... more items
  ]
}
```

##### 분석 결과 상세 조회
```
GET /api/v1/results/{analysis_id}/
```
**권한**: IsAuthenticated (본인 또는 관리자만 조회 가능)

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "url": "https://example.com/article",
    "user_email": "user@example.com",
    "title": "기사 제목",
    "content": "기사 내용...",
    "is_clickbait": false,
    "is_hate_speech": false,
    "is_misinformation": false,
    "is_safe": true,
    "confidence_score": 0.95,
    "risk_level": "safe",
    "analysis_details": { ... },
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

**Error Responses:**

- **404 Not Found**:
```json
{
  "error": true,
  "message": "Analysis result not found"
}
```

- **403 Forbidden**:
```json
{
  "error": true,
  "message": "Permission denied"
}
```

##### 분석 통계
```
GET /api/v1/statistics/
```
**권한**: IsAuthenticated

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "total_analyses": 100,
    "clickbait_detected": 15,
    "hate_speech_detected": 5,
    "misinformation_detected": 10,
    "safe_content": 70
  }
}
```

---

## 프론트엔드 코드 구조

### 디렉토리 구조

```
frontend/
├── src/
│   ├── api/                 # API 클라이언트 및 서비스
│   │   ├── client.js        # Axios 설정 및 인터셉터
│   │   ├── auth.js          # 인증 API
│   │   └── analysis.js      # 분석 API
│   ├── utils/               # 유틸리티 함수
│   │   ├── storage.js       # 로컬 스토리지 관리
│   │   └── logger.js        # 로깅 유틸리티
│   ├── components/          # 재사용 가능한 컴포넌트
│   ├── pages/               # 페이지 컴포넌트
│   └── App.jsx              # 메인 앱 컴포넌트
├── .env                     # 환경 변수
└── package.json
```

### 주요 모듈 설명

#### 1. API 클라이언트 (`src/api/client.js`)

**기능:**
- Axios 인스턴스 설정
- Request/Response 인터셉터
- 자동 토큰 갱신
- 에러 표준화

**주요 특징:**
- Base URL 설정 (환경 변수)
- Timeout: 30초
- Access Token 자동 추가
- 401 에러 시 자동 토큰 갱신
- 토큰 갱신 실패 시 자동 로그아웃
- 요청/응답 로깅

**사용 예시:**
```javascript
import apiClient from './api/client';

// GET 요청
const response = await apiClient.get('/api/v1/statistics/');

// POST 요청
const response = await apiClient.post('/api/v1/analyze/', { url: 'https://example.com' });
```

#### 2. 인증 API (`src/api/auth.js`)

**제공 함수:**

##### `login(username, password)`
```javascript
import { login } from './api/auth';

try {
  const result = await login('user123', 'password123');
  console.log('로그인 성공:', result.user);
} catch (error) {
  console.error('로그인 실패:', error.userMessage);
}
```

##### `register(userData)`
```javascript
import { register } from './api/auth';

try {
  const result = await register({
    username: 'user123',
    email: 'user@example.com',
    password: 'password123',
    password_check: 'password123',
    first_name: '홍',
    last_name: '길동'
  });
  console.log('회원가입 성공:', result.user);
} catch (error) {
  console.error('회원가입 실패:', error.userMessage);
  console.error('필드 에러:', error.fieldErrors);
}
```

##### `getProfile()`
```javascript
import { getProfile } from './api/auth';

try {
  const profile = await getProfile();
  console.log('프로필:', profile);
} catch (error) {
  console.error('프로필 조회 실패:', error.userMessage);
}
```

##### `updateProfile(profileData)`
```javascript
import { updateProfile } from './api/auth';

try {
  const result = await updateProfile({
    email: 'newemail@example.com',
    first_name: '김',
    last_name: '철수'
  });
  console.log('프로필 수정 성공:', result.user);
} catch (error) {
  console.error('프로필 수정 실패:', error.userMessage);
}
```

##### `logout()`
```javascript
import { logout } from './api/auth';

logout(); // 로컬 스토리지의 토큰 및 사용자 정보 삭제
```

#### 3. 분석 API (`src/api/analysis.js`)

**제공 함수:**

##### `analyzeUrl(url)`
```javascript
import { analyzeUrl } from './api/analysis';

try {
  const result = await analyzeUrl('https://example.com/article');
  console.log('분석 결과:', result.result);
  console.log('위험도:', result.result.risk_level);
  console.log('안전 여부:', result.result.is_safe);
} catch (error) {
  console.error('분석 실패:', error.userMessage);
}
```

##### `getAnalysisHistory(limit = 20)`
```javascript
import { getAnalysisHistory } from './api/analysis';

try {
  const result = await getAnalysisHistory(50);
  console.log('총 개수:', result.count);
  console.log('분석 이력:', result.results);
} catch (error) {
  console.error('이력 조회 실패:', error.userMessage);
}
```

##### `getAnalysisDetail(analysisId)`
```javascript
import { getAnalysisDetail } from './api/analysis';

try {
  const result = await getAnalysisDetail(1);
  console.log('분석 상세:', result.result);
} catch (error) {
  console.error('상세 조회 실패:', error.userMessage);
}
```

##### `getAnalysisStatistics()`
```javascript
import { getAnalysisStatistics } from './api/analysis';

try {
  const result = await getAnalysisStatistics();
  console.log('통계:', result.statistics);
  console.log('총 분석 수:', result.statistics.total_analyses);
} catch (error) {
  console.error('통계 조회 실패:', error.userMessage);
}
```

##### 헬퍼 함수

**`getRiskLevelText(riskLevel)`** - 위험도를 한글로 변환
```javascript
import { getRiskLevelText } from './api/analysis';

console.log(getRiskLevelText('safe'));    // "안전"
console.log(getRiskLevelText('low'));     // "낮음"
console.log(getRiskLevelText('medium'));  // "보통"
console.log(getRiskLevelText('high'));    // "높음"
```

**`getRiskLevelColor(riskLevel)`** - 위험도 색상 클래스
```javascript
import { getRiskLevelColor } from './api/analysis';

console.log(getRiskLevelColor('safe'));    // "success"
console.log(getRiskLevelColor('low'));     // "info"
console.log(getRiskLevelColor('medium'));  // "warning"
console.log(getRiskLevelColor('high'));    // "danger"
```

#### 4. 스토리지 유틸리티 (`src/utils/storage.js`)

**제공 함수:**
- `setAccessToken(token)` - Access Token 저장
- `getAccessToken()` - Access Token 조회
- `setRefreshToken(token)` - Refresh Token 저장
- `getRefreshToken()` - Refresh Token 조회
- `setUserInfo(userInfo)` - 사용자 정보 저장
- `getUserInfo()` - 사용자 정보 조회
- `clearAuth()` - 모든 인증 정보 삭제
- `isAuthenticated()` - 인증 상태 확인

**사용 예시:**
```javascript
import { isAuthenticated, getUserInfo } from './utils/storage';

if (isAuthenticated()) {
  const user = getUserInfo();
  console.log('로그인된 사용자:', user);
}
```

#### 5. 로깅 유틸리티 (`src/utils/logger.js`)

**제공 함수:**
- `logDebug(category, message, data)` - 디버그 로그 (개발 환경만)
- `logInfo(category, message, data)` - 정보 로그 (개발 환경만)
- `logWarn(category, message, data)` - 경고 로그
- `logError(category, message, error)` - 에러 로그
- `logApiRequest(method, url, data)` - API 요청 로그
- `logApiResponse(method, url, status, data)` - API 응답 로그
- `logApiError(method, url, error)` - API 에러 로그

**특징:**
- 개발 환경에서만 DEBUG, INFO 로그 출력
- 모든 환경에서 WARN, ERROR 로그 출력
- 타임스탬프 자동 추가
- 카테고리별 분류

---

## 에러 처리 및 디버깅 전략

### 에러 처리 구조

#### 1. API 에러 표준화

모든 API 에러는 다음 형식으로 표준화됩니다:

```javascript
{
  status: 400,                    // HTTP 상태 코드
  statusText: 'Bad Request',      // 상태 텍스트
  message: '사용자 친화적 메시지',  // 기본 에러 메시지
  userMessage: '사용자 표시용 메시지', // UI에 표시할 메시지
  details: { ... },               // 상세 에러 정보
  fieldErrors: { ... },           // 필드별 에러 (회원가입, 프로필 수정 등)
  isError: true                   // 에러 여부 플래그
}
```

#### 2. 에러 처리 패턴

##### 기본 패턴
```javascript
import { analyzeUrl } from './api/analysis';

const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
const [result, setResult] = useState(null);

const handleAnalyze = async (url) => {
  setLoading(true);
  setError(null);
  setResult(null);

  try {
    const response = await analyzeUrl(url);
    setResult(response.result);
  } catch (err) {
    setError(err.userMessage || '오류가 발생했습니다.');
    console.error('분석 에러:', err);
  } finally {
    setLoading(false);
  }
};
```

##### 폼 검증 에러 처리
```javascript
import { register } from './api/auth';

const [fieldErrors, setFieldErrors] = useState({});

const handleRegister = async (formData) => {
  try {
    const response = await register(formData);
    // 성공 처리
  } catch (err) {
    // 필드별 에러 표시
    if (err.fieldErrors) {
      setFieldErrors(err.fieldErrors);
    }
    // 전체 에러 메시지
    setError(err.userMessage);
  }
};

// UI에서 필드별 에러 표시
<input name="username" />
{fieldErrors.username && (
  <span className="error">{fieldErrors.username[0]}</span>
)}
```

#### 3. 에러 타입별 처리

##### 네트워크 에러
```javascript
try {
  await analyzeUrl(url);
} catch (error) {
  if (!error.status) {
    // 네트워크 연결 실패
    showMessage('네트워크 연결을 확인해주세요.');
  }
}
```

##### 인증 에러 (401)
```javascript
// client.js의 인터셉터에서 자동 처리됨
// - 토큰 갱신 시도
// - 갱신 실패 시 자동 로그아웃 및 로그인 페이지로 리다이렉트
```

##### 권한 에러 (403)
```javascript
try {
  await getAnalysisDetail(analysisId);
} catch (error) {
  if (error.status === 403) {
    showMessage('접근 권한이 없습니다.');
  }
}
```

##### 서버 에러 (500)
```javascript
try {
  await analyzeUrl(url);
} catch (error) {
  if (error.status === 500) {
    if (error.message.includes('crawl')) {
      showMessage('URL을 가져올 수 없습니다. URL을 확인해주세요.');
    } else {
      showMessage('서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
    }
  }
}
```

### 디버깅 전략

#### 1. 로깅 포인트

##### API 요청/응답 로깅
```javascript
// client.js에서 자동 로깅됨
// [2024-01-01T00:00:00.000Z] [DEBUG] [API] POST /api/v1/analyze/ { url: "..." }
// [2024-01-01T00:00:00.500Z] [DEBUG] [API] POST /api/v1/analyze/ - 200 { success: true, ... }
```

##### 커스텀 로깅
```javascript
import { logDebug, logError } from './utils/logger';

// 컴포넌트 마운트 시
useEffect(() => {
  logDebug('Component', 'Analysis page mounted');
}, []);

// 상태 변경 시
useEffect(() => {
  logDebug('State', 'Analysis result updated', result);
}, [result]);

// 에러 발생 시
try {
  // ...
} catch (error) {
  logError('Analysis', 'Failed to analyze URL', error);
}
```

#### 2. 디버깅 체크리스트

##### API 호출 문제
1. **요청이 전송되지 않는 경우**
   - 개발자 도구 Network 탭 확인
   - `logApiRequest` 로그 확인
   - axios 클라이언트 설정 확인

2. **401 에러 발생**
   - Access Token 확인: `localStorage.getItem('access_token')`
   - 토큰 만료 여부 확인
   - 로그인 상태 확인: `isAuthenticated()`

3. **CORS 에러 발생**
   - 백엔드 CORS 설정 확인
   - API Base URL 확인 (.env 파일)

4. **응답이 오지 않는 경우**
   - 타임아웃 설정 확인 (현재 30초)
   - 백엔드 서버 상태 확인
   - 네트워크 연결 확인

##### 데이터 문제
1. **데이터가 표시되지 않는 경우**
   - `logApiResponse` 로그에서 응답 데이터 구조 확인
   - 컴포넌트 상태 확인 (React DevTools)
   - 데이터 매핑 로직 확인

2. **잘못된 데이터가 표시되는 경우**
   - API 응답 데이터 구조 확인
   - Serializer 필드명 확인
   - 프론트엔드 데이터 변환 로직 확인

#### 3. 디버깅 도구

##### React DevTools
- 컴포넌트 상태 및 props 확인
- 리렌더링 추적

##### Browser DevTools
- Network 탭: API 요청/응답 확인
- Console 탭: 로그 및 에러 확인
- Application 탭: 로컬 스토리지 확인 (토큰, 사용자 정보)

##### 로컬 스토리지 직접 확인
```javascript
// Console에서 직접 확인
localStorage.getItem('access_token')
localStorage.getItem('refresh_token')
localStorage.getItem('user_info')
```

#### 4. 일반적인 문제 해결

##### 로그인 후 토큰이 저장되지 않음
```javascript
// 확인 사항:
// 1. login 함수에서 setAccessToken, setRefreshToken 호출 확인
// 2. 로컬 스토리지 권한 확인
// 3. 프라이빗 모드가 아닌지 확인
```

##### API 요청 시 토큰이 전송되지 않음
```javascript
// 확인 사항:
// 1. client.js의 request 인터셉터 확인
// 2. getAccessToken()이 토큰을 반환하는지 확인
// 3. Authorization 헤더 형식 확인: "Bearer <token>"
```

##### 토큰 갱신이 작동하지 않음
```javascript
// 확인 사항:
// 1. Refresh Token이 저장되어 있는지 확인
// 2. 백엔드 토큰 갱신 엔드포인트 확인
// 3. client.js의 response 인터셉터 로직 확인
```

---

## 백엔드 개선 사항

프론트엔드 개발 관점에서 백엔드에 필요하거나 개선이 필요한 사항들입니다.

### 1. API 응답 형식 표준화

#### 현재 상태
- 대부분의 엔드포인트가 표준화된 응답 형식 사용
- JWT 토큰 엔드포인트만 다른 형식

#### 제안
JWT 토큰 엔드포인트 응답도 표준 형식으로 변경:

**현재:**
```json
{
  "access": "...",
  "refresh": "..."
}
```

**제안:**
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

**장점:**
- 로그인 시 사용자 정보를 함께 받아 추가 API 호출 불필요
- 응답 형식 일관성 확보

---

### 2. 에러 응답 상태 코드 개선

#### 현재 상태
- Crawler 실패, LLM 실패 모두 500 에러 반환
- 프론트엔드에서 에러 타입 구분이 어려움

#### 제안
에러 타입별로 다른 상태 코드 사용:

**Crawler 실패:**
```
Status: 502 Bad Gateway
```
```json
{
  "error": true,
  "error_type": "CRAWLER_ERROR",
  "message": "Failed to crawl URL",
  "details": "Connection timeout"
}
```

**LLM 실패:**
```
Status: 503 Service Unavailable
```
```json
{
  "error": true,
  "error_type": "LLM_ERROR",
  "message": "Failed to analyze content",
  "details": "LLM service unavailable"
}
```

**장점:**
- 에러 타입을 상태 코드만으로 구분 가능
- 에러별 적절한 사용자 메시지 표시 가능
- 에러 타입별 재시도 로직 구현 가능

---

### 3. 페이지네이션 개선

#### 현재 상태
분석 이력 조회 시 `limit` 파라미터만 지원:
```
GET /api/v1/history/?limit=20
```

#### 제안
표준 페이지네이션 추가:

**요청:**
```
GET /api/v1/history/?page=1&page_size=20
```

**응답:**
```json
{
  "success": true,
  "count": 150,
  "next": "http://localhost:8000/api/v1/history/?page=2&page_size=20",
  "previous": null,
  "results": [
    // ...
  ]
}
```

**장점:**
- 무한 스크롤 구현 가능
- 페이지 내비게이션 구현 가능
- 총 개수 확인 가능

**구현 방법:**
Django REST Framework의 `PageNumberPagination` 사용

---

### 4. 필터링 및 정렬 기능

#### 제안
분석 이력 조회 시 필터링 및 정렬 옵션 추가:

**요청:**
```
GET /api/v1/history/?risk_level=high&is_safe=false&ordering=-created_at
```

**Query Parameters:**
- `risk_level`: safe, low, medium, high
- `is_safe`: true, false
- `is_clickbait`: true, false
- `is_hate_speech`: true, false
- `is_misinformation`: true, false
- `ordering`: created_at, -created_at, confidence_score, -confidence_score
- `search`: URL 또는 제목 검색

**장점:**
- 위험한 URL만 필터링
- 최신순/오래된 순 정렬
- URL 검색 기능

**구현 방법:**
Django REST Framework의 `DjangoFilterBackend`, `OrderingFilter`, `SearchFilter` 사용

---

### 5. 대량 삭제 기능

#### 제안
분석 이력 삭제 API 추가:

**단일 삭제:**
```
DELETE /api/v1/results/{analysis_id}/
```

**대량 삭제:**
```
DELETE /api/v1/results/bulk/
```
```json
{
  "ids": [1, 2, 3, 4, 5]
}
```

**응답:**
```json
{
  "success": true,
  "message": "5 results deleted successfully",
  "deleted_count": 5
}
```

**장점:**
- 사용자가 이력 관리 가능
- 개인정보 보호

---

### 6. 분석 통계 개선

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

#### 제안
기간별 통계 및 추가 정보 제공:

**요청:**
```
GET /api/v1/statistics/?period=7d
```

**Query Parameters:**
- `period`: 7d, 30d, 90d, all (기본값: 30d)

**응답:**
```json
{
  "success": true,
  "data": {
    "period": "7d",
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
        "dangerous": 5
      }
      // ... 7일치 데이터
    ],
    "most_analyzed_domains": [
      {"domain": "example.com", "count": 25},
      {"domain": "news.com", "count": 15}
    ]
  }
}
```

**장점:**
- 기간별 통계 확인
- 대시보드 UI 구성 가능
- 위험도 분포 시각화
- 자주 분석하는 도메인 확인

---

### 7. Rate Limiting 정보 제공

#### 제안
API Rate Limiting 정보를 응답 헤더에 포함:

**Response Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

**장점:**
- 프론트엔드에서 남은 요청 횟수 표시 가능
- 제한 도달 전 사용자에게 경고 가능
- 제한 초기화 시간 표시 가능

---

### 8. 배치 URL 분석

#### 제안
여러 URL을 한 번에 분석하는 API:

**요청:**
```
POST /api/v1/analyze/batch/
```
```json
{
  "urls": [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
  ]
}
```

**응답:**
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
        "result": { ... }
      },
      {
        "url": "https://example2.com",
        "status": "success",
        "result": { ... }
      },
      {
        "url": "https://example3.com",
        "status": "failed",
        "error": "Failed to crawl URL"
      }
    ]
  }
}
```

**장점:**
- 여러 URL 동시 분석 가능
- CSV 파일 업로드 후 대량 분석 가능

---

### 9. 웹훅 지원

#### 제안
분석 완료 시 웹훅 콜백 지원 (장시간 소요 분석의 경우):

**요청:**
```
POST /api/v1/analyze/
```
```json
{
  "url": "https://example.com",
  "webhook_url": "https://myapp.com/webhook/analysis"
}
```

**즉시 응답:**
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

**분석 완료 후 웹훅 호출:**
```
POST https://myapp.com/webhook/analysis
```
```json
{
  "analysis_id": 123,
  "status": "completed",
  "result": { ... }
}
```

**장점:**
- 긴 분석 작업 시 사용자 대기 불필요
- 비동기 처리 가능

---

### 10. API 버전 관리

#### 제안
향후 API 변경 시를 대비한 버전 관리:

**현재:**
```
/api/v1/analyze/
```

**제안:**
- v1 유지하면서 v2 추가 가능한 구조
- 헤더를 통한 버전 지정 지원:
```
Accept: application/vnd.api+json; version=1
```

**장점:**
- 하위 호환성 유지
- 점진적 마이그레이션 가능

---

### 우선순위

#### 높음 (즉시 구현 권장)
1. **API 응답 형식 표준화** - 개발 초기 단계에서 통일 필요
2. **에러 응답 상태 코드 개선** - 에러 처리 개선에 필수적
3. **페이지네이션 개선** - 대량 데이터 처리에 필수

#### 중간 (차기 버전에서 구현)
4. **필터링 및 정렬 기능** - 사용성 개선
5. **분석 통계 개선** - 대시보드 기능 강화
6. **대량 삭제 기능** - 사용자 편의성

#### 낮음 (장기적 개선 사항)
7. **Rate Limiting 정보 제공** - 트래픽 관리
8. **배치 URL 분석** - 고급 기능
9. **웹훅 지원** - 비동기 처리
10. **API 버전 관리** - 장기적 유지보수

---

## 사용 예시

### 로그인 페이지 구현 예시

```javascript
import { useState } from 'react';
import { login } from '../api/auth';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const result = await login(username, password);
      console.log('로그인 성공:', result.user);
      navigate('/');
    } catch (err) {
      setError(err.userMessage || '로그인에 실패했습니다.');
      console.error('로그인 에러:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error}</div>}

      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="사용자명"
        disabled={loading}
      />

      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="비밀번호"
        disabled={loading}
      />

      <button type="submit" disabled={loading}>
        {loading ? '로그인 중...' : '로그인'}
      </button>
    </form>
  );
}

export default LoginPage;
```

### URL 분석 페이지 구현 예시

```javascript
import { useState } from 'react';
import { analyzeUrl, getRiskLevelText, getRiskLevelColor } from '../api/analysis';

function AnalysisPage() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await analyzeUrl(url);
      setResult(response.result);
    } catch (err) {
      setError(err.userMessage || 'URL 분석에 실패했습니다.');
      console.error('분석 에러:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleAnalyze}>
        {error && <div className="error">{error}</div>}

        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="분석할 URL을 입력하세요"
          disabled={loading}
        />

        <button type="submit" disabled={loading || !url}>
          {loading ? '분석 중...' : 'URL 분석'}
        </button>
      </form>

      {result && (
        <div className="result">
          <h2>{result.title}</h2>
          <p>위험도: <span className={getRiskLevelColor(result.risk_level)}>
            {getRiskLevelText(result.risk_level)}
          </span></p>
          <p>신뢰도: {(result.confidence_score * 100).toFixed(1)}%</p>

          <div className="flags">
            {result.is_clickbait && <span className="badge danger">낚시성</span>}
            {result.is_hate_speech && <span className="badge danger">혐오 표현</span>}
            {result.is_misinformation && <span className="badge danger">허위 정보</span>}
            {result.is_safe && <span className="badge success">안전</span>}
          </div>

          <div className="details">
            <h3>상세 분석</h3>
            <pre>{JSON.stringify(result.analysis_details, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default AnalysisPage;
```

---

## 환경 설정

### `.env` 파일

```bash
# API Base URL
VITE_API_BASE_URL=http://localhost:8000
```

### 개발 서버 실행

```bash
# 프론트엔드
npm run dev

# 백엔드 (별도 터미널)
cd ../backend
python manage.py runserver
```

---

## 추가 참고사항

### CORS 설정 확인
백엔드에서 CORS 설정이 올바른지 확인:

```python
# backend/config/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite 기본 포트
    "http://localhost:3000",  # 다른 포트 사용 시
]

CORS_ALLOW_CREDENTIALS = True
```

### 프로덕션 빌드
```bash
npm run build
```

빌드된 파일은 `dist/` 디렉토리에 생성됩니다.
