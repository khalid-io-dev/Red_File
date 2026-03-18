import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGenerateReport } from '../hooks/useReports';
import { FileText, Loader2 } from 'lucide-react';
import Button from '../components/ui/Button';

export default function GenerateReport() {
  const navigate = useNavigate();
  const generateReport = useGenerateReport();
  const [formData, setFormData] = useState({
    title: '',
    format: 'pdf',
    scan_ids: [],
    campaign_ids: [],
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await generateReport.mutateAsync(formData);
    navigate('/reports');
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white flex items-center gap-3">
        <FileText className="w-6 h-6 text-cyan-400" />
        Generate Report
      </h1>
      <form onSubmit={handleSubmit} className="glass-panel p-6 rounded-xl space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Report Title</label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            placeholder="Q1 Security Assessment"
            className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Format</label>
          <select
            value={formData.format}
            onChange={(e) => setFormData({ ...formData, format: e.target.value })}
            className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
          >
            <option value="pdf">PDF</option>
            <option value="markdown">Markdown</option>
            <option value="json">JSON</option>
          </select>
        </div>
        <div className="flex gap-3">
          <Button type="submit" disabled={generateReport.isPending}>
            {generateReport.isPending ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
            Generate Report
          </Button>
          <Button variant="ghost" onClick={() => navigate('/reports')}>Cancel</Button>
        </div>
      </form>
    </div>
  );
}
