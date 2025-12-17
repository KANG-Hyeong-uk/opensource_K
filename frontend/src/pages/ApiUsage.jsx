import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './ApiUsage.css';

const ApiUsage = () => {
    const [apiKey, setApiKey] = useState(null);
    const [showKey, setShowKey] = useState(false);
    const [usageCount, setUsageCount] = useState(0);
    const [copySuccess, setCopySuccess] = useState(false);

    useEffect(() => {
        // Load API key and usage from localStorage
        const savedKey = localStorage.getItem('api_key');
        const savedUsage = localStorage.getItem('api_usage');

        if (savedKey) {
            setApiKey(savedKey);
        }
        if (savedUsage) {
            setUsageCount(parseInt(savedUsage, 10));
        }
    }, []);

    const generateApiKey = () => {
        // Generate random API key
        const key = 'tk_' + Array.from({ length: 32 }, () =>
            Math.random().toString(36).charAt(2)
        ).join('');

        setApiKey(key);
        localStorage.setItem('api_key', key);
        setShowKey(true);
    };

    const regenerateApiKey = () => {
        if (window.confirm('API 키를 재발급하시겠습니까? 기존 키는 더 이상 사용할 수 없습니다.')) {
            generateApiKey();
        }
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(apiKey).then(() => {
            setCopySuccess(true);
            setTimeout(() => setCopySuccess(false), 2000);
        });
    };

    const maskApiKey = (key) => {
        if (!key) return '';
        const visibleStart = key.substring(0, 8);
        const visibleEnd = key.substring(key.length - 4);
        return `${visibleStart}${'•'.repeat(20)}${visibleEnd}`;
    };

    const monthlyLimit = 1000;
    const usagePercentage = (usageCount / monthlyLimit) * 100;

    return (
        <div className="api-usage-page">
            <div className="page-header">
                <h1>API 키 & 사용량</h1>
                <p>API 키를 발급받고 서비스 사용량을 모니터링하세요</p>
            </div>

            {/* API Key Section */}
            <section className="api-key-section">
                <h2>🔑 API 키 관리</h2>

                {!apiKey ? (
                    <div className="api-key-empty">
                        <p>아직 발급된 API 키가 없습니다. 새 API 키를 발급받아 서비스를 시작하세요.</p>
                        <button className="btn btn-primary" onClick={generateApiKey}>
                            API 키 발급하기
                        </button>
                    </div>
                ) : (
                    <div className="api-key-display">
                        <div className="api-key-box">
                            <span className={`api-key-text ${!showKey ? 'api-key-masked' : ''}`}>
                                {showKey ? apiKey : maskApiKey(apiKey)}
                            </span>
                            <button className="icon-btn" onClick={() => setShowKey(!showKey)}>
                                {showKey ? '👁️ 숨기기' : '👁️ 보기'}
                            </button>
                        </div>

                        <div className="api-key-actions">
                            <button
                                className="btn btn-primary"
                                onClick={copyToClipboard}
                            >
                                {copySuccess ? '✓ 복사됨!' : '📋 복사하기'}
                            </button>
                            <button
                                className="btn btn-regenerate"
                                onClick={regenerateApiKey}
                            >
                                🔄 재발급
                            </button>
                        </div>

                        <div className="api-key-info">
                            ⚠️ API 키는 안전하게 보관하세요. 절대 공개 저장소나 클라이언트 코드에 포함하지 마세요.
                        </div>
                    </div>
                )}
            </section>

            {/* Usage Stats Section */}
            <section className="usage-stats-section">
                <div className="stat-card">
                    <div className="stat-label">이번 달 호출</div>
                    <div className="stat-value">{usageCount.toLocaleString()}</div>
                    <div className="stat-subtitle">/ {monthlyLimit.toLocaleString()} 호출</div>
                </div>

                <div className="stat-card">
                    <div className="stat-label">사용률</div>
                    <div className="stat-value">{usagePercentage.toFixed(1)}%</div>
                    <div className="stat-subtitle">매월 1일 초기화</div>
                </div>

                <div className="stat-card">
                    <div className="stat-label">남은 호출</div>
                    <div className="stat-value">{(monthlyLimit - usageCount).toLocaleString()}</div>
                    <div className="stat-subtitle">이번 달 잔여량</div>
                </div>
            </section>

            {/* Docs Link Section */}
            <div className="docs-link-section">
                <h3>개발자 문서를 찾으시나요?</h3>
                <p>API를 연동하여 나만의 서비스를 구축해보세요.</p>
                <Link to="/docs" className="btn btn-primary">
                    API 디자인/사용법 확인하기
                </Link>
            </div>
        </div>
    );
};

export default ApiUsage;
