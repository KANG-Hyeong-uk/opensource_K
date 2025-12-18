/**
 * 고급 에러 처리 유틸리티
 * - 에러 타입별 사용자 친화적 메시지 생성
 * - 에러 분류 및 분석
 * - 재시도 전략
 */

import { logError } from './logger';

/**
 * 에러 타입 정의
 */
export const ERROR_TYPES = {
  NETWORK: 'NETWORK_ERROR',
  AUTHENTICATION: 'AUTHENTICATION_ERROR',
  AUTHORIZATION: 'AUTHORIZATION_ERROR',
  VALIDATION: 'VALIDATION_ERROR',
  SERVER: 'SERVER_ERROR',
  CRAWLER: 'CRAWLER_ERROR',
  LLM: 'LLM_ERROR',
  NOT_FOUND: 'NOT_FOUND_ERROR',
  TIMEOUT: 'TIMEOUT_ERROR',
  UNKNOWN: 'UNKNOWN_ERROR',
};

/**
 * 에러 타입 분류
 * @param {Object} error - 에러 객체
 * @returns {string} 에러 타입
 */
export const classifyError = (error) => {
  // 네트워크 에러
  if (!error.status && error.message?.includes('Network')) {
    return ERROR_TYPES.NETWORK;
  }

  // 상태 코드별 분류
  switch (error.status) {
    case 401:
      return ERROR_TYPES.AUTHENTICATION;
    case 403:
      return ERROR_TYPES.AUTHORIZATION;
    case 404:
      return ERROR_TYPES.NOT_FOUND;
    case 400:
      return ERROR_TYPES.VALIDATION;
    case 408:
    case 504:
      return ERROR_TYPES.TIMEOUT;
    case 502:
      return ERROR_TYPES.CRAWLER;
    case 503:
      return ERROR_TYPES.LLM;
    case 500:
    case 501:
    case 505:
      return ERROR_TYPES.SERVER;
    default:
      return ERROR_TYPES.UNKNOWN;
  }
};

/**
 * 에러 타입별 사용자 메시지 생성
 * @param {string} errorType - 에러 타입
 * @param {Object} error - 에러 객체
 * @returns {string} 사용자 친화적 메시지
 */
export const getUserFriendlyMessage = (errorType, error = {}) => {
  const messages = {
    [ERROR_TYPES.NETWORK]: '인터넷 연결을 확인해주세요.',
    [ERROR_TYPES.AUTHENTICATION]: '로그인이 필요합니다. 다시 로그인해주세요.',
    [ERROR_TYPES.AUTHORIZATION]: '해당 작업을 수행할 권한이 없습니다.',
    [ERROR_TYPES.VALIDATION]: error.userMessage || '입력 정보를 확인해주세요.',
    [ERROR_TYPES.SERVER]: '서버에 일시적인 문제가 발생했습니다. 잠시 후 다시 시도해주세요.',
    [ERROR_TYPES.CRAWLER]: 'URL을 가져오는데 실패했습니다. URL이 정확한지 확인해주세요.',
    [ERROR_TYPES.LLM]: '콘텐츠 분석 서비스가 일시적으로 사용할 수 없습니다. 잠시 후 다시 시도해주세요.',
    [ERROR_TYPES.NOT_FOUND]: '요청하신 정보를 찾을 수 없습니다.',
    [ERROR_TYPES.TIMEOUT]: '요청 시간이 초과되었습니다. 다시 시도해주세요.',
    [ERROR_TYPES.UNKNOWN]: error.userMessage || '알 수 없는 오류가 발생했습니다.',
  };

  return messages[errorType] || messages[ERROR_TYPES.UNKNOWN];
};

/**
 * 에러가 재시도 가능한지 확인
 * @param {string} errorType - 에러 타입
 * @returns {boolean} 재시도 가능 여부
 */
export const isRetryable = (errorType) => {
  const retryableErrors = [
    ERROR_TYPES.NETWORK,
    ERROR_TYPES.TIMEOUT,
    ERROR_TYPES.SERVER,
    ERROR_TYPES.CRAWLER,
    ERROR_TYPES.LLM,
  ];

  return retryableErrors.includes(errorType);
};

/**
 * 종합 에러 처리
 * @param {Object} error - 에러 객체
 * @param {Object} options - 옵션
 * @param {string} options.context - 에러 발생 컨텍스트 (예: 'Login', 'Analysis')
 * @param {boolean} options.silent - 로깅 여부
 * @returns {Object} 처리된 에러 정보
 */
export const handleError = (error, options = {}) => {
  const { context = 'Unknown', silent = false } = options;

  const errorType = classifyError(error);
  const userMessage = getUserFriendlyMessage(errorType, error);
  const retryable = isRetryable(errorType);

  // 로깅
  if (!silent) {
    logError(context, `Error occurred: ${errorType}`, {
      type: errorType,
      status: error.status,
      message: error.message,
      retryable,
    });
  }

  return {
    type: errorType,
    userMessage,
    originalError: error,
    retryable,
    status: error.status,
    details: error.details || null,
    fieldErrors: error.fieldErrors || null,
  };
};

/**
 * 재시도 로직 (Exponential Backoff)
 * @param {Function} fn - 재시도할 함수
 * @param {Object} options - 옵션
 * @param {number} options.maxRetries - 최대 재시도 횟수 (기본값: 3)
 * @param {number} options.initialDelay - 초기 지연 시간 (ms, 기본값: 1000)
 * @param {number} options.maxDelay - 최대 지연 시간 (ms, 기본값: 10000)
 * @param {Function} options.shouldRetry - 재시도 여부 판단 함수
 * @returns {Promise} 함수 실행 결과
 */
export const retryWithBackoff = async (fn, options = {}) => {
  const {
    maxRetries = 3,
    initialDelay = 1000,
    maxDelay = 10000,
    shouldRetry = (error) => isRetryable(classifyError(error)),
  } = options;

  let lastError;
  let delay = initialDelay;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      // 마지막 시도이거나 재시도 불가능한 에러인 경우
      if (attempt === maxRetries || !shouldRetry(error)) {
        throw error;
      }

      // 지연 후 재시도
      logError('Retry', `Attempt ${attempt + 1} failed, retrying in ${delay}ms...`, error);

      await new Promise(resolve => setTimeout(resolve, delay));

      // 지연 시간 증가 (Exponential Backoff)
      delay = Math.min(delay * 2, maxDelay);
    }
  }

  throw lastError;
};

/**
 * 필드 에러 포맷팅
 * @param {Object} fieldErrors - 필드별 에러 객체
 * @returns {Object} 포맷팅된 필드 에러
 */
export const formatFieldErrors = (fieldErrors) => {
  if (!fieldErrors || typeof fieldErrors !== 'object') {
    return {};
  }

  const formatted = {};

  for (const [field, errors] of Object.entries(fieldErrors)) {
    if (Array.isArray(errors)) {
      formatted[field] = errors[0]; // 첫 번째 에러 메시지만 사용
    } else {
      formatted[field] = errors;
    }
  }

  return formatted;
};

/**
 * 에러 알림 표시 헬퍼
 * @param {Object} error - 에러 객체
 * @param {Function} showToast - 토스트 표시 함수
 * @param {Object} options - 옵션
 */
export const showErrorNotification = (error, showToast, options = {}) => {
  const { context = 'Error' } = options;
  const processedError = handleError(error, { context });

  showToast({
    type: 'error',
    message: processedError.userMessage,
    duration: 5000,
  });
};

/**
 * 에러 복구 제안
 * @param {string} errorType - 에러 타입
 * @returns {Array<string>} 복구 방법 제안 목록
 */
export const getRecoverySuggestions = (errorType) => {
  const suggestions = {
    [ERROR_TYPES.NETWORK]: [
      '인터넷 연결 상태를 확인해주세요.',
      'Wi-Fi 또는 모바일 데이터가 켜져 있는지 확인해주세요.',
      'VPN을 사용 중이라면 비활성화해보세요.',
    ],
    [ERROR_TYPES.AUTHENTICATION]: [
      '로그인 페이지로 이동하여 다시 로그인해주세요.',
      '비밀번호를 잊으셨다면 비밀번호 재설정을 이용해주세요.',
    ],
    [ERROR_TYPES.AUTHORIZATION]: [
      '해당 기능을 사용할 권한이 없을 수 있습니다.',
      '관리자에게 문의해주세요.',
    ],
    [ERROR_TYPES.CRAWLER]: [
      'URL이 정확한지 다시 확인해주세요.',
      'URL이 접근 가능한 상태인지 확인해주세요.',
      '잠시 후 다시 시도해주세요.',
    ],
    [ERROR_TYPES.LLM]: [
      'AI 분석 서비스가 일시적으로 과부하 상태일 수 있습니다.',
      '잠시 후 다시 시도해주세요.',
    ],
    [ERROR_TYPES.SERVER]: [
      '서버가 일시적으로 응답하지 않고 있습니다.',
      '잠시 후 다시 시도해주세요.',
      '문제가 지속되면 관리자에게 문의해주세요.',
    ],
    [ERROR_TYPES.TIMEOUT]: [
      '요청 처리 시간이 너무 오래 걸렸습니다.',
      '인터넷 연결 상태를 확인해주세요.',
      '다시 시도해주세요.',
    ],
  };

  return suggestions[errorType] || [
    '잠시 후 다시 시도해주세요.',
    '문제가 계속되면 관리자에게 문의해주세요.',
  ];
};
