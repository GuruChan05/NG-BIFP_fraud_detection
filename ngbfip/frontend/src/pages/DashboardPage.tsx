import { useDashboardOverview, useRecentActivity } from '@/hooks/useDashboard'
import {
  AlertCircle,
  TrendingUp,
  Activity,
  Shield,
  AlertTriangle,
  Users,
  Clock,
  CheckCircle,
} from 'lucide-react'
import Card from '@/components/Card'
import StatCard from '@/components/StatCard'
import './DashboardPage.css'

function DashboardPage() {
  const { data: overview, isLoading: overviewLoading, error: overviewError } =
    useDashboardOverview()
  const { data: recentActivity, isLoading: activityLoading, error: activityError } =
    useRecentActivity(5)

  if (overviewLoading) {
    return (
      <div className="dashboard-page">
        <h1>Dashboard</h1>
        <div className="loading-skeleton">
          <div className="skeleton-bar" />
          <div className="skeleton-bar" />
        </div>
      </div>
    )
  }

  if (overviewError || !overview) {
    return (
      <div className="dashboard-page">
        <h1>Dashboard</h1>
        <div className="error-state">
          <AlertCircle size={48} />
          <h2>Error Loading Dashboard</h2>
          <p>Unable to fetch dashboard data. Please try again later.</p>
        </div>
      </div>
    )
  }

  const stats = [
    {
      icon: <Activity size={24} />,
      label: 'Total Transactions',
      value: overview.total_transactions.toLocaleString(),
      color: 'primary' as const,
    },
    {
      icon: <AlertTriangle size={24} />,
      label: 'Fraud Cases',
      value: overview.fraud_cases.toLocaleString(),
      color: 'danger' as const,
    },
    {
      icon: <Users size={24} />,
      label: 'Active Users',
      value: overview.active_users.toLocaleString(),
      color: 'success' as const,
    },
    {
      icon: <Clock size={24} />,
      label: "Today's Activity",
      value: overview.todays_activity.toLocaleString(),
      color: 'warning' as const,
    },
    {
      icon: <TrendingUp size={24} />,
      label: 'Average Risk Score',
      value: `${(overview.average_risk_score * 100).toFixed(1)}%`,
      color: 'warning' as const,
    },
    {
      icon: <Shield size={24} />,
      label: 'Trusted Devices',
      value: overview.trusted_devices.toLocaleString(),
      color: 'success' as const,
    },
    {
      icon: <AlertCircle size={24} />,
      label: 'High-Risk Transactions',
      value: overview.high_risk_transactions.toLocaleString(),
      color: 'danger' as const,
    },
    {
      icon: <CheckCircle size={24} />,
      label: 'Resolved Alerts',
      value: overview.resolved_alerts.toLocaleString(),
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
        <Card title="Recent Transactions" className="recent-activity">
          {activityLoading ? (
            <div className="loading">Loading recent activity...</div>
          ) : activityError ? (
            <div className="error">Error loading recent activity</div>
          ) : recentActivity && recentActivity.length > 0 ? (
            <div className="activity-list">
              <table className="activity-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Amount</th>
                    <th>Merchant</th>
                    <th>Type</th>
                    <th>Risk Score</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {recentActivity.map((activity) => (
                    <tr key={activity.id}>
                      <td>#{activity.id}</td>
                      <td>${activity.amount.toFixed(2)}</td>
                      <td>{activity.merchant}</td>
                      <td>{activity.transaction_type}</td>
                      <td>
                        <span className={`risk-badge risk-${getRiskLevel(activity.risk_score)}`}>
                          {(activity.risk_score * 100).toFixed(1)}%
                        </span>
                      </td>
                      <td>
                        <span
                          className={`status-badge status-${activity.is_fraudulent}`}
                        >
                          {activity.is_fraudulent}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="empty-state">No recent transactions</div>
          )}
        </Card>
      </div>
    </div>
  )
}

function getRiskLevel(score: number): string {
  if (score < 0.3) return 'low'
  if (score < 0.6) return 'medium'
  if (score < 0.8) return 'high'
  return 'critical'
}

export default DashboardPage
