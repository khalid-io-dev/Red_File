import { useState } from 'react';
import { Filter, X, Save, Download } from 'lucide-react';
import MultiSelect from './MultiSelect';
import DateRangePicker from './DateRangePicker';
import Button from '../ui/Button';

interface FilterState {
  severity: string[];
  tools: string[];
  status: string[];
  startDate: string;
  endDate: string;
  target: string;
}

interface AdvancedFilterProps {
  onApply: (filters: FilterState) => void;
  onClear: () => void;
  onExport?: () => void;
}

const SEVERITY_OPTIONS = ['Critical', 'High', 'Medium', 'Low', 'Info'];
const STATUS_OPTIONS = ['New', 'Confirmed', 'False Positive', 'Fixed', 'Ignored'];
const TOOL_OPTIONS = ['nmap', 'sqlmap', 'nikto', 'hydra', 'nuclei', 'gobuster', 'wpscan', 'masscan', 'metasploit', 'burpsuite'];

export default function AdvancedFilter({ onApply, onClear, onExport }: AdvancedFilterProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [filters, setFilters] = useState<FilterState>({
    severity: [],
    tools: [],
    status: [],
    startDate: '',
    endDate: '',
    target: '',
  });

  const [savedFilters, setSavedFilters] = useState<{ name: string; filters: FilterState }[]>([]);

  const handleApply = () => {
    onApply(filters);
    setIsOpen(false);
  };

  const handleClear = () => {
    const emptyFilters = {
      severity: [],
      tools: [],
      status: [],
      startDate: '',
      endDate: '',
      target: '',
    };
    setFilters(emptyFilters);
    onClear();
  };

  const saveFilter = () => {
    const name = prompt('Enter filter preset name:');
    if (name) {
      setSavedFilters([...savedFilters, { name, filters }]);
    }
  };

  const loadFilter = (preset: { name: string; filters: FilterState }) => {
    setFilters(preset.filters);
  };

  const activeFilterCount = 
    filters.severity.length + 
    filters.tools.length + 
    filters.status.length + 
    (filters.startDate ? 1 : 0) + 
    (filters.target ? 1 : 0);

  return (
    <div className="relative">
      <Button
        variant="secondary"
        onClick={() => setIsOpen(!isOpen)}
        className="relative"
      >
        <Filter className="w-4 h-4 mr-2" />
        Filters
        {activeFilterCount > 0 && (
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-cyan-500 text-white text-xs rounded-full flex items-center justify-center">
            {activeFilterCount}
          </span>
        )}
      </Button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-96 bg-gray-900 border border-gray-700 rounded-lg shadow-xl z-50 p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white">Advanced Filters</h3>
            <button onClick={() => setIsOpen(false)} className="text-gray-400 hover:text-white">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Severity</label>
              <MultiSelect
                options={SEVERITY_OPTIONS}
                selected={filters.severity}
                onChange={(severity) => setFilters({ ...filters, severity })}
                placeholder="Select severity levels"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Tools</label>
              <MultiSelect
                options={TOOL_OPTIONS}
                selected={filters.tools}
                onChange={(tools) => setFilters({ ...filters, tools })}
                placeholder="Select tools"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Status</label>
              <MultiSelect
                options={STATUS_OPTIONS}
                selected={filters.status}
                onChange={(status) => setFilters({ ...filters, status })}
                placeholder="Select status"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Date Range</label>
              <DateRangePicker
                startDate={filters.startDate}
                endDate={filters.endDate}
                onChange={(startDate, endDate) => setFilters({ ...filters, startDate, endDate })}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Target</label>
              <input
                type="text"
                value={filters.target}
                onChange={(e) => setFilters({ ...filters, target: e.target.value })}
                placeholder="Search by target..."
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:border-cyan-500 focus:outline-none"
              />
            </div>

            {savedFilters.length > 0 && (
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Saved Filters</label>
                <div className="space-y-1">
                  {savedFilters.map((preset, idx) => (
                    <button
                      key={idx}
                      onClick={() => loadFilter(preset)}
                      className="w-full px-3 py-2 text-left bg-gray-800 hover:bg-gray-700 rounded text-sm text-gray-300"
                    >
                      {preset.name}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="flex gap-2 mt-4 pt-4 border-t border-gray-700">
            <Button onClick={handleApply} className="flex-1">Apply</Button>
            <Button variant="secondary" onClick={handleClear}>Clear</Button>
            <Button variant="ghost" onClick={saveFilter}>
              <Save className="w-4 h-4" />
            </Button>
            {onExport && (
              <Button variant="ghost" onClick={onExport}>
                <Download className="w-4 h-4" />
              </Button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
