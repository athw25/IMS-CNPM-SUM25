// path: src/pages/Dashboard/Coordinator/CoordDash.tsx
import { useEffect, useState } from "react";
import StatCard from "../../components/StatCard";
import MiniTable from "../../components/MiniTable";
import { getCoordCounters, getUpcomingSchedule } from "../../api/coord";

export default function CoordDash() {
  const [loading, setLoading] = useState(true);
  const [c, setC] = useState<any>({});
  const [sched, setSched] = useState<any[]>([]);

  async function load() {
    setLoading(true);
    try {
      setC(await getCoordCounters());
      const upcoming = await getUpcomingSchedule(8);
      setSched(upcoming?.items ?? upcoming ?? []);
    } finally {
      setLoading(false);
    }
  }
  useEffect(()=>{ load(); }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Bảng điều khiển (Điều phối)</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatCard title="Chương trình" value={c.programs} loading={loading} />
        <StatCard title="Dự án" value={c.projects} loading={loading} />
        <StatCard title="KPI" value={c.kpi} loading={loading} />
        <StatCard title="Lịch" value={c.schedule} loading={loading} />
      </div>

      <section className="card">
        <div className="flex items-center justify-between mb-2">
          <h2 className="font-medium">Lịch sắp tới</h2>
          <button className="btn btn-sm" onClick={load} disabled={loading}>{loading ? "Đang tải…" : "Làm mới"}</button>
        </div>
        <MiniTable cols={[
          { key: "title", label: "Tiêu đề" },
          { key: "start_time", label: "Bắt đầu" },
          { key: "end_time", label: "Kết thúc" },
          { key: "intern_name", label: "Thực tập sinh" },
          { key: "location", label: "Địa điểm" },
        ]} rows={sched} />
      </section>
    </div>
  );
}
