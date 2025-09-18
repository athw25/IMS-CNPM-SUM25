import { useEffect, useState } from 'react'
import { chat } from '../../api/chat'

export default function ChatPage() {
  const [threads, setThreads] = useState<any>({items:[], page:1, limit:10, total:0})
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [active, setActive] = useState<number|undefined>()
  const [messages, setMessages] = useState<any>({items:[], page:1, limit:20, total:0})
  const [content, setContent] = useState('')

  useEffect(() => { chat.listThreads({ page, limit }).then(setThreads) }, [page])
  useEffect(() => { if(active) chat.listMessages(active, { page:1, limit:20 }).then(setMessages) }, [active])

  async function send() {
    if (!active || !content.trim()) return
    await chat.postMessage(active, { content })
    setContent('')
    setMessages(await chat.listMessages(active, { page:1, limit:20 }))
  }

  return (
    <div className="grid md:grid-cols-3 gap-3">
      <div className="card p-3">
        <div className="font-semibold mb-2">Đoạn hội thoại</div>
        <ul className="space-y-1">
          {threads.items.map((t:any) => (
            <li key={t.id}>
              <button className={"sidebar-link w-full text-left " + (active===t.id?'sidebar-active':'')} onClick={()=>setActive(t.id)}>
                Thread #{t.id} (A:{t.user_a_id}–B:{t.user_b_id})
              </button>
            </li>
          ))}
        </ul>
      </div>
      <div className="md:col-span-2 card p-3">
        {active ? (
          <>
            <div className="font-semibold mb-2">Tin nhắn #{active}</div>
            <div className="h-80 overflow-auto border border-gray-200 dark:border-gray-800 rounded-lg p-2 space-y-1">
              {messages.items.map((m:any) => (
                <div key={m.id} className="text-sm"><b>{m.sender_id}:</b> {m.content}</div>
              ))}
            </div>
            <div className="mt-2 flex gap-2">
              <input className="input" placeholder="Nhập tin nhắn..." value={content} onChange={e=>setContent(e.target.value)} />
              <button className="btn btn-primary" onClick={send}>Gửi</button>
            </div>
          </>
        ) : (<div>Chọn đoạn hội thoại để xem.</div>)}
      </div>
    </div>
  )
}
