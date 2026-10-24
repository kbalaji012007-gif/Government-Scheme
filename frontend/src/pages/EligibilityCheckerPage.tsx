import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle,
  XCircle,
  HelpCircle,
  AlertTriangle,
  RotateCcw,
  FileCheck2,
  ListChecks,
  CheckCircle2,
  ChevronRight,
} from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { api } from '../services/api';
import {
  SchemeSummary,
  SchemeEligibilityConfigResponse,
  CheckEligibilityResponse,
  EligibilityQuestion,
} from '../types';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { Badge } from '../components/common/Badge';

export const EligibilityCheckerPage: React.FC = () => {
  const { schemeId: urlSchemeId } = useParams<{ schemeId?: string }>();
  const { language, t } = useLanguage();
  const navigate = useNavigate();

  // Selected scheme state
  const [availableSchemes, setAvailableSchemes] = useState<SchemeSummary[]>([]);
  const [selectedSchemeId, setSelectedSchemeId] = useState<string>(urlSchemeId || '');
  const [config, setConfig] = useState<SchemeEligibilityConfigResponse | null>(null);

  // Workflow step state: 0 to (questions.length - 1) = Question step;
  // step == questions.length = Review step;
  // step == questions.length + 1 = Results step.
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [validationError, setValidationError] = useState<string | null>(null);

  // Evaluation submission state
  const [isEvaluating, setIsEvaluating] = useState<boolean>(false);
  const [evaluationResult, setEvaluationResult] = useState<CheckEligibilityResponse | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);
  const [isLoadingConfig, setIsLoadingConfig] = useState<boolean>(true);

  // 1. Fetch available schemes list for selector dropdown
  useEffect(() => {
    const loadSchemesList = async () => {
      try {
        const resp = await api.getSchemes({ page_size: 50 });
        setAvailableSchemes(resp.items);
        if (!selectedSchemeId && resp.items.length > 0) {
          setSelectedSchemeId(resp.items[0].id);
        }
      } catch (err: any) {
        setApiError(err.message || 'Failed to load schemes list');
      }
    };
    loadSchemesList();
  }, []);

  // 2. Fetch eligibility questions whenever selectedSchemeId changes
  useEffect(() => {
    if (!selectedSchemeId) return;

    const loadQuestions = async () => {
      setIsLoadingConfig(true);
      setApiError(null);
      setEvaluationResult(null);
      setCurrentStep(0);
      setAnswers({});
      setValidationError(null);

      try {
        const data = await api.getEligibilityQuestions(selectedSchemeId);
        setConfig(data);
      } catch (err: any) {
        setApiError(err.message || 'Failed to load eligibility questionnaire for this scheme');
      } finally {
        setIsLoadingConfig(false);
      }
    };

    loadQuestions();
  }, [selectedSchemeId]);

  const questions = config?.questions || [];
  const currentQuestion: EligibilityQuestion | undefined = questions[currentStep];
  const isReviewStep = questions.length > 0 && currentStep === questions.length;
  const isResultStep = !!evaluationResult;

  // Handle input changes
  const handleAnswerChange = (val: any) => {
    if (!currentQuestion) return;
    setValidationError(null);
    setAnswers((prev) => ({
      ...prev,
      [currentQuestion.id]: val,
    }));
  };

  // Step navigation & validation
  const handleNext = () => {
    if (!currentQuestion) return;

    const val = answers[currentQuestion.id];
    if (currentQuestion.mandatory && (val === undefined || val === null || val === '')) {
      setValidationError(
        language === 'kn'
          ? 'ದಯವಿಟ್ಟು ಮುಂದುವರಿಯುವ ಮೊದಲು ಈ ಪ್ರಶ್ನೆಗೆ ಉತ್ತರಿಸಿ.'
          : 'Please provide an answer before continuing.'
      );
      return;
    }

    setValidationError(null);
    setCurrentStep((prev) => prev + 1);
  };

  const handleBack = () => {
    setValidationError(null);
    setCurrentStep((prev) => Math.max(0, prev - 1));
  };

  // Submit answers to FastAPI backend
  const handleSubmitEvaluation = async () => {
    if (!selectedSchemeId) return;
    setIsEvaluating(true);
    setApiError(null);

    try {
      const result = await api.checkEligibility(selectedSchemeId, answers);
      setEvaluationResult(result);
      setCurrentStep(questions.length + 1);
    } catch (err: any) {
      setApiError(err.message || 'An error occurred during eligibility verification');
    } finally {
      setIsEvaluating(false);
    }
  };

  const handleRestart = () => {
    setAnswers({});
    setCurrentStep(0);
    setEvaluationResult(null);
    setValidationError(null);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-stone-900 tracking-tight">
            {t('eligibilityTitle')}
          </h1>
          <p className="mt-1 text-sm text-stone-600">
            {t('eligibilityIntro')}
          </p>
        </div>

        {/* Scheme Selector */}
        {availableSchemes.length > 0 && !isResultStep && (
          <div className="w-full sm:w-72">
            <label htmlFor="scheme-picker" className="block text-xs font-bold text-stone-700 mb-1">
              Selected Scheme:
            </label>
            <select
              id="scheme-picker"
              value={selectedSchemeId}
              onChange={(e) => {
                setSelectedSchemeId(e.target.value);
                navigate(`/eligibility/${e.target.value}`, { replace: true });
              }}
              className="w-full text-xs font-semibold bg-white border border-stone-300 rounded-xl px-3 py-2 text-stone-900 focus:border-emerald-600 focus:outline-hidden"
            >
              {availableSchemes.map((s) => (
                <option key={s.id} value={s.id}>
                  {language === 'kn' ? s.name_kn : s.name_en}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Global Error Banner */}
      {apiError && (
        <ErrorMessage
          title="Eligibility Check Error"
          message={apiError}
          onRetry={() => {
            if (isReviewStep) handleSubmitEvaluation();
            else setSelectedSchemeId((s) => s);
          }}
        />
      )}

      {/* Loading state for questions config */}
      {isLoadingConfig ? (
        <div className="py-16 bg-white rounded-3xl border border-stone-200">
          <LoadingSpinner size="md" label="Loading scheme eligibility criteria..." />
        </div>
      ) : questions.length === 0 ? (
        <div className="bg-white rounded-3xl border border-stone-200 p-8 text-center space-y-4">
          <HelpCircle className="w-12 h-12 text-stone-400 mx-auto" />
          <h3 className="text-lg font-bold text-stone-900">Eligibility rules being configured</h3>
          <p className="text-sm text-stone-600 max-w-md mx-auto">
            Direct criteria questions for this scheme are currently being updated by the department.
          </p>
          <Link
            to={`/schemes/${selectedSchemeId}`}
            className="inline-flex items-center gap-1.5 text-sm font-bold text-emerald-800 hover:underline"
          >
            {t('viewSchemeDetailsBtn')}
            <ChevronRight className="w-4 h-4" />
          </Link>
        </div>
      ) : isResultStep && evaluationResult ? (
        /* ================================================== */
        /* RESULTS VIEW                                       */
        /* ================================================== */
        <div className="space-y-8 animate-in fade-in duration-300">
          {/* Result Status Banner */}
          <div
            className={`rounded-3xl p-6 sm:p-10 border shadow-xs ${
              evaluationResult.status === 'eligible'
                ? 'bg-emerald-50 border-emerald-300 text-emerald-950'
                : evaluationResult.status === 'not_eligible'
                ? 'bg-rose-50 border-rose-300 text-rose-950'
                : 'bg-amber-50 border-amber-300 text-amber-950'
            }`}
          >
            <div className="flex items-start gap-4 sm:gap-5">
              {evaluationResult.status === 'eligible' ? (
                <div className="w-12 h-12 rounded-2xl bg-emerald-600 text-white flex items-center justify-center shrink-0">
                  <CheckCircle className="w-7 h-7" />
                </div>
              ) : evaluationResult.status === 'not_eligible' ? (
                <div className="w-12 h-12 rounded-2xl bg-rose-600 text-white flex items-center justify-center shrink-0">
                  <XCircle className="w-7 h-7" />
                </div>
              ) : (
                <div className="w-12 h-12 rounded-2xl bg-amber-500 text-white flex items-center justify-center shrink-0">
                  <AlertTriangle className="w-7 h-7" />
                </div>
              )}

              <div className="space-y-2">
                <span className="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-white/70 border border-current">
                  {language === 'kn' ? evaluationResult.status_title_kn : evaluationResult.status_title_en}
                </span>
                <h2 className="text-xl sm:text-2xl font-black">
                  {language === 'kn' ? evaluationResult.scheme_name_kn : evaluationResult.scheme_name_en}
                </h2>
                <p className="text-sm sm:text-base leading-relaxed opacity-95">
                  {language === 'kn' ? evaluationResult.summary_kn : evaluationResult.summary_en}
                </p>
              </div>
            </div>
          </div>

          {/* Reasons / Explanation Section */}
          <div className="bg-white rounded-2xl border border-stone-200 p-6 sm:p-8 shadow-2xs space-y-4">
            <h3 className="text-base sm:text-lg font-bold text-stone-900 flex items-center gap-2">
              <ListChecks className="w-5 h-5 text-emerald-700" />
              Preliminary Verification Reasons
            </h3>
            <ul className="space-y-2.5 text-sm text-stone-700">
              {(language === 'kn' ? evaluationResult.reasons_kn : evaluationResult.reasons_en).map((reason, idx) => (
                <li key={idx} className="flex items-start gap-3">
                  <span className="w-2 h-2 rounded-full bg-emerald-600 mt-2 shrink-0"></span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Unmet Criteria (If Not Eligible) */}
          {evaluationResult.missing_requirements && evaluationResult.missing_requirements.length > 0 && (
            <div className="bg-rose-50/60 rounded-2xl border border-rose-200 p-6 sm:p-8 shadow-2xs space-y-4">
              <h3 className="text-base sm:text-lg font-bold text-rose-950 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-rose-600" />
                {t('unmetRequirementsTitle')}
              </h3>
              <div className="space-y-2">
                {evaluationResult.missing_requirements.map((req, idx) => (
                  <div key={idx} className="p-3 bg-white rounded-xl border border-rose-200 text-sm text-rose-900">
                    {language === 'kn' ? req.message_kn : req.message_en}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Document Checklist (If Eligible) */}
          {evaluationResult.document_checklist && evaluationResult.document_checklist.length > 0 && (
            <div className="bg-white rounded-2xl border border-stone-200 p-6 sm:p-8 shadow-2xs space-y-4">
              <h3 className="text-base sm:text-lg font-bold text-stone-900 flex items-center gap-2">
                <FileCheck2 className="w-5 h-5 text-emerald-700" />
                {t('documentChecklistTitle')}
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {evaluationResult.document_checklist.map((doc) => (
                  <div key={doc.id} className="p-3.5 bg-stone-50 rounded-xl border border-stone-200 text-xs sm:text-sm">
                    <span className="font-bold text-stone-900 block mb-0.5">
                      {language === 'kn' ? doc.name_kn : doc.name_en}
                    </span>
                    <span className="text-stone-600 block text-xs">
                      {language === 'kn' ? doc.description_kn : doc.description_en}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Next Steps */}
          {evaluationResult.next_steps_en && (
            <div className="bg-stone-50 rounded-2xl border border-stone-200 p-6 sm:p-8 space-y-4">
              <h3 className="text-base sm:text-lg font-bold text-stone-900">
                {t('nextStepsTitle')}
              </h3>
              <ol className="space-y-3">
                {(language === 'kn' ? evaluationResult.next_steps_kn : evaluationResult.next_steps_en).map((step, idx) => (
                  <li key={idx} className="flex items-start gap-3 text-sm text-stone-700">
                    <span className="w-6 h-6 rounded-full bg-emerald-700 text-white font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                      {idx + 1}
                    </span>
                    <span>{step}</span>
                  </li>
                ))}
              </ol>
            </div>
          )}

          {/* Preliminary Notice Disclaimer */}
          <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-900 flex items-start gap-3">
            <AlertTriangle className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
            <p>
              {language === 'kn'
                ? evaluationResult.preliminary_notice_kn
                : evaluationResult.preliminary_notice_en}
            </p>
          </div>

          {/* Action Buttons */}
          <div className="pt-4 flex flex-wrap items-center justify-between gap-4">
            <button
              onClick={handleRestart}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold border border-stone-300 bg-white text-stone-700 hover:bg-stone-50 transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
              {t('recheckBtn')}
            </button>

            <Link
              to={`/schemes/${selectedSchemeId}`}
              className="inline-flex items-center gap-2 px-6 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm rounded-xl transition-colors shadow-2xs"
            >
              <span>{t('viewSchemeDetailsBtn')}</span>
              <ChevronRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      ) : isReviewStep ? (
        /* ================================================== */
        /* REVIEW ANSWERS STEP                                */
        /* ================================================== */
        <div className="bg-white rounded-3xl border border-stone-200 p-6 sm:p-10 shadow-xs space-y-8 animate-in fade-in duration-200">
          <div>
            <Badge variant="primary" size="sm" className="mb-2">
              Step {questions.length + 1} of {questions.length + 1}
            </Badge>
            <h2 className="text-xl sm:text-2xl font-extrabold text-stone-900 tracking-tight">
              {t('reviewAnswersTitle')}
            </h2>
            <p className="mt-1 text-sm text-stone-600">
              Please ensure your answers match your official documents before submitting for verification.
            </p>
          </div>

          <div className="space-y-4 divide-y divide-stone-100">
            {questions.map((q, idx) => {
              const qText = language === 'kn' ? q.question_kn : q.question_en;
              const val = answers[q.id];
              let displayVal = 'Not answered';
              if (val === true || val === 'true') displayVal = language === 'kn' ? 'ಹೌದು (Yes)' : 'Yes';
              else if (val === false || val === 'false') displayVal = language === 'kn' ? 'ಇಲ್ಲ (No)' : 'No';
              else if (val !== undefined && val !== null && val !== '') displayVal = String(val);

              return (
                <div key={q.id} className="pt-4 first:pt-0 flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <span className="text-xs font-semibold text-stone-500">
                      Question {idx + 1}
                    </span>
                    <p className="text-sm font-bold text-stone-900">{qText}</p>
                    <p className="text-sm font-semibold text-emerald-800 bg-emerald-50 inline-block px-2.5 py-0.5 rounded-md">
                      {displayVal}
                    </p>
                  </div>
                  <button
                    onClick={() => setCurrentStep(idx)}
                    className="text-xs font-bold text-stone-500 hover:text-emerald-700 p-1.5 rounded-md hover:bg-stone-100 shrink-0"
                  >
                    {t('editAnswer')}
                  </button>
                </div>
              );
            })}
          </div>

          {/* Action Buttons */}
          <div className="pt-6 border-t border-stone-100 flex items-center justify-between gap-4">
            <button
              onClick={handleBack}
              disabled={isEvaluating}
              className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl text-sm font-bold border border-stone-300 bg-white text-stone-700 hover:bg-stone-50 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              {t('btnBack')}
            </button>

            <button
              onClick={handleSubmitEvaluation}
              disabled={isEvaluating}
              className="inline-flex items-center gap-2 px-7 py-3 bg-emerald-700 hover:bg-emerald-800 text-white font-extrabold text-sm rounded-xl transition-colors shadow-xs disabled:opacity-50"
            >
              {isEvaluating ? (
                <>
                  <LoadingSpinner size="sm" />
                  <span>Evaluating...</span>
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-4 h-4 text-emerald-300" />
                  <span>{t('btnSubmitCheck')}</span>
                </>
              )}
            </button>
          </div>
        </div>
      ) : currentQuestion ? (
        /* ================================================== */
        /* ONE QUESTION AT A TIME STEP                        */
        /* ================================================== */
        <div className="bg-white rounded-3xl border border-stone-200 p-6 sm:p-10 shadow-xs space-y-8 animate-in fade-in duration-200">
          {/* Progress Indicator */}
          <div>
            <div className="flex items-center justify-between text-xs font-bold text-stone-500 mb-2">
              <span>
                {t('questionProgress')
                  .replace('{current}', String(currentStep + 1))
                  .replace('{total}', String(questions.length))}
              </span>
              <span>{Math.round(((currentStep + 1) / questions.length) * 100)}%</span>
            </div>
            <div className="w-full h-2.5 bg-stone-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-emerald-600 transition-all duration-300 rounded-full"
                style={{ width: `${((currentStep + 1) / questions.length) * 100}%` }}
              ></div>
            </div>
          </div>

          {/* Question Text */}
          <div className="space-y-2">
            <h2 className="text-xl sm:text-2xl font-bold text-stone-900 leading-snug">
              {language === 'kn' ? currentQuestion.question_kn : currentQuestion.question_en}
            </h2>
            {(currentQuestion.help_text_en || currentQuestion.help_text_kn) && (
              <p className="text-sm text-stone-500">
                {language === 'kn' ? currentQuestion.help_text_kn : currentQuestion.help_text_en}
              </p>
            )}
          </div>

          {/* Question Controls based on Question Type */}
          <div className="py-2">
            {/* 1. Boolean Question */}
            {currentQuestion.question_type === 'boolean' && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <button
                  type="button"
                  onClick={() => handleAnswerChange(true)}
                  className={`p-5 rounded-2xl border-2 text-left font-bold transition-all flex items-center justify-between ${
                    answers[currentQuestion.id] === true
                      ? 'border-emerald-600 bg-emerald-50 text-emerald-950 ring-2 ring-emerald-600/20'
                      : 'border-stone-200 hover:border-emerald-300 text-stone-800 bg-white'
                  }`}
                >
                  <span className="text-base sm:text-lg">
                    {language === 'kn' ? 'ಹೌದು (Yes)' : 'Yes'}
                  </span>
                  <div
                    className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                      answers[currentQuestion.id] === true
                        ? 'border-emerald-700 bg-emerald-700 text-white'
                        : 'border-stone-300'
                    }`}
                  >
                    {answers[currentQuestion.id] === true && <CheckCircle className="w-4 h-4" />}
                  </div>
                </button>

                <button
                  type="button"
                  onClick={() => handleAnswerChange(false)}
                  className={`p-5 rounded-2xl border-2 text-left font-bold transition-all flex items-center justify-between ${
                    answers[currentQuestion.id] === false
                      ? 'border-emerald-600 bg-emerald-50 text-emerald-950 ring-2 ring-emerald-600/20'
                      : 'border-stone-200 hover:border-emerald-300 text-stone-800 bg-white'
                  }`}
                >
                  <span className="text-base sm:text-lg">
                    {language === 'kn' ? 'ಇಲ್ಲ (No)' : 'No'}
                  </span>
                  <div
                    className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                      answers[currentQuestion.id] === false
                        ? 'border-emerald-700 bg-emerald-700 text-white'
                        : 'border-stone-300'
                    }`}
                  >
                    {answers[currentQuestion.id] === false && <CheckCircle className="w-4 h-4" />}
                  </div>
                </button>
              </div>
            )}

            {/* 2. Number Question */}
            {currentQuestion.question_type === 'number' && (
              <div className="max-w-md">
                <input
                  type="number"
                  value={answers[currentQuestion.id] ?? ''}
                  onChange={(e) => handleAnswerChange(e.target.value === '' ? '' : Number(e.target.value))}
                  placeholder="Enter numeric value..."
                  className="w-full text-lg font-semibold bg-stone-50 border-2 border-stone-200 rounded-2xl px-5 py-4 text-stone-900 focus:bg-white focus:border-emerald-600 focus:outline-hidden"
                  autoFocus
                />
              </div>
            )}

            {/* 3. Select Question */}
            {currentQuestion.question_type === 'select' && currentQuestion.options && (
              <div className="space-y-3">
                {currentQuestion.options.map((opt) => {
                  const isSelected = answers[currentQuestion.id] === opt.value;
                  return (
                    <button
                      key={opt.value}
                      type="button"
                      onClick={() => handleAnswerChange(opt.value)}
                      className={`w-full p-4 rounded-xl border-2 text-left font-bold transition-all flex items-center justify-between ${
                        isSelected
                          ? 'border-emerald-600 bg-emerald-50 text-emerald-950'
                          : 'border-stone-200 hover:border-emerald-300 text-stone-800 bg-white'
                      }`}
                    >
                      <span>{language === 'kn' ? opt.label_kn : opt.label_en}</span>
                      <div
                        className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                          isSelected ? 'border-emerald-700 bg-emerald-700 text-white' : 'border-stone-300'
                        }`}
                      >
                        {isSelected && <div className="w-2 h-2 rounded-full bg-white"></div>}
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* Validation Alert */}
          {validationError && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-rose-800 text-xs font-semibold flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 shrink-0" />
              <span>{validationError}</span>
            </div>
          )}

          {/* Navigation Controls */}
          <div className="pt-6 border-t border-stone-100 flex items-center justify-between gap-4">
            <button
              onClick={handleBack}
              disabled={currentStep === 0}
              className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl text-sm font-bold border border-stone-300 bg-white text-stone-700 hover:bg-stone-50 transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <ArrowLeft className="w-4 h-4" />
              {t('btnBack')}
            </button>

            <button
              onClick={handleNext}
              className="inline-flex items-center gap-2 px-6 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm rounded-xl transition-colors shadow-xs"
            >
              <span>{currentStep === questions.length - 1 ? t('btnReview') : t('btnContinue')}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
};
