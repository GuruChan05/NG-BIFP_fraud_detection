# NG-BIFP Fraud Detection - Comprehensive Testing Guide

## 📊 API Testing with cURL

### Health Check
```bash
curl -X GET "http://localhost:8000/api/v1/health/"
```

### Authentication

**Login**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword"
  }'
```

**Expected Response**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Transactions

**Create Transaction**
```bash
TOKEN="your-access-token-here"

curl -X POST "http://localhost:8000/api/v1/transactions/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 500.50,
    "transaction_type": "debit",
    "merchant": "Amazon",
    "merchant_category": "Electronics",
    "location": "USA-CA",
    "device_id": "device-123"
  }'
```

**List Transactions**
```bash
curl -X GET "http://localhost:8000/api/v1/transactions/" \
  -H "Authorization: Bearer $TOKEN"
```

### Risk Analysis

**Analyze Risk**
```bash
curl -X POST "http://localhost:8000/api/v1/risk/analyze" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5000,
    "merchant_category": "Electronics",
    "location": "Nigeria",
    "device_trust": 0.3,
    "transaction_frequency": 1
  }'
```

## 🧪 Backend Unit Tests

```bash
# Install test dependencies
cd ngbfip/backend
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## 🎨 Frontend Testing

```bash
cd ngbfip/frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## 📈 Performance Testing

```bash
# Install load testing tool
pip install locust

# Create locustfile.py in backend directory
# Run load test
locust -f locustfile.py -u 100 -r 10 http://localhost:8000
```

## 🔍 Database Testing

```bash
# Connect to database
docker-compose -f ngbfip/docker-compose.prod.yml exec postgres \
  psql -U bifp_user -d ng_bifp

# Test queries
SELECT * FROM users;
SELECT COUNT(*) FROM transactions;
SELECT * FROM alerts WHERE is_resolved = false;
```

## ✅ Integration Tests

```bash
# Test full flow
1. Create user
2. Login
3. Create transaction
4. Analyze risk
5. Check alert
6. View dashboard
```

## 📊 Test Coverage

- Backend: Aim for >80% coverage
- Frontend: Aim for >70% coverage
- Critical paths: 100% coverage

## 🚀 Continuous Integration

Tests run automatically on:
- Pull requests
- Commits to main
- Scheduled daily runs

See `.github/workflows/` for CI/CD configuration.
