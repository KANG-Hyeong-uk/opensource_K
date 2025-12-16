import React, { useEffect, useState } from 'react';

const ApiUsage = () => {
    const [usageCount, setUsageCount] = useState(0);

    useEffect(() => {
        const saved = localStorage.getItem('api_usage');
        if (saved) {
            setUsageCount(parseInt(saved, 10));
        }
    }, []);

    return (
        <div className="container" style={{ padding: '80px 20px', textAlign: 'center' }}>
            <h1 style={{ fontSize: '32px', marginBottom: '40px' }}>API 사용량</h1>

            <div className="card" style={{ maxWidth: '400px', margin: '0 auto', padding: '60px 40px' }}>
                <h2 style={{ fontSize: '16px', color: '#666', marginBottom: '20px' }}>이번 달 호출 횟수</h2>
                <div style={{ fontSize: '64px', fontWeight: '800', color: 'var(--color-primary)' }}>
                    {usageCount.toLocaleString()}
                </div>
                <p style={{ marginTop: '20px', color: '#888', fontSize: '14px' }}>
                    매월 1일 초기화됩니다. (Demo)
                </p>
            </div>

            <div style={{ marginTop: '60px' }}>
                <h3 style={{ fontSize: '18px', marginBottom: '16px' }}>개발자 문서를 찾으시나요?</h3>
                <p style={{ color: '#666', marginBottom: '24px' }}>
                    API를 연동하여 나만의 서비스를 구축해보세요.
                </p>
                <a href="/docs" className="btn btn-primary" style={{ textDecoration: 'none' }}>
                    API 디자인/사용법 확인하기
                </a>
            </div>
        </div>
    );
};

export default ApiUsage;
