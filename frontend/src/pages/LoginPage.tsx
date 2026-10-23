import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { ShieldCheck, Lock, Mail, AlertCircle, ArrowRight } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';
import { signInWithGooglePopup } from '../services/firebase';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export const LoginPage: React.FC = () => {
  const { language, t } = useLanguage();
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isGoogleLoading, setIsGoogleLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const from = (location.state as any)?.from?.pathname || '/';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!email || !password) {
      setErrorMessage('Please provide both email address and password.');
      return;
    }

    setIsLoading(true);
    try {
      const resp = await api.login({ email, password });
      login(resp.access_token, resp.user);
      navigate(from, { replace: true });
    } catch (err: any) {
      setErrorMessage(err.message || 'Login failed. Please verify your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
    setErrorMessage(null);
    setIsGoogleLoading(true);

    try {
      const cred = await signInWithGooglePopup();
      const fbUser = cred.user;

      if (!fbUser.email) {
        throw new Error('Google account must have an associated email address.');
      }

      const idToken = await fbUser.getIdToken();
      const resp = await api.googleAuth({
        id_token: idToken,
        email: fbUser.email,
        full_name: fbUser.displayName || 'Google User',
        uid: fbUser.uid,
        preferred_language: language,
      });

      login(resp.access_token, resp.user);
      navigate(from, { replace: true });
    } catch (err: any) {
      if (err.code === 'auth/popup-closed-by-user') {
        return;
      }
      setErrorMessage(err.message || 'Google sign-in failed. Please ensure Google Auth is enabled in Firebase Console.');
    } finally {
      setIsGoogleLoading(false);
    }
  };

  return (
    <div className="min-h-[75vh] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md bg-white rounded-3xl border border-stone-200 p-8 sm:p-10 shadow-xs space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center mx-auto mb-2">
            <ShieldCheck className="w-6 h-6 text-emerald-700" />
          </div>
          <h1 className="text-2xl font-black text-stone-900 tracking-tight">
            {t('loginTitle')}
          </h1>
          <p className="text-xs sm:text-sm text-stone-600 leading-relaxed">
            {t('loginSubtitle')}
          </p>
        </div>

        {errorMessage && (
          <div className="p-3.5 bg-rose-50 border border-rose-200 rounded-xl text-rose-900 text-xs font-semibold flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Google Sign In Button */}
        <button
          type="button"
          onClick={handleGoogleSignIn}
          disabled={isGoogleLoading || isLoading}
          className="w-full flex items-center justify-center gap-3 py-3 px-4 bg-white hover:bg-stone-50 border border-stone-300 text-stone-700 font-bold text-sm rounded-xl transition-all shadow-xs disabled:opacity-50"
        >
          {isGoogleLoading ? (
            <>
              <LoadingSpinner size="sm" />
              <span>Connecting to Google...</span>
            </>
          ) : (
            <>
              <svg className="w-5 h-5 shrink-0" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.65v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.14z"
                />
                <path
                  fill="#34A853"
                  d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.24v3.15C3.26 21.36 7.33 24 12 24z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.24C.45 8.16 0 9.98 0 12s.45 3.84 1.24 5.42l4.04-3.15z"
                />
                <path
                  fill="#EA4335"
                  d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.24 6.58l4.04 3.15c.95-2.83 3.6-4.98 6.72-4.98z"
                />
              </svg>
              <span>{t('googleSignInBtn')}</span>
            </>
          )}
        </button>

        {/* Divider */}
        <div className="relative flex items-center justify-center">
          <div className="border-t border-stone-200 w-full"></div>
          <span className="bg-white px-3 text-xs uppercase tracking-wider font-bold text-stone-400 absolute">
            {t('orDivider')}
          </span>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-stone-700 mb-1.5">
              {t('emailLabel')}
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-stone-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="citizen@ruralconnect.karnataka.gov.in"
                className="w-full pl-10 pr-4 py-2.5 text-sm bg-stone-50 border border-stone-200 rounded-xl focus:bg-white focus:border-emerald-600 focus:outline-hidden"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-stone-700 mb-1.5">
              {t('passwordLabel')}
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-stone-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2.5 text-sm bg-stone-50 border border-stone-200 rounded-xl focus:bg-white focus:border-emerald-600 focus:outline-hidden"
              />
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={isLoading || isGoogleLoading}
              className="w-full flex items-center justify-center gap-2 py-3 px-4 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm rounded-xl transition-colors shadow-xs disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <LoadingSpinner size="sm" />
                  <span>Signing In...</span>
                </>
              ) : (
                <>
                  <span>{t('signInBtn')}</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </form>

        <div className="pt-4 border-t border-stone-100 text-center text-xs text-stone-600">
          <Link to="/register" className="font-bold text-emerald-800 hover:underline">
            {t('dontHaveAccount')}
          </Link>
        </div>

        {/* Demo Credentials Tip */}
        <div className="bg-stone-50 rounded-xl p-3 border border-stone-200 text-xs text-stone-500 space-y-1">
          <p className="font-bold text-stone-700">Quick Test Credentials:</p>
          <p>Email: <code className="bg-stone-200 px-1 py-0.5 rounded text-stone-800">citizen@ruralconnect.karnataka.gov.in</code></p>
          <p>Password: <code className="bg-stone-200 px-1 py-0.5 rounded text-stone-800">Karnataka@2026</code></p>
        </div>
      </div>
    </div>
  );
};
