#!/bin/bash

# Docker Cleanup Script for Slidespeak Project
# This script removes all containers, images, and volumes for frontend and backend services

set -e  # Exit on any error

echo "🧹 Starting Docker cleanup for Slidespeak project..."

# Stop and remove all containers from the compose file
echo "📦 Stopping and removing containers..."
docker compose down --remove-orphans

# Remove containers specifically for frontend and backend (if any are still running)
echo "🛑 Removing any remaining frontend and backend containers..."
docker ps -a --filter "name=frontend" --filter "name=backend" -q | xargs -r docker rm -f

# Remove images for frontend and backend services
echo "🖼️  Removing frontend and backend images..."

# Get the project name (directory name) for image naming
PROJECT_NAME=$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g')

# Remove images with common naming patterns
docker images --filter "reference=${PROJECT_NAME}_frontend*" -q | xargs -r docker rmi -f
docker images --filter "reference=${PROJECT_NAME}_backend*" -q | xargs -r docker rmi -f
docker images --filter "reference=${PROJECT_NAME}-frontend*" -q | xargs -r docker rmi -f
docker images --filter "reference=${PROJECT_NAME}-backend*" -q | xargs -r docker rmi -f

# Also remove images with the default docker-compose naming
docker images --filter "reference=*frontend*" --filter "reference=*backend*" -q | xargs -r docker rmi -f 2>/dev/null || true

# Remove all volumes (including anonymous volumes)
echo "💾 Removing all volumes..."
docker volume ls -q | xargs -r docker volume rm 2>/dev/null || true

# Remove any dangling images and build cache
echo "🗑️  Cleaning up dangling images and build cache..."
docker image prune -f
docker builder prune -f

# Optional: Remove all unused networks
echo "🌐 Cleaning up unused networks..."
docker network prune -f

echo "✅ Docker cleanup completed!"
echo ""
echo "🚀 Ready to rebuild with:"
echo "   docker compose up -d"
echo ""
echo "📊 Current Docker status:"
echo "   Containers: $(docker ps -a -q | wc -l)"
echo "   Images: $(docker images -q | wc -l)"
echo "   Volumes: $(docker volume ls -q | wc -l)"