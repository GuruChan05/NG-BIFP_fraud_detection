import { useQuery } from '@tanstack/react-query'
import { dashboardAPI } from '@/lib/api'
import Card from '@/components/Card'

function AnalyticsPage() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['analytics', 'statistics'],
    queryFn: () => dashboardAPI.getStatistics(),
  })

  if (isLoading) return <div className="loading">Loading analytics...</div>

  return (
    <div className="analytics-page">
      <h1>Analytics</h1>
      <Card title="System Statistics">
        <div className="stats-container">
          <div className="stat-item">
            <h3>Total Transactions</h3>
            <p>{stats?.data?.total_transactions || 0}</p>
          </div>
          <div className="stat-item">
            <h3>Fraud Cases Detected</h3>
            <p>{stats?.data?.fraud_cases_detected || 0}</p>
          </div>
          <div className="stat-item">
            <h3>Average Risk Score</h3>
            <p>{(stats?.data?.average_risk_score || 0).toFixed(2)}</p>
          </div>
          <div className="stat-item">
            <h3>System Uptime</h3>
            <p>99.9%</p>
          </div>
        </div>
      </Card>
    </div>
  )
}

export default AnalyticsPage
