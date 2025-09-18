// path: src/api/intern.ts
import { api } from "../lib/apiClient";

export async function getInternBoard() {
  // { assignments, schedule, resources }  — theo contract có sẵn từ BE
  return api.get("/reports/intern-board");
}
