import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider, useAuth } from './context/AuthContext';
import { lazy, Suspense } from 'react';
import MainLayout from './components/layout/MainLayout';
import LoadingSpinner from './components/LoadingSpinner';
import Toast from './components/ui/Toast';
import CommandPalette from './components/CommandPalette';
import ErrorBoundary from './components/ErrorBoundary';
import { useWebSocket } from './hooks/useWebSocket';
import Login from './pages/Login';
import Register from './pages/Register';

// Command Center
const Dashboard = lazy(() => import('./pages/command-center/Dashboard'));
const ActivityFeed = lazy(() => import('./pages/command-center/ActivityFeed'));
const QuickActions = lazy(() => import('./pages/command-center/QuickActions'));

// Advanced Tools
const AdvancedToolsPage = lazy(() => import('./pages/AdvancedToolsPage'));
const KaliManagement = lazy(() => import('./pages/KaliManagement'));
const ExploitDevelopment = lazy(() => import('./pages/exploitation/ExploitDevelopment'));
const Incidents = lazy(() => import('./pages/Incidents'));
const Alerts = lazy(() => import('./pages/Alerts'));
const Automation = lazy(() => import('./pages/Automation'));
const ContinuousMonitor = lazy(() => import('./pages/ContinuousMonitor'));

// Reconnaissance
const OSINTHub = lazy(() => import('./pages/reconnaissance/OSINTHub'));
const TargetDiscovery = lazy(() => import('./pages/reconnaissance/TargetDiscovery'));
const EmailHarvesting = lazy(() => import('./pages/reconnaissance/EmailHarvesting'));
const SocialMediaIntel = lazy(() => import('./pages/reconnaissance/SocialMediaIntel'));
const DomainIntelligence = lazy(() => import('./pages/reconnaissance/DomainIntelligence'));
const NetworkMapping = lazy(() => import('./pages/reconnaissance/NetworkMapping'));
const PortDiscovery = lazy(() => import('./pages/reconnaissance/PortDiscovery'));
const ServiceDetection = lazy(() => import('./pages/reconnaissance/ServiceDetection'));
const WebRecon = lazy(() => import('./pages/reconnaissance/WebRecon'));
const DirectoryEnumeration = lazy(() => import('./pages/reconnaissance/DirectoryEnumeration'));
const DNSIntelligence = lazy(() => import('./pages/reconnaissance/DNSIntelligence'));
const PassiveRecon = lazy(() => import('./pages/reconnaissance/PassiveRecon'));
const WHOISLookup = lazy(() => import('./pages/reconnaissance/WHOISLookup'));
const CertificateTransparency = lazy(() => import('./pages/reconnaissance/CertificateTransparency'));
const ArchiveAnalysis = lazy(() => import('./pages/reconnaissance/ArchiveAnalysis'));
const InvestigationDetails = lazy(() => import('./pages/reconnaissance/InvestigationDetails'));
const DataBreachSearch = lazy(() => import('./pages/reconnaissance/DataBreachSearch'));
const InvestigationHistory = lazy(() => import('./pages/reconnaissance/InvestigationHistory'));

// Vulnerability Assessment
const ScanManagement = lazy(() => import('./pages/vulnerability-assessment/ScanManagement'));
const ScanDetails = lazy(() => import('./pages/scans/ScanDetails'));
const CreateScan = lazy(() => import('./pages/vulnerability-assessment/CreateScan'));
const ScanTemplates = lazy(() => import('./pages/vulnerability-assessment/ScanTemplates'));
const ScheduledScans = lazy(() => import('./pages/vulnerability-assessment/ScheduledScans'));
const ScanHistory = lazy(() => import('./pages/vulnerability-assessment/ScanHistory'));
const VulnerabilityDatabase = lazy(() => import('./pages/vulnerability-assessment/VulnerabilityDatabase'));
const BySeverity = lazy(() => import('./pages/vulnerability-assessment/BySeverity'));
const ByCategory = lazy(() => import('./pages/vulnerability-assessment/ByCategory'));
const CVEExplorer = lazy(() => import('./pages/vulnerability-assessment/CVEExplorer'));
const WebAppTesting = lazy(() => import('./pages/vulnerability-assessment/WebAppTesting'));
const OwaspTesting = lazy(() => import('./pages/OwaspTesting'));
const SQLInjection = lazy(() => import('./pages/vulnerability-assessment/SQLInjection'));
const XSSDetection = lazy(() => import('./pages/vulnerability-assessment/XSSDetection'));
const NetworkVulnerabilities = lazy(() => import('./pages/vulnerability-assessment/NetworkVulnerabilities'));
const CloudSecurity = lazy(() => import('./pages/vulnerability-assessment/CloudSecurity'));
const ContainerSecurity = lazy(() => import('./pages/vulnerability-assessment/ContainerSecurity'));
const DockerAudit = lazy(() => import('./pages/vulnerability-assessment/DockerAudit'));
const KubernetesSecurity = lazy(() => import('./pages/vulnerability-assessment/KubernetesSecurity'));
const ImageScanning = lazy(() => import('./pages/vulnerability-assessment/ImageScanning'));
const PatchManagement = lazy(() => import('./pages/vulnerability-assessment/PatchManagement'));
const ComplianceScanning = lazy(() => import('./pages/vulnerability-assessment/ComplianceScanning'));

// Exploitation
const ExploitDatabase = lazy(() => import('./pages/exploitation/ExploitDatabase'));
const SearchByCVE = lazy(() => import('./pages/exploitation/SearchByCVE'));
const MetasploitIntegration = lazy(() => import('./pages/exploitation/MetasploitIntegration'));
const PayloadGenerator = lazy(() => import('./pages/exploitation/PayloadGenerator'));
const SessionManager = lazy(() => import('./pages/exploitation/SessionManager'));
const AttackChains = lazy(() => import('./pages/exploitation/AttackChains'));
const CustomExploits = lazy(() => import('./pages/exploitation/CustomExploits'));
const ExploitBuilder = lazy(() => import('./pages/exploitation/ExploitBuilder'));
const ChainBuilder = lazy(() => import('./pages/exploitation/ChainBuilder'));
const ChainExecution = lazy(() => import('./pages/exploitation/ChainExecution'));
const CampaignManagement = lazy(() => import('./pages/exploitation/CampaignManagement'));
const MultiTargetOperations = lazy(() => import('./pages/exploitation/MultiTargetOperations'));
const CredentialAttacks = lazy(() => import('./pages/exploitation/CredentialAttacks'));
const BruteForce = lazy(() => import('./pages/exploitation/BruteForce'));
const HashCracking = lazy(() => import('./pages/exploitation/HashCracking'));
const PrivilegeEscalation = lazy(() => import('./pages/exploitation/PrivilegeEscalation'));
const PostExploitation = lazy(() => import('./pages/exploitation/PostExploitation'));
const LateralMovement = lazy(() => import('./pages/exploitation/LateralMovement'));
const ExploitDetails = lazy(() => import('./pages/exploitation/ExploitDetails'));

// Defense & Monitoring
const HoneypotManagement = lazy(() => import('./pages/defense-monitoring/HoneypotManagement'));
const HoneypotLogs = lazy(() => import('./pages/HoneypotLogs'));
const DionaeaMonitor = lazy(() => import('./pages/defense-monitoring/DionaeaMonitor'));
const CowrieMonitor = lazy(() => import('./pages/defense-monitoring/CowrieMonitor'));
const AttackLogs = lazy(() => import('./pages/defense-monitoring/AttackLogs'));
const IDSIPSManagement = lazy(() => import('./pages/defense-monitoring/IDSIPSManagement'));
const SnortRules = lazy(() => import('./pages/defense-monitoring/SnortRules'));
const SuricataAlerts = lazy(() => import('./pages/defense-monitoring/SuricataAlerts'));
const SIEMIntegration = lazy(() => import('./pages/defense-monitoring/SIEMIntegration'));
const LogAggregation = lazy(() => import('./pages/defense-monitoring/LogAggregation'));
const EventCorrelation = lazy(() => import('./pages/defense-monitoring/EventCorrelation'));
const ThreatIntelligence = lazy(() => import('./pages/defense-monitoring/ThreatIntelligence'));
const IOCDatabase = lazy(() => import('./pages/defense-monitoring/IOCDatabase'));

// AI Operations
const AIAssistantChat = lazy(() => import('./pages/ai-operations/AIAssistantChat'));
const VoiceCommands = lazy(() => import('./pages/ai-operations/VoiceCommands'));
const ConversationHistory = lazy(() => import('./pages/ai-operations/ConversationHistory'));
const AutonomousAgents = lazy(() => import('./pages/ai-operations/AutonomousAgents'));
const AgentDashboard = lazy(() => import('./pages/ai-operations/AgentDashboard'));
const CreateAgent = lazy(() => import('./pages/ai-operations/CreateAgent'));
const AgentPerformance = lazy(() => import('./pages/ai-operations/AgentPerformance'));
const VulnerabilityPrediction = lazy(() => import('./pages/ai-operations/VulnerabilityPrediction'));
const AttackPathAnalysis = lazy(() => import('./pages/ai-operations/AttackPathAnalysis'));
const AnomalyDetection = lazy(() => import('./pages/ai-operations/AnomalyDetection'));
const ThreatHunting = lazy(() => import('./pages/ai-operations/ThreatHunting'));
const ModelTraining = lazy(() => import('./pages/ai-operations/ModelTraining'));
const DatasetManagement = lazy(() => import('./pages/ai-operations/DatasetManagement'));
const QueryBuilder = lazy(() => import('./pages/ai-operations/QueryBuilder'));
const ReportGenerationAI = lazy(() => import('./pages/ai-operations/ReportGenerationAI'));
const AITaskExecution = lazy(() => import('./pages/ai-operations/AITaskExecution'));
const MITREIntegration = lazy(() => import('./pages/ai-operations/MITREIntegration'));
const ReasoningEngine = lazy(() => import('./pages/ai-operations/ReasoningEngine'));

// Intelligence & Analytics
const ReportDashboard = lazy(() => import('./pages/intelligence-analytics/ReportDashboard'));
const SecurityReports = lazy(() => import('./pages/intelligence-analytics/SecurityReports'));
const ExecutiveSummary = lazy(() => import('./pages/intelligence-analytics/ExecutiveSummary'));
const TechnicalReports = lazy(() => import('./pages/intelligence-analytics/TechnicalReports'));
const ComplianceReports = lazy(() => import('./pages/intelligence-analytics/ComplianceReports'));
const MITREAttackFramework = lazy(() => import('./pages/intelligence-analytics/MITREAttackFramework'));
const ThreatActorProfiles = lazy(() => import('./pages/intelligence-analytics/ThreatActorProfiles'));
const ThreatIntelligenceDashboard = lazy(() => import('./pages/intelligence-analytics/ThreatIntelligenceDashboard'));
const IOCAnalysis = lazy(() => import('./pages/intelligence-analytics/IOCAnalysis'));
const CampaignTracking = lazy(() => import('./pages/intelligence-analytics/CampaignTracking'));
const VulnerabilityTrends = lazy(() => import('./pages/intelligence-analytics/VulnerabilityTrends'));
const RiskAssessment = lazy(() => import('./pages/intelligence-analytics/RiskAssessment'));
const AttackSurfaceAnalysis = lazy(() => import('./pages/intelligence-analytics/AttackSurfaceAnalysis'));
const SecurityMetrics = lazy(() => import('./pages/intelligence-analytics/SecurityMetrics'));
const KPIDashboard = lazy(() => import('./pages/intelligence-analytics/KPIDashboard'));
const TrendAnalysis = lazy(() => import('./pages/intelligence-analytics/TrendAnalysis'));
const PredictiveAnalytics = lazy(() => import('./pages/intelligence-analytics/PredictiveAnalytics'));
const IntelligenceReports = lazy(() => import('./pages/intelligence-analytics/IntelligenceReports'));

// Advanced Tools
const ReverseEngineeringPage = lazy(() => import('./pages/ReverseEngineeringPage'));
const AdvancedWebToolsPage = lazy(() => import('./pages/AdvancedWebToolsPage'));
const NetworkToolsPage = lazy(() => import('./pages/NetworkToolsPage'));
const FindingsAnalysis = lazy(() => import('./pages/FindingsAnalysis'));

// Social Engineering
const SECampaignManager = lazy(() => import('./pages/social-engineering/SECampaignManager'));
const EmailCraftingStudio = lazy(() => import('./pages/social-engineering/EmailCraftingStudio'));

// Attack Chains
const AttackChainExecutor = lazy(() => import('./pages/attack-chains/AttackChainExecutor'));

// Campaigns
const CampaignReasoningDashboard = lazy(() => import('./pages/campaigns/CampaignReasoningDashboard'));

// Asset Management
const AssetInventory = lazy(() => import('./pages/asset-management/AssetInventory'));
const AssetDiscovery = lazy(() => import('./pages/asset-management/AssetDiscovery'));
const AssetDetails = lazy(() => import('./pages/asset-management/AssetDetails'));
const AssetGroups = lazy(() => import('./pages/asset-management/AssetGroups'));
const AssetMonitoring = lazy(() => import('./pages/asset-management/AssetMonitoring'));
const SoftwareInventory = lazy(() => import('./pages/asset-management/SoftwareInventory'));
const HardwareInventory = lazy(() => import('./pages/asset-management/HardwareInventory'));
const CloudAssets = lazy(() => import('./pages/asset-management/CloudAssets'));
const NetworkTopology = lazy(() => import('./pages/asset-management/NetworkTopology'));
const AssetLifecycle = lazy(() => import('./pages/asset-management/AssetLifecycle'));

// Phase 1 - Cloud Security
const CloudSecurityDashboard = lazy(() => import('./pages/vulnerability-assessment/CloudSecurityDashboard'));
const AWSScanner = lazy(() => import('./pages/vulnerability-assessment/AWSScanner'));
const AzureScanner = lazy(() => import('./pages/vulnerability-assessment/AzureScanner'));
const GCPScanner = lazy(() => import('./pages/vulnerability-assessment/GCPScanner'));
const ContainerScanner = lazy(() => import('./pages/vulnerability-assessment/ContainerScanner'));
const KubernetesScanner = lazy(() => import('./pages/vulnerability-assessment/KubernetesScanner'));

// Phase 1 - SIEM
const SIEMDashboard = lazy(() => import('./pages/defense-monitoring/SIEMDashboard'));
const SIEMConnector = lazy(() => import('./pages/defense-monitoring/SIEMConnector'));
const SIEMQueryBuilder = lazy(() => import('./pages/defense-monitoring/SIEMQueryBuilder'));
const SIEMDashboards = lazy(() => import('./pages/defense-monitoring/SIEMDashboards'));
const SIEMAlertRules = lazy(() => import('./pages/defense-monitoring/SIEMAlertRules'));

// Phase 1 - Threat Intel
const ThreatIntelDashboard = lazy(() => import('./pages/intelligence-analytics/ThreatIntelDashboard'));
const IOCAnalyzer = lazy(() => import('./pages/intelligence-analytics/IOCAnalyzer'));
const ThreatActorBrowser = lazy(() => import('./pages/intelligence-analytics/ThreatActorBrowser'));
const CVEBrowser = lazy(() => import('./pages/intelligence-analytics/CVEBrowser'));

// Phase 2 - Defense & Monitoring
const AlertsDashboard = lazy(() => import('./pages/defense-monitoring/AlertsDashboard'));
const IncidentResponse = lazy(() => import('./pages/defense-monitoring/IncidentResponse'));
const SOARPlaybooks = lazy(() => import('./pages/defense-monitoring/SOARPlaybooks'));
const HoneypotManager = lazy(() => import('./pages/defense-monitoring/HoneypotManager'));

// Phase 3 - Offensive Security
const ExploitLibrary = lazy(() => import('./pages/exploitation/ExploitLibrary'));
const EvasionStudio = lazy(() => import('./pages/exploitation/EvasionStudio'));
const AttackChainBuilder = lazy(() => import('./pages/exploitation/AttackChainBuilder'));
const MITREMatrix = lazy(() => import('./pages/exploitation/MITREMatrix'));

// Phase 4 - Intelligence & Analytics
const ReportGenerator = lazy(() => import('./pages/intelligence-analytics/ReportGenerator'));
const ExecutiveDashboard = lazy(() => import('./pages/intelligence-analytics/ExecutiveDashboard'));
const VulnerabilityDashboard = lazy(() => import('./pages/vulnerability-assessment/VulnerabilityDashboard'));

// Phase 6 - Configuration
const SystemSettings = lazy(() => import('./pages/configuration/SystemSettings'));
const UserManagement = lazy(() => import('./pages/configuration/UserManagement'));
const SecurityPolicies = lazy(() => import('./pages/configuration/SecurityPolicies'));
const IntegrationSettings = lazy(() => import('./pages/configuration/IntegrationSettings'));
const NotificationSettings = lazy(() => import('./pages/configuration/NotificationSettings'));
const APIConfiguration = lazy(() => import('./pages/configuration/APIConfiguration'));
const BackupRestore = lazy(() => import('./pages/configuration/BackupRestore'));
const AuditLogs = lazy(() => import('./pages/configuration/AuditLogs'));

const queryClient = new QueryClient();

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
    const { user, loading } = useAuth();
    useWebSocket(!!user); // Enable WebSocket when user is logged in

    if (loading) return <LoadingSpinner />;
    if (!user) return <Navigate to="/login" replace />;
    return <>{children}</>;
};

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <BrowserRouter>
                <AuthProvider>
                    <ErrorBoundary>
                        <Toast />
                        <CommandPalette />
                        <Routes>
                            <Route path="/login" element={<Login />} />
                            <Route path="/register" element={<Register />} />

                            <Route path="/" element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
                                <Route index element={<Suspense fallback={<LoadingSpinner />}><Dashboard /></Suspense>} />

                                {/* Command Center */}
                                <Route path="command-center/executive" element={<Suspense fallback={<LoadingSpinner />}><Dashboard /></Suspense>} />
                                <Route path="command-center/operations" element={<Suspense fallback={<LoadingSpinner />}><ActivityFeed /></Suspense>} />
                                <Route path="command-center/analytics" element={<Suspense fallback={<LoadingSpinner />}><QuickActions /></Suspense>} />

                                {/* Reconnaissance */}
                                <Route path="recon/osint" element={<Suspense fallback={<LoadingSpinner />}><OSINTHub /></Suspense>} />
                                <Route path="recon/target-discovery" element={<Suspense fallback={<LoadingSpinner />}><TargetDiscovery /></Suspense>} />
                                <Route path="recon/email" element={<Suspense fallback={<LoadingSpinner />}><EmailHarvesting /></Suspense>} />
                                <Route path="recon/social-media" element={<Suspense fallback={<LoadingSpinner />}><SocialMediaIntel /></Suspense>} />
                                <Route path="recon/domain" element={<Suspense fallback={<LoadingSpinner />}><DomainIntelligence /></Suspense>} />
                                <Route path="recon/network" element={<Suspense fallback={<LoadingSpinner />}><NetworkMapping /></Suspense>} />
                                <Route path="recon/ports" element={<Suspense fallback={<LoadingSpinner />}><PortDiscovery /></Suspense>} />
                                <Route path="recon/services" element={<Suspense fallback={<LoadingSpinner />}><ServiceDetection /></Suspense>} />
                                <Route path="recon/web" element={<Suspense fallback={<LoadingSpinner />}><WebRecon /></Suspense>} />
                                <Route path="recon/directory" element={<Suspense fallback={<LoadingSpinner />}><DirectoryEnumeration /></Suspense>} />
                                <Route path="recon/dns" element={<Suspense fallback={<LoadingSpinner />}><DNSIntelligence /></Suspense>} />
                                <Route path="recon/passive" element={<Suspense fallback={<LoadingSpinner />}><PassiveRecon /></Suspense>} />
                                <Route path="recon/whois" element={<Suspense fallback={<LoadingSpinner />}><WHOISLookup /></Suspense>} />
                                <Route path="recon/certificates" element={<Suspense fallback={<LoadingSpinner />}><CertificateTransparency /></Suspense>} />
                                <Route path="recon/archive" element={<Suspense fallback={<LoadingSpinner />}><ArchiveAnalysis /></Suspense>} />
                                <Route path="recon/breaches" element={<Suspense fallback={<LoadingSpinner />}><DataBreachSearch /></Suspense>} />
                                <Route path="recon/history" element={<Suspense fallback={<LoadingSpinner />}><InvestigationHistory /></Suspense>} />
                                <Route path="recon/investigations/:id" element={<Suspense fallback={<LoadingSpinner />}><InvestigationDetails /></Suspense>} />

                                {/* Vulnerability Assessment */}
                                <Route path="scans" element={<Suspense fallback={<LoadingSpinner />}><ScanManagement /></Suspense>} />
                                <Route path="scans/:id" element={<Suspense fallback={<LoadingSpinner />}><ScanDetails /></Suspense>} />
                                <Route path="scans/create" element={<Suspense fallback={<LoadingSpinner />}><CreateScan /></Suspense>} />
                                <Route path="scans/templates" element={<Suspense fallback={<LoadingSpinner />}><ScanTemplates /></Suspense>} />
                                <Route path="scans/scheduled" element={<Suspense fallback={<LoadingSpinner />}><ScheduledScans /></Suspense>} />
                                <Route path="scans/history" element={<Suspense fallback={<LoadingSpinner />}><ScanHistory /></Suspense>} />
                                <Route path="vulnerabilities" element={<Suspense fallback={<LoadingSpinner />}><VulnerabilityDatabase /></Suspense>} />
                                <Route path="vulnerabilities/severity" element={<Suspense fallback={<LoadingSpinner />}><BySeverity /></Suspense>} />
                                <Route path="vulnerabilities/category" element={<Suspense fallback={<LoadingSpinner />}><ByCategory /></Suspense>} />
                                <Route path="vulnerabilities/cve" element={<Suspense fallback={<LoadingSpinner />}><CVEExplorer /></Suspense>} />
                                <Route path="vulnerabilities/web-app" element={<Suspense fallback={<LoadingSpinner />}><WebAppTesting /></Suspense>} />
                                <Route path="owasp" element={<Suspense fallback={<LoadingSpinner />}><OwaspTesting /></Suspense>} />
                                <Route path="vulnerabilities/sql-injection" element={<Suspense fallback={<LoadingSpinner />}><SQLInjection /></Suspense>} />
                                <Route path="vulnerabilities/xss" element={<Suspense fallback={<LoadingSpinner />}><XSSDetection /></Suspense>} />
                                <Route path="vulnerabilities/network" element={<Suspense fallback={<LoadingSpinner />}><NetworkVulnerabilities /></Suspense>} />
                                <Route path="cloud-security" element={<Suspense fallback={<LoadingSpinner />}><CloudSecurity /></Suspense>} />
                                <Route path="cloud-security/containers" element={<Suspense fallback={<LoadingSpinner />}><ContainerSecurity /></Suspense>} />
                                <Route path="cloud-security/docker" element={<Suspense fallback={<LoadingSpinner />}><DockerAudit /></Suspense>} />
                                <Route path="cloud-security/kubernetes" element={<Suspense fallback={<LoadingSpinner />}><KubernetesSecurity /></Suspense>} />
                                <Route path="cloud-security/images" element={<Suspense fallback={<LoadingSpinner />}><ImageScanning /></Suspense>} />
                                <Route path="patch-management" element={<Suspense fallback={<LoadingSpinner />}><PatchManagement /></Suspense>} />
                                <Route path="compliance" element={<Suspense fallback={<LoadingSpinner />}><ComplianceScanning /></Suspense>} />

                                {/* Exploitation */}
                                <Route path="exploits" element={<Suspense fallback={<LoadingSpinner />}><ExploitDatabase /></Suspense>} />
                                <Route path="exploits/cve" element={<Suspense fallback={<LoadingSpinner />}><SearchByCVE /></Suspense>} />
                                <Route path="exploits/metasploit" element={<Suspense fallback={<LoadingSpinner />}><MetasploitIntegration /></Suspense>} />
                                <Route path="payloads" element={<Suspense fallback={<LoadingSpinner />}><PayloadGenerator /></Suspense>} />
                                <Route path="sessions" element={<Suspense fallback={<LoadingSpinner />}><SessionManager /></Suspense>} />
                                <Route path="chains" element={<Suspense fallback={<LoadingSpinner />}><AttackChains /></Suspense>} />
                                <Route path="exploits/custom" element={<Suspense fallback={<LoadingSpinner />}><CustomExploits /></Suspense>} />
                                <Route path="exploits/builder" element={<Suspense fallback={<LoadingSpinner />}><ExploitBuilder /></Suspense>} />
                                <Route path="chains/builder" element={<Suspense fallback={<LoadingSpinner />}><ChainBuilder /></Suspense>} />
                                <Route path="chains/execute" element={<Suspense fallback={<LoadingSpinner />}><ChainExecution /></Suspense>} />
                                <Route path="campaigns" element={<Suspense fallback={<LoadingSpinner />}><CampaignManagement /></Suspense>} />
                                <Route path="campaigns/multi-target" element={<Suspense fallback={<LoadingSpinner />}><MultiTargetOperations /></Suspense>} />
                                <Route path="credentials" element={<Suspense fallback={<LoadingSpinner />}><CredentialAttacks /></Suspense>} />
                                <Route path="credentials/brute-force" element={<Suspense fallback={<LoadingSpinner />}><BruteForce /></Suspense>} />
                                <Route path="credentials/hash-cracking" element={<Suspense fallback={<LoadingSpinner />}><HashCracking /></Suspense>} />
                                <Route path="privilege-escalation" element={<Suspense fallback={<LoadingSpinner />}><PrivilegeEscalation /></Suspense>} />
                                <Route path="post-exploitation" element={<Suspense fallback={<LoadingSpinner />}><PostExploitation /></Suspense>} />
                                <Route path="lateral-movement" element={<Suspense fallback={<LoadingSpinner />}><LateralMovement /></Suspense>} />
                                <Route path="exploits/:id" element={<Suspense fallback={<LoadingSpinner />}><ExploitDetails /></Suspense>} />

                                {/* Defense & Monitoring */}
                                <Route path="honeypots" element={<Suspense fallback={<LoadingSpinner />}><HoneypotManagement /></Suspense>} />
                                <Route path="honeypots/dionaea" element={<Suspense fallback={<LoadingSpinner />}><DionaeaMonitor /></Suspense>} />
                                <Route path="honeypots/cowrie" element={<Suspense fallback={<LoadingSpinner />}><CowrieMonitor /></Suspense>} />
                                <Route path="honeypots/logs" element={<Suspense fallback={<LoadingSpinner />}><HoneypotLogs /></Suspense>} />
                                <Route path="ids-ips" element={<Suspense fallback={<LoadingSpinner />}><IDSIPSManagement /></Suspense>} />
                                <Route path="ids-ips/snort" element={<Suspense fallback={<LoadingSpinner />}><SnortRules /></Suspense>} />
                                <Route path="ids-ips/suricata" element={<Suspense fallback={<LoadingSpinner />}><SuricataAlerts /></Suspense>} />
                                <Route path="siem" element={<Suspense fallback={<LoadingSpinner />}><SIEMIntegration /></Suspense>} />
                                <Route path="siem/logs" element={<Suspense fallback={<LoadingSpinner />}><LogAggregation /></Suspense>} />
                                <Route path="siem/correlation" element={<Suspense fallback={<LoadingSpinner />}><EventCorrelation /></Suspense>} />
                                <Route path="threat-intel" element={<Suspense fallback={<LoadingSpinner />}><ThreatIntelligence /></Suspense>} />
                                <Route path="threat-intel/ioc" element={<Suspense fallback={<LoadingSpinner />}><IOCDatabase /></Suspense>} />

                                {/* AI Operations */}
                                <Route path="ai/assistant" element={<Suspense fallback={<LoadingSpinner />}><AIAssistantChat /></Suspense>} />
                                <Route path="ai/voice" element={<Suspense fallback={<LoadingSpinner />}><VoiceCommands /></Suspense>} />
                                <Route path="ai/history" element={<Suspense fallback={<LoadingSpinner />}><ConversationHistory /></Suspense>} />
                                <Route path="ai/agents" element={<Suspense fallback={<LoadingSpinner />}><AutonomousAgents /></Suspense>} />
                                <Route path="ai/agents/dashboard" element={<Suspense fallback={<LoadingSpinner />}><AgentDashboard /></Suspense>} />
                                <Route path="ai/agents/create" element={<Suspense fallback={<LoadingSpinner />}><CreateAgent /></Suspense>} />
                                <Route path="ai/agents/performance" element={<Suspense fallback={<LoadingSpinner />}><AgentPerformance /></Suspense>} />
                                <Route path="ai/analysis" element={<Suspense fallback={<LoadingSpinner />}><VulnerabilityPrediction /></Suspense>} />
                                <Route path="ai/attack-paths" element={<Suspense fallback={<LoadingSpinner />}><AttackPathAnalysis /></Suspense>} />
                                <Route path="ai/anomaly" element={<Suspense fallback={<LoadingSpinner />}><AnomalyDetection /></Suspense>} />
                                <Route path="ai/hunting" element={<Suspense fallback={<LoadingSpinner />}><ThreatHunting /></Suspense>} />
                                <Route path="ai/training" element={<Suspense fallback={<LoadingSpinner />}><ModelTraining /></Suspense>} />
                                <Route path="ai/datasets" element={<Suspense fallback={<LoadingSpinner />}><DatasetManagement /></Suspense>} />
                                <Route path="ai/query" element={<Suspense fallback={<LoadingSpinner />}><QueryBuilder /></Suspense>} />
                                <Route path="ai/reports" element={<Suspense fallback={<LoadingSpinner />}><ReportGenerationAI /></Suspense>} />
                                <Route path="ai/task-execution" element={<Suspense fallback={<LoadingSpinner />}><AITaskExecution /></Suspense>} />
                                <Route path="ai/mitre-integration" element={<Suspense fallback={<LoadingSpinner />}><MITREIntegration /></Suspense>} />
                                <Route path="ai/reasoning-engine" element={<Suspense fallback={<LoadingSpinner />}><ReasoningEngine /></Suspense>} />

                                {/* Intelligence & Analytics */}
                                <Route path="reports" element={<Suspense fallback={<LoadingSpinner />}><ReportDashboard /></Suspense>} />
                                <Route path="reports/security" element={<Suspense fallback={<LoadingSpinner />}><SecurityReports /></Suspense>} />
                                <Route path="reports/executive" element={<Suspense fallback={<LoadingSpinner />}><ExecutiveSummary /></Suspense>} />
                                <Route path="reports/technical" element={<Suspense fallback={<LoadingSpinner />}><TechnicalReports /></Suspense>} />
                                <Route path="reports/compliance" element={<Suspense fallback={<LoadingSpinner />}><ComplianceReports /></Suspense>} />
                                <Route path="mitre" element={<Suspense fallback={<LoadingSpinner />}><MITREAttackFramework /></Suspense>} />
                                <Route path="threat-actors" element={<Suspense fallback={<LoadingSpinner />}><ThreatActorProfiles /></Suspense>} />
                                <Route path="intelligence/dashboard" element={<Suspense fallback={<LoadingSpinner />}><ThreatIntelligenceDashboard /></Suspense>} />
                                <Route path="intelligence/ioc-analysis" element={<Suspense fallback={<LoadingSpinner />}><IOCAnalysis /></Suspense>} />
                                <Route path="intelligence/campaigns" element={<Suspense fallback={<LoadingSpinner />}><CampaignTracking /></Suspense>} />
                                <Route path="intelligence/trends" element={<Suspense fallback={<LoadingSpinner />}><VulnerabilityTrends /></Suspense>} />
                                <Route path="risk-assessment" element={<Suspense fallback={<LoadingSpinner />}><RiskAssessment /></Suspense>} />
                                <Route path="attack-surface" element={<Suspense fallback={<LoadingSpinner />}><AttackSurfaceAnalysis /></Suspense>} />
                                <Route path="metrics" element={<Suspense fallback={<LoadingSpinner />}><SecurityMetrics /></Suspense>} />
                                <Route path="kpi" element={<Suspense fallback={<LoadingSpinner />}><KPIDashboard /></Suspense>} />
                                <Route path="analytics/trends" element={<Suspense fallback={<LoadingSpinner />}><TrendAnalysis /></Suspense>} />
                                <Route path="analytics/predictive" element={<Suspense fallback={<LoadingSpinner />}><PredictiveAnalytics /></Suspense>} />
                                <Route path="intelligence/reports" element={<Suspense fallback={<LoadingSpinner />}><IntelligenceReports /></Suspense>} />

                                {/* Asset Management */}
                                <Route path="assets" element={<Suspense fallback={<LoadingSpinner />}><AssetInventory /></Suspense>} />
                                <Route path="assets/discovery" element={<Suspense fallback={<LoadingSpinner />}><AssetDiscovery /></Suspense>} />
                                <Route path="assets/details" element={<Suspense fallback={<LoadingSpinner />}><AssetDetails /></Suspense>} />
                                <Route path="assets/groups" element={<Suspense fallback={<LoadingSpinner />}><AssetGroups /></Suspense>} />
                                <Route path="assets/monitoring" element={<Suspense fallback={<LoadingSpinner />}><AssetMonitoring /></Suspense>} />
                                <Route path="assets/software" element={<Suspense fallback={<LoadingSpinner />}><SoftwareInventory /></Suspense>} />
                                <Route path="assets/hardware" element={<Suspense fallback={<LoadingSpinner />}><HardwareInventory /></Suspense>} />
                                <Route path="assets/cloud" element={<Suspense fallback={<LoadingSpinner />}><CloudAssets /></Suspense>} />
                                <Route path="assets/network-topology" element={<Suspense fallback={<LoadingSpinner />}><NetworkTopology /></Suspense>} />
                                <Route path="assets/lifecycle" element={<Suspense fallback={<LoadingSpinner />}><AssetLifecycle /></Suspense>} />

                                {/* Configuration */}
                                <Route path="settings" element={<Suspense fallback={<LoadingSpinner />}><SystemSettings /></Suspense>} />
                                <Route path="settings/users" element={<Suspense fallback={<LoadingSpinner />}><UserManagement /></Suspense>} />
                                <Route path="settings/security" element={<Suspense fallback={<LoadingSpinner />}><SecurityPolicies /></Suspense>} />
                                <Route path="settings/integrations" element={<Suspense fallback={<LoadingSpinner />}><IntegrationSettings /></Suspense>} />
                                <Route path="settings/notifications" element={<Suspense fallback={<LoadingSpinner />}><NotificationSettings /></Suspense>} />
                                <Route path="settings/api" element={<Suspense fallback={<LoadingSpinner />}><APIConfiguration /></Suspense>} />
                                <Route path="settings/backup" element={<Suspense fallback={<LoadingSpinner />}><BackupRestore /></Suspense>} />
                                <Route path="settings/audit" element={<Suspense fallback={<LoadingSpinner />}><AuditLogs /></Suspense>} />

                                {/* Advanced Tools */}
                                <Route path="advanced-tools/reverse-engineering" element={<Suspense fallback={<LoadingSpinner />}><ReverseEngineeringPage /></Suspense>} />
                                <Route path="advanced-tools/web-tools" element={<Suspense fallback={<LoadingSpinner />}><AdvancedWebToolsPage /></Suspense>} />
                                <Route path="advanced-tools/network-tools" element={<Suspense fallback={<LoadingSpinner />}><NetworkToolsPage /></Suspense>} />

                                {/* Findings */}
                                <Route path="findings" element={<Suspense fallback={<LoadingSpinner />}><ReportDashboard /></Suspense>} />
                                <Route path="findings/:id" element={<Suspense fallback={<LoadingSpinner />}><ReportDashboard /></Suspense>} />
                                <Route path="findings/analysis" element={<Suspense fallback={<LoadingSpinner />}><FindingsAnalysis /></Suspense>} />
                                <Route path="tools" element={<Suspense fallback={<LoadingSpinner />}><AssetInventory /></Suspense>} />
                                <Route path="users" element={<Suspense fallback={<LoadingSpinner />}><UserManagement /></Suspense>} />
                                <Route path="social-engineering" element={<Suspense fallback={<LoadingSpinner />}><SECampaignManager /></Suspense>} />
                                <Route path="social-engineering/campaigns" element={<Suspense fallback={<LoadingSpinner />}><SECampaignManager /></Suspense>} />
                                <Route path="social-engineering/email-craft" element={<Suspense fallback={<LoadingSpinner />}><EmailCraftingStudio /></Suspense>} />
                                
                                {/* Attack Chains */}
                                <Route path="attack-chains/executor" element={<Suspense fallback={<LoadingSpinner />}><AttackChainExecutor /></Suspense>} />
                                
                                {/* Campaigns */}
                                <Route path="campaigns/reasoning" element={<Suspense fallback={<LoadingSpinner />}><CampaignReasoningDashboard /></Suspense>} />
                                <Route path="obfuscation" element={<Suspense fallback={<LoadingSpinner />}><Dashboard /></Suspense>} />

                                {/* New Routes */}
                                <Route path="advanced-tools" element={<Suspense fallback={<LoadingSpinner />}><AdvancedToolsPage /></Suspense>} />
                                <Route path="kali" element={<Suspense fallback={<LoadingSpinner />}><KaliManagement /></Suspense>} />
                                <Route path="exploits/development" element={<Suspense fallback={<LoadingSpinner />}><ExploitDevelopment /></Suspense>} />
                                <Route path="incidents" element={<Suspense fallback={<LoadingSpinner />}><Incidents /></Suspense>} />
                                <Route path="alerts" element={<Suspense fallback={<LoadingSpinner />}><Alerts /></Suspense>} />
                                <Route path="automation" element={<Suspense fallback={<LoadingSpinner />}><Automation /></Suspense>} />
                                <Route path="monitoring" element={<Suspense fallback={<LoadingSpinner />}><ContinuousMonitor /></Suspense>} />

                                {/* Phase 1 - Cloud Security Routes */}
                                <Route path="cloud-security" element={<Suspense fallback={<LoadingSpinner />}><CloudSecurityDashboard /></Suspense>} />
                                <Route path="cloud/aws" element={<Suspense fallback={<LoadingSpinner />}><AWSScanner /></Suspense>} />
                                <Route path="cloud/azure" element={<Suspense fallback={<LoadingSpinner />}><AzureScanner /></Suspense>} />
                                <Route path="cloud/gcp" element={<Suspense fallback={<LoadingSpinner />}><GCPScanner /></Suspense>} />
                                <Route path="cloud/containers" element={<Suspense fallback={<LoadingSpinner />}><ContainerScanner /></Suspense>} />
                                <Route path="cloud/kubernetes" element={<Suspense fallback={<LoadingSpinner />}><KubernetesScanner /></Suspense>} />

                                {/* Phase 1 - SIEM Routes */}
                                <Route path="siem" element={<Suspense fallback={<LoadingSpinner />}><SIEMDashboard /></Suspense>} />
                                <Route path="siem/connector" element={<Suspense fallback={<LoadingSpinner />}><SIEMConnector /></Suspense>} />
                                <Route path="siem/query" element={<Suspense fallback={<LoadingSpinner />}><SIEMQueryBuilder /></Suspense>} />
                                <Route path="siem/dashboards" element={<Suspense fallback={<LoadingSpinner />}><SIEMDashboards /></Suspense>} />
                                <Route path="siem/alerts" element={<Suspense fallback={<LoadingSpinner />}><SIEMAlertRules /></Suspense>} />

                                {/* Phase 1 - Threat Intel Routes */}
                                <Route path="threat-intel" element={<Suspense fallback={<LoadingSpinner />}><ThreatIntelDashboard /></Suspense>} />
                                <Route path="threat-intel/ioc" element={<Suspense fallback={<LoadingSpinner />}><IOCAnalyzer /></Suspense>} />
                                <Route path="threat-intel/actors" element={<Suspense fallback={<LoadingSpinner />}><ThreatActorBrowser /></Suspense>} />
                                <Route path="threat-intel/cve" element={<Suspense fallback={<LoadingSpinner />}><CVEBrowser /></Suspense>} />

                                {/* Phase 2 - Defense & Monitoring Routes */}
                                <Route path="defense/alerts" element={<Suspense fallback={<LoadingSpinner />}><AlertsDashboard /></Suspense>} />
                                <Route path="defense/incidents" element={<Suspense fallback={<LoadingSpinner />}><IncidentResponse /></Suspense>} />
                                <Route path="defense/playbooks" element={<Suspense fallback={<LoadingSpinner />}><SOARPlaybooks /></Suspense>} />
                                <Route path="defense/honeypot" element={<Suspense fallback={<LoadingSpinner />}><HoneypotManager /></Suspense>} />

                                {/* Phase 3 - Offensive Security Routes */}
                                <Route path="offensive/exploits" element={<Suspense fallback={<LoadingSpinner />}><ExploitLibrary /></Suspense>} />
                                <Route path="offensive/evasion" element={<Suspense fallback={<LoadingSpinner />}><EvasionStudio /></Suspense>} />
                                <Route path="offensive/payloads" element={<Suspense fallback={<LoadingSpinner />}><PayloadGenerator /></Suspense>} />
                                <Route path="offensive/chains" element={<Suspense fallback={<LoadingSpinner />}><AttackChainBuilder /></Suspense>} />
                                <Route path="offensive/mitre" element={<Suspense fallback={<LoadingSpinner />}><MITREMatrix /></Suspense>} />

                                {/* Phase 4 - Intelligence & Analytics Routes */}
                                <Route path="intel/reports" element={<Suspense fallback={<LoadingSpinner />}><ReportGenerator /></Suspense>} />
                                <Route path="intel/executive" element={<Suspense fallback={<LoadingSpinner />}><ExecutiveDashboard /></Suspense>} />
                                <Route path="intel/compliance" element={<Suspense fallback={<LoadingSpinner />}><ComplianceReports /></Suspense>} />
                                <Route path="vulnerabilities" element={<Suspense fallback={<LoadingSpinner />}><VulnerabilityDashboard /></Suspense>} />
                                <Route path="cve-explorer" element={<Suspense fallback={<LoadingSpinner />}><CVEExplorer /></Suspense>} />

                                {/* Phase 5 - Asset Management Routes */}
                                <Route path="assets/inventory" element={<Suspense fallback={<LoadingSpinner />}><AssetInventory /></Suspense>} />
                                <Route path="assets/discovery" element={<Suspense fallback={<LoadingSpinner />}><AssetDiscovery /></Suspense>} />
                                <Route path="assets/topology" element={<Suspense fallback={<LoadingSpinner />}><NetworkTopology /></Suspense>} />

                                {/* Phase 6 - Configuration Routes */}
                                <Route path="config/settings" element={<Suspense fallback={<LoadingSpinner />}><SystemSettings /></Suspense>} />
                                <Route path="config/policies" element={<Suspense fallback={<LoadingSpinner />}><SecurityPolicies /></Suspense>} />
                                <Route path="config/users" element={<Suspense fallback={<LoadingSpinner />}><UserManagement /></Suspense>} />
                            </Route>
                        </Routes>
                    </ErrorBoundary>
                </AuthProvider>
            </BrowserRouter>
        </QueryClientProvider>
    );
}

export default App;
