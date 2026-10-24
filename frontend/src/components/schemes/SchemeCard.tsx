import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle2, Tag, Users } from 'lucide-react';
import { SchemeSummary } from '../../types';
import { useLanguage } from '../../contexts/LanguageContext';
import { Badge } from '../common/Badge';

interface SchemeCardProps {
  scheme: SchemeSummary;
}

export const SchemeCard: React.FC<SchemeCardProps> = ({ scheme }) => {
  const { language, t } = useLanguage();

  const title = language === 'kn' ? scheme.name_kn : scheme.name_en;
  const description = language === 'kn' ? scheme.short_description_kn : scheme.short_description_en;
  const beneficiary = language === 'kn' ? scheme.beneficiary_summary_kn : scheme.beneficiary_summary_en;

  const categoryLabelMap: Record<string, { en: string; kn: string }> = {
    farmers: { en: 'Farmers', kn: 'ರೈತರು' },
    students: { en: 'Students', kn: 'ವಿದ್ಯಾರ್ಥಿಗಳು' },
    women: { en: 'Women', kn: 'ಮಹಿಳೆಯರು' },
    senior_citizens: { en: 'Senior Citizens', kn: 'ಹಿರಿಯ ನಾಗರಿಕರು' },
    rural_families: { en: 'Rural Families', kn: 'ಗ್ರಾಮೀಣ ಕುಟುಂಬಗಳು' },
    other_beneficiaries: { en: 'Other Beneficiaries', kn: 'ಇತರ ಫಲಾನುಭವಿಗಳು' },
    general: { en: 'General', kn: 'ಸಾಮಾನ್ಯ' },
  };

  const catObj = categoryLabelMap[scheme.category] || { en: scheme.category, kn: scheme.category };
  const categoryLabel = language === 'kn' ? catObj.kn : catObj.en;

  return (
    <div className="bg-white rounded-2xl border border-stone-200 shadow-2xs hover:shadow-md hover:border-emerald-300 transition-all duration-200 flex flex-col justify-between p-6">
      <div>
        {/* Category & Status */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <Badge variant="primary" size="sm">
            {categoryLabel}
          </Badge>
          {scheme.tags && scheme.tags.length > 0 && (
            <span className="text-xs text-stone-500 font-medium flex items-center gap-1">
              <Tag className="w-3 h-3 text-stone-400" />
              {scheme.tags[0]}
            </span>
          )}
        </div>

        {/* Title */}
        <h3 className="text-lg font-bold text-stone-900 group-hover:text-emerald-800 transition-colors line-clamp-2 leading-snug mb-2">
          <Link to={`/schemes/${scheme.id}`} className="hover:text-emerald-700">
            {title}
          </Link>
        </h3>

        {/* Short Description */}
        <p className="text-sm text-stone-600 line-clamp-3 leading-relaxed mb-4">
          {description}
        </p>

        {/* Beneficiary Summary */}
        <div className="bg-stone-50 rounded-xl p-3 mb-6 border border-stone-100 flex items-start gap-2.5">
          <Users className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
          <p className="text-xs text-stone-700 font-medium leading-relaxed">
            <span className="font-semibold text-stone-900">{t('eligibleBeneficiaries')}:</span>{' '}
            {beneficiary}
          </p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="pt-4 border-t border-stone-100 flex items-center justify-between gap-3">
        <Link
          to={`/schemes/${scheme.id}`}
          className="inline-flex items-center gap-1 text-sm font-semibold text-stone-700 hover:text-emerald-800 px-3 py-2 rounded-lg hover:bg-stone-100 transition-colors"
        >
          {t('viewDetails')}
          <ArrowRight className="w-4 h-4" />
        </Link>

        <Link
          to={`/eligibility/${scheme.id}`}
          className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-bold bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg transition-colors shadow-2xs"
        >
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-300" />
          {t('checkEligibilityBtn')}
        </Link>
      </div>
    </div>
  );
};
