import React, { useEffect, useState } from 'react';
import {
  ClipboardList,
  ShieldAlert,
  User,
  Phone,
  Mail,
  ExternalLink,
  CheckCircle2,
  Clock,
  Layers,
  Search
} from 'lucide-react';
import { api } from '../api';
import Button from './ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/Card';
import Badge from './ui/Badge';
import Input from './ui/Input';
import Skeleton from './ui/Skeleton';
import EmptyState from './ui/EmptyState';

export default function ConsultantPortal({ setActiveTab }) {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadCases() {
      try {
        const data = await api.getEscalatedCases();
        setCases(data);
      } catch (err) {
        setError(err.message || 'Access denied or failed to load consultant queue.');
      } finally {
        setLoading(false);
      }
    }
    loadCases();
  }, []);

  const filteredCases = cases.filter(c =>
    (c.request_code || '').toLowerCase().includes(search.toLowerCase()) ||
    (c.full_name || '').toLowerCase().includes(search.toLowerCase()) ||
    (c.platform || '').toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6 animate-fade-in max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <ClipboardList className="w-6 h-6 text-indigo-400" />
            <span>Consultant Triage Queue</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Certified consultant case reviews, perpetrator account dossiers, and risk evaluations.
          </p>
        </div>

        <Badge variant="info" size="md">
          ROLE: CONSULTANT / ADMIN
        </Badge>
      </div>

      {error ? (
        <Card className="p-8 text-center text-rose-300 text-xs border-rose-500/30">
          ⚠️ {error}
        </Card>
      ) : loading ? (
        <Skeleton variant="card" count={3} />
      ) : cases.length === 0 ? (
        <EmptyState
          icon={CheckCircle2}
          title="No Pending Cases in Queue"
          description="All escalated victim inquiries and perpetrator dossiers have been assigned or resolved."
        />
      ) : (
        <div className="space-y-4">
          {/* Quick Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
            <Card className="p-4">
              <span className="text-xs text-slate-400 font-semibold uppercase">Pending Triage</span>
              <p className="text-2xl font-bold font-mono text-white mt-1">{cases.length}</p>
            </Card>

            <Card className="p-4">
              <span className="text-xs text-slate-400 font-semibold uppercase">High Priority</span>
              <p className="text-2xl font-bold font-mono text-rose-400 mt-1">
                {cases.filter(c => c.num_bullies > 2 || c.platform === 'WhatsApp').length}
              </p>
            </Card>

            <Card className="p-4">
              <span className="text-xs text-slate-400 font-semibold uppercase">Multi-Perpetrator Rings</span>
              <p className="text-2xl font-bold font-mono text-amber-400 mt-1">
                {cases.filter(c => c.num_bullies > 1).length}
              </p>
            </Card>
          </div>

          {/* Search */}
          <Input
            placeholder="Search by case reference code, reporter name, or platform..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            icon={Search}
          />

          {/* Case Dossiers */}
          <div className="space-y-4">
            {filteredCases.map(c => (
              <Card key={c.id} className="p-5 space-y-4 border-white/10 hover:border-indigo-500/30 transition-all">
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-white/10 pb-3">
                  <div className="flex items-center gap-2.5">
                    <span className="font-mono text-xs font-bold text-indigo-400 bg-indigo-500/15 px-2.5 py-1 rounded-lg border border-indigo-500/30">
                      {c.request_code}
                    </span>
                    <Badge variant="severe" size="sm">
                      {c.status || 'ESCALATED'}
                    </Badge>
                  </div>
                  <span className="text-[11px] text-slate-500 font-mono">
                    {new Date(c.created_at).toLocaleString()}
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                  <div className="space-y-1">
                    <span className="text-slate-400 font-semibold">Victim Contact:</span>
                    <p className="text-white font-medium">{c.full_name} ({c.email})</p>
                    {c.phone && <p className="text-slate-400 font-mono">📞 {c.phone}</p>}
                  </div>

                  <div className="space-y-1">
                    <span className="text-slate-400 font-semibold">Context:</span>
                    <p className="text-white font-medium">Platform: {c.platform}</p>
                    {c.account_username && <p className="text-slate-400">Handle: {c.account_username}</p>}
                  </div>

                  <div className="space-y-1">
                    <span className="text-slate-400 font-semibold">Perpetrators:</span>
                    <p className="text-rose-400 font-bold font-mono">{c.num_bullies} Identified Accounts</p>
                  </div>
                </div>

                {/* Bully Accounts Preview */}
                {c.bully_accounts && c.bully_accounts.length > 0 && (
                  <div className="p-3 rounded-xl bg-[#151c2b] border border-white/5 space-y-1.5 text-xs">
                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                      Cataloged Bully Handles:
                    </span>
                    <div className="flex flex-wrap gap-2">
                      {c.bully_accounts.map((b, bIdx) => (
                        <span key={bIdx} className="px-2 py-0.5 rounded bg-rose-500/15 text-rose-300 font-mono text-xs border border-rose-500/30">
                          {b.handle || 'Unknown'} {b.profile_url ? `(${b.profile_url})` : ''}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {c.additional_notes && (
                  <p className="text-xs text-slate-300 italic bg-[#0f141f] p-3 rounded-xl border border-white/5">
                    "{c.additional_notes}"
                  </p>
                )}
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
