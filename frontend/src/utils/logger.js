/**
 * 로깅 유틸리티
 * API 요청/응답 및 에러 추적을 위한 로거
 */

const isDevelopment = import.meta.env.MODE === 'development';

/**
 * 로그 레벨
 */
const LOG_LEVELS = {
  DEBUG: 'DEBUG',
  INFO: 'INFO',
  WARN: 'WARN',
  ERROR: 'ERROR',
};

/**
 * 로그 포맷팅
 */
const formatLog = (level, category, message, data = null) => {
  const timestamp = new Date().toISOString();
  const prefix = `[${timestamp}] [${level}] [${category}]`;

  if (data) {
    return `${prefix} ${message}`;
  }
  return `${prefix} ${message}`;
};

/**
 * Debug 로그
 */
export const logDebug = (category, message, data = null) => {
  if (!isDevelopment) return;

  const log = formatLog(LOG_LEVELS.DEBUG, category, message, data);
  console.log(log, data || '');
};

/**
 * Info 로그
 */
export const logInfo = (category, message, data = null) => {
  if (!isDevelopment) return;

  const log = formatLog(LOG_LEVELS.INFO, category, message, data);
  console.info(log, data || '');
};

/**
 * Warning 로그
 */
export const logWarn = (category, message, data = null) => {
  const log = formatLog(LOG_LEVELS.WARN, category, message, data);
  console.warn(log, data || '');
};

/**
 * Error 로그
 */
export const logError = (category, message, error = null) => {
  const log = formatLog(LOG_LEVELS.ERROR, category, message, error);
  console.error(log, error || '');

  // 운영 환경에서는 에러 트래킹 서비스로 전송 가능
  // 예: Sentry.captureException(error);
};

/**
 * API 요청 로그
 */
export const logApiRequest = (method, url, data = null) => {
  logDebug('API', `${method.toUpperCase()} ${url}`, data);
};

/**
 * API 응답 로그
 */
export const logApiResponse = (method, url, status, data = null) => {
  logDebug('API', `${method.toUpperCase()} ${url} - ${status}`, data);
};

/**
 * API 에러 로그
 */
export const logApiError = (method, url, error) => {
  const errorData = {
    status: error.response?.status,
    statusText: error.response?.statusText,
    message: error.message,
    data: error.response?.data,
  };

  logError('API', `${method.toUpperCase()} ${url} - Failed`, errorData);
};
