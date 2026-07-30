import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { AlertTriangle, CheckCircle } from 'lucide-react'
import { useState } from 'react'
import api from '@/lib/api'
import Card from '@/components/Card'
import './FraudDetectionPage.css'

interface PredictionRequest {
  user_id: number
  amount: number
  transaction_type: string
  merchant: string
  merchant_category?: string
  location?: string
  device_id?: string
}

interface PredictionResult {
  risk_score: number
  confidence_score: number
  prediction: string
  explanation: string
}

function FraudDetectionPage() {
  const [predictionRequest, setPredictionRequest] = useState<PredictionRequest>({
    user_id: 1,
    amount: 0,
    transaction_type: 'debit',
    merchant: '',
  })

  const queryClient = useQueryClient()

  // Fetch prediction statistics
  const { data: stats } = useQuery({
    queryKey: ['fraud-predictions', 'stats'],
    queryFn: async () => {
      const response = await api.get('/fraud-predictions/stats')
      return response.data
    },
  })

  // Fetch prediction history
  const { data: history, isLoading: historyLoading } = useQuery({
    queryKey: ['fraud-predictions', 'history'],
    queryFn: async () => {
      const response = await api.get('/fraud-predictions/')
      return response.data
    },
  })

  // Make prediction mutation
  const predictMutation = useMutation({
    mutationFn: async (request: PredictionRequest) => {
      const response = await api.post('/fraud-predictions/predict', request)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fraud-predictions'] })
    },
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setPredictionRequest((prev) => ({
      ...prev,
      [name]: name === 'amount' ? parseFloat(value) : value,
    }))
  }

  const handlePredict = () => {
    if (predictionRequest.amount <= 0 || !predictionRequest.merchant) {
      alert('Please fill in all required fields')
      return
    }
    predictMutation.mutate(predictionRequest)
  }

  const prediction = predictMutation.data as PredictionResult | undefined

  return (
    <div className="fraud-detection-page">
      <h1>Fraud Detection Engine</h1>

      {/* Statistics Cards */}
      <div className="stats-grid">
        <Card className="stat-card">
          <div className="stat-content">
            <div className="stat-label">Total Predictions</div>
            <div className="stat-value">{stats?.total_predictions || 0}</div>
          </div>
        </Card>
        <Card className="stat-card">
          <div className="stat-content">
            <div className="stat-label">Fraudulent Detected</div>
            <div className="stat-value">{stats?.fraud_predictions || 0}</div>
          </div>
        </Card>
        <Card className="stat-card">
          <div className="stat-content">
            <div className="stat-label">Fraud Rate</div>
            <div className="stat-value">{stats?.fraud_detection_rate?.toFixed(1) || 0}%</div>
          </div>
        </Card>
        <Card className="stat-card">
          <div className="stat-content">
            <div className="stat-label">Avg Risk Score</div>
            <div className="stat-value">{(stats?.average_risk_score * 100)?.toFixed(1) || 0}%</div>
          </div>
        </Card>
      </div>

      <div className="content-grid">
        {/* Prediction Form */}
        <Card title="Make Prediction" className="prediction-form-card">
          <div className="form-grid">
            <div className="form-group">
              <label>User ID</label>
              <input
                type="number"
                name="user_id"
                value={predictionRequest.user_id}
                onChange={handleInputChange}
                placeholder="User ID"
              />
            </div>
            <div className="form-group">
              <label>Amount</label>
              <input
                type="number"
                name="amount"
                value={predictionRequest.amount || ''}
                onChange={handleInputChange}
                placeholder="Transaction Amount"
                step="0.01"
              />
            </div>
            <div className="form-group">
              <label>Transaction Type</label>
              <select name="transaction_type" value={predictionRequest.transaction_type} onChange={handleInputChange}>
                <option value="debit">Debit</option>
                <option value="credit">Credit</option>
                <option value="transfer">Transfer</option>
              </select>
            </div>
            <div className="form-group">
              <label>Merchant</label>
              <input
                type="text"
                name="merchant"
                value={predictionRequest.merchant}
                onChange={handleInputChange}
                placeholder="Merchant Name"
              />
            </div>
            <div className="form-group">
              <label>Category</label>
              <input
                type="text"
                name="merchant_category"
                value={predictionRequest.merchant_category || ''}
                onChange={handleInputChange}
                placeholder="Merchant Category"
              />
            </div>
            <div className="form-group">
              <label>Location</label>
              <input
                type="text"
                name="location"
                value={predictionRequest.location || ''}
                onChange={handleInputChange}
                placeholder="Transaction Location"
              />
            </div>
          </div>
          <button
            className="btn btn-primary btn-large"
            onClick={handlePredict}
            disabled={predictMutation.isPending}
          >
            {predictMutation.isPending ? 'Analyzing...' : 'Analyze Transaction'}
          </button>
        </Card>

        {/* Prediction Result */}
        {prediction && (
          <Card title="Prediction Result" className="prediction-result-card">
            <div className={`risk-indicator risk-${prediction.risk_score >= 0.70 ? 'High' : 'Low'}`}>
              <div className="risk-icon">
                {prediction.prediction === 'fraudulent' && <AlertTriangle size={48} />}
                {prediction.prediction === 'legitimate' && <CheckCircle size={48} />}
              </div>
              <div className="risk-info">
                <div className="risk-status">{prediction.prediction.toUpperCase()}</div>
                <div className="risk-level-badge">{prediction.risk_score >= 0.70 ? 'High' : 'Low'}</div>
              </div>
            </div>

            <div className="scores-section">
              <div className="score-item">
                <div className="score-label">Risk Score</div>
                <div className="score-bar">
                  <div className="score-fill" style={{ width: `${prediction.risk_score * 100}%` }} />
                </div>
                <div className="score-value">{(prediction.risk_score * 100).toFixed(1)}%</div>
              </div>
              <div className="score-item">
                <div className="score-label">Confidence Score</div>
                <div className="score-bar">
                  <div className="score-fill confidence" style={{ width: `${prediction.confidence_score * 100}%` }} />
                </div>
                <div className="score-value">{(prediction.confidence_score * 100).toFixed(1)}%</div>
              </div>
            </div>

            <div className="explanation-section">
              <h3>Explanation</h3>
              <p>{prediction.explanation}</p>
            </div>

            <div className="factors-section">
              <h3>Contributing Factors</h3>
              <ul className="factors-list">
                {prediction.explanation.split(';').map((factor, index) => (
                  <li key={index}>• {factor.trim()}</li>
                ))}
              </ul>
            </div>
          </Card>
        )}
      </div>

      {/* Prediction History */}
      <Card title="Recent Predictions" className="history-card">
        {historyLoading ? (
          <div className="loading">Loading history...</div>
        ) : history?.data && history.data.length > 0 ? (
          <div className="history-table-wrapper">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Risk Score</th>
                  <th>Confidence</th>
                  <th>Status</th>
                  <th>Risk Level</th>
                </tr>
              </thead>
              <tbody>
                {history.data.map((entry: any) => (
                  <tr key={entry.id}>
                    <td>{new Date(entry.created_at).toLocaleString()}</td>
                    <td>
                      <span className="score-badge">{(entry.risk_score * 100).toFixed(1)}%</span>
                    </td>
                    <td>
                      <span className="confidence-badge">{(entry.confidence_score * 100).toFixed(1)}%</span>
                    </td>
                    <td>
                      <span className={`status-badge status-${entry.prediction}`}>
                        {entry.prediction}
                      </span>
                    </td>
                    <td>
                      <span className={`level-badge level-${entry.risk_score >= 0.70 ? 'High' : 'Low'}`}>{entry.risk_score >= 0.70 ? 'High' : 'Low'}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">No predictions yet</div>
        )}
      </Card>
    </div>
  )
}

export default FraudDetectionPage
