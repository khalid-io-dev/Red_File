import { useState } from 'react';

interface Column {
  key: string;
  label: string;
  render?: (item: any) => React.ReactNode;
}

interface DataTableWithSelectProps {
  data: any[];
  columns: Column[];
  onSelectionChange?: (selected: any[]) => void;
  selectable?: boolean;
}

export default function DataTableWithSelect({ data, columns, onSelectionChange, selectable = false }: DataTableWithSelectProps) {
  const [selected, setSelected] = useState<Set<number>>(new Set());

  const toggleAll = () => {
    if (selected.size === data.length) {
      setSelected(new Set());
      onSelectionChange?.([]);
    } else {
      const allIds = new Set(data.map((_, idx) => idx));
      setSelected(allIds);
      onSelectionChange?.(data);
    }
  };

  const toggleRow = (idx: number) => {
    const newSelected = new Set(selected);
    if (newSelected.has(idx)) {
      newSelected.delete(idx);
    } else {
      newSelected.add(idx);
    }
    setSelected(newSelected);
    onSelectionChange?.(data.filter((_, i) => newSelected.has(i)));
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-gray-700">
            {selectable && (
              <th className="px-4 py-3 text-left">
                <input
                  type="checkbox"
                  checked={selected.size === data.length && data.length > 0}
                  onChange={toggleAll}
                  className="w-4 h-4 rounded border-gray-700 bg-gray-800 text-cyan-500 focus:ring-cyan-500"
                />
              </th>
            )}
            {columns.map((col) => (
              <th key={col.key} className="px-4 py-3 text-left text-sm font-semibold text-gray-400 uppercase tracking-wider">
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-700">
          {data.map((item, idx) => (
            <tr key={idx} className="hover:bg-gray-800/50 transition-colors">
              {selectable && (
                <td className="px-4 py-3">
                  <input
                    type="checkbox"
                    checked={selected.has(idx)}
                    onChange={() => toggleRow(idx)}
                    className="w-4 h-4 rounded border-gray-700 bg-gray-800 text-cyan-500 focus:ring-cyan-500"
                  />
                </td>
              )}
              {columns.map((col) => (
                <td key={col.key} className="px-4 py-3 text-sm text-gray-300">
                  {col.render ? col.render(item) : item[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
