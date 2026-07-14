import { Link, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  TrendingUp,
  AlertCircle,
  Smartphone,
  BarChart3,
  LogOut,
} from 'lucide-react'
import { useAuthStore } from '@/stores/auth.store'
import './Sidebar.css'

function Sidebar() {
  const location = useLocation()
  const logout = useAuthStore((state) => state.logout)

  const isActive = (path: string) => location.pathname === path

  const menuItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
    { icon: TrendingUp, label: 'Transactions', path: '/transactions' },
    { icon: AlertCircle, label: 'Alerts', path: '/alerts' },
    { icon: Smartphone, label: 'Devices', path: '/devices' },
    { icon: BarChart3, label: 'Analytics', path: '/analytics' },
  ]

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1 className="sidebar-title">NG-BIFP</h1>
        <p className="sidebar-subtitle">Fraud Detection</p>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const Icon = item.icon
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${isActive(item.path) ? 'active' : ''}`}
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>

      <div className="sidebar-footer">
        <button
          onClick={logout}
          className="logout-btn"
          title="Logout"
        >
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  )
}

export default Sidebar
