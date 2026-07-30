import { ReactNode } from 'react'
import Sidebar from './Sidebar'
import Header from './Header'
import './Layout.css'

interface LayoutProps {
  children: ReactNode
}

function Layout({ children }: LayoutProps) {
  return (
    <div className="layout">
      <Sidebar />
      <div className="layout-content">
        <Header />
        <main className="layout-main">{children}</main>
      </div>
    </div>
  )
}

export default Layout
