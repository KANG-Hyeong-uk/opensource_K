# ⚡ Quick Start Guide (Simplified)

> 5분 안에 Selenium + Gemini LLM 기반 URL 분석 서비스 구축하기

---

## 🎯 간소화된 스택

### 사용하는 것
✅ Django + DRF
✅ SQLite (개발/배포 공통)
✅ Selenium (동적 웹 크롤링)
✅ Google Gemini LLM
✅ LangChain

### 제거된 것
❌ PostgreSQL
❌ Redis
❌ Celery
❌ Vector DB (ChromaDB)
❌ AWS S3

---

## ✅ 사전 요구사항

설치되어 있어야 할 소프트웨어:
- [ ] Python 3.11+
- [ ] Git
- [ ] Chrome 브라우저 (Selenium용)

---

## 🚀 5분 설치 가이드

### STEP 1: 프로젝트 구조 생성
```bash
cd /path/to/opensource_K/backend

# 프로젝트 구조 자동 생성
chmod +x scripts/create_structure.sh
./scripts/create_structure.sh
```

### STEP 2: 환경변수 설정
```bash
cp .env.example .env.dev
nano .env.dev
```

**최소 필수 설정**:
```bash
SECRET_KEY=django-insecure-local-dev-key-123
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Gemini API 키 (필수!)
GEMINI_API_KEY=your-gemini-api-key-here
```

**Gemini API 키 발급**:
1. https://makersuite.google.com/app/apikey 접속
2. "Create API Key" 클릭
3. 생성된 키를 `.env.dev`에 복사

### STEP 3: 가상환경 및 의존성 설치
```bash
# 가상환경 생성
python3 -m venv venv

# 활성화
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치 (1-2분 소요)
pip install --upgrade pip
pip install -r requirements/dev.txt
```

### STEP 4: ChromeDriver 자동 설치
```bash
# webdriver-manager가 자동으로 설치하므로 별도 작업 불필요!
# 하지만 수동 설치를 원하면:

# Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# macOS
brew install chromedriver
```

### STEP 5: Django 초기화
```bash
export DJANGO_SETTINGS_MODULE=config.settings.dev

# 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 슈퍼유저 생성 (Admin 접속용)
python manage.py createsuperuser
# Username: admin
# Password: admin123 (개발용)
```

### STEP 6: 서버 실행
```bash
python manage.py runserver
```

**접속 확인**:
- http://localhost:8000/admin/ (관리자 페이지)
- http://localhost:8000/api/v1/ (API 루트)

---

## 🎉 완료!

개발 환경 구축 완료! 이제 코드 작성을 시작하세요.

---

## 🧪 동작 테스트

### 1. Admin 접속
```bash
open http://localhost:8000/admin/
# 위에서 만든 계정으로 로그인
```

### 2. API 테스트 (회원가입)
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "password_check": "testpass123",
    "name": "테스트 유저"
  }'
```

### 3. 로그인
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# 응답에서 access token 복사
```

### 4. URL 분석 테스트
```bash
export TOKEN="your-access-token"

curl -X POST http://localhost:8000/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "url": "https://example.com/article"
  }'
```

---

## 🛠 문제 해결

### 문제 1: `ModuleNotFoundError: No module named 'selenium'`
**해결**:
```bash
source venv/bin/activate
pip install -r requirements/dev.txt
```

### 문제 2: Selenium ChromeDriver 오류
**해결**:
```bash
# webdriver-manager가 자동 설치
pip install webdriver-manager

# 또는 수동 설치
# Ubuntu: sudo apt-get install chromium-chromedriver
# macOS: brew install chromedriver
```

### 문제 3: Gemini API 오류
**해결**:
```bash
# API 키 확인
cat .env.dev | grep GEMINI

# API 키가 올바른지 확인:
# https://makersuite.google.com/app/apikey
```

### 문제 4: Port 8000 already in use
**해결**:
```bash
# 다른 포트 사용
python manage.py runserver 8001

# 또는 기존 프로세스 종료
lsof -ti:8000 | xargs kill -9
```

---

## 📝 다음 단계

### 개발 순서
1. ✅ **환경 설정 완료**
2. 📝 **모델 정의**: `apps/*/models.py`
3. 🔧 **Selenium 크롤러**: `apps/crawler/services/selenium_crawler.py`
4. 🤖 **Gemini 통합**: `apps/llm_provider/services/gemini_provider.py`
5. 🎯 **분석 서비스**: `apps/detection/services/analysis_service.py`
6. 📡 **API 엔드포인트**: `apps/*/views.py`
7. 🧪 **테스트 작성**: `pytest`

---

## 💡 유용한 명령어

```bash
# Django 쉘
python manage.py shell

# 마이그레이션 확인
python manage.py showmigrations

# 테스트 실행
pytest -v

# 코드 포맷팅
black apps/
```

---

## 🎯 체크리스트

- [ ] 프로젝트 구조 생성 완료
- [ ] 가상환경 활성화
- [ ] 의존성 설치 완료
- [ ] Gemini API 키 설정
- [ ] ChromeDriver 설치 확인
- [ ] DB 마이그레이션 완료
- [ ] 슈퍼유저 생성
- [ ] 서버 정상 실행
- [ ] Admin 페이지 접속 가능

모두 체크되었다면 개발 시작! 🚀

---

**소요 시간**: 5-7분
**난이도**: ⭐☆☆☆☆ (매우 쉬움)
