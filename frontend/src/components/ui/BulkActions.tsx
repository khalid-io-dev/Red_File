import { Trash2, Download, Tag, CheckSquare } from 'lucide-react';
import Button from '../ui/Button';

interface BulkActionsProps {
  selectedCount: number;
  onDelete: () => void;
  onExport: () => void;
  onUpdateStatus?: (status: string) => void;
  onClear: () => void;
}

export default function BulkActions({ selectedCount, onDelete, onExport, onUpdateStatus, onClear }: BulkActionsProps) {
  if (selectedCount === 0) return null;

  return (
    <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2 z-50">
      <div className="glass-panel px-6 py-4 flex items-center gap-4 shadow-2xl border-2 border-cyan-500/30">
        <div className="flex items-center gap-2">
          <CheckSquare className="w-5 h-5 text-cyan-400" />
          <span className="text-white font-medium">{selectedCount} selected</span>
        </div>

        <div className="h-6 w-px bg-gray-700" />

        <div className="flex gap-2">
          <Button size="sm" variant="danger" onClick={onDelete}>
            <Trash2 className="w-4 h-4 mr-2" />
            Delete
          </Button>

          <Button size="sm" variant="secondary" onClick={onExport}>
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>

          {onUpdateStatus && (
            <select
              onChange={(e) => onUpdateStatus(e.target.value)}
              className="px-3 py-1 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-300 hover:border-cyan-500"
            >
              <option value="">Update Status...</option>
              <option value="confirmed">Confirmed</option>
              <option value="false_positive">False Positive</option>
              <option value="fixed">Fixed</option>
              <option value="ignored">Ignored</option>
            </select>
          )}

          <Button size="sm" variant="ghost" onClick={onClear}>
            Clear
          </Button>
        </div>
      </div>
    </div>
  );
}
