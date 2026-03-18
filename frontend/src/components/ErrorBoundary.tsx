import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error boundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="min-h-screen flex items-center justify-center bg-bg-primary p-4">
          <div className="max-w-md w-full bg-bg-secondary border border-border-primary rounded-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-lg bg-danger-500/10 flex items-center justify-center">
                <AlertTriangle className="w-6 h-6 text-danger-400" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">Something went wrong</h2>
                <p className="text-sm text-text-secondary">An error occurred while rendering this page</p>
              </div>
            </div>

            {this.state.error && (
              <div className="p-3 bg-danger-500/10 border border-danger-500/30 rounded-lg mb-4">
                <p className="text-sm text-danger-400 font-mono">{this.state.error.message}</p>
              </div>
            )}

            <button
              onClick={() => window.location.reload()}
              className="w-full px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg transition-colors"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
