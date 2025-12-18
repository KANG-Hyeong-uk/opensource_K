# 백엔드 서버 실행 가이드

프론트엔드를 테스트하려면 백엔드 Django 서버가 실행되어야 합니다.

---

## 🚀 빠른 실행 (이미 설정 완료된 경우)

```bash
# 1. 백엔드 디렉토리로 이동
cd /mnt/c/Users/solok/Desktop/대학교/오픈소스\ 2/opensource_K/backend

# 2. 가상환경 활성화
source venv/bin/activate

# 3. 서버 실행
python manage.py runserver

# 또는 특정 포트 지정
python manage.py runserver 8000
```

**서버 실행 확인**:
- 브라우저에서 http://localhost:8000/admin/ 접속
- 터미널에 "Starting development server at http://127.0.0.1:8000/" 메시지 확인

---

## 📋 전체 설정 가이드 (처음 실행하는 경우)

### STEP 1: 환경변수 설정 확인

```bash
cd /mnt/c/Users/solok/Desktop/대학교/오픈소스\ 2/opensource_K/backend

# .env 파일이 있는지 확인
ls -la .env

# 없으면 생성
cp .env.example .env

# 편집
nano .env
```

**필수 설정** (.env 파일):
```bash
SECRET_KEY=django-insecure-local-dev-key-123
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ⚠️ Gemini API 키 필수!
GEMINI_API_KEY=your-gemini-api-key-here

# CORS 설정 (프론트엔드 연동용)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**Gemini API 키 발급**:
1. https://makersuite.google.com/app/apikey 접속
2. "Create API Key" 클릭
3. 생성된 키를 .env 파일에 복사

---

### STEP 2: 가상환경 확인 및 활성화

```bash
# 가상환경이 이미 있는지 확인
ls venv

# 있으면 활성화만
source venv/bin/activate

# 없으면 생성 후 활성화
python3 -m venv venv
source venv/bin/activate

# Windows의 경우
venv\Scripts\activate
```

**가상환경 활성화 확인**:
- 터미널 프롬프트 앞에 `(venv)` 표시됨
- `which python` 실행 시 venv 경로 표시

---

### STEP 3: 의존성 설치 확인

```bash
# 가상환경 활성화 상태에서
pip install -r requirements/dev.txt

# 또는 업그레이드
pip install --upgrade -r requirements/dev.txt
```

**주요 패키지**:
- Django, Django REST Framework
- django-cors-headers
- djangorestframework-simplejwt
- selenium, webdriver-manager
- google-generativeai (Gemini)
- langchain

---

### STEP 4: 데이터베이스 마이그레이션

```bash
# 마이그레이션 파일 생성
python manage.py makemigrations

# 마이그레이션 적용
python manage.py migrate
```

**결과 확인**:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying detection.0001_initial... OK
  ...
```

---

### STEP 5: 슈퍼유저 생성 (선택, Admin 사용 시)

```bash
python manage.py createsuperuser
```

**입력 예시**:
```
Username: admin
Email address: admin@example.com
Password: admin123
Password (again): admin123
```

---

### STEP 6: 서버 실행

```bash
python manage.py runserver

# 또는 특정 포트
python manage.py runserver 8000

# 모든 네트워크 인터페이스에서 접속 허용
python manage.py runserver 0.0.0.0:8000
```

**성공 메시지**:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 18, 2025 - 10:00:00
Django version 5.0.1, using settings 'config.settings.dev'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## 🧪 서버 동작 테스트

### 1. Admin 페이지 접속
```
http://localhost:8000/admin/
```
- 위에서 생성한 슈퍼유저로 로그인

### 2. API 루트 확인
```
http://localhost:8000/api/v1/
```

### 3. API 테스트 (curl)

#### 회원가입
```bash
curl -X POST http://localhost:8000/api/v1/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_check": "testpass123"
  }'
```

#### 로그인
```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

**응답 예시**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### URL 분석 (인증 필요)
```bash
# 위에서 받은 access 토큰 사용
export TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

curl -X POST http://localhost:8000/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "url": "https://www.example.com"
  }'
```

---

## 🔄 프론트엔드와 함께 실행

### 터미널 1: 백엔드
```bash
cd /mnt/c/Users/solok/Desktop/대학교/오픈소스\ 2/opensource_K/backend
source venv/bin/activate
python manage.py runserver
```

### 터미널 2: 프론트엔드
```bash
cd /mnt/c/Users/solok/Desktop/대학교/오픈소스\ 2/opensource_K/frontend
npm run dev
```

**접속**:
- 프론트엔드: http://localhost:5173
- 백엔드 Admin: http://localhost:8000/admin
- 백엔드 API: http://localhost:8000/api/v1/

---

## 🛠 문제 해결

### 문제 1: Port 8000 already in use

**에러**:
```
Error: That port is already in use.
```

**해결**:
```bash
# 다른 포트 사용
python manage.py runserver 8001

# 또는 기존 프로세스 종료 (Linux/Mac)
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID번호> /F
```

프론트엔드 `.env` 파일도 수정:
```
VITE_API_BASE_URL=http://localhost:8001
```

---

### 문제 2: ModuleNotFoundError

**에러**:
```
ModuleNotFoundError: No module named 'rest_framework'
```

**해결**:
```bash
# 가상환경 활성화 확인
source venv/bin/activate

# 의존성 재설치
pip install -r requirements/dev.txt
```

---

### 문제 3: Migration 오류

**에러**:
```
django.db.utils.OperationalError: no such table
```

**해결**:
```bash
# 기존 마이그레이션 삭제
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# DB 파일 삭제 (데이터 초기화)
rm db.sqlite3

# 마이그레이션 재생성
python manage.py makemigrations
python manage.py migrate

# 슈퍼유저 재생성
python manage.py createsuperuser
```

---

### 문제 4: CORS 오류 (프론트엔드 연동 시)

**에러** (브라우저 Console):
```
Access to XMLHttpRequest at 'http://localhost:8000/api/v1/...'
from origin 'http://localhost:5173' has been blocked by CORS policy
```

**해결**:

`.env` 파일 확인:
```bash
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

또는 `config/settings/dev.py` 확인:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True
```

---

### 문제 5: Gemini API 키 오류

**에러**:
```
google.api_core.exceptions.PermissionDenied: API key not valid
```

**해결**:
```bash
# .env 파일 확인
cat .env | grep GEMINI

# API 키 재발급
# https://makersuite.google.com/app/apikey

# .env 파일 수정
nano .env
```

**API 키 테스트**:
```bash
python check_gemini_models.py
```

---

### 문제 6: Selenium/ChromeDriver 오류

**에러**:
```
selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH
```

**해결**:
```bash
# webdriver-manager가 자동 관리하므로 보통 문제 없음
pip install webdriver-manager

# 수동 설치 (필요시)
# Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# macOS
brew install chromedriver

# Windows
# https://chromedriver.chromium.org/ 에서 다운로드
```

---

## 📊 서버 상태 확인

### 로그 확인
```bash
# 실시간 로그 (서버 실행 중 터미널)
python manage.py runserver

# 로그 파일 확인 (별도 터미널)
tail -f logs/django.log
```

### DB 확인
```bash
# Django 쉘
python manage.py shell

# Python 쉘에서
from apps.detection.models import AnalysisResult
AnalysisResult.objects.all()
```

---

## 🎯 체크리스트

실행 전 확인:
- [ ] `.env` 파일 존재 및 설정 완료
- [ ] Gemini API 키 설정
- [ ] 가상환경 활성화
- [ ] 의존성 설치 완료
- [ ] 마이그레이션 완료
- [ ] 슈퍼유저 생성 (선택)

실행 확인:
- [ ] 서버 정상 시작 (포트 8000)
- [ ] Admin 페이지 접속 가능
- [ ] API 엔드포인트 응답 확인
- [ ] CORS 설정 정상 (프론트엔드 연동 시)

---

## 💡 유용한 명령어

```bash
# 서버 재시작 (Ctrl+C 후)
python manage.py runserver

# 특정 포트로 실행
python manage.py runserver 8001

# Django 쉘
python manage.py shell

# 마이그레이션 확인
python manage.py showmigrations

# 테스트 실행
pytest -v

# 정적 파일 수집
python manage.py collectstatic

# DB 초기화
python manage.py flush
```

---

## 🔗 관련 문서

- `QUICK_START.md` - 백엔드 전체 설정 가이드
- `README.md` - 프로젝트 개요
- `TESTING_GUIDE.md` - 테스트 가이드
- `.env.example` - 환경변수 예시

---

**작성일**: 2024
**최종 수정**: 2024-12-18
