export interface Category {
  id: string;
  name_en: string;
  name_kn: string;
  description_en: string;
  description_kn: string;
  icon: string;
  scheme_count: number;
}

export interface DocumentRequirement {
  id: string;
  name_en: string;
  name_kn: string;
  description_en?: string;
  description_kn?: string;
  mandatory: boolean;
}

export interface QuestionOption {
  value: string;
  label_en: string;
  label_kn: string;
}

export interface EligibilityQuestion {
  id: string;
  question_en: string;
  question_kn: string;
  question_type: 'boolean' | 'number' | 'select';
  options?: QuestionOption[];
  help_text_en?: string;
  help_text_kn?: string;
  mandatory: boolean;
}

export interface SchemeSummary {
  id: string;
  name_en: string;
  name_kn: string;
  short_description_en: string;
  short_description_kn: string;
  category: string;
  beneficiary_summary_en: string;
  beneficiary_summary_kn: string;
  beneficiary_types: string[];
  tags: string[];
  is_development_sample: boolean;
}

export interface SchemeDetail extends SchemeSummary {
  full_description_en: string;
  full_description_kn: string;
  benefits_en: string[];
  benefits_kn: string[];
  eligibility_conditions_en: string[];
  eligibility_conditions_kn: string[];
  required_documents: DocumentRequirement[];
  application_process_en: string[];
  application_process_kn: string[];
  official_portal_url?: string;
  last_verified_date?: string;
  disclaimer_en: string;
  disclaimer_kn: string;
}

export interface SchemeListResponse {
  items: SchemeSummary[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface SchemeEligibilityConfigResponse {
  scheme_id: string;
  scheme_name_en: string;
  scheme_name_kn: string;
  questions: EligibilityQuestion[];
}

export interface MissingRequirement {
  field: string;
  message_en: string;
  message_kn: string;
}

export interface CheckEligibilityResponse {
  scheme_id: string;
  scheme_name_en: string;
  scheme_name_kn: string;
  status: 'eligible' | 'not_eligible' | 'more_info_required';
  status_title_en: string;
  status_title_kn: string;
  summary_en: string;
  summary_kn: string;
  reasons_en: string[];
  reasons_kn: string[];
  missing_requirements: MissingRequirement[];
  document_checklist: DocumentRequirement[];
  next_steps_en: string[];
  next_steps_kn: string[];
  preliminary_notice_en: string;
  preliminary_notice_kn: string;
}

export interface CenterSummary {
  id: string;
  name_en: string;
  name_kn: string;
  center_type: string;
  district: string;
  taluk: string;
  address_en: string;
  address_kn: string;
  contact_phone?: string;
  contact_email?: string;
  operating_hours_en?: string;
  operating_hours_kn?: string;
  is_development_sample: boolean;
}

export interface CenterDetail extends CenterSummary {
  directions_url?: string;
  latitude?: number;
  longitude?: number;
  services_offered_en: string[];
  services_offered_kn: string[];
}

export interface CenterListResponse {
  items: CenterSummary[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  districts: string[];
  taluks: string[];
  center_types: string[];
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  preferred_language: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
