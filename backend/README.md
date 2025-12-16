# 🚀 URL Analysis Service - Django Backend (Simplified)

> Selenium + Gemini LLM 기반 클릭베이트·혐오·낚시성 콘텐츠 탐지 서비스

## 📋 목차
- [프로젝트 개요](#프로젝트-개요)
- [디렉토리 구조](#디렉토리-구조)
- [앱별 역할 설명](#앱별-역할-설명)
- [개발 환경 설정](#개발-환경-설정)
- [배포 가이드](#배포-가이드)
- [API 문서](#api-문서)

---

## 🎯 프로젝트 개요

### 주요 기능
1. **사용자 인증**: 회원가입/로그인 (Django 기본 인증 + JWT)
2. **URL 분석**: Selenium 크롤링 → LangChain + Gemini LLM 기반 콘텐츠 위험도 판별
3. **API 키 관리**: 외부 개발자를 위한 API 키 발급 및 관리
4. **사용량 모니터링**: API 사용량 추적
5. **RESTful API**: 외부 통합을 위한 공개 API

### 기술 스택 (간소화)
- **Framework**: Django 5.0+, Django REST Framework
- **Database**: SQLite (개발/배포 공통)
- **Crawling**: Selenium (동적 페이지 지원)
- **LLM**: Google Gemini API + LangChain
- **Deployment**: Gunicorn, Nginx, AWS EC2

### 제거된 기능 (간소화)
- ❌ PostgreSQL (→ SQLite 사용)
- ❌ Redis Cache
- ❌ Celery Task Queue (→ 동기 처리)
- ❌ ChromaDB/Vector DB (→ LLM 직접 분석)
- ❌ AWS S3 (→ 로컬 저장)

---

## 📁 디렉토리 구조

```
backend/
│
├── config/                          # Django 프로젝트 설정
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py                     # WSGI 설정 (Gunicorn용)
│   ├── urls.py                     # 루트 URL 라우팅
│   │
│   └── settings/                   # 환경별 설정
│       ├── __init__.py
│       ├── base.py                 # 공통 설정
│       ├── dev.py                  # 개발 환경
│       └── prod.py                 # 프로덕션 환경
│
├── apps/                           # Django 앱 모음
│   │
│   ├── accounts/                   # 사용자 인증 및 관리
│   │   ├── models.py              # User, Profile 모델
│   │   ├── serializers.py         # User 직렬화
│   │   ├── views.py               # 회원가입, 로그인
│   │   ├── urls.py
│   │   ├── services.py            # 비즈니스 로직
│   │   └── tests/
│   │
│   ├── detection/                  # URL 분석 핵심 기능
│   │   ├── models.py              # AnalysisResult
│   │   ├── serializers.py
│   │   ├── views.py               # URL 분석 요청 처리
│   │   ├── urls.py
│   │   ├── services/
│   │   │   ├── analysis_service.py      # 분석 오케스트레이션
│   │   │   └── content_classifier.py    # 콘텐츠 분류
│   │   └── tests/
│   │
│   ├── crawler/                    # Selenium 크롤링
│   │   ├── models.py              # CrawledContent
│   │   ├── services/
│   │   │   ├── selenium_crawler.py      # Selenium 크롤러
│   │   │   ├── content_extractor.py     # 본문 추출
│   │   │   └── metadata_parser.py       # 메타데이터 파싱
│   │   ├── utils/
│   │   │   ├── validators.py            # URL 검증
│   │   │   └── sanitizers.py            # 텍스트 정제
│   │   └── tests/
│   │
│   ├── llm_provider/               # Gemini LLM 통합
│   │   ├── models.py              # LLMRequest (로깅용)
│   │   ├── services/
│   │   │   ├── gemini_provider.py       # Gemini API
│   │   │   └── prompt_manager.py        # 프롬프트 관리
│   │   ├── prompts/
│   │   │   ├── clickbait_detection.txt
│   │   │   ├── hate_speech_detection.txt
│   │   │   └── misinformation_detection.txt
│   │   └── tests/
│   │
│   ├── api_keys/                   # API 키 관리
│   │   ├── models.py              # APIKey, APIKeyUsage
│   │   ├── serializers.py
│   │   ├── views.py               # 키 발급, 조회
│   │   ├── urls.py
│   │   ├── services.py            # 키 생성, 검증
│   │   ├── permissions.py         # API 키 권한
│   │   └── tests/
│   │
│   └── analytics/                  # 사용량 통계
│       ├── models.py              # UsageLog
│       ├── serializers.py
│       ├── views.py               # 대시보드
│       ├── urls.py
│       ├── services.py
│       └── tests/
│
├── core/                           # 공통 유틸리티
│   ├── exceptions.py              # 커스텀 예외
│   ├── responses.py               # 표준 응답 포맷
│   ├── pagination.py
│   ├── permissions.py
│   ├── middleware.py
│   └── utils/
│       ├── logger.py
│       └── decorators.py
│
├── tests/                          # 통합 테스트
│   ├── conftest.py
│   ├── factories.py
│   └── integration/
│       └── test_url_analysis_flow.py
│
├── static/                         # 정적 파일
├── media/                          # 업로드 파일
├── logs/                           # 로그 파일
│
├── .env.example
├── .gitignore
├── manage.py
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── pytest.ini
└── README.md
```

---

## 🎯 앱별 역할 설명

### 1. **accounts** - 사용자 인증
```python
# models.py
class User(AbstractUser):
    """커스텀 사용자 모델"""
    pass

# services.py
class UserService:
    @staticmethod
    def register_user(username, password, name):
        """회원가입"""

    @staticmethod
    def authenticate_user(username, password):
        """로그인"""
```

### 2. **detection** - URL 분석 오케스트레이션
```python
# services/analysis_service.py
class URLAnalysisService:
    def analyze_url(self, url: str, user: User) -> AnalysisResult:
        """
        전체 분석 파이프라인
        1. Selenium으로 URL 크롤링
        2. 콘텐츠 전처리
        3. Gemini LLM 분석
        4. 결과 저장
        """
        # Selenium 크롤링
        crawler = SeleniumCrawler()
        content = crawler.crawl(url)

        # Gemini 분석
        llm = GeminiProvider()
        analysis = llm.analyze_content(content)

        # 결과 저장
        return self._save_result(url, user, analysis)
```

### 3. **crawler** - Selenium 크롤링
```python
# services/selenium_crawler.py
class SeleniumCrawler:
    def __init__(self):
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def crawl(self, url: str) -> CrawledContent:
        """동적 페이지 크롤링"""
        self.driver.get(url)
        # JavaScript 렌더링 대기
        time.sleep(2)

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # 콘텐츠 추출
        extractor = ContentExtractor()
        main_content = extractor.extract(soup)

        return CrawledContent(
            url=url,
            content=main_content,
            html=html
        )
```

### 4. **llm_provider** - Gemini LLM
```python
# services/gemini_provider.py
class GeminiProvider:
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def analyze_content(self, content: str) -> dict:
        """Gemini로 콘텐츠 분석"""
        prompt_manager = PromptManager()

        # 클릭베이트 분석
        clickbait_prompt = prompt_manager.get_clickbait_prompt(content)
        clickbait_result = self._call_gemini(clickbait_prompt)

        # 혐오 표현 분석
        hate_prompt = prompt_manager.get_hate_speech_prompt(content)
        hate_result = self._call_gemini(hate_prompt)

        # 허위정보 분석
        misinfo_prompt = prompt_manager.get_misinformation_prompt(content)
        misinfo_result = self._call_gemini(misinfo_prompt)

        return {
            'is_clickbait': clickbait_result['is_positive'],
            'is_hate_speech': hate_result['is_positive'],
            'is_misinformation': misinfo_result['is_positive'],
            'confidence': self._calculate_confidence([
                clickbait_result, hate_result, misinfo_result
            ])
        }

    def _call_gemini(self, prompt: str) -> dict:
        """Gemini API 호출"""
        response = self.model.generate_content(prompt)
        return self._parse_response(response.text)
```

### 5. **api_keys** - API 키 관리
```python
# models.py
class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    daily_limit = models.IntegerField(default=1000)

class APIKeyUsage(models.Model):
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
```

---

## 🛠 개발 환경 설정

### 1. 가상환경 생성
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치
```bash
pip install -r requirements/dev.txt
```

### 3. 환경변수 설정 (.env.dev)
```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite - 자동 생성)
DB_NAME=db.sqlite3

# Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# Selenium
CHROME_DRIVER_PATH=/usr/local/bin/chromedriver  # 선택적
```

### 4. 데이터베이스 초기화
```bash
export DJANGO_SETTINGS_MODULE=config.settings.dev
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Selenium ChromeDriver 설치
```bash
# Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# macOS
brew install chromedriver

# 또는 수동 다운로드
# https://chromedriver.chromium.org/downloads
```

### 6. 개발 서버 실행
```bash
python manage.py runserver
```

---

## 🚀 배포 가이드 (AWS EC2)

### 환경변수 (.env.prod)
```bash
SECRET_KEY=<강력한-랜덤-키>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-ec2-ip

# Gemini API
GEMINI_API_KEY=<실제-키>

# Security
CSRF_TRUSTED_ORIGINS=https://your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend.com
```

### Gunicorn 설정 (gunicorn.conf.py)
```python
bind = '0.0.0.0:8000'
workers = 2
worker_class = 'sync'
timeout = 120  # Selenium 크롤링 대기 시간
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
```

### Nginx 설정
```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/urlanalysis/static/;
    }

    location /media/ {
        alias /var/www/urlanalysis/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 120s;  # Selenium 대기
    }
}
```

### EC2 배포 스크립트
```bash
#!/bin/bash
set -e

# 코드 업데이트
git pull origin main

# 의존성 설치
source venv/bin/activate
pip install -r requirements/prod.txt

# 정적 파일
export DJANGO_SETTINGS_MODULE=config.settings.prod
python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Gunicorn 재시작
sudo systemctl restart gunicorn
sudo systemctl reload nginx

echo "✅ 배포 완료!"
```

---

## 📡 API 문서

### 인증
```
POST /api/v1/auth/register/
Body: {
  "username": "user123",
  "password": "pass123",
  "password_check": "pass123",
  "name": "홍길동"
}

POST /api/v1/auth/login/
Body: {
  "username": "user123",
  "password": "pass123"
}
Response: {
  "access": "jwt-token...",
  "refresh": "refresh-token..."
}
```

### URL 분석
```
POST /api/v1/analyze/
Headers: Authorization: Bearer <jwt-token>
Body: {
  "url": "https://example.com/article"
}
Response: {
  "id": 1,
  "url": "https://example.com/article",
  "is_clickbait": true,
  "is_hate_speech": false,
  "is_misinformation": false,
  "confidence_score": 0.87,
  "created_at": "2025-12-08T10:00:00Z"
}

GET /api/v1/history/
Headers: Authorization: Bearer <jwt-token>
Response: [분석 이력 목록]
```

### API 키 관리
```
POST /api/v1/api-keys/
Headers: Authorization: Bearer <jwt-token>
Body: {
  "name": "My App Key"
}
Response: {
  "key": "ak_...",
  "name": "My App Key"
}

GET /api/v1/api-keys/
Headers: Authorization: Bearer <jwt-token>
```

### 외부 API (API 키 사용)
```
POST /api/v1/public/analyze/
Headers: X-API-Key: ak_...
Body: {
  "url": "https://example.com"
}
```

---

## 📦 주요 의존성

### requirements/base.txt
```
Django==5.0.1
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1

# Gemini LLM
google-generativeai==0.3.1
langchain==0.1.0
langchain-google-genai==0.0.5

# Selenium
selenium==4.16.0
webdriver-manager==4.0.1

# Web Scraping
beautifulsoup4==4.12.2
lxml==5.1.0

# Utilities
python-dotenv==1.0.0
```

### requirements/dev.txt
```
-r base.txt

# Testing
pytest==7.4.4
pytest-django==4.7.0
pytest-cov==4.1.0

# Code Quality
black==23.12.1
flake8==7.0.0
```

### requirements/prod.txt
```
-r base.txt

gunicorn==21.2.0
```

---

## 🧪 테스트

```bash
# 전체 테스트
pytest

# 특정 앱
pytest apps/detection/tests/

# 커버리지
pytest --cov=apps --cov-report=html
```

---

## 🔒 보안 고려사항

1. **API 키 관리**: 환경변수로 관리, 절대 하드코딩 금지
2. **Rate Limiting**: Django Throttling 사용
3. **HTTPS**: 프로덕션 필수
4. **CSRF 보호**: Django 기본 미들웨어 활성화
5. **SQL Injection**: Django ORM 사용으로 자동 방지

---

## 📈 성능 최적화

1. **Selenium 최적화**:
   - Headless 모드 사용
   - 이미지 로딩 비활성화
   - 타임아웃 적절히 설정

2. **DB 최적화**:
   - 인덱스 추가 (url, user, created_at)
   - Select related 사용

3. **LLM 비용 절감**:
   - 중복 URL 분석 방지 (캐싱)
   - 프롬프트 최적화

---

## 📞 문의

- **팀**: K오픈소스 프로젝트
- **저장소**: https://github.com/yourteam/opensource_K

---

## 📄 라이선스

MIT License
