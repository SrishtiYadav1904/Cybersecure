import React, { useState } from 'react';
import {
  ShieldCheck,
  Lock,
  Mail,
  User,
  ArrowRight,
  Sparkles,
  KeyRound,
  AlertCircle
} from 'lucide-react';
import { api, setAuthToken, setStoredUser } from '../api';
import Button from './ui/Button';
import { Card } from './ui/Card';
import Input from './ui/Input';
import Select from './ui/Select';

export default function AuthModal({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [fullName, setFullName] = useState('');
  const [selectedRole, setSelectedRole] = useState('USER');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      let resp;
      if (isLogin) {
        resp = await api.login({
          email: email.trim(),
          password,
          role: selectedRole
        });
      } else {
        resp = await api.register({
          email: email.trim(),
          username: username.trim(),
          password,
          full_name: fullName.trim() || username.trim(),
          role: selectedRole
        });
      }

      setAuthToken(resp.access_token);
      setStoredUser(resp.user);
      onLoginSuccess(resp.user);
    } catch (err) {
      setError(err.message || 'Authentication failed. Please verify credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoFill = (role) => {
    setIsLogin(true);
    setError(null);
    if (role === 'ADMIN') {
      setEmail('admin@cyberguard.ai');
      setPassword('AdminSecure2026!');
      setSelectedRole('ADMIN');
    } else {
      setEmail('user@cyberguard.ai');
      setPassword('UserSecure2026!');
      setSelectedRole('USER');
    }
  };

  return (
    <Card className="w-full max-w-md p-8 border-white/10 shadow-2xl space-y-6 relative overflow-hidden bg-[#0f141f]">
      {/* Decorative Brand Accent */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-indigo-600"></div>

      {/* Brand Header */}
      <div className="text-center space-y-2">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-indigo-600 to-purple-600 text-white flex items-center justify-center mx-auto shadow-lg shadow-indigo-500/25">
          <ShieldCheck className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-white tracking-tight">
          {isLogin ? 'Sign In to CyberGuard' : 'Create CyberGuard Account'}
        </h2>
        <p className="text-xs text-slate-400">
          Multilingual Explainable AI Cyberbullying Forensics & Safety Platform
        </p>
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
          <span>{error}</span>
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        {!isLogin && (
          <>
            <Input
              label="Full Name"
              required
              placeholder="e.g. John Doe"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              icon={User}
            />
            <Input
              label="Username"
              required
              placeholder="e.g. jdoe"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              icon={User}
            />
          </>
        )}

        <Input
          label="Email Address"
          type="email"
          required
          placeholder="user@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          icon={Mail}
        />

        <Input
          label="Password"
          type="password"
          required
          placeholder="••••••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          icon={Lock}
        />

        <Button
          type="submit"
          variant="primary"
          className="w-full"
          isLoading={loading}
          icon={ArrowRight}
        >
          {isLogin ? 'Access Safety Platform' : 'Complete Registration'}
        </Button>
      </form>

      {/* Quick Demo Credentials */}
      <div className="pt-3 border-t border-white/10 space-y-2">
        <p className="text-[11px] font-semibold text-slate-400 text-center">
          One-Click Demo Fill:
        </p>
        <div className="grid grid-cols-2 gap-2">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => handleDemoFill('USER')}
            className="text-xs"
          >
            User Demo
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={() => handleDemoFill('ADMIN')}
            className="text-xs"
          >
            Admin Demo
          </Button>
        </div>
      </div>

      {/* Toggle Sign In / Register */}
      <div className="text-center pt-2">
        <button
          type="button"
          onClick={() => {
            setIsLogin(!isLogin);
            setError(null);
          }}
          className="text-xs text-indigo-400 hover:text-indigo-300 font-medium"
        >
          {isLogin ? "Don't have an account? Sign up" : 'Already registered? Sign in'}
        </button>
      </div>
    </Card>
  );
}
