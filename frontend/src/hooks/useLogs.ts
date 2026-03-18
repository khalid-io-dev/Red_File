import { useState, useCallback } from 'react';

export type LogLevel = 'info' | 'success' | 'warning' | 'error';

export interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
}

export const useLogs = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isLogOpen, setIsLogOpen] = useState(true);

  const addLog = useCallback((message: string, level: LogLevel = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, { timestamp, level, message }]);
  }, []);

  const addInfo = useCallback((message: string) => {
    addLog(message, 'info');
  }, [addLog]);

  const addSuccess = useCallback((message: string) => {
    addLog(message, 'success');
  }, [addLog]);

  const addWarning = useCallback((message: string) => {
    addLog(message, 'warning');
  }, [addLog]);

  const addError = useCallback((message: string) => {
    addLog(message, 'error');
  }, [addLog]);

  const clearLogs = useCallback(() => {
    setLogs([]);
  }, []);

  const openLogs = useCallback(() => {
    setIsLogOpen(true);
  }, []);

  const closeLogs = useCallback(() => {
    setIsLogOpen(false);
  }, []);

  const toggleLogs = useCallback(() => {
    setIsLogOpen(prev => !prev);
  }, []);

  return {
    logs,
    isLogOpen,
    addLog,
    addInfo,
    addSuccess,
    addWarning,
    addError,
    clearLogs,
    openLogs,
    closeLogs,
    toggleLogs,
  };
};

export default useLogs;
