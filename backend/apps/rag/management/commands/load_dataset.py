"""
데이터셋 로딩 관리 명령
Part1 디렉토리의 JSON 파일들을 NewsDocument 모델로 로드
"""
import os
import json
import logging
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from apps.rag.models import NewsDocument

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Part1 데이터셋을 데이터베이스에 로드합니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default='Part1',
            help='데이터셋 디렉토리 경로 (기본값: Part1)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='배치 크기 (기본값: 1000)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='로드할 최대 파일 수 (테스트용)'
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='이미 존재하는 문서는 건너뛰기'
        )

    def handle(self, *args, **options):
        dataset_path = options['path']
        batch_size = options['batch_size']
        limit = options['limit']
        skip_existing = options['skip_existing']

        # 경로 확인
        if not os.path.isabs(dataset_path):
            # 상대 경로인 경우 프로젝트 루트 기준
            base_dir = settings.BASE_DIR.parent if hasattr(settings.BASE_DIR, 'parent') else settings.BASE_DIR
            dataset_path = os.path.join(base_dir, dataset_path)

        if not os.path.exists(dataset_path):
            self.stdout.write(self.style.ERROR(f'경로를 찾을 수 없습니다: {dataset_path}'))
            return

        self.stdout.write(self.style.SUCCESS(f'데이터셋 로딩 시작: {dataset_path}'))

        # JSON 파일 찾기
        json_files = self._find_json_files(dataset_path, limit)
        total_files = len(json_files)

        self.stdout.write(f'총 {total_files}개의 JSON 파일을 찾았습니다.')

        # 로딩 시작
        loaded_count = 0
        skipped_count = 0
        error_count = 0
        batch = []

        for idx, file_path in enumerate(json_files, 1):
            try:
                # JSON 파일 읽기
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                source_data = data.get('sourceDataInfo', {})

                # 뉴스 ID
                news_id = source_data.get('newsID')
                if not news_id:
                    self.stdout.write(self.style.WARNING(f'뉴스 ID가 없습니다: {file_path}'))
                    error_count += 1
                    continue

                # 이미 존재하는지 확인
                if skip_existing and NewsDocument.objects.filter(news_id=news_id).exists():
                    skipped_count += 1
                    continue

                # NewsDocument 객체 생성
                document = NewsDocument(
                    news_id=news_id,
                    category=source_data.get('newsCategory', ''),
                    subcategory=source_data.get('newsSubcategory', ''),
                    title=source_data.get('newsTitle', ''),
                    subtitle=source_data.get('newsSubTitle', ''),
                    content=source_data.get('newsContent', ''),
                    is_clickbait=source_data.get('useType', 0) == 0,  # 0: 클릭베이트, 1: 비클릭베이트
                    process_type=source_data.get('processType', 'A'),
                    process_pattern=source_data.get('processPattern', ''),
                    process_level=source_data.get('processLevel', ''),
                    sentence_count=source_data.get('sentenceCount', 0),
                    sentences=source_data.get('sentenceInfo', []),
                    part_num=source_data.get('partNum', 'P1')
                )

                batch.append(document)

                # 배치 저장
                if len(batch) >= batch_size:
                    with transaction.atomic():
                        NewsDocument.objects.bulk_create(batch, ignore_conflicts=True)
                    loaded_count += len(batch)
                    self.stdout.write(f'진행: {idx}/{total_files} ({loaded_count}개 로드됨)')
                    batch = []

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'파일 처리 실패: {file_path} - {str(e)}'))
                error_count += 1
                continue

        # 남은 배치 저장
        if batch:
            with transaction.atomic():
                NewsDocument.objects.bulk_create(batch, ignore_conflicts=True)
            loaded_count += len(batch)

        # 결과 출력
        self.stdout.write(self.style.SUCCESS('\n=== 로딩 완료 ==='))
        self.stdout.write(f'총 파일 수: {total_files}')
        self.stdout.write(f'로드 성공: {loaded_count}')
        self.stdout.write(f'건너뛴 문서: {skipped_count}')
        self.stdout.write(f'오류: {error_count}')

        # 통계
        total_docs = NewsDocument.objects.count()
        clickbait_count = NewsDocument.objects.filter(is_clickbait=True).count()
        non_clickbait_count = NewsDocument.objects.filter(is_clickbait=False).count()

        self.stdout.write(f'\n현재 DB 상태:')
        self.stdout.write(f'  - 전체 문서: {total_docs}')
        self.stdout.write(f'  - 클릭베이트: {clickbait_count}')
        self.stdout.write(f'  - 비클릭베이트: {non_clickbait_count}')

    def _find_json_files(self, root_path, limit=None):
        """디렉토리에서 모든 JSON 파일 찾기"""
        json_files = []

        for dirpath, dirnames, filenames in os.walk(root_path):
            for filename in filenames:
                if filename.endswith('.json'):
                    json_files.append(os.path.join(dirpath, filename))

                    if limit and len(json_files) >= limit:
                        return json_files

        return json_files
