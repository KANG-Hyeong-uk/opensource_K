import React, { useState } from 'react';
import './ApiDocs.css';

const ApiDocs = () => {
    const [activeTab, setActiveTab] = useState('overview');

    // 실제 배포 시 환경변수로 변경
    const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
    const API_URL = `${BASE_URL}/api/v1`;

    const sections = {
        overview: {
            title: '개요 (Overview)',
            content: (
                <>
                    <p>
                        URL Analysis API를 통해 애플리케이션에 강력한 웹 콘텐츠 분석 기능을 통합할 수 있습니다.
                        RESTful 구조를 따르며, 클릭베이트 탐지, 혐오 발언 분석, 허위정보 검증 등 다양한 AI 기반 분석 결과를 JSON 형식으로 반환합니다.
                    </p>
                    <div className="info-box">
                        <strong>Base URL</strong>
                        <code className="inline-code">{API_URL}</code>
                    </div>
                    <h3>주요 기능</h3>
                    <ul>
                        <li>클릭베이트(낚시성 제목) 탐지</li>
                        <li>혐오 발언 분석</li>
                        <li>허위정보 검증</li>
                        <li>종합 위험도 평가</li>
                        <li>분석 이력 관리</li>
                    </ul>
                </>
            ),
            codeRequest: `# API 사용 전 준비사항
# 1. 회원가입 및 로그인
# 2. API 키 발급 (웹 UI > API 키 & 사용량)
# 3. API 키를 안전하게 보관`,
            codeResponse: `# API 키 형식
api키

# 모든 요청에 다음 헤더 포함 필요
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json`
        },
        auth: {
            title: '인증 (Authentication)',
            content: (
                <>
                    <p>
                        모든 API 요청은 <strong>Bearer Token</strong> 인증 방식을 사용합니다.
                        발급받은 API Key를 요청 헤더의 <code>Authorization</code> 필드에 포함해야 합니다.
                    </p>
                    <h3>API 키 발급 방법</h3>
                    <ol>
                        <li>웹 UI에 로그인</li>
                        <li>"API 키 & 사용량" 메뉴 접속</li>
                        <li>"API 키 발급하기" 버튼 클릭</li>
                        <li>발급된 키를 안전하게 복사 및 보관</li>
                    </ol>
                    <div className="info-box" style={{marginTop: '16px', backgroundColor: '#fff3cd', borderColor: '#ffc107'}}>
                        <strong>⚠️ 보안 주의사항</strong>
                        <ul style={{marginTop: '8px', marginBottom: 0}}>
                            <li>API 키를 공개 저장소(GitHub 등)에 업로드하지 마세요</li>
                            <li>클라이언트 코드에 직접 포함하지 마세요</li>
                            <li>환경변수나 서버 측에서 안전하게 관리하세요</li>
                        </ul>
                    </div>
                </>
            ),
            codeRequest: `curl -X POST ${API_URL}/analyze/ \\
  -H "Authorization: Bearer sk_live_xxxxx..." \\
  -H "Content-Type: application/json" \\
  -d '{"url": "https://example.com"}'`,
            codeResponse: `# 인증 성공
{
  "success": true,
  "message": "Analysis completed successfully",
  "data": { ... }
}

# 인증 실패 (401)
{
  "detail": "Invalid API key"
}`
        },
        analyze: {
            title: '1. URL 분석 요청',
            content: (
                <>
                    <p>
                        <code>POST {API_URL}/analyze/</code>
                    </p>
                    <p>특정 URL의 콘텐츠를 분석하여 클릭베이트, 혐오 발언, 허위정보 여부를 판단합니다.</p>
                    <h3>Headers</h3>
                    <ul>
                        <li><code>Content-Type: application/json</code></li>
                        <li><code>Authorization: Bearer YOUR_API_KEY</code></li>
                    </ul>
                    <h3>Body Parameters</h3>
                    <table className="param-table">
                        <thead><tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
                        <tbody>
                            <tr><td>url</td><td>string</td><td>Yes</td><td>분석할 대상 웹페이지 URL (http/https)</td></tr>
                        </tbody>
                    </table>
                    <h3>Response Fields</h3>
                    <ul>
                        <li><code>is_clickbait</code>: 클릭베이트 여부 (boolean)</li>
                        <li><code>is_hate_speech</code>: 혐오 발언 여부 (boolean)</li>
                        <li><code>is_misinformation</code>: 허위정보 여부 (boolean)</li>
                        <li><code>is_safe</code>: 안전한 콘텐츠 여부 (boolean)</li>
                        <li><code>risk_level</code>: 위험도 (low/medium/high)</li>
                        <li><code>confidence_score</code>: 신뢰도 점수 (0.0-1.0)</li>
                    </ul>
                </>
            ),
            codeRequest: `curl -X POST ${API_URL}/analyze/ \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "url": "https://n.news.naver.com/article/032/0003416041"
  }'`,
            codeResponse: `{
  "success": true,
  "message": "Analysis completed successfully",
  "data": {
    "id": 4,
    "url": "https://n.news.naver.com/article/032/0003416041",
    "title": "뉴스 기사 제목",
    "is_clickbait": true,
    "is_hate_speech": false,
    "is_misinformation": false,
    "is_safe": false,
    "risk_level": "medium",
    "confidence_score": 0.85,
    "analysis_details": {
      "clickbait": {
        "is_detected": true,
        "confidence": 0.85,
        "reason": "분석 근거..."
      }
    },
    "created_at": "2025-12-18T15:59:51+09:00"
  }
}`
        },
        history: {
            title: '2. 분석 이력 조회',
            content: (
                <>
                    <p>
                        <code>GET {API_URL}/history/</code>
                    </p>
                    <p>사용자의 모든 분석 이력을 조회합니다. 페이지네이션을 지원합니다.</p>
                    <h3>Query Parameters</h3>
                    <table className="param-table">
                        <thead><tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
                        <tbody>
                            <tr><td>page</td><td>integer</td><td>No</td><td>페이지 번호 (기본값: 1)</td></tr>
                            <tr><td>page_size</td><td>integer</td><td>No</td><td>페이지당 항목 수 (기본값: 10)</td></tr>
                        </tbody>
                    </table>
                </>
            ),
            codeRequest: `curl -X GET "${API_URL}/history/?page=1&page_size=10" \\
  -H "Authorization: Bearer YOUR_API_KEY"`,
            codeResponse: `{
  "success": true,
  "count": 25,
  "next": "${API_URL}/history/?page=2",
  "previous": null,
  "results": [
    {
      "id": 4,
      "url": "https://example.com/article",
      "title": "기사 제목",
      "is_clickbait": true,
      "is_hate_speech": false,
      "risk_level": "medium",
      "created_at": "2025-12-18T15:59:51+09:00"
    }
  ]
}`
        },
        detail: {
            title: '3. 분석 상세 조회',
            content: (
                <>
                    <p>
                        <code>GET {API_URL}/results/&lt;analysis_id&gt;/</code>
                    </p>
                    <p>특정 분석 결과의 상세 정보를 조회합니다.</p>
                    <h3>Path Parameters</h3>
                    <table className="param-table">
                        <thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead>
                        <tbody>
                            <tr><td>analysis_id</td><td>integer</td><td>분석 결과 ID</td></tr>
                        </tbody>
                    </table>
                </>
            ),
            codeRequest: `curl -X GET ${API_URL}/results/4/ \\
  -H "Authorization: Bearer YOUR_API_KEY"`,
            codeResponse: `{
  "success": true,
  "data": {
    "id": 4,
    "url": "https://example.com",
    "title": "기사 제목",
    "content": "본문 내용...",
    "is_clickbait": true,
    "is_hate_speech": false,
    "is_misinformation": false,
    "is_safe": false,
    "risk_level": "medium",
    "confidence_score": 0.85,
    "analysis_details": {
      "clickbait": {
        "is_detected": true,
        "confidence": 0.85,
        "reason": "상세한 분석 근거..."
      },
      "hate_speech": {
        "is_detected": false,
        "confidence": 0.95,
        "reason": "분석 근거..."
      },
      "misinformation": {
        "is_detected": false,
        "confidence": 0.7,
        "reason": "분석 근거..."
      }
    },
    "created_at": "2025-12-18T15:59:51+09:00"
  }
}`
        },
        statistics: {
            title: '4. 통계 조회',
            content: (
                <>
                    <p>
                        <code>GET {API_URL}/statistics/</code>
                    </p>
                    <p>사용자의 분석 통계를 조회합니다.</p>
                    <h3>Response Fields</h3>
                    <ul>
                        <li><code>total_analyses</code>: 총 분석 수</li>
                        <li><code>clickbait_count</code>: 클릭베이트 탐지 수</li>
                        <li><code>hate_speech_count</code>: 혐오 발언 탐지 수</li>
                        <li><code>misinformation_count</code>: 허위정보 탐지 수</li>
                        <li><code>safe_count</code>: 안전한 콘텐츠 수</li>
                    </ul>
                </>
            ),
            codeRequest: `curl -X GET ${API_URL}/statistics/ \\
  -H "Authorization: Bearer YOUR_API_KEY"`,
            codeResponse: `{
  "success": true,
  "data": {
    "total_analyses": 150,
    "clickbait_count": 45,
    "hate_speech_count": 12,
    "misinformation_count": 8,
    "safe_count": 85,
    "risk_distribution": {
      "low": 85,
      "medium": 45,
      "high": 20
    },
    "recent_activity": [
      {
        "date": "2025-12-18",
        "count": 15
      }
    ]
  }
}`
        },
        usage: {
            title: '5. API 키 사용량 조회',
            content: (
                <>
                    <p>
                        <code>GET {API_URL}/api-keys/&lt;key_id&gt;/usage/</code>
                    </p>
                    <p>API 키의 사용 통계를 조회합니다.</p>
                    <h3>Query Parameters</h3>
                    <table className="param-table">
                        <thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead>
                        <tbody>
                            <tr><td>period</td><td>string</td><td>조회 기간 (7d, 30d, 90d)</td></tr>
                        </tbody>
                    </table>
                </>
            ),
            codeRequest: `curl -X GET "${API_URL}/api-keys/3/usage/?period=30d" \\
  -H "Authorization: Bearer YOUR_API_KEY"`,
            codeResponse: `{
  "success": true,
  "data": {
    "total_requests": 150,
    "requests_today": 15,
    "requests_this_week": 67,
    "requests_this_month": 150,
    "last_used_at": "2025-12-18T15:59:51+09:00",
    "endpoint_stats": {
      "/api/v1/analyze/": 120,
      "/api/v1/history/": 30
    },
    "daily_stats": [
      {
        "date": "2025-12-18",
        "count": 15
      }
    ]
  }
}`
        }
    };

    return (
        <div className="api-docs-page">
            <aside className="docs-nav">
                <h3>API Reference</h3>
                <ul>
                    <li
                        className={activeTab === 'overview' ? 'active' : ''}
                        onClick={() => setActiveTab('overview')}
                    >
                        개요
                    </li>
                    <li
                        className={activeTab === 'auth' ? 'active' : ''}
                        onClick={() => setActiveTab('auth')}
                    >
                        인증
                    </li>
                    <li
                        className={activeTab === 'analyze' ? 'active' : ''}
                        onClick={() => setActiveTab('analyze')}
                    >
                        1. URL 분석 요청
                    </li>
                    <li
                        className={activeTab === 'history' ? 'active' : ''}
                        onClick={() => setActiveTab('history')}
                    >
                        2. 분석 이력 조회
                    </li>
                    <li
                        className={activeTab === 'detail' ? 'active' : ''}
                        onClick={() => setActiveTab('detail')}
                    >
                        3. 분석 상세 조회
                    </li>
                    <li
                        className={activeTab === 'statistics' ? 'active' : ''}
                        onClick={() => setActiveTab('statistics')}
                    >
                        4. 통계 조회
                    </li>
                    <li
                        className={activeTab === 'usage' ? 'active' : ''}
                        onClick={() => setActiveTab('usage')}
                    >
                        5. API 키 사용량
                    </li>
                </ul>
            </aside>

            <div className="docs-main-container">
                <div className="docs-content">
                    <section className="fade-in">
                        <h1>{sections[activeTab].title}</h1>
                        <div className="section-body">
                            {sections[activeTab].content}
                        </div>
                    </section>
                </div>

                <div className="docs-code-column">
                    <div className="code-block top-shadow">
                        <div className="code-header">Request Example</div>
                        <pre>{sections[activeTab].codeRequest}</pre>
                    </div>
                    <div className="code-block">
                        <div className="code-header">Response Example</div>
                        <pre className="json-output">{sections[activeTab].codeResponse}</pre>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ApiDocs;
