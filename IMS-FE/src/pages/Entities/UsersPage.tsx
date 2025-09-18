import { useEffect, useState } from 'react'
import { users } from '../../api/users'
import DataTable from '../../components/DataTable'
import { Input, Select } from '../../components/Form'
import Toast from '../../components/Toast'

export default function UsersPage() {
  const [role, setRole] = useState('')
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [data, setData] = useState<any>({items:[], page:1, limit:10, total:0})
  const [toast, setToast] = useState<string|undefined>()

  async function load() {
    const res = await users.list({ role: role || undefined, page, limit })
    setData(res)
  }
  useEffect(() => { load().catch(e=>setToast(e.message)) }, [role, page])

  return (
    <div className="space-y-3">
      <div className="flex gap-3">
        <Select label="Vai trò" value={role} onChange={e=>setRole(e.target.value)}>
          <option value="">Tất cả</option>
          <option>Admin</option><option>HR</option><option>Coordinator</option><option>Mentor</option><option>Intern</option>
        </Select>
      </div>
      <DataTable
        columns={[
          { key:'id', header:'ID', width:'80px' },
          { key:'name', header:'Họ tên' },
          { key:'email', header:'Email' },
          { key:'role', header:'Vai trò' },
        ]}
        rows={data.items}
        page={data.page} limit={data.limit} total={data.total}
        onPageChange={setPage}
      />
      {toast && <Toast text={toast} />}
    </div>
  )
}
