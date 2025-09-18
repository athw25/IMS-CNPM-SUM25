import { useEffect, useState } from 'react'
import DataTable from '../../components/DataTable'
import { kpi } from '../../api/kpi'
import { Input } from '../../components/Form'

export default function KPIPage() {
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [data, setData] = useState<any>({items:[], page:1, limit:10, total:0})
  const [internId, setInternId] = useState('1')
  const [key, setKey] = useState('tasks_completed')
  const [value, setValue] = useState('1')
  const [period, setPeriod] = useState('month')
  const [note, setNote] = useState('')

  async function load(){ setData(await kpi.list({ intern_id: internId || undefined, page, limit })) }
  useEffect(() => { load() }, [page])

  return (
    <div className="space-y-3">
      <div className="card p-3">
        <div className="font-semibold mb-2">Ghi KPI</div>
        <div className="grid md:grid-cols-4 gap-3">
          <Input label="InternProfile ID" value={internId} onChange={e=>setInternId(e.target.value)} />
          <Input label="Chỉ số (kpi_key)" value={key} onChange={e=>setKey(e.target.value)} />
          <Input label="Giá trị" value={value} onChange={e=>setValue(e.target.value)} />
          <Input label="Kỳ (period)" value={period} onChange={e=>setPeriod(e.target.value)} />
          <Input label="Ghi chú" value={note} onChange={e=>setNote(e.target.value)} />
        </div>
        <div className="mt-2">
          <button className="btn btn-primary" onClick={async ()=>{ await kpi.create({ intern_id:Number(internId), kpi_key:key, value:Number(value), period, note }); await load() }}>Ghi</button>
        </div>
      </div>

      <DataTable
        columns={[
          { key:'id', header:'ID' },
          { key:'intern_id', header:'Intern' },
          { key:'kpi_key', header:'KPI' },
          { key:'value', header:'Giá trị' },
          { key:'period', header:'Kỳ' },
          { key:'note', header:'Ghi chú' }
        ]}
        rows={data.items}
        page={data.page} limit={data.limit} total={data.total}
        onPageChange={setPage}
      />
    </div>
  )
}
