# import pytest
# import json
# from unittest.mock import patch, MagicMock
# from api_gateway import app
# from flask_socketio import SocketIOTestClient
# from flask_jwt_extended import create_access_token

# @pytest.fixture
# def client():
#     """Setup Flask test client."""
#     app.config["TESTING"] = True
#     with app.test_client() as client:
#         yield client

# @pytest.fixture
# def mock_supabase():
#     """Mock Supabase client to prevent real database interaction."""
#     with patch("api_gateway.supabase") as mock_db:
#         yield mock_db