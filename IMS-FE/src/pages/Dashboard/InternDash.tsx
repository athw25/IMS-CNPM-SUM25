// path: src/pages/Dashboard/Intern/InternDash.tsx
import { useEffect, useState } from "react";
import MiniTable from "../../components/MiniTable";
import { getInternBoard } from "../../api/intern";

export default function InternDash() {
  const [loading, setLoading] = useState(true);
  const [board, setBoard] = useState<any>({ assignments: [], schedule: [], resources: [] });

  async function load() {
    setLoading(true);
    try {
      const data = await getInternBoard();
      setBoard({
        assignments: data?.assignments ?? [],
        schedule: data?.schedule ?? [],
        resources: data?.resources ?? [],
      });
    } finally {
      setLoading(false);
    }
  }
  useEffect(()=>{ load(); }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Bảng điều khiển</h1>

      <section className="card">
        <div className="flex items-center justify-between mb-2">
          <h2 className="font-medium">Nhiệm vụ của tôi</h2>
          <button className="btn btn-sm" onClick={load} disabled={loading}>{loading ? "Đang tải…" : "Làm mới"}</button>
        </div>
        <MiniTable cols={[
          { key: "title", label: "Tiêu đề" },
          { key: "status", label: "Trạng thái" },
          { key: "due_date", label: "Hạn chót" },
          { key: "mentor_name", label: "Mentor" },
        ]} rows={board.assignments} />
      </section>

      <section className="card">
        <h2 className="font-medium mb-2">Lịch làm việc</h2>
        <MiniTable cols={[
          { key: "title", label: "Tiêu đề" },
          { key: "start_time", label: "Bắt đầu" },
          { key: "end_time", label: "Kết thúc" },
          { key: "location", label: "Địa điểm" },
        ]} rows={board.schedule} />
      </section>

      <section className="card">
        <h2 className="font-medium mb-2">Tài liệu học tập & phản hồi</h2>
        <MiniTable cols={[
          { key: "name", label: "Tên" },
          { key: "type", label: "Loại" },
          { key: "updated_at", label: "Cập nhật" },
          { key: "link", label: "Liên kết", render: (v)=> v ? <a className="underline" href={v} target="_blank">Mở</a> : "—" },
        ]} rows={board.resources} />
      </section>
    </div>
  );
}
