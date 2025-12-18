/**
 * Axios API 클라이언트 설정
 * - 기본 설정
 * - 인터셉터 (요청/응답)
 * - 에러 처리
 */

import axios from 'axios';
import {
  getAccessToken,
  getRefreshToken,
  setAccessToken,
  clearAuth
} from '../utils/storage';
import {
  logApiRequest,
  logApiResponse,
  logApiError,
  logWarn
} from '../utils/logger';

/**
 * API Base URL
 * 개발 환경: localhost:8000
 * 운영 환경: 실제 도메인
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Axios 인스턴스 생성
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 180000, // 180초 (3분) - Selenium + LLM + RAG 분석 시간 고려
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 토큰 갱신 중복 방지를 위한 플래그
 */
let isRefreshing = false;
let failedQueue = [];

/**
 * 대기 중인 요청 처리
 */
const processQueue = (error, token = null) => {
  failedQueue.forEach(promise => {
    if (error) {
      promise.reject(error);
    } else {
      promise.resolve(token);
    }
  });

  failedQueue = [];
};

/**
 * Request Interceptor
 * - Access Token 자동 추가
 * - 요청 로깅
 */
apiClient.interceptors.request.use(
  (config) => {
    // Access Token 추가
    const accessToken = getAccessToken();
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    // 요청 로깅
    logApiRequest(config.method, config.url, config.data);

    return config;
  },
  (error) => {
    logApiError('REQUEST', error.config?.url || 'unknown', error);
    return Promise.reject(error);
  }
);

/**
 * Response Interceptor
 * - 응답 로깅
 * - 401 에러 시 토큰 갱신
 * - 에러 표준화
 */
apiClient.interceptors.response.use(
  (response) => {
    // 응답 로깅
    logApiResponse(
      response.config.method,
      response.config.url,
      response.status,
      response.data
    );

    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // 요청 설정이 없는 경우
    if (!originalRequest) {
      logApiError('RESPONSE', 'unknown', error);
      return Promise.reject(error);
    }

    // 401 Unauthorized 에러 처리
    if (error.response?.status === 401 && !originalRequest._retry) {
      // 토큰 갱신 중인 경우 대기
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then(token => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return apiClient(originalRequest);
          })
          .catch(err => {
            return Promise.reject(err);
          });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = getRefreshToken();

      // Refresh Token이 없으면 로그아웃
      if (!refreshToken) {
        logWarn('Auth', 'No refresh token available. Logging out.');
        clearAuth();
        window.location.href = '/login';
        return Promise.reject(error);
      }

      try {
        // 토큰 갱신 요청
        const response = await axios.post(
          `${API_BASE_URL}/api/v1/auth/token/refresh/`,
          { refresh: refreshToken }
        );

        const { access } = response.data;

        // 새 Access Token 저장
        setAccessToken(access);

        // 대기 중인 요청들 처리
        processQueue(null, access);

        // 원래 요청 재시도
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return apiClient(originalRequest);

      } catch (refreshError) {
        // 토큰 갱신 실패 시 로그아웃
        processQueue(refreshError, null);
        clearAuth();
        window.location.href = '/login';
        return Promise.reject(refreshError);

      } finally {
        isRefreshing = false;
      }
    }

    // 에러 로깅
    logApiError(
      originalRequest.method,
      originalRequest.url,
      error
    );

    // 에러 표준화
    const standardError = {
      status: error.response?.status,
      statusText: error.response?.statusText,
      message: error.response?.data?.message || error.message || 'An error occurred',
      details: error.response?.data?.details || null,
      isError: true,
    };

    return Promise.reject(standardError);
  }
);

export default apiClient;
