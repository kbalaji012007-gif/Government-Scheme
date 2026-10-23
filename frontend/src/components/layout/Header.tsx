import React, { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import {
  Menu,
  X,
  Languages,
  ShieldCheck,
  User as UserIcon,
  LogOut,
  Sparkles,
} from 'lucide-react';
import { useLanguage } from '../../contexts/LanguageContext';
import { useAuth } from '../../contexts/AuthContext';

export const Header: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { language, setLanguage, t } = useLanguage();
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
    setMobileMenuOpen(false);
  };

  const navLinkClass = ({ isActive }: { isActive: boolean }) =>
    `text-sm font-semibold transition-colors px-3 py-2 rounded-lg ${
      isActive
        ? 'text-emerald-800 bg-emerald-50/80 font-bold'
        : 'text-stone-700 hover:text-emerald-800 hover:bg-stone-50'
    }`;

  const mobileNavLinkClass = ({ isActive }: { isActive: boolean }) =>
    `block text-base font-semibold px-4 py-3 rounded-lg transition-colors ${
      isActive
        ? 'text-emerald-800 bg-emerald-50 font-bold'
        : 'text-stone-700 hover:text-emerald-800 hover:bg-stone-50'
    }`;

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-stone-200 shadow-2xs">
      {/* Top Advisory Strip */}
      <div className="bg-[#14532D] text-emerald-100 text-xs py-1.5 px-4 text-center">
        <span className="font-semibold text-white mr-1.5">{t('disclaimerBadge')}:</span>
        <span>{t('brandTagline')}</span>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-18">
          {/* Brand Logo & Name */}
          <Link to="/" className="flex items-center gap-3 group focus:outline-hidden">
            <div className="w-10 h-10 rounded-xl bg-emerald-800 flex items-center justify-center text-white shadow-xs group-hover:bg-emerald-700 transition-colors">
              <ShieldCheck className="w-6 h-6 text-emerald-300" aria-hidden="true" />
            </div>
            <div>
              <span className="text-xl font-extrabold text-stone-900 tracking-tight block">
                {t('brandName')}
              </span>
              <span className="text-xs text-stone-500 font-medium hidden sm:block">
                Karnataka Scheme Discovery Platform
              </span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1 lg:gap-2" aria-label="Main Navigation">
            <NavLink to="/" end className={navLinkClass}>
              {t('navHome')}
            </NavLink>
            <NavLink to="/schemes" className={navLinkClass}>
              {t('navSchemes')}
            </NavLink>
            <NavLink to="/eligibility" className={navLinkClass}>
              {t('navEligibility')}
            </NavLink>
            <NavLink to="/centers" className={navLinkClass}>
              {t('navCenters')}
            </NavLink>
          </nav>

          {/* Language Selector & Auth Desktop */}
          <div className="hidden md:flex items-center gap-3">
            {/* Language Selector */}
            <div className="flex items-center bg-stone-100 p-1 rounded-xl border border-stone-200">
              <Languages className="w-4 h-4 text-stone-500 ml-2 mr-1" aria-hidden="true" />
              <button
                type="button"
                onClick={() => setLanguage('kn')}
                className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
                  language === 'kn'
                    ? 'bg-emerald-700 text-white shadow-xs'
                    : 'text-stone-600 hover:text-stone-900'
                }`}
                aria-label="Switch to Kannada"
              >
                ಕನ್ನಡ
              </button>
              <button
                type="button"
                onClick={() => setLanguage('en')}
                className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
                  language === 'en'
                    ? 'bg-emerald-700 text-white shadow-xs'
                    : 'text-stone-600 hover:text-stone-900'
                }`}
                aria-label="Switch to English"
              >
                English
              </button>
            </div>

            {/* Auth Buttons */}
            {isAuthenticated && user ? (
              <div className="flex items-center gap-2 pl-2 border-l border-stone-200">
                <div className="flex items-center gap-2 text-sm text-stone-700 font-medium">
                  <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold text-xs">
                    {user.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
                  </div>
                  <span className="hidden lg:inline-block max-w-[120px] truncate">
                    {user.full_name}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  title={t('navLogout')}
                  className="p-2 text-stone-500 hover:text-rose-600 hover:bg-stone-100 rounded-lg transition-colors"
                  aria-label={t('navLogout')}
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2 pl-2 border-l border-stone-200">
                <Link
                  to="/login"
                  className="px-3.5 py-2 text-sm font-semibold text-stone-700 hover:text-emerald-800 hover:bg-stone-50 rounded-lg transition-colors"
                >
                  {t('navLogin')}
                </Link>
                <Link
                  to="/register"
                  className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg transition-colors shadow-xs"
                >
                  <Sparkles className="w-3.5 h-3.5" aria-hidden="true" />
                  {t('navRegister')}
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="flex items-center gap-2 md:hidden">
            {/* Quick Language Toggle on Mobile Header */}
            <button
              onClick={() => setLanguage(language === 'kn' ? 'en' : 'kn')}
              className="px-2.5 py-1 text-xs font-bold bg-stone-100 hover:bg-stone-200 text-stone-800 rounded-lg border border-stone-200"
              aria-label="Toggle Language"
            >
              {language === 'kn' ? 'English' : 'ಕನ್ನಡ'}
            </button>

            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition-colors focus:ring-2 focus:ring-emerald-700"
              aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
              aria-expanded={mobileMenuOpen}
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer Overlay & Content */}
      {mobileMenuOpen && (
        <>
          <div
            className="fixed inset-0 top-[100px] bg-stone-900/40 backdrop-blur-xs z-30 md:hidden animate-in fade-in duration-200"
            onClick={() => setMobileMenuOpen(false)}
            aria-hidden="true"
          />
          <div className="relative z-40 md:hidden border-t border-stone-200 bg-white px-4 pt-3 pb-6 space-y-1.5 shadow-xl animate-in slide-in-from-top-2 duration-200">
            <NavLink
              to="/"
              end
              onClick={() => setMobileMenuOpen(false)}
              className={mobileNavLinkClass}
            >
              {t('navHome')}
            </NavLink>
            <NavLink
              to="/schemes"
              onClick={() => setMobileMenuOpen(false)}
              className={mobileNavLinkClass}
            >
              {t('navSchemes')}
            </NavLink>
            <NavLink
              to="/eligibility"
              onClick={() => setMobileMenuOpen(false)}
              className={mobileNavLinkClass}
            >
              {t('navEligibility')}
            </NavLink>
            <NavLink
              to="/centers"
              onClick={() => setMobileMenuOpen(false)}
              className={mobileNavLinkClass}
            >
              {t('navCenters')}
            </NavLink>

            <div className="pt-3 border-t border-stone-200 mt-2 space-y-3">
              {/* Mobile Language Switcher */}
              <div className="flex items-center justify-between px-3.5 py-2.5 bg-stone-50 rounded-xl border border-stone-200">
                <span className="text-xs sm:text-sm font-semibold text-stone-700 flex items-center gap-2">
                  <Languages className="w-4 h-4 text-emerald-700" />
                  Language / ಭಾಷೆ:
                </span>
                <div className="flex gap-1.5">
                  <button
                    onClick={() => setLanguage('kn')}
                    className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-colors ${
                      language === 'kn' ? 'bg-emerald-700 text-white shadow-2xs' : 'bg-stone-200 text-stone-700'
                    }`}
                  >
                    ಕನ್ನಡ
                  </button>
                  <button
                    onClick={() => setLanguage('en')}
                    className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-colors ${
                      language === 'en' ? 'bg-emerald-700 text-white shadow-2xs' : 'bg-stone-200 text-stone-700'
                    }`}
                  >
                    English
                  </button>
                </div>
              </div>

              {/* Mobile Auth */}
              {isAuthenticated && user ? (
                <div className="space-y-2 pt-1">
                  <div className="flex items-center gap-3 px-3.5 py-2.5 bg-stone-50 rounded-xl border border-stone-200">
                    <UserIcon className="w-5 h-5 text-emerald-700 shrink-0" />
                    <span className="font-bold text-stone-800 text-sm truncate">{user.full_name}</span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center justify-center gap-2 px-4 py-3 text-sm font-bold text-rose-700 bg-rose-50 hover:bg-rose-100 rounded-xl transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                    {t('navLogout')}
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-2 gap-2.5 pt-1">
                  <Link
                    to="/login"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex items-center justify-center px-4 py-3 text-sm font-bold text-stone-800 bg-stone-100 hover:bg-stone-200 rounded-xl text-center transition-colors"
                  >
                    {t('navLogin')}
                  </Link>
                  <Link
                    to="/register"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex items-center justify-center px-4 py-3 text-sm font-bold text-white bg-emerald-700 hover:bg-emerald-800 rounded-xl text-center shadow-xs transition-colors"
                  >
                    {t('navRegister')}
                  </Link>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </header>
  );
};
