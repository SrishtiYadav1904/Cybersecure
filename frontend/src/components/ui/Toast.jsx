import React, { useEffect } from 'react';
import { CheckCircle2, AlertCircle, AlertTriangle, Info, X } from 'lucide-react';

export default function Toast({
  type = 'info',
  message,
  onClose,
  autoDismiss = true,
  dismissAfter = 5000,
  className = ''
}) {
  // Auto-dismiss after `dismissAfter` ms
  useEffect(() => {
    if (!message || !autoDismiss || !onClose) return;
    const timer = setTimeout(() => onClose(), dismissAfter);
    return () => clearTimeout(timer);
  }, [message, autoDismiss, onClose, dismissAfter]);

  if (!message) return null;

  const styles = {
    success: {
      bg: 'bg-emerald-950/90 border-emerald-500/40 text-emerald-200',
      icon: CheckCircle2,
      iconColor: 'text-emerald-400',
      bar: 'bg-emerald-500'
    },
    error: {
      bg: 'bg-rose-950/90 border-rose-500/40 text-rose-200',
      icon: AlertCircle,
      iconColor: 'text-rose-400',
      bar: 'bg-rose-500'
    },
    warning: {
      bg: 'bg-amber-950/90 border-amber-500/40 text-amber-200',
      icon: AlertTriangle,
      iconColor: 'text-amber-400',
      bar: 'bg-amber-500'
    },
    info: {
      bg: 'bg-indigo-950/90 border-indigo-500/40 text-indigo-200',
      icon: Info,
      iconColor: 'text-indigo-400',
      bar: 'bg-indigo-500'
    }
  };

  const current = styles[type] || styles.info;
  const IconComponent = current.icon;

  return (
    <div
      role="alert"
      className={`
        relative flex items-center justify-between gap-3 px-4 py-3 rounded-xl border shadow-xl
        backdrop-blur-md animate-fade-in text-xs font-medium overflow-hidden
        ${current.bg}
        ${className}
      `}
    >
      {/* Auto-dismiss progress bar */}
      {autoDismiss && (
        <div
          className={`absolute bottom-0 left-0 h-0.5 ${current.bar} opacity-60`}
          style={{
            animation: `shrink ${dismissAfter}ms linear forwards`,
            width: '100%'
          }}
        />
      )}

      <div className="flex items-center gap-2.5">
        <IconComponent className={`w-4 h-4 shrink-0 ${current.iconColor}`} />
        <span className="leading-snug">{message}</span>
      </div>

      {onClose && (
        <button
          type="button"
          onClick={onClose}
          aria-label="Dismiss toast"
          className="p-1 rounded text-slate-400 hover:text-white hover:bg-white/10 transition-colors shrink-0"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      )}

      <style>{`
        @keyframes shrink {
          from { width: 100%; }
          to   { width: 0%; }
        }
      `}</style>
    </div>
  );
}
