/**
 * 로컬 스토리지 유틸리티
 * JWT 토큰 및 사용자 정보 관리
 */

const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_INFO: 'user_info',
};

/**
 * Access Token 저장
 */
export const setAccessToken = (token) => {
  try {
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, token);
  } catch (error) {
    console.error('[Storage] Failed to save access token:', error);
  }
};

/**
 * Access Token 조회
 */
export const getAccessToken = () => {
  try {
    return localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
  } catch (error) {
    console.error('[Storage] Failed to get access token:', error);
    return null;
  }
};

/**
 * Refresh Token 저장
 */
export const setRefreshToken = (token) => {
  try {
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, token);
  } catch (error) {
    console.error('[Storage] Failed to save refresh token:', error);
  }
};

/**
 * Refresh Token 조회
 */
export const getRefreshToken = () => {
  try {
    return localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
  } catch (error) {
    console.error('[Storage] Failed to get refresh token:', error);
    return null;
  }
};

/**
 * 사용자 정보 저장
 */
export const setUserInfo = (userInfo) => {
  try {
    localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(userInfo));
  } catch (error) {
    console.error('[Storage] Failed to save user info:', error);
  }
};

/**
 * 사용자 정보 조회
 */
export const getUserInfo = () => {
  try {
    const userInfo = localStorage.getItem(STORAGE_KEYS.USER_INFO);
    return userInfo ? JSON.parse(userInfo) : null;
  } catch (error) {
    console.error('[Storage] Failed to get user info:', error);
    return null;
  }
};

/**
 * 모든 인증 정보 삭제 (로그아웃)
 */
export const clearAuth = () => {
  try {
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER_INFO);
  } catch (error) {
    console.error('[Storage] Failed to clear auth data:', error);
  }
};

/**
 * 인증 상태 확인
 */
export const isAuthenticated = () => {
  return !!getAccessToken();
};
