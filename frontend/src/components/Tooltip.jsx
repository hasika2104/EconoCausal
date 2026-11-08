import React, { useState } from 'react';
import { HelpCircle } from 'lucide-react';

export default function Tooltip({ text, children, position = 'top' }) {
  const [visible, setVisible] = useState(false);

  return (
    <span 
      className="relative inline-flex items-center"
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      {children || <HelpCircle className="w-3.5 h-3.5 text-slate-400 hover:text-slate-600 cursor-help" />}
      {visible && (
        <span className={`absolute z-50 px-3 py-2 text-xs text-slate-800 bg-white border border-slate-200/90 rounded-lg shadow-lg whitespace-normal min-w-[200px] max-w-[280px] text-left pointer-events-none font-medium leading-relaxed ${
          position === 'top' ? 'bottom-full mb-1.5 left-1/2 -translate-x-1/2' : 'top-full mt-1.5 left-1/2 -translate-x-1/2'
        }`}>
          {text}
        </span>
      )}
    </span>
  );
}
