import { useState } from 'react';
import { Calendar } from 'lucide-react';

interface DateRangePickerProps {
  startDate: string;
  endDate: string;
  onChange: (start: string, end: string) => void;
}

export default function DateRangePicker({ startDate, endDate, onChange }: DateRangePickerProps) {
  const presets = [
    { label: 'Today', days: 0 },
    { label: 'Last 7 days', days: 7 },
    { label: 'Last 30 days', days: 30 },
    { label: 'Last 90 days', days: 90 },
  ];

  const applyPreset = (days: number) => {
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - days);
    onChange(start.toISOString().split('T')[0], end.toISOString().split('T')[0]);
  };

  return (
    <div className="space-y-3">
      <div className="flex gap-2">
        {presets.map(preset => (
          <button
            key={preset.label}
            onClick={() => applyPreset(preset.days)}
            className="px-3 py-1 text-sm bg-gray-800 border border-gray-700 rounded-lg text-gray-300 hover:border-cyan-500 hover:text-cyan-400"
          >
            {preset.label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm text-gray-400 mb-1">Start Date</label>
          <div className="relative">
            <input
              type="date"
              value={startDate}
              onChange={(e) => onChange(e.target.value, endDate)}
              className="w-full px-4 py-2 pl-10 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:border-cyan-500 focus:outline-none"
            />
            <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500" />
          </div>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">End Date</label>
          <div className="relative">
            <input
              type="date"
              value={endDate}
              onChange={(e) => onChange(startDate, e.target.value)}
              className="w-full px-4 py-2 pl-10 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:border-cyan-500 focus:outline-none"
            />
            <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500" />
          </div>
        </div>
      </div>
    </div>
  );
}
