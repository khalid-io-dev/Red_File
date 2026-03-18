import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface ComplianceFramework {
  id: number;
  name: string;
  version: string;
  description: string;
  controls_count: number;
}

interface ComplianceControl {
  id: number;
  framework_id: number;
  control_id: string;
  title: string;
  description: string;
  status: 'compliant' | 'non_compliant' | 'partial' | 'not_tested';
}

interface ComplianceReport {
  framework: string;
  total_controls: number;
  compliant: number;
  non_compliant: number;
  partial: number;
  not_tested: number;
  compliance_percentage: number;
}

export const useComplianceFrameworks = () => {
  return useQuery({
    queryKey: ['compliance', 'frameworks'],
    queryFn: () => apiClient.get<ComplianceFramework[]>('/compliance/frameworks'),
  });
};

export const useComplianceControls = (frameworkId: number) => {
  return useQuery({
    queryKey: ['compliance', 'controls', frameworkId],
    queryFn: () => apiClient.get<ComplianceControl[]>(`/compliance/frameworks/${frameworkId}/controls`),
    enabled: !!frameworkId,
  });
};

export const useComplianceReport = (frameworkId: number) => {
  return useQuery({
    queryKey: ['compliance', 'report', frameworkId],
    queryFn: () => apiClient.get<ComplianceReport>(`/compliance/frameworks/${frameworkId}/report`),
    enabled: !!frameworkId,
  });
};

export const useUpdateControlStatus = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ controlId, status }: { controlId: number; status: string }) =>
      apiClient.put(`/compliance/controls/${controlId}`, { status }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['compliance'] });
    },
  });
};

// Combined hook for ComplianceScanning component
export const useCompliance = () => {
  const { data: frameworks, isLoading: isLoadingFrameworks, refetch: refetchFrameworks } = useComplianceFrameworks();
  const { data: report, isLoading: isLoadingReport } = useComplianceReport(1);
  const updateStatus = useUpdateControlStatus();

  const complianceData = {
    frameworks: frameworks || [],
    report: report,
    isLoaded: !isLoadingFrameworks && !isLoadingReport,
  };

  return {
    data: complianceData,
    isLoading: isLoadingFrameworks || isLoadingReport,
    frameworks,
    report,
    updateStatus,
    refetchFrameworks,
  };
};
