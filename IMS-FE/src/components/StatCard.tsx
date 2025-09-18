// path: src/components/StatCard.tsx
type Props = { title: string; value?: number | string; hint?: string; loading?: boolean };
export default function StatCard({ title, value, hint, loading }: Props) {
  return (
    <div className="card">
      <div className="text-sm opacity-70">{title}</div>
      <div className="text-2xl font-semibold my-1">{loading ? "…" : value ?? "—"}</div>
      {hint && <div className="text-xs opacity-60">{hint}</div>}
    </div>
  );
}
