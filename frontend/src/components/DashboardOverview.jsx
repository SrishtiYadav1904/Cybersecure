import React, { useEffect, useState, useRef } from 'react';
import {
  Scan,
  Image as ImageIcon,
  MessageSquare,
  HeartHandshake,
  ShieldCheck,
  FileText,
  AlertTriangle,
  ArrowRight,
  Clock,
  ExternalLink,
  Cpu,
  PhoneCall
} from 'lucide-react';
import { api } from '../api';
import Button from './ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/Card';
import Badge from './ui/Badge';
import Skeleton from './ui/Skeleton';

// Count-up animation hook
function useCountUp(target, duration = 900, enabled = true) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    if (!enabled || target === 0) { setValue(target); return; }
    const start = performance.now();
    const tick = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      setValue(Math.round(eased * target));
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, [target, duration, enabled]);
  return value;
}


export default function DashboardOverview({ setActiveTab, user }) {
  const [stats, setStats] = useState({
    incidentsCount: 0,
    reportsCount: 0,
    activeIncidents: [],
    reportsList: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [incidents, reports] = await Promise.all([
          api.listIncidents().catch(() => []),
          api.listReports().catch(() => [])
        ]);
        setStats({
          incidentsCount: incidents.length,
          reportsCount: reports.length,
          activeIncidents: incidents.slice(0, 4),
          reportsList: reports.slice(0, 3)
        });
      } catch (e) {
        console.error('Failed to load dashboard metrics:', e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  const displayName = user?.full_name || user?.username || 'Analyst';

  // Animated metric counters (fire after data loads)
  const animatedIncidents = useCountUp(stats.incidentsCount, 900, !loading);
  const animatedReports = useCountUp(stats.reportsCount, 750, !loading);

  return (
    <div className="space-y-8 animate-fade-in">
      {/* 1. Header Greeting & Primary Action Cards (Section 7) */}
      <div className="space-y-4">
        <div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {getGreeting()}, {displayName}
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Your safety dashboard. Monitor incidents, analyze multilingual content, and access grounded support.
          </p>
        </div>

        {/* Primary Action Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
          <Card
            interactive
            onClick={() => setActiveTab('analyze')}
            className="p-4 group border-indigo-500/20 hover:border-indigo-500/50 bg-gradient-to-br from-[#0f141f] to-indigo-950/20"
          >
            <div className="w-10 h-10 rounded-xl bg-indigo-500/15 text-indigo-400 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
              <Scan className="w-5 h-5" />
            </div>
            <h3 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors flex items-center justify-between">
              <span>Analyze Text</span>
              <ArrowRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 -translate-x-1 group-hover:translate-x-0 transition-all text-indigo-400" />
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Test comments in EN, Hindi & Hinglish slang.
            </p>
          </Card>

          <Card
            interactive
            onClick={() => setActiveTab('analyze')}
            className="p-4 group border-indigo-500/20 hover:border-indigo-500/50 bg-gradient-to-br from-[#0f141f] to-indigo-950/20"
          >
            <div className="w-10 h-10 rounded-xl bg-indigo-500/15 text-indigo-400 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
              <ImageIcon className="w-5 h-5" />
            </div>
            <h3 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors flex items-center justify-between">
              <span>Upload Screenshot</span>
              <ArrowRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 -translate-x-1 group-hover:translate-x-0 transition-all text-indigo-400" />
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Extract OCR text with review & forensic hash.
            </p>
          </Card>

          <Card
            interactive
            onClick={() => setActiveTab('analyze')}
            className="p-4 group border-indigo-500/20 hover:border-indigo-500/50 bg-gradient-to-br from-[#0f141f] to-indigo-950/20"
          >
            <div className="w-10 h-10 rounded-xl bg-indigo-500/15 text-indigo-400 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
              <MessageSquare className="w-5 h-5" />
            </div>
            <h3 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors flex items-center justify-between">
              <span>Analyze Group Chat</span>
              <ArrowRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 -translate-x-1 group-hover:translate-x-0 transition-all text-indigo-400" />
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Multi-participant chat timeline evaluation.
            </p>
          </Card>

          <Card
            interactive
            onClick={() => setActiveTab('support')}
            className="p-4 group border-emerald-500/20 hover:border-emerald-500/50 bg-gradient-to-br from-[#0f141f] to-emerald-950/20"
          >
            <div className="w-10 h-10 rounded-xl bg-emerald-500/15 text-emerald-400 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
              <HeartHandshake className="w-5 h-5" />
            </div>
            <h3 className="text-sm font-bold text-white group-hover:text-emerald-300 transition-colors flex items-center justify-between">
              <span>Get Support AI</span>
              <ArrowRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 -translate-x-1 group-hover:translate-x-0 transition-all text-emerald-400" />
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Private wellbeing advice & statutory filing tips.
            </p>
          </Card>
        </div>
      </div>

      {/* 2. Safety Overview Metric Tiles (Real Backend Data) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3.5">
        {/* Tile 1: Incidents */}
        <Card className="p-4 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-indigo-500 rounded-l-2xl" />
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Active Incidents</span>
            <ShieldCheck className="w-4 h-4 text-indigo-400" />
          </div>
          {loading ? (
            <Skeleton variant="text" className="w-16 h-8" />
          ) : (
            <p className="text-3xl font-bold font-mono text-white tabular-nums">{animatedIncidents}</p>
          )}
          <span className="text-[11px] text-slate-400 mt-1 block">Preserved evidence cases</span>
        </Card>

        {/* Tile 2: Reports */}
        <Card className="p-4 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-violet-500 rounded-l-2xl" />
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Forensic Reports</span>
            <FileText className="w-4 h-4 text-violet-400" />
          </div>
          {loading ? (
            <Skeleton variant="text" className="w-16 h-8" />
          ) : (
            <p className="text-3xl font-bold font-mono text-white tabular-nums">{animatedReports}</p>
          )}
          <span className="text-[11px] text-slate-400 mt-1 block">Certified PDF artifacts</span>
        </Card>

        {/* Tile 3: Model */}
        <Card className="p-4 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-cyan-500 rounded-l-2xl" />
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Production Model</span>
            <Cpu className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-xl font-bold font-mono text-cyan-300">CB-EXP-002</p>
          <div className="flex items-center gap-1.5 mt-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-[11px] text-emerald-400">Multimodal Stack (22.5k)</span>
          </div>
        </Card>

        {/* Tile 4: Languages */}
        <Card className="p-4 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-amber-500 rounded-l-2xl" />
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Languages</span>
            <span className="text-[10px] font-mono text-amber-400 font-bold">3 CODES</span>
          </div>
          <p className="text-xl font-bold text-white">EN / HI / Hinglish</p>
          <span className="text-[11px] text-slate-400 mt-1 block">Code-mixed slang tolerant</span>
        </Card>
      </div>

      {/* 3. Incidents Timeline & Calm Support Callout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Recent Incidents Timeline */}
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>
                  <Clock className="w-4 h-4 text-indigo-400" />
                  <span>Recent Preserved Incidents</span>
                </CardTitle>
                <CardDescription>
                  Chronological record of processed evidence and classification results.
                </CardDescription>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setActiveTab('incidents')}
              >
                <span>View All</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Button>
            </CardHeader>

            <CardContent>
              {loading ? (
                <Skeleton variant="card" count={2} />
              ) : stats.activeIncidents.length === 0 ? (
                <div className="text-center py-10 bg-[#151c2b]/50 rounded-xl border border-dashed border-white/10 space-y-2">
                  <ShieldCheck className="w-8 h-8 text-slate-500 mx-auto" />
                  <p className="text-xs font-semibold text-slate-300">No active incidents yet</p>
                  <p className="text-[11px] text-slate-500 max-w-sm mx-auto">
                    When you analyze comments or screenshots, they will appear here as preserved evidence cases.
                  </p>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => setActiveTab('analyze')}
                    className="mt-3"
                  >
                    Analyze New Content
                  </Button>
                </div>
              ) : (
                <div className="space-y-2.5">
                  {stats.activeIncidents.map(inc => {
                    const sev = (inc.severity || '').toLowerCase();
                    const badgeVariant =
                      sev === 'severe' || sev === 'critical' ? 'severe' :
                      sev === 'high' ? 'harmful' :
                      sev === 'moderate' ? 'concerning' : 'safe';

                    return (
                      <div
                        key={inc.id}
                        onClick={() => setActiveTab('incidents')}
                        className="relative pl-4 pr-3.5 py-3.5 rounded-xl bg-[#151c2b] hover:bg-[#1a2233] border border-white/5 hover:border-white/15 transition-all cursor-pointer flex items-center justify-between overflow-hidden"
                      >
                        {/* Severity left bar */}
                        <div className={`absolute left-0 top-0 bottom-0 w-1 ${
                          sev === 'severe' || sev === 'critical' ? 'bg-rose-500' :
                          sev === 'high' ? 'bg-orange-500' :
                          sev === 'moderate' ? 'bg-amber-500' : 'bg-emerald-500'
                        }`} />

                        <div className="flex items-center gap-3 min-w-0">
                          <div className="w-9 h-9 rounded-xl bg-indigo-500/15 text-indigo-300 flex items-center justify-center font-bold text-xs shrink-0">
                            {inc.platform ? inc.platform[0].toUpperCase() : 'W'}
                          </div>
                          <div className="min-w-0">
                            <h4 className="text-xs font-bold text-white font-mono truncate">
                              {inc.incident_code || `INC-${inc.id}`}
                            </h4>
                            <p className="text-[11px] text-slate-400 truncate">
                              {inc.primary_category || 'Content analysis'} • {inc.platform || 'Direct input'}
                            </p>
                          </div>
                        </div>

                        <div className="text-right shrink-0 flex items-center gap-3">
                          <Badge variant={badgeVariant} size="sm">
                            {inc.severity || 'EVALUATED'}
                          </Badge>
                          <span className="text-[11px] text-slate-500 hidden sm:inline font-mono">
                            {new Date(inc.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>

                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Calm Support & Immediate Protocol */}
        <div className="space-y-4">
          {/* Calm Support Trigger Card (Section 7) */}
          <Card className="p-5 border-emerald-500/25 bg-gradient-to-br from-[#0f141f] to-emerald-950/20 space-y-3">
            <div className="flex items-center gap-2.5 text-emerald-400">
              <HeartHandshake className="w-5 h-5" />
              <h3 className="text-sm font-bold text-white">Need someone to talk to?</h3>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Cyberbullying can be distressing. Our AI assistant offers calm, private, non-clinical guidance and safety steps.
            </p>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setActiveTab('support')}
              className="w-full !border-emerald-500/40 text-emerald-300 hover:bg-emerald-500/10"
            >
              Open Support AI
            </Button>
          </Card>

          {/* Immediate Evidence Protocol Card */}
          <Card className="p-5 space-y-3">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              <span>Evidence Preservation Rules</span>
            </h3>
            <ul className="space-y-2.5 text-xs text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-indigo-400 font-bold">1.</span>
                <span><b>Preserve uncropped screenshots</b>: Retain full context, timestamps, and usernames.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-indigo-400 font-bold">2.</span>
                <span><b>Do not retaliate</b>: Aggressive responses often complicate statutory complaint verification.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-indigo-400 font-bold">3.</span>
                <span><b>Helpline 1930 / 14416</b>: Report cyber fraud or call Tele-MANAS for confidential counseling.</span>
              </li>
            </ul>

            <div className="pt-2 border-t border-white/10">
              <Button
                variant="danger"
                size="sm"
                onClick={() => setActiveTab('help')}
                className="w-full"
              >
                <span>Request Consultant Escalation</span>
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
