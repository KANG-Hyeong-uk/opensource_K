"""
RAG (Retrieval-Augmented Generation) 서비스
- 유사 문서 검색을 통해 LLM 분석 강화
"""
import logging
from typing import List, Dict, Optional

from apps.rag.services.similarity_service import SimilarityService

logger = logging.getLogger(__name__)


class RAGService:
    """RAG 통합 서비스"""

    def __init__(self):
        self.similarity_service = SimilarityService()

    def get_context_for_analysis(
        self,
        title: str,
        content: str,
        top_k: int = 3
    ) -> Dict:
        """
        분석을 위한 컨텍스트 가져오기

        Args:
            title: 분석할 기사 제목
            content: 분석할 기사 본문
            top_k: 가져올 유사 예시 수

        Returns:
            {
                'clickbait_examples': [...],  # 클릭베이트 예시
                'non_clickbait_examples': [...],  # 비클릭베이트 예시
                'context_text': str  # 프롬프트에 포함할 텍스트
            }
        """
        try:
            # 검색 쿼리 생성
            query = f"{title}\n\n{content[:500]}"  # 제목 + 본문 일부

            # 클릭베이트 예시 검색
            logger.info("클릭베이트 예시 검색 중...")
            clickbait_examples = self.similarity_service.search_similar_documents(
                query_text=query,
                top_k=top_k,
                is_clickbait=True,
                use_cache=True
            )

            # 비클릭베이트 예시 검색
            logger.info("비클릭베이트 예시 검색 중...")
            non_clickbait_examples = self.similarity_service.search_similar_documents(
                query_text=query,
                top_k=top_k,
                is_clickbait=False,
                use_cache=True
            )

            # 프롬프트용 텍스트 생성
            context_text = self._format_context_text(
                clickbait_examples,
                non_clickbait_examples
            )

            return {
                'clickbait_examples': clickbait_examples,
                'non_clickbait_examples': non_clickbait_examples,
                'context_text': context_text
            }

        except Exception as e:
            logger.error(f"RAG 컨텍스트 생성 실패: {str(e)}")
            # 실패해도 빈 컨텍스트 반환
            return {
                'clickbait_examples': [],
                'non_clickbait_examples': [],
                'context_text': ''
            }

    def _format_context_text(
        self,
        clickbait_examples: List[Dict],
        non_clickbait_examples: List[Dict]
    ) -> str:
        """
        유사 예시들을 프롬프트에 포함할 텍스트로 포맷팅

        Args:
            clickbait_examples: 클릭베이트 예시 리스트
            non_clickbait_examples: 비클릭베이트 예시 리스트

        Returns:
            포맷팅된 컨텍스트 텍스트
        """
        context_parts = []

        # 클릭베이트 예시
        if clickbait_examples:
            context_parts.append("## 클릭베이트 예시 (유사한 사례):\n")
            for idx, example in enumerate(clickbait_examples[:3], 1):
                doc = example['document']
                score = example['score']
                context_parts.append(
                    f"{idx}. [{score:.2f}] {doc.title}\n"
                    f"   본문: {doc.content[:200]}...\n"
                )

        # 비클릭베이트 예시
        if non_clickbait_examples:
            context_parts.append("\n## 비클릭베이트 예시 (유사한 사례):\n")
            for idx, example in enumerate(non_clickbait_examples[:3], 1):
                doc = example['document']
                score = example['score']
                context_parts.append(
                    f"{idx}. [{score:.2f}] {doc.title}\n"
                    f"   본문: {doc.content[:200]}...\n"
                )

        return "\n".join(context_parts)

    def enrich_prompt_with_context(
        self,
        base_prompt: str,
        title: str,
        content: str,
        include_examples: bool = True
    ) -> str:
        """
        기본 프롬프트에 RAG 컨텍스트 추가

        Args:
            base_prompt: 기본 프롬프트
            title: 분석할 기사 제목
            content: 분석할 기사 본문
            include_examples: 예시 포함 여부

        Returns:
            강화된 프롬프트
        """
        if not include_examples:
            return base_prompt

        try:
            # RAG 컨텍스트 가져오기
            context = self.get_context_for_analysis(title, content)

            if not context['context_text']:
                logger.warning("RAG 컨텍스트가 비어있습니다.")
                return base_prompt

            # 프롬프트에 컨텍스트 추가
            enriched_prompt = f"""
{base_prompt}

---

참고: 다음은 데이터베이스에서 검색한 유사한 기사 예시입니다. 이를 참고하여 분석하세요.

{context['context_text']}

---

위의 예시들을 참고하되, 분석 대상 기사의 고유한 특성을 반드시 고려하여 판단하세요.
"""

            logger.info("RAG 컨텍스트가 프롬프트에 추가되었습니다.")
            return enriched_prompt

        except Exception as e:
            logger.error(f"프롬프트 강화 실패: {str(e)}")
            # 실패 시 기본 프롬프트 반환
            return base_prompt

    def get_similar_cases(
        self,
        title: str,
        content: str,
        category: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict]:
        """
        유사한 사례 검색 (API 응답용)

        Args:
            title: 제목
            content: 본문
            category: 카테고리 필터 (선택)
            top_k: 결과 수

        Returns:
            유사 사례 리스트
        """
        query = f"{title}\n\n{content[:500]}"

        results = self.similarity_service.search_similar_documents(
            query_text=query,
            top_k=top_k,
            is_clickbait=None,  # 전체 검색
            use_cache=True
        )

        # API 응답 포맷으로 변환
        formatted_results = []
        for result in results:
            doc = result['document']
            formatted_results.append({
                'news_id': doc.news_id,
                'title': doc.title,
                'category': doc.category,
                'is_clickbait': doc.is_clickbait,
                'similarity_score': round(result['score'], 4),
                'content_preview': doc.content[:200]
            })

        return formatted_results
