# Project Structure

**auction-app/**  
│  
├── **services/**  
│   ├── **user-service/**        # Manages users & auth  
│   │   ├── `app.py`  
│   │   ├── `requirements.txt`  
│   │   └── `Dockerfile`  
│   │  
│   └── **auction-service/**     # Handles auctions & bidding  
│       ├── `app.py`  
│       └── `requirements.txt`  
│  
├── **api-gateway/**             # Routes requests to the correct service  
│   ├── `app.py`  
│   ├── `requirements.txt`  
│   └── `Dockerfile`  
│  
├── **.github/**                 # GitHub Actions for CI/CD  
├── `docker-compose.yml`       # Local setup for all services  
└── `README.md`

## Local Test
### Local Docker-compose Build (test only)
#### builds with .env in root by default
`docker compose -f docker-compose-local.yml up -d --build`

### Local Docker-compose Test
`docker compose -f docker-compose-local.yml -f docker-compose-test.yml up --abort-on-container-exit`

### Local - Shut down all services
`docker compose -f docker-compose-local.yml down -v`


## Heroku Deployment
### Run shell in Heroku
`heroku run sh -a auction-app-sse`

### Heroku app release
`heroku container:release frontend api-gateway user-service auction-service -a auction-app-sse`
