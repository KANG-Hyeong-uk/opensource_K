import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { register } from '../api/auth';

const Signup = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        password_check: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [fieldErrors, setFieldErrors] = useState({});

    const [showPassword, setShowPassword] = useState(false);
    const [showPasswordCheck, setShowPasswordCheck] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        if (fieldErrors[name]) {
            setFieldErrors(prev => ({
                ...prev,
                [name]: null
            }));
        }
        if (error) setError('');
    };

    const togglePassword = () => setShowPassword(!showPassword);
    const togglePasswordCheck = () => setShowPasswordCheck(!showPasswordCheck);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!formData.username.trim()) {
            setError('사용자명을 입력해주세요.');
            return;
        }
        if (!formData.email.trim()) {
            setError('이메일을 입력해주세요.');
            return;
        }
        if (!formData.password) {
            setError('비밀번호를 입력해주세요.');
            return;
        }
        if (formData.password !== formData.password_check) {
            setError('비밀번호가 일치하지 않습니다.');
            return;
        }

        setLoading(true);
        setError('');
        setFieldErrors({});

        try {
            const result = await register(formData);
            alert(result.message || '회원가입이 완료되었습니다. 로그인해주세요.');
            navigate('/login');
        } catch (err) {
            console.error('회원가입 실패:', err);
            setError(err.userMessage || err.message || '회원가입에 실패했습니다.');
            if (err.fieldErrors) {
                setFieldErrors(err.fieldErrors);
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: 'calc(100vh - 200px)' }}>
            <div className="card" style={{ width: '100%', maxWidth: '400px', padding: '40px' }}>
                <h1 style={{ fontSize: '24px', marginBottom: '32px', textAlign: 'center' }}>회원가입</h1>

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
                        {fieldErrors.username && (
                            <div style={{ color: '#c33', fontSize: '12px', marginTop: '4px' }}>
                                {Array.isArray(fieldErrors.username) ? fieldErrors.username[0] : fieldErrors.username}
                            </div>
                        )}
                    </div>

                    <div style={{ marginBottom: '20px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>이메일</label>
                        <input
                            type="email"
                            name="email"
                            className="input-field"
                            placeholder="이메일을 입력하세요."
                            value={formData.email}
                            onChange={handleChange}
                            disabled={loading}
                        />
                        {fieldErrors.email && (
                            <div style={{ color: '#c33', fontSize: '12px', marginTop: '4px' }}>
                                {Array.isArray(fieldErrors.email) ? fieldErrors.email[0] : fieldErrors.email}
                            </div>
                        )}
                    </div>

                    <div style={{ marginBottom: '20px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>비밀번호</label>
                        <div style={{ position: 'relative' }}>
                            <input
                                type={showPassword ? "text" : "password"}
                                name="password"
                                className="input-field"
                                placeholder="비밀번호를 입력하세요."
                                value={formData.password}
                                onChange={handleChange}
                                disabled={loading}
                                style={{ paddingRight: '40px' }}
                            />
                            <button
                                type="button"
                                onClick={togglePassword}
                                style={{
                                    position: 'absolute',
                                    right: '10px',
                                    top: '50%',
                                    transform: 'translateY(-50%)',
                                    background: 'none',
                                    border: 'none',
                                    cursor: 'pointer',
                                    padding: '4px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    color: '#666'
                                }}
                            >
                                {showPassword ? (
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                        <circle cx="12" cy="12" r="3"></circle>
                                    </svg>
                                ) : (
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                                        <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                                    </svg>
                                )}
                            </button>
                        </div>
                        {fieldErrors.password && (
                            <div style={{ color: '#c33', fontSize: '12px', marginTop: '4px' }}>
                                {Array.isArray(fieldErrors.password) ? fieldErrors.password[0] : fieldErrors.password}
                            </div>
                        )}
                    </div>

                    <div style={{ marginBottom: '32px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>비밀번호 확인</label>
                        <div style={{ position: 'relative' }}>
                            <input
                                type={showPasswordCheck ? "text" : "password"}
                                name="password_check"
                                className="input-field"
                                placeholder="비밀번호를 다시 입력하세요."
                                value={formData.password_check}
                                onChange={handleChange}
                                disabled={loading}
                                style={{ paddingRight: '40px' }}
                            />
                            <button
                                type="button"
                                onClick={togglePasswordCheck}
                                style={{
                                    position: 'absolute',
                                    right: '10px',
                                    top: '50%',
                                    transform: 'translateY(-50%)',
                                    background: 'none',
                                    border: 'none',
                                    cursor: 'pointer',
                                    padding: '4px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    color: '#666'
                                }}
                            >
                                {showPasswordCheck ? (
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                        <circle cx="12" cy="12" r="3"></circle>
                                    </svg>
                                ) : (
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                                        <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                                    </svg>
                                )}
                            </button>
                        </div>
                        {fieldErrors.password_check && (
                            <div style={{ color: '#c33', fontSize: '12px', marginTop: '4px' }}>
                                {Array.isArray(fieldErrors.password_check) ? fieldErrors.password_check[0] : fieldErrors.password_check}
                            </div>
                        )}
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary"
                        style={{ width: '100%', fontSize: '16px' }}
                        disabled={loading}
                    >
                        {loading ? '가입 중...' : '가입하기'}
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
