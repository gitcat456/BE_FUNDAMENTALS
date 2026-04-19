import { Route, Routes } from 'react-router-dom'
import { AuthProvider } from './auth/AuthContext'
import { Protected } from './routes/Protected'
import { RoleParamGuard } from './routes/RoleParamGuard'
import { WorkspaceShell } from './components/WorkspaceShell'
import { LoginPage } from './pages/LoginPage'
import { RootRedirect } from './pages/RootRedirect'
import { DashboardHome } from './pages/workspace/DashboardHome'
import { BooksManagePage } from './pages/workspace/BooksManagePage'
import { BrowsePage } from './pages/workspace/BrowsePage'
import { LoansPage } from './pages/workspace/LoansPage'

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<Protected />}>
          <Route
            path="/workspace/:role"
            element={
              <RoleParamGuard>
                <WorkspaceShell />
              </RoleParamGuard>
            }
          >
            <Route index element={<DashboardHome />} />
            <Route path="books" element={<BooksManagePage />} />
            <Route path="browse" element={<BrowsePage />} />
            <Route path="loans" element={<LoansPage />} />
          </Route>
        </Route>
        <Route path="/" element={<RootRedirect />} />
      </Routes>
    </AuthProvider>
  )
}
