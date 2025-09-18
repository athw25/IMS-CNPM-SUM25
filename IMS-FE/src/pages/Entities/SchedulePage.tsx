import { useEffect, useState } from 'react'
import DataTable from '../../components/DataTable'
import { schedule } from '../../api/schedule'
import { Input, Select, DateTime } from '../../components/Form'
import ConfirmDialog from '../../components/ConfirmDialog'

export default function SchedulePage() {
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [data, setData] = useState<any>({items:[], page:1, limit:10, total:0})

  const [internId, setInternId] = useState('1')
  const [title, setTitle] = useState('Lịch mới')
  const [type, setType] = useState('Onboarding')
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')
  const [loc, setLoc] = useState('HQ')

  async function load(){ setData(await schedule.list({ intern_id: internId || undefined, page, limit })) }
  useEffect(() => { load() }, [page])

  return (
    <div className="space-y-3">
      <div className="card p-3">
        <div className="font-semibold mb-2">Tạo lịch</div>
        <div className="grid md:grid-cols-3 gap-3">
          <Input label="InternProfile ID" value={internId} onChange={e=>setInternId(e.target.value)} />
          <Input label="Tiêu đề" value={title} onChange={e=>setTitle(e.target.value)} />
          <Select label="Loại" value={type} onChange={e=>setType(e.target.value)}>
            <option>Interview</option><option>Onboarding</option><option>Training</option><option>Work</option>
          </Select>
          <DateTime label="Bắt đầu" value={start} onChange={e=>setStart(e.target.value)} />
          <DateTime label="Kết thúc" value={end} onChange={e=>setEnd(e.target.value)} />
          <Input label="Địa điểm" value={loc} onChange={e=>setLoc(e.target.value)} />
        </div>
        <div className="mt-2">
          <button className="btn btn-primary" onClick={async ()=>{ await schedule.create({ intern_id:Number(internId), title, type, start_time:start, end_time:end, location:loc }); await load() }}>Tạo</button>
        </div>
      </div>

      <DataTable
        columns={[
          { key:'id', header:'ID' },
          { key:'title', header:'Tiêu đề' },
          { key:'type', header:'Loại' },
          { key:'start_time', header:'Bắt đầu' },
          { key:'end_time', header:'Kết thúc' },
          { key:'actions', header:'Thao tác', render:(r:any)=> (
            <ConfirmDialog title="Xóa" message="Xóa lịch?" onConfirm={async ()=>{ await schedule.remove(r.id); await load() }} />
          ) }
        ]}
        rows={data.items}
        page={data.page} limit={data.limit} total={data.total}
        onPageChange={setPage}
      />
    </div>
  )
}
