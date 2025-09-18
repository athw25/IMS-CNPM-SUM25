import AdminDash from '../pages/Dashboard/AdminDash'
import HRDash from '../pages/Dashboard/HRDash'
import CoordDash from '../pages/Dashboard/CoordDash'
import MentorDash from '../pages/Dashboard/MentorDash'
import InternDash from '../pages/Dashboard/InternDash'
import UsersPage from '../pages/Entities/UsersPage'
import InternProfilesPage from '../pages/Entities/InternProfilesPage'
import CampaignsPage from '../pages/Entities/CampaignsPage'
import ApplicationsPage from '../pages/Entities/ApplicationsPage'
import ProgramsPage from '../pages/Entities/ProgramsPage'
import ProjectsPage from '../pages/Entities/ProjectsPage'
import AssignmentsPage from '../pages/Entities/AssignmentsPage'
import EvaluationsPage from '../pages/Entities/EvaluationsPage'
import SchedulePage from '../pages/Entities/SchedulePage'
import KPIPage from '../pages/Entities/KPIPage'
import NotificationsPage from '../pages/Entities/NotificationsPage'
import ChatPage from '../pages/Entities/ChatPage'
import HealthPage from '../pages/Dashboard/HealthPage'
import AdminSettings from '../pages/Dashboard/AdminSettings'
import type { Role } from '../lib/auth'

import { lazy } from "react";
import { Navigate } from "react-router-dom";


type Route = { path: string; element: any; protected?: boolean; roles?: Role[] }

export const routes: Route[] = [

  { path: "/", element: <Navigate to="/login" replace /> },
  { path: "/login", element: lazy(() => import("../pages/Auth/Login")) },
  { path: "/register", element: lazy(() => import("../pages/Auth/Register")) },

  // Dashboards
  { path: '/dashboard/admin', element: AdminDash, protected: true, roles: ['Admin'] },
  { path: '/dashboard/admin/health', element: HealthPage, protected: true, roles: ["Admin"] },
  { path: "/dashboard/admin/settings", element: AdminSettings,  protected: true, roles: ["Admin"], },

  { path: '/dashboard/hr', element: HRDash, protected: true, roles: ['HR'] },
  { path: '/dashboard/coord', element: CoordDash, protected: true, roles: ['Coordinator'] },
  { path: '/dashboard/mentor', element: MentorDash, protected: true, roles: ['Mentor'] },
  { path: '/dashboard/intern', element: InternDash, protected: true, roles: ['Intern'] },

  // Entities
  { path: '/entities/users', element: UsersPage, protected: true, roles: ['Admin','HR'] },
  { path: '/entities/profiles', element: InternProfilesPage, protected: true, roles: ['HR','Coordinator'] },
  { path: '/entities/campaigns', element: CampaignsPage, protected: true },
  { path: '/entities/applications', element: ApplicationsPage, protected: true },
  { path: '/entities/programs', element: ProgramsPage, protected: true },
  { path: '/entities/projects', element: ProjectsPage, protected: true },
  { path: '/entities/assignments', element: AssignmentsPage, protected: true },
  { path: '/entities/evaluations', element: EvaluationsPage, protected: true },
  { path: '/entities/schedule', element: SchedulePage, protected: true },
  { path: '/entities/kpi', element: KPIPage, protected: true },
  { path: '/entities/notifications', element: NotificationsPage, protected: true },
  { path: '/entities/chat', element: ChatPage, protected: true },
  { path: '/entities/admin', element: HealthPage, protected: true, roles: ['Admin'] }

]

