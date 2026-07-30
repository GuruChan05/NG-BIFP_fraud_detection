import { useState, useEffect } from 'react'
import { Search, FileDown, Filter, ChevronLeft, ChevronRight } from 'lucide-react'
import { transactionAPI } from '@/lib/api'
import '../styles/TransactionsPage.css'

interface Transaction {
  id: number
  user_id: number
  amount: number
  transaction_type: string
  merchant: string
  risk_score: number
  is_fraudulent: string
  created_at: string
}

function TransactionsPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [totalTransactions, setTotalTransactions] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [filters, setFilters] = useState({
    is_fraudulent: '',
    min_amount: '',
    max_amount: '',
  })
  const pageSize = 20

  useEffect(() => {
    const loadTransactions = async () => {
      try {
        setIsLoading(true)
        const response = await transactionAPI.list(
          currentPage,
          pageSize,
          {
            merchant: searchQuery || undefined,
            is_fraudulent: filters.is_fraudulent || undefined,
            min_amount: filters.min_amount ? parseFloat(filters.min_amount) : undefined,
            max_amount: filters.max_amount ? parseFloat(filters.max_amount) : undefined,
          }
        )
        setTransactions(response.data.data)
        setTotalTransactions(response.data.total)
      } catch (err) {
        setError('Failed to load transactions')
      } finally {
        setIsLoading(false)
      }
    }

    loadTransactions()
  }, [currentPage, searchQuery, filters])

  const handleExport = async () => {
    try {
      const response = await transactionAPI.exportCSV()
      const csv = response.data.csv
      const blob = new Blob([csv], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `transactions-${new Date().toISOString()}.csv`
      a.click()
    } catch (err) {
      setError('Failed to export transactions')
    }
  }

  const getRiskColor = (riskScore: number) => {
    if (riskScore < 30) return '#4caf50'
    if (riskScore < 70) return '#ffc107'
    return '#ff6b6b'
  }

  const totalPages = Math.ceil(totalTransactions / pageSize)

  return (
    <div className="transactions-page">
      {error && <div className="error-alert">{error}</div>}

      <div className="transactions-header">
        <h1>Transactions</h1>
        <button className="export-btn" onClick={handleExport}>
          <FileDown size={18} />
          Export CSV
        </button>
      </div>

      {/* Search and Filters */}
      <div className="filters-section">
        <div className="search-box">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search by merchant..."
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value)
              setCurrentPage(1)
            }}
          />
        </div>

        <div className="filter-controls">
          <select
            value={filters.is_fraudulent}
            onChange={(e) => {
              setFilters({ ...filters, is_fraudulent: e.target.value })
              setCurrentPage(1)
            }}
          >
            <option value="">All Status</option>
            <option value="Yes">Fraudulent</option>
            <option value="No">Legitimate</option>
          </select>

          <input
            type="number"
            placeholder="Min Amount"
            value={filters.min_amount}
            onChange={(e) => {
              setFilters({ ...filters, min_amount: e.target.value })
              setCurrentPage(1)
            }}
          />

          <input
            type="number"
            placeholder="Max Amount"
            value={filters.max_amount}
            onChange={(e) => {
              setFilters({ ...filters, max_amount: e.target.value })
              setCurrentPage(1)
            }}
          />
        </div>
      </div>

      {/* Transactions Table */}
      <div className="transactions-table-container">
        {isLoading ? (
          <div className="loading">Loading transactions...</div>
        ) : (
          <>
            <table className="transactions-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Merchant</th>
                  <th>Type</th>
                  <th>Amount</th>
                  <th>Risk Score</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((tx) => (
                  <tr key={tx.id}>
                    <td>#{tx.id}</td>
                    <td>{tx.merchant}</td>
                    <td>{tx.transaction_type}</td>
                    <td>${tx.amount.toFixed(2)}</td>
                    <td>
                      <span
                        className="risk-badge"
                        style={{ backgroundColor: getRiskColor(tx.risk_score) + '20', color: getRiskColor(tx.risk_score) }}
                      >
                        {tx.risk_score.toFixed(1)}
                      </span>
                    </td>
                    <td>
                      <span className={`status-badge ${tx.is_fraudulent === 'Yes' ? 'fraudulent' : 'legitimate'}`}>
                        {tx.is_fraudulent === 'Yes' ? '⚠️ Fraud' : '✓ Legitimate'}
                      </span>
                    </td>
                    <td>{new Date(tx.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Pagination */}
            <div className="pagination">
              <button
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
              >
                <ChevronLeft size={18} />
              </button>
              <span>
                Page {currentPage} of {totalPages}
              </span>
              <button
                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                disabled={currentPage === totalPages}
              >
                <ChevronRight size={18} />
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default TransactionsPage
