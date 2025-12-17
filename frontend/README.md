# TRAIN Korea - ThinkforBL

AI 기반 웹페이지 콘텐츠 안전성 분석 서비스

## 프로젝트 소개

URL 하나로 웹페이지의 콘텐츠 안전성을 AI가 자동으로 분석하는 서비스입니다. 복잡한 절차 없이 URL만 입력하면 해당 페이지의 텍스트와 콘텐츠를 자동으로 스캔하여 유해성, 오탐 가능성, 부적절한 표현을 즉시 진단합니다.

## 기술 스택

- **Frontend**: React 19.2.0
- **Build Tool**: Vite 7.2.4
- **Router**: React Router DOM 7.10.1
- **Styling**: CSS3 (Custom Design System)

## 시작하기

### 설치

```bash
npm install
```

### 개발 서버 실행

```bash
npm run dev
```

개발 서버가 `http://localhost:5173`에서 실행됩니다.

### 빌드

```bash
npm run build
```

### 프리뷰

```bash
npm run preview
```

## 페이지 구조

### 1. Home (/)

**주요 기능:**
- URL 분석 폼 (Hero 섹션)
- 실시간 분석 결과 표시
- 서비스 주요 기능 소개

**분석 결과 항목:**
- 보안 점수
- 응답 속도
- SEO 최적화
- SSL 인증
- 모바일 호환성
- 접근성

**Features:**
- 텍스트 & 파일 정밀 분석
- 직관적인 결과 시각화
- 안전 모드 & 피드백

---

### 2. AI평가 및 검증 문서 (/analysis)

**주요 기능:**
- AI 평가 및 검증 문서 6개 제공
- 카드 플립 인터랙션
- 문서 다운로드 기능

**문서 목록:**
1. **영향 식별·기획 문서**
   - 사용자 가치 & 위험 사전 분석

2. **위험 평가·관리 문서**
   - 위험도 기반 안전 관리

3. **데이터 거버넌스·편향 문서**
   - 결과 품질 & 데이터 무결성 보장

4. **모델 성능 평가·안전장치 문서**
   - 성능 검증 & 신뢰도 산출 근거

5. **인간 감독·통제 문서**
   - Human-in-the-loop 검토 시스템

6. **운영·모니터링·검토 문서**
   - 지속적 개선 & 안정성 유지

**UI 특징:**
- 카드 클릭 → 앞뒤 플립 애니메이션
- 뒷면 호버 → 다운로드 버튼 표시
- 레이어드 문서 그래픽 디자인

---

### 3. API 명세서 (/docs)

**주요 기능:**
- API 사용법 및 디자인 가이드
- 개발자 문서 제공

---

### 4. API 사용량 (/api-usage)

**주요 기능:**

#### API 키 관리
- **키 발급**: 랜덤 API 키 생성 (`tk_` + 32자)
- **키 마스킹**: 앞 8자/뒤 4자만 표시
- **보기/숨기기**: 토글 버튼으로 전체 키 확인
- **복사하기**: 클립보드 복사 기능
- **재발급**: 확인 후 새 키 생성
- **보안 경고**: API 키 보안 주의사항 안내

#### 사용량 통계
- **이번 달 호출**: 현재 사용량 / 1,000 호출
- **사용률**: 퍼센트로 표시
- **남은 호출**: 잔여 가능 호출 수

#### 저장소
- LocalStorage 사용
  - `api_key`: 발급된 API 키
  - `api_usage`: 현재 사용량

---

### 5. 로그인 (/login)

사용자 인증 페이지

---

### 6. 회원가입 (/signup)

신규 사용자 등록 페이지

---

## 주요 컴포넌트

### Header
- 반응형 네비게이션
- 모바일 햄버거 메뉴
- 활성 페이지 하이라이트

**메뉴 구조:**
- Home
- AI평가 및 검증 문서
- API 명세서
- API 사용량
- 로그인

### Layout
- 공통 레이아웃 래퍼
- Header + Content 구조

### DocCard
- 플립 애니메이션 카드 컴포넌트
- 문서 정보 표시
- 다운로드 기능

---

## 디자인 시스템

### 컬러
- **Primary**: `#FF2E2E` (Red)
- **Text Main**: `#111111`
- **Text Sub**: `#6B7280`
- **Background**: `#FFFFFF`, `#F9FAFB`
- **Border**: `#E5E7EB`

### 타이포그래피
- **메인 폰트**: System fonts stack
- **제목**: 800 weight, letter-spacing -1px
- **본문**: 400 weight, line-height 1.6

### 그림자
- **Small**: `0 2px 4px rgba(0,0,0,0.05)`
- **Medium**: `0 4px 6px rgba(0,0,0,0.05)`
- **Large**: `0 12px 24px rgba(0,0,0,0.08)`

---

## 반응형 디자인

### Breakpoints
- **Desktop**: > 1024px
- **Tablet**: 768px - 1024px
- **Mobile**: < 768px

### 주요 반응형 기능
- 그리드 레이아웃 자동 조정 (3열 → 2열 → 1열)
- 모바일 햄버거 메뉴
- 터치 최적화된 UI
- 가변 폰트 크기

---

## 폴더 구조

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Header.css
│   │   ├── Layout.jsx
│   │   └── Layout.css
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Home.css
│   │   ├── Analysis.jsx
│   │   ├── Analysis.css
│   │   ├── ApiDocs.jsx
│   │   ├── ApiUsage.jsx
│   │   ├── ApiUsage.css
│   │   ├── AiEvalDocs.jsx
│   │   ├── Login.jsx
│   │   └── Signup.jsx
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
├── package.json
└── vite.config.js
```

---

## 주요 기능

### 1. URL 분석
- URL 입력 폼
- 실시간 분석 시뮬레이션
- 6개 항목 결과 카드

### 2. 문서 관리
- 카드 플립 애니메이션
- 문서 다운로드
- 반응형 그리드

### 3. API 키 관리
- 자동 키 생성
- 마스킹 처리
- 클립보드 복사
- 재발급 기능

### 4. 사용량 모니터링
- 실시간 통계
- 월별 제한 (1,000 호출)
- 사용률 시각화

---

## 브라우저 지원

- Chrome (최신 버전)
- Firefox (최신 버전)
- Safari (최신 버전)
- Edge (최신 버전)

---

## 라이선스

이 프로젝트는 오픈소스 프로젝트입니다.

---

## 개발팀

**TRAIN Korea | ThinkforBL**

AI 기반 콘텐츠 안전성 분석 솔루션 제공
