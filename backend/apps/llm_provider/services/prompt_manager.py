"""
프롬프트 관리자
"""

import os
from pathlib import Path
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class PromptManager:
    """
    프롬프트 템플릿 관리
    """

    def __init__(self):
        """프롬프트 관리자 초기화"""
        self.prompts_dir = Path(__file__).parent.parent / 'prompts'
        self._prompts_cache: Dict[str, str] = {}

    def _load_prompt_file(self, filename: str) -> str:
        """
        프롬프트 파일 로드

        Args:
            filename: 프롬프트 파일명

        Returns:
            str: 프롬프트 템플릿
        """
        if filename in self._prompts_cache:
            return self._prompts_cache[filename]

        file_path = self.prompts_dir / filename

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                prompt = f.read()
                self._prompts_cache[filename] = prompt
                return prompt
        except FileNotFoundError:
            logger.error(f"Prompt file not found: {filename}")
            raise
        except Exception as e:
            logger.error(f"Failed to load prompt file {filename}: {str(e)}")
            raise

    def get_clickbait_prompt(self, title: str, content: str) -> str:
        """
        클릭베이트 탐지 프롬프트 생성

        Args:
            title: 콘텐츠 제목
            content: 콘텐츠 본문

        Returns:
            str: 완성된 프롬프트
        """
        template = self._load_prompt_file('clickbait_detection.txt')

        # 콘텐츠 길이 제한 (토큰 절약)
        content = self._truncate_content(content, max_length=2000)

        return template.format(title=title, content=content)

    def get_hate_speech_prompt(self, title: str, content: str) -> str:
        """
        혐오 표현 탐지 프롬프트 생성

        Args:
            title: 콘텐츠 제목
            content: 콘텐츠 본문

        Returns:
            str: 완성된 프롬프트
        """
        template = self._load_prompt_file('hate_speech_detection.txt')
        content = self._truncate_content(content, max_length=2000)
        return template.format(title=title, content=content)

    def get_misinformation_prompt(self, title: str, content: str) -> str:
        """
        허위정보 탐지 프롬프트 생성

        Args:
            title: 콘텐츠 제목
            content: 콘텐츠 본문

        Returns:
            str: 완성된 프롬프트
        """
        template = self._load_prompt_file('misinformation_detection.txt')
        content = self._truncate_content(content, max_length=2000)
        return template.format(title=title, content=content)

    def _truncate_content(self, content: str, max_length: int = 2000) -> str:
        """
        콘텐츠 길이 제한

        Args:
            content: 원본 콘텐츠
            max_length: 최대 길이

        Returns:
            str: 길이 제한된 콘텐츠
        """
        if len(content) <= max_length:
            return content

        return content[:max_length] + "..."

    def get_combined_analysis_prompt(self, title: str, content: str) -> str:
        """
        통합 분석 프롬프트 (모든 항목을 한 번에 분석)

        Args:
            title: 콘텐츠 제목
            content: 콘텐츠 본문

        Returns:
            str: 통합 분석 프롬프트
        """
        content = self._truncate_content(content, max_length=2000)

        prompt = f"""당신은 웹 콘텐츠 분석 전문가입니다.
다음 콘텐츠를 분석하여 클릭베이트, 혐오 표현, 허위정보 여부를 판단해주세요.

제목: {title}

본문: {content}

다음 세 가지 항목을 모두 분석하고 JSON 형식으로 응답해주세요:

1. 클릭베이트 여부
2. 혐오 표현 포함 여부
3. 허위정보 가능성

응답 형식 (반드시 JSON 형식으로):
{{
  "clickbait": {{
    "is_detected": true/false,
    "confidence": 0.0~1.0,
    "reason": "판단 이유"
  }},
  "hate_speech": {{
    "is_detected": true/false,
    "confidence": 0.0~1.0,
    "reason": "판단 이유"
  }},
  "misinformation": {{
    "is_detected": true/false,
    "confidence": 0.0~1.0,
    "reason": "판단 이유"
  }},
  "overall_risk_score": 0.0~1.0
}}
"""
        return prompt
