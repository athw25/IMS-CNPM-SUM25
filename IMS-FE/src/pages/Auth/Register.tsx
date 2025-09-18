// path: src/pages/Auth/Register.tsx
import React, { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { Input, Select } from '../../components/Form'
import type { Role } from '../../types'
import { Link } from 'react-router-dom'

export default function Register() {
  const { register, user } = useAuth()

  // Mặc định Intern; nếu người dùng chưa đăng nhập thì sẽ cố định Intern
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState<Role>('Intern')
  const [err, setErr] = useState<string | null>(null)

  async function handle(e: React.FormEvent) {
    e.preventDefault()
    setErr(null)
    try {
      // Nếu chưa đăng nhập -> ép role = Intern (backend cũng enforce như vậy)
      const finalRole: Role = user ? role : 'Intern'
      await register(name, email, password, finalRole)
    } catch (e: any) {
      setErr(e.message || 'Đăng ký thất bại')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md card p-6 space-y-4">
        <h1 className="text-2xl font-semibold text-blue-600">Đăng kí</h1>
        {err && <div className="text-red-600 text-sm">{err}</div>}

        <form onSubmit={handle} className="space-y-3">
          <Input label="Họ tên" value={name} onChange={e => setName(e.target.value)} required />
          <Input label="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          <Input label="Mật khẩu" type="password" value={password} onChange={e => setPassword(e.target.value)} required />

          {/* Nếu chưa đăng nhập: ẩn select role (mặc định Intern).
              Nếu đã đăng nhập (Admin/HR): cho phép chọn role để tạo hộ. */}
          {user ? (
            <Select label="Vai trò" value={role} onChange={e => setRole(e.target.value as Role)}>
              <option>Intern</option>
              <option>HR</option>
              <option>Coordinator</option>
              <option>Mentor</option>
              <option>Admin</option>
            </Select>
          ) : (
            <p className="text-xs opacity-70">
              Lưu ý: Tài khoản ẩn danh chỉ đăng ký được vai trò <b>Intern</b>.
            </p>
          )}

          <button className="btn w-full" type="submit">Tạo tài khoản</button>
        </form>

        <p className="text-sm">
          Đã có tài khoản? <Link to="/login" className="underline">Đăng nhập</Link>
        </p>
      </div>
    </div>
  )
}
