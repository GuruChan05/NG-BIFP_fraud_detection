import { useQuery } from '@tanstack/react-query'
import { transactionsAPI } from '@/lib/api'
import Card from '@/components/Card'
import './TransactionsPage.css'

function TransactionsPage() {
  const { data: transactions, isLoading } = useQuery({
    queryKey: ['transactions'],
    queryFn: () => transactionsAPI.list(),
  })

  if (isLoading) return <div className="loading">Loading transactions...</div>

  return (
    <div className="transactions-page">
      <h1>Transactions</h1>
      <Card>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Amount</th>
              <th>Type</th>
              <th>Merchant</th>
              <th>Risk Level</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {transactions?.data?.map((txn: any) => (
              <tr key={txn.id}>
                <td>{txn.id}</td>
                <td>${txn.amount}</td>
                <td>{txn.transaction_type}</td>
                <td>{txn.merchant}</td>
                <td>
                  <span className={`risk-badge risk-${txn.risk_level}`}>
                    {txn.risk_level}
                  </span>
                </td>
                <td>{new Date(txn.created_at).toLocaleDateString()}</td>
              </tr>
            )) || []}
          </tbody>
        </table>
      </Card>
    </div>
  )
}

export default TransactionsPage
