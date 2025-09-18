import { api } from "../lib/apiClient";

export const kpi = {
  list: (q: { intern_id?: number | string; period?: string; key?: string; page?: number; limit?: number }) =>
    api.get("/kpi", q),
  create: (payload: any) => api.post("/kpi", payload),
};

export default kpi;
