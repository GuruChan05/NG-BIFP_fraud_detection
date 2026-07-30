# NG-BIFP: Next-Generation Bank Integrated Fraud Prevention System

## 🚀 Quick Deployment

```bash
# Clone and deploy in 3 commands
git clone https://github.com/GuruChan05/NG-BIFP_fraud_detection.git
cd NG-BIFP_fraud_detection
bash ngbfip/deploy.sh
```

**Access:**
- 🌐 Frontend: http://localhost:3000
- 📚 API Docs: http://localhost:8000/docs
- 🗄️ Database: localhost:5432

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)

## 📖 Overview

NG-BIFP is an **enterprise-grade fraud detection and prevention system** designed for banking institutions. It combines advanced machine learning models, real-time transaction monitoring, and intelligent device trust scoring to provide comprehensive fraud protection.

### Key Capabilities
- ✅ Real-time transaction analysis and risk scoring
- ✅ Machine learning-powered fraud detection
- ✅ Device trust assessment and management
- ✅ Comprehensive audit trails and compliance logging
- ✅ Professional web dashboard for monitoring
- ✅ RESTful API for third-party integration

## ✨ Features

### 🔐 Security & Authentication
- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Audit logging for all activities

### 🤖 Machine Learning
- **Isolation Forest**: Unsupervised anomaly detection for transaction fraud
- **Random Forest**: Device trust classification model
- **Risk Fusion Engine**: Multi-signal risk aggregation
- Real-time model inference

### 📊 Analytics & Monitoring
- Transaction risk scoring (0-1 scale)
- Risk level classification (low, medium, high, critical)
- Device consistency analysis
- Behavioral pattern recognition
- Alert generation and tracking

### 💾 Data Management
- PostgreSQL relational database
- SQLAlchemy ORM with migrations
- Comprehensive data models
- Transaction history and audit logs

### 🎨 User Interface
- React 18 modern frontend
- Responsive design
- Real-time data updates
- Intuitive dashboard

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│          FRONTEND (React 18)            │
│  Port 3000 • Vite • TanStack Query    │
└────────────────┬────────────────────────┘
                 │ HTTP/REST
┌────────────────▼────────────────────────┐
│      BACKEND (FastAPI/Uvicorn)         │
│  Port 8000 • Python 3.11              │
│  ├─ Auth Service (JWT)                 │
│  ├─ Transaction Processing             │
│  ├─ ML Model Inference                 │
│  ├─ Alert Management                   │
│  └─ Audit Logging                      │
└────────────────┬────────────────────────┘
                 │ SQL
┌────────────────▼────────────────────────┐
│   DATABASE (PostgreSQL 16)             │
│  Port 5432 • Persistent Storage       │
│  ├─ Users & Auth                       │
│  ├─ Transactions                       │
│  ├─ Alerts                             │
│  ├─ Devices                            │
│  └─ Audit Logs                         │
└─────────────────────────────────────────┘
```

## 🎯 Quick Start

### Prerequisites
- Docker Desktop (includes Docker & Docker Compose)
- Git
- 2GB RAM minimum
- Ports 3000, 8000, 5432 available

### Step-by-Step

**1. Clone Repository**
```bash
git clone https://github.com/GuruChan05/NG-BIFP_fraud_detection.git
cd NG-BIFP_fraud_detection
```

**2. One-Command Deploy**
```bash
bash ngbfip/deploy.sh
```

**3. Verify Services**
```bash
# Check logs
docker-compose -f ngbfip/docker-compose.prod.yml logs -f

# Wait for "Application startup" message
```

**4. Access Application**
- Frontend: http://localhost:3000
- API Swagger UI: http://localhost:8000/docs
- API ReDoc: http://localhost:8000/redoc

## 📦 Deployment

### Docker Compose (Recommended)

```bash
cd ngbfip

# Start all services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

### Environment Configuration

```bash
# Create .env from template
cp ngbfip/backend/.env.example ngbfip/backend/.env

# Edit with your settings
nano ngbfip/backend/.env
```

**Required Environment Variables:**
```bash
DATABASE_URL=postgresql://bifp_user:password@postgres:5432/ng_bifp
SECRET_KEY=your-secret-key-min-32-chars
DEBUG=False
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database Setup

```bash
# Run migrations
docker-compose -f ngbfip/docker-compose.prod.yml exec backend alembic upgrade head

# Access database
docker-compose -f ngbfip/docker-compose.prod.yml exec postgres \
  psql -U bifp_user -d ng_bifp
```

## 📁 Project Structure

```
NG-BIFP_fraud_detection/
├── ngbfip/
│   ├── frontend/                 # React application
│   │   ├── src/
│   │   │   ├── components/       # Reusable UI components
│   │   │   ├── hooks/            # Custom React hooks
│   │   │   ├── pages/            # Page components
│   │   │   ├── lib/              # Utilities (API client, etc)
│   │   │   └── main.tsx          # Application entry point
│   │   ├── Dockerfile            # Frontend container image
│   │   └── package.json          # Dependencies
│   │
│   ├── backend/                  # FastAPI application
│   │   ├── app/
│   │   │   ├── main.py           # FastAPI entry point
│   │   │   ├── core/             # Configuration & security
│   │   │   ├── db/               # Database models & setup
│   │   │   ├── api/v1/           # API endpoints
│   │   │   ├── services/         # Business logic
│   │   │   ├── schemas/          # Pydantic validation
│   │   │   └── ml/               # ML models
│   │   ├── Dockerfile            # Backend container image
│   │   └── requirements.txt      # Python dependencies
│   │
│   ├── datasets/                 # ML training data
│   │   ├── fraud_detection_dataset.csv
│   │   ├── fraud_train_processed.csv
│   │   ├── fraud_test_processed.csv
│   │   └── behavior_dataset_with_scores.csv
│   │
│   ├── docker-compose.prod.yml   # Orchestration
│   ├── deploy.sh                 # Deployment script
│   ├── stop.sh                   # Stop services
│   ├── setup-dev.sh              # Development setup
│   ├── DEPLOYMENT.md             # Detailed deployment guide
│   └── QUICKSTART.md             # Quick reference
│
├── .github/
│   └── workflows/
│       └── deploy.yml            # CI/CD pipeline
│
└── README.md                     # This file
```

## 🔌 API Endpoints

### Authentication
```
POST   /api/v1/auth/login        # User login
POST   /api/v1/auth/logout       # User logout
```

### Users
```
GET    /api/v1/users/me          # Get current user
GET    /api/v1/users/{id}        # Get user by ID
POST   /api/v1/users/            # Create user
PUT    /api/v1/users/{id}        # Update user
DELETE /api/v1/users/{id}        # Delete user
```

### Transactions
```
GET    /api/v1/transactions/            # List all transactions
GET    /api/v1/transactions/{id}        # Get transaction details
POST   /api/v1/transactions/            # Create transaction
GET    /api/v1/transactions/user/{id}   # Get user transactions
```

### Risk Analysis
```
POST   /api/v1/risk/analyze      # Analyze transaction risk
GET    /api/v1/risk/trends       # Get risk trends
```

### Alerts
```
GET    /api/v1/alerts/                  # List alerts
GET    /api/v1/alerts/{id}              # Get alert details
POST   /api/v1/alerts/                  # Create alert
PUT    /api/v1/alerts/{id}/resolve      # Resolve alert
```

### Devices
```
GET    /api/v1/devices/                 # List devices
GET    /api/v1/devices/{id}             # Get device details
POST   /api/v1/devices/                 # Register device
PUT    /api/v1/devices/{id}/trust       # Update device trust
```

### Dashboard
```
GET    /api/v1/dashboard/overview       # Dashboard summary
GET    /api/v1/dashboard/statistics     # Detailed statistics
```

### Health
```
GET    /api/v1/health/                  # Health check
```

## 🛠️ Technologies

### Backend Stack
- **Framework**: FastAPI 0.104
- **Server**: Uvicorn
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT + bcrypt
- **ML Libraries**: scikit-learn, pandas, numpy
- **Language**: Python 3.11

### Frontend Stack
- **Framework**: React 18
- **Build Tool**: Vite
- **Language**: TypeScript
- **HTTP Client**: Axios
- **State Management**: TanStack Query (React Query)
- **Routing**: React Router v6

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Database**: PostgreSQL
- **CI/CD**: GitHub Actions

## 📊 Machine Learning Models

### Isolation Forest
- **Purpose**: Unsupervised anomaly detection
- **Use Case**: Detect unusual transaction patterns
- **File**: `app/ml/isolation_forest_model.py`
- **Output**: Anomaly score (0-1)

### Random Forest Device Trust
- **Purpose**: Supervised device classification
- **Use Case**: Assess device reliability
- **File**: `app/ml/random_forest_device_trust.py`
- **Output**: Trust score (0-1)

### Risk Fusion Engine
- **Purpose**: Combine multiple risk signals
- **Weights**:
  - Transaction Risk: 40%
  - Device Trust: 30%
  - Behavioral Anomaly: 30%
- **File**: `app/ml/risk_fusion_engine.py`
- **Output**: Final risk score (0-1) + risk level

## 🔧 Development Setup

### Local Development

```bash
# Install dependencies
bash ngbfip/setup-dev.sh

# Backend
cd ngbfip/backend
python -m uvicorn app.main:app --reload

# Frontend (new terminal)
cd ngbfip/frontend
npm run dev
```

### Testing

```bash
# Backend tests
cd ngbfip/backend
pytest

# Frontend tests
cd ngbfip/frontend
npm test
```

## 📈 Scaling

### Horizontal Scaling
```yaml
# Multiple backend instances
services:
  backend:
    deploy:
      replicas: 3
```

### Database Optimization
- Add connection pooling (PgBouncer)
- Enable query caching
- Create indexes on frequently queried columns
- Archive old records

### Load Balancing
- Use Nginx as reverse proxy
- Configure round-robin load balancing
- Implement sticky sessions for authentication

## 🐛 Troubleshooting

### Common Issues

**Port already in use**
```bash
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
lsof -ti:5432 | xargs kill -9
```

**Docker not running**
```bash
# macOS/Windows
open -a Docker

# Linux
sudo systemctl start docker
```

**Database connection failed**
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# View logs
docker-compose -f ngbfip/docker-compose.prod.yml logs postgres
```

**Frontend can't reach API**
```bash
# Verify API_BASE_URL
echo $VITE_API_BASE_URL

# Check backend is running
curl http://localhost:8000/api/v1/health/
```

## 📝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Code Standards
- Backend: PEP 8 with Black formatter
- Frontend: ESLint + Prettier
- Commit messages: Conventional Commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Documentation**: [DEPLOYMENT.md](ngbfip/DEPLOYMENT.md)
- **Quick Start**: [QUICKSTART.md](ngbfip/QUICKSTART.md)
- **Issues**: https://github.com/GuruChan05/NG-BIFP_fraud_detection/issues
- **Discussions**: https://github.com/GuruChan05/NG-BIFP_fraud_detection/discussions

## 👨‍💼 Author

**GuruChan05**
- GitHub: [@GuruChan05](https://github.com/GuruChan05)
- Email: ajahguru11@gmail.com

## 🎯 Roadmap

- [ ] Enhanced ML model training pipeline
- [ ] Real-time notification system
- [ ] Advanced analytics dashboard
- [ ] Mobile app integration
- [ ] Cloud deployment templates (AWS, GCP, Azure)
- [ ] GraphQL API
- [ ] WebSocket support for real-time updates
- [ ] Multi-language support
- [ ] Advanced RBAC system
- [ ] Compliance reporting (PCI-DSS, GDPR)

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the powerful UI library
- PostgreSQL community
- scikit-learn for ML capabilities
- All contributors and supporters

---

**Made with ❤️ for fraud detection excellence**
