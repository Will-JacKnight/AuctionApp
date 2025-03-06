import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from flask import json
from app import app

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))

class TestUserLogin(unittest.TestCase):

    def setUp(self):
        """Setup the test client."""
        self.app = app.test_client()
        self.headers = {"Content-Type": "application/json"}

    @patch("app.supabase")
    def test_invalid_password(self, mock_supabase):
        mock_user = {
            "id": 1,
            "password": "$2b$12$e7i5k6W5aT36uZAcXOTYMeWiO3JX8N5eX6cOSXzW5OjU2xYFNffP6",  # bcrypt hash
            "username": "testuser"
        }

        mock_response = MagicMock()
        mock_response.data = [mock_user]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        payload = json.dumps({"email": "test@example.com", "password": "wrongpassword"})
        response = self.app.post("/login", data=payload, headers=self.headers)

        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Invalid password")

    @patch("app.supabase")
    def test_user_not_found(self, mock_supabase):
        mock_response = MagicMock()
        mock_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        payload = json.dumps({"email": "nonexistent@example.com", "password": "password123"})
        response = self.app.post("/login", data=payload, headers=self.headers)

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "User not found")

if __name__ == '__main__':
    unittest.main()