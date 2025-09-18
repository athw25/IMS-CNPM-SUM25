// path: src/components/RefreshButton.tsx
export default function RefreshButton({ onClick, loading }: { onClick: () => void; loading?: boolean }) {
  return (
    <button onClick={onClick} className="btn btn-sm" disabled={loading}>
      {loading ? "Đang làm mới…" : "Làm mới"}
    </button>
  );
}
