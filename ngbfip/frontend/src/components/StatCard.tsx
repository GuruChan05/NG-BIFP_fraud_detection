import { ReactNode } from 'react'
import './StatCard.css'

interface StatCardProps {
  icon: ReactNode
  label: string
  value: string | number
  change?: string
  color?: 'primary' | 'success' | 'warning' | 'danger'
}

function StatCard({
  icon,
  label,
  value,
  change,
  color = 'primary',
}: StatCardProps) {
  return (
    <div className={`stat-card stat-card-${color}`}>
      <div className="stat-icon">{icon}</div>
      <div className="stat-content">
        <p className="stat-label">{label}</p>
        <h3 className="stat-value">{value}</h3>
        {change && <p className="stat-change">{change}</p>}
      </div>
    </div>
  )
}

export default StatCard
