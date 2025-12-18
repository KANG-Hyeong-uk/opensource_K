import React, { useState } from 'react';
import './Home.css';
import { analyzeUrl, submitFeedback } from '../api/analysis';

const Home = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);
    const [showFeedbackModal, setShowFeedbackModal] = useState(false);
    const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);

    // 위험도 레벨별 등급 변환
    const getRiskGrade = (riskLevel) => {
        const grades = {
            safe: 'A+',
            low: 'B+',
            medium: 'C',
            high: 'D'
        };
        return grades[riskLevel] || 'N/A';
    };

    // 위험도 설명 변환
    const getRiskDescription = (riskLevel) => {
        const descriptions = {
            safe: '안전한 콘텐츠입니다.',
            low: '낮은 위험도가 감지되었습니다.',
            medium: '보통 수준의 위험도가 감지되었습니다.',
            high: '높은 위험도가 감지되었습니다.'
        };
        return descriptions[riskLevel] || '분석 결과를 확인할 수 없습니다.';
    };

    // 백엔드 응답을 화면 표시용 형식으로 변환
    const transformAnalysisResult = (analysisData) => {
        const {
            is_clickbait,
            is_hate_speech,
            is_misinformation,
            is_safe,
            confidence_score,
            risk_level,
            analysis_details,
            explanation
        } = analysisData;

        const resultCards = [];

        // 1. 위험도 점수
        resultCards.push({
            title: '위험도 등급',
            value: getRiskGrade(risk_level),
            desc: getRiskDescription(risk_level),
            icon: is_safe ? '🛡️' : '⚠️'
        });

        // 2. 신뢰도 점수
        resultCards.push({
            title: '신뢰도 점수',
            value: `${Math.round(confidence_score * 100)}/100`,
            desc: `AI 분석 신뢰도: ${(confidence_score * 100).toFixed(1)}%`,
            icon: '🎯'
        });

        // 3. 클릭베이트 탐지
        resultCards.push({
            title: '클릭베이트 탐지',
            value: is_clickbait ? '감지됨' : '안전',
            desc: is_clickbait
                ? (analysis_details?.clickbait_reason || '낚시성 콘텐츠가 감지되었습니다.')
                : '클릭베이트 요소가 발견되지 않았습니다.',
            icon: is_clickbait ? '🎣' : '✅'
        });

        // 4. 혐오 표현 탐지
        resultCards.push({
            title: '혐오 표현 탐지',
            value: is_hate_speech ? '감지됨' : '안전',
            desc: is_hate_speech
                ? (analysis_details?.hate_speech_reason || '혐오 표현이 감지되었습니다.')
                : '혐오 표현이 발견되지 않았습니다.',
            icon: is_hate_speech ? '🚫' : '✅'
        });

        // 5. 허위정보 탐지
        resultCards.push({
            title: '허위정보 탐지',
            value: is_misinformation ? '감지됨' : '안전',
            desc: is_misinformation
                ? (analysis_details?.misinformation_reason || '허위 정보 가능성이 감지되었습니다.')
                : '허위 정보가 발견되지 않았습니다.',
            icon: is_misinformation ? '❌' : '✅'
        });

        // 6. 종합 안전도
        resultCards.push({
            title: '종합 안전도',
            value: is_safe ? 'Safe' : 'Unsafe',
            desc: is_safe
                ? '전반적으로 안전한 콘텐츠입니다.'
                : '주의가 필요한 콘텐츠입니다.',
            icon: is_safe ? '✔️' : '⚠️'
        });

        return {
            cards: resultCards,
            explanation: explanation || null
        };
    };

    const handleAnalyze = async (e) => {
        e.preventDefault();
        if (!url) return;

        setLoading(true);
        setError(null);
        setResults(null);
        setFeedbackSubmitted(false);

        try {
            // 실제 API 호출
            const response = await analyzeUrl(url);

            if (response.success && response.result) {
                // 백엔드 응답을 화면 표시 형식으로 변환
                const transformedResults = transformAnalysisResult(response.result);
                setResults(transformedResults);

                // API 사용 카운트 증가
                const currentUsage = parseInt(localStorage.getItem('api_usage') || '0', 10);
                localStorage.setItem('api_usage', currentUsage + 1);
            } else {
                setError('분석 결과를 받지 못했습니다.');
            }
        } catch (err) {
            console.error('Analysis error:', err);
            setError(err.userMessage || err.message || 'URL 분석 중 오류가 발생했습니다.');
        } finally {
            setLoading(false);
        }
    };

    // 피드백 제출 처리
    const handleFeedbackSubmit = async (reason) => {
        try {
            // 백엔드 API로 피드백 제출
            await submitFeedback(url, reason, results);

            // 피드백 제출 완료
            setFeedbackSubmitted(true);
            setShowFeedbackModal(false);

            // 3초 후 메시지 숨기기
            setTimeout(() => {
                setFeedbackSubmitted(false);
            }, 3000);

        } catch (error) {
            console.error('Feedback submission error:', error);
            alert('피드백 제출에 실패했습니다. 다시 시도해주세요.');
        }
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
                            disabled={loading}
                        />
                        <button type="submit" className="btn btn-primary btn-large" disabled={loading}>
                            {loading ? '🔍 AI 분석 중...' : '무료로 분석 시작하기'}
                        </button>
                    </form>
                    {loading && (
                        <div style={{
                            marginTop: '20px',
                            padding: '15px',
                            backgroundColor: '#f0f9ff',
                            border: '2px solid #3b82f6',
                            borderRadius: '8px',
                            textAlign: 'center',
                            fontSize: '14px',
                            color: '#1e40af'
                        }}>
                            <div style={{ marginBottom: '10px', fontSize: '16px', fontWeight: 'bold' }}>
                                ⏳ 콘텐츠 분석이 진행 중입니다
                            </div>
                            <div style={{ marginBottom: '5px' }}>
                                • Selenium으로 웹페이지 크롤링 중...
                            </div>
                            <div style={{ marginBottom: '5px' }}>
                                • Gemini LLM으로 콘텐츠 분석 중...
                            </div>
                            <div style={{ marginBottom: '5px' }}>
                                • RAG 기반 유해성 검증 중...
                            </div>
                            <div style={{ marginTop: '10px', fontSize: '13px', color: '#6b7280' }}>
                                분석에는 최대 2-3분이 소요될 수 있습니다. 잠시만 기다려주세요.
                            </div>
                        </div>
                    )}
                </div>
            </section>

            {/* Error Section */}
            {error && (
                <section className="results-section">
                    <div className="container">
                        <div className="error-message" style={{
                            backgroundColor: '#fee',
                            border: '2px solid #f66',
                            borderRadius: '8px',
                            padding: '20px',
                            textAlign: 'center',
                            color: '#c33'
                        }}>
                            <h3 style={{ marginBottom: '10px' }}>⚠️ 분석 실패</h3>
                            <p>{error}</p>
                        </div>
                    </div>
                </section>
            )}

            {/* Results Section */}
            {results && (
                <section className="results-section">
                    <div className="container">
                        <h2 className="results-title">분석 결과</h2>
                        <div className="results-grid">
                            {results.cards.map((item, index) => (
                                <div key={index} className="result-card">
                                    <div className="result-icon">{item.icon}</div>
                                    <h3>{item.title}</h3>
                                    <div className="result-value">{item.value}</div>
                                    <p>{item.desc}</p>
                                </div>
                            ))}
                        </div>

                        {/* AI 판단 근거 - 가로로 길게 표시 */}
                        {results.explanation && (
                            <div className="explanation-section">
                                <div className="explanation-card">
                                    <div className="explanation-header">
                                        <span className="explanation-icon">🔍</span>
                                        <h3>AI 판단 근거</h3>
                                    </div>
                                    <div className="explanation-content">
                                        {results.explanation}
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* 사용자 피드백 섹션 */}
                        <div className="feedback-section">
                            <div className="feedback-header">
                                <p>이 분석 결과가 정확하지 않다고 생각하시나요?</p>
                            </div>
                            <button
                                className="feedback-button"
                                onClick={() => setShowFeedbackModal(true)}
                                disabled={feedbackSubmitted}
                            >
                                ❌ 오탐입니다
                            </button>
                            {feedbackSubmitted && (
                                <div className="feedback-success-message">
                                    ✅ 피드백이 제출되었습니다. 감사합니다!
                                </div>
                            )}
                        </div>
                    </div>
                </section>
            )}

            {/* 피드백 모달 */}
            {showFeedbackModal && (
                <div className="feedback-modal-overlay" onClick={() => setShowFeedbackModal(false)}>
                    <div className="feedback-modal-content" onClick={(e) => e.stopPropagation()}>
                        <button
                            className="modal-close-btn"
                            onClick={() => setShowFeedbackModal(false)}
                        >
                            ×
                        </button>
                        <div className="feedback-modal-header">
                            <h3>오탐 사유를 선택해주세요</h3>
                            <p>여러분의 피드백으로 AI가 더 정확해집니다</p>
                        </div>
                        <div className="feedback-modal-body">
                            <button
                                className="feedback-reason-btn"
                                onClick={() => handleFeedbackSubmit('교육적 맥락')}
                            >
                                <span className="reason-icon">📚</span>
                                <div className="reason-text">
                                    <strong>교육적 맥락</strong>
                                    <span>교육, 학습 목적의 콘텐츠입니다</span>
                                </div>
                            </button>
                            <button
                                className="feedback-reason-btn"
                                onClick={() => handleFeedbackSubmit('인용/보도')}
                            >
                                <span className="reason-icon">📰</span>
                                <div className="reason-text">
                                    <strong>인용/보도</strong>
                                    <span>뉴스, 인용문 등 보도 목적입니다</span>
                                </div>
                            </button>
                            <button
                                className="feedback-reason-btn"
                                onClick={() => handleFeedbackSubmit('문맥 오해')}
                            >
                                <span className="reason-icon">💬</span>
                                <div className="reason-text">
                                    <strong>문맥 오해</strong>
                                    <span>AI가 문맥을 잘못 이해했습니다</span>
                                </div>
                            </button>
                        </div>
                    </div>
                </div>
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
