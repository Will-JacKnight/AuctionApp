#!/bin/bash

# Define paths
ENV_REPO=".env-repo"
ENV_FILE=".env"
BRANCH="main"  # Change if needed
USER_SERVICE_ROOT="services/user-service"
AUCTION_SERVICE_ROOT="services/auction-service"
API_GATEWAY_ROOT="services/api-gateway"
FRONTEND_ROOT="services/frontend"

echo "Fetching latest .env from remote..."
cd $ENV_REPO || exit
git pull origin $BRANCH --quiet

# Sync main .env to project root
cp "$ENV_REPO/$ENV_FILE" "../$ENV_FILE"

# Sync services .env to each root
cp "$ENV_REPO/$USER_SERVICE_ROOT/$ENV_FILE" "../$USER_SERVICE_ROOT/$ENV_FILE"
cp "$ENV_REPO/$AUCTION_SERVICE_ROOT/$ENV_FILE" "../$AUCTION_SERVICE_ROOT/$ENV_FILE"
cp "$ENV_REPO/$API_GATEWAY_ROOT/$ENV_FILE" "../$API_GATEWAY_ROOT/$ENV_FILE"
cp "$ENV_REPO/$FRONTEND_ROOT/$ENV_FILE" "../$FRONTEND_ROOT/$ENV_FILE"

echo "✅ .env files updated successfully!"