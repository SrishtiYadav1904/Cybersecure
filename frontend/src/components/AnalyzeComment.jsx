import React, { useState, useRef } from 'react';
import {
  Scan,
  Image as ImageIcon,
  MessageSquare,
  Upload,
  CheckCircle2,
  AlertCircle,
  FileText,
  ShieldAlert,
  ShieldCheck,
  HeartHandshake,
  ArrowRight,
  RotateCcw,
  Sparkles,
  HelpCircle,
  Plus,
  Trash2,
  Clock,
  User,
  Info
} from 'lucide-react';
import { api } from '../api';
import Button from './ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/Card';
import Badge from './ui/Badge';
import Input from './ui/Input';
import Select from './ui/Select';
import Tabs from './ui/Tabs';
import Toast from './ui/Toast';

// --- Radial Confidence Arc Meter ---
function ConfidenceMeter({ value, isCyberbullying }) {
  const r = 40;
  const cx = 56;
  const cy = 56;
  const startAngle = -210;
  const endAngle = 30;
  const totalArc = endAngle - startAngle; // 240 degrees
  const filled = (value / 100) * totalArc;

  const toRad = (deg) => (deg * Math.PI) / 180;
  const arcPath = (cx, cy, r, startDeg, endDeg) => {
    const s = { x: cx + r * Math.cos(toRad(startDeg)), y: cy + r * Math.sin(toRad(startDeg)) };
    const e = { x: cx + r * Math.cos(toRad(endDeg)), y: cy + r * Math.sin(toRad(endDeg)) };
    const largeArc = endDeg - startDeg > 180 ? 1 : 0;
    return `M ${s.x} ${s.y} A ${r} ${r} 0 ${largeArc} 1 ${e.x} ${e.y}`;
  };

  const trackColor = '#1e293b';
  const fillColor = isCyberbullying
    ? value > 80 ? '#ef4444' : value > 60 ? '#f97316' : '#f59e0b'
    : '#10b981';

  return (
    <svg width="112" height="90" viewBox="0 0 112 90">
      {/* Track */}
      <path
        d={arcPath(cx, cy, r, startAngle, endAngle)}
        fill="none"
        stroke={trackColor}
        strokeWidth="8"
        strokeLinecap="round"
      />
      {/* Fill */}
      <path
        d={arcPath(cx, cy, r, startAngle, startAngle + filled)}
        fill="none"
        stroke={fillColor}
        strokeWidth="8"
        strokeLinecap="round"
        style={{ filter: `drop-shadow(0 0 6px ${fillColor}88)` }}
      />
      {/* Center value */}
      <text x={cx} y={cy + 4} textAnchor="middle" fill="#f8fafc" fontSize="16" fontWeight="700" fontFamily="'JetBrains Mono', monospace">
        {Math.round(value)}%
      </text>
    </svg>
  );
}



export default function AnalyzeComment({ setActiveTab, onIncidentUpdate }) {
  const [activeTabMode, setActiveTabMode] = useState('text'); // 'text' | 'screenshot' | 'chat'
  const [inputText, setInputText] = useState('');
  const [platform, setPlatform] = useState('Instagram');
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [ocrText, setOcrText] = useState('');
  const [rawOcrText, setRawOcrText] = useState('');
  const [savedFilePath, setSavedFilePath] = useState(null);

  // Group chat thread state
  const [chatMessages, setChatMessages] = useState([
    { sender: '@target_user', text: 'Hey everyone, check out my new project demo!', timestamp: '10:01 AM' },
    { sender: '@bully_alpha', text: 'Nobody cares about your garbage project, you complete loser.', timestamp: '10:02 AM' },
    { sender: '@troll_beta', text: 'Tu kitna bada kutta hai, shakal dekh apni.', timestamp: '10:03 AM' }
  ]);
  const [chatSender, setChatSender] = useState('');
  const [chatText, setChatText] = useState('');

  // Status and results
  const [loading, setLoading] = useState(false);
  const [ocrLoading, setOcrLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState(0); // 1: uploaded, 2: ocr, 3: inference, 4: complete
  const [analysisResult, setAnalysisResult] = useState(null);
  const [currentIncidentId, setCurrentIncidentId] = useState(null);
  const [error, setError] = useState(null);
  const [toastMsg, setToastMsg] = useState(null);

  const fileInputRef = useRef(null);

  // Verified benchmark samples for instant evaluation
  const benchmarkSamples = [
    {
      title: "English Appearance Bullying",
      text: "Look at your ugly face in the mirror, nobody in this group likes you.",
      lang: "English"
    },
    {
      title: "Hindi Abuse & Insult",
      text: "तुम बहुत बेकार और मूर्ख इंसान हो, यहाँ से निकल जाओ।",
      lang: "Hindi"
    },
    {
      title: "Hinglish Slang & Harassment",
      text: "Tu kitna bada kutta aur chutiya hai saale, aukat me reh.",
      lang: "Hinglish"
    },
    {
      title: "Threat & Intimidation",
      text: "I will track your IP address and destroy you and your family.",
      lang: "English"
    },
    {
      title: "Non-Cyberbullying (Clean)",
      text: "Thank you so much for explaining the code, this was very helpful!",
      lang: "English"
    }
  ];

  const handleFileSelect = async (file) => {
    if (!file) return;
    if (file.size > 10 * 1024 * 1024) {
      setError('Screenshot exceeds 10MB limit. Please upload a smaller file.');
      return;
    }

    setSelectedFile(file);
    setImagePreview(URL.createObjectURL(file));
    setError(null);
    setOcrLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);
      if (currentIncidentId) {
        formData.append('incident_id', currentIncidentId);
      }

      const ocrResp = await api.uploadImageOCR(formData);
      setOcrText(ocrResp.extracted_text || '');
      setRawOcrText(ocrResp.extracted_text || '');
      setSavedFilePath(ocrResp.file_path || null);
      setToastMsg({ type: 'success', message: 'OCR text extracted successfully. Please review or edit before analysis.' });
    } catch (err) {
      setError(err.message || 'OCR extraction failed. You can paste the text manually.');
    } finally {
      setOcrLoading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  // Run Direct Text Inference
  const handleAnalyzeText = async (customText) => {
    const textToAnalyze = customText || inputText;
    if (!textToAnalyze.trim()) {
      setError('Please provide text content to analyze.');
      return;
    }

    setLoading(true);
    setError(null);
    setLoadingStage(1);

    try {
      setTimeout(() => setLoadingStage(2), 250);
      const payload = {
        text: textToAnalyze.trim(),
        platform,
        incident_id: currentIncidentId
      };
      const resp = await api.analyzeText(payload);
      setLoadingStage(3);
      setAnalysisResult(resp);
      setCurrentIncidentId(resp.incident_id);
      if (onIncidentUpdate) onIncidentUpdate(resp.incident_id);
      setToastMsg({ type: 'success', message: 'Analysis complete. Results and explainability generated.' });
    } catch (err) {
      setError(err.message || 'Text analysis failed. Please verify server connection.');
    } finally {
      setLoading(false);
      setLoadingStage(0);
    }
  };

  // Confirm OCR Screenshot Analysis
  const handleConfirmOCRAnalysis = async () => {
    if (!ocrText.trim()) {
      setError('OCR extracted text cannot be empty.');
      return;
    }

    setLoading(true);
    setError(null);
    setLoadingStage(2);

    try {
      const formData = new FormData();
      formData.append('edited_text', ocrText.trim());
      if (savedFilePath) formData.append('file_path', savedFilePath);
      if (rawOcrText) formData.append('raw_ocr_text', rawOcrText);
      if (currentIncidentId) formData.append('incident_id', currentIncidentId);
      formData.append('platform', platform);

      const resp = await api.confirmImageAnalysis(formData);
      setLoadingStage(3);
      setAnalysisResult(resp);
      setCurrentIncidentId(resp.incident_id);
      if (onIncidentUpdate) onIncidentUpdate(resp.incident_id);
      setToastMsg({ type: 'success', message: 'Screenshot evidence analyzed and stored in incident docket.' });
    } catch (err) {
      setError(err.message || 'Image analysis confirmation failed.');
    } finally {
      setLoading(false);
      setLoadingStage(0);
    }
  };

  // Group Chat Analysis
  const handleAnalyzeChat = async () => {
    if (chatMessages.length === 0) {
      setError('Please add at least one message to the chat thread.');
      return;
    }

    setLoading(true);
    setError(null);
    setLoadingStage(2);

    try {
      const resp = await api.analyzeChat({
        messages: chatMessages,
        platform
      });
      setLoadingStage(3);
      // Format chat result for standard display
      setAnalysisResult({
        is_cyberbullying: resp.is_cyberbullying,
        predicted_class: resp.predicted_class || (resp.is_cyberbullying ? 'Cyberbullying' : 'Non-Cyberbullying'),
        confidence: resp.confidence,
        detected_language: resp.detected_language || 'Multilingual',
        severity: resp.severity || 'MODERATE',
        important_tokens: resp.bullying_messages ? resp.bullying_messages.map(m => m.sender) : [],
        explanation: resp.summary || `Evaluated ${resp.total_messages} messages across conversation thread.`,
        model_version: resp.model_version || 'CB-EXP-002',
        probabilities: resp.probabilities || [
          { category: 'Cyberbullying', probability: resp.confidence },
          { category: 'Non-Cyberbullying', probability: 1 - resp.confidence }
        ],
        recommended_action: resp.recommended_action || 'Preserve group chat export and submit to platform safety.'
      });
      if (resp.incident_id) {
        setCurrentIncidentId(resp.incident_id);
        if (onIncidentUpdate) onIncidentUpdate(resp.incident_id);
      }
      setToastMsg({ type: 'success', message: 'Group chat thread evaluated.' });
    } catch (err) {
      setError(err.message || 'Chat analysis failed.');
    } finally {
      setLoading(false);
      setLoadingStage(0);
    }
  };

  const handleAddChatMessage = () => {
    if (!chatSender.trim() || !chatText.trim()) return;
    setChatMessages([
      ...chatMessages,
      {
        sender: chatSender.trim(),
        text: chatText.trim(),
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
    ]);
    setChatText('');
  };

  const handleResetAnalysis = () => {
    setAnalysisResult(null);
    setInputText('');
    setSelectedFile(null);
    setImagePreview(null);
    setOcrText('');
    setRawOcrText('');
    setSavedFilePath(null);
  };

  const handleStopAndReport = async () => {
    if (!currentIncidentId) {
      setActiveTab('reports');
      return;
    }
    setLoading(true);
    try {
      await api.closeIncident(currentIncidentId);
      setActiveTab('reports');
    } catch (err) {
      setError(err.message || 'Failed to finalize report.');
    } finally {
      setLoading(false);
    }
  };

  const workspaceTabs = [
    { id: 'text', label: 'Paste Text', icon: Scan },
    { id: 'screenshot', label: 'Upload Screenshot', icon: ImageIcon },
    { id: 'chat', label: 'Group Chat', icon: MessageSquare }
  ];

  return (
    <div className="space-y-6 animate-fade-in max-w-5xl mx-auto">
      {/* Toast Alert */}
      {toastMsg && (
        <Toast
          type={toastMsg.type}
          message={toastMsg.message}
          onClose={() => setToastMsg(null)}
        />
      )}

      {/* Error Banner */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
            <span>{error}</span>
          </div>
          <button onClick={() => setError(null)} className="text-slate-400 hover:text-white">✕</button>
        </div>
      )}

      {/* Active Incident Context Header */}
      {currentIncidentId && (
        <div className="p-3.5 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-between text-xs">
          <div className="flex items-center gap-2.5 text-indigo-300">
            <ShieldCheck className="w-4 h-4 text-indigo-400" />
            <span>
              Active Case Context: <b>Incident #{currentIncidentId}</b>
            </span>
          </div>
          <Badge variant="info" size="sm">
            APPENDING EVIDENCE
          </Badge>
        </div>
      )}

      {/* Analysis Workspace Container */}
      {!analysisResult ? (
        <Card className="p-6 space-y-6">
          {/* Header & Controls */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-5">
            <div>
              <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
                <Scan className="w-5 h-5 text-indigo-400" />
                <span>Multilingual Analysis Workspace</span>
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Evaluate suspicious comments, images, or chat logs using production model <b>CB-EXP-002</b>.
              </p>
            </div>

            {/* Platform Selector */}
            <div className="w-full sm:w-48">
              <Select
                label="Target Platform"
                value={platform}
                onChange={(e) => setPlatform(e.target.value)}
                options={[
                  { value: 'Instagram', label: 'Instagram' },
                  { value: 'WhatsApp', label: 'WhatsApp' },
                  { value: 'Twitter', label: 'X / Twitter' },
                  { value: 'Discord', label: 'Discord' },
                  { value: 'Facebook', label: 'Facebook' },
                  { value: 'Other', label: 'Other Social Media' }
                ]}
              />
            </div>
          </div>

          {/* Segmented Mode Switcher */}
          <div className="flex justify-start">
            <Tabs
              tabs={workspaceTabs}
              activeTab={activeTabMode}
              onChange={setActiveTabMode}
              variant="segmented"
            />
          </div>

          {/* 1. Paste Text Mode */}
          {activeTabMode === 'text' && (
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label htmlFor="text-input" className="text-xs font-semibold text-slate-300">
                    Paste comment or message to analyze:
                  </label>
                  <span className="text-[11px] text-slate-500 font-mono">
                    {inputText.length} characters
                  </span>
                </div>
                <textarea
                  id="text-input"
                  rows={4}
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Paste text in English, Hindi (Devanagari), or Hinglish slang here..."
                  className="input-field text-sm font-sans resize-y"
                />
              </div>

              <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                <div className="flex items-center gap-2 text-[11px] text-slate-400">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  <span>Auto-detects English, Hindi & Hinglish slang</span>
                </div>

                <Button
                  variant="primary"
                  onClick={() => handleAnalyzeText()}
                  disabled={loading || !inputText.trim()}
                  isLoading={loading}
                  icon={Sparkles}
                >
                  Analyze Content
                </Button>
              </div>

              {/* Sample benchmark buttons */}
              <div className="pt-4 border-t border-white/10 space-y-2">
                <p className="text-[11px] font-semibold text-slate-400">
                  Or test verified benchmark samples:
                </p>
                <div className="flex flex-wrap gap-2">
                  {benchmarkSamples.map((sample, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => {
                        setInputText(sample.text);
                        handleAnalyzeText(sample.text);
                      }}
                      className="text-[11px] py-1.5 px-3 rounded-xl bg-[#151c2b] hover:bg-[#1e293b] text-slate-300 hover:text-white border border-white/10 hover:border-indigo-500/40 transition-all font-medium"
                    >
                      {sample.title} ({sample.lang})
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* 2. Upload Screenshot Mode */}
          {activeTabMode === 'screenshot' && (
            <div className="space-y-6">
              {/* Drag & Drop Area */}
              <div
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-white/15 hover:border-indigo-500/50 rounded-2xl p-8 text-center bg-[#151c2b]/50 hover:bg-[#151c2b] transition-all cursor-pointer flex flex-col items-center justify-center space-y-2 group"
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".png,.jpg,.jpeg,.webp"
                  onChange={(e) => handleFileSelect(e.target.files[0])}
                  className="hidden"
                />
                <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <Upload className="w-6 h-6" />
                </div>
                <p className="text-sm font-bold text-white">
                  Drag & drop screenshot or <span className="text-indigo-400 underline underline-offset-2">browse files</span>
                </p>
                <p className="text-[11px] text-slate-500">
                  PNG, JPG, JPEG, WEBP up to 10MB
                </p>
              </div>

              {/* Loading progress during OCR */}
              {ocrLoading && (
                <div className="p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs flex items-center justify-center gap-2.5 animate-pulse">
                  <Clock className="w-4 h-4 animate-spin text-indigo-400" />
                  <span>Extracting text via multi-engine OCR pipeline...</span>
                </div>
              )}

              {/* OCR Review & Edit Box (Section 9 Requirement) */}
              {selectedFile && !ocrLoading && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-white/10">
                  <div className="space-y-2">
                    <p className="text-xs font-semibold text-slate-300">Original Screenshot Preview:</p>
                    {imagePreview && (
                      <img
                        src={imagePreview}
                        alt="Screenshot Preview"
                        className="rounded-xl border border-white/10 max-h-60 object-contain w-full bg-black/50"
                      />
                    )}
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <p className="text-xs font-semibold text-slate-300">
                        Extracted OCR Text
                      </p>
                      <span className="text-[10px] text-indigo-400 font-medium">Review & correct if needed</span>
                    </div>

                    <textarea
                      rows={6}
                      value={ocrText}
                      onChange={(e) => setOcrText(e.target.value)}
                      placeholder="OCR text will appear here. Edit any misread words before running detection..."
                      className="input-field text-xs font-mono"
                    />

                    <Button
                      variant="primary"
                      onClick={handleConfirmOCRAnalysis}
                      disabled={loading || !ocrText.trim()}
                      isLoading={loading}
                      className="w-full"
                      icon={Sparkles}
                    >
                      Analyze Extracted Text
                    </Button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* 3. Group Chat Mode */}
          {activeTabMode === 'chat' && (
            <div className="space-y-6">
              {/* Messages feed */}
              <div className="space-y-2.5 max-h-72 overflow-y-auto p-4 rounded-xl bg-[#151c2b] border border-white/5">
                {chatMessages.length === 0 ? (
                  <p className="text-xs text-slate-500 text-center py-6">No messages in chat thread yet.</p>
                ) : (
                  chatMessages.map((msg, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-xl bg-[#0f141f] border border-white/5 flex items-start justify-between gap-3 text-xs"
                    >
                      <div className="space-y-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-indigo-300 font-mono">{msg.sender}</span>
                          <span className="text-[10px] text-slate-500">{msg.timestamp}</span>
                        </div>
                        <p className="text-slate-200">{msg.text}</p>
                      </div>
                      <button
                        type="button"
                        onClick={() => setChatMessages(chatMessages.filter((_, i) => i !== idx))}
                        className="text-slate-500 hover:text-rose-400 p-1"
                        aria-label="Remove message"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  ))
                )}
              </div>

              {/* Add message controls */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                <Input
                  placeholder="Sender (e.g. @bully)"
                  value={chatSender}
                  onChange={(e) => setChatSender(e.target.value)}
                  icon={User}
                />
                <div className="sm:col-span-2 flex gap-2">
                  <Input
                    placeholder="Message content..."
                    value={chatText}
                    onChange={(e) => setChatText(e.target.value)}
                    className="flex-1"
                  />
                  <Button
                    variant="secondary"
                    onClick={handleAddChatMessage}
                    icon={Plus}
                  >
                    Add
                  </Button>
                </div>
              </div>

              <div className="pt-2 border-t border-white/10 flex justify-end">
                <Button
                  variant="primary"
                  onClick={handleAnalyzeChat}
                  disabled={loading || chatMessages.length === 0}
                  isLoading={loading}
                  icon={Sparkles}
                >
                  Analyze Conversation Thread
                </Button>
              </div>
            </div>
          )}

          {/* Honest Step-by-Step Progress State (Section 10) */}
          {loading && (
            <div className="p-4 rounded-xl bg-[#151c2b] border border-white/10 space-y-2 text-xs">
              <p className="font-semibold text-white flex items-center gap-2">
                <Clock className="w-4 h-4 animate-spin text-indigo-400" />
                <span>Processing content inference pipeline</span>
              </p>
              <div className="space-y-1.5 text-slate-300 pl-6 text-[11px]">
                <p className="text-emerald-400">✓ Content received & validated</p>
                <p className={loadingStage >= 2 ? 'text-emerald-400' : 'text-slate-500'}>
                  {loadingStage >= 2 ? '✓ Preprocessing & feature extraction' : '○ Preprocessing & feature extraction'}
                </p>
                <p className={loadingStage >= 3 ? 'text-emerald-400' : 'text-indigo-400 font-semibold animate-pulse'}>
                  {loadingStage >= 3 ? '✓ Multilingual AML model evaluation' : '● Multilingual AML model evaluation'}
                </p>
                <p className="text-slate-500">○ Generating explainability tokens</p>
              </div>
            </div>
          )}
        </Card>
      ) : (
        /* 4. Results View — Premium Forensic Report Style */
        <div className="space-y-5 animate-fade-in">
          {/* Verdict Header Card */}
          <Card className={`overflow-hidden border-0 ${
            analysisResult.is_cyberbullying
              ? 'ring-1 ring-rose-500/40 bg-gradient-to-br from-[#1a0a0a] to-[#0f141f]'
              : 'ring-1 ring-emerald-500/30 bg-gradient-to-br from-[#061a12] to-[#0f141f]'
          }`}>
            {/* Status banner */}
            <div className={`h-1.5 w-full ${analysisResult.is_cyberbullying ? 'bg-gradient-to-r from-rose-700 via-red-500 to-orange-500' : 'bg-gradient-to-r from-emerald-700 via-emerald-500 to-teal-400'}`} />

            <div className="p-6">
              <div className="flex flex-col md:flex-row gap-6 items-center md:items-start">

                {/* Left: Radial Confidence Arc Meter */}
                <div className="flex flex-col items-center shrink-0">
                  <ConfidenceMeter
                    value={analysisResult.confidence * 100}
                    isCyberbullying={analysisResult.is_cyberbullying}
                  />
                  <p className="text-[10px] text-slate-500 mt-1 uppercase tracking-wider">Confidence</p>
                </div>

                {/* Right: Verdict Details */}
                <div className="flex-1 min-w-0 text-center md:text-left space-y-3">
                  {/* Verdict label */}
                  <div>
                    <div className="flex items-center justify-center md:justify-start gap-2 mb-1">
                      {analysisResult.is_cyberbullying
                        ? <ShieldAlert className="w-5 h-5 text-rose-400" />
                        : <ShieldCheck className="w-5 h-5 text-emerald-400" />
                      }
                      <span className={`text-xs font-bold uppercase tracking-widest font-mono ${
                        analysisResult.is_cyberbullying ? 'text-rose-400' : 'text-emerald-400'
                      }`}>
                        {analysisResult.is_cyberbullying ? 'Cyberbullying Detected' : 'No Cyberbullying'}
                      </span>
                    </div>
                    <h3 className="text-2xl font-extrabold text-white tracking-tight">{analysisResult.predicted_class}</h3>
                  </div>

                  {/* Meta row */}
                  <div className="flex flex-wrap gap-3 justify-center md:justify-start">
                    <div className="px-2.5 py-1 rounded-lg bg-white/5 border border-white/10 text-xs">
                      <span className="text-slate-500">Language: </span>
                      <span className="text-indigo-300 font-bold font-mono">{analysisResult.detected_language}</span>
                    </div>
                    <div className={`px-2.5 py-1 rounded-lg border text-xs font-bold font-mono ${
                      analysisResult.severity === 'SEVERE' || analysisResult.severity === 'CRITICAL'
                        ? 'bg-rose-500/15 border-rose-500/30 text-rose-300'
                        : analysisResult.severity === 'HIGH'
                          ? 'bg-orange-500/15 border-orange-500/30 text-orange-300'
                          : analysisResult.severity === 'MODERATE'
                            ? 'bg-amber-500/15 border-amber-500/30 text-amber-300'
                            : 'bg-emerald-500/15 border-emerald-500/30 text-emerald-300'
                    }`}>
                      {analysisResult.severity}
                    </div>
                    <div className="px-2.5 py-1 rounded-lg bg-white/5 border border-white/10 text-xs font-mono text-slate-400">
                      {analysisResult.model_version}
                    </div>
                  </div>

                  {/* Recommended action */}
                  <div className={`p-3 rounded-xl text-xs leading-relaxed border ${
                    analysisResult.is_cyberbullying
                      ? 'bg-rose-500/10 border-rose-500/20 text-rose-200'
                      : 'bg-emerald-500/10 border-emerald-500/20 text-emerald-200'
                  }`}>
                    <span className="font-semibold">Recommended: </span>
                    {analysisResult.recommended_action}
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {analysisResult.predicted_class === 'Threat/Intimidation' && (
            <Card className="border border-rose-500/40 bg-rose-950/30 p-5 space-y-3" role="alert">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-5 h-5 shrink-0 text-rose-300 mt-0.5" />
                <div className="space-y-2">
                  <h4 className="text-sm font-bold text-rose-200">Urgent safety review</h4>
                  <p className="text-xs leading-relaxed text-rose-100/90">
                    The model flagged possible threatening language. This is an automated signal,
                    not a verified finding. Review the message and its context. If someone is in
                    immediate danger, contact local emergency services directly.
                  </p>
                  <p className="text-[11px] text-rose-200/70">
                    CyberGuard will not contact authorities or share this message automatically.
                  </p>
                  <Button
                    variant="danger"
                    onClick={() => setActiveTab('help')}
                    icon={ShieldAlert}
                  >
                    Request human review
                  </Button>
                </div>
              </div>
            </Card>
          )}

          {/* XAI + Explanation Card */}
          <Card className="p-5 space-y-4">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-violet-400" />
              Explainable AI — Salient Term Attribution
            </h4>

            {analysisResult.important_tokens && analysisResult.important_tokens.length > 0 ? (
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs text-slate-400 shrink-0">Offensive triggers:</span>
                {analysisResult.important_tokens.map((tok, i) => (
                  <span
                    key={i}
                    className="px-3 py-1 rounded-lg text-xs font-bold font-mono border"
                    style={{
                      background: `rgba(239,68,68,${0.12 + i * 0.04})`,
                      borderColor: `rgba(239,68,68,${0.3 + i * 0.05})`,
                      color: `hsl(${5 - i * 5}, 85%, ${70 - i * 4}%)`
                    }}
                  >
                    "{tok}"
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-400 italic">No specific offensive terms isolated — classification is context-driven.</p>
            )}

            <div className="p-4 rounded-xl bg-[#151c2b] border border-white/5 text-xs text-slate-300 leading-relaxed space-y-1.5">
              <p><span className="text-white font-semibold">Model Rationale: </span>{analysisResult.explanation}</p>
              <p className="text-[11px] text-slate-500 font-mono">
                Architecture: PCA(30d) + Contextual(384d) → Stacking Ensemble {analysisResult.model_version}
              </p>
            </div>
          </Card>

          {/* Probability Distribution Card */}
          {analysisResult.probabilities && (
            <Card className="p-5 space-y-4">
              <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                Multi-Class Probability Distribution
              </h4>
              <div className="space-y-2.5">
                {analysisResult.probabilities
                  .slice()
                  .sort((a, b) => b.probability - a.probability)
                  .map((p, idx) => {
                    const pct = Math.min(p.probability * 100, 100);
                    const isTop = idx === 0;
                    const barColor =
                      p.category === 'Non-Cyberbullying' ? '#10b981' :
                      p.category === 'Threat' || p.category === 'Hate-Speech' ? '#ef4444' :
                      p.category === 'Harassment' ? '#f97316' :
                      p.category === 'Appearance-based' ? '#f59e0b' :
                      '#8b5cf6';

                    return (
                      <div key={idx} className="space-y-1">
                        <div className="flex items-center justify-between text-xs">
                          <span className={`font-medium ${isTop ? 'text-white' : 'text-slate-400'}`}>
                            {p.category}
                          </span>
                          <span className="font-mono font-bold" style={{ color: isTop ? barColor : '#64748b' }}>
                            {pct.toFixed(1)}%
                          </span>
                        </div>
                        <div className="h-2 rounded-full overflow-hidden bg-[#151c2b]">
                          <div
                            className="h-full rounded-full transition-all duration-700 ease-out"
                            style={{
                              width: `${pct}%`,
                              background: isTop
                                ? `linear-gradient(90deg, ${barColor}bb, ${barColor})`
                                : `${barColor}55`
                            }}
                          />
                        </div>
                      </div>
                    );
                })}
              </div>
            </Card>
          )}

          {/* Next-Step Action Buttons */}
          <Card className="p-5">
            <div className="flex flex-wrap items-center justify-center gap-3">
              <Button
                variant="secondary"
                onClick={handleResetAnalysis}
                icon={RotateCcw}
              >
                Analyze Another
              </Button>

              <Button
                variant="primary"
                onClick={handleStopAndReport}
                disabled={loading}
                icon={FileText}
              >
                Generate Forensic Report
              </Button>

              <Button
                variant="outline"
                onClick={() => setActiveTab('support')}
                icon={HeartHandshake}
              >
                Get Support AI
              </Button>

              {analysisResult.is_cyberbullying && (
                <Button
                  variant="danger"
                  onClick={() => setActiveTab('help')}
                  icon={ShieldAlert}
                >
                  Consultant Escalation
                </Button>
              )}
            </div>
            <p className="text-[11px] text-slate-500 text-center mt-3">
              Evidence automatically timestamped and preserved in your incident repository.
            </p>
          </Card>
        </div>
      )}
    </div>
  );
}
