import { useEffect, useState } from 'react'
import DataTable from '../../components/DataTable'
import { profiles } from '../../api/profiles'
import { Input, Select } from '../../components/Form'

export default function InternProfilesPage() {
  const [status, setStatus] = useState('')
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [data, setData] = useState<any>({items:[], page:1, limit:10, total:0})

  useEffect(() => {
    profiles.list({ status: status || undefined, page, limit }).then(setData)
  }, [status, page])

  return (
    <div className="space-y-3">
      <Select label="Trạng thái" value={status} onChange={e=>setStatus(e.target.value)}>
        <option value="">Tất cả</option>
        <option>Active</option><option>Paused</option><option>Completed</option>
      </Select>
      <DataTable
        columns={[
          { key:'id', header:'ID', width:'80px' },
          { key:'user_id', header:'User' },
          { key:'school', header:'Trường' },
          { key:'major', header:'Chuyên ngành' },
          { key:'gpa', header:'GPA' }
        ]}
        rows={data.items}
        page={data.page} limit={data.limit} total={data.total}
        onPageChange={setPage}
      />
    </div>
  )
}
