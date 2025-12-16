"""
임베딩 서비스
- Google Gemini Embedding API를 사용하여 텍스트를 벡터로 변환
"""
import os
import logging
from typing import List, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)


class EmbeddingService:
    """텍스트 임베딩 서비스"""

    def __init__(self):
        """Gemini API 초기화"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")

        genai.configure(api_key=api_key)
        self.model_name = 'models/embedding-001'
        self.dimension = 768  # Gemini embedding-001의 벡터 차원

    def generate_embedding(self, text: str) -> List[float]:
        """
        단일 텍스트에 대한 임베딩 생성

        Args:
            text: 임베딩할 텍스트

        Returns:
            임베딩 벡터 (768차원 리스트)
        """
        try:
            # 텍스트 길이 제한 (Gemini API 제한)
            if len(text) > 10000:
                text = text[:10000]
                logger.warning(f"텍스트가 너무 길어 10000자로 잘랐습니다.")

            # Gemini Embedding API 호출
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"
            )

            embedding = result['embedding']
            logger.debug(f"임베딩 생성 완료: {len(embedding)}차원")

            return embedding

        except Exception as e:
            logger.error(f"임베딩 생성 실패: {str(e)}")
            raise

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        쿼리 텍스트에 대한 임베딩 생성

        Args:
            query: 검색 쿼리 텍스트

        Returns:
            임베딩 벡터 (768차원 리스트)
        """
        try:
            # 쿼리용 임베딩은 task_type을 retrieval_query로 설정
            result = genai.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query"
            )

            embedding = result['embedding']
            logger.debug(f"쿼리 임베딩 생성 완료: {len(embedding)}차원")

            return embedding

        except Exception as e:
            logger.error(f"쿼리 임베딩 생성 실패: {str(e)}")
            raise

    def generate_batch_embeddings(
        self,
        texts: List[str],
        batch_size: int = 100
    ) -> List[List[float]]:
        """
        여러 텍스트에 대한 임베딩을 배치로 생성

        Args:
            texts: 임베딩할 텍스트 리스트
            batch_size: 배치 크기 (기본값: 100)

        Returns:
            임베딩 벡터 리스트
        """
        embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            logger.info(f"배치 처리 중: {i+1}-{min(i+batch_size, len(texts))}/{len(texts)}")

            for text in batch:
                try:
                    embedding = self.generate_embedding(text)
                    embeddings.append(embedding)
                except Exception as e:
                    logger.error(f"텍스트 임베딩 실패: {str(e)}")
                    # 실패한 경우 None 추가
                    embeddings.append(None)

        return embeddings

    def get_dimension(self) -> int:
        """임베딩 벡터의 차원 수 반환"""
        return self.dimension
