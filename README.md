# NG-BIFP Fraud Detection Platform

**Next-Generation Bank Integrated Fraud Prevention** - A production-ready AI-powered fraud detection platform built with React, FastAPI, and PostgreSQL.

## 🎯 Overview

NG-BIFP is an enterprise-grade fraud detection system featuring:

- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **Machine Learning**: ML-powered fraud detection with risk scoring
- **Real-time Dashboard**: Interactive glassmorphism UI with live statistics
- **Transaction Analysis**: Comprehensive transaction risk assessment
- **Device Trust**: Device fingerprinting and trust scoring
- **Alert Management**: Automated alert generation and resolution tracking
- **Audit Logging**: Complete audit trail for compliance
- **Role-based Access**: User, Analyst, and Admin roles

## 🏗️ Architecture

```
┌─────────────────┐
│  React 18 SPA   │ (Glassmorphism UI)
│  TypeScript     │
│  Tailwind CSS   │
└────────┬────────┘
         │ HTTP/REST
         ↓
┌─────────────────────────────────┐
│   FastAPI Backend               │
│   - Authentication (JWT)        │
│   - Business Logic Services     │
│   - ML Model Integration        │
└────────┬────────────────────────┘
         │ SQL
         ↓
┌─────────────────┐
│   PostgreSQL    │
│   Database      │
└─────────────────┘
```

## 📋 Tech Stack

### Frontend
- **React 18**: Modern UI library
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first CSS
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Lucide React**: Icon library

### Backend
- **FastAPI**: Modern async web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation
- **PostgreSQL**: Relational database
- **python-jose**: JWT token generation
- **passlib**: Password hashing
- **scikit-learn**: ML models

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- PostgreSQL 16+ (if running without Docker)

### Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/GuruChan05/NG-BIFP_fraud_detection.git
cd NG-BIFP_fraud_detection
```

#### 2. Backend Setup
```bash
cd ngbfip/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database
python -m app.db.init_db

# Run backend
python app/main.py
```

Backend will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

#### 3. Frontend Setup
```bash
cd ngbfip/frontend

# Install dependencies
npm install

# Update .env.local if needed
echo "VITE_API_BASE_URL=http://localhost:8000" > .env.local

# Run frontend
npm run dev
```

Frontend will be available at: `http://localhost:5173`

### Production Deployment

#### Using Docker Compose
```bash
# Navigate to project root
cd ngbfip

# Make deployment script executable
chmod +x deploy.sh stop.sh

# Deploy
./deploy.sh
```

Services will be available at:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## 🔐 Environment Variables

### Backend (.env)
```bash
# Application
APP_NAME=NG-BIFP Fraud Detection
DEBUG=False  # Set to True for development
VERSION=1.0.0

# Database
DATABASE_URL=postgresql://bifp_user:bifp_password@localhost:5432/ng_bifp
SQLALCHEMY_ECHO=False

# Security (CHANGE IN PRODUCTION)
SECRET_KEY=your-super-secret-key-change-this-in-production-to-random-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Frontend (.env.local)
```bash
VITE_API_BASE_URL=http://localhost:8000
```

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/logout` - Logout user
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/forgot-password` - Request password reset

### Users
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user

### Transactions
- `GET /api/v1/transactions/` - List transactions
- `GET /api/v1/transactions/{transaction_id}` - Get transaction
- `POST /api/v1/transactions/` - Create transaction

### Risk Analysis
- `POST /api/v1/risk/analyze` - Analyze transaction risk
- `GET /api/v1/risk/trends` - Get risk trends

### Alerts
- `GET /api/v1/alerts/` - List alerts
- `GET /api/v1/alerts/{alert_id}` - Get alert
- `PUT /api/v1/alerts/{alert_id}/resolve` - Resolve alert

### Devices
- `GET /api/v1/devices/` - List devices
- `POST /api/v1/devices/` - Register device
- `PUT /api/v1/devices/{device_id}/trust` - Update device trust

### Dashboard
- `GET /api/v1/dashboard/overview` - Dashboard overview
- `GET /api/v1/dashboard/statistics` - Detailed statistics

## 🧪 Testing

### Backend Tests
```bash
cd ngbfip/backend

# Run tests (when test suite is added)
pytest

# With coverage
pytest --cov
```

### Frontend Tests
```bash
cd ngbfip/frontend

# Run tests (when test suite is added)
npm test

# With coverage
npm test -- --coverage
```

## 🔍 Audit Report Summary

### ✅ Implemented
- [x] Complete authentication system (Register, Login, JWT)
- [x] Comprehensive database models with relationships
- [x] Full REST API with error handling
- [x] Service layer with business logic
- [x] React frontend with authentication flow
- [x] Dashboard with statistics
- [x] Glassmorphism UI design
- [x] Docker containerization
- [x] Audit logging system
- [x] Role-based access control
- [x] Request/response validation with Pydantic
- [x] CORS configuration
- [x] Health check endpoints
- [x] Comprehensive logging
- [x] Environment configuration

### 🔧 Configuration Files
- Backend: `.env.example` → `.env`
- Frontend: `.env.local` (pre-configured)
- Docker: `docker-compose.prod.yml`
- Database: PostgreSQL initialization included

## 📊 Database Schema

### Tables
- `users` - User accounts and profiles
- `transactions` - Transaction records with risk scores
- `alerts` - Fraud detection alerts
- `devices` - Device fingerprints and trust scores
- `notifications` - User notifications
- `audit_logs` - Compliance audit trail

## 🛡️ Security Features

- **Password Security**: Bcrypt with configurable rounds
- **JWT Authentication**: Secure token-based auth
- **CORS Protection**: Configurable origin whitelist
- **SQL Injection Prevention**: SQLAlchemy parameterized queries
- **Request Validation**: Pydantic schema validation
- **Audit Logging**: Complete action tracking
- **Rate Limiting**: Ready for implementation
- **HTTPS Ready**: Docker/production ready

## 📈 Performance Optimizations

- Database connection pooling
- Query optimization with indexes
- Async/await patterns
- Frontend code splitting
- Lazy loading of components
- Caching-ready architecture

## 🐳 Docker Management

### Start Services
```bash
cd ngbfip
./deploy.sh
```

### Stop Services
```bash
cd ngbfip
./stop.sh
```

### View Logs
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### Access Container
```bash
docker-compose -f docker-compose.prod.yml exec backend bash
docker-compose -f docker-compose.prod.yml exec frontend sh
```

## 📝 Default Test Credentials

After initial setup, you can use:
- **Email**: test@example.com
- **Password**: TestPassword123

> Note: Create an actual user through the registration form for production use.

## 🚨 Production Checklist

- [ ] Update `SECRET_KEY` in backend `.env`
- [ ] Set `DEBUG=False` in backend `.env`
- [ ] Update `DATABASE_URL` for production database
- [ ] Configure `CORS_ORIGINS` for your domain
- [ ] Update `VITE_API_BASE_URL` in frontend
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up backup strategy for database
- [ ] Configure logging aggregation
- [ ] Set up monitoring and alerting
- [ ] Create admin user account
- [ ] Run security audit
- [ ] Set up CI/CD pipeline

## 📞 Support

For issues, questions, or contributions:
1. Check existing issues on GitHub
2. Review API documentation at `/docs`
3. Check logs in `ngbfip/backend/logs/app.log`

## 📄 License

This project is proprietary software.

## 🎉 Acknowledgments

Built with modern web technologies for enterprise-grade fraud detection.

---

**Last Updated**: 2026-07-15
**Version**: 1.0.0
