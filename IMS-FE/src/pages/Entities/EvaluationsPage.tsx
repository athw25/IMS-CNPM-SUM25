import { useEffect, useState } from 'react'
import DataTable from '../../components/DataTable'
import { evaluations } from '../../api/evaluations'
import { Input } from '../../components/Form'

export default function EvaluationsPage() {
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [data, setData] = useState<any>({items:[], page:1, limit:10, total:0})
  const [internId, setInternId] = useState('')
  const [score, setScore] = useState('85')
  const [comment, setComment] = useState('Tốt')

  async function load(){ setData(await evaluations.list({ intern_id: internId ? Number(internId) : undefined, page, limit })) }
  useEffect(() => { load() }, [page, internId])

  return (
    <div className="space-y-3">
      <div className="card p-3">
        <div className="font-semibold mb-2">Tạo đánh giá</div>
        <div className="grid md:grid-cols-3 gap-3">
          <Input label="InternProfile ID" value={internId} onChange={e=>setInternId(e.target.value)} />
          <Input label="Điểm (0..100)" value={score} onChange={e=>setScore(e.target.value)} />
          <Input label="Nhận xét" value={comment} onChange={e=>setComment(e.target.value)} />
        </div>
        <div className="mt-2">
          <button className="btn btn-primary" onClick={async ()=>{ await evaluations.create({ intern_id:Number(internId), score:Number(score), comment }); await load() }}>Tạo</button>
        </div>
      </div>

      <DataTable
        columns={[
          { key:'id', header:'ID' },
          { key:'intern_id', header:'Intern' },
          { key:'evaluator_id', header:'Người chấm' },
          { key:'score', header:'Điểm' },
          { key:'comment', header:'Nhận xét' },
        ]}
        rows={data.items}
        page={data.page} limit={data.limit} total={data.total}
        onPageChange={setPage}
      />
    </div>
  )
}
