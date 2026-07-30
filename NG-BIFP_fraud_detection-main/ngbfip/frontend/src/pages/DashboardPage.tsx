import { useState, useEffect } from 'react'
import { AlertCircle, TrendingUp, Users, Activity, Zap } from 'lucide-react'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'
import { dashboardAPI } from '@/lib/api'
import StatCard from '@/components/StatCard'
import '../styles/DashboardPage.css'

const COLORS = ['#00d4ff', '#ff6b6b', '#4caf50', '#ffc107', '#9c27b0']

function DashboardPage() {
  const [overview, setOverview] = useState<any>(null)
  const [recentTransactions, setRecentTransactions] = useState<any[]>([])
  const [riskDistribution, setRiskDistribution] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [lastRefresh, setLastRefresh] = useState<Date | null>(null)

  const loadDashboard = async () => {
    try {
      setIsLoading(true)
      const [overviewData, recentData, riskData] = await Promise.all([
        dashboardAPI.getOverview(),
        dashboardAPI.getRecentTransactions(10),
        dashboardAPI.getRiskDistribution(),
      ])
      setOverview(overviewData.data)
      setRecentTransactions(recentData.data)
      setRiskDistribution(riskData.data)
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
    if (riskScore < 0.30) return '#4caf50'
    if (riskScore < 0.70) return '#ffc107'
    return '#ff6b6b'
  }

  if (isLoading) return <div className="dashboard-page"><div className="loading">Loading dashboard...</div></div>

  const riskData = [
    { name: 'Very Low', value: riskDistribution?.very_low || 0, color: COLORS[2] },
    { name: 'Low', value: riskDistribution?.low || 0, color: COLORS[3] },
    { name: 'Medium', value: riskDistribution?.medium || 0, color: COLORS[0] },
    { name: 'High', value: riskDistribution?.high || 0, color: COLORS[1] },
    { name: 'Very High', value: riskDistribution?.very_high || 0, color: '#ff0000' },
  ]

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
          label="Total Transactions"
          value={overview?.total_transactions || 0}
          icon={<Activity size={24} />}
          color="primary"
        />
        <StatCard
          label="Fraud Cases"
          value={overview?.fraud_cases || 0}
          change={`${overview?.fraud_percentage || 0}% rate`}
          icon={<AlertCircle size={24} />}
          color="danger"
        />
        <StatCard
          label="Active Users"
          value={overview?.active_users || 0}
          icon={<Users size={24} />}
          color="success"
        />
        <StatCard
          label="Avg Risk Score"
          value={overview?.average_risk_score?.toFixed(1) || 0}
          icon={<TrendingUp size={24} />}
          color="warning"
        />
        <StatCard
          label="High-Risk Transactions"
          value={overview?.high_risk_transactions || 0}
          icon={<AlertCircle size={24} />}
          color="warning"
        />
        <StatCard
          label="Today's Activity"
          value={overview?.todays_activity || 0}
          icon={<Activity size={24} />}
          color="primary"
        />
      </div>

      {/* Risk Distribution Chart */}
      <div className="risk-distribution-section" style={{ marginTop: '24px', backgroundColor: 'var(--bg-secondary)', padding: '20px', borderRadius: '12px' }}>
        <h2>Risk Score Distribution</h2>
        <div style={{ height: '300px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={riskData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {riskData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
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
                      <span className={`status-badge ${tx.is_fraudulent === 'fraudulent' ? 'fraud' : 'legitimate'}`}>
                        {tx.is_fraudulent === 'fraudulent' ? '⚠️ Fraud' : '✓ Legitimate'}
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
