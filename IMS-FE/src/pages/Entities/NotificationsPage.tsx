import { useEffect, useState } from 'react'
import DataTable from '../../components/DataTable'
import { notifications } from '../../api/notifications'

export default function NotificationsPage() {
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [data, setData] = useState<any>({items:[], page:1, limit:10, total:0})

  async function load(){ setData(await notifications.list({ page, limit })) }
  useEffect(() => { load() }, [page])

  return (
    <div className="space-y-3">
      <DataTable
        columns={[
          { key:'id', header:'ID' },
          { key:'type', header:'Loại' },
          { key:'payload', header:'Nội dung', render:(r:any)=> <pre className="text-xs">{JSON.stringify(r.payload, null, 2)}</pre> },
          { key:'is_read', header:'Trạng thái', render:(r:any)=> r.is_read ? 'Đã đọc' : 'Chưa đọc' },
          { key:'actions', header:'Thao tác', render:(r:any)=> !r.is_read && <button className="btn" onClick={async ()=>{ await notifications.markRead(r.id); await load() }}>Đánh dấu đã đọc</button> }
        ]}
        rows={data.items}
        page={data.page} limit={data.limit} total={data.total}
        onPageChange={setPage}
      />
    </div>
  )
}
