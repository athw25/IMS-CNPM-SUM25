import { useEffect, useState } from 'react'
import DataTable from '../../components/DataTable'
import { assignments } from '../../api/assignments'
import { Input, Select } from '../../components/Form'
import Toast from '../../components/Toast'

export default function AssignmentsPage() {
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [data, setData] = useState<any>({items:[], page:1, limit:10, total:0})
  const [projId, setProjId] = useState('')
  const [internId, setInternId] = useState('')
  const [status, setStatus] = useState('')
  const [toast, setToast] = useState<string|undefined>()

  async function load(){ setData(await assignments.list({ proj_id: projId || undefined, intern_id: internId || undefined, status: status || undefined, page, limit })) }
  useEffect(() => { load() }, [page, projId, internId, status])

  async function advance(r:any) {
    const next = r.status==='Pending' ? 'Doing' : r.status==='Doing' ? 'Done' : null
    if (!next) return
    try {
      await assignments.updateStatus(r.id, next)
      await load()
      setToast('Cập nhật trạng thái thành công')
    } catch(e:any){ setToast(e.message) }
  }

  return (
    <div className="space-y-3">
      <div className="grid md:grid-cols-3 gap-3">
        <Input label="Project ID" value={projId} onChange={e=>setProjId(e.target.value)} />
        <Input label="InternProfile ID" value={internId} onChange={e=>setInternId(e.target.value)} />
        <Select label="Trạng thái" value={status} onChange={e=>setStatus(e.target.value)}>
          <option value="">Tất cả</option><option>Pending</option><option>Doing</option><option>Done</option>
        </Select>
      </div>
      <DataTable
        columns={[
          { key:'id', header:'ID' },
          { key:'proj_id', header:'Dự án' },
          { key:'intern_id', header:'Intern' },
          { key:'status', header:'Trạng thái' },
          { key:'actions', header:'Thao tác', render:(r:any)=> (
            <div className="flex gap-2">
              {r.status!=='Done' && <button className="btn" onClick={()=>advance(r)}>
                {r.status==='Pending' ? 'Bắt đầu (Doing)' : 'Hoàn tất (Done)'}
              </button>}
            </div>
          ) }
        ]}
        rows={data.items}
        page={data.page} limit={data.limit} total={data.total}
        onPageChange={setPage}
      />
      {toast && <Toast text={toast} />}
    </div>
  )
}
