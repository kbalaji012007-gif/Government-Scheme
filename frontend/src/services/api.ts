import {
  Category,
  SchemeListResponse,
  SchemeDetail,
  DocumentRequirement,
  SchemeEligibilityConfigResponse,
  CheckEligibilityResponse,
  CenterListResponse,
  CenterDetail,
  AuthResponse,
  User,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
  }

  private getAuthHeader(): Record<string, string> {
    const token = localStorage.getItem('ruralconnect_token');
    if (token) {
      return { Authorization: `Bearer ${token}` };
    }
    return {};
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
    const headers = {
      'Content-Type': 'application/json',
      ...this.getAuthHeader(),
      ...(options.headers || {}),
    };

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        let errorDetail = `Request failed with status ${response.status}`;
        try {
          const errorJson = await response.json();
          if (errorJson && errorJson.detail) {
            errorDetail = typeof errorJson.detail === 'string' ? errorJson.detail : JSON.stringify(errorJson.detail);
          }
        } catch {
          // Non-JSON response
        }
        throw new Error(errorDetail);
      }

      return (await response.json()) as T;
    } catch (error: any) {
      if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
        throw new Error('Unable to connect to the RuralConnect Karnataka server. Please ensure the backend service is running.');
      }
      throw error;
    }
  }

  // Health
  async getHealth(): Promise<{ status: string; database: { status: string; type: string } }> {
    return this.request('/health');
  }

  // Categories
  async getCategories(): Promise<Category[]> {
    return this.request<Category[]>('/categories');
  }

  // Schemes
  async getSchemes(params?: {
    category?: string;
    beneficiary_type?: string;
    query?: string;
    page?: number;
    page_size?: number;
  }): Promise<SchemeListResponse> {
    const queryParams = new URLSearchParams();
    if (params?.category && params.category !== 'all') {
      queryParams.append('category', params.category);
    }
    if (params?.beneficiary_type && params.beneficiary_type !== 'all') {
      queryParams.append('beneficiary_type', params.beneficiary_type);
    }
    if (params?.query && params.query.trim()) {
      queryParams.append('query', params.query.trim());
    }
    if (params?.page) {
      queryParams.append('page', params.page.toString());
    }
    if (params?.page_size) {
      queryParams.append('page_size', params.page_size.toString());
    }

    const queryString = queryParams.toString();
    const endpoint = `/schemes${queryString ? `?${queryString}` : ''}`;
    return this.request<SchemeListResponse>(endpoint);
  }

  async getSchemeById(schemeId: string): Promise<SchemeDetail> {
    return this.request<SchemeDetail>(`/schemes/${encodeURIComponent(schemeId)}`);
  }

  async getSchemeDocuments(schemeId: string): Promise<DocumentRequirement[]> {
    return this.request<DocumentRequirement[]>(`/schemes/${encodeURIComponent(schemeId)}/documents`);
  }

  // Eligibility
  async getEligibilityQuestions(schemeId: string): Promise<SchemeEligibilityConfigResponse> {
    return this.request<SchemeEligibilityConfigResponse>(`/schemes/${encodeURIComponent(schemeId)}/eligibility`);
  }

  async checkEligibility(schemeId: string, answers: Record<string, any>): Promise<CheckEligibilityResponse> {
    return this.request<CheckEligibilityResponse>(`/schemes/${encodeURIComponent(schemeId)}/check-eligibility`, {
      method: 'POST',
      body: JSON.stringify({ answers }),
    });
  }

  // Service Centres
  async getCenters(params?: {
    district?: string;
    taluk?: string;
    center_type?: string;
    query?: string;
    page?: number;
    page_size?: number;
  }): Promise<CenterListResponse> {
    const queryParams = new URLSearchParams();
    if (params?.district && params.district !== 'all') {
      queryParams.append('district', params.district);
    }
    if (params?.taluk && params.taluk !== 'all') {
      queryParams.append('taluk', params.taluk);
    }
    if (params?.center_type && params.center_type !== 'all') {
      queryParams.append('center_type', params.center_type);
    }
    if (params?.query && params.query.trim()) {
      queryParams.append('query', params.query.trim());
    }
    if (params?.page) {
      queryParams.append('page', params.page.toString());
    }
    if (params?.page_size) {
      queryParams.append('page_size', params.page_size.toString());
    }

    const queryString = queryParams.toString();
    const endpoint = `/centers${queryString ? `?${queryString}` : ''}`;
    return this.request<CenterListResponse>(endpoint);
  }

  async getCenterById(centerId: string): Promise<CenterDetail> {
    return this.request<CenterDetail>(`/centers/${encodeURIComponent(centerId)}`);
  }

  // Authentication
  async register(payload: {
    email: string;
    password: string;
    full_name: string;
    preferred_language?: string;
  }): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async login(payload: { email: string; password: string }): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async googleAuth(payload: {
    id_token?: string;
    email: string;
    full_name: string;
    uid: string;
    preferred_language?: string;
  }): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/google', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async getMe(): Promise<User> {
    return this.request<User>('/auth/me');
  }
}

export const api = new ApiClient(API_BASE_URL);
