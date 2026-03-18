import { FileText, Download, Eye, Loader2 } from 'lucide-react';
import { useReports, useDownloadReport } from '../hooks/useReports';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

export default function Reports() {
  const { data: reports = [], isLoading } = useReports();
  const downloadReport = useDownloadReport();

  const handleDownload = async (id: number) => {
    const { blob } = await downloadReport.mutateAsync(id);
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `report-${id}.pdf`;
    a.click();
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Reports</h1>
          <p className="text-gray-400 mt-1">Generated security reports</p>
        </div>
        <Button>
          <FileText className="w-5 h-5 mr-2" />
          Generate Report
        </Button>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {reports.length > 0 ? (
          reports.map((report) => (
            <div key={report.id} className="p-6 rounded-xl bg-gray-900/50 border border-cyan-500/20 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="p-3 rounded-lg bg-cyan-500/20">
                  <FileText className="w-6 h-6 text-cyan-400" />
                </div>
                <div>
                  <h3 className="font-bold text-gray-300">{report.title}</h3>
                  <div className="flex items-center gap-3 mt-1">
                    <Badge variant="info">{report.format.toUpperCase()}</Badge>
                    <span className="text-sm text-gray-500">{new Date(report.created_at).toLocaleDateString()}</span>
                    <Badge variant={report.status === 'completed' ? 'success' : 'secondary'}>{report.status}</Badge>
                  </div>
                </div>
              </div>
              <div className="flex gap-2">
                <Button size="sm" variant="ghost">
                  <Eye className="w-4 h-4" />
                </Button>
                <Button 
                  size="sm" 
                  onClick={() => handleDownload(report.id)}
                  disabled={downloadReport.isPending || report.status !== 'completed'}
                >
                  {downloadReport.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
                </Button>
              </div>
            </div>
          ))
        ) : (
          <p className="text-center text-gray-500 py-12">No reports generated yet</p>
        )}
      </div>
    </div>
  );
}
