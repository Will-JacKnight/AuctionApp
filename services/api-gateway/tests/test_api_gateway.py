import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock
from flask_socketio import SocketIOTestClient
from flask_jwt_extended import create_access_token

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from app import app

@pytest.fixture
def client():
    """Create a test client for Flask"""
    app.config["TESTING"] = True
    client = app.test_client()
    return client

def test_login(client, mocker):
    """Test the login API"""
    mock_response = mocker.patch("requests.post")
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = {"message": "Login successful"}

    response = client.post("/login", json={"username": "test", "password": "1234"})

    assert response.status_code == 200
    assert response.get_json()["message"] == "Login successful"

def test_search(client, mocker):
    """Test the search API"""
    mock_response = mocker.patch("requests.post")
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = {"results": ["item1", "item2"]}

    response = client.post("/search", json={"query": "laptop"})

    assert response.status_code == 200
    assert response.get_json() == {"results": ["item1", "item2"]}


def test_product_details(client, mocker):
    """Test the product details API"""
    mock_response = mocker.patch("requests.get")
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = {"product": "Laptop", "price": 1000}

    response = client.get("/product/12345")

    assert response.status_code == 200
    assert response.get_json() == {"product": "Laptop", "price": 1000}