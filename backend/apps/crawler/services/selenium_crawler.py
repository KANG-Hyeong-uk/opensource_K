"""
Selenium 기반 웹 크롤러
"""

import time
import logging
from typing import Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.conf import settings

from core.exceptions import CrawlerException
from apps.crawler.utils.validators import URLValidator
from apps.crawler.services.content_extractor import ContentExtractor

logger = logging.getLogger(__name__)


class SeleniumCrawler:
    """
    Selenium 기반 동적 웹 페이지 크롤러
    """

    def __init__(self):
        """크롤러 초기화"""
        self.driver: Optional[webdriver.Chrome] = None
        self.timeout = getattr(settings, 'SELENIUM_TIMEOUT', 30)
        self.headless = getattr(settings, 'SELENIUM_HEADLESS', True)
        self.content_extractor = ContentExtractor()

    def _setup_driver(self) -> webdriver.Chrome:
        """
        Chrome WebDriver 설정

        Returns:
            webdriver.Chrome: 설정된 Chrome 드라이버
        """
        try:
            chrome_options = Options()

            # Headless 모드
            if self.headless:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')

            # 성능 최적화
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-infobars')
            chrome_options.add_argument('--disable-notifications')

            # 이미지 로딩 비활성화 (속도 향상)
            prefs = {
                'profile.managed_default_content_settings.images': 2,
                'profile.default_content_setting_values.notifications': 2,
            }
            chrome_options.add_experimental_option('prefs', prefs)

            # User Agent 설정
            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            )

            # WebDriver 설정
            # Selenium 4의 자동 ChromeDriver 관리 사용
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(self.timeout)

            return driver

        except Exception as e:
            logger.error(f"Failed to setup Chrome driver: {str(e)}")
            raise CrawlerException(f"Failed to initialize crawler: {str(e)}")

    def crawl(self, url: str) -> Dict[str, any]:
        """
        URL 크롤링

        Args:
            url: 크롤링할 URL

        Returns:
            Dict: 크롤링 결과
                - url: 크롤링한 URL
                - title: 페이지 제목
                - content: 본문 콘텐츠
                - description: 메타 설명
                - html: 전체 HTML
                - status: 크롤링 상태
        """
        # URL 검증 및 정규화
        url = URLValidator.normalize_url(url)
        URLValidator.validate_url(url)

        try:
            # WebDriver 설정
            self.driver = self._setup_driver()

            logger.info(f"Starting to crawl URL: {url}")

            # 페이지 로드
            self.driver.get(url)

            # JavaScript 렌더링 대기
            time.sleep(2)  # 기본 대기

            # 페이지가 완전히 로드될 때까지 대기
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # 추가 대기 (동적 콘텐츠 로딩)
            self._wait_for_dynamic_content()

            # HTML 가져오기
            html = self.driver.page_source

            # 콘텐츠 추출
            extracted_content = self.content_extractor.extract(html)

            logger.info(f"Successfully crawled URL: {url}")

            return {
                'url': url,
                'title': extracted_content['title'],
                'content': extracted_content['content'],
                'description': extracted_content['description'],
                'html': html[:50000],  # HTML은 50KB로 제한
                'status': 'success'
            }

        except Exception as e:
            logger.error(f"Failed to crawl URL {url}: {str(e)}")
            raise CrawlerException(f"Failed to crawl URL: {str(e)}")

        finally:
            # WebDriver 종료
            if self.driver:
                self.driver.quit()
                self.driver = None

    def _wait_for_dynamic_content(self, max_wait: int = 5) -> None:
        """
        동적 콘텐츠 로딩 대기

        Args:
            max_wait: 최대 대기 시간 (초)
        """
        try:
            # 일반적인 로딩 인디케이터가 사라질 때까지 대기
            loading_selectors = [
                '.loading',
                '.loader',
                '#loading',
                '[class*="spinner"]',
                '[class*="loading"]'
            ]

            for selector in loading_selectors:
                try:
                    WebDriverWait(self.driver, max_wait).until_not(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                except:
                    continue

        except Exception as e:
            # 로딩 인디케이터가 없을 수도 있으므로 에러 무시
            pass

    def crawl_batch(self, urls: list) -> list:
        """
        여러 URL을 배치로 크롤링

        Args:
            urls: 크롤링할 URL 리스트

        Returns:
            list: 크롤링 결과 리스트
        """
        results = []

        for url in urls:
            try:
                result = self.crawl(url)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to crawl {url} in batch: {str(e)}")
                results.append({
                    'url': url,
                    'status': 'failed',
                    'error': str(e)
                })

        return results

    def __del__(self):
        """소멸자: WebDriver 종료"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
