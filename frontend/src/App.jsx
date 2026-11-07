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

export default function App() {
  const [currentPage, setCurrentPage] = useState('landing');

  const renderPage = () => {
    switch (currentPage) {
      case 'landing':
        return <LandingPage onNavigate={setCurrentPage} />;
      case 'dashboard':
        return <DashboardOverview onNavigate={setCurrentPage} />;
      case 'eda':
        return <EDAPage onNavigate={setCurrentPage} />;
      case 'causal':
        return <CausalAnalysisPage onNavigate={setCurrentPage} />;
      case 'simulation':
        return <PriceSimulationPage onNavigate={setCurrentPage} />;
      case 'recommendations':
        return <RecommendationsPage onNavigate={setCurrentPage} />;
      case 'dataset':
        return <DatasetExplorerPage onNavigate={setCurrentPage} />;
      default:
        return <LandingPage onNavigate={setCurrentPage} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col md:flex-row font-sans">
      {/* Sidebar Navigation */}
      <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />

      {/* Main Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar currentPage={currentPage} onNavigate={setCurrentPage} />

        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto">
          {renderPage()}
        </main>

        <Footer />
      </div>
    </div>
  );
}
