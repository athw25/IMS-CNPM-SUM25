# IMS-FE (React 19 + TS + Vite + Tailwind)

Giao diện tiếng Việt cho hệ thống **Intern Management System**.

## Chạy nhanh
```bash
npm install
cp .env.example .env
# nếu backend khác host/port, sửa VITE_API_BASE trong .env
npm run dev
```

## Build & Preview
```bash
npm run build
npm run preview
```

## Ghi chú
- URL API đọc từ `VITE_API_BASE`
- Token được lưu trong `localStorage` và tự refresh khi hết hạn (`/auth/refresh`), sau đó *replay* request 1 lần.
- RBAC: Admin, HR, Coordinator, Mentor, Intern — ẩn menu và chặn route theo vai trò.
- Bảng có phân trang theo `page/limit`; có khung tìm kiếm cơ bản.
- UI dark/light tự động theo system.
