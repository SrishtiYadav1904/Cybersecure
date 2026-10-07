import React from 'react';

export function Card({ children, className = '', interactive = false, ...props }) {
  return (
    <div
      className={`
        bg-[#0f141f] border border-white/10 rounded-2xl shadow-lg
        transition-all duration-200
        ${interactive ? 'cursor-pointer hover:border-indigo-500/40 hover:-translate-y-0.5 hover:shadow-indigo-500/10' : ''}
        ${className}
      `}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ children, className = '', ...props }) {
  return (
    <div className={`p-5 pb-3 border-b border-white/5 ${className}`} {...props}>
      {children}
    </div>
  );
}

export function CardTitle({ children, className = '', ...props }) {
  return (
    <h3 className={`text-base font-bold text-white tracking-tight flex items-center gap-2 ${className}`} {...props}>
      {children}
    </h3>
  );
}

export function CardDescription({ children, className = '', ...props }) {
  return (
    <p className={`text-xs text-slate-400 mt-1 leading-relaxed ${className}`} {...props}>
      {children}
    </p>
  );
}

export function CardContent({ children, className = '', ...props }) {
  return (
    <div className={`p-5 ${className}`} {...props}>
      {children}
    </div>
  );
}

export function CardFooter({ children, className = '', ...props }) {
  return (
    <div className={`p-5 pt-3 border-t border-white/5 flex items-center justify-between ${className}`} {...props}>
      {children}
    </div>
  );
}

export default Card;
