#!/bin/bash

# Define paths
ENV_REPO=".env-repo"
ENV_FILE=".env"
BRANCH="main"
USER_SERVICE_ROOT="services/user-service"
AUCTION_SERVICE_ROOT="services/auction-service"
API_GATEWAY_ROOT="services/api-gateway"
FRONTEND_ROOT="services/frontend"

echo "Fetching latest .env from remote..."
cd $ENV_REPO || { echo "Failed to change to $ENV_REPO directory"; exit 1; }
git pull origin $BRANCH --quiet || { echo "Failed to pull from remote $BRANCH"; exit 1; }

# Sync main .env to project root
cp "$ENV_FILE" "../$ENV_FILE" || { echo "Failed to copy main .env file"; exit 1; }

# Sync services .env to each service root
cp "$USER_SERVICE_ROOT/$ENV_FILE" "../$USER_SERVICE_ROOT/$ENV_FILE" || { echo "Failed to copy .env for user-service"; exit 1; }
cp "$AUCTION_SERVICE_ROOT/$ENV_FILE" "../$AUCTION_SERVICE_ROOT/$ENV_FILE" || { echo "Failed to copy .env for auction-service"; exit 1; }
cp "$API_GATEWAY_ROOT/$ENV_FILE" "../$API_GATEWAY_ROOT/$ENV_FILE" || { echo "Failed to copy .env for api-gateway"; exit 1; }
cp "$FRONTEND_ROOT/$ENV_FILE" "../$FRONTEND_ROOT/$ENV_FILE" || { echo "Failed to copy .env for frontend"; exit 1; }

echo "✅ .env files updated successfully!"