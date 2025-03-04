#!/bin/bash

# Define paths
ENV_REPO=".env-repo"
ENV_FILE=".env"
BRANCH="main"
USER_SERVICE_ROOT="services/user-service"
AUCTION_SERVICE_ROOT="services/auction-service"
API_GATEWAY_ROOT="services/api-gateway"
FRONTEND_ROOT="services/frontend"

cd $ENV_REPO || exit 1

# Sync main .env to project root
cp "../$ENV_FILE" "$ENV_FILE"

# Copy services .env to each .env-repo
cp "../$USER_SERVICE_ROOT/$ENV_FILE" "$USER_SERVICE_ROOT/$ENV_FILE"
cp "../$AUCTION_SERVICE_ROOT/$ENV_FILE" "$AUCTION_SERVICE_ROOT/$ENV_FILE"
cp "../$API_GATEWAY_ROOT/$ENV_FILE" "$API_GATEWAY_ROOT/$ENV_FILE"
cp "../$FRONTEND_ROOT/$ENV_FILE" "$FRONTEND_ROOT/$ENV_FILE"

echo "getting the latest .env from remote"
git pull
echo "Pushing latest .env to remote..."
git add .
git commit --quiet
git push

echo "✅ .env files uploaded successfully!"