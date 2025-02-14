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

### Local Docker-compose Test
`docker-compose up --build`
