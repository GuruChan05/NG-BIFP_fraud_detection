# NG-BIFP Deployment Guide

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 20GB storage
- Linux/macOS/Windows with WSL2

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/GuruChan05/NG-BIFP_fraud_detection.git
cd NG-BIFP_fraud_detection
```

### 2. Configure Environment
```bash
cd ngbfip/backend
cp .env.example .env

# Edit .env with your settings
# IMPORTANT: Change SECRET_KEY to a random 32-character string
nano .env
```

### 3. Deploy
```bash
cd ../
chmod +x deploy.sh
./deploy.sh
```

## Production Setup

### Generate Secure Secret Key
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Update Database
```bash
# In production .env
DATABASE_URL=postgresql://username:password@your-db-host:5432/ng_bifp
```

### Configure CORS
```bash
# In production .env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Enable HTTPS
```bash
# Use nginx reverse proxy or AWS ALB
# Configure SSL certificates (Let's Encrypt recommended)
```

## Monitoring

### Check Service Status
```bash
docker-compose -f docker-compose.prod.yml ps
```

### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Database Backup
```bash
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U bifp_user ng_bifp > backup.sql
```

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Verify database connection
docker-compose -f docker-compose.prod.yml exec backend python -c "import sqlalchemy; print('OK')"
```

### Frontend can't connect to API
- Verify backend is running: `curl http://localhost:8000/api/v1/health/`
- Check `VITE_API_BASE_URL` in frontend `.env.local`
- Check CORS settings in backend `.env`

### Database connection error
```bash
# Reset database
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d
```

## Performance Tuning

### Database
```sql
-- Create indexes for queries
CREATE INDEX idx_transaction_risk ON transactions(risk_score);
CREATE INDEX idx_user_email ON users(email);
```

### Application
- Increase worker count for production
- Configure connection pool size
- Enable caching for static assets

## Security Hardening

1. **Update all passwords** in `.env`
2. **Enable firewall** - Only expose ports 80/443
3. **SSL/TLS certificates** - Use Let's Encrypt
4. **Regular backups** - Daily automated backups
5. **Monitor logs** - Set up log aggregation
6. **Rate limiting** - Configure API rate limits
7. **Regular updates** - Keep Docker images updated

## Scaling

### Horizontal Scaling
```yaml
# Use Docker Swarm or Kubernetes
docker service create --replicas 3 backend
```

### Load Balancing
```bash
# Configure nginx or HAProxy
# Point to multiple backend instances
```

## Backup & Recovery

### Daily Backup
```bash
#!/bin/bash
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump \
  -U bifp_user ng_bifp > /backups/ng_bifp_$(date +%Y%m%d_%H%M%S).sql
```

### Restore from Backup
```bash
docker-compose -f docker-compose.prod.yml exec -T postgres psql \
  -U bifp_user ng_bifp < /backups/backup.sql
```

## Support

For deployment issues, check:
- Docker logs: `docker-compose logs`
- Application logs: `/ngbfip/backend/logs/app.log`
- Database logs: `docker logs ng-bifp-postgres`
