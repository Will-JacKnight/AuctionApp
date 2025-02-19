import unittest
from flask import Flask
from mainPage import create_app  # Import the create_app function
from unittest.mock import patch


class TestMainPageAPI(unittest.TestCase):

    @patch('supabase_client.supabase')  # Mock supabase client
    def setUp(self, mock_supabase):
        """Setup the test client."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.mock_supabase = mock_supabase

    def test_search_item(self):
        """Test the /search route."""
        # Set up the mock data for Supabase
        self.mock_supabase.table.return_value.select.return_value.ilike.return_value.execute.return_value.data = [
            {"id": 1, "item_name": "Test Item 1", "price": 100},
            {"id": 2, "item_name": "Test Item 2", "price": 200},
        ]
        
        # Simulate a GET request to the search API with a keyword
        response = self.client.get('/search?keyword=Test')
        
        # Assert that the status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Assert that the response data contains the mocked items
        data = response.get_json()
        self.assertEqual(len(data), 2)  # Two items should be returned in this case

    def test_display_item(self):
        """Test the /display_mainPage route."""
        # Set up the mock data for Supabase
        self.mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"id": 1, "item_name": "Item 1", "price": 100},
            {"id": 2, "item_name": "Item 2", "price": 200},
            {"id": 3, "item_name": "Item 3", "price": 300},
        ]

        # Simulate a GET request to the display API
        response = self.client.get('/display_mainPage')
        
        # Assert that the status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Assert that the response data is a list (shuffled items)
        data = response.get_json()
        self.assertTrue(len(data) > 0)  # Check if items are returned

if __name__ == '__main__':
    unittest.main()