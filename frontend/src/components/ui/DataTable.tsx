import { ReactNode } from 'react';

interface Column<T> {
  key: string;
  label: string;
  render?: (item: T) => ReactNode;
}

interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (item: T) => void;
}

export default function DataTable<T extends Record<string, any>>({ data, columns, onRowClick }: DataTableProps<T>) {
  return (
    <div className="overflow-x-auto rounded-xl border border-cyan-500/20 bg-gray-900/50 backdrop-blur-xl">
      <table className="w-full">
        <thead className="border-b border-cyan-500/20">
          <tr>
            {columns.map((col) => (
              <th key={col.key} className="px-6 py-4 text-left text-sm font-semibold text-cyan-400">
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-800">
          {data.map((item, idx) => (
            <tr
              key={idx}
              onClick={() => onRowClick?.(item)}
              className={`transition-colors ${onRowClick ? 'cursor-pointer hover:bg-gray-800/50' : ''}`}
            >
              {columns.map((col) => (
                <td key={col.key} className="px-6 py-4 text-sm text-gray-300">
                  {col.render ? col.render(item) : item[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {data.length === 0 && (
        <div className="py-12 text-center text-gray-500">
          No data available
        </div>
      )}
    </div>
  );
}
