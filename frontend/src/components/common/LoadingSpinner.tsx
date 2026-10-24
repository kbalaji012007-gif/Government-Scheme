import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  label?: string;
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  label,
  className = '',
}) => {
  const sizeClass = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  }[size];

  return (
    <div className={`flex flex-col items-center justify-center py-8 ${className}`} role="status">
      <Loader2 className={`${sizeClass} animate-spin text-emerald-700`} aria-hidden="true" />
      {label && <p className="mt-3 text-sm text-stone-600 font-medium">{label}</p>}
      <span className="sr-only">{label || 'Loading...'}</span>
    </div>
  );
};
