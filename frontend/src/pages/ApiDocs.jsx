import React, { useState } from 'react';
import './ApiDocs.css';

const ApiDocs = () => {
    const [activeTab, setActiveTab] = useState('overview');

    const sections = {
        overview: {
            title: '개요 (Overview)',
            content: (
                <>
                    <p>
                        URL Analysis API를 통해 애플리케이션에 강력한 웹 콘텐츠 분석 기능을 통합할 수 있습니다.
                        RESTful 구조를 따르며, 유해성 탐지, 오탐 가능성 분석, 키워드 검출 등 다양한 AI 기반 분석 결과를 JSON 형식으로 반환합니다.
                    </p>
                    <div className="info-box">
                        <strong>Base URL</strong>
                        <code className="inline-code">https://api.trainkorea.com/v1</code>
                    </div>
                </>
            ),
            codeRequest: `curl -X GET https://api.trainkorea.com/v1/health`,
            codeResponse: `{
  "status": "ok",
  "version": "1.2.0"
}`
        },
        auth: {
            title: '인증 (Authentication)',
            content: (
                <>
                    <p>
                        모든 API 요청은 <strong>Bearer Token</strong> 인증 방식을 사용합니다.
                        발급받은 API Key를 요청 헤더의 <code>Authorization</code> 필드에 포함해야 합니다.
                    </p>
                    <p>API Key가 유출되지 않도록 주의하십시오. 클라이언트 사이드 코드(HTML/JS)에 키를 직접 노출하는 것은 권장하지 않습니다.</p>
                </>
            ),
            codeRequest: `curl -X GET https://api.trainkorea.com/v1/profile \\
  -H "Authorization: Bearer YOUR_API_KEY"`,
            codeResponse: `{
  "authenticated": true,
  "user": "gildong_hong",
  "quota_remaining": 950
}`
        },
        analyze: {
            title: 'URL 분석 요청 (POST)',
            content: (
                <>
                    <p>특정 URL의 콘텐츠를 비동기적으로 분석을 요청합니다. 요청이 접수되면 <code>job_id</code>가 즉시 반환됩니다.</p>
                    <h3>Headers</h3>
                    <ul>
                        <li><code>Content-Type: application/json</code></li>
                        <li><code>Authorization: Bearer YOUR_KEY</code></li>
                    </ul>
                    <h3>Body Parameters</h3>
                    <table className="param-table">
                        <thead><tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
                        <tbody>
                            <tr><td>url</td><td>string</td><td>Yes</td><td>분석할 대상 웹페이지 URL (http/https)</td></tr>
                            <tr><td>fast_mode</td><td>boolean</td><td>No</td><td>빠른 분석 모드 사용 여부 (기본값: false)</td></tr>
                        </tbody>
                    </table>
                </>
            ),
            codeRequest: `curl -X POST https://api.trainkorea.com/v1/analyze \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "url": "https://example.com/article/123",
    "fast_mode": true
  }'`,
            codeResponse: `{
  "status": "queued",
  "job_id": "job_8f7d9a2b",
  "estimated_time": "3s"
}`
        },
        result: {
            title: '결과 조회 (GET)',
            content: (
                <>
                    <p>분석 작업의 상태 및 최종 결과를 조회합니다. 상태가 <code>completed</code>일 때 상세 레포트가 포함됩니다.</p>
                    <h3>Parameters</h3>
                    <p>URL 경로에 <code>job_id</code>를 포함하여 요청합니다.</p>
                </>
            ),
            codeRequest: `curl -X GET https://api.trainkorea.com/v1/analyze/job_8f7d9a2b \\
  -H "Authorization: Bearer YOUR_API_KEY"`,
            codeResponse: `{
  "status": "completed",
  "result": {
    "safety_score": 98,
    "risk_level": "Safe",
    "categories": ["Technology", "Verfied"],
    "flagged_keywords": []
  },
  "analyzed_at": "2024-12-12T10:00:00Z"
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
                        인증 (Authentication)
                    </li>
                    <li
                        className={activeTab === 'analyze' ? 'active' : ''}
                        onClick={() => setActiveTab('analyze')}
                    >
                        URL 분석 요청
                    </li>
                    <li
                        className={activeTab === 'result' ? 'active' : ''}
                        onClick={() => setActiveTab('result')}
                    >
                        결과 조회
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
