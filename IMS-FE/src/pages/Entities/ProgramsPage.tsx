import { useEffect, useState } from 'react'
import DataTable from '../../components/DataTable'
import { programs } from '../../api/programs'
import { Input } from '../../components/Form'
import ConfirmDialog from '../../components/ConfirmDialog'

export default function ProgramsPage() {
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [data, setData] = useState<any>({items:[], page:1, limit:10, total:0})
  const [title, setTitle] = useState('Chương trình mới')
  const [goal, setGoal] = useState('')

  async function load(){ setData(await programs.list({ page, limit })) }
  useEffect(() => { load() }, [page])

  return (
    <div className="space-y-3">
      <div className="card p-3">
        <div className="font-semibold mb-2">Tạo chương trình</div>
        <div className="grid md:grid-cols-2 gap-3">
          <Input label="Tiêu đề" value={title} onChange={e=>setTitle(e.target.value)} />
          <Input label="Mục tiêu" value={goal} onChange={e=>setGoal(e.target.value)} />
        </div>
        <div className="mt-2">
          <button className="btn btn-primary" onClick={async ()=>{ await programs.create({title, goal}); await load() }}>Tạo</button>
        </div>
      </div>

      <DataTable
        columns={[
          { key:'id', header:'ID', width:'80px' },
          { key:'title', header:'Tiêu đề' },
          { key:'goal', header:'Mục tiêu' },
          { key:'actions', header:'Thao tác', render:(r:any)=> (
            <ConfirmDialog title="Xóa" message="Xóa chương trình? (bị chặn nếu có dự án)" onConfirm={async ()=>{ try { await programs.remove(r.id); await load() } catch(e:any){ alert(e.message) } }} />
          ) }
        ]}
        rows={data.items}
        page={data.page} limit={data.limit} total={data.total}
        onPageChange={setPage}
      />
    </div>
  )
}
