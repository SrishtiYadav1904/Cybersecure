import React, { useState } from 'react';
import { api } from '../api';

export default function AnalyzeChat({ setActiveTab, onIncidentUpdate }) {
  const [platform, setPlatform] = useState('WhatsApp');
  const [messages, setMessages] = useState([
    { sender: '@bully_user', text: 'You are completely useless, nobody in this group likes you.', timestamp: '10:02 AM' },
    { sender: 'Victim', text: 'Please leave me alone, I did not do anything to you.', timestamp: '10:03 AM' },
    { sender: '@bully_user', text: 'Shut up or we will track your address and teach you a lesson.', timestamp: '10:04 AM' },
    { sender: '@troll_2', text: 'Yeah you clown, cry more, look at your pathetic face.', timestamp: '10:05 AM' }
  ]);

  const [newSender, setNewSender] = useState('');
  const [newText, setNewText] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatResult, setChatResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAddMessage = () => {
    if (!newSender.trim() || !newText.trim()) return;
    setMessages([
      ...messages,
      {
        sender: newSender.trim(),
        text: newText.trim(),
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
    ]);
    setNewText('');
  };

  const handleRemoveMessage = (index) => {
    setMessages(messages.filter((_, i) => i !== index));
  };

  const handleAnalyzeChat = async () => {
    if (messages.length === 0) {
      setError('Please add at least one message.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const resp = await api.analyzeChat({
        messages,
        platform
      });
      setChatResult(resp);
      if (onIncidentUpdate) onIncidentUpdate(resp.incident_id);
    } catch (err) {
      setError(err.message || 'Chat analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <span>💬</span>
          <span>Conversation & Chat Transcript Forensics</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Analyze sequential chat streams for repeated targeting, escalation trajectories, and coordinated harassment.
        </p>
      </div>

      {error && (
        <div className="p-3 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
          <span>⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {/* Message Sequence Builder */}
      <div className="glass-panel p-6 border border-white/10 space-y-6">
        <div className="flex items-center justify-between border-b border-white/10 pb-4">
          <h3 className="text-sm font-bold text-white tracking-wide uppercase">
            Sequential Chat Thread ({messages.length} Messages)
          </h3>
          <div className="flex items-center gap-2">
            <span className="text-[11px] text-slate-400">Platform:</span>
            <select
              value={platform}
              onChange={(e) => setPlatform(e.target.value)}
              className="bg-slate-900 border border-white/10 text-xs text-slate-200 rounded-lg px-2.5 py-1 outline-none"
            >
              <option value="WhatsApp">WhatsApp</option>
              <option value="Instagram DM">Instagram DM</option>
              <option value="Discord">Discord Server</option>
              <option value="Telegram">Telegram Group</option>
            </select>
          </div>
        </div>

        {/* Message Feed */}
        <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5 flex items-start justify-between gap-3"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-indigo-400 font-mono">{m.sender}</span>
                  <span className="text-[10px] text-slate-500">{m.timestamp}</span>
                </div>
                <p className="text-xs text-slate-200">{m.text}</p>
              </div>
              <button
                onClick={() => handleRemoveMessage(idx)}
                className="text-slate-500 hover:text-rose-400 text-xs px-2 py-1"
              >
                ✕
              </button>
            </div>
          ))}
        </div>

        {/* Add Message Form */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 pt-4 border-t border-white/10">
          <div>
            <input
              type="text"
              placeholder="Sender handle (e.g. @bully)"
              value={newSender}
              onChange={(e) => setNewSender(e.target.value)}
              className="input-field text-xs font-mono"
            />
          </div>
          <div className="sm:col-span-2">
            <input
              type="text"
              placeholder="Type or paste chat message..."
              value={newText}
              onChange={(e) => setNewText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAddMessage()}
              className="input-field text-xs"
            />
          </div>
          <div>
            <button
              type="button"
              onClick={handleAddMessage}
              className="btn-secondary w-full text-xs"
            >
              Add Message
            </button>
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            onClick={handleAnalyzeChat}
            disabled={loading || messages.length === 0}
            className="btn-primary"
          >
            {loading ? 'Evaluating Context & Escalation...' : 'Run Conversation Forensics'}
          </button>
        </div>
      </div>

      {/* Results Card */}
      {chatResult && (
        <div className="glass-panel p-6 border border-white/10 space-y-6 animate-fade-in">
          <div className="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 pb-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
                  {chatResult.primary_category}
                </span>
                <span className="text-xs text-slate-400 font-mono">
                  Confidence: {(chatResult.overall_confidence * 100).toFixed(1)}%
                </span>
              </div>
              <h3 className="text-lg font-bold text-white mt-1">Context Analysis Finding</h3>
            </div>

            {chatResult.escalation_detected && (
              <div className="px-3 py-1 rounded-lg bg-rose-500/20 border border-rose-500/40 text-rose-300 text-xs font-bold flex items-center gap-1.5">
                <span>⚠️</span>
                <span>Escalation Trajectory Detected</span>
              </div>
            )}
          </div>

          {/* Repeated Harassment Finding (Section 14 & 15 requirement) */}
          <div className="p-4 rounded-xl bg-slate-900/60 border border-white/5 space-y-2">
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wide">
              Behavioral Pattern Finding:
            </h4>
            <p className="text-xs text-slate-200 leading-relaxed">
              {chatResult.repeated_targeting_summary}
            </p>
            {chatResult.active_bullies.length > 0 && (
              <p className="text-[11px] text-slate-400">
                Active antagonists identified in stream: <b>{chatResult.active_bullies.join(', ')}</b>
              </p>
            )}
          </div>

          {/* Incident Assessment */}
          <div className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-500/30 space-y-1">
            <p className="text-xs font-bold text-indigo-300">Assessment:</p>
            <p className="text-xs text-slate-200">{chatResult.incident_assessment}</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/40 border border-white/5 space-y-1">
            <p className="text-xs font-bold text-slate-400">Recommended Safety Action:</p>
            <p className="text-xs text-slate-300">{chatResult.recommended_safety_action}</p>
          </div>

          {/* Message-wise Classifications */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Segmented Message Classifications:
            </h4>
            <div className="space-y-2">
              {chatResult.analyzed_messages.map((m, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-xl bg-slate-900/40 border border-white/5 flex items-center justify-between gap-3 text-xs"
                >
                  <div className="space-y-0.5 max-w-xl">
                    <span className="font-bold text-slate-300">{m.sender}:</span>
                    <span className="text-slate-400 ml-2">"{m.text}"</span>
                  </div>
                  <div className="text-right">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                      m.is_bullying ? 'bg-rose-500/20 text-rose-300' : 'bg-slate-800 text-slate-400'
                    }`}>
                      {m.predicted_class}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Tri-Choice Actions */}
          <div className="pt-4 border-t border-white/10 flex flex-wrap justify-end gap-3">
            <button
              onClick={() => setActiveTab('reports')}
              className="btn-primary"
            >
              <span>📄</span>
              <span>View Incidents & Reports</span>
            </button>
            <button
              onClick={() => setActiveTab('help')}
              className="btn-danger"
            >
              <span>🚨</span>
              <span>Escalate to Consultant</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
