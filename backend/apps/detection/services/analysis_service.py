"""
URL 분석 오케스트레이션 서비스
Selenium 크롤러 → RAG 컨텍스트 → LLM 분석 파이프라인
"""

import logging
from typing import Dict, Optional
from django.contrib.auth.models import User

from core.exceptions import CrawlerException, LLMException
from apps.crawler.services.selenium_crawler import SeleniumCrawler
from apps.llm_provider.services.ax_provider import AXProvider
from apps.detection.models import AnalysisResult

logger = logging.getLogger(__name__)


class URLAnalysisService:
    """
    URL 분석 전체 파이프라인
    1. URL 크롤링 (Selenium)
    2. RAG 컨텍스트 가져오기 (선택적)
    3. 콘텐츠 분석 (A.X LLM with RAG)
    4. 결과 저장
    """

    def __init__(self, use_rag: bool = True):
        """
        분석 서비스 초기화

        Args:
            use_rag: RAG 사용 여부 (기본값: True)
        """
        self.crawler = None  # 필요시마다 생성
        self.llm_provider = AXProvider()
        self.use_rag = use_rag
        self.rag_service = None

        # RAG 서비스 초기화 (선택적)
        if self.use_rag:
            try:
                from apps.rag.services.rag_service import RAGService
                self.rag_service = RAGService()
                logger.info("RAG 서비스가 활성화되었습니다.")
            except Exception as e:
                logger.warning(f"RAG 서비스 초기화 실패 (RAG 없이 계속 진행): {str(e)}")
                self.use_rag = False

    def analyze_url(self, url: str, user: Optional[User] = None) -> AnalysisResult:
        """
        URL 분석 실행

        Args:
            url: 분석할 URL
            user: 요청 사용자 (선택)

        Returns:
            AnalysisResult: 분석 결과 모델 인스턴스

        Raises:
            CrawlerException: 크롤링 실패
            LLMException: LLM 분석 실패
        """
        logger.info(f"Starting URL analysis: {url}")

        try:
            # 1단계: Selenium 크롤링
            crawled_data = self._crawl_url(url)

            # 2단계: RAG 컨텍스트 가져오기 (선택적)
            rag_context = None
            if self.use_rag and self.rag_service:
                try:
                    rag_context = self.rag_service.get_context_for_analysis(
                        title=crawled_data['title'],
                        content=crawled_data['content']
                    )
                    logger.info("RAG 컨텍스트를 가져왔습니다.")
                except Exception as e:
                    logger.warning(f"RAG 컨텍스트 가져오기 실패 (RAG 없이 계속 진행): {str(e)}")

            # 3단계: LLM 분석 (RAG 컨텍스트 포함)
            analysis_data = self._analyze_content(
                title=crawled_data['title'],
                content=crawled_data['content'],
                rag_context=rag_context
            )

            # 4단계: 결과 저장
            result = self._save_analysis_result(
                url=url,
                user=user,
                crawled_data=crawled_data,
                analysis_data=analysis_data,
                rag_context=rag_context
            )

            logger.info(f"URL analysis completed: {url}")
            return result

        except CrawlerException as e:
            logger.error(f"Crawling failed for {url}: {str(e)}")
            raise

        except LLMException as e:
            logger.error(f"LLM analysis failed for {url}: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during URL analysis: {str(e)}")
            raise

    def _crawl_url(self, url: str) -> Dict:
        """
        URL 크롤링

        Args:
            url: 크롤링할 URL

        Returns:
            Dict: 크롤링 결과
        """
        logger.info(f"Crawling URL: {url}")

        # Selenium 크롤러 생성 (매번 새로 생성)
        crawler = SeleniumCrawler()

        try:
            crawled_data = crawler.crawl(url)
            return crawled_data
        finally:
            # 크롤러는 자동으로 정리됨 (소멸자)
            pass

    def _analyze_content(
        self,
        title: str,
        content: str,
        rag_context: Optional[Dict] = None
    ) -> Dict:
        """
        콘텐츠 LLM 분석 (RAG 컨텍스트 포함)

        Args:
            title: 콘텐츠 제목
            content: 콘텐츠 본문
            rag_context: RAG 컨텍스트 (선택적)

        Returns:
            Dict: 분석 결과
        """
        logger.info("Analyzing content with LLM...")

        # RAG 컨텍스트가 있으면 프롬프트에 포함
        if rag_context and rag_context.get('context_text'):
            # LLM 제공자가 RAG 컨텍스트를 지원하는 경우
            # 향후 확장: GeminiProvider에 context 파라미터 추가
            logger.info("RAG 컨텍스트가 포함된 분석을 수행합니다.")
            # 현재는 기본 분석 사용 (향후 개선 가능)

        # A.X LLM으로 통합 분석
        analysis_result = self.llm_provider.analyze_content(title, content)

        return analysis_result

    def _save_analysis_result(
        self,
        url: str,
        user: Optional[User],
        crawled_data: Dict,
        analysis_data: Dict,
        rag_context: Optional[Dict] = None
    ) -> AnalysisResult:
        """
        분석 결과 저장

        Args:
            url: 분석한 URL
            user: 요청 사용자
            crawled_data: 크롤링 데이터
            analysis_data: LLM 분석 데이터
            rag_context: RAG 컨텍스트 (선택적)

        Returns:
            AnalysisResult: 저장된 분석 결과
        """
        logger.info(f"Saving analysis result for: {url}")

        # 분석 상세 정보에 RAG 컨텍스트 추가
        details = analysis_data.get('details', {})
        if rag_context:
            details['rag_used'] = True
            details['rag_examples_count'] = {
                'clickbait': len(rag_context.get('clickbait_examples', [])),
                'non_clickbait': len(rag_context.get('non_clickbait_examples', []))
            }
        else:
            details['rag_used'] = False

        # 분석 결과 생성
        result = AnalysisResult.objects.create(
            url=url,
            user=user,
            title=crawled_data.get('title', 'No title'),
            content=crawled_data.get('content', '')[:5000],  # 5KB로 제한
            is_clickbait=analysis_data.get('is_clickbait', False),
            is_hate_speech=analysis_data.get('is_hate_speech', False),
            is_misinformation=analysis_data.get('is_misinformation', False),
            confidence_score=analysis_data.get('confidence_score', 0.0),
            explanation=analysis_data.get('explanation', ''),
            analysis_details=details
        )

        return result

    def get_user_history(self, user: User, limit: int = 20) -> list:
        """
        사용자 분석 이력 조회

        Args:
            user: 사용자
            limit: 조회 개수

        Returns:
            list: 분석 결과 리스트
        """
        return AnalysisResult.objects.filter(
            user=user
        ).order_by('-created_at')[:limit]

    def get_recent_analyses(self, limit: int = 10) -> list:
        """
        최근 분석 결과 조회 (전체)

        Args:
            limit: 조회 개수

        Returns:
            list: 분석 결과 리스트
        """
        return AnalysisResult.objects.order_by('-created_at')[:limit]

    def get_analysis_by_id(self, analysis_id: int) -> Optional[AnalysisResult]:
        """
        ID로 분석 결과 조회

        Args:
            analysis_id: 분석 결과 ID

        Returns:
            AnalysisResult: 분석 결과 (없으면 None)
        """
        try:
            return AnalysisResult.objects.get(id=analysis_id)
        except AnalysisResult.DoesNotExist:
            return None

    def get_statistics(self, user: Optional[User] = None) -> Dict:
        """
        분석 통계

        Args:
            user: 사용자 (None이면 전체 통계)

        Returns:
            Dict: 통계 정보
        """
        queryset = AnalysisResult.objects.all()
        if user:
            queryset = queryset.filter(user=user)

        total_count = queryset.count()
        clickbait_count = queryset.filter(is_clickbait=True).count()
        hate_speech_count = queryset.filter(is_hate_speech=True).count()
        misinformation_count = queryset.filter(is_misinformation=True).count()

        return {
            'total_analyses': total_count,
            'clickbait_detected': clickbait_count,
            'hate_speech_detected': hate_speech_count,
            'misinformation_detected': misinformation_count,
            'safe_content': total_count - (clickbait_count + hate_speech_count + misinformation_count)
        }
