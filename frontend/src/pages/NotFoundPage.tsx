import React from 'react';
import { Link } from 'react-router-dom';
import { Home, Compass } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

export const NotFoundPage: React.FC = () => {
  const { t } = useLanguage();

  return (
    <div className="min-h-[60vh] flex items-center justify-center px-4 py-16 text-center">
      <div className="max-w-md space-y-6">
        <div className="w-16 h-16 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center mx-auto text-2xl font-black">
          404
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-stone-900">
          Page Not Found
        </h1>
        <p className="text-sm text-stone-600 leading-relaxed">
          The page or scheme discovery link you followed does not exist or has been moved.
        </p>
        <div className="flex items-center justify-center gap-3 pt-2">
          <Link
            to="/"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold bg-emerald-700 hover:bg-emerald-800 text-white transition-colors shadow-2xs"
          >
            <Home className="w-4 h-4" />
            {t('navHome')}
          </Link>
          <Link
            to="/schemes"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold border border-stone-300 bg-white text-stone-700 hover:bg-stone-50 transition-colors"
          >
            <Compass className="w-4 h-4" />
            {t('navSchemes')}
          </Link>
        </div>
      </div>
    </div>
  );
};
