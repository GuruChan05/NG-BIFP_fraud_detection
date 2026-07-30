#!/bin/bash

# Quick development setup

echo "Setting up NG-BIFP development environment..."

# Backend setup
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Frontend setup
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "✅ Development setup complete!"
echo ""
echo "To start development:"
echo "  Backend:  cd backend && python -m uvicorn app.main:app --reload"
echo "  Frontend: cd frontend && npm run dev"
