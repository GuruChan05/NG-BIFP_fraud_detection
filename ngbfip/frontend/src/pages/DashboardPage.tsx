import { useQuery } from '@tanstack/react-query'
import { AlertCircle, TrendingUp, Activity, Shield } from 'lucide-react'
import { dashboardAPI } from '@/lib/api'
import Card from '@/components/Card'
import StatCard from '@/components/StatCard'
import './DashboardPage.css'

function DashboardPage() {
  const { data: overview, isLoading } = useQuery({
    queryKey: ['dashboard', 'overview'],
    queryFn: () => dashboardAPI.getOverview(),
  })

  if (isLoading) return <div className="loading">Loading...</div>

  const stats = [
    {
      icon: <Activity size={24} />,
      label: 'Total Transactions',
      value: overview?.data?.total_transactions || 0,
      color: 'primary' as const,
    },
    {
      icon: <AlertCircle size={24} />,
      label: 'Active Alerts',
      value: overview?.data?.active_alerts || 0,
      color: 'danger' as const,
    },
    {
      icon: <TrendingUp size={24} />,
      label: 'Risk Score',
      value: `${overview?.data?.average_risk_score || 0}%`,
      color: 'warning' as const,
    },
    {
      icon: <Shield size={24} />,
      label: 'Trusted Devices',
      value: overview?.data?.trusted_devices || 0,
      color: 'success' as const,
    },
  ]

  return (
    <div className="dashboard-page">
      <h1>Dashboard</h1>

      <div className="stats-grid">
        {stats.map((stat, index) => (
          <StatCard key={index} {...stat} />
        ))}
      </div>

      <div className="charts-grid">
        <Card title="Recent Transactions">
          <p>Transaction history will be displayed here</p>
        </Card>
        <Card title="Risk Trends">
          <p>Risk trends chart will be displayed here</p>
        </Card>
      </div>
    </div>
  )
}

export default DashboardPage
