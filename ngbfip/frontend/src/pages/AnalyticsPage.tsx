import { useState, useEffect } from 'react'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'
import { TrendingUp, TrendingDown, AlertCircle, Activity } from 'lucide-react'
import { dashboardAPI } from '@/lib/api'
import '../styles/AnalyticsPage.css'

const COLORS = ['#00d4ff', '#ff6b6b', '#4caf50', '#ffc107', '#9c27b0']

function AnalyticsPage() {
  const [dailyData, setDailyData] = useState<any[]>([])
  const [fraudTrends, setFraudTrends] = useState<any[]>([])
  const [riskDistribution, setRiskDistribution] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [dateRange, setDateRange] = useState(30)

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        setIsLoading(true)
        const [daily, fraud, risk] = await Promise.all([
          dashboardAPI.getDailySummary(7),
          dashboardAPI.getFraudTrends(dateRange),
          dashboardAPI.getRiskDistribution(),
        ])
        
        setDailyData(daily.data || [])
        setFraudTrends(fraud.data || [])
        setRiskDistribution(risk.data || {})
      } catch (err) {
        setError('Failed to load analytics')
      } finally {
        setIsLoading(false)
      }
    }

    loadAnalytics()
  }, [dateRange])

  if (isLoading) return <div className="analytics-page"><div className="loading">Loading analytics...</div></div>

  const riskData = [
    { name: 'Very Low', value: riskDistribution?.very_low || 0, color: COLORS[2] },
    { name: 'Low', value: riskDistribution?.low || 0, color: COLORS[3] },
    { name: 'Medium', value: riskDistribution?.medium || 0, color: COLORS[0] },
    { name: 'High', value: riskDistribution?.high || 0, color: COLORS[1] },
    { name: 'Very High', value: riskDistribution?.very_high || 0, color: '#ff0000' },
  ]

  return (
    <div className="analytics-page">
      {error && <div className="error-alert">{error}</div>}

      <div className="analytics-header">
        <h1>Analytics & Insights</h1>
        <div className="date-range-selector">
          <select value={dateRange} onChange={(e) => setDateRange(parseInt(e.target.value))}>
            <option value={7}>Last 7 Days</option>
            <option value={30}>Last 30 Days</option>
            <option value={90}>Last 90 Days</option>
            <option value={365}>Last Year</option>
          </select>
        </div>
      </div>

      {/* Daily Transaction Summary */}
      <div className="analytics-card">
        <h2>Daily Transaction Summary</h2>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={dailyData}>
            <defs>
              <linearGradient id="colorTransactions" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#00d4ff" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#00d4ff" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="date" stroke="rgba(255,255,255,0.5)" />
            <YAxis stroke="rgba(255,255,255,0.5)" />
            <Tooltip contentStyle={{ background: 'rgba(0,0,0,0.8)', border: 'none', borderRadius: '8px' }} />
            <Area type="monotone" dataKey="transactions" stroke="#00d4ff" fillOpacity={1} fill="url(#colorTransactions)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="analytics-grid">
        {/* Fraud Trends */}
        <div className="analytics-card">
          <h2>Fraud Trends</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={fraudTrends}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="date" stroke="rgba(255,255,255,0.5)" />
              <YAxis stroke="rgba(255,255,255,0.5)" />
              <Tooltip contentStyle={{ background: 'rgba(0,0,0,0.8)', border: 'none', borderRadius: '8px' }} />
              <Legend />
              <Line type="monotone" dataKey="fraud_rate" stroke="#ff6b6b" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Risk Distribution */}
        <div className="analytics-card">
          <h2>Risk Score Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
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
                {riskData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Fraud Rate Comparison */}
      <div className="analytics-card">
        <h2>Fraud Detection Rate</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={fraudTrends.slice(-7)}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="date" stroke="rgba(255,255,255,0.5)" />
            <YAxis stroke="rgba(255,255,255,0.5)" />
            <Tooltip contentStyle={{ background: 'rgba(0,0,0,0.8)', border: 'none', borderRadius: '8px' }} />
            <Legend />
            <Bar dataKey="fraud_count" fill="#ff6b6b" name="Fraud Cases" />
            <Bar dataKey="total_count" fill="#00d4ff" name="Total Transactions" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default AnalyticsPage
