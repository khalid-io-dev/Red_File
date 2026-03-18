export interface Tool {
  name: string;
  description: string;
  category: string;
  parameters: ToolParameter[];
  mitre_techniques?: string[];
}

export interface ToolParameter {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'array';
  required: boolean;
  default?: any;
  description?: string;
}

export interface ToolExecution {
  tool: string;
  target: string;
  parameters: Record<string, any>;
}
