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

## 🏗️ 시스템 아키텍처

### 분석 파이프라인

clickradar는 **3단계 AI 분석 파이프라인**으로 URL의 안전성을 평가합니다.

```
1️⃣ URL 입력
   ↓
2️⃣ [Selenium 크롤러]
   - 동적 웹페이지 렌더링
   - 제목, 본문, 메타데이터 추출
   - JavaScript 실행 후 콘텐츠 수집
   ↓
3️⃣ [RAG 시스템] (Retrieval-Augmented Generation)
   - Vector DB에서 유사 사례 검색
   - 클릭베이트/비클릭베이트 예시 제공
   - 컨텍스트 기반 분석 정확도 향상
   ↓
4️⃣ [SKT A.X-4.0-Light LLM]
   - RAG 컨텍스트 + 크롤링 데이터 통합 분석
   - 3가지 유해성 동시 탐지:
     ✓ 클릭베이트 (과장/선정성)
     ✓ 혐오 표현 (차별/공격성)
     ✓ 허위정보 (근거 부족/오정보)
   ↓
5️⃣ 결과 반환
   - 위험도 점수 (0.0 ~ 1.0)
   - 위험 레벨 (LOW/MEDIUM/HIGH)
   - AI 판단 근거 설명
   - 데이터베이스 저장
```

### RAG (Retrieval-Augmented Generation)

- **목적**: LLM의 제로샷 분석 한계를 극복하기 위한 few-shot 학습
- **방식**: 유사한 클릭베이트/정상 콘텐츠 예시를 프롬프트에 주입
- **효과**: 판단 정확도 향상, 일관성 있는 기준 적용

### 분석 정확도 향상 전략

1. **동적 크롤링** - Selenium으로 SPA/동적 콘텐츠 완벽 수집
2. **RAG 컨텍스트** - 과거 분석 사례 기반 few-shot 학습
3. **종합 분석** - 제목, 본문, 구조적 특징 모두 고려
4. **설명 생성** - 판단 근거를 사용자에게 명확히 전달

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

## 🎯 신뢰성 및 성능

### 모델 성능

- **기반 모델**: SKT A.X-4.0-Light (경량화된 로컬 LLM)
- **RAG 적용**: 유사 사례 기반 few-shot 학습으로 정확도 향상
- **실시간 분석**: URL 입력 후 평균 5-15초 내 결과 반환

### 분석 신뢰성

**강점:**
- ✅ **종합적 판단** - 제목뿐 아니라 본문 전체를 분석
- ✅ **컨텍스트 학습** - RAG로 과거 사례 참고하여 일관성 유지
- ✅ **근거 제시** - AI 판단 이유를 명확한 설명으로 제공
- ✅ **동적 크롤링** - JavaScript 기반 SPA도 정확히 분석

**제한사항:**
- ⚠️ **언어 제약** - 한국어 콘텐츠에 최적화 (영어/다국어는 정확도 낮음)
- ⚠️ **주관적 판단** - 클릭베이트/혐오 기준은 모델의 학습 데이터에 의존
- ⚠️ **동영상/이미지** - 텍스트 기반 분석으로 멀티미디어 콘텐츠는 미지원
- ⚠️ **실시간 팩트체크 한계** - 외부 검증 없이 콘텐츠 내부 일관성만 평가

### 사용 권장사항

clickradar는 **보조 도구**로 사용하는 것을 권장합니다.
- 의심스러운 콘텐츠의 1차 필터링
- 사용자의 비판적 사고를 돕는 참고 자료
- 최종 판단은 사용자의 책임 하에 수행

---

## 🔗 외부 개발자를 위한 API 통합

clickradar는 **RESTful API**를 제공하여 외부 애플리케이션에서 콘텐츠 안전성 분석 기능을 사용할 수 있습니다.

### API 키 발급 절차

1. 웹 UI에서 회원가입 및 로그인
2. "API Keys" 페이지로 이동
3. "새 API 키 발급" 버튼 클릭
4. API 키 이름 입력 후 생성
5. 발급된 키 복사 (재발급 불가하므로 안전하게 보관)

### 통합 예시 (Python)

```python
import requests

API_KEY = "ak_your_api_key_here"
API_URL = "http://your-server.com/api/v1/analyze/"

def check_url_safety(url):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        API_URL,
        json={"url": url},
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()["data"]
        return {
            "is_safe": data["is_safe"],
            "risk_level": data["risk_level"],
            "explanation": data["explanation"]
        }
    else:
        return {"error": response.json()}

# 사용 예시
result = check_url_safety("https://example.com/article")
print(f"안전 여부: {result['is_safe']}")
print(f"위험도: {result['risk_level']}")
print(f"판단 근거: {result['explanation']}")
```

### 사용량 제한

- **기본 일일 한도**: API 키당 1,000회/일
- **Rate Limiting**: 분당 최대 60회 요청
- **타임아웃**: 30초 이내 응답 보장

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
│   │   ├── accounts/     # 사용자 인증 (JWT)
│   │   ├── detection/    # URL 분석 오케스트레이션
│   │   ├── crawler/      # Selenium 웹 크롤러
│   │   ├── llm_provider/ # SKT A.X LLM 통합
│   │   ├── rag/          # RAG 시스템 (벡터 검색)
│   │   ├── api_keys/     # API 키 발급/관리
│   │   └── analytics/    # 사용량 통계
│   └── config/           # Django 설정
│
└── frontend/             # React 프론트엔드
    ├── src/
    │   ├── pages/        # 페이지 컴포넌트
    │   │   ├── AiEval.jsx        # URL 분석 페이지
    │   │   ├── ApiDocs.jsx       # API 문서
    │   │   ├── ApiUsage.jsx      # API 사용량
    │   │   └── AnalysisHistory.jsx
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

