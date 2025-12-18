/**
 * API 키 관리 API (백엔드 구현 필요)
 *
 * ⚠️ 주의: 이 API는 백엔드에 아직 구현되지 않았습니다.
 * 백엔드 구현 후 사용 가능합니다.
 */

import apiClient from './client';
import { logInfo, logError } from '../utils/logger';

/**
 * API 키 목록 조회
 * @returns {Promise<Object>} API 키 목록
 */
export const getApiKeys = async () => {
  try {
    const response = await apiClient.get('/api/v1/api-keys/');

    logInfo('ApiKeys', 'API keys fetched successfully');

    return {
      success: true,
      keys: response.data.data
    };

  } catch (error) {
    logError('ApiKeys', 'Failed to fetch API keys', error);

    const errorMessage = error.message || 'API 키 목록을 불러오는데 실패했습니다.';

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage
    };
  }
};

/**
 * 새 API 키 생성
 * @param {Object} keyData - API 키 정보
 * @param {string} keyData.name - API 키 이름
 * @param {string} keyData.description - 설명
 * @param {Array<string>} keyData.permissions - 권한 목록
 * @returns {Promise<Object>} 생성된 API 키
 */
export const createApiKey = async (keyData) => {
  try {
    const response = await apiClient.post('/api/v1/api-keys/', keyData);

    logInfo('ApiKeys', 'API key created successfully', { name: keyData.name });

    return {
      success: true,
      message: response.data.message || 'API 키가 생성되었습니다.',
      key: response.data.data
    };

  } catch (error) {
    logError('ApiKeys', 'Failed to create API key', error);

    let errorMessage = 'API 키 생성에 실패했습니다.';
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
 * API 키 수정
 * @param {number} keyId - API 키 ID
 * @param {Object} updateData - 수정할 데이터
 * @returns {Promise<Object>} 수정된 API 키
 */
export const updateApiKey = async (keyId, updateData) => {
  try {
    const response = await apiClient.put(`/api/v1/api-keys/${keyId}/`, updateData);

    logInfo('ApiKeys', 'API key updated successfully', { keyId });

    return {
      success: true,
      message: response.data.message || 'API 키가 수정되었습니다.',
      key: response.data.data
    };

  } catch (error) {
    logError('ApiKeys', 'Failed to update API key', error);

    const errorMessage = error.message || 'API 키 수정에 실패했습니다.';

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage
    };
  }
};

/**
 * API 키 삭제
 * @param {number} keyId - API 키 ID
 * @returns {Promise<Object>} 삭제 결과
 */
export const deleteApiKey = async (keyId) => {
  try {
    const response = await apiClient.delete(`/api/v1/api-keys/${keyId}/`);

    logInfo('ApiKeys', 'API key deleted successfully', { keyId });

    return {
      success: true,
      message: response.data.message || 'API 키가 삭제되었습니다.'
    };

  } catch (error) {
    logError('ApiKeys', 'Failed to delete API key', error);

    let errorMessage = 'API 키 삭제에 실패했습니다.';

    if (error.status === 404) {
      errorMessage = 'API 키를 찾을 수 없습니다.';
    } else if (error.status === 403) {
      errorMessage = '해당 API 키에 대한 권한이 없습니다.';
    }

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage
    };
  }
};

/**
 * API 키 재생성
 * @param {number} keyId - API 키 ID
 * @returns {Promise<Object>} 새로운 API 키
 */
export const regenerateApiKey = async (keyId) => {
  try {
    const response = await apiClient.post(`/api/v1/api-keys/${keyId}/regenerate/`);

    logInfo('ApiKeys', 'API key regenerated successfully', { keyId });

    return {
      success: true,
      message: response.data.message || 'API 키가 재생성되었습니다.',
      key: response.data.data
    };

  } catch (error) {
    logError('ApiKeys', 'Failed to regenerate API key', error);

    const errorMessage = error.message || 'API 키 재생성에 실패했습니다.';

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage
    };
  }
};

/**
 * API 키 사용 통계
 * @param {number} keyId - API 키 ID
 * @param {string} period - 조회 기간 (7d, 30d, 90d)
 * @returns {Promise<Object>} 사용 통계
 */
export const getApiKeyUsage = async (keyId, period = '30d') => {
  try {
    const response = await apiClient.get(`/api/v1/api-keys/${keyId}/usage/`, {
      params: { period }
    });

    logInfo('ApiKeys', 'API key usage fetched successfully', { keyId, period });

    return {
      success: true,
      usage: response.data.data
    };

  } catch (error) {
    logError('ApiKeys', 'Failed to fetch API key usage', error);

    const errorMessage = error.message || 'API 키 사용 통계를 불러오는데 실패했습니다.';

    throw {
      ...error,
      message: errorMessage,
      userMessage: errorMessage
    };
  }
};
