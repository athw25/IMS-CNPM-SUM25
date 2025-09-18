// path: src/pages/Dashboard/Admin/AdminDash.tsx
import { useEffect, useState } from "react";
import StatCard from "../../components/StatCard";
import MiniTable from "../../components/MiniTable";
import { getOverview } from "../../api/admin";

export default function AdminDash() {
  const [loading, setLoading] = useState(true);
  const [counters, setCounters] = useState<any>({});
  const [recent, setRecent] = useState<{ type: string; name: string; at: string }[]>([]);

  async function load() {
    setLoading(true);
    try {
      const data = await getOverview();
      setCounters(data?.counters ?? {});
      setRecent(data?.recent ?? []);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Bảng điều khiển (Admin)</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatCard title="Người dùng" value={counters.users} loading={loading} />
        <StatCard title="Chiến dịch" value={counters.campaigns} loading={loading} />
        <StatCard title="Chương trình" value={counters.programs} loading={loading} />
        <StatCard title="Dự án" value={counters.projects} loading={loading} />
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <section className="card">
          <div className="flex items-center justify-between mb-2">
            <h2 className="font-medium">Hoạt động gần đây</h2>
            <button className="btn btn-sm" onClick={load} disabled={loading}>{loading ? "Đang tải…" : "Làm mới"}</button>
          </div>
          <MiniTable cols={[
            { key: "type", label: "Loại" },
            { key: "name", label: "Tên" },
            { key: "at", label: "Thời gian" },
          ]} rows={recent} />
        </section>

        <section className="card">
          <h2 className="font-medium mb-2">Hỗ trợ kỹ thuật</h2>
          <ul className="list-disc pl-5 text-sm space-y-2 opacity-90">
            <li>Nếu không đăng nhập được: kiểm tra cấu hình <code>VITE_API_BASE</code> và trạng thái máy chủ.</li>
            <li>Nếu API trả 401 liên tục: đăng xuất và đăng nhập lại để cấp mới token.</li>
            <li>Kiểm tra <strong>Sức khỏe hệ thống</strong> tại mục “Health”.</li>
            <li>Liên hệ Điều phối viên/Quản trị khi DB báo “fail”.</li>
          </ul>
        </section>
      </div>
    </div>
  );
}
