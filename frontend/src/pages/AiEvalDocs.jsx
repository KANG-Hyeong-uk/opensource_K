import React, { useState } from 'react';
import './AiEvalDocs.css';

const DocCard = ({ doc }) => {
    const [isFlipped, setIsFlipped] = useState(false);

    const handleClick = () => {
        if (!isFlipped) {
            setIsFlipped(true);
        } else {
            // 이미 뒤집힌 상태(내용이 보이는 상태)에서 클릭 시 다운로드
            const link = document.createElement('a');
            link.href = doc.file;
            link.download = '';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    };

    return (
        <div className={`doc-card-container ${isFlipped ? 'flipped' : ''}`} onClick={handleClick}>
            <div className="doc-card-inner">
                {/* Front Face (뒷면 디자인 - 초기 상태) */}
                {/* CSS에서 transform: rotateY(180deg)를 주지 않은 면이 Front입니다. 
            하지만 '뒤집어져 있다가' 라는 표현은 보통 뒷면이 먼저 보인다는 뜻이므로,
            여기서는 'Card Back' 디자인을 Front Face에 배치하고,
            'Card Content'를 Back Face에 배치해서 180도 돌리는 식이나,
            혹은 상태에 따라 클래스를 붙여서 돌리는 방식을 씁니다.
            
            일반적인 카드 뒤집기:
            Container에 perspective.
            Inner에 transform-style: preserve-3d.
            Front, Back에 backface-visibility: hidden.
            Back은 rotateY(180deg) 미리 적용.
            
            사용자 요청: "뒤집어져 있다가(내용 안 보임) -> 클릭 -> 내용 보임 -> 클릭 -> 다운로드"
            즉, 초기 상태 = 뒷면(디자인).
            클릭 -> 180도 회전 -> 앞면(내용).
        */}

                {/* Front: 카드 뒷면 디자인 (초기 노출) */}
                <div className="doc-card-face doc-card-front">
                    <div className="card-pattern">
                        <div className="icon-wrapper">
                            <span className="lock-icon">🔒</span>
                        </div>
                        <p className="click-hint">Click to Reveal</p>
                    </div>
                    <div className="corner-deco top-left">✦</div>
                    <div className="corner-deco top-right">✦</div>
                    <div className="corner-deco bottom-left">✦</div>
                    <div className="corner-deco bottom-right">✦</div>
                </div>

                {/* Back: 카드 내용 (클릭 후 노출) */}
                <div className="doc-card-face doc-card-back">
                    <div className="doc-content">
                        <div className="doc-icon">📄</div>
                        <h3>{doc.title}</h3>
                        <span className="doc-subtitle">{doc.subtitle}</span>
                        <p>{doc.desc}</p>
                    </div>
                    <div className="download-hint">
                        <span className="download-icon-small">⬇</span>
                        <span>Click again to Download</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

const AiEvalDocs = () => {
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
        <div className="ai-eval-page">
            <div className="container">
                <div className="ai-eval-header">
                    <h1>AI 평가 문서</h1>
                    <p>
                        카드를 뒤집어 상세 내용을 확인하세요.<br />
                        내용 확인 후 다시 클릭하면 문서가 다운로드됩니다.
                    </p>
                </div>

                <div className="docs-grid">
                    {docs.map((doc) => (
                        <DocCard key={doc.id} doc={doc} />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AiEvalDocs;
