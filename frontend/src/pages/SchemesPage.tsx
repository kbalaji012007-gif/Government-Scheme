import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Search, Filter, X, ChevronLeft, ChevronRight, RotateCcw } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { api } from '../services/api';
import { SchemeSummary } from '../types';
import { SchemeCard } from '../components/schemes/SchemeCard';
import { SchemeCardSkeleton } from '../components/common/LoadingSkeleton';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { EmptyState } from '../components/common/EmptyState';

export const SchemesPage: React.FC = () => {
  const { language, t } = useLanguage();
  const [searchParams, setSearchParams] = useSearchParams();

  const queryFromUrl = searchParams.get('query') || '';
  const categoryFromUrl = searchParams.get('category') || 'all';
  const pageFromUrl = parseInt(searchParams.get('page') || '1', 10);

  const [searchInput, setSearchInput] = useState(queryFromUrl);
  const [selectedCategory, setSelectedCategory] = useState(categoryFromUrl);
  const [currentPage, setCurrentPage] = useState(pageFromUrl);

  const [schemes, setSchemes] = useState<SchemeSummary[]>([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Sync state if URL query params change
  useEffect(() => {
    setSearchInput(queryFromUrl);
    setSelectedCategory(categoryFromUrl);
    setCurrentPage(pageFromUrl);
  }, [queryFromUrl, categoryFromUrl, pageFromUrl]);

  const loadSchemes = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const resp = await api.getSchemes({
        category: selectedCategory !== 'all' ? selectedCategory : undefined,
        query: searchInput.trim() || undefined,
        page: currentPage,
        page_size: 9,
      });
      setSchemes(resp.items);
      setTotal(resp.total);
      setTotalPages(resp.total_pages);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch schemes from server');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadSchemes();
  }, [selectedCategory, currentPage]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
    updateUrl(searchInput, selectedCategory, 1);
    loadSchemes();
  };

  const handleCategoryChange = (cat: string) => {
    setSelectedCategory(cat);
    setCurrentPage(1);
    updateUrl(searchInput, cat, 1);
  };

  const handleClearFilters = () => {
    setSearchInput('');
    setSelectedCategory('all');
    setCurrentPage(1);
    setSearchParams({});
  };

  const updateUrl = (q: string, cat: string, page: number) => {
    const params: Record<string, string> = {};
    if (q.trim()) params.query = q.trim();
    if (cat && cat !== 'all') params.category = cat;
    if (page > 1) params.page = page.toString();
    setSearchParams(params);
  };

  const categoryOptions = [
    { id: 'all', en: 'All Categories', kn: 'ಎಲ್ಲಾ ವರ್ಗಗಳು' },
    { id: 'farmers', en: 'Farmers', kn: 'ರೈತರು' },
    { id: 'students', en: 'Students', kn: 'ವಿದ್ಯಾರ್ಥಿಗಳು' },
    { id: 'women', en: 'Women', kn: 'ಮಹಿಳೆಯರು' },
    { id: 'senior_citizens', en: 'Senior Citizens', kn: 'ಹಿರಿಯ ನಾಗರಿಕರು' },
    { id: 'rural_families', en: 'Rural Families', kn: 'ಗ್ರಾಮೀಣ ಕುಟುಂಬಗಳು' },
    { id: 'other_beneficiaries', en: 'Other Beneficiaries', kn: 'ಇತರ ಫಲಾನುಭವಿಗಳು' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-stone-900 tracking-tight">
          {t('navSchemes')}
        </h1>
        <p className="mt-1 text-stone-600 text-sm sm:text-base">
          {t('featuredSubtitle')}
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-2xl border border-stone-200 p-4 sm:p-6 shadow-2xs space-y-4">
        <form onSubmit={handleSearchSubmit} className="flex flex-col sm:flex-row gap-2.5 sm:gap-3">
          <div className="relative flex-1">
            <Search className="w-5 h-5 text-stone-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              placeholder={t('searchPlaceholder')}
              className="w-full pl-10 pr-10 py-2.5 text-sm bg-stone-50 border border-stone-200 rounded-xl focus:bg-white focus:border-emerald-600 focus:outline-hidden"
            />
            {searchInput && (
              <button
                type="button"
                onClick={() => setSearchInput('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-stone-400 hover:text-stone-600"
                aria-label="Clear search text"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
          <button
            type="submit"
            className="px-6 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm rounded-xl transition-colors shadow-2xs"
          >
            {t('btnSearch')}
          </button>
        </form>

        {/* Category Pills (Touch scrollable on mobile, wrapping on laptop) */}
        <div className="pt-2 border-t border-stone-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-1.5 sm:gap-2 overflow-x-auto pb-1.5 sm:pb-0 sm:flex-wrap -mx-2 px-2 sm:mx-0 sm:px-0">
            <span className="text-xs font-semibold text-stone-500 shrink-0 flex items-center gap-1 mr-1">
              <Filter className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Category:</span>
            </span>
            {categoryOptions.map((cat) => (
              <button
                key={cat.id}
                type="button"
                onClick={() => handleCategoryChange(cat.id)}
                className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all shrink-0 whitespace-nowrap ${
                  selectedCategory === cat.id
                    ? 'bg-emerald-700 text-white shadow-2xs'
                    : 'bg-stone-100 text-stone-700 hover:bg-stone-200'
                }`}
              >
                {language === 'kn' ? cat.kn : cat.en}
              </button>
            ))}
          </div>

          {(searchInput || selectedCategory !== 'all') && (
            <button
              onClick={handleClearFilters}
              className="inline-flex items-center gap-1.5 text-xs font-bold text-stone-500 hover:text-rose-600 transition-colors py-1 shrink-0 self-start sm:self-auto"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              {t('clearFilters')}
            </button>
          )}
        </div>
      </div>

      {/* Results Count */}
      {!isLoading && !error && (
        <div className="flex items-center justify-between text-xs sm:text-sm text-stone-500">
          <p>
            Showing <span className="font-semibold text-stone-900">{schemes.length}</span> of{' '}
            <span className="font-semibold text-stone-900">{total}</span> schemes
          </p>
          {totalPages > 1 && (
            <p>
              Page <span className="font-semibold text-stone-900">{currentPage}</span> of{' '}
              <span className="font-semibold text-stone-900">{totalPages}</span>
            </p>
          )}
        </div>
      )}

      {/* Main Content Area */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <SchemeCardSkeleton />
          <SchemeCardSkeleton />
          <SchemeCardSkeleton />
          <SchemeCardSkeleton />
          <SchemeCardSkeleton />
          <SchemeCardSkeleton />
        </div>
      ) : error ? (
        <ErrorMessage
          title="Could not load schemes"
          message={error}
          onRetry={loadSchemes}
        />
      ) : schemes.length === 0 ? (
        <EmptyState
          title={t('noSchemesFound')}
          description="Try removing keywords or selecting 'All Categories' to discover more welfare programs."
          actionLabel={t('clearFilters')}
          onAction={handleClearFilters}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {schemes.map((scheme) => (
            <SchemeCard key={scheme.id} scheme={scheme} />
          ))}
        </div>
      )}

      {/* Pagination Controls */}
      {!isLoading && !error && totalPages > 1 && (
        <div className="flex items-center justify-center gap-3 pt-6 border-t border-stone-200">
          <button
            onClick={() => {
              const prev = Math.max(1, currentPage - 1);
              setCurrentPage(prev);
              updateUrl(searchInput, selectedCategory, prev);
            }}
            disabled={currentPage <= 1}
            className="inline-flex items-center gap-1 px-4 py-2 text-sm font-semibold rounded-xl border border-stone-300 bg-white text-stone-700 hover:bg-stone-50 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="w-4 h-4" />
            Previous
          </button>

          <span className="text-sm font-semibold text-stone-700 px-3">
            {currentPage} / {totalPages}
          </span>

          <button
            onClick={() => {
              const next = Math.min(totalPages, currentPage + 1);
              setCurrentPage(next);
              updateUrl(searchInput, selectedCategory, next);
            }}
            disabled={currentPage >= totalPages}
            className="inline-flex items-center gap-1 px-4 py-2 text-sm font-semibold rounded-xl border border-stone-300 bg-white text-stone-700 hover:bg-stone-50 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Next
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
};
