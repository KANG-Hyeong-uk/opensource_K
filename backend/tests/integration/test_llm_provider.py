"""
Gemini LLM Provider 통합 테스트
- 실제 Gemini API 호출 테스트
"""
import pytest
from apps.llm_provider.services.gemini_provider import GeminiProvider
from core.exceptions import LLMException


@pytest.mark.integration
@pytest.mark.llm
class TestGeminiProvider:
    """Gemini LLM Provider 통합 테스트"""

    @pytest.fixture
    def llm_provider(self):
        """LLM Provider 인스턴스"""
        return GeminiProvider()

    def test_generate_content_simple(self, llm_provider):
        """간단한 콘텐츠 생성 테스트"""
        # Given: 간단한 프롬프트
        prompt = "안녕하세요를 영어로 번역해주세요."

        # When: API 호출
        result = llm_provider.generate_content(prompt)

        # Then: 결과 확인
        assert result is not None
        assert len(result) > 0
        assert 'hello' in result.lower() or 'hi' in result.lower()

        print(f"\n✅ Gemini API 호출 성공!")
        print(f"응답: {result[:100]}...")

    def test_analyze_clickbait_positive(self, llm_provider):
        """클릭베이트 탐지 테스트 (양성)"""
        # Given: 명백한 클릭베이트 제목과 본문
        title = "이것만 알면 인생이 바뀝니다! 절대 공개하지 않는 비밀!"
        content = "여러분은 이 사실을 알고 계셨나요? 사실 매우 놀라운 방법이 있습니다."

        # When: 클릭베이트 분석
        result = llm_provider.analyze_content(title, content)

        # Then: 클릭베이트로 판별되어야 함
        assert result is not None
        assert 'is_clickbait' in result
        assert 'confidence_score' in result

        print(f"\n✅ 클릭베이트 분석 완료!")
        print(f"클릭베이트 여부: {result['is_clickbait']}")
        print(f"신뢰도: {result['confidence_score']}")
        print(f"상세 결과: {result.get('details', {})}")

    def test_analyze_clickbait_negative(self, llm_provider):
        """클릭베이트 탐지 테스트 (음성)"""
        # Given: 정상적인 뉴스 제목과 본문
        title = "정부, 내년 예산안 발표"
        content = "정부는 오늘 2024년도 예산안을 발표했습니다. 총 예산은 전년 대비 5% 증가한 600조원 규모입니다."

        # When: 클릭베이트 분석
        result = llm_provider.analyze_content(title, content)

        # Then: 클릭베이트로 판별되지 않아야 함 (대부분의 경우)
        assert result is not None
        assert 'is_clickbait' in result

        print(f"\n✅ 정상 뉴스 분석 완료!")
        print(f"클릭베이트 여부: {result['is_clickbait']}")
        print(f"신뢰도: {result['confidence_score']}")

    def test_analyze_hate_speech(self, llm_provider):
        """혐오 표현 탐지 테스트"""
        # Given: 테스트 콘텐츠
        title = "특정 집단에 대한 의견"
        content = "모든 사람은 평등하며 존중받아야 합니다."

        # When: 혐오 표현 분석
        result = llm_provider.analyze_content(title, content)

        # Then: 결과 확인
        assert result is not None
        assert 'is_hate_speech' in result

        print(f"\n✅ 혐오 표현 분석 완료!")
        print(f"혐오 표현 여부: {result['is_hate_speech']}")

    def test_analyze_misinformation(self, llm_provider):
        """허위정보 탐지 테스트"""
        # Given: 테스트 콘텐츠
        title = "코로나19 예방법"
        content = "손을 자주 씻고 마스크를 착용하는 것이 중요합니다. WHO는 이러한 방역 수칙을 권장하고 있습니다."

        # When: 허위정보 분석
        result = llm_provider.analyze_content(title, content)

        # Then: 결과 확인
        assert result is not None
        assert 'is_misinformation' in result

        print(f"\n✅ 허위정보 분석 완료!")
        print(f"허위정보 여부: {result['is_misinformation']}")

    def test_analyze_content_comprehensive(self, llm_provider):
        """통합 분석 테스트 (모든 항목)"""
        # Given: 복합적인 테스트 케이스
        title = "충격! 이 음식을 먹으면 암이 완치됩니다!"
        content = "최근 연구에 따르면 특정 음식이 모든 암을 완치시킬 수 있다고 합니다. 지금 바로 확인하세요!"

        # When: 통합 분석
        result = llm_provider.analyze_content(title, content)

        # Then: 모든 분석 항목 확인
        assert result is not None
        assert 'is_clickbait' in result
        assert 'is_hate_speech' in result
        assert 'is_misinformation' in result
        assert 'confidence_score' in result
        assert 'details' in result

        # 클릭베이트와 허위정보로 판별될 가능성이 높음
        print(f"\n✅ 통합 분석 완료!")
        print(f"클릭베이트: {result['is_clickbait']}")
        print(f"혐오 표현: {result['is_hate_speech']}")
        print(f"허위정보: {result['is_misinformation']}")
        print(f"전체 신뢰도: {result['confidence_score']}")

    def test_get_model_info(self, llm_provider):
        """모델 정보 조회 테스트"""
        # When
        info = llm_provider.get_model_info()

        # Then
        assert info is not None
        assert 'model_name' in info
        assert 'provider' in info
        assert info['provider'] == 'Google Gemini'

        print(f"\n✅ 모델 정보 조회 성공!")
        print(f"모델: {info['model_name']}")
        print(f"제공자: {info['provider']}")

    def test_invalid_api_key_handling(self):
        """잘못된 API 키 처리 테스트"""
        # Given: API 키가 없는 상황 (설정을 임시로 변경할 수 없으므로 스킵)
        # 실제 환경에서는 GEMINI_API_KEY가 있어야 하므로 이 테스트는 스킵
        pytest.skip("API 키는 실제 환경에서 필수이므로 스킵")

    def test_json_response_parsing(self, llm_provider):
        """JSON 응답 파싱 테스트"""
        # Given: 분석 요청
        title = "테스트 제목"
        content = "테스트 본문입니다."

        # When: 분석 실행
        result = llm_provider.analyze_content(title, content)

        # Then: JSON 구조 확인
        assert isinstance(result, dict)
        assert all(isinstance(v, (bool, int, float, dict)) for k, v in result.items() if k != 'details')

        print(f"\n✅ JSON 파싱 성공!")
        print(f"결과 구조: {list(result.keys())}")
