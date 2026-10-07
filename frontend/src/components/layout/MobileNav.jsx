import React from 'react';
import {
  LayoutDashboard,
  Scan,
  ShieldAlert,
  HeartHandshake,
  Menu,
  FileText,
  AlertOctagon,
  ClipboardList,
  Sliders,
  LogOut,
  ShieldCheck,
  Cpu
} from 'lucide-react';
import Drawer from '../ui/Drawer';

export default function MobileNav({
  activeTab,
  setActiveTab,
  user,
  onLogout,
  isOpen,
  onClose
}) {
  const bottomBarItems = [
    { id: 'dashboard', label: 'Home', icon: LayoutDashboard },
    { id: 'analyze', label: 'Analyze', icon: Scan },
    { id: 'incidents', label: 'Incidents', icon: ShieldAlert },
    { id: 'support', label: 'Support', icon: HeartHandshake }
  ];

  const allDrawerItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, group: 'Main' },
    { id: 'analyze', label: 'Analyze Workspace', icon: Scan, group: 'Main' },
    { id: 'incidents', label: 'My Incidents', icon: ShieldAlert, group: 'Main' },
    { id: 'reports', label: 'Forensic Reports', icon: FileText, group: 'Main' },
    { id: 'support', label: 'Support AI', icon: HeartHandshake, group: 'Main' },
    { id: 'help', label: 'Consultant Escalation', icon: AlertOctagon, group: 'Assistance' }
  ];

  if (user && user.role === 'CONSULTANT') {
    allDrawerItems.push({ id: 'consultant', label: 'Consultant Portal', icon: ClipboardList, group: 'Portals' });
  }
  if (user && user.role === 'ADMIN') {
    allDrawerItems.push({ id: 'admin', label: 'Admin Portal', icon: Sliders, group: 'Portals' });
  }

  const handleSelectTab = (id) => {
    setActiveTab(id);
    onClose();
  };

  return (
    <>
      {/* Fixed Mobile Bottom Bar */}
      <nav className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-[#0a0e17]/95 backdrop-blur-md border-t border-white/10 px-2 py-1.5 flex items-center justify-around select-none">
        {bottomBarItems.map(item => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              type="button"
              onClick={() => setActiveTab(item.id)}
              className={`
                flex flex-col items-center gap-1 py-1 px-3 rounded-xl transition-all text-[10px] font-medium
                ${isActive ? 'text-indigo-400 font-bold' : 'text-slate-400 hover:text-slate-200'}
              `}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-400 stroke-[2.5]' : 'text-slate-400'}`} />
              <span>{item.label}</span>
            </button>
          );
        })}

        {/* Menu toggle button */}
        <button
          type="button"
          onClick={() => (isOpen ? onClose() : handleSelectTab(activeTab))}
          className="flex flex-col items-center gap-1 py-1 px-3 rounded-xl text-slate-400 hover:text-slate-200 text-[10px] font-medium"
        >
          <Menu className="w-4 h-4" />
          <span>More</span>
        </button>
      </nav>

      {/* Slide-over Mobile Navigation Drawer */}
      <Drawer
        isOpen={isOpen}
        onClose={onClose}
        title="Navigation Menu"
        side="left"
        width="sm"
      >
        <div className="space-y-6">
          {/* User Header */}
          {user && (
            <div className="p-4 rounded-xl bg-[#151c2b] border border-white/10 flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 text-white flex items-center justify-center font-bold text-sm">
                {user.username ? user.username.slice(0, 2).toUpperCase() : 'CG'}
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-xs font-bold text-white truncate">{user.full_name || user.username}</p>
                <span className="text-[10px] font-mono text-indigo-400 uppercase tracking-wider">{user.role}</span>
              </div>
            </div>
          )}

          {/* Links list */}
          <div className="space-y-1">
            {allDrawerItems.map(item => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => handleSelectTab(item.id)}
                  className={`
                    w-full flex items-center gap-3 px-3.5 py-3 rounded-xl text-xs font-medium transition-all text-left
                    ${isActive
                      ? 'bg-gradient-to-r from-indigo-600 to-indigo-500 text-white font-semibold'
                      : 'text-slate-300 hover:bg-slate-800/60'}
                  `}
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span className="flex-1">{item.label}</span>
                </button>
              );
            })}
          </div>

          {/* System Telemetry */}
          <div className="p-3.5 rounded-xl bg-[#151c2b] border border-white/10 space-y-1 text-xs">
            <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider flex items-center gap-1.5">
              <Cpu className="w-3 h-3 text-indigo-400" />
              Engine Status
            </span>
            <p className="font-mono text-indigo-300 font-bold text-[11px]">CB-EXP-002 Online</p>
            <p className="text-[10px] text-slate-500">22.5k Multi-source Multilingual</p>
          </div>

          {/* Logout CTA */}
          <div className="pt-2">
            <button
              type="button"
              onClick={() => {
                onClose();
                onLogout();
              }}
              className="w-full flex items-center justify-center gap-2 p-3 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs font-semibold transition-all"
            >
              <LogOut className="w-4 h-4" />
              <span>Sign Out</span>
            </button>
          </div>
        </div>
      </Drawer>
    </>
  );
}
