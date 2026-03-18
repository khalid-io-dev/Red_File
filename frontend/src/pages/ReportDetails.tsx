import { useParams, useNavigate } from 'react-router-dom';
import { useReport, useDownloadReport } from '../hooks/useReports';
import { ArrowLeft, FileText, Download, Calendar, Loader2 } from 'lucide-react';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

export default function ReportDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: report, isLoading } = useReport(Number(id));
  const downloadReport = useDownloadReport();

  const handleDownload = async () => {
    const { blob } = await downloadReport.mutateAsync(Number(id));
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${report?.title || 'report'}.${report?.format || 'pdf'}`;
    a.click();
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  if (!report) return <p className="text-center text-gray-500 py-8">Report not found</p>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="secondary" onClick={() => navigate('/reports')}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-white">{report.title}</h1>
            <p className="text-gray-400 mt-1">Report Details</p>
          </div>
        </div>
        <Button 
          onClick={handleDownload} 
          disabled={downloadReport.isPending || report.status !== 'completed'}
        >
          {downloadReport.isPending ? (
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
          ) : (
            <Download className="w-4 h-4 mr-2" />
          )}
          Download
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-panel p-4">
          <div className="flex items-center gap-2 text-gray-400 text-sm mb-2">
            <FileText className="w-4 h-4" />
            Format
          </div>
          <Badge variant="info">{report.format.toUpperCase()}</Badge>
        </div>
        <div className="glass-panel p-4">
          <div className="flex items-center gap-2 text-gray-400 text-sm mb-2">
            <Calendar className="w-4 h-4" />
            Status
          </div>
          <Badge variant={report.status === 'completed' ? 'success' : 'warning'}>
            {report.status}
          </Badge>
        </div>
        <div className="glass-panel p-4">
          <div className="flex items-center gap-2 text-gray-400 text-sm mb-2">
            <Calendar className="w-4 h-4" />
            Created
          </div>
          <p className="text-gray-300 text-sm">{new Date(report.created_at).toLocaleString()}</p>
        </div>
      </div>

      <div className="glass-panel p-6">
        <h2 className="text-xl font-bold text-white mb-4">Report Information</h2>
        <div className="space-y-3">
          <div>
            <p className="text-sm text-gray-400">Report ID</p>
            <p className="text-gray-300 font-mono">{report.id}</p>
          </div>
          {report.file_path && (
            <div>
              <p className="text-sm text-gray-400">File Path</p>
              <p className="text-gray-300 font-mono text-sm">{report.file_path}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
