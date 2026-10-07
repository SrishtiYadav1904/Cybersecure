import React from 'react';
import { ChevronDown } from 'lucide-react';

export default function Select({
  label,
  error,
  helperText,
  options = [],
  id,
  className = '',
  required = false,
  children,
  ...props
}) {
  const selectId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined);

  return (
    <div className="w-full space-y-1.5 text-left">
      {label && (
        <label htmlFor={selectId} className="block text-xs font-semibold text-slate-300">
          {label}
          {required && <span className="text-rose-400 ml-1">*</span>}
        </label>
      )}

      <div className="relative flex items-center">
        <select
          id={selectId}
          required={required}
          aria-invalid={error ? 'true' : 'false'}
          className={`
            w-full appearance-none bg-[#0f141f] border text-slate-100
            text-sm rounded-xl py-2.5 pl-3.5 pr-10 transition-all duration-200 outline-none
            focus-visible:ring-2 focus-visible:ring-indigo-500 cursor-pointer
            ${error ? 'border-rose-500/80 bg-rose-500/5 focus-visible:ring-rose-500' : 'border-white/10 hover:border-white/20 focus:border-indigo-500'}
            ${className}
          `}
          {...props}
        >
          {children || options.map(opt => (
            <option key={opt.value} value={opt.value} className="bg-slate-900 text-slate-200">
              {opt.label || opt.value}
            </option>
          ))}
        </select>

        <div className="absolute right-3 text-slate-400 pointer-events-none">
          <ChevronDown className="w-4 h-4" />
        </div>
      </div>

      {error ? (
        <p className="text-xs text-rose-400 font-medium">{error}</p>
      ) : helperText ? (
        <p className="text-[11px] text-slate-400 leading-tight">{helperText}</p>
      ) : null}
    </div>
  );
}
