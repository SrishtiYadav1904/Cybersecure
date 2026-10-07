import React, { useState } from 'react';

export default function Tooltip({
  content,
  children,
  position = 'top',
  className = ''
}) {
  const [isVisible, setIsVisible] = useState(false);

  if (!content) return children;

  const positionClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2'
  };

  return (
    <div
      className={`relative inline-flex ${className}`}
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
      onFocus={() => setIsVisible(true)}
      onBlur={() => setIsVisible(false)}
    >
      {children}
      {isVisible && (
        <div
          role="tooltip"
          className={`
            absolute z-50 px-2.5 py-1 text-[11px] font-medium text-slate-200
            bg-[#1c2538] border border-white/15 rounded-lg shadow-xl whitespace-nowrap
            pointer-events-none animate-fade-in
            ${positionClasses[position] || positionClasses.top}
          `}
        >
          {content}
        </div>
      )}
    </div>
  );
}
