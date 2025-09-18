import { useEffect, useState } from 'react'
import DataTable from '../../components/DataTable'
import { campaigns } from '../../api/campaigns'
import { Input, Select } from '../../components/Form'
import ConfirmDialog from '../../components/ConfirmDialog'
import Toast from '../../components/Toast'

export default function CampaignsPage() {
  const [status, setStatus] = useState('')
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [data, setData] = useState<any>({items:[], page:1, limit:10, total:0})
  const [title, setTitle] = useState('Chiến dịch mới')
  const [desc, setDesc] = useState('')

  async function load(){ setData(await campaigns.list({ status: status || undefined, page, limit })) }
  useEffect(() => { load() }, [status, page])

  return (
    <div className="space-y-3">
      <div className="card p-3">
        <div className="font-semibold mb-2">Tạo chiến dịch</div>
        <div className="grid md:grid-cols-2 gap-3">
          <Input label="Tiêu đề" value={title} onChange={e=>setTitle(e.target.value)} />
          <Input label="Mô tả" value={desc} onChange={e=>setDesc(e.target.value)} />
        </div>
        <div className="mt-2">
          <button className="btn btn-primary" onClick={async ()=>{ await campaigns.create({title, description: desc}); await load() }}>Tạo</button>
        </div>
      </div>

      <Select label="Trạng thái" value={status} onChange={e=>setStatus(e.target.value)}>
        <option value="">Tất cả</option><option>Open</option><option>Closed</option>
      </Select>

      <DataTable
        columns={[
          { key:'id', header:'ID', width:'80px' },
          { key:'title', header:'Tiêu đề' },
          { key:'status', header:'Trạng thái' },
          { key:'created_by', header:'Tạo bởi' },
          { key:'actions', header:'Thao tác', render:(r:any) => (
            <div className="flex gap-2">
              <button className="btn" onClick={async ()=>{ await campaigns.patch(r.id, {status: r.status==='Open'?'Closed':'Open'}); await load() }}>{r.status==='Open'?'Đóng':'Mở'}</button>
              <ConfirmDialog title="Xóa" message="Xóa chiến dịch? (bị chặn nếu đã có đơn)" onConfirm={async ()=>{ try{ await campaigns.remove(r.id); await load() } catch(e:any){ alert(e.message) } }} />
            </div>
          )}
        ]}
        rows={data.items}
        page={data.page} limit={data.limit} total={data.total}
        onPageChange={setPage}
      />
    </div>
  )
}
