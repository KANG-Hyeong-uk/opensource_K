"""
API Key 인증
"""

from rest_framework import authentication
from rest_framework import exceptions


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    API Key 기반 인증
    헤더: X-API-Key: your-api-key
    """

    def authenticate(self, request):
        """
        API Key 인증

        Args:
            request: HTTP 요청

        Returns:
            tuple: (user, token) 또는 None
        """
        api_key = request.META.get('HTTP_X_API_KEY')

        if not api_key:
            # API Key가 없으면 인증 시도하지 않음 (다른 인증 방식 사용)
            return None

        # TODO: 실제 API Key 검증 로직 구현
        # 현재는 간단하게 패스 (JWT 인증이 주 인증 방식)
        return None

    def authenticate_header(self, request):
        """
        401 응답 시 WWW-Authenticate 헤더 값
        """
        return 'X-API-Key'
