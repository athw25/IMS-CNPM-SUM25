import { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import Toast from '../../components/Toast'

import { Link } from "react-router-dom";


export default function Login() {
  const { login } = useAuth()
  const [email, setEmail] = useState('admin@ims.local')
  const [password, setPassword] = useState('password')
  const [toast, setToast] = useState<string|undefined>()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    try {
      await login(email, password)
      setToast('Đăng nhập thành công!')
    } catch (e:any) {
      setToast(e?.message || 'Đăng nhập thất bại')
    }
  }

  return (
   <div className="max-w-md mx-auto card p-4">
     <h1 className="text-xl font-semibold mb-3">Đăng nhập</h1>
     <form onSubmit={handleSubmit} className="space-y-3">
       <label className="block">
         <div className="label">Email</div>
         <input className="input" value={email} onChange={e=>setEmail(e.target.value)} placeholder="nhập email" />
       </label>
       <label className="block">
         <div className="label">Mật khẩu</div>
         <input type="password" className="input" value={password} onChange={e=>setPassword(e.target.value)} placeholder="mật khẩu" />
       </label>
       <button className="btn btn-primary w-full" type="submit">Đăng nhập</button>
        <p className="text-sm">Chưa có tài khoản? <Link to="/register" className="link">Đăng ký</Link></p>
       <p className="text-xs text-gray-500">Tài khoản mẫu: admin@ims.local / password (hoặc hr@ims.local, coord@ims.local, mentor@ims.local, intern@ims.local)</p>
     </form>
     {toast && <Toast text={toast} />}
   </div>
  )
}
