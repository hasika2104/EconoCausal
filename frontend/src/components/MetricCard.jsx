import React from 'react';

export default function MetricCard({
  title,
  value,
  subtitle,
  badgeText,
  badgeType = 'neutral', // 'success', 'warning', 'info', 'neutral'
  icon: Icon,
  tooltip
}) {
  const badgeClasses = {
    success: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    warning: 'bg-amber-50 text-amber-700 border-amber-200',
    info: 'bg-blue-50 text-blue-700 border-blue-200',
    neutral: 'bg-slate-100 text-slate-700 border-slate-200'
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm hover:shadow transition-shadow">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
          {title}
          {tooltip && (
            <span className="cursor-help text-slate-400 hover:text-slate-600" title={tooltip}>
              ⓘ
            </span>
          )}
        </span>
        {Icon && (
          <div className="w-8 h-8 rounded-lg bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-700">
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>

      <div className="flex items-baseline gap-2 mb-1">
        <span className="text-2xl font-bold text-slate-900 tracking-tight">{value}</span>
      </div>

      <div className="flex items-center justify-between text-xs text-slate-500 mt-2">
        <span>{subtitle}</span>
        {badgeText && (
          <span className={`px-2 py-0.5 rounded-full text-[11px] font-medium border ${badgeClasses[badgeType] || badgeClasses.neutral}`}>
            {badgeText}
          </span>
        )}
      </div>
    </div>
  );
}
