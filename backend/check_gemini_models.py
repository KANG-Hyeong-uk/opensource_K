"""
Gemini 사용 가능한 모델 확인 스크립트
"""
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY가 설정되지 않았습니다.")
    sys.exit(1)

genai.configure(api_key=api_key)

print("🔍 사용 가능한 Gemini 모델 목록:\n")
print("=" * 80)

try:
    models = genai.list_models()
    for model in models:
        print(f"\n📦 모델: {model.name}")
        print(f"   표시 이름: {model.display_name}")
        print(f"   설명: {model.description[:100] if model.description else 'N/A'}...")
        print(f"   지원 메서드: {model.supported_generation_methods}")
except Exception as e:
    print(f"❌ 모델 목록 조회 실패: {str(e)}")
    sys.exit(1)

print("\n" + "=" * 80)
print("\n✅ 모델 목록 조회 완료!")
print("\n💡 사용 방법: genai.GenerativeModel('모델이름')")
