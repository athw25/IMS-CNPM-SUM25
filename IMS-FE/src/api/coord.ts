// path: src/api/coord.ts
import { api } from "../lib/apiClient";

export async function getCoordCounters() {
  // { programs, projects, kpi, schedule }
  return api.get("/reports/coord-counters");
}
export async function getUpcomingSchedule(limit = 5) {
  return api.get("/schedule", { from: new Date().toISOString(), limit, sort: "start_time:asc" });
}
