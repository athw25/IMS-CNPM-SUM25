import { api } from '../lib/apiClient'
export const admin = {
  health: () => api.get('/admin/health')
}
export default admin

// path: src/api/admin.ts
export type Health = {
  api: "ok" | "fail";
  db: "ok" | "fail";
  latency_ms: number;
  server_time: string; // ISO
  version?: string;
};

export async function getHealth(): Promise<Health> {
  const res = await api.get("/admin/health");
  return res as Health;
}

export async function getOverview() {
  // Giữ nguyên contract phía BE (ví dụ /reports/overview đã tồn tại)
  return api.get("/reports/overview");
}
