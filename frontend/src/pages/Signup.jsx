import React from 'react';
import { Link } from 'react-router-dom';

const Signup = () => {
    return (
        <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: 'calc(100vh - 200px)' }}>
            <div className="card" style={{ width: '100%', maxWidth: '400px', padding: '40px' }}>
                <h1 style={{ fontSize: '24px', marginBottom: '32px', textAlign: 'center' }}>회원가입</h1>

                <form onSubmit={(e) => e.preventDefault()}>
                    <div style={{ marginBottom: '20px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>이름</label>
                        <input type="text" className="input-field" placeholder="홍길동" />
                    </div>

                    <div style={{ marginBottom: '20px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>이메일</label>
                        <input type="email" className="input-field" placeholder="user@example.com" />
                    </div>

                    <div style={{ marginBottom: '20px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>비밀번호</label>
                        <input type="password" className="input-field" placeholder="••••••••" />
                    </div>

                    <div style={{ marginBottom: '32px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>비밀번호 확인</label>
                        <input type="password" className="input-field" placeholder="••••••••" />
                    </div>

                    <button type="submit" className="btn btn-primary" style={{ width: '100%', fontSize: '16px' }}>
                        가입하기
                    </button>
                </form>

                <div style={{ marginTop: '24px', textAlign: 'center', fontSize: '14px', color: '#666' }}>
                    이미 계정이 있으신가요? <Link to="/login" className="t-primary" style={{ fontWeight: '600' }}>로그인</Link>
                </div>
            </div>
        </div>
    );
};

export default Signup;
