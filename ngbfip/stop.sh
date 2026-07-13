#!/bin/bash

# Stop all services
echo "Stopping NG-BIFP services..."
docker-compose -f docker-compose.prod.yml down
echo "✅ All services stopped"
