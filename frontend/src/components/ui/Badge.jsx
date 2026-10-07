import React from 'react';
import { ShieldCheck, AlertCircle, AlertTriangle, ShieldAlert, Info, HelpCircle } from 'lucide-react';

export default function Badge({
  children,
  variant = 'default',
  size = 'md',
  icon: CustomIcon,
  className = '',
  ...props
}) {
  const sizeClasses = {
    sm: 'text-[10px] px-2 py-0.5 rounded gap-1 font-semibold uppercase tracking-wider',
    md: 'text-xs px-2.5 py-1 rounded-lg gap-1.5 font-medium'
  };

  const variantStyles = {
    default: {
      class: 'bg-slate-800 text-slate-300 border border-white/10',
      DefaultIcon: null
    },
    safe: {
      class: 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30',
      DefaultIcon: ShieldCheck
    },
    concerning: {
      class: 'bg-amber-500/15 text-amber-400 border border-amber-500/30',
      DefaultIcon: AlertCircle
    },
    harmful: {
      class: 'bg-orange-500/15 text-orange-400 border border-orange-500/30',
      DefaultIcon: AlertTriangle
    },
    severe: {
      class: 'bg-rose-500/15 text-rose-400 border border-rose-500/30',
      DefaultIcon: ShieldAlert
    },
    info: {
      class: 'bg-indigo-500/15 text-indigo-300 border border-indigo-500/30',
      DefaultIcon: Info
    },
    outline: {
      class: 'bg-transparent text-slate-300 border border-white/20',
      DefaultIcon: null
    }
  };

  const selected = variantStyles[variant] || variantStyles.default;
  const IconComponent = CustomIcon || selected.DefaultIcon;

  return (
    <span
      className={`
        inline-flex items-center select-none font-mono
        ${sizeClasses[size] || sizeClasses.md}
        ${selected.class}
        ${className}
      `}
      {...props}
    >
      {IconComponent && <IconComponent className="w-3.5 h-3.5 shrink-0" />}
      <span>{children}</span>
    </span>
  );
}
