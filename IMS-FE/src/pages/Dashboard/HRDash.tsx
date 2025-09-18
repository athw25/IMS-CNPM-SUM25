// path: src/pages/Dashboard/HR/HRDash.tsx
import { useEffect, useState } from "react";
import StatCard from "../../components/StatCard";
import MiniTable from "../../components/MiniTable";
import { getHRCounters, getRecentApplications } from "../../api/hr";

export default function HRDash() {
  const [loading, setLoading] = useState(true);
  const [c, setC] = useState<any>({});
  const [apps, setApps] = useState<any[]>([]);

  async function load() {
    setLoading(true);
    try {
      const counters = await getHRCounters();
      setC(counters);
      const recent = await getRecentApplications(8);
      setApps(recent?.items ?? recent ?? []);
    } finally {
      setLoading(false);
    }
  }
  useEffect(()=>{ load(); }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Bảng điều khiển (HR)</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatCard title="Chiến dịch mở" value={c.openCampaigns} loading={loading} />
        <StatCard title="Tổng đơn" value={c.totalApplications} loading={loading} />
        <StatCard title="Chờ duyệt" value={c.pendingApplications} loading={loading} />
        <StatCard title="Đã duyệt" value={c.approvedApplications} loading={loading} />
      </div>

      <section className="card">
        <div className="flex items-center justify-between mb-2">
          <h2 className="font-medium">Đơn ứng tuyển gần đây</h2>
          <button className="btn btn-sm" onClick={load} disabled={loading}>{loading ? "Đang tải…" : "Làm mới"}</button>
        </div>
        <MiniTable cols={[
          { key: "id", label: "Mã" },
          { key: "user_name", label: "Ứng viên" },
          { key: "campaign_title", label: "Chiến dịch" },
          { key: "status", label: "Trạng thái" },
          { key: "created_at", label: "Thời gian" },
        ]} rows={apps} />
      </section>
    </div>
  );
}
