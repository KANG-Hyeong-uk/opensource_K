import React from 'react';
import Header from './Header';
import './Layout.css';

const Layout = ({ children }) => {
    return (
        <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
            <Header />
            <main style={{ flex: 1 }}>
                {children}
            </main>
            <footer className="footer-section">
                <div className="container footer-container">
                    <span className="copyright">&copy; 2025 URL Analysis Service. All rights reserved.</span>
                    <div className="footer-links">
                        <a href="/docs">API Documentation</a>
                        <a href="#">Terms</a>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Layout;
