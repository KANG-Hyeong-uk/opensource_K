# 🎯 START HERE - 간소화된 Django 백엔드

> **Selenium + Gemini LLM 기반 URL 분석 서비스**

---

## 📋 프로젝트 개요

Selenium 크롤링과 Google Gemini LLM을 활용한 **클릭베이트·혐오·낚시성 콘텐츠 탐지 서비스**입니다.

### 🎯 간소화된 기술 스택

**사용하는 기술**:
- ✅ Django 5.0 + DRF
- ✅ SQLite (개발/배포 공통)
- ✅ Selenium (동적 웹 크롤링)
- ✅ Google Gemini LLM
- ✅ LangChain

**제거된 기술** (복잡도 감소):
- ❌ PostgreSQL
- ❌ Redis
- ❌ Celery
- ❌ Vector DB (ChromaDB)
- ❌ AWS S3

---

## 🚀 초고속 시작 (5분)

```bash
# 1. 프로젝트 구조 생성
chmod +x scripts/create_structure.sh
./scripts/create_structure.sh

# 2. 환경 설정
cp .env.example .env.dev
# .env.dev에서 GEMINI_API_KEY 설정

# 3. 가상환경 및 의존성
python -m venv venv
source venv/bin/activate
pip install -r requirements/dev.txt

# 4. Django 초기화
python manage.py migrate
python manage.py createsuperuser

# 5. 서버 실행
python manage.py runserver
```

**상세 가이드**: [QUICK_START.md](./QUICK_START.md)

---

## 📚 문서 가이드

| 문서 | 목적 | 예상 시간 |
|------|------|-----------|
| **[README.md](./README.md)** | 프로젝트 전체 개요, API 문서 | 10분 |
| **[QUICK_START.md](./QUICK_START.md)** | 5분 안에 환경 구축 | 5분 |
| **[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)** | 디렉토리 구조 | 5분 |

---

## 🗂️ 간소화된 프로젝트 구조

```
backend/
├── 📄 문서
│   ├── README.md                  # 메인 문서
│   ├── QUICK_START.md             # 빠른 시작
│   └── PROJECT_STRUCTURE.md       # 구조 설명
│
├── 🐍 Django 앱 (5개)
│   ├── accounts/                  # 사용자 인증
│   ├── detection/                 # URL 분석 (핵심)
│   ├── crawler/                   # Selenium 크롤링
│   ├── llm_provider/              # Gemini LLM
│   ├── api_keys/                  # API 키 관리
│   └── analytics/                 # 사용량 통계
│
├── ⚙️ 설정
│   ├── config/settings/           # 환경별 설정
│   ├── requirements/              # 의존성
│   └── scripts/                   # 자동화 스크립트
│
└── 🗄️ 데이터
    ├── db.sqlite3                 # SQLite DB
    ├── static/                    # 정적 파일
    └── media/                     # 업로드 파일
```

---

## 🔑 핵심 API 엔드포인트

### 인증
```
POST /api/v1/auth/register/          # 회원가입
POST /api/v1/auth/login/             # 로그인 (JWT)
```

### URL 분석
```
POST /api/v1/analyze/                # URL 분석 요청
GET  /api/v1/history/                # 분석 이력
```

### API 키
```
POST /api/v1/api-keys/               # API 키 발급
GET  /api/v1/api-keys/               # 내 API 키 목록
```

---

## 🎯 핵심 플로우

```
사용자 요청 (URL)
    ↓
[Selenium Crawler] - 동적 웹페이지 크롤링
    ↓
[Content Extractor] - 본문 추출
    ↓
[Gemini LLM] - 클릭베이트/혐오/낚시 분석
    ↓
[Result] - 분석 결과 저장 (SQLite)
    ↓
응답 반환
```

---

## 📦 주요 의존성

```txt
Django==5.0.1
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1

# Gemini LLM
google-generativeai==0.3.1
langchain==0.1.0
langchain-google-genai==0.0.5

# Selenium
selenium==4.16.0
webdriver-manager==4.0.1
beautifulsoup4==4.12.2
```

**전체 목록**: [requirements/base.txt](./requirements/base.txt)

---

## 🛠️ 개발 워크플로우

### 1. 기능 개발
```bash
# 브랜치 생성
git checkout -b feature/new-feature

# 코드 작성
# (edit files)

# 테스트
pytest apps/your_app/

# 코드 포맷
black apps/

# 커밋
git commit -m "feat: add feature"
```

### 2. 주요 구현 파일

| 파일 | 역할 |
|------|------|
| `apps/crawler/services/selenium_crawler.py` | Selenium 크롤러 |
| `apps/llm_provider/services/gemini_provider.py` | Gemini LLM 통합 |
| `apps/detection/services/analysis_service.py` | 분석 오케스트레이션 |

---

## 🚀 배포 (AWS EC2)

### 간소화된 배포 프로세스

```bash
# EC2에서
git clone <repo>
cd backend

# 환경 설정
cp .env.example .env.prod
# GEMINI_API_KEY, SECRET_KEY 설정

# 의존성 설치
python -m venv venv
source venv/bin/activate
pip install -r requirements/prod.txt

# Django 설정
python manage.py migrate
python manage.py collectstatic

# Gunicorn으로 실행
gunicorn config.wsgi:application
```

**주의사항**:
- SQLite는 동시 쓰기 제한이 있으므로 트래픽이 많으면 PostgreSQL 고려
- Selenium은 메모리를 많이 사용하므로 최소 2GB RAM 권장

---

## ✅ 완성된 결과물

### 📚 생성된 문서
- ✅ README.md (간소화)
- ✅ QUICK_START.md (업데이트)
- ✅ PROJECT_STRUCTURE.md
- ✅ START_HERE.md (이 파일)

### ⚙️ 설정 파일
- ✅ .env.example (Gemini API 키 포함)
- ✅ requirements/base.txt (간소화)
- ✅ requirements/dev.txt
- ✅ requirements/prod.txt
- ✅ scripts/create_structure.sh (간소화)

---

## 🎯 다음 단계

### Phase 1: 기본 구조 (1일)
- [ ] `./scripts/create_structure.sh` 실행
- [ ] Django 설정 파일 작성
- [ ] 기본 모델 정의

### Phase 2: 핵심 기능 (3-4일)
- [ ] Selenium 크롤러 구현
- [ ] Gemini LLM 통합
- [ ] 분석 서비스 구현
- [ ] API 엔드포인트 작성

### Phase 3: 테스트 및 배포 (1-2일)
- [ ] 단위 테스트
- [ ] EC2 배포

---

## 💡 Gemini API 키 발급

1. **Google AI Studio 접속**:
   - https://makersuite.google.com/app/apikey

2. **API 키 생성**:
   - "Create API Key" 클릭
   - 프로젝트 선택 또는 생성
   - API 키 복사

3. **.env.dev에 추가**:
   ```bash
   GEMINI_API_KEY=AIzaSy...
   ```

---

## 🆘 문제 해결

### Selenium ChromeDriver 오류
```bash
# webdriver-manager가 자동으로 처리
pip install webdriver-manager

# 수동 설치 (선택)
# Ubuntu: sudo apt-get install chromium-chromedriver
# macOS: brew install chromedriver
```

### Gemini API 오류
```bash
# API 키 확인
cat .env.dev | grep GEMINI

# 할당량 확인
# https://makersuite.google.com/app/apikey
```

---

## 📞 연락처

- **팀**: K오픈소스 프로젝트
- **저장소**: https://github.com/yourteam/opensource_K

---

## ✨ 핵심 특징

✅ **간단한 스택** - SQLite + Selenium + Gemini만 사용
✅ **빠른 시작** - 5분 안에 환경 구축
✅ **자동화** - 구조 생성 스크립트 제공
✅ **명확한 구조** - 5개 Django 앱으로 분리
✅ **쉬운 배포** - EC2 원티어 배포 가능

**지금 바로 시작하세요!** 🚀

```bash
./scripts/create_structure.sh
```

---

**작성일**: 2025-12-08
**버전**: 2.0 (Simplified)
**라이선스**: MIT
