import React from 'react';
import Button from './Button';

export default function EmptyState({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
  actionIcon,
  className = ''
}) {
  return (
    <div
      className={`
        p-12 text-center bg-[#0f141f]/60 border border-dashed border-white/10 rounded-2xl
        flex flex-col items-center justify-center space-y-3
        ${className}
      `}
    >
      {Icon && (
        <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center mb-1">
          <Icon className="w-6 h-6" />
        </div>
      )}

      {title && (
        <h4 className="text-sm font-bold text-white tracking-tight">
          {title}
        </h4>
      )}

      {description && (
        <p className="text-xs text-slate-400 max-w-md leading-relaxed">
          {description}
        </p>
      )}

      {actionLabel && onAction && (
        <div className="pt-2">
          <Button
            size="sm"
            onClick={onAction}
            icon={actionIcon}
          >
            {actionLabel}
          </Button>
        </div>
      )}
    </div>
  );
}
