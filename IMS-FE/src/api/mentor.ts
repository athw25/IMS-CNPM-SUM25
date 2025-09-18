// path: src/api/mentor.ts
import { api } from "../lib/apiClient";

export async function getMentorCounters() {
  // { ownedProjects, assignedTasks, evaluations, chatThreads }
  return api.get("/reports/mentor-counters");
}
export async function getRecentAssignments(limit = 5) {
  return api.get("/assignments", { limit, sort: "updated_at:desc" });
}
