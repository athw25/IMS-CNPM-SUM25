// path: src/pages/Dashboard/Admin/HealthPage.tsx
import { useEffect, useState } from "react";
import RefreshButton from "../../components/RefreshButton";
import { getHealth } from "../../api/admin";
import StatCard from "../../components/StatCard";

export default function HealthPage() {
  const [loading, setLoading] = useState(true);
  const [health, setHealth] = useState<any>(null);
  async function load() {
    setLoading(true);
    try {
      const data = await getHealth();
      setHealth(data);
    } finally {
      setLoading(false);
    }
  }
  useEffect(()=>{ load(); }, []);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Sức khỏe hệ thống</h1>
        <RefreshButton onClick={load} loading={loading} />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatCard title="API" value={health?.api?.toUpperCase?.()} loading={loading} hint="Trạng thái dịch vụ API" />
        <StatCard title="CSDL" value={health?.db?.toUpperCase?.()} loading={loading} hint="Kết nối cơ sở dữ liệu" />
        <StatCard title="Độ trễ (ms)" value={health?.latency_ms} loading={loading} hint="Request round-trip" />
        <StatCard title="Giờ máy chủ" value={health?.server_time?.replace('T',' ').replace('Z','')} loading={loading} hint="ISO time" />
      </div>

      <div className="card">
        <h2 className="font-medium mb-2">Xử lý sự cố nhanh</h2>
        <ol className="list-decimal pl-5 text-sm space-y-2 opacity-90">
          <li>Kiểm tra cấu hình mạng, proxy, CORS giữa FE/BE.</li>
          <li>Nếu DB = <code>fail</code>: kiểm tra biến môi trường DB của backend và quyền truy cập.</li>
          <li>Nếu API = <code>fail</code>: xem log máy chủ, kiểm tra /admin/health trực tiếp.</li>
          <li>Độ trễ cao: kiểm thử lại ở môi trường nội bộ; đọc log truy vấn chậm.</li>
        </ol>
      </div>
    </div>
  );
}
