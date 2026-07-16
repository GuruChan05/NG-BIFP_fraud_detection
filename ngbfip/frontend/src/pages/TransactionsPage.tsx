import { useState } from 'react'
import { useTransactions } from '@/hooks/useTransactions'
import { Search, Download, Upload, ChevronLeft, ChevronRight } from 'lucide-react'
import Card from '@/components/Card'
import './TransactionsPage.css'

function TransactionsPage() {
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)
  const [filters, setFilters] = useState<any>({})
  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState('created_at')
  const [sortOrder, setSortOrder] = useState('desc')

  const { data: transactions, isLoading, error } = useTransactions(page, pageSize, {
    ...filters,
    sort_by: sortBy,
    sort_order: sortOrder,
  })

  const handleFilterChange = (key: string, value: any) => {
    setFilters((prev: any) => ({ ...prev, [key]: value }))
    setPage(1)
  }

  const handleSearch = (term: string) => {
    setSearchTerm(term)
    if (term) {
      handleFilterChange('search', term)
    } else {
      const newFilters = { ...filters }
      delete newFilters.search
      setFilters(newFilters)
    }
  }

  const handleSort = (field: string) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(field)
      setSortOrder('asc')
    }
  }

  if (error) {
    return (
      <div className="transactions-page">
        <h1>Transactions</h1>
        <div className="error-state">
          <p>Error loading transactions</p>
        </div>
      </div>
    )
  }

  return (
    <div className="transactions-page">
      <div className="page-header">
        <h1>Transactions</h1>
        <div className="header-actions">
          <button className="btn btn-secondary">
            <Upload size={18} /> Import CSV
          </button>
          <button className="btn btn-secondary">
            <Download size={18} /> Export CSV
          </button>
        </div>
      </div>

      <Card title="Transaction Filters" className="filters-card">
        <div className="filters-grid">
          <div className="filter-input">
            <label>Search</label>
            <div className="search-box">
              <Search size={18} />
              <input
                type="text"
                placeholder="Search merchant, location, device..."
                value={searchTerm}
                onChange={(e) => handleSearch(e.target.value)}
              />
            </div>
          </div>

          <div className="filter-input">
            <label>Fraud Status</label>
            <select
              value={filters.fraud_status || ''}
              onChange={(e) => handleFilterChange('fraud_status', e.target.value || undefined)}
            >
              <option value="">All</option>
              <option value="legitimate">Legitimate</option>
              <option value="fraudulent">Fraudulent</option>
              <option value="unknown">Unknown</option>
            </select>
          </div>

          <div className="filter-input">
            <label>Min Amount</label>
            <input
              type="number"
              placeholder="Min"
              value={filters.min_amount || ''}
              onChange={(e) =>
                handleFilterChange('min_amount', e.target.value ? parseFloat(e.target.value) : undefined)
              }
            />
          </div>

          <div className="filter-input">
            <label>Max Amount</label>
            <input
              type="number"
              placeholder="Max"
              value={filters.max_amount || ''}
              onChange={(e) =>
                handleFilterChange('max_amount', e.target.value ? parseFloat(e.target.value) : undefined)
              }
            />
          </div>

          <div className="filter-input">
            <label>Merchant</label>
            <input
              type="text"
              placeholder="Merchant name"
              value={filters.merchant || ''}
              onChange={(e) => handleFilterChange('merchant', e.target.value || undefined)}
            />
          </div>

          <div className="filter-input">
            <label>Page Size</label>
            <select value={pageSize} onChange={(e) => setPageSize(parseInt(e.target.value))}>
              <option value={10}>10</option>
              <option value={20}>20</option>
              <option value={50}>50</option>
              <option value={100}>100</option>
            </select>
          </div>
        </div>
      </Card>

      <Card title="Transaction List" className="transactions-card">
        {isLoading ? (
          <div className="loading">Loading transactions...</div>
        ) : transactions?.data && transactions.data.length > 0 ? (
          <>
            <div className="table-wrapper">
              <table className="transactions-table">
                <thead>
                  <tr>
                    <th onClick={() => handleSort('created_at')} style={{ cursor: 'pointer' }}>
                      Date {sortBy === 'created_at' && (sortOrder === 'asc' ? '↑' : '↓')}
                    </th>
                    <th>User ID</th>
                    <th onClick={() => handleSort('amount')} style={{ cursor: 'pointer' }}>
                      Amount {sortBy === 'amount' && (sortOrder === 'asc' ? '↑' : '↓')}
                    </th>
                    <th>Type</th>
                    <th>Merchant</th>
                    <th>Location</th>
                    <th onClick={() => handleSort('risk_score')} style={{ cursor: 'pointer' }}>
                      Risk {sortBy === 'risk_score' && (sortOrder === 'asc' ? '↑' : '↓')}
                    </th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.data.map((transaction) => (
                    <tr key={transaction.id}>
                      <td>{new Date(transaction.created_at).toLocaleDateString()}</td>
                      <td>#{transaction.user_id}</td>
                      <td>${transaction.amount.toFixed(2)}</td>
                      <td>
                        <span className="badge badge-info">{transaction.transaction_type}</span>
                      </td>
                      <td>{transaction.merchant}</td>
                      <td>{transaction.location || '-'}</td>
                      <td>
                        <span className={`risk-badge risk-${getRiskLevel(transaction.risk_score)}`}>
                          {(transaction.risk_score * 100).toFixed(0)}%
                        </span>
                      </td>
                      <td>
                        <span className={`status-badge status-${transaction.is_fraudulent}`}>
                          {transaction.is_fraudulent}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="pagination">
              <button
                className="btn btn-sm"
                onClick={() => setPage(Math.max(1, page - 1))}
                disabled={page === 1}
              >
                <ChevronLeft size={18} /> Previous
              </button>

              <span className="page-info">
                Page {transactions.page} of {transactions.total_pages} (Total: {transactions.total})
              </span>

              <button
                className="btn btn-sm"
                onClick={() => setPage(Math.min(transactions.total_pages, page + 1))}
                disabled={page === transactions.total_pages}
              >
                Next <ChevronRight size={18} />
              </button>
            </div>
          </>
        ) : (
          <div className="empty-state">No transactions found</div>
        )}
      </Card>
    </div>
  )
}

function getRiskLevel(score: number): string {
  if (score < 0.3) return 'low'
  if (score < 0.6) return 'medium'
  if (score < 0.8) return 'high'
  return 'critical'
}

export default TransactionsPage
