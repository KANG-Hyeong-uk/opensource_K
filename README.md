# 🛡️ clickradar - AI 기반 웹 콘텐츠 안전성 분석 시스템

> URL 하나로 웹페이지의 유해성, 클릭베이트, 허위정보를 AI가 자동으로 분석하는 서비스


---

## 📌 프로젝트 소개

**clickradar**은 AI 기반 웹 콘텐츠 안전성 분석 시스템으로, URL을 입력하면 클릭베이트, 혐오 표현, 허위정보를 자동으로 탐지합니다.

### 🎯 핵심 기능

- **클릭베이트 탐지** - 선정적이고 과장된 제목 식별
- **혐오 표현 감지** - 차별적이고 공격적인 언어 패턴 분석
- **허위정보 검증** - 근거 없는 주장과 오정보 탐지
- **실시간 분석** - Selenium + SKT A.X-4.0-Light LLM
- **API 제공** - JWT 인증 및 API 키 기반 외부 통합

---

## 🚀 기술 스택

**Frontend:** React 19.2.0 + Vite 7.2.4
**Backend:** Django 5.0.1 + DRF + SKT A.X-4.0-Light
**Crawling:** Selenium 4.16.0
**Database:** SQLite
**Auth:** JWT (djangorestframework-simplejwt)

---

## 📡 API 엔드포인트

**Base URL:** `http://localhost:8000/api/v1`

### 주요 API 목록

| 메서드 | 엔드포인트 | 설명 | 인증 |
|--------|-----------|------|------|
| POST | `/analyze/` | URL 분석 요청 | Bearer Token |
| GET | `/history/` | 분석 이력 조회 (페이지네이션) | Bearer Token |
| GET | `/results/{id}/` | 분석 상세 조회 | Bearer Token |
| GET | `/statistics/` | 사용자 통계 조회 | Bearer Token |
| GET | `/api-keys/{id}/usage/` | API 키 사용량 조회 | Bearer Token |

### API 사용 예시

#### 1. URL 분석 요청
```bash
curl -X POST http://localhost:8000/api/v1/analyze/ \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

**응답:**
```json
{
  "success": true,
  "data": {
    "id": 4,
    "url": "https://example.com/article",
    "title": "기사 제목",
    "is_clickbait": true,
    "is_hate_speech": false,
    "is_misinformation": false,
    "is_safe": false,
    "risk_level": "medium",
    "confidence_score": 0.85,
    "created_at": "2025-12-18T15:59:51+09:00"
  }
}
```

#### 2. 분석 이력 조회
```bash
curl -X GET "http://localhost:8000/api/v1/history/?page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 3. 통계 조회
```bash
curl -X GET http://localhost:8000/api/v1/statistics/ \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**응답:**
```json
{
  "success": true,
  "data": {
    "total_analyses": 150,
    "clickbait_count": 45,
    "hate_speech_count": 12,
    "misinformation_count": 8,
    "safe_count": 85
  }
}
```

**📖 상세 API 문서:** 웹 UI의 "API Docs" 페이지 또는 [Backend README](./backend/README.md#-api-문서) 참조

---

## 🖥️ UI 화면 구성

1. **로그인/회원가입** - JWT 기반 인증
2. **URL 분석** - URL 입력 시 실시간 AI 분석 결과 표시 (클릭베이트/혐오/허위정보 여부, 신뢰도, 위험도)
3. **분석 히스토리** - 과거 분석 기록 조회 (페이지네이션)
4. **API Docs** - 대화형 API 명세서 페이지 (5개 엔드포인트 문서화)
5. **API 키 & 사용량** - API 키 발급/관리 및 사용량 통계
6. **통계** - 전체 분석 통계 및 시각화

---

## 🚀 빠른 시작

### 사전 요구사항

- Python 3.12+
- Node.js 18+
- Chrome 브라우저

### 1️⃣ 백엔드 설정

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements/base.txt

# 환경변수 설정
cp .env.example .env

# 데이터베이스 마이그레이션
python manage.py migrate

# 개발 서버 실행
python manage.py runserver
```

백엔드가 `http://localhost:8000`에서 실행됩니다.

### 2️⃣ 프론트엔드 설정

```bash
cd frontend

# 패키지 설치
npm install

# 개발 서버 실행
npm run dev
```

프론트엔드가 `http://localhost:5173`에서 실행됩니다.

---

## 📖 사용 방법

1. 브라우저에서 `http://localhost:5173` 접속
2. 회원가입 후 로그인
3. URL 입력하여 분석 실행
4. API Docs 페이지에서 API 명세 확인
5. API 키 발급 후 외부 통합 가능

---

## 📂 프로젝트 구조

```
opensource_K/
├── backend/              # Django 백엔드
│   ├── apps/
│   │   ├── accounts/     # 사용자 인증
│   │   ├── detection/    # URL 분석 엔진
│   │   ├── crawler/      # Selenium 크롤러
│   │   ├── llm_provider/ # A.X LLM 통합
│   │   └── api_keys/     # API 키 관리
│   └── config/           # Django 설정
│
└── frontend/             # React 프론트엔드
    ├── src/
    │   ├── pages/        # 페이지 (ApiDocs, AiEval, ApiUsage 등)
    │   ├── components/   # 재사용 컴포넌트
    │   └── api/          # API 클라이언트
    └── public/
```

---

## 🚢 배포

### Docker
```bash
docker-compose up -d
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

상세 가이드: [Backend README](./backend/README.md) | [Frontend README](./frontend/README.md)

---

