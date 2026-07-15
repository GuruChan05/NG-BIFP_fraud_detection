#!/bin/bash

# NG-BIFP Stop Services Script

echo "Stopping NG-BIFP services..."
cd "$(dirname "$0")"

docker-compose -f docker-compose.prod.yml down

echo "✅ Services stopped"
