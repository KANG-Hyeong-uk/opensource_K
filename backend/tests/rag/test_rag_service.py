"""
RAG 서비스 테스트
"""
import pytest
from django.test import TestCase
from apps.rag.models import NewsDocument, DocumentEmbedding


class TestNewsDocumentModel(TestCase):
    """NewsDocument 모델 테스트"""

    def setUp(self):
        """테스트 데이터 설정"""
        self.document = NewsDocument.objects.create(
            news_id='TEST_001',
            category='테스트',
            title='테스트 제목',
            content='테스트 본문 내용입니다.',
            is_clickbait=True,
            process_type='A',
            process_pattern='99',
            process_level='하',
            sentence_count=1,
            sentences=[{'sentenceNo': 1, 'sentenceContent': '테스트 문장'}]
        )

    def test_document_creation(self):
        """문서 생성 테스트"""
        self.assertEqual(self.document.news_id, 'TEST_001')
        self.assertEqual(self.document.category, '테스트')
        self.assertTrue(self.document.is_clickbait)

    def test_full_text_property(self):
        """full_text 프로퍼티 테스트"""
        full_text = self.document.full_text
        self.assertIn('테스트 제목', full_text)
        self.assertIn('테스트 본문', full_text)

    def test_document_str(self):
        """__str__ 메서드 테스트"""
        str_repr = str(self.document)
        self.assertIn('TEST_001', str_repr)


class TestEmbeddingService(TestCase):
    """임베딩 서비스 테스트"""

    def setUp(self):
        """테스트 데이터 설정"""
        self.document = NewsDocument.objects.create(
            news_id='TEST_EMB_001',
            category='테스트',
            title='임베딩 테스트',
            content='임베딩 테스트 본문',
            is_clickbait=False,
            process_type='A',
            process_pattern='00',
            process_level='하',
            sentence_count=1
        )

    @pytest.mark.skip(reason="API 키 필요 - 통합 테스트에서 실행")
    def test_embedding_creation(self):
        """임베딩 생성 테스트 (실제 API 호출 필요)"""
        from apps.rag.services.embedding_service import EmbeddingService

        service = EmbeddingService()
        embedding = service.generate_embedding("테스트 텍스트")

        self.assertEqual(len(embedding), 768)
        self.assertIsInstance(embedding, list)


class TestSimilarityService(TestCase):
    """유사도 검색 서비스 테스트"""

    def setUp(self):
        """테스트 데이터 설정"""
        # 클릭베이트 문서
        self.clickbait_doc = NewsDocument.objects.create(
            news_id='CB_001',
            category='테스트',
            title='충격적인 사실!',
            content='여러분은 이것을 모를 것입니다.',
            is_clickbait=True,
            process_type='A',
            process_pattern='99',
            process_level='하',
            sentence_count=1
        )

        # 비클릭베이트 문서
        self.normal_doc = NewsDocument.objects.create(
            news_id='NC_001',
            category='테스트',
            title='경제 동향 보고서',
            content='최근 경제 지표에 따르면...',
            is_clickbait=False,
            process_type='A',
            process_pattern='00',
            process_level='하',
            sentence_count=1
        )

    def test_document_filtering(self):
        """문서 필터링 테스트"""
        clickbait_count = NewsDocument.objects.filter(is_clickbait=True).count()
        normal_count = NewsDocument.objects.filter(is_clickbait=False).count()

        self.assertEqual(clickbait_count, 1)
        self.assertEqual(normal_count, 1)


class TestRAGIntegration(TestCase):
    """RAG 통합 테스트"""

    @pytest.mark.skip(reason="전체 데이터셋 로드 필요 - 통합 테스트에서 실행")
    def test_rag_service_integration(self):
        """RAG 서비스 통합 테스트"""
        from apps.rag.services.rag_service import RAGService

        service = RAGService()
        context = service.get_context_for_analysis(
            title="테스트 제목",
            content="테스트 본문"
        )

        self.assertIn('clickbait_examples', context)
        self.assertIn('non_clickbait_examples', context)
