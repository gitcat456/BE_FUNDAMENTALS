import { Route, Routes } from 'react-router-dom'
import { AuthProvider } from './auth/AuthContext'
import { GoogleAuthProvider } from './components/auth/GoogleAuthProvider'
import { Protected } from './routes/Protected'
import { RoleParamGuard } from './routes/RoleParamGuard'
import { WorkspaceShell } from './components/WorkspaceShell'
import { SnackbarProvider } from './components/snackbar/SnackbarProvider'
import { LoginPage } from './pages/LoginPage'
import { SignupPage } from './pages/SignupPage'
import { ForgotPasswordPage } from './pages/ForgotPasswordPage'
import { ResetPasswordPage } from './pages/ResetPasswordPage'
import { RootRedirect } from './pages/RootRedirect'
import { DashboardHome } from './pages/workspace/DashboardHome'
import { BooksManagePage } from './pages/workspace/BooksManagePage'
import { BrowsePage } from './pages/workspace/BrowsePage'
import { LoansPage } from './pages/workspace/LoansPage'
import { ProfilePage } from './pages/workspace/ProfilePage'
import { PaymentsPage } from './pages/workspace/PaymentsPage'
import { PaymentCallbackPage } from './pages/PaymentCallbackPage'
import { NotFoundPage } from './pages/NotFoundPage'

export default function App() {
  return (
    <SnackbarProvider>
      <GoogleAuthProvider>
        <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />
        <Route element={<Protected />}>
          <Route path="/payment/callback" element={<PaymentCallbackPage />} />
          <Route path="/workspace/:role" element={<RoleParamGuard />}>
            <Route element={<WorkspaceShell />}>
              <Route index element={<DashboardHome />} />
              <Route path="books" element={<BooksManagePage />} />
              <Route path="browse" element={<BrowsePage />} />
              <Route path="loans" element={<LoansPage />} />
              <Route path="payments" element={<PaymentsPage />} />
              <Route path="profile" element={<ProfilePage />} />
            </Route>
          </Route>
        </Route>
        <Route path="/" element={<RootRedirect />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
        </AuthProvider>
      </GoogleAuthProvider>
    </SnackbarProvider>
  )
}
