#!/bin/bash

# 색상 정의
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Django Project Structure Generator${NC}"
echo -e "${BLUE}  (Simplified: SQLite + Selenium + Gemini)${NC}"
echo -e "${BLUE}========================================${NC}\n"

# 프로젝트 루트 확인
if [ ! -f "README.md" ]; then
    echo -e "${YELLOW}Warning: README.md not found. Are you in the project root?${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 디렉토리 생성 함수
create_dir() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        echo -e "${GREEN}✓${NC} Created directory: $1"
    else
        echo -e "${YELLOW}→${NC} Directory already exists: $1"
    fi
}

# 파일 생성 함수
create_file() {
    if [ ! -f "$1" ]; then
        touch "$1"
        echo -e "${GREEN}✓${NC} Created file: $1"
    else
        echo -e "${YELLOW}→${NC} File already exists: $1"
    fi
}

echo -e "\n${BLUE}[1/6] Creating root directories...${NC}"
create_dir "config/settings"
create_dir "apps"
create_dir "core/utils"
create_dir "tests/integration"
create_dir "scripts"
create_dir "static"
create_dir "media"
create_dir "logs"
create_dir "requirements"

echo -e "\n${BLUE}[2/6] Creating Django app: accounts${NC}"
create_dir "apps/accounts/tests"
create_file "apps/accounts/__init__.py"
create_file "apps/accounts/models.py"
create_file "apps/accounts/serializers.py"
create_file "apps/accounts/views.py"
create_file "apps/accounts/urls.py"
create_file "apps/accounts/services.py"
create_file "apps/accounts/tests/__init__.py"

echo -e "\n${BLUE}[3/6] Creating Django app: detection${NC}"
create_dir "apps/detection/services"
create_dir "apps/detection/tests"
create_file "apps/detection/__init__.py"
create_file "apps/detection/models.py"
create_file "apps/detection/serializers.py"
create_file "apps/detection/views.py"
create_file "apps/detection/urls.py"
create_file "apps/detection/services/__init__.py"
create_file "apps/detection/services/analysis_service.py"
create_file "apps/detection/services/content_classifier.py"
create_file "apps/detection/tests/__init__.py"

echo -e "\n${BLUE}[4/6] Creating Django app: crawler (Selenium)${NC}"
create_dir "apps/crawler/services"
create_dir "apps/crawler/utils"
create_dir "apps/crawler/tests"
create_file "apps/crawler/__init__.py"
create_file "apps/crawler/models.py"
create_file "apps/crawler/services/__init__.py"
create_file "apps/crawler/services/selenium_crawler.py"
create_file "apps/crawler/services/content_extractor.py"
create_file "apps/crawler/services/metadata_parser.py"
create_file "apps/crawler/utils/__init__.py"
create_file "apps/crawler/utils/validators.py"
create_file "apps/crawler/utils/sanitizers.py"
create_file "apps/crawler/tests/__init__.py"

echo -e "\n${BLUE}[5/6] Creating Django app: llm_provider (Gemini)${NC}"
create_dir "apps/llm_provider/services"
create_dir "apps/llm_provider/prompts"
create_dir "apps/llm_provider/tests"
create_file "apps/llm_provider/__init__.py"
create_file "apps/llm_provider/models.py"
create_file "apps/llm_provider/services/__init__.py"
create_file "apps/llm_provider/services/gemini_provider.py"
create_file "apps/llm_provider/services/prompt_manager.py"
create_file "apps/llm_provider/prompts/clickbait_detection.txt"
create_file "apps/llm_provider/prompts/hate_speech_detection.txt"
create_file "apps/llm_provider/prompts/misinformation_detection.txt"
create_file "apps/llm_provider/tests/__init__.py"

echo -e "\n${BLUE}[6/6] Creating Django apps: api_keys, analytics${NC}"
# API Keys
create_dir "apps/api_keys/tests"
create_file "apps/api_keys/__init__.py"
create_file "apps/api_keys/models.py"
create_file "apps/api_keys/serializers.py"
create_file "apps/api_keys/views.py"
create_file "apps/api_keys/urls.py"
create_file "apps/api_keys/services.py"
create_file "apps/api_keys/permissions.py"
create_file "apps/api_keys/tests/__init__.py"

# Analytics
create_dir "apps/analytics/tests"
create_file "apps/analytics/__init__.py"
create_file "apps/analytics/models.py"
create_file "apps/analytics/serializers.py"
create_file "apps/analytics/views.py"
create_file "apps/analytics/urls.py"
create_file "apps/analytics/services.py"
create_file "apps/analytics/tests/__init__.py"

echo -e "\n${BLUE}Creating core, config, and other files...${NC}"
# Apps init
create_file "apps/__init__.py"

# Core
create_file "core/__init__.py"
create_file "core/exceptions.py"
create_file "core/responses.py"
create_file "core/pagination.py"
create_file "core/permissions.py"
create_file "core/middleware.py"
create_file "core/utils/__init__.py"
create_file "core/utils/logger.py"
create_file "core/utils/decorators.py"

# Config
create_file "config/__init__.py"
create_file "config/asgi.py"
create_file "config/wsgi.py"
create_file "config/urls.py"
create_file "config/settings/__init__.py"
create_file "config/settings/base.py"
create_file "config/settings/dev.py"
create_file "config/settings/prod.py"

# Tests
create_file "tests/__init__.py"
create_file "tests/conftest.py"
create_file "tests/factories.py"
create_file "tests/integration/__init__.py"
create_file "tests/integration/test_url_analysis_flow.py"

# Scripts
create_file "scripts/deploy.sh"

# Requirements (이미 존재)
create_file "requirements/base.txt"
create_file "requirements/dev.txt"
create_file "requirements/prod.txt"

# Other configs
create_file "pytest.ini"

# Make scripts executable
chmod +x scripts/*.sh 2>/dev/null

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  ✓ Project structure created!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "${BLUE}Tech Stack (Simplified):${NC}"
echo -e "  • Django + DRF"
echo -e "  • SQLite (no PostgreSQL)"
echo -e "  • Selenium (web scraping)"
echo -e "  • Gemini LLM (Google AI)"
echo -e "  • No Redis, No Celery, No S3\n"

echo -e "${BLUE}Next steps:${NC}"
echo -e "1. ${YELLOW}cp .env.example .env.dev${NC}"
echo -e "2. ${YELLOW}python -m venv venv${NC}"
echo -e "3. ${YELLOW}source venv/bin/activate${NC}"
echo -e "4. ${YELLOW}pip install -r requirements/dev.txt${NC}"
echo -e "5. ${YELLOW}python manage.py migrate${NC}"
echo -e "6. ${YELLOW}python manage.py runserver${NC}\n"

echo -e "${GREEN}Ready to code! 🚀${NC}\n"
