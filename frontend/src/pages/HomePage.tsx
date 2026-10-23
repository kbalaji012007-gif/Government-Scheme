import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Search,
  Tractor,
  GraduationCap,
  HeartHandshake,
  Users,
  Compass,
  CheckCircle,
  MapPin,
  ArrowRight,
  ShieldAlert,
} from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { api } from '../services/api';
import { SchemeSummary } from '../types';
import { SchemeCard } from '../components/schemes/SchemeCard';
import { SchemeCardSkeleton } from '../components/common/LoadingSkeleton';
import { ErrorMessage } from '../components/common/ErrorMessage';

export const HomePage: React.FC = () => {
  const { t } = useLanguage();
  const navigate = useNavigate();

  const [searchQuery, setSearchQuery] = useState('');
  const [featuredSchemes, setFeaturedSchemes] = useState<SchemeSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchFeatured = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const resp = await api.getSchemes({ page_size: 6 });
      setFeaturedSchemes(resp.items);
    } catch (err: any) {
      setError(err.message || 'Failed to load schemes from server');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchFeatured();
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/schemes?query=${encodeURIComponent(searchQuery.trim())}`);
    } else {
      navigate('/schemes');
    }
  };

  return (
    <div className="space-y-12 sm:space-y-20 pb-16">
      {/* ================================================== */}
      {/* B. HERO SECTION                                    */}
      {/* ================================================== */}
      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-900/10 via-emerald-800/5 to-transparent pt-8 pb-12 sm:pt-16 sm:pb-24 px-4 sm:px-6 lg:px-8 border-b border-stone-200/60">
        <div className="max-w-5xl mx-auto text-center space-y-4 sm:space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 sm:px-3.5 sm:py-1.5 rounded-full text-[11px] sm:text-xs font-bold bg-emerald-100 text-emerald-900 border border-emerald-300 shadow-2xs">
            <span className="w-2 h-2 rounded-full bg-emerald-600 animate-ping"></span>
            Public Welfare Discovery • ಜನಹಿತ ಯೋಜನೆಗಳು
          </div>

          <h1 className="text-2xl xs:text-3xl sm:text-5xl lg:text-6xl font-extrabold text-stone-900 tracking-tight leading-tight">
            {t('heroHeadline')}
          </h1>

          <p className="max-w-3xl mx-auto text-sm sm:text-lg text-stone-600 leading-relaxed font-normal px-2">
            {t('heroSubtitle')}
          </p>

          {/* Search Box */}
          <form
            onSubmit={handleSearchSubmit}
            className="max-w-2xl mx-auto mt-6 sm:mt-8 flex flex-col sm:flex-row items-stretch gap-2 bg-white p-2 sm:p-2.5 rounded-2xl shadow-md border border-stone-300/80 focus-within:border-emerald-600 focus-within:ring-3 focus-within:ring-emerald-600/20 transition-all"
          >
            <div className="relative flex-1 flex items-center min-h-[46px]">
              <Search className="w-5 h-5 text-stone-400 ml-3 shrink-0" aria-hidden="true" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={t('searchPlaceholder')}
                className="w-full pl-3 pr-4 py-2 text-stone-900 placeholder-stone-400 text-sm sm:text-base bg-transparent border-0 focus:outline-hidden focus:ring-0"
                aria-label="Search schemes"
              />
            </div>
            <button
              type="submit"
              className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-emerald-700 hover:bg-emerald-800 text-white font-bold rounded-xl transition-colors shadow-xs text-sm sm:text-base"
            >
              <Search className="w-4 h-4" />
              <span>{t('btnSearch')}</span>
            </button>
          </form>

          {/* Quick Action CTA Buttons */}
          <div className="flex flex-col xs:flex-row items-stretch xs:items-center justify-center gap-3 pt-2 sm:pt-4 max-w-md xs:max-w-none mx-auto">
            <Link
              to="/schemes"
              className="inline-flex items-center justify-center gap-2 px-5 py-3 sm:py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-white text-emerald-800 border border-emerald-300 hover:bg-emerald-50 transition-all shadow-2xs"
            >
              <Compass className="w-4 h-4 text-emerald-700" />
              {t('btnBrowseSchemes')}
            </Link>

            <Link
              to="/eligibility"
              className="inline-flex items-center justify-center gap-2 px-5 py-3 sm:py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-emerald-800 hover:bg-emerald-900 text-white transition-all shadow-xs"
            >
              <CheckCircle className="w-4 h-4 text-emerald-300" />
              {t('btnCheckEligibility')}
            </Link>
          </div>
        </div>
      </section>

      {/* ================================================== */}
      {/* C. BENEFICIARY CATEGORIES                          */}
      {/* ================================================== */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-6 sm:mb-10">
          <h2 className="text-xl sm:text-3xl font-bold text-stone-900 tracking-tight">
            {t('categoriesTitle')}
          </h2>
          <p className="mt-1 sm:mt-2 text-stone-600 text-xs sm:text-base">
            {t('categoriesSubtitle')}
          </p>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6">
          {/* Card 1: Farmers */}
          <Link
            to="/schemes?category=farmers"
            className="group bg-white rounded-2xl p-4 sm:p-6 border border-stone-200 shadow-2xs hover:shadow-lg hover:border-emerald-500 transition-all duration-200 flex flex-col justify-between"
          >
            <div>
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center mb-3 sm:mb-4 group-hover:scale-105 transition-transform">
                <Tractor className="w-5 h-5 sm:w-6 sm:h-6" />
              </div>
              <h3 className="text-sm sm:text-lg font-bold text-stone-900 group-hover:text-emerald-800 transition-colors">
                {t('catFarmers')}
              </h3>
              <p className="mt-1.5 sm:mt-2 text-xs sm:text-sm text-stone-600 leading-relaxed line-clamp-2 sm:line-clamp-none">
                {t('catFarmersDesc')}
              </p>
            </div>
            <div className="mt-4 sm:mt-6 flex items-center gap-1 text-[11px] sm:text-xs font-bold text-emerald-700 group-hover:translate-x-1 transition-transform">
              <span>{t('btnBrowseSchemes')}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </Link>

          {/* Card 2: Students */}
          <Link
            to="/schemes?category=students"
            className="group bg-white rounded-2xl p-4 sm:p-6 border border-stone-200 shadow-2xs hover:shadow-lg hover:border-emerald-500 transition-all duration-200 flex flex-col justify-between"
          >
            <div>
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-sky-50 text-sky-700 flex items-center justify-center mb-3 sm:mb-4 group-hover:scale-105 transition-transform">
                <GraduationCap className="w-5 h-5 sm:w-6 sm:h-6" />
              </div>
              <h3 className="text-sm sm:text-lg font-bold text-stone-900 group-hover:text-emerald-800 transition-colors">
                {t('catStudents')}
              </h3>
              <p className="mt-1.5 sm:mt-2 text-xs sm:text-sm text-stone-600 leading-relaxed line-clamp-2 sm:line-clamp-none">
                {t('catStudentsDesc')}
              </p>
            </div>
            <div className="mt-4 sm:mt-6 flex items-center gap-1 text-[11px] sm:text-xs font-bold text-emerald-700 group-hover:translate-x-1 transition-transform">
              <span>{t('btnBrowseSchemes')}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </Link>

          {/* Card 3: Women */}
          <Link
            to="/schemes?category=women"
            className="group bg-white rounded-2xl p-4 sm:p-6 border border-stone-200 shadow-2xs hover:shadow-lg hover:border-emerald-500 transition-all duration-200 flex flex-col justify-between"
          >
            <div>
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-rose-50 text-rose-700 flex items-center justify-center mb-3 sm:mb-4 group-hover:scale-105 transition-transform">
                <HeartHandshake className="w-5 h-5 sm:w-6 sm:h-6" />
              </div>
              <h3 className="text-sm sm:text-lg font-bold text-stone-900 group-hover:text-emerald-800 transition-colors">
                {t('catWomen')}
              </h3>
              <p className="mt-1.5 sm:mt-2 text-xs sm:text-sm text-stone-600 leading-relaxed line-clamp-2 sm:line-clamp-none">
                {t('catWomenDesc')}
              </p>
            </div>
            <div className="mt-4 sm:mt-6 flex items-center gap-1 text-[11px] sm:text-xs font-bold text-emerald-700 group-hover:translate-x-1 transition-transform">
              <span>{t('btnBrowseSchemes')}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </Link>

          {/* Card 4: Other Beneficiaries */}
          <Link
            to="/schemes?category=other_beneficiaries"
            className="group bg-white rounded-2xl p-4 sm:p-6 border border-stone-200 shadow-2xs hover:shadow-lg hover:border-emerald-500 transition-all duration-200 flex flex-col justify-between"
          >
            <div>
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-purple-50 text-purple-700 flex items-center justify-center mb-3 sm:mb-4 group-hover:scale-105 transition-transform">
                <Users className="w-5 h-5 sm:w-6 sm:h-6" />
              </div>
              <h3 className="text-sm sm:text-lg font-bold text-stone-900 group-hover:text-emerald-800 transition-colors">
                {t('catOther')}
              </h3>
              <p className="mt-1.5 sm:mt-2 text-xs sm:text-sm text-stone-600 leading-relaxed line-clamp-2 sm:line-clamp-none">
                {t('catOtherDesc')}
              </p>
            </div>
            <div className="mt-4 sm:mt-6 flex items-center gap-1 text-[11px] sm:text-xs font-bold text-emerald-700 group-hover:translate-x-1 transition-transform">
              <span>{t('btnBrowseSchemes')}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </Link>
        </div>
      </section>

      {/* ================================================== */}
      {/* D. FEATURED SCHEMES                                */}
      {/* ================================================== */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-6 sm:mb-10 gap-3">
          <div>
            <h2 className="text-xl sm:text-3xl font-bold text-stone-900 tracking-tight">
              {t('featuredTitle')}
            </h2>
            <p className="mt-1 text-stone-600 text-xs sm:text-base">
              {t('featuredSubtitle')}
            </p>
          </div>
          <Link
            to="/schemes"
            className="inline-flex items-center gap-1 text-xs sm:text-sm font-bold text-emerald-800 hover:text-emerald-900 shrink-0"
          >
            {t('btnBrowseSchemes')}
            <ArrowRight className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
          </Link>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <SchemeCardSkeleton />
            <SchemeCardSkeleton />
            <SchemeCardSkeleton />
          </div>
        ) : error ? (
          <ErrorMessage
            title="Unable to load featured schemes"
            message={error}
            onRetry={fetchFeatured}
          />
        ) : featuredSchemes.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-2xl border border-stone-200">
            <p className="text-stone-600">{t('noSchemesFound')}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {featuredSchemes.map((scheme) => (
              <SchemeCard key={scheme.id} scheme={scheme} />
            ))}
          </div>
        )}
      </section>

      {/* ================================================== */}
      {/* E. HOW IT WORKS                                    */}
      {/* ================================================== */}
      <section className="bg-stone-100/70 border-y border-stone-200/80 py-10 sm:py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-8 sm:mb-12">
            <h2 className="text-xl sm:text-3xl font-bold text-stone-900 tracking-tight">
              {t('howItWorksTitle')}
            </h2>
            <p className="mt-1 sm:mt-2 text-stone-600 text-xs sm:text-base">
              {t('howItWorksSubtitle')}
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-8">
            <div className="bg-white rounded-2xl p-5 sm:p-6 border border-stone-200/80 shadow-2xs text-center space-y-2.5 sm:space-y-3">
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center font-extrabold text-base sm:text-lg mx-auto">
                1
              </div>
              <h3 className="text-base sm:text-lg font-bold text-stone-900">{t('step1Title')}</h3>
              <p className="text-xs sm:text-sm text-stone-600 leading-relaxed">{t('step1Desc')}</p>
            </div>

            <div className="bg-white rounded-2xl p-5 sm:p-6 border border-stone-200/80 shadow-2xs text-center space-y-2.5 sm:space-y-3">
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center font-extrabold text-base sm:text-lg mx-auto">
                2
              </div>
              <h3 className="text-base sm:text-lg font-bold text-stone-900">{t('step2Title')}</h3>
              <p className="text-xs sm:text-sm text-stone-600 leading-relaxed">{t('step2Desc')}</p>
            </div>

            <div className="bg-white rounded-2xl p-5 sm:p-6 border border-stone-200/80 shadow-2xs text-center space-y-2.5 sm:space-y-3">
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center font-extrabold text-base sm:text-lg mx-auto">
                3
              </div>
              <h3 className="text-base sm:text-lg font-bold text-stone-900">{t('step3Title')}</h3>
              <p className="text-xs sm:text-sm text-stone-600 leading-relaxed">{t('step3Desc')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* ================================================== */}
      {/* F. SERVICE CENTRE SECTION                          */}
      {/* ================================================== */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-emerald-900 text-white rounded-3xl p-6 sm:p-12 shadow-lg relative overflow-hidden flex flex-col md:flex-row items-stretch md:items-center justify-between gap-6 sm:gap-8">
          <div className="space-y-3 sm:space-y-4 max-w-2xl text-left">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] sm:text-xs font-bold bg-emerald-800/90 text-emerald-200 border border-emerald-700">
              <MapPin className="w-3.5 h-3.5" />
              Grama One • Karnataka One • Seva Kendra
            </div>
            <h2 className="text-xl sm:text-3xl font-extrabold tracking-tight">
              {t('centersPromoTitle')}
            </h2>
            <p className="text-emerald-100 text-xs sm:text-base leading-relaxed">
              {t('centersPromoDesc')}
            </p>
          </div>

          <Link
            to="/centers"
            className="inline-flex items-center justify-center gap-2 px-6 py-3.5 bg-white text-emerald-950 font-bold rounded-xl hover:bg-emerald-50 transition-colors shrink-0 shadow-md text-sm sm:text-base w-full sm:w-auto"
          >
            <MapPin className="w-4 h-4 text-emerald-700" />
            <span>{t('btnFindCentres')}</span>
          </Link>
        </div>
      </section>

      {/* ================================================== */}
      {/* G. TRUST AND ACCESSIBILITY SECTION                 */}
      {/* ================================================== */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-2xl border border-stone-200 p-5 sm:p-10 shadow-2xs space-y-3 sm:space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0">
              <ShieldAlert className="w-5 h-5 text-emerald-700" />
            </div>
            <h3 className="text-lg sm:text-xl font-bold text-stone-900 tracking-tight">
              {t('trustTitle')}
            </h3>
          </div>
          <p className="text-stone-700 text-xs sm:text-base leading-relaxed">
            {t('trustDesc')}
          </p>
          <div className="pt-2 text-[11px] sm:text-xs text-stone-500 border-t border-stone-100 flex flex-wrap gap-2 sm:gap-4">
            <span className="font-semibold text-stone-700">Public Note:</span>
            <span>Preliminary guidance only. Official decisions are made by relevant government authorities.</span>
          </div>
        </div>
      </section>
    </div>
  );
};
