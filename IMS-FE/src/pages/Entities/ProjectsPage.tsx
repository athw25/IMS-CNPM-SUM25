import { useEffect, useState } from 'react'
import DataTable from '../../components/DataTable'
import { projects } from '../../api/projects'
import { Input } from '../../components/Form'
import ConfirmDialog from '../../components/ConfirmDialog'
import { useAuth } from '../../contexts/AuthContext'

export default function ProjectsPage() {
  const { user } = useAuth()
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [data, setData] = useState<any>({items:[], page:1, limit:10, total:0})
  const [progId, setProgId] = useState('1')
  const [title, setTitle] = useState('Dự án mới')
  const [desc, setDesc] = useState('')

  async function load(){ setData(await projects.list({ prog_id: progId, page, limit })) }
  useEffect(() => { load() }, [page, progId])

  return (
    <div className="space-y-3">
      <div className="card p-3">
        <div className="font-semibold mb-2">Tạo dự án</div>
        <div className="grid md:grid-cols-3 gap-3">
          <Input label="Program ID" value={progId} onChange={e=>setProgId(e.target.value)} />
          <Input label="Tiêu đề" value={title} onChange={e=>setTitle(e.target.value)} />
          <Input label="Mô tả" value={desc} onChange={e=>setDesc(e.target.value)} />
        </div>
        <div className="mt-2">
          <button className="btn btn-primary" onClick={async ()=>{ await projects.create({prog_id:Number(progId), title, description:desc, owner_id: user?.id}); await load() }}>Tạo</button>
        </div>
      </div>

      <DataTable
        columns={[
          { key:'id', header:'ID', width:'80px' },
          { key:'prog_id', header:'Program' },
          { key:'title', header:'Tiêu đề' },
          { key:'owner_id', header:'Chủ trì' },
          { key:'actions', header:'Thao tác', render:(r:any)=> (
            <ConfirmDialog title="Xóa" message="Xóa dự án? (bị chặn nếu có assignment)" onConfirm={async ()=>{ try { await projects.remove(r.id); await load() } catch(e:any){ alert(e.message) } }} />
          ) }
        ]}
        rows={data.items}
        page={data.page} limit={data.limit} total={data.total}
        onPageChange={setPage}
      />
    </div>
  )
}
