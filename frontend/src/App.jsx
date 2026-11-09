import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Pages
import LandingPage from './pages/LandingPage';
import DashboardOverview from './pages/DashboardOverview';
import EDAPage from './pages/EDAPage';
import CausalAnalysisPage from './pages/CausalAnalysisPage';
import PriceSimulationPage from './pages/PriceSimulationPage';
import RecommendationsPage from './pages/RecommendationsPage';
import DatasetExplorerPage from './pages/DatasetExplorerPage';
import AIAssistantPage from './pages/AIAssistantPage';
import ReportsPage from './pages/ReportsPage';
import HelpSettingsPage from './pages/HelpSettingsPage';

export default function App() {
  const [currentPage, setCurrentPage] = useState('landing');
  const [lang, setLang] = useState('en');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const renderPage = () => {
    switch (currentPage) {
      case 'landing':
        return <LandingPage onNavigate={setCurrentPage} lang={lang} onSetLang={setLang} />;
      case 'dashboard':
        return <DashboardOverview onNavigate={setCurrentPage} lang={lang} />;
      case 'eda':
        return <EDAPage onNavigate={setCurrentPage} lang={lang} />;
      case 'causal':
        return <CausalAnalysisPage onNavigate={setCurrentPage} lang={lang} />;
      case 'simulation':
        return <PriceSimulationPage onNavigate={setCurrentPage} lang={lang} />;
      case 'recommendations':
        return <RecommendationsPage onNavigate={setCurrentPage} lang={lang} />;
      case 'upload':
      case 'dataset':
        return <DatasetExplorerPage onNavigate={setCurrentPage} lang={lang} />;
      case 'assistant':
        return <AIAssistantPage onNavigate={setCurrentPage} lang={lang} />;
      case 'reports':
        return <ReportsPage onNavigate={setCurrentPage} lang={lang} />;
      case 'help':
        return <HelpSettingsPage onNavigate={setCurrentPage} lang={lang} onSetLang={setLang} />;
      default:
        return <LandingPage onNavigate={setCurrentPage} lang={lang} onSetLang={setLang} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col md:flex-row font-sans">
      {/* Sidebar Navigation */}
      <Sidebar
        currentPage={currentPage}
        onNavigate={setCurrentPage}
        lang={lang}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Main Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar
          currentPage={currentPage}
          onNavigate={setCurrentPage}
          lang={lang}
          onSetLang={setLang}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="flex-1 p-4 md:p-8 max-w-7xl w-full mx-auto">
          {renderPage()}
        </main>

        <Footer lang={lang} />
      </div>
    </div>
  );
}
