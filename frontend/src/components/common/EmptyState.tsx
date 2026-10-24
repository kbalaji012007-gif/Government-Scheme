import React from 'react';
import { SearchX } from 'lucide-react';

interface EmptyStateProps {
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  description,
  actionLabel,
  onAction,
  className = '',
}) => {
  return (
    <div className={`text-center py-16 px-4 bg-white rounded-2xl border border-stone-200 ${className}`}>
      <div className="w-16 h-16 bg-stone-100 rounded-full flex items-center justify-center mx-auto mb-4 text-stone-500">
        <SearchX className="w-8 h-8" aria-hidden="true" />
      </div>
      <h3 className="text-lg font-bold text-stone-900">{title}</h3>
      <p className="mt-2 text-sm text-stone-600 max-w-md mx-auto leading-relaxed">{description}</p>
      {actionLabel && onAction && (
        <button
          onClick={onAction}
          className="mt-6 inline-flex items-center justify-center px-4 py-2 text-sm font-medium bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg transition-colors focus:ring-2 focus:ring-emerald-600 focus:outline-hidden"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
};
