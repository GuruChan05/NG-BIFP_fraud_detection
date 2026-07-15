#!/bin/bash

# NG-BIFP Production Deployment Script

set -e

echo "================================"
echo "NG-BIFP Fraud Detection Platform"
echo "Production Deployment"
echo "================================"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    exit 1
fi

echo "Starting services..."
cd "$(dirname "$0")"

# Create .env if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "Creating .env file from template..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please update backend/.env with your production settings"
fi

# Start services
echo "Building and starting Docker containers..."
docker-compose -f docker-compose.prod.yml up -d

echo "Waiting for services to be ready..."
sleep 10

# Run database migrations
echo "Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head || true

# Initialize database if needed
echo "Initializing database tables..."
docker-compose -f docker-compose.prod.yml exec -T backend python -m app.db.init_db || true

echo ""
echo "================================"
echo "✅ Deployment Complete!"
echo "================================"
echo ""
echo "Services running:"
echo "  🌐 Frontend: http://localhost:3000"
echo "  📚 API Docs: http://localhost:8000/docs"
echo "  📖 ReDoc: http://localhost:8000/redoc"
echo "  🗄️  Database: localhost:5432"
echo ""
echo "View logs:"
echo "  docker-compose -f ngbfip/docker-compose.prod.yml logs -f"
echo ""
echo "Stop services:"
echo "  bash ngbfip/stop.sh"
echo ""
