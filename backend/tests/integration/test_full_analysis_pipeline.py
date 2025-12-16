"""
전체 URL 분석 파이프라인 통합 테스트
- Selenium → RAG → Gemini → 결과 저장
- 실제 엔드-투-엔드 테스트
"""
import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from apps.detection.services.analysis_service import URLAnalysisService
from apps.detection.models import AnalysisResult
from apps.rag.models import NewsDocument, DocumentEmbedding
from apps.rag.services.embedding_service import EmbeddingService


@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.django_db
class TestFullAnalysisPipeline(TestCase):
    """전체 분석 파이프라인 통합 테스트"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """테스트 사용자 및 RAG 데이터 준비"""
        # 테스트 사용자 생성
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # RAG용 샘플 데이터 생성
        self._setup_rag_data()

    def _setup_rag_data(self):
        """RAG 테스트용 샘플 데이터 생성"""
        embedding_service = EmbeddingService()

        # 클릭베이트 예시
        clickbait_docs = [
            {
                "news_id": "CB001",
                "title": "믿을 수 없는 충격! 이것만 먹으면 건강해진다",
                "content": "한 연구에 따르면 이 음식만 먹으면 모든 질병이 사라진다고 합니다!",
                "category": "LC",
                "is_clickbait": True,
                "process_type": "A",
                "process_pattern": "P1",
                "process_level": "L1",
                "sentence_count": 1,
                "sentences": ["한 연구에 따르면 이 음식만 먹으면 모든 질병이 사라진다고 합니다!"]
            },
            {
                "news_id": "CB002",
                "title": "당신이 몰랐던 놀라운 비밀! 지금 확인하세요",
                "content": "이 방법을 쓰면 당신의 인생이 완전히 바뀔 것입니다.",
                "category": "GB",
                "is_clickbait": True,
                "process_type": "A",
                "process_pattern": "P1",
                "process_level": "L1",
                "sentence_count": 1,
                "sentences": ["이 방법을 쓰면 당신의 인생이 완전히 바뀔 것입니다."]
            }
        ]

        # 정상 뉴스 예시
        normal_docs = [
            {
                "news_id": "NM001",
                "title": "보건복지부, 건강 가이드라인 발표",
                "content": "보건복지부는 오늘 국민 건강을 위한 새로운 가이드라인을 발표했습니다. 전문가들은 균형 잡힌 식단과 운동을 권장합니다.",
                "category": "LC",
                "is_clickbait": False,
                "process_type": "D",
                "process_pattern": "P1",
                "process_level": "L1",
                "sentence_count": 2,
                "sentences": [
                    "보건복지부는 오늘 국민 건강을 위한 새로운 가이드라인을 발표했습니다.",
                    "전문가들은 균형 잡힌 식단과 운동을 권장합니다."
                ]
            },
            {
                "news_id": "NM002",
                "title": "전문가들, 건강한 생활 습관 중요성 강조",
                "content": "의료 전문가들은 규칙적인 생활 습관이 건강 유지에 중요하다고 강조했습니다.",
                "category": "LC",
                "is_clickbait": False,
                "process_type": "D",
                "process_pattern": "P1",
                "process_level": "L1",
                "sentence_count": 1,
                "sentences": ["의료 전문가들은 규칙적인 생활 습관이 건강 유지에 중요하다고 강조했습니다."]
            }
        ]

        # 문서 생성 및 임베딩
        for doc_data in clickbait_docs + normal_docs:
            doc = NewsDocument.objects.create(**doc_data)
            embedding = embedding_service.generate_embedding(doc.full_text)
            DocumentEmbedding.objects.create(
                document=doc,
                vector=embedding,
                model_name=embedding_service.model_name,
                dimension=embedding_service.dimension
            )

        print(f"\n✅ RAG 샘플 데이터 {len(clickbait_docs) + len(normal_docs)}개 생성 완료!")

    @pytest.mark.slow
    def test_full_pipeline_with_rag(self):
        """전체 파이프라인 테스트 (RAG 활성화)"""
        # Given: RAG가 활성화된 분석 서비스
        service = URLAnalysisService(use_rag=True)
        test_url = "https://www.example.com"

        # When: URL 분석 실행
        result = service.analyze_url(test_url, user=self.user)

        # Then: 결과 검증
        assert result is not None
        assert isinstance(result, AnalysisResult)
        assert result.url == test_url
        assert result.user == self.user
        assert result.title is not None
        assert len(result.title) > 0
        assert result.content is not None

        # 분석 결과 확인
        assert hasattr(result, 'is_clickbait')
        assert hasattr(result, 'is_hate_speech')
        assert hasattr(result, 'is_misinformation')
        assert hasattr(result, 'confidence_score')

        # RAG 사용 여부 확인
        assert result.analysis_details is not None
        assert 'rag_used' in result.analysis_details
        if result.analysis_details['rag_used']:
            assert 'rag_examples_count' in result.analysis_details

        print(f"\n✅ 전체 파이프라인 테스트 성공 (RAG 활성화)!")
        print(f"URL: {result.url}")
        print(f"제목: {result.title}")
        print(f"클릭베이트: {result.is_clickbait}")
        print(f"혐오 표현: {result.is_hate_speech}")
        print(f"허위정보: {result.is_misinformation}")
        print(f"신뢰도: {result.confidence_score}")
        print(f"RAG 사용: {result.analysis_details.get('rag_used', False)}")
        if result.analysis_details.get('rag_used'):
            print(f"RAG 예시 수: {result.analysis_details.get('rag_examples_count')}")

    @pytest.mark.slow
    def test_full_pipeline_without_rag(self):
        """전체 파이프라인 테스트 (RAG 비활성화)"""
        # Given: RAG가 비활성화된 분석 서비스
        service = URLAnalysisService(use_rag=False)
        test_url = "https://www.example.com"

        # When: URL 분석 실행
        result = service.analyze_url(test_url, user=self.user)

        # Then: 결과 검증
        assert result is not None
        assert isinstance(result, AnalysisResult)
        assert result.url == test_url

        # RAG 미사용 확인
        assert result.analysis_details is not None
        assert result.analysis_details.get('rag_used') == False

        print(f"\n✅ 전체 파이프라인 테스트 성공 (RAG 비활성화)!")
        print(f"URL: {result.url}")
        print(f"제목: {result.title}")
        print(f"클릭베이트: {result.is_clickbait}")
        print(f"RAG 사용: {result.analysis_details.get('rag_used', False)}")

    def test_pipeline_with_clickbait_url(self):
        """클릭베이트 URL 분석 테스트"""
        # Given: 클릭베이트가 의심되는 URL (실제로는 example.com 사용)
        service = URLAnalysisService(use_rag=True)
        test_url = "https://www.example.com"

        # When: 분석 실행
        result = service.analyze_url(test_url, user=self.user)

        # Then: 결과가 저장되었는지 확인
        assert result is not None
        assert AnalysisResult.objects.filter(url=test_url).exists()

        # 데이터베이스에서 다시 조회
        saved_result = AnalysisResult.objects.get(id=result.id)
        assert saved_result.url == test_url
        assert saved_result.user == self.user

        print(f"\n✅ 클릭베이트 URL 분석 성공!")
        print(f"분석 ID: {saved_result.id}")
        print(f"결과: {saved_result.get_risk_level()}")

    def test_pipeline_with_normal_news_url(self):
        """정상 뉴스 URL 분석 테스트"""
        # Given: 정상 뉴스 URL
        service = URLAnalysisService(use_rag=True)
        test_url = "https://www.example.com"

        # When: 분석 실행
        result = service.analyze_url(test_url, user=self.user)

        # Then: 결과 확인
        assert result is not None
        # is_safe 속성이 있다면 확인
        if hasattr(result, 'is_safe'):
            print(f"안전 여부: {result.is_safe}")

        print(f"\n✅ 정상 뉴스 URL 분석 성공!")
        print(f"위험 레벨: {result.get_risk_level()}")

    def test_multiple_analyses_tracking(self):
        """여러 분석 추적 테스트"""
        # Given: 분석 서비스
        service = URLAnalysisService(use_rag=True)
        urls = [
            "https://www.example.com",
            "https://www.example.org"
        ]

        # When: 여러 URL 분석
        results = []
        for url in urls:
            result = service.analyze_url(url, user=self.user)
            results.append(result)

        # Then: 모든 결과가 저장되었는지 확인
        assert len(results) == len(urls)
        assert AnalysisResult.objects.filter(user=self.user).count() >= len(urls)

        # 통계 확인
        stats = service.get_statistics(user=self.user)
        assert stats['total_analyses'] >= len(urls)

        print(f"\n✅ 여러 URL 분석 추적 성공!")
        print(f"분석 수: {len(results)}")
        print(f"통계: {stats}")

    def test_user_history_retrieval(self):
        """사용자 분석 이력 조회 테스트"""
        # Given: 사용자가 이미 분석을 수행함
        service = URLAnalysisService(use_rag=True)
        service.analyze_url("https://www.example.com", user=self.user)

        # When: 이력 조회
        history = service.get_user_history(user=self.user, limit=10)

        # Then: 이력 확인
        assert len(history) > 0
        assert all(h.user == self.user for h in history)

        # 시간 순으로 정렬되어 있는지 확인
        if len(history) > 1:
            for i in range(len(history) - 1):
                assert history[i].created_at >= history[i + 1].created_at

        print(f"\n✅ 사용자 이력 조회 성공!")
        print(f"이력 수: {len(history)}")
        for idx, h in enumerate(history[:3], 1):
            print(f"{idx}. {h.url} - {h.created_at}")

    def test_analysis_details_structure(self):
        """분석 상세 정보 구조 테스트"""
        # Given: 분석 서비스
        service = URLAnalysisService(use_rag=True)

        # When: 분석 실행
        result = service.analyze_url("https://www.example.com", user=self.user)

        # Then: 상세 정보 구조 확인
        assert result.analysis_details is not None
        assert isinstance(result.analysis_details, dict)

        # 필수 필드 확인
        assert 'rag_used' in result.analysis_details

        if result.analysis_details.get('details'):
            details = result.analysis_details['details']
            assert 'clickbait' in details or 'hate_speech' in details or 'misinformation' in details

        print(f"\n✅ 분석 상세 정보 구조 확인!")
        print(f"상세 정보 키: {list(result.analysis_details.keys())}")

    @pytest.mark.slow
    def test_end_to_end_real_workflow(self):
        """실제 워크플로우 엔드-투-엔드 테스트"""
        print("\n" + "="*60)
        print("🚀 전체 엔드-투-엔드 테스트 시작")
        print("="*60)

        # 1단계: 사용자 생성
        print("\n1️⃣ 사용자 생성...")
        user = self.user
        print(f"   ✅ 사용자: {user.username}")

        # 2단계: 분석 서비스 초기화
        print("\n2️⃣ 분석 서비스 초기화 (RAG 활성화)...")
        service = URLAnalysisService(use_rag=True)
        print("   ✅ 서비스 초기화 완료")

        # 3단계: URL 크롤링
        print("\n3️⃣ URL 크롤링 시작...")
        test_url = "https://www.example.com"
        print(f"   URL: {test_url}")

        # 4단계: 전체 분석 실행
        print("\n4️⃣ 전체 분석 파이프라인 실행...")
        print("   - Selenium 크롤링...")
        print("   - RAG 유사 문서 검색...")
        print("   - Gemini LLM 분석...")
        print("   - 결과 저장...")

        result = service.analyze_url(test_url, user=user)

        # 5단계: 결과 확인
        print("\n5️⃣ 분석 결과:")
        print(f"   📰 제목: {result.title}")
        print(f"   🔗 URL: {result.url}")
        print(f"   📊 클릭베이트: {result.is_clickbait}")
        print(f"   💬 혐오 표현: {result.is_hate_speech}")
        print(f"   ⚠️  허위정보: {result.is_misinformation}")
        print(f"   🎯 신뢰도: {result.confidence_score}")
        print(f"   ⚡ 위험 레벨: {result.get_risk_level()}")

        if result.analysis_details.get('rag_used'):
            print(f"   🔍 RAG 사용: ✅")
            rag_count = result.analysis_details.get('rag_examples_count', {})
            print(f"   📚 유사 예시: 클릭베이트 {rag_count.get('clickbait', 0)}개, "
                  f"정상 {rag_count.get('non_clickbait', 0)}개")
        else:
            print(f"   🔍 RAG 사용: ❌")

        # 6단계: 검증
        print("\n6️⃣ 결과 검증...")
        assert result is not None
        assert result.id is not None
        assert AnalysisResult.objects.filter(id=result.id).exists()
        print("   ✅ 모든 검증 통과!")

        print("\n" + "="*60)
        print("✨ 전체 엔드-투-엔드 테스트 완료!")
        print("="*60)

        return result
