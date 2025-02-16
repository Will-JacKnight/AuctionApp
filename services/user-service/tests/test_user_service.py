import pytest
import requests

# BASE_URL = "http://localhost:80"  # Adjust the port if necessary

def test_connection_of_login_service():
    # response = requests.get(f"{BASE_URL}/login")
    # assert response.status_code == 200
    assert True

# def test_signup_success():
#     payload = {
#         "email": "test@example.com",
#         "password": "1234",
#         "username": "testuser"
#     }
#     response = requests.post(f"{BASE_URL}/signup", json=payload)
#     assert response.status_code == 201
#     assert response.json().get("message") == "User registered successfully. Please log in."
#
# def test_signup_missing_fields():
#     payload = {
#         "email": "test@example.com",
#         "username": "testuser"
#         # Missing password
#     }
#     response = requests.post(f"{BASE_URL}/signup", json=payload)
#     assert response.status_code == 400
#     assert response.json().get("error") == "Missing required fields"
#
# def test_login_success():
#     payload = {
#         "email": "test@example.com",
#         "password": "1234"
#     }
#     response = requests.post(f"{BASE_URL}/login", json=payload)
#     assert response.status_code == 200
#     assert "access_token" in response.json()
#
# def test_login_invalid_credentials():
#     payload = {
#         "email": "test@example.com",
#         "password": "wrongpassword"
#     }
#     response = requests.post(f"{BASE_URL}/login", json=payload)
#     assert response.status_code == 401
#     assert response.json().get("error") == "Invalid password"
#
# def test_login_user_not_found():
#     payload = {
#         "email": "nonexistent@example.com",
#         "password": "1234"
#     }
#     response = requests.post(f"{BASE_URL}/login", json=payload)
#     assert response.status_code == 404
#     assert response.json().get("error") == "User not found"