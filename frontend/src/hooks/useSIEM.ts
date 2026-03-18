import { useState, useCallback } from 'react';
import { apiClient } from '../lib/api-client';

interface SIEMConfig {
  id: string;
  platform: string;
  url: string;
  apiKey: string;
  enabled: boolean;
}

interface SIEMEvent {
  id: string;
  timestamp: string;
  source: string;
  message: string;
  severity: string;
}

interface AlertRule {
  id: string;
  name: string;
  condition: string;
  severity: string;
  enabled: boolean;
}

export function useSIEM() {
  const [config, setConfig] = useState<SIEMConfig[]>([]);
  const [events, setEvents] = useState<SIEMEvent[]>([]);
  const [alertRules, setAlertRules] = useState<AlertRule[]>([]);
  const [loading, setLoading] = useState(false);

  const getSIEMStatus = useCallback(async () => {
    try {
      const response = await apiClient.get('/siem/status');
      return response.data;
    } catch (error) {
      console.error('Failed to get SIEM status:', error);
      return { connected: false, platforms: [] };
    }
  }, []);

  const connectPlatform = useCallback(async (platform: string, credentials: any) => {
    try {
      const response = await apiClient.post(`/siem/connect/${platform}`, credentials);
      return response.data;
    } catch (error) {
      console.error(`Failed to connect to ${platform}:`, error);
      throw error;
    }
  }, []);

  const disconnectPlatform = useCallback(async (platform: string) => {
    try {
      const response = await apiClient.delete(`/siem/connect/${platform}`);
      return response.data;
    } catch (error) {
      console.error(`Failed to disconnect from ${platform}:`, error);
      throw error;
    }
  }, []);

  const getEvents = useCallback(async (params?: { limit?: number; source?: string; severity?: string }) => {
    try {
      const response = await apiClient.get('/siem/events', { params });
      setEvents(response.data.events || []);
      return response.data.events || [];
    } catch (error) {
      console.error('Failed to get events:', error);
      // Return mock data for demo
      return [
        { id: '1', timestamp: new Date().toISOString(), source: 'Splunk', message: 'Failed login attempt detected', severity: 'medium' },
        { id: '2', timestamp: new Date().toISOString(), source: 'Elasticsearch', message: 'Suspicious network activity', severity: 'high' },
      ];
    }
  }, []);

  const searchEvents = useCallback(async (query: string, filters?: any) => {
    try {
      const response = await apiClient.post('/siem/query', { query, filters });
      return response.data.results;
    } catch (error) {
      console.error('Failed to search events:', error);
      throw error;
    }
  }, []);

  const getAlertRules = useCallback(async () => {
    try {
      const response = await apiClient.get('/siem/alert-rules');
      setAlertRules(response.data.rules || []);
      return response.data.rules || [];
    } catch (error) {
      console.error('Failed to get alert rules:', error);
      return [];
    }
  }, []);

  const createAlertRule = useCallback(async (rule: Partial<AlertRule>) => {
    try {
      const response = await apiClient.post('/siem/alert-rules', rule);
      setAlertRules(prev => [...prev, response.data]);
      return response.data;
    } catch (error) {
      console.error('Failed to create alert rule:', error);
      throw error;
    }
  }, []);

  const updateAlertRule = useCallback(async (id: string, updates: Partial<AlertRule>) => {
    try {
      const response = await apiClient.put(`/siem/alert-rules/${id}`, updates);
      setAlertRules(prev => prev.map(rule => rule.id === id ? { ...rule, ...updates } : rule));
      return response.data;
    } catch (error) {
      console.error('Failed to update alert rule:', error);
      throw error;
    }
  }, []);

  const deleteAlertRule = useCallback(async (id: string) => {
    try {
      await apiClient.delete(`/siem/alert-rules/${id}`);
      setAlertRules(prev => prev.filter(rule => rule.id !== id));
    } catch (error) {
      console.error('Failed to delete alert rule:', error);
      throw error;
    }
  }, []);

  const getDashboards = useCallback(async () => {
    try {
      const response = await apiClient.get('/siem/dashboards');
      return response.data.dashboards || [];
    } catch (error) {
      console.error('Failed to get dashboards:', error);
      return [];
    }
  }, []);

  return {
    config,
    events,
    alertRules,
    loading,
    getSIEMStatus,
    connectPlatform,
    disconnectPlatform,
    getEvents,
    searchEvents,
    getAlertRules,
    createAlertRule,
    updateAlertRule,
    deleteAlertRule,
    getDashboards,
  };
}
