import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect, vi } from 'vitest';
import { HomePage } from '../pages/HomePage';
import { LanguageProvider } from '../contexts/LanguageContext';
import { AuthProvider } from '../contexts/AuthContext';

// Mock the API client
vi.mock('../services/api', () => ({
  api: {
    getSchemes: vi.fn().mockResolvedValue({
      items: [
        {
          id: 'raitha-siri',
          name_en: 'Raitha Siri Millet Assistance Scheme',
          name_kn: 'ರೈತ ಸಿರಿ ಸಿರಿಧಾನ್ಯ ಪ್ರೋತ್ಸಾಹ ಯೋಜನೆ',
          category: 'farmers',
          short_description_en: 'Financial incentive for millet cultivation.',
          short_description_kn: 'ಸಿರಿಧಾನ್ಯ ಬೆಳೆಯುವ ರೈತರಿಗೆ ಆರ್ಥಿಕ ನೆರವು.',
          beneficiary_summary_en: 'Dryland farmers',
          beneficiary_summary_kn: 'ಒಣಭೂಮಿ ರೈತರು',
          beneficiary_types: ['farmers'],
          tags: ['Millets'],
          is_development_sample: true,
        },
      ],
      total: 1,
      page: 1,
      page_size: 6,
      total_pages: 1,
    }),
  },
}));

describe('HomePage Component', () => {
  it('renders hero headline, search input, and category cards', async () => {
    render(
      <LanguageProvider>
        <AuthProvider>
          <BrowserRouter>
            <HomePage />
          </BrowserRouter>
        </AuthProvider>
      </LanguageProvider>
    );

    // Hero headline text exists
    expect(
      screen.getByText(/Find the Government Schemes|ನೀವು ಅರ್ಹರಾಗಿರುವ ಸರ್ಕಾರಿ/i)
    ).toBeInTheDocument();

    // Search input exists
    expect(screen.getByRole('textbox', { name: /search schemes/i })).toBeInTheDocument();

    // Category cards exist
    expect(screen.getByText(/Farmers|ರೈತರು/i)).toBeInTheDocument();
    expect(screen.getByText(/Students|ವಿದ್ಯಾರ್ಥಿಗಳು/i)).toBeInTheDocument();
    expect(screen.getByText(/Women|ಮಹಿಳೆಯರು/i)).toBeInTheDocument();
  });
});
