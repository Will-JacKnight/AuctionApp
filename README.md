# Project Structure

```
auction-app/
│  
├── services/  
│ ├── user-service/        # Manages users & auth  
│ │ ├── app.py             # Main application file for user service  
│ │ ├── requirements.txt   # Python dependencies for user service  
│ │ └── Dockerfile         # Dockerfile for building the user service image  
│ │  
│ ├── auction-service/     # Handles auctions & bidding  
│ │ ├── app.py             # Main application file for auction service  
│ │ ├── requirements.txt   # Python dependencies for auction service  
│ │ └── Dockerfile         # Dockerfile for building the auction service image  
│ │  
│ ├── api-gateway/         # Routes requests to the correct service  
│ │ ├── app.py             # Main application file for API gateway  
│ │ ├── requirements.txt   # Python dependencies for API gateway  
│ │ └── Dockerfile         # Dockerfile for building the API gateway image  
│ │  
│ └── frontend/            # Frontend application  
│   ├── src/               # Source code for the frontend  
│   │ ├── pages/           # React components for different pages  
│   │ ├── components/      # Reusable React components  
│   │ ├── styles/          # CSS styles  
│   │ └── App.jsx          # Main React application file  
│   ├──  package.json      # Node.js dependencies for frontend  
│   ├──  vite.config.js    # Vite configuration file  
│   └──  Dockerfile        # Dockerfile for building the frontend image  
│
├── .env-repo/ # Private environment variables repository
├── .github/               # GitHub Actions for CI/CD  
│ └── workflows/           # GitHub Actions workflows  
│ └── heroku-deploy.yml    # Workflow for deploying to Heroku  
│  
├── docker-compose.yml         # Docker Compose configuration for production  
├── docker-compose-local.yml   # Docker Compose configuration for local development  
├── docker-compose-test.yml    # Docker Compose configuration for running tests  
└── README.md                  # Project documentation
```

## Local Test Commands

### Local Docker-compose Build (test only)

#### builds with .env in root by default
```
docker compose -f docker-compose-local.yml up -d --build
```

### Local Unit Tests
```
docker compose -f docker-compose-local.yml -f docker-compose-test.yml up
```

### Local - Shut down all services
```
docker compose -f docker-compose-local.yml down -v
```

## Heroku Deployment Commands

### Run shell in Heroku
```
heroku run sh -a <HEROKU_APP_NAME>
```

### Heroku app release
```
heroku container:release web -a <HEROKU_APP_NAME>
```

### set app stack as container
```
heroku stack:set container -a <HEROKU_APP_NAME>
```

## Project .env management

To keep updated with the latest .env, you should ask for permission to the private .env-repo and have it savely cloned
in the project root as `./.env-repo`. This step is only needed for the first time.

To get the latest .env, just run the script:
```
sync-env.sh
```
in the project root. Voilà! All .env files are synced.

Similarly, to update the env-repo with the latest local .env, run the following:
```
upload-env.sh
```
