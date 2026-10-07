import React from 'react';

export default function Navbar({ activeTab, setActiveTab, user, onLogout }) {
  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: '⚡' },
    { id: 'analyze', label: 'Analyze Comment', icon: '🔍' },
    { id: 'chat', label: 'Analyze Chat', icon: '💬' },
    { id: 'incidents', label: 'My Incidents', icon: '🛡️' },
    { id: 'reports', label: 'Reports', icon: '📄' },
    { id: 'support', label: 'Support AI', icon: '🤝' },
    { id: 'help', label: 'Seek Help', icon: '🚨' }
  ];

  if (user && user.role === 'ADMIN') {
    tabs.push({ id: 'admin', label: 'Admin Portal', icon: '⚙️' });
  }

  if (user && user.role === 'CONSULTANT') {
    tabs.push({ id: 'consultant', label: 'Consultant Portal', icon: '📋' });
  }

  return (
    <header className="sticky top-0 z-50 bg-[#0a0e17]/90 backdrop-blur-md border-b border-white/10 px-6 py-3.5">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Brand */}
        <div 
          onClick={() => setActiveTab('dashboard')} 
          className="flex items-center gap-3 cursor-pointer select-none"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/25">
            <span className="text-xl font-black text-white">CG</span>
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight leading-tight flex items-center gap-2">
              CyberGuard
              <span className="text-[10px] px-2 py-0.5 rounded-full font-mono font-medium bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                AML v1.0
              </span>
            </h1>
            <p className="text-[11px] text-slate-400 font-medium">Multilingual Explainable AI Detection</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden md:flex items-center gap-1 bg-slate-900/60 p-1 rounded-xl border border-white/5">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === tab.id
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </nav>

        {/* User profile & actions */}
        <div className="flex items-center gap-3">
          {user ? (
            <div className="flex items-center gap-3">
              <div className="text-right hidden sm:block">
                <p className="text-xs font-bold text-slate-200">{user.full_name || user.username}</p>
                <div className="flex items-center justify-end gap-1.5">
                  <span className={`inline-block w-1.5 h-1.5 rounded-full ${user.role === 'ADMIN' ? 'bg-amber-400' : 'bg-emerald-400'}`}></span>
                  <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">{user.role}</span>
                </div>
              </div>
              <button
                onClick={onLogout}
                className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-rose-500/20 text-slate-300 hover:text-rose-400 border border-white/10 hover:border-rose-500/30 transition-all"
              >
                Logout
              </button>
            </div>
          ) : (
            <button
              onClick={() => setActiveTab('login')}
              className="btn-primary text-xs !py-2 !px-4"
            >
              Sign In
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
