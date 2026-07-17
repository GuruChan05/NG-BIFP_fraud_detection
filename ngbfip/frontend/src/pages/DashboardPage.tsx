import { useState, useEffect } from 'react'
import { AlertCircle, TrendingUp, Users, Activity, Zap } from 'lucide-react'
import { dashboardAPI } from '@/lib/api'
import StatCard from '@/components/StatCard'
import '../styles/DashboardPage.css'

function DashboardPage() {
  const [overview, setOverview] = useState<any>(null)
  const [recentTransactions, setRecentTransactions] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [lastRefresh, setLastRefresh] = useState<Date | null>(null)

  const loadDashboard = async () => {
    try {
      setIsLoading(true)
      const [overviewData, recentData] = await Promise.all([
        dashboardAPI.getOverview(),
        dashboardAPI.getRecentTransactions(10),
      ])
      setOverview(overviewData.data)
      setRecentTransactions(recentData.data)
      setLastRefresh(new Date())
    } catch (err) {
      setError('Failed to load dashboard')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadDashboard()
    const interval = setInterval(loadDashboard, 30000) // Auto-refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const getRiskColor = (riskScore: number) => {
    if (riskScore < 30) return '#4caf50'
    if (riskScore < 70) return '#ffc107'
    return '#ff6b6b'
  }

  if (isLoading) return <div className="dashboard-page"><div className="loading">Loading dashboard...</div></div>

  return (
    <div className="dashboard-page">
      {error && <div className="error-alert">{error}</div>}

      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <div className="refresh-info">
          <button onClick={loadDashboard} className="refresh-btn">
            <Zap size={16} />
            Refresh
          </button>
          {lastRefresh && (
            <span className="last-refresh">
              Last updated: {lastRefresh.toLocaleTimeString()}
            </span>
          )}
        </div>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <StatCard
          title="Total Transactions"
          value={overview?.total_transactions || 0}
          icon={<Activity size={24} />}
          color="#00d4ff"
        />
        <StatCard
          title="Fraud Cases"
          value={overview?.fraud_cases || 0}
          subtitle={`${overview?.fraud_percentage || 0}% rate`}
          icon={<AlertCircle size={24} />}
          color="#ff6b6b"
        />
        <StatCard
          title="Active Users"
          value={overview?.active_users || 0}
          icon={<Users size={24} />}
          color="#4caf50"
        />
        <StatCard
          title="Avg Risk Score"
          value={overview?.average_risk_score?.toFixed(1) || 0}
          icon={<TrendingUp size={24} />}
          color="#ffc107"
        />
        <StatCard
          title="High-Risk Transactions"
          value={overview?.high_risk_transactions || 0}
          icon={<AlertCircle size={24} />}
          color="#ff9800"
        />
        <StatCard
          title="Today's Activity"
          value={overview?.todays_activity || 0}
          icon={<Activity size={24} />}
          color="#9c27b0"
        />
      </div>

      {/* Recent Transactions */}
      <div className="recent-transactions">
        <h2>Recent Transactions</h2>
        <div className="transactions-list">
          {recentTransactions.length === 0 ? (
            <div className="no-data">No recent transactions</div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Merchant</th>
                  <th>Amount</th>
                  <th>Type</th>
                  <th>Risk Score</th>
                  <th>Status</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                {recentTransactions.map((tx: any) => (
                  <tr key={tx.id}>
                    <td>{tx.merchant}</td>
                    <td>${tx.amount.toFixed(2)}</td>
                    <td>{tx.transaction_type}</td>
                    <td>
                      <span
                        className="risk-score"
                        style={{ color: getRiskColor(tx.risk_score) }}
                      >
                        {tx.risk_score.toFixed(1)}
                      </span>
                    </td>
                    <td>
                      <span className={`status-badge ${tx.is_fraudulent === 'Yes' ? 'fraud' : 'legitimate'}`}>
                        {tx.is_fraudulent === 'Yes' ? '⚠️ Fraud' : '✓ Legitimate'}
                      </span>
                    </td>
                    <td>{new Date(tx.created_at).toLocaleTimeString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}

export default DashboardPage
