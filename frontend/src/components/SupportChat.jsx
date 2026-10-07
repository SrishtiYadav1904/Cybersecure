import React, { useEffect, useState, useRef } from 'react';
import {
  HeartHandshake,
  Send,
  PhoneCall,
  ShieldCheck,
  AlertTriangle,
  Info,
  BookOpen,
  User,
  Bot,
  Sparkles,
  ExternalLink,
  ShieldAlert,
  Clock
} from 'lucide-react';
import { api } from '../api';
import Button from './ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/Card';
import Badge from './ui/Badge';
import Input from './ui/Input';
import Modal from './ui/Modal';

export default function SupportChat({ setActiveTab }) {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [wellbeingStatus, setWellbeingStatus] = useState(null);
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [initLoading, setInitLoading] = useState(true);
  const [isCrisisModalOpen, setIsCrisisModalOpen] = useState(false);
  const messagesEndRef = useRef(null);

  const feelingsPrompts = [
    { label: "I'm overwhelmed", prompt: "I am feeling overwhelmed by abusive messages online and need advice on what to do first." },
    { label: "I'm worried about threats", prompt: "Someone is threatening to leak my personal details or harm me. How do I protect myself?" },
    { label: "How do I block safely?", prompt: "How can I block someone on social media without losing evidence for police or legal action?" },
    { label: "How to report on 1930?", prompt: "Can you explain how to file a formal cybercrime report in India on the 1930 portal?" }
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    async function initSupport() {
      try {
        const [sessionResp, resResp] = await Promise.all([
          api.startSupportSession(),
          api.getEmergencyResources()
        ]);
        setSessionId(sessionResp.id);
        setMessages(sessionResp.messages || []);
        setWellbeingStatus(sessionResp.wellbeing_indicators || null);
        setResources(resResp || []);
      } catch (err) {
        console.error('Error initializing support session:', err);
      } finally {
        setInitLoading(false);
        scrollToBottom();
      }
    }
    initSupport();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (textToSend) => {
    const text = textToSend || inputText;
    if (!text.trim() || loading) return;

    const userText = text.trim();
    if (!textToSend) setInputText('');

    // Optimistic user message append
    const tempMsg = {
      id: Date.now(),
      sender: 'user',
      content: userText,
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, tempMsg]);
    setLoading(true);

    try {
      const resp = await api.sendSupportMessage({
        session_id: sessionId,
        message: userText
      });
      setMessages(prev => [...prev, resp]);
      if (resp.wellbeing_signals) {
        setWellbeingStatus(resp.wellbeing_signals);
        if (resp.wellbeing_signals.stress_level === 'CRITICAL') {
          setIsCrisisModalOpen(true);
        }
      }
    } catch (err) {
      alert('Error sending message: ' + (err.message || 'Server error'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-emerald-400 mb-1">
            <HeartHandshake className="w-5 h-5" />
            <span className="text-xs font-semibold uppercase tracking-wider">Confidential Support Space</span>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            Grounded Wellbeing & Safety Assistant
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Private, non-judgmental guidance for emotional de-escalation, evidence preservation, and statutory cybercrime reporting.
          </p>
        </div>

        {/* Wellbeing Status Indicator */}
        {wellbeingStatus && (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#151c2b] border border-white/10 text-xs">
            <span className="text-slate-400">Calibrated Support Level:</span>
            <span className={`font-bold font-mono ${
              wellbeingStatus.stress_level === 'CRITICAL' ? 'text-rose-400 animate-pulse' :
              wellbeingStatus.stress_level === 'ELEVATED' ? 'text-amber-400' : 'text-emerald-400'
            }`}>
              {wellbeingStatus.stress_level}
            </span>
          </div>
        )}
      </div>

      {/* Main Grid: Chat Feed & Helplines Sidebar */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Chat Feed (8 cols) */}
        <div className="lg:col-span-8 flex flex-col h-[650px]">
          <Card className="flex-1 flex flex-col p-5 border-white/10 h-full overflow-hidden">
            {/* Quick feelings prompt chips */}
            <div className="pb-3 border-b border-white/10">
              <p className="text-[11px] font-semibold text-slate-400 mb-2">
                How can we support you right now?
              </p>
              <div className="flex flex-wrap gap-1.5">
                {feelingsPrompts.map((item, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSendMessage(item.prompt)}
                    disabled={loading}
                    className="text-[11px] py-1 px-2.5 rounded-lg bg-[#151c2b] hover:bg-emerald-950/40 text-slate-300 hover:text-emerald-300 border border-white/10 hover:border-emerald-500/40 transition-all font-medium"
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Messages Scroll Area */}
            <div className="flex-1 overflow-y-auto space-y-4 py-4 pr-2">
              {initLoading ? (
                <div className="text-center py-24 text-xs text-slate-400 space-y-2">
                  <div className="w-8 h-8 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin mx-auto"></div>
                  <p>Connecting to grounded safety agent...</p>
                </div>
              ) : (
                messages.map((m, idx) => {
                  const isUser = m.sender === 'user';
                  return (
                    <div
                      key={idx}
                      className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}
                    >
                      {!isUser && (
                        <div className="w-8 h-8 rounded-xl bg-emerald-500/15 text-emerald-400 flex items-center justify-center font-bold text-xs shrink-0 border border-emerald-500/30">
                          <Bot className="w-4 h-4" />
                        </div>
                      )}

                      <div className={`max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed space-y-2 ${
                        isUser
                          ? 'bg-gradient-to-r from-indigo-600 to-indigo-500 text-white rounded-br-none shadow-md shadow-indigo-600/20'
                          : 'bg-[#151c2b] text-slate-200 border border-white/10 rounded-bl-none'
                      }`}>
                        <div className="whitespace-pre-wrap">{m.content}</div>

                        {/* Grounded RAG Sources */}
                        {m.rag_sources && m.rag_sources.length > 0 && (
                          <div className="pt-2.5 border-t border-white/10 space-y-1">
                            <span className="text-[10px] text-emerald-400 font-semibold uppercase flex items-center gap-1">
                              <BookOpen className="w-3 h-3" />
                              Referenced Safety Source:
                            </span>
                            <div className="flex flex-wrap gap-1.5 mt-1">
                              {m.rag_sources.map((src, sIdx) => (
                                <span
                                  key={sIdx}
                                  className="text-[10px] px-2 py-0.5 rounded bg-[#0f141f] text-slate-300 border border-white/10 font-mono"
                                >
                                  {src.title}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        <span className="text-[10px] text-slate-400 block text-right font-mono">
                          {new Date(m.created_at || Date.now()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>

                      {isUser && (
                        <div className="w-8 h-8 rounded-xl bg-slate-800 text-slate-300 flex items-center justify-center font-bold text-xs shrink-0 border border-white/10">
                          <User className="w-4 h-4" />
                        </div>
                      )}
                    </div>
                  );
                })
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Form */}
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSendMessage();
              }}
              className="pt-3 border-t border-white/10 flex gap-2"
            >
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Ask about blocking, filing police reports, evidence retention, or feeling safe..."
                className="input-field text-xs flex-1"
              />
              <Button
                type="submit"
                variant="primary"
                size="sm"
                disabled={loading || !inputText.trim()}
                isLoading={loading}
                icon={Send}
              >
                Send
              </Button>
            </form>
          </Card>
        </div>

        {/* Helplines & Emergency Sidebar (4 cols) */}
        <div className="lg:col-span-4 space-y-4">
          <Card className="p-5 space-y-4 border-white/10">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <PhoneCall className="w-4 h-4 text-rose-400" />
              <span>National Crisis & Legal Helplines</span>
            </h3>

            <div className="space-y-3">
              {resources.map((res, i) => (
                <div
                  key={i}
                  className="p-3.5 rounded-xl bg-[#151c2b] border border-white/5 space-y-1.5 text-xs"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white">{res.name}</span>
                    {res.is_emergency && (
                      <span className="text-[9px] bg-rose-500/20 text-rose-300 px-1.5 py-0.5 rounded font-bold font-mono">
                        24x7 TOLL-FREE
                      </span>
                    )}
                  </div>
                  {res.contact_number && (
                    <p className="text-indigo-300 font-mono font-bold text-xs flex items-center gap-1.5">
                      <PhoneCall className="w-3.5 h-3.5 text-indigo-400" />
                      {res.contact_number}
                    </p>
                  )}
                  <p className="text-[11px] text-slate-400 leading-tight">
                    {res.description}
                  </p>
                </div>
              ))}
            </div>

            <div className="pt-2 border-t border-white/10">
              <Button
                variant="danger"
                size="sm"
                onClick={() => setActiveTab('help')}
                className="w-full"
                icon={ShieldAlert}
              >
                Escalate to Certified Consultant
              </Button>
            </div>
          </Card>

          {/* Privacy & Non-Medical Disclaimer Card */}
          <div className="p-4 rounded-xl bg-[#0f141f] border border-white/5 space-y-1.5 text-[11px] text-slate-400 leading-relaxed">
            <div className="flex items-center gap-1.5 text-slate-300 font-semibold">
              <Info className="w-3.5 h-3.5 text-indigo-400" />
              <span>Privacy & Medical Boundary</span>
            </div>
            <p>
              Support AI provides grounded information and safety guidelines. It is not a mental health therapist or medical provider. In immediate danger, call 112 or local emergency services.
            </p>
          </div>
        </div>
      </div>

      {/* Emergency Crisis Intervention Modal */}
      <Modal
        isOpen={isCrisisModalOpen}
        onClose={() => setIsCrisisModalOpen(false)}
        title="Immediate Safety Support Available"
        description="Our AI detected indicators of elevated distress or severe cyber intimidation. Please remember you are not alone, and free confidential human help is available 24x7."
        footer={
          <Button
            variant="primary"
            size="sm"
            onClick={() => setIsCrisisModalOpen(false)}
          >
            I Understand
          </Button>
        }
      >
        <div className="space-y-4 text-xs">
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-200 space-y-2">
            <h4 className="font-bold text-white flex items-center gap-2">
              <PhoneCall className="w-4 h-4 text-rose-400" />
              <span>Tele-MANAS National Counseling Helpline: 14416</span>
            </h4>
            <p className="text-[11px] leading-relaxed">
              Govt. of India 24x7 toll-free mental health helpline providing free, confidential psychological support in multiple regional languages.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-200 space-y-2">
            <h4 className="font-bold text-white flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-indigo-400" />
              <span>National Cybercrime Helpline: 1930</span>
            </h4>
            <p className="text-[11px] leading-relaxed">
              Official portal (cybercrime.gov.in) for reporting online abuse, financial fraud, impersonation, and non-consensual media sharing.
            </p>
          </div>
        </div>
      </Modal>
    </div>
  );
}
