"""
Detection 앱 Views
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from apps.detection.services.analysis_service import URLAnalysisService
from apps.detection.serializers import (
    AnalysisRequestSerializer,
    AnalysisResultSerializer,
    AnalysisResultListSerializer,
    AnalysisStatisticsSerializer
)
from core.exceptions import CrawlerException, LLMException

import logging

logger = logging.getLogger(__name__)


class URLAnalysisView(APIView):
    """
    URL 분석 API
    POST: URL 분석 요청
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        URL 분석 요청

        Body:
            - url: 분석할 URL (required)

        Returns:
            - 분석 결과
        """
        # 요청 데이터 검증
        serializer = AnalysisRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'error': True,
                    'message': 'Invalid request data',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        url = serializer.validated_data['url']

        try:
            # URL 분석 실행
            analysis_service = URLAnalysisService()
            result = analysis_service.analyze_url(url, user=request.user)

            # 결과 반환
            result_serializer = AnalysisResultSerializer(result)

            return Response(
                {
                    'success': True,
                    'message': 'Analysis completed successfully',
                    'data': result_serializer.data
                },
                status=status.HTTP_200_OK
            )

        except CrawlerException as e:
            logger.error(f"Crawling failed: {str(e)}")
            return Response(
                {
                    'error': True,
                    'message': 'Failed to crawl URL',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except LLMException as e:
            logger.error(f"LLM analysis failed: {str(e)}")
            return Response(
                {
                    'error': True,
                    'message': 'Failed to analyze content',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response(
                {
                    'error': True,
                    'message': 'Internal server error',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AnalysisHistoryView(APIView):
    """
    분석 이력 조회 API
    GET: 사용자의 분석 이력
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        사용자 분석 이력 조회

        Query Parameters:
            - limit: 조회 개수 (default: 20)

        Returns:
            - 분석 이력 리스트
        """
        limit = int(request.query_params.get('limit', 20))
        limit = min(limit, 100)  # 최대 100개로 제한

        analysis_service = URLAnalysisService()
        results = analysis_service.get_user_history(request.user, limit=limit)

        serializer = AnalysisResultListSerializer(results, many=True)

        return Response(
            {
                'success': True,
                'count': len(results),
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class AnalysisDetailView(APIView):
    """
    분석 결과 상세 조회 API
    GET: 특정 분석 결과 상세
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, analysis_id):
        """
        분석 결과 상세 조회

        Path Parameters:
            - analysis_id: 분석 결과 ID

        Returns:
            - 분석 결과 상세
        """
        analysis_service = URLAnalysisService()
        result = analysis_service.get_analysis_by_id(analysis_id)

        if not result:
            return Response(
                {
                    'error': True,
                    'message': 'Analysis result not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # 권한 체크: 본인 또는 관리자만 조회 가능
        if result.user != request.user and not request.user.is_staff:
            return Response(
                {
                    'error': True,
                    'message': 'Permission denied'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AnalysisResultSerializer(result)

        return Response(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class AnalysisStatisticsView(APIView):
    """
    분석 통계 API
    GET: 사용자의 분석 통계
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        사용자 분석 통계

        Returns:
            - 통계 정보
        """
        analysis_service = URLAnalysisService()
        stats = analysis_service.get_statistics(user=request.user)

        serializer = AnalysisStatisticsSerializer(stats)

        return Response(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
