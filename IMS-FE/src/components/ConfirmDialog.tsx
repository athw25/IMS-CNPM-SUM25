import { useState } from 'react'

export default function ConfirmDialog({ title='Xác nhận', message='Bạn có chắc?', onConfirm }: {title?:string; message?:string; onConfirm:() => Promise<void>|void}) {
  const [open, setOpen] = useState(false)
  return (
    <>
      <button className="btn" onClick={() => setOpen(true)}>{title}</button>
      {open && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="card p-4 max-w-sm w-full">
            <div className="font-semibold mb-2">{title}</div>
            <div className="text-sm text-gray-500 mb-4">{message}</div>
            <div className="flex justify-end gap-2">
              <button className="btn" onClick={() => setOpen(false)}>Hủy</button>
              <button className="btn btn-primary" onClick={async () => { await onConfirm(); setOpen(false) }}>Đồng ý</button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
