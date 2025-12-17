import React, { useState } from 'react';
import './Home.css';

const Home = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);

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
        <div className="home-page">
            {/* Hero Section */}
            <section className="hero">
                <div className="container">
                    <span className="hero-subtitle">URL BASED AI CONTENT ANALYSIS</span>
                    <h1 className="hero-title">
                        URL 하나로 확인하는<br className="mobile-break" />
                        <span className="keep-sentence">웹페이지 콘텐츠</span> <span className="highlight keep-sentence">안전성 분석</span>
                    </h1>
                    <p className="hero-desc">
                        복잡한 절차 없이 URL만 입력하세요. AI가 해당 페이지의 텍스트와 콘텐츠를 자동으로 스캔하여 유해성, 오탐 가능성, 부적절한 표현을 즉시 진단합니다.<br />
                        <span style={{ display: 'block', marginTop: '12px', fontSize: '15px', color: '#6B7280', fontWeight: '500' }}>
                            * 분석 결과는 엄격한 위험 관리 및 데이터 거버넌스 기준에 따라 안전하게 검증되었습니다.
                        </span>
                    </p>
                    <form className="hero-analysis-form" onSubmit={handleAnalyze}>
                        <input
                            type="url"
                            className="input-field url-input"
                            placeholder="https://example.com"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            required
                        />
                        <button type="submit" className="btn btn-primary btn-large" disabled={loading}>
                            {loading ? '분석 중...' : '무료로 분석 시작하기'}
                        </button>
                    </form>
                </div>
            </section>

            {/* Results Section */}
            {results && (
                <section className="results-section">
                    <div className="container">
                        <h2 className="results-title">분석 결과</h2>
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
                    </div>
                </section>
            )}

            {/* Features Section */}
            <section className="features">
                <div className="container grid-3">
                    <div className="feature-item">
                        <h2 className="feature-number">01.</h2>
                        <h3>텍스트 & 파일 정밀 분석</h3>
                        <p>문장 및 게시글 입력은 물론, PDF/TXT 파일 업로드까지 지원하여 콘텐츠의 위험 요소를 심층 분석합니다.</p>
                    </div>
                    <div className="feature-item">
                        <h2 className="feature-number">02.</h2>
                        <h3>직관적인 결과 시각화</h3>
                        <p>위험도 점수와 세부 항목별 평가를 대시보드 형태로 제공하며, 판단 근거와 추천 조치를 함께 제시합니다.</p>
                    </div>
                    <div className="feature-item">
                        <h2 className="feature-number">03.</h2>
                        <h3>안전 모드 & 피드백</h3>
                        <p>사용 환경에 맞는 필터 강도를 선택할 수 있으며, 오탐/미탐 신고 기능을 통해 모델을 지속적으로 개선합니다.</p>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Home;
