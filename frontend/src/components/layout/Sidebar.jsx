import React from 'react';
import {
  LayoutDashboard,
  Scan,
  ShieldAlert,
  FileText,
  HeartHandshake,
  AlertOctagon,
  ClipboardList,
  Sliders,
  ChevronLeft,
  ChevronRight,
  LogOut,
  ShieldCheck,
  Cpu
} from 'lucide-react';
import Tooltip from '../ui/Tooltip';

export default function Sidebar({
  activeTab,
  setActiveTab,
  user,
  onLogout,
  isCollapsed,
  setIsCollapsed
}) {
  const mainNavItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'analyze', label: 'Analyze Workspace', icon: Scan },
    { id: 'incidents', label: 'My Incidents', icon: ShieldAlert },
    { id: 'reports', label: 'Forensic Reports', icon: FileText },
    { id: 'support', label: 'Support AI', icon: HeartHandshake }
  ];

  const escalationItems = [
    { id: 'help', label: 'Consultant Escalation', icon: AlertOctagon, badge: 'Help' }
  ];

  const roleItems = [];
  if (user && user.role === 'CONSULTANT') {
    roleItems.push({ id: 'consultant', label: 'Consultant Portal', icon: ClipboardList, badge: 'Role' });
  }
  if (user && user.role === 'ADMIN') {
    roleItems.push({ id: 'admin', label: 'Admin Portal', icon: Sliders, badge: 'Admin' });
  }

  const renderNavGroup = (title, items) => (
    <div className="space-y-1">
      {!isCollapsed && title && (
        <p className="px-3 text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-1.5 select-none">
          {title}
        </p>
      )}
      {items.map((item) => {
        const Icon = item.icon;
        const isActive = activeTab === item.id;

        const buttonContent = (
          <button
            type="button"
            onClick={() => setActiveTab(item.id)}
            className={`
              w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all select-none
              ${isActive
                ? 'bg-gradient-to-r from-indigo-600 to-indigo-500 text-white font-semibold shadow-md shadow-indigo-600/25'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'}
              ${isCollapsed ? 'justify-center px-0' : ''}
            `}
          >
            <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-slate-400'}`} />
            {!isCollapsed && (
              <span className="truncate flex-1 text-left">{item.label}</span>
            )}
            {!isCollapsed && item.badge && (
              <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono font-bold ${
                isActive ? 'bg-white/20 text-white' : 'bg-slate-800 text-indigo-400 border border-indigo-500/30'
              }`}>
                {item.badge}
              </span>
            )}
          </button>
        );

        if (isCollapsed) {
          return (
            <Tooltip key={item.id} content={item.label} position="right">
              {buttonContent}
            </Tooltip>
          );
        }

        return <div key={item.id}>{buttonContent}</div>;
      })}
    </div>
  );

  return (
    <aside
      className={`
        hidden lg:flex flex-col h-screen sticky top-0 bg-[#0a0e17] border-r border-white/10
        transition-all duration-300 z-30 select-none
        ${isCollapsed ? 'w-20' : 'w-64'}
      `}
    >
      {/* Brand Header */}
      <div className="h-16 px-4 flex items-center justify-between border-b border-white/10">
        <div
          onClick={() => setActiveTab('dashboard')}
          className="flex items-center gap-3 cursor-pointer overflow-hidden"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/25 shrink-0">
            <ShieldCheck className="w-5 h-5 text-white" />
          </div>
          {!isCollapsed && (
            <div className="min-w-0">
              <div className="flex items-center gap-1.5">
                <span className="text-sm font-bold text-white tracking-tight">CyberGuard</span>
                <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  AML
                </span>
              </div>
              <p className="text-[10px] text-slate-500 truncate">Multilingual AI Forensics</p>
            </div>
          )}
        </div>

        <button
          type="button"
          onClick={() => setIsCollapsed(!isCollapsed)}
          aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
        >
          {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Navigation Groups */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-6">
        {renderNavGroup('Main Navigation', mainNavItems)}
        {renderNavGroup('Assistance', escalationItems)}
        {roleItems.length > 0 && renderNavGroup('Specialized Portals', roleItems)}
      </div>

      {/* Active Model & Engine Lineage */}
      {!isCollapsed && (
        <div className="mx-3 mb-3 p-3 rounded-xl bg-[#0f141f] border border-white/10 text-xs space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider flex items-center gap-1">
              <Cpu className="w-3 h-3 text-indigo-400" />
              Active AML Model
            </span>
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          </div>
          <p className="font-mono font-bold text-indigo-300 text-[11px]">CB-EXP-002</p>
          <p className="text-[10px] text-slate-500">Multimodal Ingested (22.5k)</p>
        </div>
      )}

      {/* User Info & Logout Footer */}
      <div className="p-3 border-t border-white/10 bg-[#070a10]">
        <div className={`flex items-center gap-2 ${isCollapsed ? 'justify-center' : 'justify-between'}`}>
          {!isCollapsed && user && (
            <div className="min-w-0 pr-2">
              <p className="text-xs font-semibold text-white truncate">{user.full_name || user.username}</p>
              <div className="flex items-center gap-1.5">
                <span className={`w-1.5 h-1.5 rounded-full ${user.role === 'ADMIN' ? 'bg-amber-400' : 'bg-emerald-400'}`}></span>
                <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">{user.role}</span>
              </div>
            </div>
          )}

          <Tooltip content="Sign Out" position="right">
            <button
              type="button"
              onClick={onLogout}
              className="p-2 rounded-xl text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 border border-transparent hover:border-rose-500/30 transition-all"
              aria-label="Logout"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </Tooltip>
        </div>
      </div>
    </aside>
  );
}
