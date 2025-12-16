import React, { useState } from 'react';
import './Analysis.css';

const Analysis = () => {
    const [url, setUrl] = useState('');
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);

    // Mock Data
    const mockResults = [
        { title: '보안 점수', value: 'A+', desc: '최고 수준의 보안 등급입니다.', icon: '🛡️' },
        { title: '응답 속도', value: '120ms', desc: '매우 빠른 응답 속도입니다.', icon: '⚡' },
        { title: 'SEO 최적화', value: '92/100', desc: '검색 엔진 최적화가 잘 되어 있습니다.', icon: '🔍' },
        { title: 'SSL 인증', value: 'Valid', desc: '유효한 인증서를 보유 중입니다.', icon: '🔒' },
        { title: '모바일 호환', value: 'Good', desc: '모바일 기기에서 잘 보입니다.', icon: '📱' },
        { title: '접근성', value: 'Pass', desc: '웹 접근성 표준을 준수합니다.', icon: '♿' },
    ];

    const handleAnalyze = (e) => {
        e.preventDefault();
        if (!url) return;
        setLoading(true);
        // Simulate API call
        setTimeout(() => {
            setResults(mockResults);
            setLoading(false);
            // Increment usage counter in localStorage
            const currentUsage = parseInt(localStorage.getItem('api_usage') || '0', 10);
            localStorage.setItem('api_usage', currentUsage + 1);
        }, 1500);
    };

    return (
        <div className="analysis-page container">
            <div className="analysis-header">
                <h1>URL 분석</h1>
                <p>URL을 입력하고 통합 분석 리포트를 받아보세요.</p>
            </div>

            <form className="analysis-form" onSubmit={handleAnalyze}>
                <input
                    type="url"
                    className="input-field url-input"
                    placeholder="https://example.com"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    required
                />
                <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? '분석 중...' : '분석하기'}
                </button>
            </form>

            {results && (
                <div className="results-grid">
                    {results.map((item, index) => (
                        <div key={index} className="result-card">
                            <div className="result-icon">{item.icon}</div>
                            <h3>{item.title}</h3>
                            <div className="result-value">{item.value}</div>
                            <p>{item.desc}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Analysis;
