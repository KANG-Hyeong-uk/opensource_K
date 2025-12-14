"""
Custom exceptions and exception handler
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class BaseAPIException(Exception):
    """Base exception for API errors"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = "An error occurred"

    def __init__(self, message=None, status_code=None):
        self.message = message or self.default_message
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)


class CrawlerException(BaseAPIException):
    """크롤러 관련 예외"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = "Crawling failed"


class LLMException(BaseAPIException):
    """LLM API 관련 예외"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = "LLM processing failed"


class ValidationException(BaseAPIException):
    """유효성 검증 예외"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Validation failed"


class AuthenticationException(BaseAPIException):
    """인증 예외"""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = "Authentication failed"


class PermissionException(BaseAPIException):
    """권한 예외"""
    status_code = status.HTTP_403_FORBIDDEN
    default_message = "Permission denied"


def custom_exception_handler(exc, context):
    """
    커스텀 예외 핸들러
    DRF의 기본 예외 핸들러를 확장
    """
    # DRF의 기본 예외 핸들러 먼저 호출
    response = exception_handler(exc, context)

    # 커스텀 예외 처리
    if isinstance(exc, BaseAPIException):
        logger.error(f"Custom exception: {exc.message}", exc_info=True)
        return Response(
            {
                'error': True,
                'message': exc.message,
                'status_code': exc.status_code
            },
            status=exc.status_code
        )

    # DRF에서 처리된 예외
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': response.data.get('detail', 'An error occurred'),
            'status_code': response.status_code
        }
        response.data = custom_response_data
        return response

    # 처리되지 않은 예외 (500 에러)
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return Response(
        {
            'error': True,
            'message': 'Internal server error',
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
