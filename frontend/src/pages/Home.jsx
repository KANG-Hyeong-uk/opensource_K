import React, { useState, useEffect } from 'react';
import './Home.css';
import { Link } from 'react-router-dom';

const DocCard = ({ doc }) => {
    const [isFlipped, setIsFlipped] = useState(false);
    const [canDownload, setCanDownload] = useState(false);

    useEffect(() => {
        let timer;
        if (isFlipped) {
            // Wait 1 second after flipping before enabling download overlay
            timer = setTimeout(() => {
                setCanDownload(true);
            }, 1000);
        } else {
            setCanDownload(false);
        }
        return () => clearTimeout(timer);
    }, [isFlipped]);

    const handleClick = () => {
        if (!isFlipped) {
            setIsFlipped(true); // First click: Flip
        } else {
            setIsFlipped(false);
        }
    };

    const handleDownload = (e) => {
        e.stopPropagation(); // Prevent card from flipping back
        const link = document.createElement('a');
        link.href = doc.file;
        link.download = '';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div
            className={`doc-card-container simple-grid ${isFlipped ? 'flipped' : ''} ${canDownload ? 'can-download' : ''}`}
            onClick={handleClick}
        >
            <div className="doc-card-inner">
                {/* Front (Blue Pattern) - Visible initially */}
                {/* Front (Document Cover Style) */}
                {/* Front (Iconic Document Style) */}
                <div className="doc-card-face doc-card-front">
                    {/* The Layered Document Graphic */}
                    <div className="doc-graphic-wrapper">
                        <div className="doc-graphic-layer layer-1"></div>
                        <div className="doc-graphic-layer layer-2"></div>
                        <div className="doc-graphic-main">
                            <div className="doc-line title-line"></div>
                            <div className="doc-line body-line"></div>
                            <div className="doc-line body-line short"></div>
                            <div className="doc-line body-line"></div>

                            {/* Folded Corner Effect via CSS */}
                            <div className="doc-corner-fold"></div>
                        </div>
                    </div>

                    <div className="doc-front-content">
                        <h4 className="doc-front-title">{doc.title}</h4>
                        <span className="doc-front-tag">OFFICIAL DOCS</span>
                    </div>
                </div>

                {/* Back (Content) - Visible when flipped */}
                <div className="doc-card-face doc-card-back">
                    <div className="doc-content">
                        <div className="doc-icon">📄</div>
                        <h3>{doc.title}</h3>
                        <span className="doc-subtitle">{doc.subtitle}</span>
                        <p>{doc.desc}</p>
                    </div>

                    {/* Overlay appears on HOVER of the Back Face */}
                    <div className="download-overlay" onClick={handleDownload}>
                        <div className="download-btn">
                            <span className="download-icon-large">⬇</span>
                            <span>Download</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

const Home = () => {
    // No deck state needed, always open grid
    const docs = [
        {
            id: 1,
            title: '영향 식별·기획 문서',
            subtitle: '사용자 가치 & 위험 사전 분석',
            desc: '서비스가 어떤 상황에서 오판할 수 있는지 사전에 분석하여, 예상치 못한 오류나 위험한 응답을 최소화합니다.',
            file: '/docs/impact_assessment.doc'
        },
        {
            id: 2,
            title: '위험 평가·관리 문서',
            subtitle: '위험도 기반 안전 관리',
            desc: 'AI가 잘못된 판단을 할 가능성을 위험도 기반으로 관리합니다. 어떤 기준으로 위험이 관리되는지 투명하게 공개합니다.',
            file: '/docs/risk_management.doc'
        },
        {
            id: 3,
            title: '데이터 거버넌스·편향 문서',
            subtitle: '결과 품질 & 데이터 무결성 보장',
            desc: '편향된 데이터를 걸러내고 품질 기준을 통과한 데이터만 사용합니다. 유해 분류의 근거를 명확히 이해할 수 있습니다.',
            file: '/docs/data_governance.doc'
        },
        {
            id: 4,
            title: '모델 성능 평가·안전장치 문서',
            subtitle: '성능 검증 & 신뢰도 산출 근거',
            desc: '성능 검증 방식, 슬라이스별 테스트, 실패 대응 로직을 포함하여 결과의 신뢰도를 어떻게 산출했는지 설명합니다.',
            file: '/docs/model_validation.docx'
        },
        {
            id: 5,
            title: '인간 감독·통제 문서',
            subtitle: 'Human-in-the-loop 검토 시스템',
            desc: 'AI가 단독으로 판단하지 않습니다. 일정 기준을 넘는 위험 상황은 사람이 직접 검토하여 신뢰성을 높입니다.',
            file: '/docs/human_oversight.doc'
        },
        {
            id: 6,
            title: '운영·모니터링·검토 문서',
            subtitle: '지속적 개선 & 안정성 유지',
            desc: '모델 오류나 이상 징후 발생 시 대응 매뉴얼을 공개하며, 서비스가 지속적으로 모니터링됨을 보장합니다.',
            file: '/docs/operation_monitoring.doc'
        }
    ];

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
                    <Link to="/analysis" className="btn btn-primary btn-large">
                        무료로 분석 시작하기
                    </Link>
                </div>
            </section>

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

            {/* AI Eval Docs Section (Simple Grid Style) */}
            <section className="ai-docs-section">
                <div className="container">
                    <div className="section-header">
                        <h2>AI 평가 및 검증 문서</h2>
                        <p>카드를 클릭하여 상세 내용을 확인하고 다운로드하세요.</p>
                    </div>

                    <div className="deck-container open simple-grid-view">
                        {docs.map((doc) => (
                            <DocCard key={doc.id} doc={doc} />
                        ))}
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Home;
