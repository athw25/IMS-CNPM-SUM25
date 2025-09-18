import { useEffect, useState } from 'react'
import DataTable from '../../components/DataTable'
import { applications } from '../../api/applications'
import { Select } from '../../components/Form'

export default function ApplicationsPage() {
  const [status, setStatus] = useState('')
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [data, setData] = useState<any>({items:[], page:1, limit:10, total:0})

  async function load() {
    setData(await applications.list({ status: status || undefined, page, limit }))
  }
  useEffect(() => { load() }, [status, page])

  return (
    <div className="space-y-3">
      <Select label="Trạng thái" value={status} onChange={e=>setStatus(e.target.value)}>
        <option value="">Tất cả</option><option>Pending</option><option>Approved</option><option>Rejected</option>
      </Select>
      <DataTable
        columns={[
          { key:'id', header:'ID', width:'80px' },
          { key:'camp_id', header:'Chiến dịch' },
          { key:'user_id', header:'Ứng viên' },
          { key:'status', header:'Trạng thái' },
          { key:'actions', header:'Thao tác', render:(r:any)=> (
            <div className="flex gap-2">
              <button className="btn" onClick={async ()=>{ await applications.patch(r.id,{status:'Approved'}); await load() }}>Duyệt</button>
              <button className="btn" onClick={async ()=>{ await applications.patch(r.id,{status:'Rejected'}); await load() }}>Từ chối</button>
            </div>
          ) }
        ]}
        rows={data.items}
        page={data.page} limit={data.limit} total={data.total}
        onPageChange={setPage}
      />
    </div>
  )
}
