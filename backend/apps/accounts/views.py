"""
Accounts 앱 Views
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.accounts.serializers import UserRegisterSerializer, UserProfileSerializer

import logging

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    """
    회원가입 API
    POST: 새 사용자 등록
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        사용자 등록

        Body:
            - username: 사용자명 (required)
            - email: 이메일
            - password: 비밀번호 (required)
            - password_check: 비밀번호 확인 (required)
            - first_name: 이름
            - last_name: 성

        Returns:
            - 생성된 사용자 정보
        """
        serializer = UserRegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'error': True,
                    'message': 'Invalid registration data',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 사용자 생성
        user = serializer.save()

        logger.info(f"New user registered: {user.username}")

        return Response(
            {
                'success': True,
                'message': 'User registered successfully',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            },
            status=status.HTTP_201_CREATED
        )


class ProfileView(APIView):
    """
    사용자 프로필 API
    GET: 프로필 조회
    PUT: 프로필 수정
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        프로필 조회

        Returns:
            - 사용자 프로필
        """
        serializer = UserProfileSerializer(request.user)

        return Response(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def put(self, request):
        """
        프로필 수정

        Body:
            - email: 이메일
            - first_name: 이름
            - last_name: 성

        Returns:
            - 수정된 프로필
        """
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(
                {
                    'error': True,
                    'message': 'Invalid profile data',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            {
                'success': True,
                'message': 'Profile updated successfully',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
