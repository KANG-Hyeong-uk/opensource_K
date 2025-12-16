"""
RAG 모델 정의
- NewsDocument: 뉴스 기사 원본 데이터
- DocumentEmbedding: 임베딩 벡터 데이터
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class NewsDocument(models.Model):
    """뉴스 문서 모델"""

    # 메타데이터
    news_id = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='뉴스 ID')
    category = models.CharField(max_length=50, db_index=True, verbose_name='카테고리')
    subcategory = models.CharField(max_length=50, blank=True, verbose_name='하위 카테고리')

    # 콘텐츠
    title = models.CharField(max_length=500, verbose_name='제목')
    subtitle = models.CharField(max_length=500, blank=True, verbose_name='부제목')
    content = models.TextField(verbose_name='본문')

    # 분류 정보
    is_clickbait = models.BooleanField(db_index=True, verbose_name='클릭베이트 여부')
    process_type = models.CharField(
        max_length=10,
        choices=[('A', 'Auto'), ('D', 'Direct')],
        verbose_name='수집 방식'
    )
    process_pattern = models.CharField(max_length=10, verbose_name='처리 패턴')
    process_level = models.CharField(max_length=10, verbose_name='처리 레벨')

    # 문장 정보
    sentence_count = models.IntegerField(verbose_name='문장 수')
    sentences = models.JSONField(default=list, verbose_name='문장 정보')

    # 메타
    part_num = models.CharField(max_length=10, default='P1', verbose_name='파트 번호')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        db_table = 'news_documents'
        verbose_name = '뉴스 문서'
        verbose_name_plural = '뉴스 문서들'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_clickbait']),
            models.Index(fields=['process_type']),
        ]

    def __str__(self):
        return f"{self.news_id}: {self.title[:50]}"

    @property
    def full_text(self):
        """검색용 전체 텍스트"""
        return f"{self.title} {self.subtitle} {self.content}".strip()


class DocumentEmbedding(models.Model):
    """문서 임베딩 벡터 모델"""

    document = models.OneToOneField(
        NewsDocument,
        on_delete=models.CASCADE,
        related_name='embedding',
        verbose_name='문서'
    )

    # 임베딩 벡터 (Gemini embedding-001: 768차원)
    # SQLite에서는 ArrayField를 지원하지 않으므로 JSON으로 저장
    vector = models.JSONField(verbose_name='임베딩 벡터')

    # 임베딩 메타데이터
    model_name = models.CharField(max_length=100, default='models/embedding-001', verbose_name='모델명')
    dimension = models.IntegerField(default=768, verbose_name='차원 수')

    # 메타
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        db_table = 'document_embeddings'
        verbose_name = '문서 임베딩'
        verbose_name_plural = '문서 임베딩들'

    def __str__(self):
        return f"Embedding for {self.document.news_id}"

    def get_vector(self):
        """벡터를 리스트로 반환"""
        if isinstance(self.vector, str):
            return json.loads(self.vector)
        return self.vector

    def set_vector(self, vector_list):
        """벡터 설정"""
        self.vector = vector_list
        self.dimension = len(vector_list)


class SimilarityCache(models.Model):
    """유사도 검색 캐시 (성능 최적화용)"""

    query_text = models.CharField(max_length=500, db_index=True, verbose_name='쿼리 텍스트')
    query_hash = models.CharField(max_length=64, unique=True, db_index=True, verbose_name='쿼리 해시')

    # 검색 결과 (뉴스 ID 리스트와 유사도 점수)
    results = models.JSONField(verbose_name='검색 결과')

    # 메타
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    hit_count = models.IntegerField(default=0, verbose_name='히트 횟수')

    class Meta:
        db_table = 'similarity_cache'
        verbose_name = '유사도 캐시'
        verbose_name_plural = '유사도 캐시들'
        ordering = ['-hit_count']

    def __str__(self):
        return f"Cache: {self.query_text[:50]} (hits: {self.hit_count})"
