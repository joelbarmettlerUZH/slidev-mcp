export interface Overview {
  days: number;
  totals: {
    events: number;
    toolCalls: number;
    resourceReads: number;
    errors: number;
    errorRate: number;
    p50Ms: number | null;
    p95Ms: number | null;
    firstEvent: string | null;
    lastEvent: string | null;
  };
  daily: { day: string; toolCalls: number; resourceReads: number }[];
  tools: { name: string; count: number; p50Ms: number | null; p95Ms: number | null; errors: number }[];
  themes: { theme: string; count: number }[];
  clients: { client: string; count: number }[];
  resources: { name: string; count: number }[];
  errorCodes: { error: string; count: number }[];
  recentErrors: { timestamp: string; name: string; theme: string | null; error: string }[];
}
