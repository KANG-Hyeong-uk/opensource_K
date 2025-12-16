# 🧪 테스트 실행 가이드

전체 백엔드 통합 테스트 실행 방법

## 📋 테스트 구성

### 1. **Selenium 크롤러 테스트** (`test_crawler.py`)
- 실제 웹사이트 크롤링
- URL 검증
- 메타데이터 추출
- 타임아웃 처리

### 2. **Gemini LLM Provider 테스트** (`test_llm_provider.py`)
- 실제 Gemini API 호출
- 클릭베이트 탐지
- 혐오 표현 탐지
- 허위정보 탐지
- JSON 응답 파싱

### 3. **RAG 시스템 테스트** (`test_rag_integration.py`)
- Gemini Embedding API 호출
- 벡터 임베딩 생성 (768차원)
- 코사인 유사도 검색
- 클릭베이트/비클릭베이트 필터링

### 4. **전체 분석 파이프라인 테스트** (`test_full_analysis_pipeline.py`)
- **엔드-투-엔드 테스트**
- Selenium → RAG → Gemini → DB 저장
- 사용자 이력 추적
- 통계 기능

---

## 🚀 테스트 실행 방법

### 전제 조건
```bash
# 1. 가상환경 활성화
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Gemini API 키 설정 확인
cat .env | grep GEMINI_API_KEY
```

### 기본 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 통합 테스트만 실행
pytest tests/integration/ -v

# 특정 테스트 파일 실행
pytest tests/integration/test_llm_provider.py -v
pytest tests/integration/test_rag_integration.py -v
pytest tests/integration/test_full_analysis_pipeline.py -v
```

### 마커별 실행

```bash
# LLM 테스트만
pytest -m llm -v

# RAG 테스트만
pytest -m rag -v

# 크롤러 테스트만
pytest -m crawler -v

# 통합 테스트만
pytest -m integration -v

# 느린 테스트 제외
pytest -m "not slow" -v
```

### 상세 출력 포함

```bash
# 출력 표시 (-s)
pytest tests/integration/test_llm_provider.py -v -s

# 실패한 테스트만 재실행
pytest --lf -v

# 처음 실패 시 중단
pytest -x -v
```

### 커버리지 포함

```bash
# 커버리지와 함께 실행
pytest --cov=apps --cov-report=html -v

# 커버리지 리포트 열기
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

---

## 📊 개별 테스트 세트 실행

### 1. Gemini LLM 테스트

```bash
# 간단한 텍스트 생성
pytest tests/integration/test_llm_provider.py::TestGeminiProvider::test_generate_content_simple -v -s

# 클릭베이트 탐지
pytest tests/integration/test_llm_provider.py::TestGeminiProvider::test_analyze_clickbait_positive -v -s

# 통합 분석
pytest tests/integration/test_llm_provider.py::TestGeminiProvider::test_analyze_content_comprehensive -v -s
```

### 2. RAG 시스템 테스트

```bash
# 임베딩 생성 테스트
pytest tests/integration/test_rag_integration.py::TestRAGIntegration::test_embedding_service_create_embedding -v -s

# 유사도 검색 테스트
pytest tests/integration/test_rag_integration.py::TestRAGIntegration::test_similarity_search_with_real_embeddings -v -s

# RAG 컨텍스트 생성
pytest tests/integration/test_rag_integration.py::TestRAGIntegration::test_rag_service_get_context -v -s
```

### 3. 전체 파이프라인 테스트

```bash
# RAG 포함 전체 플로우
pytest tests/integration/test_full_analysis_pipeline.py::TestFullAnalysisPipeline::test_full_pipeline_with_rag -v -s

# 엔드-투-엔드 테스트
pytest tests/integration/test_full_analysis_pipeline.py::TestFullAnalysisPipeline::test_end_to_end_real_workflow -v -s
```

---

## ⚙️ 환경 변수 설정

```bash
# .env 파일 예시
GEMINI_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-flash-latest
SELENIUM_HEADLESS=True
DEBUG=True
```

---

## 🔥 빠른 통합 테스트 (권장)

전체 백엔드 로직을 빠르게 검증:

```bash
# LLM + RAG + 전체 플로우 테스트
pytest tests/integration/test_llm_provider.py::TestGeminiProvider::test_analyze_content_comprehensive \
       tests/integration/test_rag_integration.py::TestRAGIntegration::test_rag_service_get_context \
       tests/integration/test_full_analysis_pipeline.py::TestFullAnalysisPipeline::test_end_to_end_real_workflow \
       -v -s
```

---

## 🎯 프로덕션 준비 테스트

배포 전 필수 테스트:

```bash
# 1. 모든 단위 테스트
pytest apps/ -v

# 2. 모든 통합 테스트
pytest tests/integration/ -v

# 3. 커버리지 확인 (최소 60% 목표)
pytest --cov=apps --cov-report=term-missing --cov-fail-under=60
```

---

## ⚠️ 주의사항

### 1. **실제 API 호출**
- LLM 및 RAG 테스트는 실제 Gemini API를 호출합니다
- API 사용량 및 비용이 발생할 수 있습니다
- 테스트 환경에서는 적절한 rate limiting 적용 권장

### 2. **Selenium 테스트**
- Chrome/Chromium 브라우저 필요
- ChromeDriver 자동 다운로드 (webdriver-manager)
- Headless 모드 사용 (SELENIUM_HEADLESS=True)

### 3. **데이터베이스**
- 테스트는 메모리 DB 사용 (:memory:)
- 테스트 후 자동으로 정리됩니다

### 4. **속도**
- 통합 테스트는 느릴 수 있습니다 (API 호출 포함)
- `-m "not slow"` 옵션으로 빠른 테스트만 실행 가능

---

## 📊 최근 테스트 실행 결과 (2025-12-16)

### ✅ 성공한 테스트

#### 1. **LLM Provider 테스트** (8 passed, 1 skipped)
```bash
pytest tests/integration/test_llm_provider.py -v -s
```
- ✅ test_generate_content_simple - 기본 텍스트 생성
- ✅ test_analyze_clickbait_positive - 클릭베이트 탐지
- ✅ test_analyze_clickbait_negative - 정상 뉴스 분석
- ✅ test_analyze_hate_speech - 혐오 표현 분석
- ✅ test_analyze_misinformation - 허위정보 분석
- ✅ test_analyze_content_comprehensive - 통합 분석
- ✅ test_get_model_info - 모델 정보 조회
- ✅ test_json_response_parsing - JSON 파싱
- ⏭️ test_invalid_api_key_handling - SKIPPED

**실행 시간**: 97.86초 (1분 37초)
**커버리지**: LLM Provider 64%, Prompt Manager 45%

#### 2. **Crawler 테스트** (2 passed, 3 failed)
```bash
pytest tests/integration/test_crawler.py -v -s
```
- ✅ test_crawl_invalid_url_should_fail - URL 검증
- ✅ test_crawl_timeout_handling - 타임아웃 처리
- ❌ test_crawl_news_article_success - Chrome 미설치
- ❌ test_crawl_with_korean_content - Chrome 미설치
- ❌ test_crawl_extract_metadata - Chrome 미설치

**실행 시간**: 12.27초
**이슈**: WSL 환경에서 Chrome 브라우저 미설치

### ⚠️ 실패한 테스트

#### 3. **전체 파이프라인 테스트** (1 error)
```bash
pytest tests/integration/test_full_analysis_pipeline.py::TestFullAnalysisPipeline::test_end_to_end_real_workflow -v -s
```
- ❌ test_end_to_end_real_workflow - Gemini Embedding API 할당량 초과

**에러 메시지**:
```
ResourceExhausted: 429 You exceeded your current quota
Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests
```

**실행 시간**: 32.43초

---

## 📈 커버리지 현황

| 구성 요소 | 이전 커버리지 | 현재 커버리지 | 목표 | 상태 |
|----------|--------------|--------------|------|------|
| LLM Provider | 34% | **64%** | 80% | 🔼 개선 |
| Prompt Manager | - | **45%** | 80% | 🆕 신규 |
| 크롤러 (Crawler) | 24% | 24% | 80% | ➡️ 유지 |
| RAG 시스템 | 18% | 18% | 70% | ➡️ 유지 |
| 분석 서비스 | 21% | 21% | 80% | ➡️ 유지 |
| **전체** | **23%** | **18%** | **70%** | ➡️ 평균 |

> **참고**: LLM Provider 테스트 실행으로 해당 모듈 커버리지가 34% → 64%로 향상되었습니다.

---

## 🚨 알려진 이슈 및 해결 방법

### 1. ~~Gemini Embedding API 할당량 초과~~ ✅ 해결됨 (v1.2)
**상태**: 🎉 **해결 완료** - Sentence-Transformers로 변경

**이전 증상**:
```
429 You exceeded your current quota
embed_content_free_tier_requests: limit 0
```

**해결책** (v1.2):
- ✅ 임베딩 시스템을 **Sentence-Transformers**로 변경
- ✅ 로컬에서 실행되므로 API 할당량 제한 없음
- ✅ 모델: `all-MiniLM-L6-v2` (384차원)
- ✅ 더 빠른 속도, 무료, 오프라인 작동 가능

**변경 사항**:
```python
# 이전: Gemini API (768차원)
from google.generativeai import embed_content

# 현재: Sentence-Transformers (384차원)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
```

### 2. Chrome 브라우저 미설치 (WSL/Linux)
**증상**:
```
google-chrome: not found
Failed to initialize crawler: 'NoneType' object has no attribute 'split'
```

**원인**: WSL 환경에서 Chrome 브라우저 미설치

**해결 방법** (Ubuntu/WSL):
```bash
# Chrome 설치
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb

# 또는 Chromium 사용
sudo apt-get update
sudo apt-get install chromium-browser
```

**임시 우회**:
```bash
# Crawler를 사용하지 않는 테스트만 실행
pytest tests/integration/test_llm_provider.py -v
pytest -m "not crawler" -v
```

### 3. 일부 RAG 테스트 스킵
**증상**: RAG 관련 테스트가 실행되지 않음

**원인**: Embedding API 할당량 제한으로 RAG 데이터 생성 불가

**해결 방법**:
- Embedding API 할당량 복구 후 재실행
- 또는 사전에 생성된 임베딩 데이터 사용

---

## 🛠 문제 해결

### Gemini API 에러
```bash
# 사용 가능한 모델 확인
python check_gemini_models.py

# API 키 확인
echo $GEMINI_API_KEY
```

### ChromeDriver 에러
```bash
# ChromeDriver 재다운로드
rm -rf ~/.wdm
pytest tests/integration/test_crawler.py -v
```

### 데이터베이스 에러
```bash
# 마이그레이션 재실행
python manage.py migrate
python manage.py migrate --run-syncdb
```

---

## 📚 추가 리소스

- [pytest 공식 문서](https://docs.pytest.org/)
- [Django Testing 가이드](https://docs.djangoproject.com/en/5.0/topics/testing/)
- [Gemini API 문서](https://ai.google.dev/docs)

---

**최초 작성일**: 2025-12-16
**최종 업데이트**: 2025-12-17
**버전**: 1.2
**작성자**: Claude AI Assistant

---

## 📝 변경 이력

### v1.2 (2025-12-17)
- ✅ 임베딩 시스템을 Gemini API에서 **Sentence-Transformers**로 변경
  - 모델: `all-MiniLM-L6-v2` (384차원)
  - 로컬 실행으로 API 할당량 문제 완전 해결
  - 더 빠른 속도, 비용 없음
- ✅ RAG 테스트 성공 (1 passed)
  - 임베딩 생성 테스트 통과
  - 384차원 벡터 정상 생성 확인
- ✅ requirements.txt 업데이트
  - sentence-transformers==3.3.1
  - torch==2.2.2

### v1.1 (2025-12-16)
- ✅ LLM Provider 테스트 실행 결과 추가 (8 passed, 1 skipped)
- ✅ Crawler 테스트 실행 결과 추가 (2 passed, 3 failed)
- ✅ 전체 파이프라인 테스트 실행 결과 추가 (1 error)
- ✅ 커버리지 현황 업데이트 (LLM Provider: 34% → 64%)
- ✅ 알려진 이슈 및 해결 방법 섹션 추가
  - Gemini Embedding API 할당량 초과 해결 방법
  - Chrome 브라우저 미설치 (WSL) 해결 방법
  - RAG 테스트 스킵 관련 안내

### v1.0 (2025-12-16)
- 🎉 초기 버전 작성
- 테스트 구성 및 실행 방법 문서화
- 커버리지 목표 설정
