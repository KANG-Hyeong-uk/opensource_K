import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Header.css';

const Header = () => {
    const location = useLocation();
    const [isMenuOpen, setIsMenuOpen] = React.useState(false);

    const isActive = (path) => location.pathname === path;

    const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
    const closeMenu = () => setIsMenuOpen(false);

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
                    <Link to="/analysis" className={isActive('/analysis') ? 'active' : ''} onClick={closeMenu}>분석</Link>
                    <Link to="/docs" className={isActive('/docs') ? 'active' : ''} onClick={closeMenu}>API 명세서</Link>
                    <Link to="/api-usage" className={isActive('/api-usage') ? 'active' : ''} onClick={closeMenu}>API 사용량</Link>
                    <Link to="/login" className="btn-login" onClick={closeMenu}>로그인</Link>
                </nav>
            </div>
            {/* Overlay for mobile menu */}
            {isMenuOpen && <div className="menu-overlay" onClick={closeMenu}></div>}
        </header>
    );
};

export default Header;
