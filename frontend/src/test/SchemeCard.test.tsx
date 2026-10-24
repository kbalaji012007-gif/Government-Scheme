import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect } from 'vitest';
import { SchemeCard } from '../components/schemes/SchemeCard';
import { LanguageProvider } from '../contexts/LanguageContext';
import { SchemeSummary } from '../types';

const mockScheme: SchemeSummary = {
  id: 'raitha-siri',
  name_en: 'Raitha Siri Millet Scheme',
  name_kn: 'ರೈತ ಸಿರಿ ಯೋಜನೆ',
  short_description_en: 'Direct financial incentive of ₹10,000 per hectare for millet growers.',
  short_description_kn: 'ಸಿರಿಧಾನ್ಯ ಬೆಳೆಯುವ ರೈತರಿಗೆ ಪ್ರತಿ ಹೆಕ್ಟೇರ್‌ಗೆ ₹10,000 ನೆರವು.',
  category: 'farmers',
  beneficiary_summary_en: 'Small and marginal dryland farmers.',
  beneficiary_summary_kn: 'ಸಣ್ಣ ಮತ್ತು ಅತಿ ಸಣ್ಣ ಒಣಭೂಮಿ ರೈತರು.',
  beneficiary_types: ['farmers'],
  tags: ['Agriculture', 'Millets'],
  is_development_sample: true,
};

describe('SchemeCard Component', () => {
  it('renders scheme name, category badge, and action buttons', () => {
    render(
      <LanguageProvider>
        <BrowserRouter>
          <SchemeCard scheme={mockScheme} />
        </BrowserRouter>
      </LanguageProvider>
    );

    // Name or Kannada name should render
    expect(screen.getByText(/Raitha Siri|ರೈತ ಸಿರಿ/i)).toBeInTheDocument();

    // Check Eligibility button should be present
    expect(screen.getByRole('link', { name: /Eligibility|ಅರ್ಹತೆ/i })).toBeInTheDocument();

    // View Details link should be present
    expect(screen.getByRole('link', { name: /View Details|ವಿವರ/i })).toBeInTheDocument();
  });
});
