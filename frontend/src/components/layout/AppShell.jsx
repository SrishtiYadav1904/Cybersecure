import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Topbar from './Topbar';
import MobileNav from './MobileNav';

export default function AppShell({
  children,
  activeTab,
  setActiveTab,
  user,
  onLogout
}) {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isMobileNavOpen, setIsMobileNavOpen] = useState(false);

  return (
    <div className="min-h-screen flex bg-[#080b11] text-slate-100 font-sans selection:bg-indigo-500 selection:text-white antialiased">
      {/* Collapsible Desktop Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        user={user}
        onLogout={onLogout}
        isCollapsed={isSidebarCollapsed}
        setIsCollapsed={setIsSidebarCollapsed}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Topbar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          user={user}
          onLogout={onLogout}
          onOpenMobileNav={() => setIsMobileNavOpen(true)}
        />

        <main className="flex-1 px-4 sm:px-6 lg:px-8 py-6 pb-24 lg:pb-12 max-w-7xl w-full mx-auto">
          {children}
        </main>

        <footer className="border-t border-white/5 py-4 px-6 text-center text-xs text-slate-500 bg-[#070a10]">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
            <p>© 2026 CyberGuard Forensic Intelligence. Multilingual Explainable AI Architecture.</p>
            <div className="flex items-center gap-3 text-[11px] text-slate-400 font-mono">
              <span>Cybercrime: <b>1930</b></span>
              <span>•</span>
              <span>Tele-MANAS: <b>14416</b></span>
            </div>
          </div>
        </footer>
      </div>

      {/* Mobile Bottom Bar + Drawer */}
      <MobileNav
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        user={user}
        onLogout={onLogout}
        isOpen={isMobileNavOpen}
        onClose={() => setIsMobileNavOpen(false)}
      />
    </div>
  );
}
