"""
임베딩 서비스
- Sentence-Transformers 라이브러리를 사용하여 텍스트를 벡터로 변환
- 로컬에서 실행되므로 API 할당량 제한 없음
"""
import logging
from typing import List, Optional
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingService:
    """텍스트 임베딩 서비스 (Sentence-Transformers 사용)"""

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Sentence-Transformers 모델 초기화

        Args:
            model_name: 사용할 모델 이름 (기본값: 'all-MiniLM-L6-v2')
                - all-MiniLM-L6-v2: 384차원, 빠르고 효율적
                - paraphrase-multilingual-MiniLM-L12-v2: 384차원, 다국어 지원
        """
        logger.info(f"임베딩 모델 로딩 중: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.dimension = self.model.get_sentence_embedding_dimension()

    def generate_embedding(self, text: str) -> List[float]:
        """
        단일 텍스트에 대한 임베딩 생성

        Args:
            text: 임베딩할 텍스트

        Returns:
            임베딩 벡터 (384차원 리스트)
        """
        try:
            # 텍스트 길이 제한
            if len(text) > 10000:
                text = text[:10000]
                logger.warning(f"텍스트가 너무 길어 10000자로 잘랐습니다.")

            # Sentence-Transformers 모델로 임베딩 생성
            embedding = self.model.encode(text, convert_to_numpy=True)
            embedding_list = embedding.tolist()

            logger.debug(f"임베딩 생성 완료: {len(embedding_list)}차원")

            return embedding_list

        except Exception as e:
            logger.error(f"임베딩 생성 실패: {str(e)}")
            raise

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        쿼리 텍스트에 대한 임베딩 생성

        Args:
            query: 검색 쿼리 텍스트

        Returns:
            임베딩 벡터 (384차원 리스트)
        """
        try:
            # Sentence-Transformers에서는 문서와 쿼리를 동일하게 처리
            embedding = self.model.encode(query, convert_to_numpy=True)
            embedding_list = embedding.tolist()

            logger.debug(f"쿼리 임베딩 생성 완료: {len(embedding_list)}차원")

            return embedding_list

        except Exception as e:
            logger.error(f"쿼리 임베딩 생성 실패: {str(e)}")
            raise

    def generate_batch_embeddings(
        self,
        texts: List[str],
        batch_size: int = 32
    ) -> List[List[float]]:
        """
        여러 텍스트에 대한 임베딩을 배치로 생성

        Args:
            texts: 임베딩할 텍스트 리스트
            batch_size: 배치 크기 (기본값: 32)

        Returns:
            임베딩 벡터 리스트
        """
        try:
            # 텍스트 길이 제한
            processed_texts = []
            for text in texts:
                if len(text) > 10000:
                    text = text[:10000]
                    logger.warning(f"텍스트가 너무 길어 10000자로 잘랐습니다.")
                processed_texts.append(text)

            logger.info(f"배치 임베딩 생성 시작: {len(processed_texts)}개 텍스트")

            # Sentence-Transformers의 배치 처리 사용
            embeddings_array = self.model.encode(
                processed_texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                show_progress_bar=True
            )

            # numpy array를 리스트로 변환
            embeddings = [emb.tolist() for emb in embeddings_array]

            logger.info(f"배치 임베딩 생성 완료: {len(embeddings)}개")

            return embeddings

        except Exception as e:
            logger.error(f"배치 임베딩 생성 실패: {str(e)}")
            raise

    def get_dimension(self) -> int:
        """임베딩 벡터의 차원 수 반환"""
        return self.dimension
