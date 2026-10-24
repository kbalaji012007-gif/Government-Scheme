import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

interface ErrorMessageProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  className?: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  title = 'Something went wrong',
  message,
  onRetry,
  className = '',
}) => {
  return (
    <div
      role="alert"
      className={`bg-rose-50 border border-rose-200 text-rose-900 rounded-xl p-6 ${className}`}
    >
      <div className="flex items-start gap-4">
        <AlertCircle className="w-6 h-6 text-rose-600 shrink-0 mt-0.5" aria-hidden="true" />
        <div className="flex-1">
          <h3 className="font-semibold text-rose-950 text-base">{title}</h3>
          <p className="mt-1 text-sm text-rose-800 leading-relaxed">{message}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-4 inline-flex items-center gap-2 px-4 py-2 text-sm font-medium bg-rose-600 hover:bg-rose-700 text-white rounded-lg transition-colors focus:ring-2 focus:ring-rose-500 focus:outline-hidden"
            >
              <RefreshCw className="w-4 h-4" aria-hidden="true" />
              Try Again
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
