"""
유사도 검색 서비스
- 코사인 유사도 기반 문서 검색
- 캐싱을 통한 성능 최적화
"""
import logging
import hashlib
from typing import List, Dict, Optional, Tuple
import numpy as np
from django.db.models import Q

from apps.rag.models import NewsDocument, DocumentEmbedding, SimilarityCache
from apps.rag.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class SimilarityService:
    """유사도 검색 서비스"""

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def cosine_similarity(
        self,
        vector1: List[float],
        vector2: List[float]
    ) -> float:
        """
        두 벡터 간의 코사인 유사도 계산

        Args:
            vector1: 첫 번째 벡터
            vector2: 두 번째 벡터

        Returns:
            코사인 유사도 (-1 ~ 1)
        """
        v1 = np.array(vector1)
        v2 = np.array(vector2)

        # 코사인 유사도 계산
        dot_product = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = dot_product / (norm1 * norm2)
        return float(similarity)

    def _generate_query_hash(self, query: str) -> str:
        """쿼리 텍스트의 해시 생성 (캐싱용)"""
        return hashlib.sha256(query.encode()).hexdigest()

    def search_similar_documents(
        self,
        query_text: str,
        top_k: int = 5,
        is_clickbait: Optional[bool] = None,
        use_cache: bool = True
    ) -> List[Dict]:
        """
        쿼리와 유사한 문서 검색

        Args:
            query_text: 검색 쿼리 텍스트
            top_k: 상위 k개 결과 반환
            is_clickbait: 클릭베이트 필터 (None이면 전체 검색)
            use_cache: 캐시 사용 여부

        Returns:
            유사 문서 리스트 [{"document": NewsDocument, "score": float}, ...]
        """
        try:
            # 캐시 확인
            if use_cache:
                cached_result = self._get_cached_result(query_text, is_clickbait)
                if cached_result:
                    logger.info(f"캐시에서 결과 반환: {query_text[:50]}")
                    return cached_result

            # 쿼리 임베딩 생성
            logger.info(f"쿼리 임베딩 생성 중: {query_text[:50]}")
            query_embedding = self.embedding_service.generate_query_embedding(query_text)

            # 검색할 문서 필터링
            queryset = DocumentEmbedding.objects.select_related('document')

            if is_clickbait is not None:
                queryset = queryset.filter(document__is_clickbait=is_clickbait)

            # 모든 문서와 유사도 계산
            similarities = []
            for doc_embedding in queryset:
                try:
                    vector = doc_embedding.get_vector()
                    score = self.cosine_similarity(query_embedding, vector)

                    similarities.append({
                        'document': doc_embedding.document,
                        'score': score
                    })
                except Exception as e:
                    logger.error(f"유사도 계산 실패 (문서 ID: {doc_embedding.document.news_id}): {str(e)}")
                    continue

            # 유사도 기준 정렬
            similarities.sort(key=lambda x: x['score'], reverse=True)

            # 상위 k개 결과
            results = similarities[:top_k]

            # 캐시 저장
            if use_cache and results:
                self._save_cache(query_text, results, is_clickbait)

            logger.info(f"검색 완료: {len(results)}개 문서 반환")
            return results

        except Exception as e:
            logger.error(f"유사도 검색 실패: {str(e)}")
            raise

    def search_similar_by_document(
        self,
        document_id: int,
        top_k: int = 5,
        exclude_self: bool = True
    ) -> List[Dict]:
        """
        특정 문서와 유사한 문서 검색

        Args:
            document_id: 기준 문서 ID
            top_k: 상위 k개 결과 반환
            exclude_self: 자기 자신 제외 여부

        Returns:
            유사 문서 리스트
        """
        try:
            # 기준 문서 가져오기
            base_embedding = DocumentEmbedding.objects.select_related('document').get(
                document_id=document_id
            )
            base_vector = base_embedding.get_vector()

            # 모든 문서와 유사도 계산
            similarities = []
            queryset = DocumentEmbedding.objects.select_related('document')

            if exclude_self:
                queryset = queryset.exclude(document_id=document_id)

            for doc_embedding in queryset:
                try:
                    vector = doc_embedding.get_vector()
                    score = self.cosine_similarity(base_vector, vector)

                    similarities.append({
                        'document': doc_embedding.document,
                        'score': score
                    })
                except Exception as e:
                    logger.error(f"유사도 계산 실패: {str(e)}")
                    continue

            # 유사도 기준 정렬
            similarities.sort(key=lambda x: x['score'], reverse=True)

            # 상위 k개 결과
            results = similarities[:top_k]

            logger.info(f"문서 기반 검색 완료: {len(results)}개 문서 반환")
            return results

        except Exception as e:
            logger.error(f"문서 기반 검색 실패: {str(e)}")
            raise

    def _get_cached_result(
        self,
        query_text: str,
        is_clickbait: Optional[bool]
    ) -> Optional[List[Dict]]:
        """캐시에서 검색 결과 가져오기"""
        try:
            query_hash = self._generate_query_hash(f"{query_text}_{is_clickbait}")
            cache = SimilarityCache.objects.get(query_hash=query_hash)

            # 히트 카운트 증가
            cache.hit_count += 1
            cache.save()

            # 캐시된 결과를 Document 객체로 변환
            results = []
            for item in cache.results:
                try:
                    document = NewsDocument.objects.get(news_id=item['news_id'])
                    results.append({
                        'document': document,
                        'score': item['score']
                    })
                except NewsDocument.DoesNotExist:
                    logger.warning(f"캐시된 문서를 찾을 수 없음: {item['news_id']}")
                    continue

            return results if results else None

        except SimilarityCache.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"캐시 조회 실패: {str(e)}")
            return None

    def _save_cache(
        self,
        query_text: str,
        results: List[Dict],
        is_clickbait: Optional[bool]
    ):
        """검색 결과를 캐시에 저장"""
        try:
            query_hash = self._generate_query_hash(f"{query_text}_{is_clickbait}")

            # 결과를 JSON 형식으로 변환
            cache_data = [
                {
                    'news_id': item['document'].news_id,
                    'score': item['score']
                }
                for item in results
            ]

            # 캐시 저장 또는 업데이트
            SimilarityCache.objects.update_or_create(
                query_hash=query_hash,
                defaults={
                    'query_text': query_text[:500],
                    'results': cache_data,
                    'hit_count': 0
                }
            )

            logger.debug(f"캐시 저장 완료: {query_text[:50]}")

        except Exception as e:
            logger.error(f"캐시 저장 실패: {str(e)}")

    def get_statistics(self) -> Dict:
        """검색 통계 반환"""
        total_docs = NewsDocument.objects.count()
        total_embeddings = DocumentEmbedding.objects.count()
        clickbait_count = NewsDocument.objects.filter(is_clickbait=True).count()
        non_clickbait_count = NewsDocument.objects.filter(is_clickbait=False).count()
        cache_count = SimilarityCache.objects.count()

        return {
            'total_documents': total_docs,
            'total_embeddings': total_embeddings,
            'clickbait_documents': clickbait_count,
            'non_clickbait_documents': non_clickbait_count,
            'cache_entries': cache_count,
            'embedding_coverage': f"{(total_embeddings / total_docs * 100) if total_docs > 0 else 0:.2f}%"
        }
