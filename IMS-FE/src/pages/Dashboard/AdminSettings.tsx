// path: src/pages/Dashboard/Admin/AdminSettings.tsx
import { useEffect, useMemo, useState } from "react";
import { getAppConfig, saveAppConfig, getSecurityConfig, saveSecurityConfig, rotateJwtKeys, listUsers, updateUserRole } from "../../api/admin-settings";
import type { Role } from "../../types";

type TabKey = "general" | "rbac" | "security";

export default function AdminSettings() {
  const [tab, setTab] = useState<TabKey>("general");

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Cấu hình & bảo trì hệ thống</h1>

      <div className="flex gap-2">
        <TabBtn k="general" cur={tab} set={setTab} label="Cài đặt chung" />
        <TabBtn k="rbac" cur={tab} set={setTab} label="Phân quyền người dùng (RBAC)" />
        <TabBtn k="security" cur={tab} set={setTab} label="Bảo mật dữ liệu" />
      </div>

      {tab === "general" && <GeneralTab />}
      {tab === "rbac" && <RBACTab />}
      {tab === "security" && <SecurityTab />}
    </div>
  );
}

function TabBtn({ k, cur, set, label }: { k: TabKey; cur: TabKey; set: (k: TabKey)=>void; label: string }) {
  const active = cur === k;
  return (
    <button
      onClick={()=>set(k)}
      className={`btn btn-sm ${active ? "bg-gray-100 dark:bg-neutral-800" : ""}`}
      aria-pressed={active}
    >
      {label}
    </button>
  );
}

/* --------- GENERAL --------- */
function GeneralTab() {
  const [loading, setLoading] = useState(true);
  const [supported, setSupported] = useState(true);
  const [appName, setAppName] = useState("IMS");
  const [defaultLimit, setDefaultLimit] = useState<number>(10);
  const [saveMsg, setSaveMsg] = useState<string>("");

  useEffect(() => {
    (async () => {
      setLoading(true);
      const cfg = await getAppConfig();
      if (!cfg) { setSupported(false); setLoading(false); return; }
      setAppName(cfg.app_name ?? "IMS");
      setDefaultLimit(cfg.default_limit ?? 10);
      setLoading(false);
    })();
  }, []);

  async function onSave() {
    setSaveMsg("");
    const ok = await saveAppConfig({ app_name: appName, default_limit: defaultLimit });
    setSaveMsg(ok ? "Đã lưu cấu hình." : "Backend chưa hỗ trợ lưu cấu hình này.");
  }

  return (
    <section className="card space-y-3">
      <h2 className="font-medium">Cài đặt chung</h2>
      {/* {!supported && <p className="text-sm opacity-80">Backend hiện chưa hỗ trợ <code>/admin/config</code>. Bạn vẫn có thể dùng các tính năng khác ở tab RBAC/Bảo mật.</p>} */}
      <div className="grid md:grid-cols-2 gap-3">
        <div>
          <label className="text-sm opacity-70">Tên hệ thống</label>
          <input className="input w-full" value={appName} onChange={e=>setAppName(e.target.value)} disabled={!supported || loading} />
        </div>
        <div>
          <label className="text-sm opacity-70">Số bản ghi mỗi trang (mặc định)</label>
          <input type="number" className="input w-full" value={defaultLimit} onChange={e=>setDefaultLimit(Number(e.target.value || 10))} disabled={!supported || loading} />
        </div>
      </div>
      <div className="flex gap-2">
        <button onClick={onSave} className="btn btn-sm" disabled={!supported || loading}>Lưu</button>
        {saveMsg && <span className="text-sm opacity-80">{saveMsg}</span>}
      </div>
    </section>
  );
}

/* --------- RBAC --------- */
function RBACTab() {
  const [loading, setLoading] = useState(true);
  const [q, setQ] = useState("");
  const [roleFilter, setRoleFilter] = useState<Role | "">("");
  const [page, setPage] = useState(1);
  const [rows, setRows] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const limit = 10;
  const roles: Role[] = useMemo(()=>["Admin","HR","Coordinator","Mentor","Intern"],[]);

  async function load() {
    setLoading(true);
    const res = await listUsers({ page, limit, q: q || undefined, role: (roleFilter || undefined) as any });
    const items = res?.items ?? res ?? [];
    setRows(items);
    setTotal(res?.total ?? items.length);
    setLoading(false);
  }
  useEffect(()=>{ load(); }, [page, roleFilter]);

  async function onChangeRole(userId: number, newRole: Role) {
    await updateUserRole(userId, newRole);
    await load();
  }

  return (
    <section className="card space-y-3">
      <h2 className="font-medium">Phân quyền người dùng</h2>
      <div className="grid md:grid-cols-3 gap-3">
        <input className="input" placeholder="Tìm theo tên/email…" value={q} onChange={e=>setQ(e.target.value)} />
        <select className="input" value={roleFilter} onChange={e=>setRoleFilter(e.target.value as Role | "")}>
          <option value="">Tất cả vai trò</option>
          {roles.map(r => <option key={r} value={r}>{r}</option>)}
        </select>
        <button className="btn" onClick={()=>{ setPage(1); load(); }} disabled={loading}>Tìm</button>
      </div>

      <div className="overflow-auto rounded-2xl border border-gray-200 dark:border-neutral-800">
        <table className="w-full table">
          <thead>
            <tr>
              <th className="text-left p-2">ID</th>
              <th className="text-left p-2">Họ tên</th>
              <th className="text-left p-2">Email</th>
              <th className="text-left p-2">Vai trò</th>
              <th className="text-left p-2">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            {(rows || []).map((u:any)=>(
              <tr key={u.id} className="odd:bg-gray-50/60 dark:odd:bg-neutral-900/50">
                <td className="p-2">{u.id}</td>
                <td className="p-2">{u.name}</td>
                <td className="p-2">{u.email}</td>
                <td className="p-2">{u.role}</td>
                <td className="p-2">
                  <select
                    className="input"
                    defaultValue={u.role}
                    onChange={(e)=>onChangeRole(u.id, e.target.value as Role)}
                  >
                    {roles.map(r => <option key={r} value={r}>{r}</option>)}
                  </select>
                </td>
              </tr>
            ))}
            {!rows?.length && (
              <tr><td className="p-3 text-sm opacity-70" colSpan={5}>{loading ? "Đang tải…" : "Không có người dùng"}</td></tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="flex items-center gap-2">
        <button className="btn btn-sm" onClick={()=>setPage(p=>Math.max(1, p-1))} disabled={page<=1 || loading}>Trang trước</button>
        <span className="text-sm opacity-80">Trang {page}</span>
        <button className="btn btn-sm" onClick={()=>setPage(p=>p+1)} disabled={loading || rows.length < limit}>Trang sau</button>
        <span className="text-sm opacity-60">Tổng (ước tính): {total}</span>
      </div>
    </section>
  );
}

/* --------- SECURITY --------- */
function SecurityTab() {
  const [loading, setLoading] = useState(true);
  const [supported, setSupported] = useState(true);
  const [cors, setCors] = useState<string>("");
  const [tokenExp, setTokenExp] = useState<number>(3600);
  const [pwdMinLen, setPwdMinLen] = useState<number>(8);
  const [enforceHttps, setEnforceHttps] = useState<boolean>(false);
  const [audit, setAudit] = useState<boolean>(true);
  const [saveMsg, setSaveMsg] = useState("");

  useEffect(() => {
    (async ()=>{
      const sec = await getSecurityConfig();
      if (!sec) { setSupported(false); setLoading(false); return; }
      setCors((sec.cors_origins ?? []).join(","));
      setTokenExp(Number(sec.jwt_access_expires ?? 3600));
      setPwdMinLen(Number(sec.password_min_len ?? 8));
      setEnforceHttps(!!sec.enforce_https);
      setAudit(!!sec.audit_log_enabled);
      setLoading(false);
    })();
  }, []);

  async function onSave() {
    setSaveMsg("");
    const ok = await saveSecurityConfig({
      cors_origins: cors.split(",").map(s=>s.trim()).filter(Boolean),
      jwt_access_expires: tokenExp,
      password_min_len: pwdMinLen,
      enforce_https: enforceHttps,
      audit_log_enabled: audit,
    });
    setSaveMsg(ok ? "Đã lưu cấu hình bảo mật." : "Backend chưa hỗ trợ lưu cấu hình này.");
  }

  async function onRotateKeys() {
    const ok = await rotateJwtKeys();
    setSaveMsg(ok ? "Đã yêu cầu xoay khóa JWT." : "Backend chưa hỗ trợ xoay khóa JWT.");
  }

  return (
    <section className="card space-y-3">
      <h2 className="font-medium">Bảo mật dữ liệu</h2>
      {!supported && (
        <p className="text-sm opacity-80">
          {/* Backend hiện chưa hỗ trợ <code>/admin/security</code>. Bạn vẫn có thể quản trị RBAC ở tab bên cạnh. */}
        </p>
      )}

      <div className="grid md:grid-cols-2 gap-3">
        <div>
          <label className="text-sm opacity-70">CORS Origins (phân tách bởi dấu phẩy)</label>
          <input className="input w-full" value={cors} onChange={e=>setCors(e.target.value)} disabled={!supported || loading} placeholder="http://localhost:5173, https://ims.example.com" />
        </div>
        <div>
          <label className="text-sm opacity-70">JWT Access Expiry (giây)</label>
          <input type="number" className="input w-full" value={tokenExp} onChange={e=>setTokenExp(Number(e.target.value||3600))} disabled={!supported || loading} />
        </div>
        <div>
          <label className="text-sm opacity-70">Độ dài mật khẩu tối thiểu</label>
          <input type="number" className="input w-full" value={pwdMinLen} onChange={e=>setPwdMinLen(Number(e.target.value||8))} disabled={!supported || loading} />
        </div>
        <div className="flex items-center gap-2">
          <input id="https" type="checkbox" className="h-4 w-4" checked={enforceHttps} onChange={e=>setEnforceHttps(e.target.checked)} disabled={!supported || loading} />
          <label htmlFor="https" className="text-sm">Bắt buộc HTTPS</label>
        </div>
        <div className="flex items-center gap-2">
          <input id="audit" type="checkbox" className="h-4 w-4" checked={audit} onChange={e=>setAudit(e.target.checked)} disabled={!supported || loading} />
          <label htmlFor="audit" className="text-sm">Bật ghi nhật ký/audit</label>
        </div>
      </div>

      <div className="flex gap-2">
        <button className="btn btn-sm" onClick={onSave} disabled={!supported || loading}>Lưu</button>
        <button className="btn btn-sm" onClick={onRotateKeys} disabled={loading}>Xoay khóa JWT</button>
        {saveMsg && <span className="text-sm opacity-80">{saveMsg}</span>}
      </div>

      <div className="rounded-xl border border-gray-200 dark:border-neutral-800 p-3 text-sm opacity-90">
        <p className="font-medium mb-1">Khuyến nghị:</p>
        <ul className="list-disc pl-5 space-y-1">
          <li>Đặt <b>JWT Access</b> 15–60 phút; dùng Refresh Token để kéo dài phiên.</li>
          <li>Bật <b>HTTPS</b> trong môi trường triển khai.</li>
          <li>Giới hạn <b>CORS</b> theo domain tin cậy.</li>
          <li>Bật <b>Audit log</b> cho hành động nhạy cảm (đổi quyền, xoá dữ liệu).</li>
        </ul>
      </div>
    </section>
  );
}
