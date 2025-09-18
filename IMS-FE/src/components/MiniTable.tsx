// path: src/components/MiniTable.tsx
type Col<T> = { key: keyof T; label: string; render?: (v: any, row: T) => any };
export default function MiniTable<T>({ cols, rows }: { cols: Col<T>[]; rows: T[] }) {
  return (
    <div className="overflow-auto rounded-2xl border border-gray-200 dark:border-neutral-800">
      <table className="w-full table">
        <thead>
          <tr>{cols.map(c => <th key={String(c.key)} className="text-left p-2">{c.label}</th>)}</tr>
        </thead>
        <tbody>
          {rows.length ? rows.map((r, i) => (
            <tr key={i} className="odd:bg-gray-50/60 dark:odd:bg-neutral-900/50">
              {cols.map(c => <td key={String(c.key)} className="p-2">{c.render ? c.render((r as any)[c.key], r) : (r as any)[c.key]}</td>)}
            </tr>
          )) : (
            <tr><td className="p-3 text-sm opacity-70" colSpan={cols.length}>Không có dữ liệu</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
