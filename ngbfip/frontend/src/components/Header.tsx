import { useAuthStore } from '@/stores/auth.store'
import { Bell, User } from 'lucide-react'
import './Header.css'

function Header() {
  const user = useAuthStore((state) => state.user)

  return (
    <header className="header">
      <div className="header-left">
        <h2>Welcome back, {user?.name || 'User'}!</h2>
      </div>
      <div className="header-right">
        <button className="icon-btn" title="Notifications">
          <Bell size={20} />
        </button>
        <button className="icon-btn" title="Profile">
          <User size={20} />
        </button>
      </div>
    </header>
  )
}

export default Header
