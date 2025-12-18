# ⚛️ Frontend - React Web Application

> AI 콘텐츠 안전성 분석 서비스의 사용자 인터페이스

---

## 📋 목차

- [개요](#개요)
- [기술 스택](#기술-스택)
- [설치 및 실행](#설치-및-실행)
- [페이지 구조](#페이지-구조)
- [주요 기능](#주요-기능)
- [디자인 시스템](#디자인-시스템)
- [배포](#배포)

---

## 🎯 개요

clickradar의 프론트엔드는 React 기반의 현대적인 웹 애플리케이션으로, 직관적이고 반응형인 UI를 제공합니다.

### 핵심 가치

- 🎨 **직관적인 UX** - 복잡한 분석 결과를 쉽게 이해할 수 있는 시각화
- ⚡ **빠른 성능** - Vite 기반 초고속 빌드 및 HMR
- 📱 **반응형 디자인** - 모바일, 태블릿, 데스크톱 모두 지원
- ♿ **접근성** - WCAG 2.1 가이드라인 준수

---

## 💻 기술 스택

### Core
- **React 19.2.0** - 최신 UI 라이브러리
- **Vite 7.2.4** - 차세대 프론트엔드 빌드 도구
- **React Router DOM 7.10.1** - SPA 라우팅

### Styling
- **CSS3** - 커스텀 디자인 시스템
- **CSS Modules** - 스타일 격리
- **Flexbox & Grid** - 레이아웃

### Build & Dev Tools
- **ESLint** - 코드 품질 관리
- **Vite** - 개발 서버 및 빌드

---

## 🚀 설치 및 실행

### 1. 사전 요구사항

- Node.js 18.0 이상
- npm 또는 yarn

### 2. 패키지 설치

```bash
npm install
```

### 3. 환경변수 설정

`.env` 파일 생성:
```bash
VITE_API_BASE_URL=http://localhost:8000
```

### 4. 개발 서버 실행

```bash
npm run dev
```

개발 서버가 `http://localhost:5173`에서 실행됩니다.

### 5. 프로덕션 빌드

```bash
npm run build
```

빌드된 파일은 `dist/` 디렉토리에 생성됩니다.

### 6. 프로덕션 미리보기

```bash
npm run preview
```

---

## 📄 페이지 구조

### 1. 홈 (`/`)

**주요 컴포넌트:**
- Hero 섹션 - URL 분석 폼
- 분석 결과 카드 - 6개 항목 실시간 표시
- 기능 소개 - 서비스 핵심 기능

**분석 항목:**
- 보안 점수
- 응답 속도
- SEO 최적화
- SSL 인증
- 모바일 호환성
- 접근성

### 2. AI 평가 문서 (`/analysis`)

**기능:**
- 6개 AI 검증 문서 카드
- 카드 플립 애니메이션
- 문서 다운로드

**문서 목록:**
1. 영향 식별·기획 문서
2. 위험 평가·관리 문서
3. 데이터 거버넌스·편향 문서
4. 모델 성능 평가·안전장치 문서
5. 인간 감독·통제 문서
6. 운영·모니터링·검토 문서

### 3. API 명세서 (`/docs`)

**내용:**
- API 사용법
- 디자인 가이드
- 개발자 문서

### 4. API 사용량 (`/api-usage`)

**기능:**
- API 키 발급 및 관리
- 키 마스킹 (앞 8자/뒤 4자)
- 클립보드 복사
- 재발급
- 사용량 통계 (이번 달 호출, 사용률, 남은 호출)

### 5. 로그인 (`/login`)

**기능:**
- JWT 기반 로그인
- 토큰 자동 저장
- 보안 경고

### 6. 회원가입 (`/signup`)

**기능:**
- 사용자 등록
- 비밀번호 확인
- 유효성 검증

---

## 🎨 디자인 시스템

### 색상 팔레트

```css
/* Primary Colors */
--color-primary: #FF2E2E;
--color-primary-hover: #E62929;

/* Text Colors */
--color-text-main: #111111;
--color-text-sub: #6B7280;
--color-text-muted: #9CA3AF;

/* Background Colors */
--color-bg-main: #FFFFFF;
--color-bg-light: #F9FAFB;
--color-bg-hover: #F3F4F6;

/* Border Colors */
--color-border: #E5E7EB;
--color-border-light: #F3F4F6;

/* Status Colors */
--color-success: #10B981;
--color-warning: #F59E0B;
--color-error: #EF4444;
--color-info: #3B82F6;
```

### 타이포그래피

```css
/* Headings */
h1 { font-size: 48px; font-weight: 800; letter-spacing: -1px; }
h2 { font-size: 36px; font-weight: 700; letter-spacing: -0.5px; }
h3 { font-size: 24px; font-weight: 600; }

/* Body */
body { font-size: 16px; line-height: 1.6; font-weight: 400; }
small { font-size: 14px; }
```

### 그림자

```css
/* Shadows */
--shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.05);
--shadow-lg: 0 12px 24px rgba(0, 0, 0, 0.08);
--shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.12);
```

### 브레이크포인트

```css
/* Responsive Breakpoints */
--breakpoint-mobile: 768px;
--breakpoint-tablet: 1024px;
--breakpoint-desktop: 1440px;
```

---

## 🧩 주요 컴포넌트

### Header

**기능:**
- 반응형 네비게이션
- 모바일 햄버거 메뉴
- 활성 페이지 하이라이트

**메뉴:**
- Home
- AI평가 및 검증 문서
- API 명세서
- API 사용량
- 로그인

### Layout

**역할:**
- 공통 레이아웃 래퍼
- Header + Content 구조
- 페이지 일관성 유지

### DocCard

**기능:**
- 3D 플립 애니메이션
- 문서 정보 표시
- 다운로드 버튼
- 호버 효과

---

## 🎭 주요 기능

### 1. URL 분석

**플로우:**
```
URL 입력
  ↓
검증 (형식 체크)
  ↓
백엔드 API 호출
  ↓
로딩 인디케이터
  ↓
결과 시각화
```

**UI 요소:**
- 입력 폼
- 로딩 스피너
- 결과 카드 (6개 항목)
- 에러 메시지

### 2. 인증 관리

**로그인 플로우:**
```
사용자명/비밀번호 입력
  ↓
백엔드 인증
  ↓
JWT 토큰 수신
  ↓
LocalStorage 저장
  ↓
홈으로 리다이렉트
```

**보안:**
- JWT 토큰 자동 갱신
- 보안 헤더 설정
- HTTPS 권장

### 3. API 키 관리

**키 생성:**
```javascript
// API 키 형식: tk_ + 32자 랜덤 문자
const generateApiKey = () => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let key = 'tk_';
  for (let i = 0; i < 32; i++) {
    key += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return key;
};
```

**마스킹:**
```javascript
// 앞 8자 + *** + 뒤 4자
const maskApiKey = (key) => {
  return key.slice(0, 8) + '***' + key.slice(-4);
};
```

### 4. 사용량 통계

**표시 항목:**
- 이번 달 호출 수 / 1,000
- 사용률 (%)
- 남은 호출 수

---

## 📱 반응형 디자인

### 모바일 (< 768px)

- 1열 그리드 레이아웃
- 햄버거 메뉴
- 터치 최적화
- 폰트 크기 조정

### 태블릿 (768px ~ 1024px)

- 2열 그리드 레이아웃
- 축소된 네비게이션
- 적응형 이미지

### 데스크톱 (> 1024px)

- 3열 그리드 레이아웃
- 전체 네비게이션
- 호버 효과

---

## 📂 폴더 구조

```
frontend/
├── src/
│   ├── components/          # 재사용 컴포넌트
│   │   ├── Header.jsx
│   │   ├── Header.css
│   │   ├── Layout.jsx
│   │   └── Layout.css
│   │
│   ├── pages/               # 페이지 컴포넌트
│   │   ├── Home.jsx
│   │   ├── Home.css
│   │   ├── Analysis.jsx
│   │   ├── Analysis.css
│   │   ├── ApiDocs.jsx
│   │   ├── ApiUsage.jsx
│   │   ├── ApiUsage.css
│   │   ├── Login.jsx
│   │   └── Signup.jsx
│   │
│   ├── api/                 # API 클라이언트
│   │   ├── client.js
│   │   ├── auth.js
│   │   ├── analysis.js
│   │   └── apiKeys.js
│   │
│   ├── utils/               # 유틸리티
│   │   ├── storage.js
│   │   ├── logger.js
│   │   └── errorHandler.js
│   │
│   ├── App.jsx              # 라우터 설정
│   ├── main.jsx             # 진입점
│   └── index.css            # 글로벌 스타일
│
├── public/                  # 정적 파일
│   └── assets/
│
├── .env                     # 환경변수
├── .env.example
├── package.json
├── vite.config.js
└── README.md
```

---

## 🚢 배포

### 빌드

```bash
npm run build
```

### 환경변수 설정

**프로덕션 `.env`:**
```bash
VITE_API_BASE_URL=https://api.thinkforbl.com
```

### Nginx 설정

```nginx
server {
    listen 80;
    server_name thinkforbl.com;

    root /var/www/thinkforbl/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # 정적 파일 캐싱
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Docker 배포

```dockerfile
FROM node:18-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 🧪 테스트

```bash
# 단위 테스트
npm test

# E2E 테스트
npm run test:e2e

# 커버리지
npm run test:coverage
```

---

## 🔧 개발 도구

### ESLint

```bash
npm run lint
```

### 포맷팅

```bash
npm run format
```

---

## 🌐 브라우저 지원

- ✅ Chrome (최신 2개 버전)
- ✅ Firefox (최신 2개 버전)
- ✅ Safari (최신 2개 버전)
- ✅ Edge (최신 2개 버전)

---

## 📈 성능 최적화

### 코드 스플리팅

```javascript
// 라우트 기반 코드 스플리팅
const Home = lazy(() => import('./pages/Home'));
const Analysis = lazy(() => import('./pages/Analysis'));
```

### 이미지 최적화

- WebP 포맷 사용
- Lazy loading
- 반응형 이미지 (`srcset`)

### 번들 최적화

- Tree shaking
- Minification
- Gzip 압축

---

## 🎯 향후 계획

- [ ] Progressive Web App (PWA) 지원
- [ ] 다크 모드
- [ ] 다국어 지원 (i18n)
- [ ] 실시간 알림 (WebSocket)
- [ ] 오프라인 모드

---

## 📞 문의

프론트엔드 관련 문의사항이나 버그 리포트는 [Issues](https://github.com/KANG-Hyeong-uk/opensource_K/issues)에 등록해주세요.

---

**Built with ⚛️ React & ⚡ Vite**
