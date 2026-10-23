import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Info, MapPin, AlertTriangle } from 'lucide-react';
import { useLanguage } from '../../contexts/LanguageContext';

export const Footer: React.FC = () => {
  const { t } = useLanguage();

  return (
    <footer className="bg-stone-900 text-stone-300 pt-10 sm:pt-16 pb-10 sm:pb-12 border-t border-stone-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 sm:gap-10 mb-8 sm:mb-12">
          {/* Col 1: Brand & Description */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
                <ShieldCheck className="w-5 h-5 text-emerald-100" />
              </div>
              <span className="text-lg font-bold text-white tracking-tight">
                {t('brandName')}
              </span>
            </div>
            <p className="text-sm text-stone-400 leading-relaxed">
              {t('footerAboutDesc')}
            </p>
            <div className="pt-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                Karnataka Public Welfare Discovery
              </span>
            </div>
          </div>

          {/* Col 2: Quick Links */}
          <div>
            <h4 className="text-white text-sm font-bold uppercase tracking-wider mb-4">
              {t('footerQuickLinks')}
            </h4>
            <ul className="space-y-2.5 text-sm">
              <li>
                <Link to="/" className="text-stone-400 hover:text-emerald-400 transition-colors">
                  {t('navHome')}
                </Link>
              </li>
              <li>
                <Link to="/schemes" className="text-stone-400 hover:text-emerald-400 transition-colors">
                  {t('navSchemes')}
                </Link>
              </li>
              <li>
                <Link to="/eligibility" className="text-stone-400 hover:text-emerald-400 transition-colors">
                  {t('navEligibility')}
                </Link>
              </li>
              <li>
                <Link to="/centers" className="text-stone-400 hover:text-emerald-400 transition-colors">
                  {t('navCenters')}
                </Link>
              </li>
            </ul>
          </div>

          {/* Col 3: Beneficiary Categories */}
          <div>
            <h4 className="text-white text-sm font-bold uppercase tracking-wider mb-4">
              {t('categoriesTitle')}
            </h4>
            <ul className="space-y-2.5 text-sm">
              <li>
                <Link to="/schemes?category=farmers" className="text-stone-400 hover:text-emerald-400 transition-colors">
                  {t('catFarmers')}
                </Link>
              </li>
              <li>
                <Link to="/schemes?category=students" className="text-stone-400 hover:text-emerald-400 transition-colors">
                  {t('catStudents')}
                </Link>
              </li>
              <li>
                <Link to="/schemes?category=women" className="text-stone-400 hover:text-emerald-400 transition-colors">
                  {t('catWomen')}
                </Link>
              </li>
              <li>
                <Link to="/schemes?category=other_beneficiaries" className="text-stone-400 hover:text-emerald-400 transition-colors">
                  {t('catOther')}
                </Link>
              </li>
            </ul>
          </div>

          {/* Col 4: Public Guidance Advisory */}
          <div className="space-y-3">
            <h4 className="text-white text-sm font-bold uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              {t('disclaimerBadge')}
            </h4>
            <div className="bg-stone-800/80 p-4 rounded-xl border border-stone-700/60 text-xs text-stone-300 leading-relaxed space-y-2">
              <p>{t('disclaimerText')}</p>
              <p className="text-stone-400">
                Official applications are processed via authorized Grama One, Seva Sindhu, or designated department portals.
              </p>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 mt-8 border-t border-stone-800 flex flex-col sm:flex-row items-center justify-between text-xs text-stone-500 gap-4">
          <p>© {new Date().getFullYear()} {t('copyright')}</p>
          <div className="flex items-center gap-6">
            <span className="flex items-center gap-1">
              <Info className="w-3.5 h-3.5 text-emerald-400" />
              Bilingual (ಕನ್ನಡ / English)
            </span>
            <span className="flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5 text-emerald-400" />
              Serving All 31 Districts
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};
