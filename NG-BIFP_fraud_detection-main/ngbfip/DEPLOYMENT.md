# NG-BIFP Fraud Detection - Deployment Guide

## Quick Start with Docker Compose

### Prerequisites
- Docker Desktop (includes Docker Engine and Docker Compose)
- Git
- Minimum 2GB RAM available
- Ports 5432, 8000, 3000 should be available

### Steps to Deploy

1. **Clone the Repository**
```bash
git clone https://github.com/GuruChan05/NG-BIFP_fraud_detection.git
cd NG-BIFP_fraud_detection/ngbfip
```

2. **Configure Environment Variables**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration

# Frontend (optional for local development)
cp frontend/.env.example frontend/.env
```

3. **Start Services**
```bash
# Navigate to ngbfip directory
cd ngbfip

# Build and start all services
docker-compose -f docker-compose.prod.yml up -d

# Monitor logs
docker-compose -f docker-compose.prod.yml logs -f
```

4. **Access the Application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Database**: localhost:5432

### Database Setup

```bash
# Run migrations (if needed)
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Access PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres psql -U bifp_user -d ng_bifp
```

### Stopping Services

```bash
# Stop all services
docker-compose -f docker-compose.prod.yml down

# Stop and remove volumes (careful!)
docker-compose -f docker-compose.prod.yml down -v
```

## Service Details

### PostgreSQL Database
- **Container**: ng_bifp_db
- **Port**: 5432
- **Database**: ng_bifp
- **User**: bifp_user
- **Password**: secure_password_change_me (change in production!)

### FastAPI Backend
- **Container**: ng_bifp_api
- **Port**: 8000
- **Framework**: FastAPI with Uvicorn
- **Features**: JWT Auth, SQLAlchemy ORM, ML Models

### React Frontend
- **Container**: ng_bifp_web
- **Port**: 3000
- **Framework**: React 18 with Vite
- **Features**: TanStack Query, Axios, React Router

## Debugging

### View Service Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs

# Specific service
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend
docker-compose -f docker-compose.prod.yml logs postgres
```

### Access Service Shell
```bash
# Backend shell
docker-compose -f docker-compose.prod.yml exec backend bash

# Frontend shell
docker-compose -f docker-compose.prod.yml exec frontend sh

# Database shell
docker-compose -f docker-compose.prod.yml exec postgres bash
```

### Common Issues

**Port already in use**
```bash
# Change ports in docker-compose.prod.yml or use:
docker-compose -f docker-compose.prod.yml down
```

**Database connection failed**
```bash
# Wait for postgres to be healthy
docker-compose -f docker-compose.prod.yml logs postgres
# Check environment variables in docker-compose.prod.yml
```

**Frontend can't reach backend**
```bash
# Verify VITE_API_BASE_URL in frontend environment
# Should match backend service URL
```

## Production Deployment

### Security Checklist
- [ ] Change all default passwords
- [ ] Update SECRET_KEY with a strong random string
- [ ] Set DEBUG=False
- [ ] Update CORS_ORIGINS with actual domain
- [ ] Use environment-specific .env files
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up proper database backups
- [ ] Enable database authentication
- [ ] Configure API rate limiting

### Environment Variables for Production
```bash
# backend/.env
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]
SECRET_KEY=[generate-secure-random-string]
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
LOG_LEVEL=WARNING
```

### Database Backup
```bash
# Backup
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U bifp_user ng_bifp > backup.sql

# Restore
docker-compose -f docker-compose.prod.yml exec -T postgres \
  psql -U bifp_user ng_bifp < backup.sql
```

## Performance Optimization

### Scale Backend
```yaml
# In docker-compose.prod.yml
services:
  backend:
    deploy:
      replicas: 3
```

### Database Connection Pool
Update connection pool settings in `app/core/config.py` for production loads.

## Monitoring

### Health Check Endpoint
```bash
curl http://localhost:8000/api/v1/health/
```

### Metrics (can be extended)
- API Response Times
- Database Query Performance
- Error Rates
- User Activity Logs

## Support & Documentation

- **API Documentation**: http://localhost:8000/docs
- **GitHub Repository**: https://github.com/GuruChan05/NG-BIFP_fraud_detection
- **Issues**: https://github.com/GuruChan05/NG-BIFP_fraud_detection/issues

## License

MIT License - See LICENSE file
