"""
Selenium 크롤러 통합 테스트
- 실제 웹사이트 크롤링 테스트
"""
import pytest
from apps.crawler.services.selenium_crawler import SeleniumCrawler
from core.exceptions import CrawlerException


@pytest.mark.integration
@pytest.mark.crawler
class TestSeleniumCrawler:
    """Selenium 크롤러 통합 테스트"""

    def test_crawl_news_article_success(self):
        """뉴스 기사 크롤링 성공 테스트"""
        # Given: 실제 뉴스 URL
        url = "https://www.naver.com"  # 테스트용 URL
        crawler = SeleniumCrawler()

        # When: 크롤링 실행
        result = crawler.crawl(url)

        # Then: 결과 검증
        assert result is not None
        assert result['status'] == 'success'
        assert result['url'] == url
        assert 'title' in result
        assert 'content' in result
        assert len(result['content']) > 0

        print(f"\n✅ 크롤링 성공!")
        print(f"URL: {result['url']}")
        print(f"제목: {result['title']}")
        print(f"본문 길이: {len(result['content'])} 글자")

    def test_crawl_with_korean_content(self):
        """한글 콘텐츠 크롤링 테스트"""
        # Given: 한글 뉴스 사이트 URL
        url = "https://www.naver.com"
        crawler = SeleniumCrawler()

        # When: 크롤링 실행
        result = crawler.crawl(url)

        # Then: 한글 콘텐츠 확인
        assert result is not None
        assert result['status'] == 'success'
        # 한글이 포함되어 있는지 확인
        has_korean = any('\uac00' <= char <= '\ud7a3' for char in result['title'] + result['content'])
        assert has_korean, "한글 콘텐츠가 없습니다"

        print(f"\n✅ 한글 크롤링 성공!")
        print(f"제목: {result['title'][:50]}...")

    def test_crawl_invalid_url_should_fail(self):
        """잘못된 URL 크롤링 실패 테스트"""
        # Given: 잘못된 URL
        invalid_url = "invalid-url-format"
        crawler = SeleniumCrawler()

        # When & Then: 예외 발생 확인
        with pytest.raises(CrawlerException):
            crawler.crawl(invalid_url)

        print("\n✅ 잘못된 URL 예외 처리 확인!")

    def test_crawl_timeout_handling(self):
        """타임아웃 처리 테스트"""
        # Given: 느린 응답 사이트 (타임아웃 설정을 짧게)
        url = "https://httpstat.us/200?sleep=5000"  # 5초 지연
        crawler = SeleniumCrawler()
        crawler.timeout = 3  # 3초 타임아웃

        # When & Then: 타임아웃 예외 처리
        with pytest.raises(CrawlerException):
            crawler.crawl(url)

        print("\n✅ 타임아웃 처리 확인!")

    def test_crawl_extract_metadata(self):
        """메타데이터 추출 테스트"""
        # Given
        url = "https://www.example.com"
        crawler = SeleniumCrawler()

        # When
        result = crawler.crawl(url)

        # Then: 메타데이터 확인
        assert 'title' in result
        assert 'description' in result
        assert 'html' in result
        assert len(result['html']) > 0

        print(f"\n✅ 메타데이터 추출 성공!")
        print(f"설명: {result['description'][:100] if result['description'] else 'N/A'}...")
