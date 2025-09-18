// path: src/pages/Dashboard/Mentor/MentorDash.tsx
import { useEffect, useState } from "react";
import StatCard from "../../components/StatCard";
import MiniTable from "../../components/MiniTable";
import { getMentorCounters, getRecentAssignments } from "../../api/mentor";

export default function MentorDash() {
  const [loading, setLoading] = useState(true);
  const [c, setC] = useState<any>({});
  const [tasks, setTasks] = useState<any[]>([]);

  async function load() {
    setLoading(true);
    try {
      setC(await getMentorCounters());
      const recent = await getRecentAssignments(8);
      setTasks(recent?.items ?? recent ?? []);
    } finally {
      setLoading(false);
    }
  }
  useEffect(()=>{ load(); }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Bảng điều khiển (Mentor)</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatCard title="Dự án phụ trách" value={c.ownedProjects} loading={loading} />
        <StatCard title="Nhiệm vụ gán" value={c.assignedTasks} loading={loading} />
        <StatCard title="Đánh giá" value={c.evaluations} loading={loading} />
        <StatCard title="Chuỗi chat" value={c.chatThreads} loading={loading} />
      </div>

      <section className="card">
        <div className="flex items-center justify-between mb-2">
          <h2 className="font-medium">Nhiệm vụ gần đây</h2>
          <button className="btn btn-sm" onClick={load} disabled={loading}>{loading ? "Đang tải…" : "Làm mới"}</button>
        </div>
        <MiniTable cols={[
          { key: "id", label: "Mã" },
          { key: "title", label: "Tiêu đề" },
          { key: "intern_name", label: "Thực tập sinh" },
          { key: "status", label: "Trạng thái" },
          { key: "updated_at", label: "Cập nhật" },
        ]} rows={tasks} />
      </section>
    </div>
  );
}
