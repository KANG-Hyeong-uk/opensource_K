"""
웹 페이지 콘텐츠 추출기
"""

from bs4 import BeautifulSoup
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ContentExtractor:
    """웹 페이지에서 본문 콘텐츠 추출"""

    # 본문일 가능성이 높은 태그와 클래스/ID
    CONTENT_TAGS = ['article', 'main', 'section', 'div']
    CONTENT_INDICATORS = [
        'content', 'article', 'post', 'entry', 'main',
        'body', 'text', 'story', 'description'
    ]

    # 제거할 태그
    REMOVE_TAGS = [
        'script', 'style', 'nav', 'header', 'footer',
        'aside', 'iframe', 'noscript', 'meta', 'link'
    ]

    def extract(self, html: str) -> Dict[str, str]:
        """
        HTML에서 콘텐츠 추출

        Args:
            html: HTML 문자열

        Returns:
            Dict: 추출된 콘텐츠
                - title: 제목
                - content: 본문
                - description: 요약
        """
        soup = BeautifulSoup(html, 'lxml')

        # 불필요한 태그 제거
        self._remove_unwanted_tags(soup)

        # 제목 추출
        title = self._extract_title(soup)

        # 본문 추출
        content = self._extract_main_content(soup)

        # 메타 설명 추출
        description = self._extract_meta_description(soup)

        return {
            'title': title,
            'content': content,
            'description': description
        }

    def _remove_unwanted_tags(self, soup: BeautifulSoup) -> None:
        """불필요한 태그 제거"""
        for tag_name in self.REMOVE_TAGS:
            for tag in soup.find_all(tag_name):
                tag.decompose()

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """제목 추출"""
        # 1. <title> 태그
        if soup.title:
            return soup.title.string.strip()

        # 2. <h1> 태그
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()

        # 3. og:title 메타 태그
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()

        return "No title found"

    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """메타 설명 추출"""
        # 1. description 메타 태그
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()

        # 2. og:description 메타 태그
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc['content'].strip()

        return ""

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """본문 콘텐츠 추출"""
        # 1. article 태그 시도
        article = soup.find('article')
        if article:
            return self._clean_text(article.get_text())

        # 2. main 태그 시도
        main = soup.find('main')
        if main:
            return self._clean_text(main.get_text())

        # 3. 클래스/ID로 본문 찾기
        content_div = self._find_content_by_indicators(soup)
        if content_div:
            return self._clean_text(content_div.get_text())

        # 4. 가장 긴 텍스트 블록 찾기
        longest_text = self._find_longest_text_block(soup)
        return longest_text

    def _find_content_by_indicators(self, soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        """클래스명/ID로 본문 요소 찾기"""
        for tag in self.CONTENT_TAGS:
            for indicator in self.CONTENT_INDICATORS:
                # 클래스명으로 찾기
                element = soup.find(tag, class_=lambda x: x and indicator in x.lower())
                if element:
                    return element

                # ID로 찾기
                element = soup.find(tag, id=lambda x: x and indicator in x.lower())
                if element:
                    return element

        return None

    def _find_longest_text_block(self, soup: BeautifulSoup) -> str:
        """가장 긴 텍스트 블록 찾기"""
        max_length = 0
        longest_text = ""

        for tag in soup.find_all(['p', 'div', 'section']):
            text = self._clean_text(tag.get_text())
            if len(text) > max_length:
                max_length = len(text)
                longest_text = text

        return longest_text if longest_text else "No content found"

    def _clean_text(self, text: str) -> str:
        """텍스트 정제"""
        import re

        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text)

        # 앞뒤 공백 제거
        text = text.strip()

        return text
