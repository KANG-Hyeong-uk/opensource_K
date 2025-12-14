"""
Custom middleware for URL Analysis Service
"""

import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    요청/응답 로깅 미들웨어
    """

    def process_request(self, request):
        """요청 시작 시간 기록"""
        request.start_time = time.time()

    def process_response(self, request, response):
        """요청 처리 시간 로깅"""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                f"{request.method} {request.path} - "
                f"Status: {response.status_code} - "
                f"Duration: {duration:.2f}s"
            )
        return response

    def process_exception(self, request, exception):
        """예외 발생 시 로깅"""
        logger.error(
            f"Exception in {request.method} {request.path}: {str(exception)}",
            exc_info=True
        )
        return None
