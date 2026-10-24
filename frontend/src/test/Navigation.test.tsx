import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect } from 'vitest';
import { Header } from '../components/layout/Header';
import { LanguageProvider } from '../contexts/LanguageContext';
import { AuthProvider } from '../contexts/AuthContext';

describe('Header & Navigation', () => {
  it('renders branding and navigations links, toggles language', () => {
    render(
      <LanguageProvider>
        <AuthProvider>
          <BrowserRouter>
            <Header />
          </BrowserRouter>
        </AuthProvider>
      </LanguageProvider>
    );

    // Initial Brand rendering
    expect(screen.getByText(/RuralConnect Karnataka|ರೂರಲ್ ಕನೆಕ್ಟ್ ಕರ್ನಾಟಕ/i)).toBeInTheDocument();

    // Language buttons using accessible aria-labels
    const knBtn = screen.getByRole('button', { name: /Switch to Kannada/i });
    const enBtn = screen.getByRole('button', { name: /Switch to English/i });

    expect(knBtn).toBeInTheDocument();
    expect(enBtn).toBeInTheDocument();

    // Click English
    fireEvent.click(enBtn);
    expect(screen.getByText('RuralConnect Karnataka')).toBeInTheDocument();
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Browse Schemes')).toBeInTheDocument();

    // Click Kannada
    fireEvent.click(knBtn);
    expect(screen.getByText('ರೂರಲ್ ಕನೆಕ್ಟ್ ಕರ್ನಾಟಕ')).toBeInTheDocument();
    expect(screen.getByText('ಮುಖಪುಟ')).toBeInTheDocument();
    expect(screen.getByText('ಯೋಜನೆಗಳ ಪಟ್ಟಿ')).toBeInTheDocument();
  });
});
