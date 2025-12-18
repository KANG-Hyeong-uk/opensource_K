# 🔧 Backend - Django REST API Server

> SKT A.X-4.0-Light 기반 AI 콘텐츠 분석 백엔드 시스템

---

## 📋 목차

- [개요](#개요)
- [기술 스택](#기술-스택)
- [시스템 아키텍처](#시스템-아키텍처)
- [설치 및 실행](#설치-및-실행)
- [API 문서](#api-문서)
- [환경 설정](#환경-설정)
- [배포](#배포)

---

## 🎯 개요

ThinkforBL의 백엔드는 Django REST Framework 기반으로 구축된 API 서버로, URL 크롤링부터 AI 분석까지 모든 핵심 로직을 처리합니다.

### 주요 기능

- **사용자 인증** - JWT 기반 회원가입/로그인
- **URL 분석 엔진** - Selenium + A.X LLM 통합 파이프라인
- **RAG 시스템** - 유사 사례 기반 컨텍스트 제공
- **API 키 관리** - 외부 개발자용 API 키 발급 및 사용량 추적
- **분석 히스토리** - 사용자별 분석 기록 저장

---

## 💻 기술 스택

### Core Framework
- **Django 5.0.1** - Python 웹 프레임워크
- **Django REST Framework 3.14.0** - RESTful API
- **djangorestframework-simplejwt 5.3.1** - JWT 인증
- **django-cors-headers 4.3.1** - CORS 처리

### AI & Machine Learning
- **SKT A.X-4.0-Light** - 로컬 LLM 모델
- **transformers 4.36.0** - Hugging Face Transformers
- **torch 2.2.2** - PyTorch 딥러닝 프레임워크
- **sentence-transformers 3.3.1** - 문장 임베딩

### Web Crawling
- **selenium 4.16.0** - 동적 웹 크롤링
- **beautifulsoup4 4.12.2** - HTML 파싱
- **lxml 5.1.0** - XML/HTML 처리

### Database
- **SQLite** - 경량 관계형 DB (개발/운영 공통)

---

## 🏗️ 시스템 아키텍처

### 앱 구조

```
apps/
├── accounts/        # 사용자 인증 및 관리
├── detection/       # URL 분석 오케스트레이션
├── crawler/         # Selenium 기반 웹 크롤링
├── llm_provider/    # A.X LLM 통합
├── rag/             # RAG(Retrieval-Augmented Generation) 시스템
├── api_keys/        # API 키 발급 및 관리
└── analytics/       # 사용량 통계
```

### 분석 파이프라인

```
URL 입력
  ↓
[Selenium Crawler]
  ↓
콘텐츠 추출 (제목, 본문, 메타데이터)
  ↓
[RAG Service] - 유사 사례 검색
  ↓
[A.X LLM Provider]
  ├─ 클릭베이트 분석
  ├─ 혐오 표현 분석
  └─ 허위정보 분석
  ↓
종합 위험도 점수 계산
  ↓
데이터베이스 저장
  ↓
JSON 응답 반환
```

---

## 🚀 설치 및 실행

### 1. 사전 요구사항

- Python 3.12 이상
- Chrome 브라우저
- (선택) CUDA 지원 GPU (A.X 모델 가속화)

### 2. 가상환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows
```

### 3. 패키지 설치

```bash
# 기본 패키지 (운영 환경)
pip install -r requirements/base.txt

# 개발 환경 (테스트, 린터 포함)
pip install -r requirements/dev.txt
```

### 4. 환경변수 설정

```bash
# .env.example을 복사하여 .env 생성
cp .env.example .env
```

`.env` 파일 예시:
```bash
# Django 설정
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 데이터베이스
DB_NAME=db.sqlite3

# A.X 모델 설정 (선택사항, 기본값 사용)
# AX_MODEL=skt/A.X-4.0-Light
# AX_MAX_NEW_TOKENS=2048

# Selenium
SELENIUM_HEADLESS=True

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 5. 데이터베이스 마이그레이션

```bash
python manage.py migrate
```

### 6. 슈퍼유저 생성 (관리자 계정)

```bash
python manage.py createsuperuser
```

### 7. 개발 서버 실행

```bash
python manage.py runserver
```

서버가 `http://localhost:8000`에서 실행됩니다.

### 8. 관리자 페이지 접속

`http://localhost:8000/admin/`에서 Django 관리자 페이지에 접속할 수 있습니다.

---

## 📡 API 문서

### 인증 API

#### 회원가입
```http
POST /api/v1/accounts/signup/
Content-Type: application/json

{
  "username": "testuser",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "name": "홍길동"
}
```

**응답:**
```json
{
  "message": "회원가입이 완료되었습니다.",
  "user": {
    "id": 1,
    "username": "testuser",
    "name": "홍길동"
  }
}
```

#### 로그인
```http
POST /api/v1/accounts/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "securepass123"
}
```

**응답:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "testuser"
  }
}
```

---

### 분석 API

#### URL 분석
```http
POST /api/v1/detection/analyze/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "url": "https://example.com/article"
}
```

**응답:**
```json
{
  "id": 42,
  "url": "https://example.com/article",
  "title": "기사 제목",
  "is_clickbait": true,
  "is_hate_speech": false,
  "is_misinformation": false,
  "confidence_score": 0.85,
  "explanation": "클릭베이트: 제목이 과장되고 선정적입니다.",
  "risk_level": "HIGH",
  "created_at": "2025-12-19T12:00:00Z"
}
```

#### 분석 히스토리 조회
```http
GET /api/v1/detection/history/
Authorization: Bearer {access_token}
```

**응답:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 42,
      "url": "https://example.com/article",
      "is_clickbait": true,
      "confidence_score": 0.85,
      "created_at": "2025-12-19T12:00:00Z"
    }
  ]
}
```

#### 특정 분석 결과 조회
```http
GET /api/v1/detection/results/{id}/
Authorization: Bearer {access_token}
```

---

### API 키 관리

#### API 키 발급
```http
POST /api/v1/api-keys/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "My App API Key"
}
```

**응답:**
```json
{
  "id": 1,
  "key": "ak_1234567890abcdef1234567890abcdef",
  "name": "My App API Key",
  "is_active": true,
  "daily_limit": 1000,
  "created_at": "2025-12-19T12:00:00Z"
}
```

#### API 키 목록 조회
```http
GET /api/v1/api-keys/
Authorization: Bearer {access_token}
```

#### API 키로 분석 (외부 통합용)
```http
POST /api/v1/public/analyze/
X-API-Key: ak_1234567890abcdef1234567890abcdef
Content-Type: application/json

{
  "url": "https://example.com/article"
}
```

---

### 통계 API

#### 사용량 통계
```http
GET /api/v1/analytics/stats/
Authorization: Bearer {access_token}
```

**응답:**
```json
{
  "total_analyses": 150,
  "clickbait_detected": 45,
  "hate_speech_detected": 12,
  "misinformation_detected": 8,
  "safe_content": 85
}
```

---

## ⚙️ 환경 설정

### 환경변수 상세

| 변수명 | 설명 | 기본값 | 필수 |
|--------|------|--------|------|
| `SECRET_KEY` | Django 시크릿 키 | - | ✅ |
| `DEBUG` | 디버그 모드 | `False` | ❌ |
| `ALLOWED_HOSTS` | 허용 호스트 | `localhost` | ✅ |
| `DB_NAME` | SQLite DB 파일명 | `db.sqlite3` | ❌ |
| `AX_MODEL` | A.X 모델명 | `skt/A.X-4.0-Light` | ❌ |
| `AX_MAX_NEW_TOKENS` | 최대 생성 토큰 수 | `2048` | ❌ |
| `SELENIUM_HEADLESS` | Selenium Headless 모드 | `True` | ❌ |
| `CORS_ALLOWED_ORIGINS` | CORS 허용 도메인 | - | ✅ |

---

## 🧪 테스트

### 전체 테스트 실행
```bash
pytest
```

### 특정 앱 테스트
```bash
# URL 분석 테스트
pytest apps/detection/tests/

# LLM Provider 테스트
pytest apps/llm_provider/tests/
```

### 커버리지 리포트
```bash
pytest --cov=apps --cov-report=html
```

커버리지 리포트는 `htmlcov/index.html`에서 확인할 수 있습니다.

---

## 🚢 배포

### Gunicorn 설정

```bash
# Gunicorn 설치
pip install gunicorn

# 운영 서버 실행
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Docker 배포

```bash
# Docker 이미지 빌드
docker build -t thinkforbl-backend .

# 컨테이너 실행
docker run -p 8000:8000 thinkforbl-backend
```

### 환경별 설정

- **개발**: `config/settings/dev.py`
- **운영**: `config/settings/prod.py`

운영 환경에서는 다음 설정을 확인하세요:
- `DEBUG=False`
- 강력한 `SECRET_KEY` 사용
- HTTPS 설정
- CORS 도메인 제한
- 로깅 설정

---

## 🔒 보안 고려사항

1. **API 키 보호** - 환경변수로 관리, 절대 하드코딩 금지
2. **JWT 토큰** - 안전하게 저장, HTTPS 사용 권장
3. **Rate Limiting** - DRF Throttling으로 API 남용 방지
4. **CSRF 보호** - Django 기본 미들웨어 활성화
5. **SQL Injection** - Django ORM 사용으로 자동 방지

---

## 📈 성능 최적화

### A.X 모델 최적화
- GPU 사용 시 자동으로 CUDA 활성화
- CPU 환경에서도 동작하나 속도는 느림
- 첫 실행 시 모델 다운로드 필요 (약 수 GB)

### Selenium 최적화
- Headless 모드 사용으로 리소스 절감
- 타임아웃 적절히 설정 (기본 30초)
- 이미지 로딩 비활성화 옵션 고려

### 데이터베이스 최적화
- 적절한 인덱스 사용 (url, created_at)
- QuerySet 최적화 (select_related, prefetch_related)

---

## 🛠️ 개발 도구

### 코드 포맷팅
```bash
# Black - 코드 포맷터
black apps/

# isort - import 정렬
isort apps/
```

### 린터
```bash
# Flake8
flake8 apps/

# Pylint
pylint apps/
```

---

## 📞 문의

백엔드 관련 문의사항이나 버그 리포트는 [Issues](https://github.com/KANG-Hyeong-uk/opensource_K/issues)에 등록해주세요.

---

**Powered by Django & SKT A.X-4.0-Light**
