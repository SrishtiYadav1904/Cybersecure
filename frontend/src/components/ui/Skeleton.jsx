import React from 'react';

export default function Skeleton({
  variant = 'text',
  count = 1,
  className = ''
}) {
  const variantStyles = {
    text: 'h-4 w-full rounded',
    rect: 'h-24 w-full rounded-xl',
    circle: 'w-10 h-10 rounded-full',
    card: 'h-40 w-full rounded-2xl',
    'table-row': 'h-10 w-full rounded-lg'
  };

  const items = Array.from({ length: count }, (_, i) => i);

  return (
    <div className="space-y-2.5 w-full">
      {items.map((key) => (
        <div
          key={key}
          className={`
            animate-pulse bg-slate-800/60 border border-white/5
            ${variantStyles[variant] || variantStyles.text}
            ${className}
          `}
        />
      ))}
    </div>
  );
}
