"""
Accounts 앱 Serializers
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    """사용자 회원가입"""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_check = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_check', 'first_name', 'last_name']

    def validate(self, attrs):
        """비밀번호 일치 확인"""
        if attrs['password'] != attrs['password_check']:
            raise serializers.ValidationError({
                'password': 'Passwords do not match'
            })
        return attrs

    def create(self, validated_data):
        """사용자 생성"""
        validated_data.pop('password_check')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """사용자 프로필"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']
