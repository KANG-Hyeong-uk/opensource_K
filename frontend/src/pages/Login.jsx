import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { login } from '../api/auth';

const Login = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        if (error) setError('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!formData.username.trim()) {
            setError('사용자명을 입력해주세요.');
            return;
        }
        if (!formData.password) {
            setError('비밀번호를 입력해주세요.');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const result = await login(formData.username, formData.password);
            alert('로그인 성공!');
            navigate('/');
        } catch (err) {
            console.error('로그인 실패:', err);
            setError(err.userMessage || err.message || '로그인에 실패했습니다.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: 'calc(100vh - 200px)' }}>
            <div className="card" style={{ width: '100%', maxWidth: '400px', padding: '40px' }}>
                <h1 style={{ fontSize: '24px', marginBottom: '32px', textAlign: 'center' }}>로그인</h1>

                {error && (
                    <div style={{
                        padding: '12px',
                        marginBottom: '20px',
                        backgroundColor: '#fee',
                        border: '1px solid #fcc',
                        borderRadius: '4px',
                        color: '#c33',
                        fontSize: '14px'
                    }}>
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    <div style={{ marginBottom: '20px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>사용자명</label>
                        <input
                            type="text"
                            name="username"
                            className="input-field"
                            placeholder="아이디를 입력하세요."
                            value={formData.username}
                            onChange={handleChange}
                            disabled={loading}
                        />
                    </div>

                    <div style={{ marginBottom: '32px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>비밀번호</label>
                        <input
                            type="password"
                            name="password"
                            className="input-field"
                            placeholder="비밀번호를 입력하세요."
                            value={formData.password}
                            onChange={handleChange}
                            disabled={loading}
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary"
                        style={{ width: '100%', fontSize: '16px' }}
                        disabled={loading}
                    >
                        {loading ? '로그인 중...' : '로그인'}
                    </button>
                </form>

                <div style={{ marginTop: '24px', textAlign: 'center', fontSize: '14px', color: '#666' }}>
                    계정이 없으신가요? <Link to="/signup" className="t-primary" style={{ fontWeight: '600' }}>회원가입</Link>
                </div>
            </div>
        </div>
    );
};

export default Login;
