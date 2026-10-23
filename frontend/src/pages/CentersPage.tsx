import React, { useState, useEffect } from 'react';
import {
  Search,
  MapPin,
  Phone,
  Mail,
  Clock,
  ExternalLink,
  RotateCcw,
} from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { api } from '../services/api';
import { CenterSummary, CenterListResponse } from '../types';
import { CenterCardSkeleton } from '../components/common/LoadingSkeleton';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { EmptyState } from '../components/common/EmptyState';
import { Badge } from '../components/common/Badge';

export const CentersPage: React.FC = () => {
  const { language, t } = useLanguage();

  const [searchInput, setSearchInput] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('all');
  const [selectedTaluk, setSelectedTaluk] = useState('all');
  const [selectedType, setSelectedType] = useState('all');

  const [centers, setCenters] = useState<CenterSummary[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [taluks, setTaluks] = useState<string[]>([]);
  const [centerTypes, setCenterTypes] = useState<string[]>([]);

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCenters = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const resp: CenterListResponse = await api.getCenters({
        district: selectedDistrict !== 'all' ? selectedDistrict : undefined,
        taluk: selectedTaluk !== 'all' ? selectedTaluk : undefined,
        center_type: selectedType !== 'all' ? selectedType : undefined,
        query: searchInput.trim() || undefined,
        page_size: 20,
      });

      setCenters(resp.items);
      setDistricts(resp.districts || []);
      setTaluks(resp.taluks || []);
      setCenterTypes(resp.center_types || []);
    } catch (err: any) {
      setError(err.message || 'Could not load service centres from server');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCenters();
  }, [selectedDistrict, selectedTaluk, selectedType]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchCenters();
  };

  const handleClearFilters = () => {
    setSearchInput('');
    setSelectedDistrict('all');
    setSelectedTaluk('all');
    setSelectedType('all');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Page Title */}
      <div>
        <h1 className="text-3xl font-extrabold text-stone-900 tracking-tight">
          {t('centersPageTitle')}
        </h1>
        <p className="mt-1 text-stone-600 text-sm sm:text-base max-w-3xl">
          {t('centersPageSubtitle')}
        </p>
      </div>

      {/* Search & Filter Bar */}
      <div className="bg-white rounded-2xl border border-stone-200 p-6 shadow-2xs space-y-4">
        <form onSubmit={handleSearchSubmit} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-5 h-5 text-stone-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              placeholder={t('searchCentersPlaceholder')}
              className="w-full pl-10 pr-4 py-2.5 text-sm bg-stone-50 border border-stone-200 rounded-xl focus:bg-white focus:border-emerald-600 focus:outline-hidden"
            />
          </div>
          <button
            type="submit"
            className="px-6 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm rounded-xl transition-colors shadow-2xs"
          >
            {t('btnSearch')}
          </button>
        </form>

        {/* Filter Dropdowns */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 border-t border-stone-100">
          {/* District Filter */}
          <div>
            <label className="block text-xs font-bold text-stone-700 mb-1">
              {t('filterDistrict')}
            </label>
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              className="w-full text-xs font-semibold bg-stone-50 border border-stone-200 rounded-lg p-2 text-stone-900 focus:outline-hidden"
            >
              <option value="all">{t('allDistricts')}</option>
              {districts.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
          </div>

          {/* Taluk Filter */}
          <div>
            <label className="block text-xs font-bold text-stone-700 mb-1">
              {t('filterTaluk')}
            </label>
            <select
              value={selectedTaluk}
              onChange={(e) => setSelectedTaluk(e.target.value)}
              className="w-full text-xs font-semibold bg-stone-50 border border-stone-200 rounded-lg p-2 text-stone-900 focus:outline-hidden"
            >
              <option value="all">{t('allTaluks')}</option>
              {taluks.map((tItem) => (
                <option key={tItem} value={tItem}>
                  {tItem}
                </option>
              ))}
            </select>
          </div>

          {/* Centre Type Filter */}
          <div>
            <label className="block text-xs font-bold text-stone-700 mb-1">
              {t('filterType')}
            </label>
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="w-full text-xs font-semibold bg-stone-50 border border-stone-200 rounded-lg p-2 text-stone-900 focus:outline-hidden"
            >
              <option value="all">{t('allTypes')}</option>
              {centerTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Clear Filters Button */}
        {(searchInput || selectedDistrict !== 'all' || selectedTaluk !== 'all' || selectedType !== 'all') && (
          <div className="pt-2 flex justify-end">
            <button
              onClick={handleClearFilters}
              className="inline-flex items-center gap-1.5 text-xs font-bold text-stone-500 hover:text-rose-600 transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              {t('clearFilters')}
            </button>
          </div>
        )}
      </div>

      {/* Results Section */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          <CenterCardSkeleton />
          <CenterCardSkeleton />
          <CenterCardSkeleton />
        </div>
      ) : error ? (
        <ErrorMessage
          title="Could not load centres"
          message={error}
          onRetry={fetchCenters}
        />
      ) : centers.length === 0 ? (
        <EmptyState
          title={t('noCentersFound')}
          description="Try broadening your district or taluk filter to discover authorized government centres."
          actionLabel={t('clearFilters')}
          onAction={handleClearFilters}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          {centers.map((center) => {
            const name = language === 'kn' ? center.name_kn : center.name_en;
            const address = language === 'kn' ? center.address_kn : center.address_en;
            const hours = language === 'kn' ? center.operating_hours_kn : center.operating_hours_en;

            return (
              <div
                key={center.id}
                className="bg-white rounded-2xl border border-stone-200/90 shadow-2xs hover:shadow-md hover:border-emerald-300 transition-all p-4 sm:p-6 flex flex-col justify-between"
              >
                <div className="space-y-3 sm:space-y-4">
                  <div className="flex items-center justify-between gap-2">
                    <Badge variant="primary" size="sm">
                      {center.center_type}
                    </Badge>
                    <span className="text-[11px] sm:text-xs font-bold text-stone-500">
                      {center.district}
                    </span>
                  </div>

                  <h3 className="text-base sm:text-lg font-bold text-stone-900 leading-snug">
                    {name}
                  </h3>

                  <div className="space-y-2 sm:space-y-2.5 text-xs sm:text-sm text-stone-600">
                    {/* Address */}
                    <div className="flex items-start gap-2">
                      <MapPin className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                      <span className="leading-relaxed">{address}</span>
                    </div>

                    {/* Phone */}
                    {center.contact_phone && (
                      <div className="flex items-center gap-2">
                        <Phone className="w-4 h-4 text-stone-400 shrink-0" />
                        <a
                          href={`tel:${center.contact_phone}`}
                          className="text-emerald-800 hover:underline font-semibold"
                        >
                          {center.contact_phone}
                        </a>
                      </div>
                    )}

                    {/* Email */}
                    {center.contact_email && (
                      <div className="flex items-center gap-2">
                        <Mail className="w-4 h-4 text-stone-400 shrink-0" />
                        <span className="truncate">{center.contact_email}</span>
                      </div>
                    )}

                    {/* Hours */}
                    {hours && (
                      <div className="flex items-start gap-2 pt-0.5 text-[11px] sm:text-xs text-stone-500">
                        <Clock className="w-3.5 h-3.5 text-stone-400 shrink-0 mt-0.5" />
                        <span>{hours}</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Directions Button */}
                <div className="pt-3 sm:pt-4 mt-4 sm:mt-6 border-t border-stone-100 flex flex-col xs:flex-row items-stretch xs:items-center justify-between gap-2.5">
                  <span className="text-[11px] sm:text-xs font-semibold text-stone-500">
                    Taluk: {center.taluk}
                  </span>
                  <a
                    href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                      `${center.name_en}, ${center.address_en}`
                    )}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center gap-1.5 px-3 py-2 text-xs font-bold bg-emerald-50 text-emerald-800 hover:bg-emerald-100 rounded-lg transition-colors"
                  >
                    <span>{t('getDirections')}</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
