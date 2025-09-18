// path: src/api/hr.ts
import { api } from "../lib/apiClient";

export async function getHRCounters() {
  // BE cần trả về { openCampaigns, totalApplications, pendingApplications, approvedApplications }
  return api.get("/reports/hr-counters");
}
export async function getRecentApplications(limit = 5) {
  return api.get("/applications", { limit, sort: "created_at:desc" });
}
