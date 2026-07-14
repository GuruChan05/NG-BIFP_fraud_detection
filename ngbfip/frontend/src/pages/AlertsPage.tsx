import { useQuery } from '@tanstack/react-query'
import { alertsAPI } from '@/lib/api'
import Card from '@/components/Card'

function AlertsPage() {
  const { data: alerts, isLoading } = useQuery({
    queryKey: ['alerts'],
    queryFn: () => alertsAPI.list(),
  })

  if (isLoading) return <div className="loading">Loading alerts...</div>

  return (
    <div className="alerts-page">
      <h1>Security Alerts</h1>
      <Card>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Type</th>
              <th>Message</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {alerts?.data?.map((alert: any) => (
              <tr key={alert.id}>
                <td>{alert.id}</td>
                <td>{alert.alert_type}</td>
                <td>{alert.message}</td>
                <td>{alert.is_resolved ? 'Resolved' : 'Active'}</td>
                <td>{new Date(alert.created_at).toLocaleDateString()}</td>
              </tr>
            )) || []}
          </tbody>
        </table>
      </Card>
    </div>
  )
}

export default AlertsPage
