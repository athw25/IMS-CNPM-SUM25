import { useEffect, useMemo, useState } from 'react'

export type Column<T> = {
  key: keyof T | string
  header: string
  render?: (row: T) => React.ReactNode
  width?: string
}
type Props<T> = {
  columns: Column<T>[]
  rows: T[]
  page: number
  limit: number
  total: number
  onPageChange: (p:number) => void
  onSearch?: (q:string) => void
  right?: React.ReactNode
}
export default function DataTable<T extends { id?: number | string }>(p: Props<T>) {
  const pages = Math.max(1, Math.ceil(p.total / p.limit))
  const [q, setQ] = useState('')
  useEffect(() => { const h = setTimeout(() => p.onSearch?.(q), 400); return () => clearTimeout(h) }, [q])
  return (
    <div className="card p-3">
      <div className="flex items-center justify-between gap-3 mb-3">
        <input className="input max-w-sm" placeholder="Tìm kiếm..." value={q} onChange={e => setQ(e.target.value)} />
        <div>{p.right}</div>
      </div>
      <div className="overflow-x-auto">
        <table className="table">
          <thead>
            <tr>{p.columns.map(c => <th key={String(c.key)} style={{width: c.width}}>{c.header}</th>)}</tr>
          </thead>
          <tbody>
            {p.rows.length === 0 && <tr><td className="py-6 text-center text-gray-500" colSpan={p.columns.length}>Không có dữ liệu</td></tr>}
            {p.rows.map((r, i) => (
              <tr key={String((r as any).id ?? i)}>
                {p.columns.map(c => <td key={String(c.key)}>{c.render ? c.render(r) : String((r as any)[c.key as any])}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex items-center justify-end gap-2 mt-3">
        <button className="btn" disabled={p.page<=1} onClick={() => p.onPageChange(p.page-1)}>Trước</button>
        <div className="text-sm">Trang {p.page}/{pages}</div>
        <button className="btn" disabled={p.page>=pages} onClick={() => p.onPageChange(p.page+1)}>Sau</button>
      </div>
    </div>
  )
}
