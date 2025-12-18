import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import './Header.css';
import { getUserInfo, isAuthenticated, clearAuth } from '../utils/storage';

const Header = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [isMenuOpen, setIsMenuOpen] = React.useState(false);
    const [userInfo, setUserInfo] = React.useState(null);

    // 사용자 정보 확인
    React.useEffect(() => {
        if (isAuthenticated()) {
            const user = getUserInfo();
            setUserInfo(user);
        } else {
            setUserInfo(null);
        }
    }, [location.pathname]); // location이 변경될 때마다 다시 확인

    const isActive = (path) => location.pathname === path;

    const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
    const closeMenu = () => setIsMenuOpen(false);

    // 로그아웃 처리
    const handleLogout = () => {
        clearAuth();
        setUserInfo(null);
        closeMenu();
        navigate('/');
    };

    return (
        <header className="header">
            <div className="container header-container">
                <Link to="/" className="logo" onClick={closeMenu}>
                    TRAIN Korea <span className="logo-sub">| ThinkforBL</span>
                </Link>

                <button className={`hamburger ${isMenuOpen ? 'active' : ''}`} onClick={toggleMenu} aria-label="Menu">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>

                <nav className={`gnb ${isMenuOpen ? 'open' : ''}`}>
                    <Link to="/" className={isActive('/') ? 'active' : ''} onClick={closeMenu}>Home</Link>
                    <Link to="/analysis" className={isActive('/analysis') ? 'active' : ''} onClick={closeMenu}>AI평가 및 검증 문서</Link>
                    <Link to="/docs" className={isActive('/docs') ? 'active' : ''} onClick={closeMenu}>API 명세서</Link>
                    <Link to="/api-usage" className={isActive('/api-usage') ? 'active' : ''} onClick={closeMenu}>API 사용량</Link>
                    {userInfo ? (
                        <div className="user-menu">
                            <span className="user-name">{userInfo.username || userInfo.first_name || '사용자'}</span>
                            <button className="btn-logout" onClick={handleLogout}>로그아웃</button>
                        </div>
                    ) : (
                        <Link to="/login" className="btn-login" onClick={closeMenu}>로그인</Link>
                    )}
                </nav>
            </div>
            {/* Overlay for mobile menu */}
            {isMenuOpen && <div className="menu-overlay" onClick={closeMenu}></div>}
        </header>
    );
};

export default Header;
