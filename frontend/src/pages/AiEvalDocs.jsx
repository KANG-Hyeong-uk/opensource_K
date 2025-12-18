import React, { useState } from 'react';
import './AiEvalPage.css';

const DocCard = ({ doc, onClick }) => {
    return (
        <div className="doc-card-container" onClick={() => onClick(doc)}>
            <div className="doc-card-inner">
                {/* Front Face: Orange Pattern Top + White Info Bottom */}
                <div className="doc-card-front">
                    <div className="card-front-top">
                        <div className="doc-icon-wrapper">
                            <svg width="60" height="70" viewBox="0 0 60 70" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect x="5" y="5" width="45" height="55" rx="4" fill="#f8fafc" stroke="#334155" strokeWidth="2" />
                                <rect x="10" y="0" width="45" height="55" rx="4" fill="white" stroke="#334155" strokeWidth="2" />
                                <path d="M20 15H45" stroke="#94a3b8" strokeWidth="3" strokeLinecap="round" />
                                <path d="M20 25H45" stroke="#cbd5e1" strokeWidth="3" strokeLinecap="round" />
                                <path d="M20 35H35" stroke="#cbd5e1" strokeWidth="3" strokeLinecap="round" />
                                <path d="M43 0L55 12H47C44.7909 12 43 10.2091 43 8V0Z" fill="#cbd5e1" />
                            </svg>
                        </div>
                    </div>
                    <div className="card-front-bottom">
                        <h3 className="front-title">{doc.title}</h3>
                        <span className="official-badge">OFFICIAL DOCS</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Modal Component
const DocumentModal = ({ doc, onClose }) => {
    if (!doc) return null;

    return (
        <div className="doc-modal-overlay" onClick={onClose}>
            <div className="doc-modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="modal-close-btn" onClick={onClose}>&times;</button>

                <div className="modal-header">
                    <div className="modal-icon-badge">📄</div>
                    <h2>{doc.title}</h2>
                    <span className="modal-subtitle">{doc.subtitle}</span>
                </div>

                <div className="modal-body">
                    <div className="summary-section">
                        <h3>상세 내용 요약</h3>
                        <div className="summary-text">
                            {doc.details.split('\n').map((line, idx) => (
                                <p key={idx}>{line}</p>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="modal-footer">
                    <a href={doc.file} download className="modal-download-btn">
                        <span>문서 다운로드</span>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                            <polyline points="7 10 12 15 17 10"></polyline>
                            <line x1="12" y1="15" x2="12" y2="3"></line>
                        </svg>
                    </a>
                </div>
            </div>
        </div>
    );
};

const AiEvalDocs = () => {
    const [selectedDoc, setSelectedDoc] = useState(null);

    const docs = [
        {
            id: 1,
            title: '영향 식별·기획 문서',
            subtitle: '사용자 가치 & 위험 사전 분석',
            desc: '서비스가 어떤 상황에서 오판할 수 있는지 사전에 분석하여, 예상치 못한 오류나 위험한 응답을 최소화합니다.',
            file: '/docs/impact_assessment.doc',
            details: `본 문서는 AI 서비스 기획 단계에서 예상되는 사회적, 윤리적 영향을 포괄적으로 식별한 결과 보고서입니다.
            
주요 내용:
1. 이해관계자 분석: 사용자, 개발자, 그리고 사회 전반에 미칠 수 있는 영향을 다각도로 분석하였습니다.
2. 잠재적 위험 시나리오: 서비스 오용, 데이터 편향, 예상치 못한 오작동 등 15가지 핵심 위험 시나리오를 도출하고 등급을 매겼습니다.
3. 선제적 대응 전략: 식별된 위험을 기술적(모델 튜닝, 필터링) 및 정책적(이용약관, 가이드라인)으로 완화하기 위한 구체적인 실행 계획을 수립하였습니다.

이 문서를 통해 우리는 서비스가 단순히 기능을 제공하는 것을 넘어, 안전하고 신뢰할 수 있는 사용자 경험을 제공함을 보장합니다.`
        },
        {
            id: 2,
            title: '위험 평가·관리 문서',
            subtitle: '위험도 기반 안전 관리',
            desc: 'AI가 잘못된 판단을 할 가능성을 위험도 기반으로 관리합니다. 어떤 기준으로 위험이 관리되는지 투명하게 공개합니다.',
            file: '/docs/risk_management.doc',
            details: `본 문서는 ISO/IEC 23894 및 NIST AI Risk Management Framework를 기반으로 수립된 위험 평가 및 관리 체계를 기술합니다.

주요 내용:
1. 위험 평가 매트릭스: 발생 가능성과 영향도를 축으로 하여 4단계(Low, Medium, High, Critical)의 위험 등급을 정의하였습니다.
2. 지속적인 모니터링 체계: 모델 배포 이후에도 실시간으로 입력 데이터와 출력 결과를 모니터링하여, 드리프트(Drift) 현상이나 새로운 유형의 위험을 탐지하는 프로세스를 구축하였습니다.
3. 잔여 위험 수용 기준: 완벽한 제거가 불가능한 AI 특성을 고려하여, 사회적으로 용인 가능한 수준의 잔여 위험 기준을 명시하고 투명하게 관리합니다.`
        },
        {
            id: 3,
            title: '데이터 거버넌스·편향 문서',
            subtitle: '결과 품질 & 데이터 무결성 보장',
            desc: '편향된 데이터를 걸러내고 품질 기준을 통과한 데이터만 사용합니다. 유해 분류의 근거를 명확히 이해할 수 있습니다.',
            file: '/docs/data_governance.doc',
            details: `본 문서는 AI 학습에 사용된 데이터의 수집, 가공, 관리 전 과정에 걸친 거버넌스 원칙과 편향성 완화 조치를 설명합니다.

주요 내용:
1. 데이터 다양성 확보: 성별, 연령, 지역 등 인구통계학적 다양성을 고려한 데이터셋 구성 비율을 공개합니다.
2. 편향 제거 알고리즘: 학습 데이터 내 특정 집단에 대한 혐오 표현이나 스테레오타입을 탐지하고 제거하기 위해 사용된 NLP 전처리 기술과 필터링 로직을 상세히 기술합니다.
3. 개인정보 비식별화: GDPR 및 국내 개인정보보호법에 의거하여, 학습 데이터 내 민감 정보를 가명/익명 처리한 절차와 검증 결과를 포함합니다.`
        },
        {
            id: 4,
            title: '모델 성능 평가·안전장치 문서',
            subtitle: '성능 검증 & 신뢰도 산출 근거',
            desc: '성능 검증 방식, 슬라이스별 테스트, 실패 대응 로직을 포함하여 결과의 신뢰도를 어떻게 산출했는지 설명합니다.',
            file: '/docs/model_validation.docx',
            details: `본 문서는 AI 모델의 성능을 정량적, 정성적으로 검증한 결과와 안전장치(Safety Guardrail) 구축 현황을 다룹니다.

주요 내용:
1. 성능 지표(Metrics): 정확도(Accuracy), 정밀도(Precision), 재현율(Recall) 외에도 강건성(Robustness)과 공정성(Fairness) 지표를 별도로 산출하여 평가하였습니다.
2. 레드티밍(Red Teaming) 결과: 적대적 공격(Adversarial Attack) 시나리오를 가정한 모의 해킹 테스트 결과와 이에 대한 방어율을 공개합니다.
3. 안전장치 로직: 모델이 답변하기 곤란하거나 위험한 질문을 받았을 때 발동하는 우회 답변(Refusal) 메커니즘과 윤리 필터의 작동 원리를 설명합니다.`
        },
        {
            id: 5,
            title: '인간 감독·통제 문서',
            subtitle: 'Human-in-the-loop 검토 시스템',
            desc: 'AI가 단독으로 판단하지 않습니다. 일정 기준을 넘는 위험 상황은 사람이 직접 검토하여 신뢰성을 높입니다.',
            file: '/docs/human_oversight.doc',
            details: `본 문서는 AI의 판단을 인간이 검토하고 개입하는 HITL(Human-in-the-Loop) 시스템의 설계와 운영 방식을 설명합니다.

주요 내용:
1. 개입 기준(Threshold): 모델의 신뢰도 점수가 일정 수준(예: 85%) 미만이거나, 민감한 주제(의료, 법률 등)와 관련된 질의일 경우 자동으로 인간 검토자에게 에스컬레이션되는 로직을 정의합니다.
2. 운영 인력 전문성: 검토를 수행하는 인력의 자격 요건과 정기적인 윤리/직무 교육 이수 현황을 기술합니다.
3. 피드백 루프: 인간의 수정 사항이 다시 모델 학습에 반영되어(RLHF) 지속적으로 성능이 개선되는 선순환 구조를 시각화하여 제시합니다.`
        },
        {
            id: 6,
            title: '운영·모니터링·검토 문서',
            subtitle: '지속적 개선 & 안정성 유지',
            desc: '모델 오류나 이상 징후 발생 시 대응 매뉴얼을 공개하며, 서비스가 지속적으로 모니터링됨을 보장합니다.',
            file: '/docs/operation_monitoring.doc',
            details: `본 문서는 서비스 출시 이후의 안정적인 운영을 위한 모니터링 파이프라인과 사고 대응(Incident Response) 매뉴얼을 포함합니다.

주요 내용:
1. 실시간 대시보드: API 응답 시간, 에러율, 사용자 신고 건수 등을 실시간으로 시각화하여 관리하는 모니터링 시스템을 소개합니다.
2. 이상 징후 탐지 알림: 급격한 트래픽 증가나 비정상적인 패턴의 입력이 감지될 때, 운영팀에게 즉시 알림이 전송되는 자동화 시스템을 설명합니다.
3. 버전 관리 및 롤백: 문제 발생 시 즉시 이전의 안정적인 모델 버전으로 원복(Rollback)할 수 있는 배포 파이프라인과 절차를 명시하여 서비스 연속성을 보장합니다.`
        }
    ];

    return (
        <div className="ai-eval-page">
            <div className="wide-container">
                <div className="ai-eval-header">
                    <h1>AI 평가 문서</h1>
                    <p>
                        카드를 클릭하면 상세 내용을 확인하고 문서를 다운로드할 수 있습니다.
                    </p>
                </div>

                <div className="docs-grid">
                    {docs.map((doc) => (
                        <DocCard
                            key={doc.id}
                            doc={doc}
                            onClick={setSelectedDoc}
                        />
                    ))}
                </div>

                {/* Modal for details */}
                {selectedDoc && (
                    <DocumentModal
                        doc={selectedDoc}
                        onClose={() => setSelectedDoc(null)}
                    />
                )}
            </div>
        </div>
    );
};

export default AiEvalDocs;
