// path: src/api/admin-settings.ts
import { api } from "../lib/apiClient";
import type { Role } from "../types";

// —— Cấu hình chung (tùy BE có hỗ trợ /admin/config hay không) ——
export async function getAppConfig(): Promise<any | null> {
  try { return await api.get("/admin/config"); } catch { return null; }
}
export async function saveAppConfig(payload: any): Promise<boolean> {
  try { await api.patch("/admin/config", payload); return true; } catch { return false; }
}

// —— Bảo mật (tùy BE có hỗ trợ /admin/security) ——
export async function getSecurityConfig(): Promise<any | null> {
  try { return await api.get("/admin/security"); } catch { return null; }
}
export async function saveSecurityConfig(payload: any): Promise<boolean> {
  try { await api.patch("/admin/security", payload); return true; } catch { return false; }
}
export async function rotateJwtKeys(): Promise<boolean> {
  try { await api.post("/admin/rotate-keys", {}); return true; } catch { return false; }
}

// —— RBAC: dùng contract sẵn có của Users (/users/:id) ——
export async function listUsers(params: { page?: number; limit?: number; q?: string; role?: Role } = {}) {
  return api.get("/users", params);
}
export async function updateUserRole(userId: number | string, role: Role) {
  // BE chuẩn ims_api.py hỗ trợ PATCH user (Admin) để đổi role
  return api.patch(`/users/${userId}`, { role });
}
