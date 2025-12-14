"""
URL 분석 오케스트레이션 서비스
Selenium 크롤러 → LLM 분석 파이프라인
"""

import logging
from typing import Dict, Optional
from django.contrib.auth.models import User

from core.exceptions import CrawlerException, LLMException
from apps.crawler.services.selenium_crawler import SeleniumCrawler
from apps.llm_provider.services.gemini_provider import GeminiProvider
from apps.detection.models import AnalysisResult

logger = logging.getLogger(__name__)


class URLAnalysisService:
    """
    URL 분석 전체 파이프라인
    1. URL 크롤링 (Selenium)
    2. 콘텐츠 분석 (Gemini LLM)
    3. 결과 저장
    """

    def __init__(self):
        """분석 서비스 초기화"""
        self.crawler = None  # 필요시마다 생성
        self.llm_provider = GeminiProvider()

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

            # 2단계: LLM 분석
            analysis_data = self._analyze_content(
                title=crawled_data['title'],
                content=crawled_data['content']
            )

            # 3단계: 결과 저장
            result = self._save_analysis_result(
                url=url,
                user=user,
                crawled_data=crawled_data,
                analysis_data=analysis_data
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

    def _analyze_content(self, title: str, content: str) -> Dict:
        """
        콘텐츠 LLM 분석

        Args:
            title: 콘텐츠 제목
            content: 콘텐츠 본문

        Returns:
            Dict: 분석 결과
        """
        logger.info("Analyzing content with LLM...")

        # Gemini LLM으로 통합 분석
        analysis_result = self.llm_provider.analyze_content(title, content)

        return analysis_result

    def _save_analysis_result(
        self,
        url: str,
        user: Optional[User],
        crawled_data: Dict,
        analysis_data: Dict
    ) -> AnalysisResult:
        """
        분석 결과 저장

        Args:
            url: 분석한 URL
            user: 요청 사용자
            crawled_data: 크롤링 데이터
            analysis_data: LLM 분석 데이터

        Returns:
            AnalysisResult: 저장된 분석 결과
        """
        logger.info(f"Saving analysis result for: {url}")

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
            analysis_details=analysis_data.get('details', {})
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
