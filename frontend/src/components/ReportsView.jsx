import React, { useEffect, useState } from 'react';
import {
  FileText,
  Download,
  ShieldCheck,
  Calendar,
  Layers,
  ArrowRight,
  ExternalLink,
  Plus,
  Clock,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { api } from '../api';
import Button from './ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/Card';
import Badge from './ui/Badge';
import Skeleton from './ui/Skeleton';
import EmptyState from './ui/EmptyState';
import Modal from './ui/Modal';
import Toast from './ui/Toast';

export default function ReportsView({ setActiveTab }) {
  const [reports, setReports] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloadingId, setDownloadingId] = useState(null);
  const [generatingId, setGeneratingId] = useState(null);
  const [isGenerateModalOpen, setIsGenerateModalOpen] = useState(false);
  const [selectedIncidentForReport, setSelectedIncidentForReport] = useState('');
  const [error, setError] = useState(null);
  const [toastMsg, setToastMsg] = useState(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const [reportsData, incidentsData] = await Promise.all([
        api.listReports().catch(() => []),
        api.listIncidents().catch(() => [])
      ]);
      setReports(reportsData);
      setIncidents(incidentsData);
      if (incidentsData.length > 0) {
        setSelectedIncidentForReport(incidentsData[0].id);
      }
    } catch (err) {
      setError(err.message || 'Failed to load forensic reports.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleDownload = async (report) => {
    setDownloadingId(report.id);
    try {
      const blob = await api.downloadReport(report.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `CyberGuard_${report.report_code}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      setToastMsg({ type: 'success', message: `Report ${report.report_code} downloaded.` });
    } catch (err) {
      setError('Download failed: ' + (err.message || 'Error fetching PDF file'));
    } finally {
      setDownloadingId(null);
    }
  };

  const handleGenerateReport = async () => {
    if (!selectedIncidentForReport) return;
    setGeneratingId(selectedIncidentForReport);
    try {
      await api.generateReport(selectedIncidentForReport);
      setToastMsg({ type: 'success', message: 'New forensic PDF report compiled successfully!' });
      setIsGenerateModalOpen(false);
      await loadData();
    } catch (err) {
      setError(err.message || 'Report generation failed.');
    } finally {
      setGeneratingId(null);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in max-w-6xl mx-auto">
      {/* Toast */}
      {toastMsg && (
        <Toast
          type={toastMsg.type}
          message={toastMsg.message}
          onClose={() => setToastMsg(null)}
        />
      )}

      {/* Error */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-400" />
            <span>{error}</span>
          </div>
          <button onClick={() => setError(null)} className="text-slate-400 hover:text-white">✕</button>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <FileText className="w-6 h-6 text-indigo-400" />
            <span>Certified Forensic Reports</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Download certified PDF dossiers containing evidence screenshots, timestamps, XAI model attributions, and statutory complaint filing instructions.
          </p>
        </div>

        {incidents.length > 0 && (
          <Button
            variant="primary"
            onClick={() => setIsGenerateModalOpen(true)}
            icon={Plus}
          >
            Compile New Report
          </Button>
        )}
      </div>

      {/* Reports Grid */}
      {loading ? (
        <Skeleton variant="card" count={3} />
      ) : reports.length === 0 ? (
        <EmptyState
          icon={FileText}
          title="No Forensic Reports Compiled Yet"
          description="When you finalize an incident investigation, CyberGuard compiles a structured court-ready PDF artifact. Analyze content or finalize an active case to generate your first dossier."
          actionLabel="Analyze New Evidence"
          onAction={() => setActiveTab('analyze')}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {reports.map(report => {
            const summary = report.summary_json || {};
            const sev = (summary.severity || '').toLowerCase();
            const badgeVariant =
              sev === 'severe' || sev === 'critical' ? 'severe' :
              sev === 'high' ? 'harmful' :
              sev === 'moderate' ? 'concerning' : 'safe';

            return (
              <Card
                key={report.id}
                className="p-5 border-white/10 flex flex-col justify-between space-y-4 hover:border-indigo-500/40 transition-all"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-mono font-bold text-xs text-indigo-300 bg-indigo-500/15 px-2.5 py-1 rounded-lg border border-indigo-500/30">
                      {report.report_code}
                    </span>
                    <span className="text-[11px] text-slate-500 font-mono">
                      {new Date(report.generated_at).toLocaleString()}
                    </span>
                  </div>

                  <div>
                    <h3 className="text-sm font-bold text-white">
                      Forensic Incident Dossier #{report.incident_id}
                    </h3>
                    <p className="text-xs text-slate-400 mt-0.5">
                      Platform: <b>{summary.platform || 'Cross-platform'}</b> • Certified Forensic Hash
                    </p>
                  </div>

                  <div className="p-3.5 rounded-xl bg-[#151c2b] border border-white/5 space-y-1.5 text-xs text-slate-300">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Classification:</span>
                      <span className="font-bold text-white">{summary.primary_category || 'Evaluated Content'}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Severity:</span>
                      <Badge variant={badgeVariant} size="sm">
                        {summary.severity || 'EVALUATED'}
                      </Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Model Certainty:</span>
                      <span className="font-mono text-emerald-400 font-bold">
                        {summary.confidence ? `${(summary.confidence * 100).toFixed(1)}%` : 'Active Stack'}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="pt-3 border-t border-white/10 flex items-center justify-between">
                  <span className="text-[11px] text-emerald-400 flex items-center gap-1.5 font-medium">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    Verified PDF Document
                  </span>

                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => handleDownload(report)}
                    isLoading={downloadingId === report.id}
                    icon={Download}
                  >
                    Download PDF
                  </Button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      {/* Guided Report Generation Modal */}
      <Modal
        isOpen={isGenerateModalOpen}
        onClose={() => setIsGenerateModalOpen(false)}
        title="Compile Forensic PDF Dossier"
        description="Select an active or past incident case. The system will compile all preserved screenshots, OCR extractions, model probabilities, and legal filing steps into a certified PDF."
        footer={
          <>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => setIsGenerateModalOpen(false)}
            >
              Cancel
            </Button>
            <Button
              variant="primary"
              size="sm"
              onClick={handleGenerateReport}
              isLoading={!!generatingId}
              icon={FileText}
            >
              Generate PDF
            </Button>
          </>
        }
      >
        <div className="space-y-4">
          <label className="text-xs font-semibold text-slate-300 block">
            Select Case File to Compile:
          </label>
          <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
            {incidents.map(inc => (
              <div
                key={inc.id}
                onClick={() => setSelectedIncidentForReport(inc.id)}
                className={`
                  p-3 rounded-xl border text-xs cursor-pointer transition-all flex items-center justify-between
                  ${selectedIncidentForReport === inc.id
                    ? 'bg-[#151c2b] border-indigo-500/60 shadow-sm'
                    : 'bg-[#0f141f] border-white/10 hover:border-white/20'}
                `}
              >
                <div>
                  <span className="font-mono font-bold text-indigo-400">
                    {inc.incident_code || `INC-${inc.id}`}
                  </span>
                  <p className="text-slate-300 mt-0.5">{inc.primary_category || 'Investigation Case'} • {inc.platform}</p>
                </div>
                <Badge variant="outline" size="sm">
                  {inc.status || 'ACTIVE'}
                </Badge>
              </div>
            ))}
          </div>
        </div>
      </Modal>
    </div>
  );
}
