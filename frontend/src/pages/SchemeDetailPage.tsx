import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  CheckCircle,
  CheckCircle2,
  Calendar,
  ExternalLink,
  FileText,
  AlertTriangle,
  Users,
  ShieldCheck,
  Building,
} from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { api } from '../services/api';
import { SchemeDetail } from '../types';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { Badge } from '../components/common/Badge';

export const SchemeDetailPage: React.FC = () => {
  const { schemeId } = useParams<{ schemeId: string }>();
  const { language, t } = useLanguage();
  const navigate = useNavigate();

  const [scheme, setScheme] = useState<SchemeDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchScheme = async () => {
    if (!schemeId) return;
    setIsLoading(true);
    setError(null);
    try {
      const data = await api.getSchemeById(schemeId);
      setScheme(data);
    } catch (err: any) {
      setError(err.message || 'Scheme details could not be loaded');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchScheme();
  }, [schemeId]);

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20">
        <LoadingSpinner size="lg" label="Loading scheme details..." />
      </div>
    );
  }

  if (error || !scheme) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 space-y-4">
        <button
          onClick={() => navigate('/schemes')}
          className="inline-flex items-center gap-1.5 text-sm font-semibold text-stone-600 hover:text-emerald-800"
        >
          <ArrowLeft className="w-4 h-4" />
          {t('backToSchemes')}
        </button>
        <ErrorMessage
          title="Scheme Not Found"
          message={error || 'The requested scheme could not be found or is unavailable.'}
          onRetry={fetchScheme}
        />
      </div>
    );
  }

  const title = language === 'kn' ? scheme.name_kn : scheme.name_en;
  const fullDesc = language === 'kn' ? scheme.full_description_kn : scheme.full_description_en;
  const benefits = language === 'kn' ? scheme.benefits_kn : scheme.benefits_en;
  const conditions = language === 'kn' ? scheme.eligibility_conditions_kn : scheme.eligibility_conditions_en;
  const processSteps = language === 'kn' ? scheme.application_process_kn : scheme.application_process_en;
  const beneficiarySummary = language === 'kn' ? scheme.beneficiary_summary_kn : scheme.beneficiary_summary_en;
  const disclaimer = language === 'kn' ? scheme.disclaimer_kn : scheme.disclaimer_en;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10 space-y-6 sm:space-y-8 pb-24 md:pb-12">
      {/* Back Link & Breadcrumb */}
      <div>
        <Link
          to="/schemes"
          className="inline-flex items-center gap-1.5 text-xs sm:text-sm font-bold text-stone-600 hover:text-emerald-800 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          {t('backToSchemes')}
        </Link>
      </div>

      {/* Main Grid: 2 Columns on Laptop / Desktop, Single Column on Mobile */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8 items-start">
        {/* Left Column (Content, 2 cols on lg) */}
        <div className="lg:col-span-2 space-y-6 sm:space-y-8">
          {/* Main Scheme Header Card */}
          <div className="bg-white rounded-2xl sm:rounded-3xl border border-stone-200 p-5 sm:p-8 shadow-xs space-y-4 sm:space-y-6">
            <div className="flex flex-wrap items-center justify-between gap-2.5">
              <Badge variant="primary" size="md">
                {scheme.category.toUpperCase()}
              </Badge>
              {scheme.last_verified_date ? (
                <span className="inline-flex items-center gap-1.5 text-[11px] sm:text-xs text-stone-500 font-medium bg-stone-50 px-2.5 py-1 rounded-full border border-stone-100">
                  <Calendar className="w-3.5 h-3.5 text-stone-400" />
                  {t('lastVerifiedDate')}: {scheme.last_verified_date}
                </span>
              ) : null}
            </div>

            <h1 className="text-xl sm:text-3xl lg:text-4xl font-extrabold text-stone-900 tracking-tight leading-snug">
              {title}
            </h1>

            <p className="text-stone-700 text-sm sm:text-base leading-relaxed">
              {fullDesc}
            </p>

            {/* Beneficiary Banner */}
            <div className="bg-emerald-50/70 border border-emerald-200/80 rounded-2xl p-4 sm:p-5 flex items-start gap-3">
              <Users className="w-5 h-5 text-emerald-800 shrink-0 mt-0.5" />
              <div>
                <h4 className="text-[11px] sm:text-xs font-bold text-emerald-950 uppercase tracking-wider mb-1">
                  {t('eligibleBeneficiaries')}
                </h4>
                <p className="text-xs sm:text-sm text-emerald-900 font-medium leading-relaxed">
                  {beneficiarySummary}
                </p>
              </div>
            </div>
          </div>

          {/* Grid: Benefits & Conditions */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {/* Key Benefits */}
            <div className="bg-white rounded-2xl border border-stone-200 p-5 sm:p-6 shadow-2xs space-y-3 sm:space-y-4">
              <h2 className="text-base sm:text-lg font-bold text-stone-900 tracking-tight flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-700" />
                {t('keyBenefits')}
              </h2>
              {benefits && benefits.length > 0 ? (
                <ul className="space-y-2.5">
                  {benefits.map((benefit, index) => (
                    <li key={index} className="flex items-start gap-2.5 text-xs sm:text-sm text-stone-700 leading-relaxed">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 mt-2 shrink-0"></span>
                      <span>{benefit}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-xs sm:text-sm text-stone-500 italic">Benefits detail not currently available.</p>
              )}
            </div>

            {/* Eligibility Conditions */}
            <div className="bg-white rounded-2xl border border-stone-200 p-5 sm:p-6 shadow-2xs space-y-3 sm:space-y-4">
              <h2 className="text-base sm:text-lg font-bold text-stone-900 tracking-tight flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-emerald-700" />
                {t('eligibilityConditions')}
              </h2>
              {conditions && conditions.length > 0 ? (
                <ul className="space-y-2.5">
                  {conditions.map((cond, index) => (
                    <li key={index} className="flex items-start gap-2.5 text-xs sm:text-sm text-stone-700 leading-relaxed">
                      <span className="w-1.5 h-1.5 rounded-full bg-stone-400 mt-2 shrink-0"></span>
                      <span>{cond}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-xs sm:text-sm text-stone-500 italic">Conditions detail not currently available.</p>
              )}
            </div>
          </div>

          {/* Required Documents Section */}
          <div className="bg-white rounded-2xl border border-stone-200 p-5 sm:p-6 shadow-2xs space-y-4">
            <h2 className="text-base sm:text-lg font-bold text-stone-900 tracking-tight flex items-center gap-2">
              <FileText className="w-5 h-5 text-emerald-700" />
              {t('requiredDocuments')}
            </h2>

            {scheme.required_documents && scheme.required_documents.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
                {scheme.required_documents.map((doc) => {
                  const docName = language === 'kn' ? doc.name_kn : doc.name_en;
                  const docDesc = language === 'kn' ? doc.description_kn : doc.description_en;
                  return (
                    <div
                      key={doc.id}
                      className="p-3.5 rounded-xl border border-stone-200 bg-stone-50/70 flex items-start justify-between gap-3"
                    >
                      <div className="space-y-1">
                        <h4 className="text-xs sm:text-sm font-bold text-stone-900">{docName}</h4>
                        {docDesc && <p className="text-[11px] sm:text-xs text-stone-600 leading-relaxed">{docDesc}</p>}
                      </div>
                      <Badge variant={doc.mandatory ? 'danger' : 'secondary'} size="sm">
                        {doc.mandatory ? t('mandatoryDoc') : t('optionalDoc')}
                      </Badge>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="text-xs sm:text-sm text-stone-500 italic">Document requirements not currently available.</p>
            )}
          </div>

          {/* Step-by-Step Application Process */}
          <div className="bg-white rounded-2xl border border-stone-200 p-5 sm:p-6 shadow-2xs space-y-4">
            <h2 className="text-base sm:text-lg font-bold text-stone-900 tracking-tight flex items-center gap-2">
              <Building className="w-5 h-5 text-emerald-700" />
              {t('applicationProcess')}
            </h2>

            {processSteps && processSteps.length > 0 ? (
              <ol className="space-y-3 sm:space-y-4">
                {processSteps.map((step, idx) => (
                  <li key={idx} className="flex items-start gap-3 sm:gap-4">
                    <span className="w-6 h-6 sm:w-7 sm:h-7 rounded-full bg-emerald-100 text-emerald-800 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                      {idx + 1}
                    </span>
                    <span className="text-xs sm:text-sm text-stone-700 leading-relaxed">{step}</span>
                  </li>
                ))}
              </ol>
            ) : (
              <p className="text-xs sm:text-sm text-stone-500 italic">Application steps not currently available.</p>
            )}
          </div>

          {/* Disclaimer Card */}
          <div className="bg-amber-50/80 border border-amber-200 rounded-2xl p-4 sm:p-5 flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
            <div className="space-y-1 text-xs text-amber-900 leading-relaxed">
              <h4 className="font-bold text-amber-950 uppercase tracking-wider">{t('disclaimerBadge')}</h4>
              <p>{disclaimer || t('disclaimerText')}</p>
            </div>
          </div>
        </div>

        {/* Right Sticky Sidebar (Visible on Laptop / Desktop screens) */}
        <div className="hidden lg:block lg:col-span-1">
          <div className="sticky top-24 bg-white rounded-3xl border border-stone-200 p-6 shadow-sm space-y-5">
            <div className="space-y-2">
              <span className="text-xs font-bold text-emerald-800 uppercase tracking-wider">
                Quick Action • ತ್ವರಿತ ಕ್ರಮ
              </span>
              <h3 className="text-lg font-bold text-stone-900">
                Check Eligibility & Apply
              </h3>
              <p className="text-xs text-stone-600 leading-relaxed">
                Answer few preliminary questions to verify your eligibility for this welfare scheme.
              </p>
            </div>

            <div className="space-y-3 pt-2 border-t border-stone-100">
              <Link
                to={`/eligibility/${scheme.id}`}
                className="w-full inline-flex items-center justify-center gap-2 px-5 py-3.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold rounded-xl transition-colors shadow-xs text-sm"
              >
                <CheckCircle className="w-4 h-4 text-emerald-300" />
                <span>{t('checkEligibilityBtn')}</span>
              </Link>

              {scheme.official_portal_url && (
                <a
                  href={scheme.official_portal_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full inline-flex items-center justify-center gap-2 text-xs font-bold text-stone-700 hover:text-emerald-800 bg-stone-50 hover:bg-stone-100 border border-stone-200 px-4 py-3 rounded-xl transition-colors"
                >
                  <span>{t('officialPortalNotice')}</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}

              <Link
                to="/centers"
                className="w-full inline-flex items-center justify-center gap-2 text-xs font-semibold text-emerald-800 hover:underline pt-1 text-center"
              >
                <span>Need help? Find nearest Seva Kendra</span>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Floating Bottom Sticky Action Bar (Mobile Only) */}
      <div className="fixed bottom-0 left-0 right-0 p-3 bg-white/95 backdrop-blur-md border-t border-stone-200 z-30 shadow-lg lg:hidden flex items-center justify-between gap-3">
        <Link
          to={`/eligibility/${scheme.id}`}
          className="flex-1 inline-flex items-center justify-center gap-2 px-4 py-3 bg-emerald-700 hover:bg-emerald-800 active:scale-[0.98] text-white font-bold rounded-xl text-xs sm:text-sm shadow-xs transition-transform"
        >
          <CheckCircle className="w-4 h-4 text-emerald-300" />
          <span>{t('checkEligibilityBtn')}</span>
        </Link>

        {scheme.official_portal_url && (
          <a
            href={scheme.official_portal_url}
            target="_blank"
            rel="noopener noreferrer"
            className="p-3 bg-stone-100 text-stone-800 rounded-xl hover:bg-stone-200 shrink-0"
            aria-label="Official Portal"
          >
            <ExternalLink className="w-5 h-5 text-stone-700" />
          </a>
        )}
      </div>
    </div>
  );
};
