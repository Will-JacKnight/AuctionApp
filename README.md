The repo structure is as follows:

auction-app/
│── services/
│   │── user-service/        # Manages users & auth
│   │   │── app.py
│   │   │── requirements.txt
│   │── auction-service/     # Handles auctions & bidding
│   │   │── app.py
│   │   │── requirements.txt
│   │── payment-service/     # Manages payments
│   │── notification-service/ # Sends notifications
│
│── api-gateway/             # Routes requests to the correct service
│   │── app.py
│
│── frontend/                # React frontend
│   │── src/
│
│── .github/                 # GitHub Actions for CI/CD
│── docker-compose.yml       # Local setup for all services
│── README.md