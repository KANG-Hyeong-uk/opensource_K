# Docker 배포 가이드

가장 간단하게 Docker로 배포하는 방법입니다.

## 사전 요구사항

- Docker
- Docker Compose

## 사용 방법

### 1. 환경 변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열어서 Gemini API 키를 입력하세요:

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

### 2. VM IP 주소 설정 (필요시)

VM이나 서버에 배포하는 경우, `docker-compose.yml` 파일을 열어서 IP 주소를 수정하세요:

```yaml
environment:
  - ALLOWED_HOSTS=YOUR_VM_IP,localhost,127.0.0.1
  - CORS_ALLOWED_ORIGINS=http://YOUR_VM_IP:3000,http://localhost:3000
  - CSRF_TRUSTED_ORIGINS=http://YOUR_VM_IP:3000,http://localhost:3000

frontend:
  build:
    context: ./frontend
    args:
      - VITE_API_BASE_URL=http://YOUR_VM_IP:8000
```

**현재 설정된 IP**: 20.200.128.111

### 3. 실행

```bash
docker-compose up --build
```

### 4. 접속

- Frontend: http://20.200.128.111:3000 (또는 http://localhost:3000)
- Backend: http://20.200.128.111:8000 (또는 http://localhost:8000)

## 종료

```bash
docker-compose down
```

## 주의사항

- 컨테이너를 종료하면 데이터베이스 데이터가 삭제됩니다.
- 개발/테스트용으로 적합합니다.
- VM에서 외부 접속을 허용하려면 방화벽에서 3000, 8000 포트를 열어야 합니다.
