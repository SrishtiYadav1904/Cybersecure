import React, { useState, useEffect } from 'react';
import { getAuthToken, getStoredUser, setAuthToken, setStoredUser, api } from './api';

import AppShell from './components/layout/AppShell';
import AuthModal from './components/AuthModal';
import DashboardOverview from './components/DashboardOverview';
import AnalyzeComment from './components/AnalyzeComment';
// AnalyzeChat removed — group chat analysis lives inside AnalyzeComment
import IncidentsView from './components/IncidentsView';
import ReportsView from './components/ReportsView';
import SupportChat from './components/SupportChat';
import HelpRequestForm from './components/HelpRequestForm';
import ConsultantPortal from './components/ConsultantPortal';
import AdminDashboard from './components/AdminDashboard';
import ComponentShowcase from './components/ComponentShowcase';

export default function App() {
  const [user, setUser] = useState(getStoredUser());
  const [isVerifying, setIsVerifying] = useState(() => Boolean(getAuthToken() && getStoredUser()));
  const initialTab = window.location.hash.replace('#', '') || 
    new URLSearchParams(window.location.search).get('tab') || 'dashboard';
  const [activeTab, setActiveTab] = useState(initialTab);
  const [currentIncidentId, setCurrentIncidentId] = useState(null);

  useEffect(() => {
    async function checkAuth() {
      try {
        const u = await api.getMe();
        setUser(u);
        setStoredUser(u);
      } catch (e) {
        setUser(null);
        setAuthToken(null);
        setStoredUser(null);
      } finally {
        setIsVerifying(false);
      }
    }
    if (getAuthToken()) {
      checkAuth();
    } else {
      setIsVerifying(false);
    }
  }, []);

  const handleLoginSuccess = (authenticatedUser) => {
    setUser(authenticatedUser);
    setActiveTab('dashboard');
  };

  const handleLogout = () => {
    setAuthToken(null);
    setStoredUser(null);
    setUser(null);
    setActiveTab('login');
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardOverview setActiveTab={setActiveTab} user={user} />;
      case 'analyze':
        return (
          <AnalyzeComment
            setActiveTab={setActiveTab}
            onIncidentUpdate={(id) => setCurrentIncidentId(id)}
          />
        );
      case 'chat':
        // redirect to unified analyze workspace (Group Chat tab)
        return (
          <AnalyzeComment
            setActiveTab={setActiveTab}
            onIncidentUpdate={(id) => setCurrentIncidentId(id)}
          />
        );
      case 'incidents':
        return (
          <IncidentsView
            setActiveTab={setActiveTab}
            onSelectIncident={(id) => setCurrentIncidentId(id)}
          />
        );
      case 'reports':
        return <ReportsView setActiveTab={setActiveTab} />;
      case 'support':
        return <SupportChat setActiveTab={setActiveTab} />;
      case 'help':
        return <HelpRequestForm setActiveTab={setActiveTab} incidentId={currentIncidentId} />;
      case 'consultant':
        if (user?.role !== 'CONSULTANT' && user?.role !== 'ADMIN') {
          return (
            <div className="max-w-xl mx-auto my-16 p-8 bg-rose-500/10 border border-rose-500/30 rounded-2xl text-center">
              <span className="text-4xl block mb-2">🚫</span>
              <h2 className="text-xl font-bold text-rose-400">403 Access Forbidden</h2>
              <p className="text-xs text-slate-300 mt-2">
                Consultant portal is strictly restricted to verified human consultants and admins.
              </p>
              <button
                type="button"
                onClick={() => setActiveTab('dashboard')}
                className="btn-secondary text-xs mt-6"
              >
                Return to Dashboard
              </button>
            </div>
          );
        }
        return <ConsultantPortal setActiveTab={setActiveTab} />;
      case 'admin':
        if (user?.role !== 'ADMIN') {
          return (
            <div className="max-w-xl mx-auto my-16 p-8 bg-rose-500/10 border border-rose-500/30 rounded-2xl text-center">
              <span className="text-4xl block mb-2">🔒</span>
              <h2 className="text-xl font-bold text-rose-400">403 Access Forbidden</h2>
              <p className="text-xs text-slate-300 mt-2">
                Administrative portal is strictly restricted to verified system administrators.
              </p>
              <button
                type="button"
                onClick={() => setActiveTab('dashboard')}
                className="btn-secondary text-xs mt-6"
              >
                Return to Dashboard
              </button>
            </div>
          );
        }
        return <AdminDashboard />;
      case 'showcase':
        return <ComponentShowcase />;
      default:
        return <DashboardOverview setActiveTab={setActiveTab} user={user} />;
    }
  };

  if (isVerifying) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: '#080b11' }}>
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin" />
          <span className="text-xs text-slate-400 font-medium">Verifying session...</span>
        </div>
      </div>
    );
  }

  if (!user || activeTab === 'login') {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden" style={{ background: '#080b11' }}>
        {/* Animated background grid */}
        <div className="absolute inset-0" style={{
          backgroundImage: `
            linear-gradient(rgba(99,102,241,0.06) 1px, transparent 1px),
            linear-gradient(90deg, rgba(99,102,241,0.06) 1px, transparent 1px)
          `,
          backgroundSize: '40px 40px'
        }} />

        {/* Gradient orbs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full opacity-20 blur-3xl" style={{ background: 'radial-gradient(circle, #4f46e5, transparent)' }} />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full opacity-15 blur-3xl" style={{ background: 'radial-gradient(circle, #7c3aed, transparent)' }} />
        <div className="absolute top-3/4 left-1/3 w-64 h-64 rounded-full opacity-10 blur-3xl" style={{ background: 'radial-gradient(circle, #06b6d4, transparent)' }} />

        {/* Brand strip at top */}
        <div className="absolute top-0 left-0 right-0 flex items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-indigo-600 to-purple-500 flex items-center justify-center">
              <span className="text-white text-xs font-black">CG</span>
            </div>
            <span className="text-slate-300 text-xs font-bold tracking-wide">CyberGuard</span>
          </div>
          <div className="flex items-center gap-4 text-[11px] text-slate-500 font-mono">
            <span>Cybercrime: <b className="text-slate-400">1930</b></span>
            <span>Tele-MANAS: <b className="text-slate-400">14416</b></span>
          </div>
        </div>

        {/* Auth card */}
        <div className="relative z-10 w-full max-w-md animate-fade-in">
          <AuthModal onLoginSuccess={handleLoginSuccess} />
        </div>

        {/* Bottom tag */}
        <p className="absolute bottom-4 text-[10px] text-slate-600 font-mono text-center w-full">
          Multilingual Explainable AI — CB-EXP-002 — India Cybercrime Act 2000 / IT Act 2008
        </p>
      </div>
    );
  }


  return (
    <AppShell
      activeTab={activeTab}
      setActiveTab={setActiveTab}
      user={user}
      onLogout={handleLogout}
    >
      {renderContent()}
    </AppShell>
  );
}
