import React, { useState } from 'react';
import {
  AlertOctagon,
  ArrowRight,
  ArrowLeft,
  CheckCircle2,
  User,
  Plus,
  Trash2,
  ShieldAlert,
  Send,
  ExternalLink,
  Lock
} from 'lucide-react';
import { api } from '../api';
import Button from './ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/Card';
import Badge from './ui/Badge';
import Input from './ui/Input';
import Select from './ui/Select';
import Toast from './ui/Toast';

export default function HelpRequestForm({ setActiveTab, incidentId }) {
  const [currentStep, setCurrentStep] = useState(1); // 1: Personal & Platform, 2: Bullies, 3: Review & Submit
  const [fullName, setFullName] = useState('');
  const [age, setAge] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [accountUsername, setAccountUsername] = useState('');
  const [platform, setPlatform] = useState('Instagram');
  const [numBullies, setNumBullies] = useState(1);
  const [bullyAccounts, setBullyAccounts] = useState([
    { handle: '', profile_url: '', platform: 'Instagram' }
  ]);
  const [whatsappGroup, setWhatsappGroup] = useState('');
  const [whatsappNumbers, setWhatsappNumbers] = useState('');
  const [notes, setNotes] = useState('');

  const [loading, setLoading] = useState(false);
  const [submittedCode, setSubmittedCode] = useState(null);
  const [error, setError] = useState(null);

  const handleNumBulliesChange = (n) => {
    const count = Math.max(1, Math.min(10, parseInt(n) || 1));
    setNumBullies(count);
    const updated = [...bullyAccounts];
    while (updated.length < count) {
      updated.push({ handle: '', profile_url: '', platform });
    }
    setBullyAccounts(updated.slice(0, count));
  };

  const handleBullyFieldChange = (index, field, value) => {
    const updated = [...bullyAccounts];
    updated[index][field] = value;
    setBullyAccounts(updated);
  };

  const handleAddBully = () => {
    if (bullyAccounts.length < 10) {
      setBullyAccounts([...bullyAccounts, { handle: '', profile_url: '', platform }]);
      setNumBullies(bullyAccounts.length + 1);
    }
  };

  const handleRemoveBully = (index) => {
    if (bullyAccounts.length > 1) {
      const updated = bullyAccounts.filter((_, i) => i !== index);
      setBullyAccounts(updated);
      setNumBullies(updated.length);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const numbersList = whatsappNumbers.split(',').map(s => s.trim()).filter(Boolean);
      const payload = {
        incident_id: incidentId || null,
        full_name: fullName.trim(),
        age: age ? parseInt(age) : null,
        email: email.trim(),
        phone: phone.trim() || null,
        account_username: accountUsername.trim() || null,
        platform,
        num_bullies: bullyAccounts.length,
        bully_accounts: bullyAccounts,
        whatsapp_group_name: platform === 'WhatsApp' ? whatsappGroup : null,
        whatsapp_numbers: platform === 'WhatsApp' ? numbersList : null,
        additional_notes: notes.trim() || null
      };

      const resp = await api.submitHelpRequest(payload);
      setSubmittedCode(resp.request_code);
    } catch (err) {
      setError(err.message || 'Submission failed. Please check required fields.');
    } finally {
      setLoading(false);
    }
  };

  // Success Confirmation View
  if (submittedCode) {
    return (
      <div className="max-w-2xl mx-auto my-12 animate-fade-in">
        <Card className="p-8 text-center space-y-4 border-emerald-500/30">
          <div className="w-16 h-16 rounded-2xl bg-emerald-500/15 text-emerald-400 flex items-center justify-center mx-auto">
            <CheckCircle2 className="w-8 h-8" />
          </div>

          <h2 className="text-2xl font-bold text-white tracking-tight">
            Consultant Escalation Case Created
          </h2>

          <p className="text-xs text-slate-300 max-w-md mx-auto leading-relaxed">
            Your case file and cataloged perpetrator accounts have been securely encrypted and routed to certified human consultants for triage.
          </p>

          <div className="p-4 rounded-xl bg-[#151c2b] border border-white/10 max-w-sm mx-auto">
            <span className="text-[11px] text-slate-400 block uppercase tracking-wider">Tracking Reference Code</span>
            <p className="font-mono text-xl font-extrabold text-indigo-300 mt-1">{submittedCode}</p>
          </div>

          <div className="pt-4 flex items-center justify-center gap-3">
            <Button
              variant="secondary"
              onClick={() => setActiveTab('dashboard')}
            >
              Return to Dashboard
            </Button>
            <Button
              variant="primary"
              onClick={() => setActiveTab('support')}
            >
              Open Support AI
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in max-w-3xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <AlertOctagon className="w-6 h-6 text-rose-400" />
          <span>Consultant Escalation & Bully Cataloging Form</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Escalate serious threats, doxxing, or coordinated harassment to certified forensic consultants.
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
          ⚠️ {error}
        </div>
      )}

      {/* Stepper Progress */}
      <div className="grid grid-cols-3 gap-2 text-center text-xs font-semibold">
        <div className={`p-2.5 rounded-xl border transition-all ${
          currentStep >= 1 ? 'bg-indigo-600/20 text-indigo-300 border-indigo-500/40' : 'bg-[#151c2b] text-slate-500 border-white/5'
        }`}>
          1. Context & Contact
        </div>
        <div className={`p-2.5 rounded-xl border transition-all ${
          currentStep >= 2 ? 'bg-indigo-600/20 text-indigo-300 border-indigo-500/40' : 'bg-[#151c2b] text-slate-500 border-white/5'
        }`}>
          2. Perpetrator Accounts
        </div>
        <div className={`p-2.5 rounded-xl border transition-all ${
          currentStep >= 3 ? 'bg-indigo-600/20 text-indigo-300 border-indigo-500/40' : 'bg-[#151c2b] text-slate-500 border-white/5'
        }`}>
          3. Review & Submit
        </div>
      </div>

      <Card className="p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Step 1: Personal & Platform Context */}
          {currentStep === 1 && (
            <div className="space-y-4">
              <h3 className="text-sm font-bold text-white border-b border-white/10 pb-3 flex items-center gap-2">
                <Lock className="w-4 h-4 text-indigo-400" />
                <span>Your Contact & Platform Context</span>
              </h3>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Input
                  label="Full Name"
                  required
                  placeholder="Your legal or preferred name"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                />
                <Input
                  label="Contact Email"
                  type="email"
                  required
                  placeholder="Where consultants can reach you"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <Input
                  label="Age"
                  type="number"
                  placeholder="Helps determine minor safety protocols"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                />
                <Input
                  label="Phone Number"
                  placeholder="Optional, for emergency contact"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                />
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
                    { value: 'Other', label: 'Other Platform' }
                  ]}
                />
                <Input
                  label="Your Account Username"
                  placeholder="@yourhandle"
                  value={accountUsername}
                  onChange={(e) => setAccountUsername(e.target.value)}
                />
              </div>

              {platform === 'WhatsApp' && (
                <div className="p-4 rounded-xl bg-[#151c2b] border border-white/5 space-y-3">
                  <Input
                    label="WhatsApp Group Name"
                    placeholder="Exact group title if harassment occurred in a group"
                    value={whatsappGroup}
                    onChange={(e) => setWhatsappGroup(e.target.value)}
                  />
                  <Input
                    label="Perpetrator Phone Numbers"
                    placeholder="Comma-separated: +91 98765 43210, +91 91234 56789"
                    value={whatsappNumbers}
                    onChange={(e) => setWhatsappNumbers(e.target.value)}
                  />
                </div>
              )}

              <div className="flex justify-end pt-4">
                <Button
                  variant="primary"
                  onClick={() => {
                    if (!fullName.trim() || !email.trim()) {
                      setError('Please provide your name and email before proceeding.');
                      return;
                    }
                    setError(null);
                    setCurrentStep(2);
                  }}
                  icon={ArrowRight}
                >
                  Continue to Perpetrator Accounts
                </Button>
              </div>
            </div>
          )}

          {/* Step 2: Bully / Perpetrator Accounts Catalog */}
          {currentStep === 2 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-white/10 pb-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 text-rose-400" />
                  <span>Catalog Bully / Perpetrator Accounts ({bullyAccounts.length})</span>
                </h3>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={handleAddBully}
                  icon={Plus}
                >
                  Add Another Account
                </Button>
              </div>

              <div className="space-y-3">
                {bullyAccounts.map((account, index) => (
                  <div
                    key={index}
                    className="p-4 rounded-xl bg-[#151c2b] border border-white/10 space-y-3"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-indigo-300">
                        Perpetrator #{index + 1}
                      </span>
                      {bullyAccounts.length > 1 && (
                        <button
                          type="button"
                          onClick={() => handleRemoveBully(index)}
                          className="text-slate-500 hover:text-rose-400 text-xs p-1"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <Input
                        label="Username / Handle"
                        required
                        placeholder="@harasser_account"
                        value={account.handle}
                        onChange={(e) => handleBullyFieldChange(index, 'handle', e.target.value)}
                      />
                      <Input
                        label="Profile URL"
                        placeholder="https://instagram.com/..."
                        value={account.profile_url}
                        onChange={(e) => handleBullyFieldChange(index, 'profile_url', e.target.value)}
                      />
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex items-center justify-between pt-4">
                <Button
                  variant="secondary"
                  onClick={() => setCurrentStep(1)}
                  icon={ArrowLeft}
                >
                  Back
                </Button>
                <Button
                  variant="primary"
                  onClick={() => {
                    const hasEmpty = bullyAccounts.some(b => !b.handle.trim());
                    if (hasEmpty) {
                      setError('Please specify at least a handle or identifier for each perpetrator.');
                      return;
                    }
                    setError(null);
                    setCurrentStep(3);
                  }}
                  icon={ArrowRight}
                >
                  Continue to Review
                </Button>
              </div>
            </div>
          )}

          {/* Step 3: Review & Submit */}
          {currentStep === 3 && (
            <div className="space-y-4">
              <h3 className="text-sm font-bold text-white border-b border-white/10 pb-3 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>Review Case & Additional Context</span>
              </h3>

              <div className="p-4 rounded-xl bg-[#151c2b] border border-white/5 space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-400">Reporter:</span>
                  <span className="font-bold text-white">{fullName} ({email})</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Target Platform:</span>
                  <span className="font-bold text-white">{platform}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Perpetrator Accounts:</span>
                  <span className="font-bold text-rose-400">{bullyAccounts.length} cataloged</span>
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1.5">
                  Additional Incident Notes / Timeline Details:
                </label>
                <textarea
                  rows={4}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Describe when harassment started, if threats were made, or any other relevant information..."
                  className="input-field text-xs font-sans"
                />
              </div>

              <div className="p-3.5 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-[11px] leading-relaxed">
                By submitting this request, your evidence and perpetrator catalog will be assigned to a certified human consultant for case escalation and advisory.
              </div>

              <div className="flex items-center justify-between pt-4">
                <Button
                  variant="secondary"
                  onClick={() => setCurrentStep(2)}
                  icon={ArrowLeft}
                >
                  Back
                </Button>
                <Button
                  type="submit"
                  variant="danger"
                  isLoading={loading}
                  icon={Send}
                >
                  Submit Escalation Case
                </Button>
              </div>
            </div>
          )}
        </form>
      </Card>
    </div>
  );
}
