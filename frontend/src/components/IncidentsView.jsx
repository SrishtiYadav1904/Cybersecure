import React, { useEffect, useState } from 'react';
import {
  ShieldAlert,
  Search,
  Filter,
  ArrowUpDown,
  Plus,
  FileText,
  Clock,
  CheckCircle,
  AlertTriangle,
  ChevronRight,
  ExternalLink,
  Layers,
  Sparkles,
  Calendar,
  Share2
} from 'lucide-react';
import { api } from '../api';
import Button from './ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/Card';
import Badge from './ui/Badge';
import Input from './ui/Input';
import Select from './ui/Select';
import Tabs from './ui/Tabs';
import Skeleton from './ui/Skeleton';
import EmptyState from './ui/EmptyState';

export default function IncidentsView({ setActiveTab, onSelectIncident }) {
  const [incidents, setIncidents] = useState([]);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [selectedDetailTab, setSelectedDetailTab] = useState('overview'); // overview, evidence, timeline, analysis

  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [severityFilter, setSeverityFilter] = useState('ALL');
  const [platformFilter, setPlatformFilter] = useState('ALL');
  const [error, setError] = useState(null);

  const loadIncidents = async () => {
    setLoading(true);
    try {
      const data = await api.listIncidents();
      setIncidents(data);
      if (data.length > 0 && !selectedIncident) {
        loadIncidentDetails(data[0].id);
      }
    } catch (err) {
      setError(err.message || 'Failed to load incidents.');
    } finally {
      setLoading(false);
    }
  };

  const loadIncidentDetails = async (id) => {
    setDetailLoading(true);
    try {
      const details = await api.getIncident(id);
      setSelectedIncident(details);
      if (onSelectIncident) onSelectIncident(id);
    } catch (err) {
      console.error('Error fetching incident details:', err);
    } finally {
      setDetailLoading(false);
    }
  };

  useEffect(() => {
    loadIncidents();
  }, []);

  const handleCloseAndGenerateReport = async (incidentId) => {
    setActionLoading(true);
    try {
      await api.closeIncident(incidentId);
      await loadIncidentDetails(incidentId);
      await loadIncidents();
      setActiveTab('reports');
    } catch (err) {
      setError(err.message || 'Failed to finalize report.');
    } finally {
      setActionLoading(false);
    }
  };

  // Filtered & Searched Incidents
  const filteredIncidents = incidents.filter(inc => {
    const matchesSearch =
      (inc.incident_code || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (inc.primary_category || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (inc.platform || '').toLowerCase().includes(searchQuery.toLowerCase());

    const matchesSeverity =
      severityFilter === 'ALL' || (inc.severity || '').toUpperCase() === severityFilter;

    const matchesPlatform =
      platformFilter === 'ALL' || (inc.platform || '').toLowerCase() === platformFilter.toLowerCase();

    return matchesSearch && matchesSeverity && matchesPlatform;
  });

  const detailTabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'evidence', label: 'Evidence Vault' },
    { id: 'timeline', label: 'Timeline' },
    { id: 'analysis', label: 'Model Evaluation' }
  ];

  return (
    <div className="space-y-6 animate-fade-in max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <ShieldAlert className="w-6 h-6 text-indigo-400" />
            <span>Case Management & Evidence Vault</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Certified evidence preservation with OCR extractions, timestamps, and model attribution records.
          </p>
        </div>

        <Button
          variant="primary"
          onClick={() => setActiveTab('analyze')}
          icon={Plus}
        >
          New Analysis Case
        </Button>
      </div>

      {/* Filter and Search Bar (Section 33) */}
      <Card className="p-4">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <Input
            placeholder="Search incident code, category, or platform..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            icon={Search}
          />

          <Select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            options={[
              { value: 'ALL', label: 'All Severities' },
              { value: 'SEVERE', label: 'Severe / Critical' },
              { value: 'HIGH', label: 'High' },
              { value: 'MODERATE', label: 'Moderate' },
              { value: 'LOW', label: 'Low / Safe' }
            ]}
          />

          <Select
            value={platformFilter}
            onChange={(e) => setPlatformFilter(e.target.value)}
            options={[
              { value: 'ALL', label: 'All Platforms' },
              { value: 'Instagram', label: 'Instagram' },
              { value: 'WhatsApp', label: 'WhatsApp' },
              { value: 'Twitter', label: 'X / Twitter' },
              { value: 'Discord', label: 'Discord' },
              { value: 'Facebook', label: 'Facebook' }
            ]}
          />
        </div>
      </Card>

      {/* Main Split Layout: Incidents List & Incident Details */}
      {loading ? (
        <Skeleton variant="card" count={3} />
      ) : incidents.length === 0 ? (
        <EmptyState
          icon={ShieldAlert}
          title="No Preserved Incidents Yet"
          description="When you analyze suspicious comments or screenshots, they will appear here as formal case files with complete forensic lineage."
          actionLabel="Start New Analysis"
          onAction={() => setActiveTab('analyze')}
        />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Incidents Master List (5 cols) */}
          <div className="lg:col-span-5 space-y-3">
            <div className="flex items-center justify-between text-xs text-slate-400 px-1">
              <span>{filteredIncidents.length} cases found</span>
              <span className="font-mono">Real-time sync</span>
            </div>

            <div className="space-y-2.5 max-h-[700px] overflow-y-auto pr-1">
              {filteredIncidents.map(inc => {
                const isSelected = selectedIncident?.id === inc.id;
                const sev = (inc.severity || '').toLowerCase();
                const badgeVariant =
                  sev === 'severe' || sev === 'critical' ? 'severe' :
                  sev === 'high' ? 'harmful' :
                  sev === 'moderate' ? 'concerning' : 'safe';

                return (
                  <div
                    key={inc.id}
                    onClick={() => loadIncidentDetails(inc.id)}
                    className={`
                      p-4 rounded-xl border transition-all cursor-pointer text-left
                      ${isSelected
                        ? 'bg-[#151c2b] border-indigo-500/60 shadow-md shadow-indigo-500/10'
                        : 'bg-[#0f141f] border-white/10 hover:border-white/20 hover:bg-[#151c2b]/70'}
                    `}
                  >
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="font-mono font-bold text-xs text-indigo-400">
                        {inc.incident_code || `INC-${inc.id}`}
                      </span>
                      <Badge variant={badgeVariant} size="sm">
                        {inc.severity || 'EVALUATED'}
                      </Badge>
                    </div>

                    <h4 className="text-sm font-semibold text-white truncate">
                      {inc.primary_category || 'Cyberbullying Case'}
                    </h4>

                    <div className="flex items-center justify-between text-[11px] text-slate-400 mt-2 pt-2 border-t border-white/5">
                      <span>Platform: <b>{inc.platform}</b></span>
                      <span>{new Date(inc.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Incident Detail View (7 cols) */}
          <div className="lg:col-span-7">
            {detailLoading ? (
              <Card className="p-8">
                <Skeleton variant="card" count={2} />
              </Card>
            ) : selectedIncident ? (
              <Card className="p-6 space-y-6">
                {/* Detail Header */}
                <div className="flex flex-wrap items-start justify-between gap-4 border-b border-white/10 pb-5">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold text-indigo-400 px-2.5 py-0.5 rounded bg-indigo-500/15 border border-indigo-500/30">
                        {selectedIncident.incident_code || `INC-${selectedIncident.id}`}
                      </span>
                      <Badge
                        variant={
                          selectedIncident.status === 'CLOSED' ? 'default' : 'safe'
                        }
                        size="sm"
                      >
                        {selectedIncident.status || 'ACTIVE'}
                      </Badge>
                    </div>

                    <h3 className="text-xl font-bold text-white mt-2">
                      {selectedIncident.primary_category || 'Preserved Evidence Case'}
                    </h3>
                  </div>

                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => handleCloseAndGenerateReport(selectedIncident.id)}
                    isLoading={actionLoading}
                    icon={FileText}
                  >
                    Generate Certified Report
                  </Button>
                </div>

                {/* Detail Tab Navigation */}
                <Tabs
                  tabs={detailTabs}
                  activeTab={selectedDetailTab}
                  onChange={setSelectedDetailTab}
                  variant="underline"
                />

                {/* Tab 1: Overview */}
                {selectedDetailTab === 'overview' && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-3 text-xs">
                      <div className="p-3.5 rounded-xl bg-[#151c2b] border border-white/5 space-y-1">
                        <span className="text-slate-400">Target Platform:</span>
                        <p className="font-bold text-white">{selectedIncident.platform}</p>
                      </div>
                      <div className="p-3.5 rounded-xl bg-[#151c2b] border border-white/5 space-y-1">
                        <span className="text-slate-400">Created Timestamp:</span>
                        <p className="font-mono text-white">
                          {new Date(selectedIncident.created_at).toLocaleString()}
                        </p>
                      </div>
                      <div className="p-3.5 rounded-xl bg-[#151c2b] border border-white/5 space-y-1">
                        <span className="text-slate-400">Model Confidence:</span>
                        <p className="font-mono text-emerald-400 font-bold">
                          {selectedIncident.confidence ? `${(selectedIncident.confidence * 100).toFixed(1)}%` : 'Evaluated'}
                        </p>
                      </div>
                      <div className="p-3.5 rounded-xl bg-[#151c2b] border border-white/5 space-y-1">
                        <span className="text-slate-400">Preserved Items:</span>
                        <p className="font-mono text-indigo-300 font-bold">
                          {selectedIncident.messages?.length || 1} evidence items
                        </p>
                      </div>
                    </div>

                    <div className="p-4 rounded-xl bg-[#151c2b] border border-white/5 space-y-2">
                      <span className="text-xs font-semibold text-slate-300 block">Case Summary:</span>
                      <p className="text-xs text-slate-300 leading-relaxed">
                        {selectedIncident.notes || 'This incident contains certified forensic evidence. Model confidence and contextual markers are stored in the database.'}
                      </p>
                    </div>
                  </div>
                )}

                {/* Tab 2: Evidence Vault */}
                {selectedDetailTab === 'evidence' && (
                  <div className="space-y-4">
                    {selectedIncident.screenshot_path ? (
                      <div className="space-y-2">
                        <p className="text-xs font-semibold text-slate-300">Preserved Screenshot Attachment:</p>
                        <img
                          src={`/api/uploads/${selectedIncident.screenshot_path.split(/[\\/]/).pop()}`}
                          alt="Evidence screenshot"
                          className="rounded-xl border border-white/10 max-h-72 object-contain w-full bg-black/50"
                          onError={(e) => {
                            e.target.style.display = 'none';
                          }}
                        />
                      </div>
                    ) : null}

                    <div className="space-y-2">
                      <p className="text-xs font-semibold text-slate-300">Target Analyzed Text:</p>
                      <div className="p-4 rounded-xl bg-[#151c2b] border border-white/5 font-mono text-xs text-slate-200 whitespace-pre-wrap">
                        {selectedIncident.ocr_extracted_text || selectedIncident.text || 'No text extracted.'}
                      </div>
                    </div>
                  </div>
                )}

                {/* Tab 3: Timeline */}
                {selectedDetailTab === 'timeline' && (
                  <div className="space-y-3">
                    <p className="text-xs font-semibold text-slate-300">Chronological Events:</p>
                    <div className="space-y-2 border-l-2 border-indigo-500/30 pl-4 ml-2">
                      <div className="relative space-y-1">
                        <div className="w-2.5 h-2.5 rounded-full bg-indigo-500 absolute -left-[21px] top-1"></div>
                        <span className="text-[10px] text-slate-500 font-mono">
                          {new Date(selectedIncident.created_at).toLocaleString()}
                        </span>
                        <p className="text-xs font-semibold text-white">Incident Initialized</p>
                        <p className="text-[11px] text-slate-400">Content submitted via {selectedIncident.platform}</p>
                      </div>

                      <div className="relative space-y-1 pt-3">
                        <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 absolute -left-[21px] top-4"></div>
                        <span className="text-[10px] text-slate-500 font-mono">
                          {new Date(selectedIncident.created_at).toLocaleString()}
                        </span>
                        <p className="text-xs font-semibold text-white">AML Model Classification</p>
                        <p className="text-[11px] text-slate-400">
                          Tagged as <b>{selectedIncident.primary_category}</b> with {selectedIncident.severity} severity
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Tab 4: Model Evaluation */}
                {selectedDetailTab === 'analysis' && (
                  <div className="space-y-3">
                    <div className="p-4 rounded-xl bg-[#151c2b] border border-white/5 space-y-2 text-xs">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-white">Inference Engine Version</span>
                        <span className="font-mono text-indigo-300">CB-EXP-002</span>
                      </div>
                      <p className="text-slate-400 leading-relaxed">
                        Multimodal stacking ensemble using PCA dimensionality reduction, GloVe word embeddings, and dense contextual sentence embeddings.
                      </p>
                    </div>

                    <div className="pt-2 flex gap-3">
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => setActiveTab('support')}
                        icon={HeartHandshake}
                      >
                        Ask Support AI about this Incident
                      </Button>
                    </div>
                  </div>
                )}
              </Card>
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
}
