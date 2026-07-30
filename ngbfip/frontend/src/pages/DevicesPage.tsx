import { useQuery } from '@tanstack/react-query'
import { devicesAPI } from '@/lib/api'
import Card from '@/components/Card'

function DevicesPage() {
  const { data: devices, isLoading } = useQuery({
    queryKey: ['devices'],
    queryFn: () => devicesAPI.list(),
  })

  if (isLoading) return <div className="loading">Loading devices...</div>

  return (
    <div className="devices-page">
      <h1>Devices</h1>
      <Card>
        <table>
          <thead>
            <tr>
              <th>Device ID</th>
              <th>Trust Score</th>
              <th>Status</th>
              <th>Last Seen</th>
            </tr>
          </thead>
          <tbody>
            {devices?.data?.map((device: any) => (
              <tr key={device.id}>
                <td>{device.device_id}</td>
                <td>{(device.trust_score * 100).toFixed(1)}%</td>
                <td>{device.is_trusted ? 'Trusted' : 'Untrusted'}</td>
                <td>{new Date(device.last_seen).toLocaleDateString()}</td>
              </tr>
            )) || []}
          </tbody>
        </table>
      </Card>
    </div>
  )
}

export default DevicesPage
