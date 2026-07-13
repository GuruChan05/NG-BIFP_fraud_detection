# Quick Start Guide

## 🚀 One-Command Deployment

```bash
bash deploy.sh
```

This will:
1. ✅ Check Docker installation
2. ✅ Create environment files
3. ✅ Build all Docker images
4. ✅ Start all services (PostgreSQL, Backend, Frontend)
5. ✅ Display access URLs

## 📱 Access the Application

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Database**: postgresql://bifp_user:secure_password_change_me@localhost:5432/ng_bifp

## 🛑 Stop Services

```bash
bash stop.sh
```

## 📝 Manual Commands

```bash
# View logs
docker-compose -f ngbfip/docker-compose.prod.yml logs -f

# Access backend shell
docker-compose -f ngbfip/docker-compose.prod.yml exec backend bash

# Access database
docker-compose -f ngbfip/docker-compose.prod.yml exec postgres psql -U bifp_user -d ng_bifp

# Restart services
docker-compose -f ngbfip/docker-compose.prod.yml restart
```

## 📚 Documentation

See [DEPLOYMENT.md](ngbfip/DEPLOYMENT.md) for comprehensive deployment guide.

## ⚙️ Development Setup

```bash
bash ngbfip/setup-dev.sh
```

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different ports in docker-compose.prod.yml
```

**Docker not running:**
```bash
# Make sure Docker Desktop is running
# On Linux: sudo systemctl start docker
```

**Can't connect to database:**
```bash
# Check PostgreSQL is running
docker-compose -f ngbfip/docker-compose.prod.yml logs postgres

# Verify credentials in .env
```

## 📞 Support

For issues: https://github.com/GuruChan05/NG-BIFP_fraud_detection/issues
