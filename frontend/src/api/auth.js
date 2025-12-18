/**
 * 인증 관련 API
 * - 로그인
 * - 회원가입
 * - 프로필 조회/수정
 * - 로그아웃
 */

import apiClient from './client';
import {
  setAccessToken,
  setRefreshToken,
  setUserInfo,
  clearAuth
} from '../utils/storage';
import { logInfo, logError } from '../utils/logger';

/**
 * 로그인
 * @param {string} username - 사용자명
 * @param {string} password - 비밀번호
 * @returns {Promise<Object>} 토큰 및 사용자 정보
 */
export const login = async (username, password) => {
  try {
    const response = await apiClient.post('/api/v1/auth/token/', {
      username,
      password
    });

    const { access, refresh } = response.data;

    // 토큰 저장
    setAccessToken(access);
    setRefreshToken(refresh);

    logInfo('Auth', 'Login successful', { username });

    // 프로필 조회하여 사용자 정보 저장
    try {
      const profile = await getProfile();
      setUserInfo(profile);
      return {
        success: true,
        tokens: { access, refresh },
        user: profile
      };
    } catch (profileError) {
      logError('Auth', 'Failed to fetch profile after login', profileError);
      // 프로필 조회 실패해도 로그인은 성공으로 처리
      return {
        success: true,
        tokens: { access, refresh },
        user: null
      };
    }

  } catch (error) {
    logError('Auth', 'Login failed', error);

    // 에러 메시지 표준화
    const errorMessage = error.details?.detail ||
                        error.message ||
                        '로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.';

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage
    };
  }
};

/**
 * 회원가입
 * @param {Object} userData - 사용자 정보
 * @param {string} userData.username - 사용자명 (필수)
 * @param {string} userData.email - 이메일
 * @param {string} userData.password - 비밀번호 (필수)
 * @param {string} userData.password_check - 비밀번호 확인 (필수)
 * @param {string} userData.first_name - 이름
 * @param {string} userData.last_name - 성
 * @returns {Promise<Object>} 등록된 사용자 정보
 */
export const register = async (userData) => {
  try {
    const response = await apiClient.post('/api/v1/accounts/register/', userData);

    logInfo('Auth', 'Registration successful', { username: userData.username });

    return {
      success: true,
      message: response.data.message || '회원가입이 완료되었습니다.',
      user: response.data.data
    };

  } catch (error) {
    logError('Auth', 'Registration failed', error);

    // 유효성 검사 에러 처리
    let errorMessage = '회원가입에 실패했습니다.';
    let fieldErrors = {};

    if (error.details) {
      fieldErrors = error.details;

      // 첫 번째 에러 메시지를 메인 메시지로 사용
      const firstError = Object.values(error.details)[0];
      if (Array.isArray(firstError)) {
        errorMessage = firstError[0];
      } else {
        errorMessage = firstError;
      }
    }

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage,
      fieldErrors
    };
  }
};

/**
 * 프로필 조회
 * @returns {Promise<Object>} 사용자 프로필
 */
export const getProfile = async () => {
  try {
    const response = await apiClient.get('/api/v1/accounts/profile/');

    logInfo('Auth', 'Profile fetched successfully');

    return response.data.data;

  } catch (error) {
    logError('Auth', 'Failed to fetch profile', error);

    const errorMessage = error.message || '프로필 조회에 실패했습니다.';

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage
    };
  }
};

/**
 * 프로필 수정
 * @param {Object} profileData - 수정할 프로필 정보
 * @param {string} profileData.email - 이메일
 * @param {string} profileData.first_name - 이름
 * @param {string} profileData.last_name - 성
 * @returns {Promise<Object>} 수정된 프로필
 */
export const updateProfile = async (profileData) => {
  try {
    const response = await apiClient.put('/api/v1/accounts/profile/', profileData);

    logInfo('Auth', 'Profile updated successfully');

    // 업데이트된 프로필 저장
    const updatedProfile = response.data.data;
    setUserInfo(updatedProfile);

    return {
      success: true,
      message: response.data.message || '프로필이 수정되었습니다.',
      user: updatedProfile
    };

  } catch (error) {
    logError('Auth', 'Failed to update profile', error);

    let errorMessage = '프로필 수정에 실패했습니다.';
    let fieldErrors = {};

    if (error.details) {
      fieldErrors = error.details;
      const firstError = Object.values(error.details)[0];
      if (Array.isArray(firstError)) {
        errorMessage = firstError[0];
      } else {
        errorMessage = firstError;
      }
    }

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage,
      fieldErrors
    };
  }
};

/**
 * 로그아웃
 * @returns {void}
 */
export const logout = () => {
  clearAuth();
  logInfo('Auth', 'Logout successful');
};
