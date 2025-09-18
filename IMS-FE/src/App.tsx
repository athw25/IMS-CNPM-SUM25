import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import { AuthProvider } from './contexts/AuthContext'
import Login from './pages/Auth/Login'
import Register from './pages/Auth/Register'
import Home from './pages/Home'
import { routes } from './routes/routes'
import ProtectedRoute from './routes/ProtectedRoute'

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<Layout />}>
          <Route index element={<Home />} />
          {routes.map((r) => (
            <Route
              key={r.path}
              path={r.path}
              element={
                r.protected ? (
                  <ProtectedRoute roles={r.roles}>
                    <r.element />
                  </ProtectedRoute>
                ) : (
                  <r.element />
                )
              }
            />
          ))}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </AuthProvider>
  )
}
