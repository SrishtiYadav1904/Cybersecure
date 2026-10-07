import React from 'react';
import {
  Menu,
  PhoneCall,
  ShieldCheck,
  Cpu,
  User,
  LogOut,
  LifeBuoy
} from 'lucide-react';
import Tooltip from '../ui/Tooltip';

export default function Topbar({
  activeTab,
  setActiveTab,
  user,
  onLogout,
  onOpenMobileNav
}) {
  const pageTitles = {
    dashboard: 'Safety & Evidence Dashboard',
    analyze: 'Multilingual Analysis Workspace',
    incidents: 'Preserved Incident Cases',
    reports: 'Forensic PDF Artifacts',
    support: 'AI Wellbeing & Legal Support',
    help: 'Consultant Escalation Request',
    consultant: 'Consultant Case Triage',
    admin: 'MLOps & Admin Analytics'
  };

  return (
    <header className="sticky top-0 z-20 h-16 bg-[#0a0e17]/95 backdrop-blur-md border-b border-white/10 px-4 sm:px-6 flex items-center justify-between">
      {/* Left: Mobile hamburger & Page Title */}
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onOpenMobileNav}
          aria-label="Open mobile navigation"
          className="lg:hidden p-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="hidden sm:block">
          <h1 className="text-sm font-bold text-white tracking-tight">
            {pageTitles[activeTab] || 'CyberGuard System'}
          </h1>
          <p className="text-[11px] text-slate-400">
            Real-time inference & grounded crisis response
          </p>
        </div>
      </div>

      {/* Right: Quick Emergency Helplines, Engine Status, User Menu */}
      <div className="flex items-center gap-2.5 sm:gap-3">
        {/* National Emergency Hotline Quick Action */}
        <div className="flex items-center gap-2">
          <Tooltip content="Call National Cybercrime Hotline 1930 / Tele-MANAS 14416" position="bottom">
            <button
              type="button"
              onClick={() => setActiveTab('support')}
              className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs font-semibold transition-all"
            >
              <PhoneCall className="w-3.5 h-3.5 text-rose-400" />
              <span className="hidden md:inline font-mono">1930 / 14416</span>
              <span className="md:hidden font-mono">1930</span>
            </button>
          </Tooltip>

          {/* Active Model Indicator */}
          <div className="hidden xl:flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-[#151c2b] border border-white/10 text-xs font-mono text-slate-300">
            <Cpu className="w-3.5 h-3.5 text-indigo-400" />
            <span>CB-EXP-002</span>
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
          </div>
        </div>

        {/* User Pill */}
        {user ? (
          <div className="flex items-center gap-2 pl-2 border-l border-white/10">
            <div className="w-8 h-8 rounded-xl bg-indigo-600/20 border border-indigo-500/30 text-indigo-300 flex items-center justify-center font-bold text-xs select-none">
              {user.username ? user.username.slice(0, 2).toUpperCase() : 'CG'}
            </div>
            <div className="hidden sm:block text-left text-xs leading-tight">
              <span className="font-semibold text-slate-200 block truncate max-w-[120px]">
                {user.full_name || user.username}
              </span>
              <span className="text-[10px] text-slate-400 font-mono uppercase">
                {user.role}
              </span>
            </div>
          </div>
        ) : (
          <button
            type="button"
            onClick={() => setActiveTab('login')}
            className="btn-primary text-xs !py-1.5 !px-3"
          >
            Sign In
          </button>
        )}
      </div>
    </header>
  );
}
