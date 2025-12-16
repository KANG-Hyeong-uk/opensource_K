"""
임베딩 생성 관리 명령
NewsDocument의 임베딩 벡터를 생성하여 DocumentEmbedding에 저장
"""
import logging
import time
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.rag.models import NewsDocument, DocumentEmbedding
from apps.rag.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'NewsDocument의 임베딩 벡터를 생성합니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=10,
            help='배치 크기 (기본값: 10, Gemini API 제한 고려)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='처리할 최대 문서 수 (테스트용)'
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='이미 임베딩이 있는 문서는 건너뛰기'
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=1.0,
            help='API 호출 간 지연 시간(초) - Rate limit 방지'
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        limit = options['limit']
        skip_existing = options['skip_existing']
        delay = options['delay']

        self.stdout.write(self.style.SUCCESS('임베딩 생성 시작'))

        # 임베딩 서비스 초기화
        try:
            embedding_service = EmbeddingService()
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'임베딩 서비스 초기화 실패: {str(e)}'))
            return

        # 처리할 문서 가져오기
        if skip_existing:
            # 임베딩이 없는 문서만
            queryset = NewsDocument.objects.filter(embedding__isnull=True)
        else:
            queryset = NewsDocument.objects.all()

        if limit:
            queryset = queryset[:limit]

        total_docs = queryset.count()
        self.stdout.write(f'처리할 문서 수: {total_docs}')

        if total_docs == 0:
            self.stdout.write(self.style.WARNING('처리할 문서가 없습니다.'))
            return

        # 임베딩 생성
        success_count = 0
        error_count = 0
        skipped_count = 0
        start_time = time.time()

        for idx, document in enumerate(queryset, 1):
            try:
                # 이미 임베딩이 있는지 확인
                if skip_existing and hasattr(document, 'embedding'):
                    skipped_count += 1
                    continue

                # 텍스트 생성 (제목 + 본문)
                text = document.full_text

                if not text.strip():
                    self.stdout.write(self.style.WARNING(f'빈 텍스트: {document.news_id}'))
                    error_count += 1
                    continue

                # 임베딩 생성
                self.stdout.write(f'[{idx}/{total_docs}] 임베딩 생성 중: {document.news_id}')
                embedding_vector = embedding_service.generate_embedding(text)

                # 임베딩 저장
                with transaction.atomic():
                    DocumentEmbedding.objects.update_or_create(
                        document=document,
                        defaults={
                            'vector': embedding_vector,
                            'model_name': embedding_service.model_name,
                            'dimension': len(embedding_vector)
                        }
                    )

                success_count += 1

                # 진행 상황 출력
                if idx % 10 == 0:
                    elapsed_time = time.time() - start_time
                    avg_time_per_doc = elapsed_time / idx
                    remaining_docs = total_docs - idx
                    estimated_time = avg_time_per_doc * remaining_docs

                    self.stdout.write(
                        f'진행: {idx}/{total_docs} ({success_count}개 성공) | '
                        f'예상 남은 시간: {estimated_time/60:.1f}분'
                    )

                # Rate limit 방지를 위한 지연
                if delay > 0:
                    time.sleep(delay)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'임베딩 생성 실패: {document.news_id} - {str(e)}'))
                error_count += 1
                continue

        # 결과 출력
        total_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS('\n=== 임베딩 생성 완료 ==='))
        self.stdout.write(f'총 처리 문서: {total_docs}')
        self.stdout.write(f'성공: {success_count}')
        self.stdout.write(f'건너뛴 문서: {skipped_count}')
        self.stdout.write(f'오류: {error_count}')
        self.stdout.write(f'소요 시간: {total_time/60:.1f}분')

        # 통계
        total_embeddings = DocumentEmbedding.objects.count()
        total_documents = NewsDocument.objects.count()
        coverage = (total_embeddings / total_documents * 100) if total_documents > 0 else 0

        self.stdout.write(f'\n현재 임베딩 상태:')
        self.stdout.write(f'  - 전체 문서: {total_documents}')
        self.stdout.write(f'  - 임베딩 생성: {total_embeddings}')
        self.stdout.write(f'  - 커버리지: {coverage:.2f}%')
