#!/usr/bin/env bash
set -e
echo "Starting lab: building and bringing up containers..."
docker-compose up --build -d
echo "Services:"
docker-compose ps
echo "You can access web app at http://localhost:5000"
