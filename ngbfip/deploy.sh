#!/bin/bash

# NG-BIFP Deployment Script

set -e

echo "====================================="
echo "NG-BIFP Fraud Detection Deployment"
echo "====================================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop."
    exit 1
fi
echo "✅ Docker found: $(docker --version)"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed."
    exit 1
fi
echo "✅ Docker Compose found: $(docker-compose --version)"

echo ""
echo "📦 Building and starting services..."
echo ""

# Change to project directory
cd "$(dirname "$0")/ngbfip" || exit

# Create .env files if they don't exist
if [ ! -f backend/.env ]; then
    echo "Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env with your configuration"
fi

if [ ! -f frontend/.env ]; then
    echo "Creating frontend/.env from template..."
    cp frontend/.env.example frontend/.env
fi

echo ""
echo "🚀 Starting Docker Compose services..."
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "Access the application:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "To view logs:"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose -f docker-compose.prod.yml down"
echo ""
