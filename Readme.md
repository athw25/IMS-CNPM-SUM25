# Intern Management System (IMS)

## 1. Giới thiệu

`IMS.zip` bao gồm **toàn bộ mã nguồn Backend và Frontend** cho hệ thống **Intern Management System (IMS)** — một nền tảng web quản lý vòng đời thực tập sinh trong doanh nghiệp (tuyển dụng → onboarding → đào tạo → giao việc → theo dõi KPI → đánh giá → báo cáo).

Cấu trúc chính:
- **IMS-BE/**: Backend viết bằng **Flask + SQLAlchemy + JWT**, kiến trúc đa module.  
- **IMS-FE/**: Frontend viết bằng **React 19 + TypeScript + Vite 6 + Tailwind**, UI tiếng Việt, dark/light theo system.

---

## 2. Nội dung 

### Backend (IMS-BE)
- **Framework**: Flask REST API.
- **Công nghệ chính**: Flask, SQLAlchemy ORM, JWT Auth, CORS, dotenv.
- **Tính năng**:
  - Quản lý **User** & **InternProfile** (thực tập sinh).
  - Quản lý **RecruitmentCampaign** & **Application** (tuyển dụng, apply).
  - Quản lý **TrainingProgram** & **Project**.
  - Quản lý **Assignment** với state machine `Pending → Doing → Done`.
  - Quản lý **Evaluation**, **ScheduleItem**, **KPIRecord**.
  - Hệ thống **Notification** & **Chat**.
  - RBAC với roles: `Admin`, `HR`, `Coordinator`, `Mentor`, `Intern`.
  - CLI: `flask --app src/app.py db` (tạo DB), `flask --app src/app.py seed` (tạo dữ liệu mẫu).
- **Điểm mạnh**: Cấu trúc module rõ ràng (`controllers/`, `models/`, `security/`, `utils/`), seed demo đầy đủ.

### Frontend (IMS-FE)
- **Framework**: React 19, Vite 6.
- **UI**: TailwindCSS, dark/light mode theo system.
- **Quản lý state**: Context API (`AuthContext`), zustand.
- **Router**: React Router v6.
- **Tính năng**:
  - Đăng nhập/Đăng ký (JWT).
  - Dashboard theo role: Admin, HR, Coordinator, Mentor, Intern.
  - Các trang quản lý entity: Users, InternProfiles, Campaigns, Applications, Programs, Projects, Assignments, Evaluations, Schedule, KPI, Notifications, Chat.
  - Giao tiếp API qua `apiClient` (tự gắn Bearer token, refresh khi 401).
- **Điểm mạnh**: Tách rõ `pages/`, `components/`, `api/`. UI thuần tiếng Việt, dễ dùng.

---

## 3. Hướng dẫn chạy chương trình

### Backend (IMS-BE)
```bash

cd IMS/IMS-BE

# 1. Tạo virtualenv
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# 2. Cài dependencies
pip install -r requirements.txt

# 3. Cấu hình biến môi trường (.env)
# Ví dụ:
# SECRET_KEY=your_secret
# JWT_SECRET_KEY=your_jwt_secret
# DATABASE_URL=sqlite:///ims.db
# PORT=5000
# INIT_DB=1

# 4. Khởi tạo DB & seed
flask --app src/app.py db
flask --app src/app.py seed

# 5. Chạy server
python -m src.app
# Mặc định http://localhost:5000
```
### Frontend (IMS-FE)
```bash

cd IMS/IMS-FE

# 1. Cài dependencies
npm install

# 2. Tạo file .env
# VITE_API_BASE=http://localhost:5000

# 3. Chạy dev server
npm run dev
# Mặc định http://localhost:5173
```
## 4. Cấu trúc thư mục
```bash
IMS/
├── IMS-BE/
│   ├── README.md
│   ├── requirements.txt
│   └── src/
│       ├── app.py
│       ├── create_app.py
│       ├── config.py
│       ├── infrastructure/
│       │   ├── databases.py
│       │   └── seeds.py
│       ├── security/
│       │   ├── auth.py
│       │   └── rbac.py
│       ├── utils/
│       │   ├── pagination.py
│       │   └── time.py
│       ├── domain/models/
│       │   ├── identity.py
│       │   ├── recruitment.py
│       │   ├── training.py
│       │   ├── assignment.py
│       │   ├── evaluation.py
│       │   ├── schedule.py
│       │   ├── kpi.py
│       │   └── messaging.py
│       └── api/controllers/
│           ├── auth_controller.py
│           ├── me_controller.py
│           ├── users_controller.py
│           ├── intern_profiles_controller.py
│           ├── campaigns_controller.py
│           ├── applications_controller.py
│           ├── programs_controller.py
│           ├── projects_controller.py
│           ├── assignments_controller.py
│           ├── evaluations_controller.py
│           ├── schedule_controller.py
│           ├── kpi_controller.py
│           ├── notifications_controller.py
│           ├── chat_controller.py
│           ├── admin_controller.py
│           └── root_controller.py
│
└── IMS-FE/
    ├── README.md
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    ├── tailwind.config.js
    ├── postcss.config.js
    └── src/
        ├── App.tsx
        ├── main.tsx
        ├── api/
        │   ├── auth.ts
        │   ├── users.ts
        │   ├── profiles.ts
        │   ├── campaigns.ts
        │   ├── applications.ts
        │   ├── programs.ts
        │   ├── projects.ts
        │   ├── assignments.ts
        │   ├── evaluations.ts
        │   ├── schedule.ts
        │   ├── kpi.ts
        │   ├── notifications.ts
        │   ├── chat.ts
        │   └── admin-settings.ts
        ├── contexts/
        │   └── AuthContext.tsx
        ├── lib/
        │   ├── apiClient.ts
        │   ├── auth.ts
        │   └── storage.ts
        ├── components/
        │   ├── Layout.tsx
        │   ├── DataTable.tsx
        │   ├── Form.tsx
        │   ├── StatCard.tsx
        │   └── ...
        └── pages/
            ├── Auth/
            │   ├── Login.tsx
            │   └── Register.tsx
            ├── Dashboard/
            │   ├── AdminDash.tsx
            │   ├── HRDash.tsx
            │   ├── CoordDash.tsx
            │   ├── MentorDash.tsx
            │   └── InternDash.tsx
            ├── Entities/
            │   ├── Users.tsx
            │   ├── InternProfiles.tsx
            │   ├── Campaigns.tsx
            │   ├── Applications.tsx
            │   ├── Programs.tsx
            │   ├── Projects.tsx
            │   ├── Assignments.tsx
            │   ├── Evaluations.tsx
            │   ├── Schedule.tsx
            │   ├── KPI.tsx
            │   ├── Notifications.tsx
            │   └── Chat.tsx
            └── AdminSettings.tsx



