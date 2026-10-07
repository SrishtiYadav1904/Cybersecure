import React from 'react';

export default function Input({
  label,
  error,
  helperText,
  icon: Icon,
  rightElement,
  id,
  className = '',
  required = false,
  ...props
}) {
  const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined);

  return (
    <div className="w-full space-y-1.5 text-left">
      {label && (
        <label htmlFor={inputId} className="block text-xs font-semibold text-slate-300">
          {label}
          {required && <span className="text-rose-400 ml-1">*</span>}
        </label>
      )}

      <div className="relative flex items-center">
        {Icon && (
          <div className="absolute left-3 text-slate-400 pointer-events-none">
            <Icon className="w-4 h-4" />
          </div>
        )}

        <input
          id={inputId}
          required={required}
          aria-invalid={error ? 'true' : 'false'}
          className={`
            w-full bg-[#0f141f] border text-slate-100 placeholder-slate-500
            text-sm rounded-xl py-2.5 transition-all duration-200 outline-none
            focus-visible:ring-2 focus-visible:ring-indigo-500
            ${Icon ? 'pl-9' : 'pl-3.5'}
            ${rightElement ? 'pr-10' : 'pr-3.5'}
            ${error ? 'border-rose-500/80 bg-rose-500/5 focus-visible:ring-rose-500' : 'border-white/10 hover:border-white/20 focus:border-indigo-500'}
            ${className}
          `}
          {...props}
        />

        {rightElement && (
          <div className="absolute right-3 flex items-center">
            {rightElement}
          </div>
        )}
      </div>

      {error ? (
        <p className="text-xs text-rose-400 font-medium">{error}</p>
      ) : helperText ? (
        <p className="text-[11px] text-slate-400 leading-tight">{helperText}</p>
      ) : null}
    </div>
  );
}
