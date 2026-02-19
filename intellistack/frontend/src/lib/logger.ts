/**
 * Client-side error logging utility
 * Logs errors to console in development and sends to monitoring service in production
 */

export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARN = 'warn',
  ERROR = 'error',
}

interface LogContext {
  [key: string]: any;
}

interface LogEntry {
  level: LogLevel;
  message: string;
  context?: LogContext;
  timestamp: string;
  userAgent?: string;
  url?: string;
}

class Logger {
  private isDevelopment: boolean;
  private monitoringEndpoint?: string;

  constructor() {
    this.isDevelopment = process.env.NODE_ENV === 'development';
    this.monitoringEndpoint = process.env.NEXT_PUBLIC_MONITORING_ENDPOINT;
  }

  private createLogEntry(
    level: LogLevel,
    message: string,
    context?: LogContext
  ): LogEntry {
    return {
      level,
      message,
      context,
      timestamp: new Date().toISOString(),
      userAgent: typeof window !== 'undefined' ? window.navigator.userAgent : undefined,
      url: typeof window !== 'undefined' ? window.location.href : undefined,
    };
  }

  private async sendToMonitoring(entry: LogEntry): Promise<void> {
    if (!this.monitoringEndpoint) return;

    try {
      await fetch(this.monitoringEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(entry),
        // Don't block on logging
        keepalive: true,
      });
    } catch (error) {
      // Silently fail - don't want logging errors to break the app
      console.error('Failed to send log to monitoring service:', error);
    }
  }

  private log(level: LogLevel, message: string, context?: LogContext): void {
    const entry = this.createLogEntry(level, message, context);

    // Always log to console in development
    if (this.isDevelopment) {
      const consoleMethod = level === LogLevel.ERROR ? 'error' :
                           level === LogLevel.WARN ? 'warn' :
                           level === LogLevel.INFO ? 'info' : 'log';
      console[consoleMethod](`[${level.toUpperCase()}]`, message, context || '');
    }

    // Send to monitoring service in production for warnings and errors
    if (!this.isDevelopment && (level === LogLevel.WARN || level === LogLevel.ERROR)) {
      this.sendToMonitoring(entry);
    }
  }

  debug(message: string, context?: LogContext): void {
    this.log(LogLevel.DEBUG, message, context);
  }

  info(message: string, context?: LogContext): void {
    this.log(LogLevel.INFO, message, context);
  }

  warn(message: string, context?: LogContext): void {
    this.log(LogLevel.WARN, message, context);
  }

  error(message: string, error?: Error | unknown, context?: LogContext): void {
    const errorContext: LogContext = {
      ...context,
    };

    if (error instanceof Error) {
      errorContext.error = {
        name: error.name,
        message: error.message,
        stack: error.stack,
      };
    } else if (error) {
      errorContext.error = error;
    }

    this.log(LogLevel.ERROR, message, errorContext);
  }

  /**
   * Log API errors with additional context
   */
  apiError(
    endpoint: string,
    method: string,
    error: Error | unknown,
    context?: LogContext
  ): void {
    this.error(`API Error: ${method} ${endpoint}`, error, {
      ...context,
      endpoint,
      method,
    });
  }

  /**
   * Log user actions for analytics
   */
  userAction(action: string, context?: LogContext): void {
    this.info(`User Action: ${action}`, context);
  }

  /**
   * Log performance metrics
   */
  performance(metric: string, value: number, context?: LogContext): void {
    this.info(`Performance: ${metric}`, {
      ...context,
      metric,
      value,
      unit: 'ms',
    });
  }
}

export const logger = new Logger();

/**
 * Global error handler for unhandled errors
 */
if (typeof window !== 'undefined') {
  window.addEventListener('error', (event) => {
    logger.error('Unhandled error', event.error, {
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno,
    });
  });

  window.addEventListener('unhandledrejection', (event) => {
    logger.error('Unhandled promise rejection', event.reason, {
      promise: 'Promise rejection',
    });
  });
}
