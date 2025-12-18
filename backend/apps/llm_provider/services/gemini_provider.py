"""
Google Gemini LLM 제공자
"""

import json
import logging
from typing import Dict, Optional
import google.generativeai as genai
from django.conf import settings

from core.exceptions import LLMException
from apps.llm_provider.services.prompt_manager import PromptManager

logger = logging.getLogger(__name__)


class GeminiProvider:
    """
    Google Gemini API 제공자
    확장 가능하고 유지보수가 용이한 구조
    """

    def __init__(self):
        """Gemini Provider 초기화"""
        # API 키 설정
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            raise LLMException("GEMINI_API_KEY is not configured")

        genai.configure(api_key=api_key)

        # 모델 설정
        model_name = getattr(settings, 'GEMINI_MODEL', 'gemini-flash-latest')
        self.model = genai.GenerativeModel(model_name)

        # 프롬프트 관리자
        self.prompt_manager = PromptManager()

        logger.info(f"Gemini Provider initialized with model: {model_name}")

    async def list_available_models(self) -> list:
        """
        사용 가능한 모델 목록 조회

        Returns:
            list: 모델 이름 리스트
        """
        try:
            models = genai.list_models()
            return [model.name for model in models]
        except Exception as e:
            logger.error(f"Failed to list models: {str(e)}")
            return []

    def generate_content(self, prompt: str) -> str:
        """
        Gemini API로 콘텐츠 생성

        Args:
            prompt: 프롬프트 문자열

        Returns:
            str: 생성된 텍스트

        Raises:
            LLMException: API 호출 실패 시
        """
        try:
            logger.info("Calling Gemini API...")

            # Gemini API 호출
            response = self.model.generate_content(prompt)

            if not response or not response.text:
                raise LLMException("Empty response from Gemini API")

            logger.info("Gemini API call successful")
            return response.text

        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            raise LLMException(f"Failed to generate content: {str(e)}")

    def analyze_content(self, title: str, content: str) -> Dict:
        """
        콘텐츠 통합 분석 (클릭베이트, 혐오 표현, 허위정보)

        Args:
            title: 콘텐츠 제목
            content: 콘텐츠 본문

        Returns:
            Dict: 분석 결과
                - is_clickbait: 클릭베이트 여부
                - is_hate_speech: 혐오 표현 포함 여부
                - is_misinformation: 허위정보 가능성
                - confidence_score: 전체 신뢰도
                - details: 상세 분석 결과
        """
        try:
            # 통합 프롬프트 생성
            prompt = self.prompt_manager.get_combined_analysis_prompt(title, content)

            # Gemini API 호출
            response_text = self.generate_content(prompt)

            # JSON 파싱
            analysis_result = self._parse_json_response(response_text)

            # 결과 정규화
            normalized_result = self._normalize_analysis_result(analysis_result)

            return normalized_result

        except Exception as e:
            logger.error(f"Content analysis failed: {str(e)}")
            raise LLMException(f"Failed to analyze content: {str(e)}")

    def analyze_clickbait(self, title: str, content: str) -> Dict:
        """
        클릭베이트 분석 (개별)

        Args:
            title: 콘텐츠 제목
            content: 콘텐츠 본문

        Returns:
            Dict: 클릭베이트 분석 결과
        """
        prompt = self.prompt_manager.get_clickbait_prompt(title, content)
        response_text = self.generate_content(prompt)
        return self._parse_json_response(response_text)

    def analyze_hate_speech(self, title: str, content: str) -> Dict:
        """
        혐오 표현 분석 (개별)

        Args:
            title: 콘텐츠 제목
            content: 콘텐츠 본문

        Returns:
            Dict: 혐오 표현 분석 결과
        """
        prompt = self.prompt_manager.get_hate_speech_prompt(title, content)
        response_text = self.generate_content(prompt)
        return self._parse_json_response(response_text)

    def analyze_misinformation(self, title: str, content: str) -> Dict:
        """
        허위정보 분석 (개별)

        Args:
            title: 콘텐츠 제목
            content: 콘텐츠 본문

        Returns:
            Dict: 허위정보 분석 결과
        """
        prompt = self.prompt_manager.get_misinformation_prompt(title, content)
        response_text = self.generate_content(prompt)
        return self._parse_json_response(response_text)

    def _parse_json_response(self, response_text: str) -> Dict:
        """
        JSON 응답 파싱

        Args:
            response_text: Gemini API 응답 텍스트

        Returns:
            Dict: 파싱된 JSON 객체

        Raises:
            LLMException: JSON 파싱 실패 시
        """
        try:
            # JSON 코드 블록 추출 (```json ... ``` 형식)
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(1)
            else:
                # JSON 블록이 없으면 전체 텍스트에서 JSON 찾기
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_text = json_match.group(0)
                else:
                    json_text = response_text

            # JSON 파싱
            result = json.loads(json_text)
            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.debug(f"Response text: {response_text}")
            raise LLMException(f"Invalid JSON response from LLM: {str(e)}")

    def _normalize_analysis_result(self, analysis_result: Dict) -> Dict:
        """
        분석 결과 정규화

        Args:
            analysis_result: 원본 분석 결과

        Returns:
            Dict: 정규화된 분석 결과
        """
        try:
            clickbait = analysis_result.get('clickbait', {})
            hate_speech = analysis_result.get('hate_speech', {})
            misinformation = analysis_result.get('misinformation', {})

            # 전체 위험도 계산
            overall_risk = analysis_result.get('overall_risk_score', 0.0)

            if overall_risk == 0.0:
                # overall_risk_score가 없으면 각 항목의 평균으로 계산
                scores = []
                if clickbait.get('is_detected'):
                    scores.append(clickbait.get('confidence', 0.0))
                if hate_speech.get('is_detected'):
                    scores.append(hate_speech.get('confidence', 0.0))
                if misinformation.get('is_detected'):
                    scores.append(misinformation.get('confidence', 0.0))

                overall_risk = sum(scores) / len(scores) if scores else 0.0

            # 전체 판단 근거 추출
            explanation = analysis_result.get('explanation', '')

            # explanation이 없으면 각 항목의 reason을 조합
            if not explanation:
                reasons = []
                if clickbait.get('is_detected'):
                    reasons.append(f"클릭베이트: {clickbait.get('reason', '')}")
                if hate_speech.get('is_detected'):
                    reasons.append(f"혐오표현: {hate_speech.get('reason', '')}")
                if misinformation.get('is_detected'):
                    reasons.append(f"허위정보: {misinformation.get('reason', '')}")

                if reasons:
                    explanation = ', '.join(reasons)
                else:
                    explanation = '안전한 콘텐츠로 판단됨'

            return {
                'is_clickbait': clickbait.get('is_detected', False),
                'is_hate_speech': hate_speech.get('is_detected', False),
                'is_misinformation': misinformation.get('is_detected', False),
                'confidence_score': round(overall_risk, 2),
                'explanation': explanation,
                'details': {
                    'clickbait': clickbait,
                    'hate_speech': hate_speech,
                    'misinformation': misinformation
                }
            }

        except Exception as e:
            logger.error(f"Failed to normalize analysis result: {str(e)}")
            raise LLMException(f"Failed to normalize result: {str(e)}")

    def get_model_info(self) -> Dict:
        """
        현재 사용 중인 모델 정보

        Returns:
            Dict: 모델 정보
        """
        return {
            'model_name': getattr(settings, 'GEMINI_MODEL', 'gemini-flash-latest'),
            'provider': 'Google Gemini',
            'version': '2.5'
        }
