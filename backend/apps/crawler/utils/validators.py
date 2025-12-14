"""
URL 검증 유틸리티
"""

import re
from urllib.parse import urlparse
from core.exceptions import ValidationException


class URLValidator:
    """URL 유효성 검사"""

    # 허용되는 스킴
    ALLOWED_SCHEMES = ['http', 'https']

    # 차단할 확장자 (실행 파일 등)
    BLOCKED_EXTENSIONS = [
        '.exe', '.dmg', '.pkg', '.deb', '.rpm',
        '.zip', '.tar', '.gz', '.rar', '.7z',
        '.apk', '.ipa', '.msi'
    ]

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        URL 유효성 검사

        Args:
            url: 검증할 URL

        Returns:
            bool: 유효한 URL이면 True

        Raises:
            ValidationException: 유효하지 않은 URL
        """
        if not url or not isinstance(url, str):
            raise ValidationException("URL must be a non-empty string")

        # URL 길이 제한
        if len(url) > 2048:
            raise ValidationException("URL is too long (max 2048 characters)")

        # URL 파싱
        try:
            parsed = urlparse(url)
        except Exception:
            raise ValidationException("Invalid URL format")

        # 스킴 검증
        if parsed.scheme not in URLValidator.ALLOWED_SCHEMES:
            raise ValidationException(
                f"Invalid URL scheme. Allowed: {', '.join(URLValidator.ALLOWED_SCHEMES)}"
            )

        # 도메인 검증
        if not parsed.netloc:
            raise ValidationException("URL must have a domain")

        # 차단된 확장자 검증
        url_lower = url.lower()
        for ext in URLValidator.BLOCKED_EXTENSIONS:
            if url_lower.endswith(ext):
                raise ValidationException(f"Blocked file extension: {ext}")

        # 로컬 주소 차단 (선택적)
        blocked_hosts = ['localhost', '127.0.0.1', '0.0.0.0']
        if parsed.netloc.split(':')[0] in blocked_hosts:
            raise ValidationException("Local addresses are not allowed")

        return True

    @staticmethod
    def normalize_url(url: str) -> str:
        """
        URL 정규화

        Args:
            url: 정규화할 URL

        Returns:
            str: 정규화된 URL
        """
        # 앞뒤 공백 제거
        url = url.strip()

        # http:// 또는 https://가 없으면 https:// 추가
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        return url
