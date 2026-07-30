# NG-BIFP: Next-Generation Bank Integrated Fraud Prevention

## Overview

NG-BIFP is an enterprise-grade fraud detection and prevention system for banking institutions. It combines machine learning models, real-time transaction monitoring, and device trust scoring to provide comprehensive fraud protection.

## Features

- **Real-time Transaction Monitoring**: Analyze transactions as they occur
- **ML-Powered Fraud Detection**: Isolation Forest and Random Forest models
- **Device Trust Scoring**: Assess device reliability and trustworthiness
- **Risk Fusion Engine**: Combine multiple risk signals into actionable insights
- **Audit Trail**: Complete logging of all system actions
- **Enterprise Dashboard**: Comprehensive monitoring and management interface
- **REST API**: Full-featured API for integration

## Architecture

### Backend Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **ML Libraries**: scikit-learn, pandas, numpy
- **Authentication**: JWT with bcrypt

### Frontend Stack
- **Framework**: React 18
- **State Management**: TanStack Query
- **HTTP Client**: Axios
- **Styling**: TBD

## Project Structure

```
ngbfip/
├── frontend/              # React enterprise frontend
├── backend/               # FastAPI backend
├── datasets/              # Training and test datasets
├── docker-compose.prod.yml
├── .github/workflows/
└── README.md
```

## Setup Instructions

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+

### Development

1. Clone the repository
```bash
git clone https://github.com/GuruChan05/NG-BIFP_fraud_detection.git
cd NG-BIFP_fraud_detection/ngbfip
```

2. Start services with Docker Compose
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. Run migrations
```bash
cd backend
alembic upgrade head
```

4. Install frontend dependencies
```bash
cd frontend
npm install
npm run dev
```

### API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout

### Users
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/users/{user_id}` - Get user details
- `POST /api/v1/users/` - Create new user

### Transactions
- `GET /api/v1/transactions/` - List transactions
- `GET /api/v1/transactions/{transaction_id}` - Get transaction
- `POST /api/v1/transactions/` - Create transaction

### Alerts
- `GET /api/v1/alerts/` - List alerts
- `GET /api/v1/alerts/{alert_id}` - Get alert
- `POST /api/v1/alerts/` - Create alert

### Risk Analysis
- `POST /api/v1/risk/analyze` - Analyze transaction risk
- `GET /api/v1/risk/trends` - Get risk trends

### Dashboard
- `GET /api/v1/dashboard/overview` - Dashboard overview
- `GET /api/v1/dashboard/statistics` - Dashboard statistics

## Machine Learning Models

### Isolation Forest
- **Purpose**: Unsupervised anomaly detection for transaction fraud
- **Implementation**: `app/ml/isolation_forest_model.py`
- **Contamination**: 10% (configurable)

### Random Forest (Device Trust)
- **Purpose**: Supervised classification for device trustworthiness
- **Implementation**: `app/ml/random_forest_device_trust.py`
- **Classes**: Trusted (1), Untrusted (0)

### Risk Fusion Engine
- **Purpose**: Combine multiple risk signals
- **Implementation**: `app/ml/risk_fusion_engine.py`
- **Weights**: Transaction (40%), Device Trust (30%), Behavioral Anomaly (30%)

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.
