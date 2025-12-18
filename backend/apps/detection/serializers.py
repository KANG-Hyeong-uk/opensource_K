"""
Detection 앱 Serializers
"""

from rest_framework import serializers
from apps.detection.models import AnalysisResult, UserFeedback


class AnalysisRequestSerializer(serializers.Serializer):
    """URL 분석 요청"""

    url = serializers.URLField(
        required=True,
        max_length=2048,
        help_text="분석할 URL"
    )


class AnalysisResultSerializer(serializers.ModelSerializer):
    """URL 분석 결과"""

    is_safe = serializers.BooleanField(read_only=True)
    risk_level = serializers.CharField(read_only=True)
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = AnalysisResult
        fields = [
            'id',
            'url',
            'user_email',
            'title',
            'content',
            'is_clickbait',
            'is_hate_speech',
            'is_misinformation',
            'is_safe',
            'confidence_score',
            'risk_level',
            'explanation',
            'analysis_details',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields

    def get_user_email(self, obj):
        """사용자 이메일 반환"""
        return obj.user.email if obj.user else None


class AnalysisResultListSerializer(serializers.ModelSerializer):
    """URL 분석 결과 리스트 (간략)"""

    is_safe = serializers.BooleanField(read_only=True)
    risk_level = serializers.CharField(read_only=True)

    class Meta:
        model = AnalysisResult
        fields = [
            'id',
            'url',
            'title',
            'is_clickbait',
            'is_hate_speech',
            'is_misinformation',
            'is_safe',
            'confidence_score',
            'risk_level',
            'explanation',
            'created_at'
        ]
        read_only_fields = fields


class AnalysisStatisticsSerializer(serializers.Serializer):
    """분석 통계"""

    total_analyses = serializers.IntegerField()
    clickbait_detected = serializers.IntegerField()
    hate_speech_detected = serializers.IntegerField()
    misinformation_detected = serializers.IntegerField()
    safe_content = serializers.IntegerField()


class UserFeedbackSerializer(serializers.ModelSerializer):
    """사용자 피드백"""

    class Meta:
        model = UserFeedback
        fields = ['id', 'url', 'reason', 'analysis_result', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        """피드백 생성"""
        # 현재 요청 사용자 추가
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)
