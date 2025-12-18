/**
 * URL 분석 관련 API
 * - URL 분석 요청
 * - 분석 이력 조회
 * - 분석 결과 상세 조회
 * - 분석 통계 조회
 */

import apiClient from './client';
import { logInfo, logError } from '../utils/logger';

/**
 * URL 분석
 * @param {string} url - 분석할 URL
 * @returns {Promise<Object>} 분석 결과
 */
export const analyzeUrl = async (url) => {
  try {
    const response = await apiClient.post('/api/v1/analyze/', { url });

    logInfo('Analysis', 'URL analysis successful', { url });

    return {
      success: true,
      message: response.data.message || '분석이 완료되었습니다.',
      result: response.data.data
    };

  } catch (error) {
    logError('Analysis', 'URL analysis failed', error);

    // 에러 타입별 메시지
    let errorMessage = 'URL 분석에 실패했습니다.';

    if (error.status === 400) {
      errorMessage = error.details?.url?.[0] || '올바른 URL을 입력해주세요.';
    } else if (error.status === 500) {
      if (error.message.includes('crawl')) {
        errorMessage = 'URL을 가져오는데 실패했습니다. URL이 정확한지 확인해주세요.';
      } else if (error.message.includes('analyze')) {
        errorMessage = '콘텐츠 분석 중 오류가 발생했습니다.';
      } else {
        errorMessage = '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
      }
    }

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage
    };
  }
};

/**
 * 분석 이력 조회
 * @param {number} limit - 조회 개수 (기본값: 20, 최대: 100)
 * @returns {Promise<Object>} 분석 이력 목록
 */
export const getAnalysisHistory = async (limit = 20) => {
  try {
    const response = await apiClient.get('/api/v1/history/', {
      params: { limit: Math.min(limit, 100) }
    });

    logInfo('Analysis', 'Analysis history fetched', { count: response.data.count });

    return {
      success: true,
      count: response.data.count,
      results: response.data.data
    };

  } catch (error) {
    logError('Analysis', 'Failed to fetch analysis history', error);

    const errorMessage = error.message || '분석 이력을 불러오는데 실패했습니다.';

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage
    };
  }
};

/**
 * 분석 결과 상세 조회
 * @param {number} analysisId - 분석 결과 ID
 * @returns {Promise<Object>} 분석 결과 상세
 */
export const getAnalysisDetail = async (analysisId) => {
  try {
    const response = await apiClient.get(`/api/v1/results/${analysisId}/`);

    logInfo('Analysis', 'Analysis detail fetched', { analysisId });

    return {
      success: true,
      result: response.data.data
    };

  } catch (error) {
    logError('Analysis', 'Failed to fetch analysis detail', error);

    let errorMessage = '분석 결과를 불러오는데 실패했습니다.';

    if (error.status === 404) {
      errorMessage = '분석 결과를 찾을 수 없습니다.';
    } else if (error.status === 403) {
      errorMessage = '해당 분석 결과에 접근할 권한이 없습니다.';
    }

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage
    };
  }
};

/**
 * 분석 통계 조회
 * @returns {Promise<Object>} 분석 통계
 */
export const getAnalysisStatistics = async () => {
  try {
    const response = await apiClient.get('/api/v1/statistics/');

    logInfo('Analysis', 'Analysis statistics fetched');

    return {
      success: true,
      statistics: response.data.data
    };

  } catch (error) {
    logError('Analysis', 'Failed to fetch analysis statistics', error);

    const errorMessage = error.message || '통계 정보를 불러오는데 실패했습니다.';

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage
    };
  }
};

/**
 * 위험도 레벨 텍스트 변환
 * @param {string} riskLevel - 위험도 레벨 (safe, low, medium, high)
 * @returns {string} 한글 위험도
 */
export const getRiskLevelText = (riskLevel) => {
  const riskLevels = {
    safe: '안전',
    low: '낮음',
    medium: '보통',
    high: '높음'
  };

  return riskLevels[riskLevel] || '알 수 없음';
};

/**
 * 위험도 레벨 색상
 * @param {string} riskLevel - 위험도 레벨
 * @returns {string} CSS 클래스명
 */
export const getRiskLevelColor = (riskLevel) => {
  const colors = {
    safe: 'success',   // 초록색
    low: 'info',       // 파란색
    medium: 'warning', // 노란색
    high: 'danger'     // 빨간색
  };

  return colors[riskLevel] || 'secondary';
};

/**
 * 사용자 피드백 제출 (오탐 신고)
 * @param {string} url - 분석된 URL
 * @param {string} reason - 오탐 사유
 * @param {object} analysisResult - 분석 결과
 * @returns {Promise<Object>} 피드백 제출 결과
 */
export const submitFeedback = async (url, reason, analysisResult) => {
  try {
    // reason 매핑 (한글 -> 영문 키)
    const reasonMap = {
      '교육적 맥락': 'educational',
      '인용/보도': 'citation',
      '문맥 오해': 'context_misunderstanding'
    };

    const response = await apiClient.post('/api/v1/feedback/', {
      url,
      reason: reasonMap[reason] || reason,
      analysis_result: analysisResult
    });

    logInfo('Feedback', 'Feedback submitted successfully', { url, reason });

    return {
      success: true,
      message: response.data.message || '피드백이 제출되었습니다.',
      data: response.data.data
    };

  } catch (error) {
    logError('Feedback', 'Failed to submit feedback', error);

    const errorMessage = error.message || '피드백 제출에 실패했습니다.';

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage
    };
  }
};
