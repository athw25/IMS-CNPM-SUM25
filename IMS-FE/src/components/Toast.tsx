import { useEffect, useState } from 'react'

export default function Toast({ text, timeout=2000 }: { text: string; timeout?: number }) {
  const [show, setShow] = useState(true)
  useEffect(() => { const t = setTimeout(() => setShow(false), timeout); return () => clearTimeout(t) }, [timeout])
  if (!show) return null
  return <div className="toast">{text}</div>
}
