import React from 'react';

export const SchemeCardSkeleton: React.FC = () => {
  return (
    <div className="bg-white rounded-xl border border-stone-200 p-6 shadow-xs animate-pulse">
      <div className="flex items-center justify-between mb-4">
        <div className="h-6 w-24 bg-stone-200 rounded-md"></div>
        <div className="h-4 w-16 bg-stone-100 rounded-md"></div>
      </div>
      <div className="h-7 w-3/4 bg-stone-200 rounded-md mb-3"></div>
      <div className="space-y-2 mb-6">
        <div className="h-4 bg-stone-100 rounded-md"></div>
        <div className="h-4 w-5/6 bg-stone-100 rounded-md"></div>
      </div>
      <div className="pt-4 border-t border-stone-100 flex items-center justify-between">
        <div className="h-9 w-28 bg-stone-200 rounded-lg"></div>
        <div className="h-9 w-32 bg-emerald-100 rounded-lg"></div>
      </div>
    </div>
  );
};

export const CenterCardSkeleton: React.FC = () => {
  return (
    <div className="bg-white rounded-xl border border-stone-200 p-6 shadow-xs animate-pulse">
      <div className="h-6 w-24 bg-stone-200 rounded-md mb-3"></div>
      <div className="h-7 w-2/3 bg-stone-200 rounded-md mb-2"></div>
      <div className="h-4 w-1/2 bg-stone-100 rounded-md mb-4"></div>
      <div className="space-y-2 mb-6">
        <div className="h-4 bg-stone-100 rounded-md"></div>
        <div className="h-4 w-4/5 bg-stone-100 rounded-md"></div>
      </div>
      <div className="h-9 w-36 bg-emerald-100 rounded-lg"></div>
    </div>
  );
};
