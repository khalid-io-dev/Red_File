import { useEffect, useRef, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

interface WebSocketMessage {
  type: 'scan_update' | 'campaign_update' | 'finding_created' | 'credential_found';
  data: any;
}

export const useWebSocket = (enabled: boolean = true) => {
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const queryClient = useQueryClient();
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    if (!enabled) return;

    const connect = () => {
      const token = localStorage.getItem('token');
      if (!token) return;

      const ws = new WebSocket(`${WS_URL}?token=${token}`);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          handleMessage(message);
        } catch (error) {
          console.error('WebSocket message error:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
        
        // Reconnect after 5 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          connect();
        }, 5000);
      };
    };

    const handleMessage = (message: WebSocketMessage) => {
      switch (message.type) {
        case 'scan_update':
          queryClient.invalidateQueries({ queryKey: ['scans'] });
          if (message.data.id) {
            queryClient.invalidateQueries({ queryKey: ['scans', message.data.id] });
          }
          break;

        case 'campaign_update':
          queryClient.invalidateQueries({ queryKey: ['campaigns'] });
          if (message.data.id) {
            queryClient.invalidateQueries({ queryKey: ['campaigns', message.data.id] });
          }
          break;

        case 'finding_created':
          queryClient.invalidateQueries({ queryKey: ['findings'] });
          queryClient.invalidateQueries({ queryKey: ['dashboard'] });
          break;

        case 'credential_found':
          queryClient.invalidateQueries({ queryKey: ['credentials'] });
          queryClient.invalidateQueries({ queryKey: ['dashboard'] });
          break;
      }
    };

    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [enabled, queryClient]);

  return { isConnected };
};
