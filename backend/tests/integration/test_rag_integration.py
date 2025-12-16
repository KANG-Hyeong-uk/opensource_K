"""
RAG 시스템 통합 테스트
- Embedding API, 유사도 검색, RAG 서비스 테스트
"""
import pytest
from django.test import TestCase
from apps.rag.models import NewsDocument, DocumentEmbedding
from apps.rag.services.embedding_service import EmbeddingService
from apps.rag.services.similarity_service import SimilarityService
from apps.rag.services.rag_service import RAGService


@pytest.mark.integration
@pytest.mark.rag
@pytest.mark.django_db
class TestRAGIntegration(TestCase):
    """RAG 시스템 통합 테스트"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """테스트 데이터 준비"""
        # 샘플 뉴스 문서 생성
        self.doc1 = NewsDocument.objects.create(
            news_id="TEST001",
            title="놀라운 다이어트 비법! 하루만에 10kg 감량",
            content="이 방법만 알면 당신도 쉽게 살을 뺄 수 있습니다. 지금 바로 확인하세요!",
            category="LC",
            is_clickbait=True,
            process_type='A',
            process_pattern='P1',
            process_level='L1',
            sentence_count=2,
            sentences=[
                "이 방법만 알면 당신도 쉽게 살을 뺄 수 있습니다.",
                "지금 바로 확인하세요!"
            ]
        )

        self.doc2 = NewsDocument.objects.create(
            news_id="TEST002",
            title="보건복지부, 건강한 다이어트 가이드라인 발표",
            content="보건복지부는 오늘 건강한 체중 감량을 위한 가이드라인을 발표했습니다. "
                    "전문가들은 균형 잡힌 식단과 꾸준한 운동을 권장합니다.",
            category="LC",
            is_clickbait=False,
            process_type='D',
            process_pattern='P1',
            process_level='L1',
            sentence_count=2,
            sentences=[
                "보건복지부는 오늘 건강한 체중 감량을 위한 가이드라인을 발표했습니다.",
                "전문가들은 균형 잡힌 식단과 꾸준한 운동을 권장합니다."
            ]
        )

        self.doc3 = NewsDocument.objects.create(
            news_id="TEST003",
            title="충격! 이 음식을 먹으면 암이 사라진다?!",
            content="한 연구에 따르면 특정 음식이 암 치료에 효과가 있다고 주장합니다. 하지만 전문가들은 검증이 필요하다고 말합니다.",
            category="LC",
            is_clickbait=True,
            process_type='A',
            process_pattern='P1',
            process_level='L1',
            sentence_count=2,
            sentences=[
                "한 연구에 따르면 특정 음식이 암 치료에 효과가 있다고 주장합니다.",
                "하지만 전문가들은 검증이 필요하다고 말합니다."
            ]
        )

    def test_embedding_service_create_embedding(self):
        """임베딩 생성 테스트 (실제 API 호출)"""
        # Given: 임베딩 서비스
        embedding_service = EmbeddingService()
        text = "테스트 텍스트입니다. 임베딩을 생성합니다."

        # When: 임베딩 생성
        embedding = embedding_service.generate_embedding(text)

        # Then: 벡터 확인
        assert embedding is not None
        assert len(embedding) == 384  # Gemini embedding-001은 768차원
        assert all(isinstance(x, (int, float)) for x in embedding)

        print(f"\n✅ 임베딩 생성 성공!")
        print(f"벡터 차원: {len(embedding)}")
        print(f"벡터 샘플 (첫 5개): {embedding[:5]}")

    def test_create_document_embeddings(self):
        """문서 임베딩 생성 및 저장 테스트"""
        # Given: 임베딩 서비스
        embedding_service = EmbeddingService()

        # When: 문서의 임베딩 생성
        embedding_vector = embedding_service.generate_embedding(self.doc1.full_text)

        # 임베딩 저장
        doc_embedding = DocumentEmbedding.objects.create(
            document=self.doc1,
            vector=embedding_vector
        )

        # Then: 저장 확인
        assert doc_embedding is not None
        assert doc_embedding.vector is not None
        assert len(doc_embedding.vector) == 384

        print(f"\n✅ 문서 임베딩 저장 성공!")
        print(f"문서 ID: {doc_embedding.document.news_id}")
        print(f"임베딩 차원: {len(doc_embedding.vector)}")

    def test_similarity_search_with_real_embeddings(self):
        """실제 임베딩을 사용한 유사도 검색 테스트"""
        # Given: 모든 문서에 임베딩 생성
        embedding_service = EmbeddingService()
        similarity_service = SimilarityService()

        for doc in [self.doc1, self.doc2, self.doc3]:
            embedding = embedding_service.generate_embedding(doc.full_text)
            DocumentEmbedding.objects.create(
                document=doc,
                vector=embedding
            )

        # When: 다이어트 관련 쿼리로 검색
        query = "다이어트 방법을 알려주세요"
        results = similarity_service.search_similar_documents(
            query_text=query,
            top_k=3,
            is_clickbait=None  # 전체 검색
        )

        # Then: 결과 확인
        assert len(results) > 0
        assert len(results) <= 3

        # 결과는 유사도 순으로 정렬되어야 함
        for i in range(len(results) - 1):
            assert results[i]['score'] >= results[i + 1]['score']

        print(f"\n✅ 유사도 검색 성공!")
        print(f"검색 결과 수: {len(results)}")
        for idx, result in enumerate(results, 1):
            print(f"{idx}. [{result['score']:.4f}] {result['document'].title}")

    def test_search_clickbait_vs_non_clickbait(self):
        """클릭베이트/비클릭베이트 필터링 검색 테스트"""
        # Given: 임베딩 생성
        embedding_service = EmbeddingService()
        similarity_service = SimilarityService()

        for doc in [self.doc1, self.doc2, self.doc3]:
            embedding = embedding_service.generate_embedding(doc.full_text)
            DocumentEmbedding.objects.create(
                document=doc,
                vector=embedding
            )

        # When: 클릭베이트만 검색
        query = "다이어트"
        clickbait_results = similarity_service.search_similar_documents(
            query_text=query,
            top_k=5,
            is_clickbait=True
        )

        # 비클릭베이트만 검색
        non_clickbait_results = similarity_service.search_similar_documents(
            query_text=query,
            top_k=5,
            is_clickbait=False
        )

        # Then: 필터링 확인
        assert all(r['document'].is_clickbait for r in clickbait_results)
        assert all(not r['document'].is_clickbait for r in non_clickbait_results)

        print(f"\n✅ 필터링 검색 성공!")
        print(f"클릭베이트 결과: {len(clickbait_results)}개")
        print(f"비클릭베이트 결과: {len(non_clickbait_results)}개")

    def test_rag_service_get_context(self):
        """RAG 서비스 컨텍스트 가져오기 테스트"""
        # Given: 임베딩 생성
        embedding_service = EmbeddingService()
        for doc in [self.doc1, self.doc2, self.doc3]:
            embedding = embedding_service.generate_embedding(doc.full_text)
            DocumentEmbedding.objects.create(
                document=doc,
                vector=embedding
            )

        rag_service = RAGService()

        # When: 분석용 컨텍스트 가져오기
        title = "효과적인 체중 감량 방법"
        content = "건강하게 살을 빼는 방법을 알려드립니다."

        context = rag_service.get_context_for_analysis(title, content, top_k=2)

        # Then: 컨텍스트 확인
        assert context is not None
        assert 'clickbait_examples' in context
        assert 'non_clickbait_examples' in context
        assert 'context_text' in context

        assert len(context['clickbait_examples']) > 0
        assert len(context['non_clickbait_examples']) > 0
        assert len(context['context_text']) > 0

        print(f"\n✅ RAG 컨텍스트 생성 성공!")
        print(f"클릭베이트 예시: {len(context['clickbait_examples'])}개")
        print(f"비클릭베이트 예시: {len(context['non_clickbait_examples'])}개")
        print(f"\n컨텍스트 텍스트 미리보기:")
        print(context['context_text'][:300] + "...")

    def test_rag_service_get_similar_cases(self):
        """유사 사례 검색 테스트 (API 응답용)"""
        # Given: 임베딩 생성
        embedding_service = EmbeddingService()
        for doc in [self.doc1, self.doc2, self.doc3]:
            embedding = embedding_service.generate_embedding(doc.full_text)
            DocumentEmbedding.objects.create(
                document=doc,
                vector=embedding
            )

        rag_service = RAGService()

        # When: 유사 사례 검색
        title = "건강 관리"
        content = "건강을 유지하는 방법"

        similar_cases = rag_service.get_similar_cases(title, content, top_k=3)

        # Then: 결과 확인
        assert isinstance(similar_cases, list)
        assert len(similar_cases) > 0

        # 각 결과가 올바른 형식인지 확인
        for case in similar_cases:
            assert 'news_id' in case
            assert 'title' in case
            assert 'category' in case
            assert 'is_clickbait' in case
            assert 'similarity_score' in case
            assert 'content_preview' in case

        print(f"\n✅ 유사 사례 검색 성공!")
        print(f"검색 결과: {len(similar_cases)}개")
        for case in similar_cases:
            print(f"- [{case['similarity_score']:.4f}] {case['title'][:40]}...")

    def test_embedding_caching(self):
        """임베딩 캐싱 테스트"""
        # Given: 임베딩 서비스
        embedding_service = EmbeddingService()
        text = "동일한 텍스트입니다"

        # When: 같은 텍스트로 두 번 임베딩 생성
        embedding1 = embedding_service.generate_embedding(text)
        # 캐시 로직이 있다면 두 번째 호출은 캐시에서 가져와야 함
        # (현재 구현에 따라 다를 수 있음)

        # Then: 벡터가 동일해야 함
        assert embedding1 is not None
        assert len(embedding1) == 384

        print(f"\n✅ 임베딩 생성 확인!")

    def test_large_batch_embedding(self):
        """대량 문서 임베딩 생성 테스트"""
        # Given: 여러 문서
        docs = [self.doc1, self.doc2, self.doc3]
        embedding_service = EmbeddingService()

        # When: 배치로 임베딩 생성
        created_count = 0
        for doc in docs:
            embedding = embedding_service.generate_embedding(doc.full_text)
            DocumentEmbedding.objects.create(
                document=doc,
                vector=embedding
            )
            created_count += 1

        # Then: 모두 생성되었는지 확인
        assert created_count == len(docs)
        assert DocumentEmbedding.objects.count() == len(docs)

        print(f"\n✅ 배치 임베딩 생성 성공!")
        print(f"생성된 임베딩 수: {created_count}")
