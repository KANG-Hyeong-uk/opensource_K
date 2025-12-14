"""
텍스트 정제 유틸리티
"""

import re


class TextSanitizer:
    """텍스트 정제"""

    @staticmethod
    def clean_text(text: str) -> str:
        """
        텍스트 정제

        Args:
            text: 원본 텍스트

        Returns:
            str: 정제된 텍스트
        """
        if not text:
            return ""

        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text)

        # 앞뒤 공백 제거
        text = text.strip()

        return text

    @staticmethod
    def remove_html_tags(text: str) -> str:
        """
        HTML 태그 제거

        Args:
            text: HTML이 포함된 텍스트

        Returns:
            str: HTML 태그가 제거된 텍스트
        """
        if not text:
            return ""

        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)

        # HTML 엔티티 디코딩
        import html
        text = html.unescape(text)

        return text

    @staticmethod
    def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
        """
        특수 문자 제거

        Args:
            text: 원본 텍스트
            keep_punctuation: 문장 부호 유지 여부

        Returns:
            str: 특수 문자가 제거된 텍스트
        """
        if not text:
            return ""

        if keep_punctuation:
            # 기본 문장 부호는 유지
            text = re.sub(r'[^\w\s.,!?;:\-\'\"()가-힣]', '', text)
        else:
            # 모든 특수 문자 제거
            text = re.sub(r'[^\w\s가-힣]', '', text)

        return text

    @staticmethod
    def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
        """
        텍스트 길이 제한

        Args:
            text: 원본 텍스트
            max_length: 최대 길이
            suffix: 잘렸을 때 추가할 접미사

        Returns:
            str: 길이가 제한된 텍스트
        """
        if not text or len(text) <= max_length:
            return text

        return text[:max_length - len(suffix)] + suffix

    @staticmethod
    def extract_text_from_html(html: str) -> str:
        """
        HTML에서 텍스트 추출 및 정제

        Args:
            html: HTML 문자열

        Returns:
            str: 정제된 텍스트
        """
        # HTML 태그 제거
        text = TextSanitizer.remove_html_tags(html)

        # 텍스트 정제
        text = TextSanitizer.clean_text(text)

        return text
