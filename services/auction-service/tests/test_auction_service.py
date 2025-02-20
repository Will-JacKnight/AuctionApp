from unittest.mock import patch, MagicMock
import unittest
from flask import Flask
from app import app  # Import the Flask app instance


class TestMainPageAPI(unittest.TestCase):

    def setUp(self):
        """Setup the test client."""
        self.app = app
        self.client = self.app.test_client()

    @patch('mainPage.supabase')  # Patch where Flask is actually using supabase
    def test_search_item(self, mock_supabase):  # Pass the mock as an argument
        """Test the /search route."""
        
        mock_supabase.table.return_value.select.return_value.ilike.return_value.execute.return_value.data = [
            {"id": 1, "name": "Test Item 1", "price": 100},
            {"id": 2, "name": "Test Item 2", "price": 200},
        ]

        # Simulate a POST request
        payload = {"keyword": "Test"}
        response = self.client.post('/search', json=payload)

        # Assert response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        print("Mocked data:", data)
        self.assertEqual(len(data), 2)  # Should return only mocked data

    @patch('mainPage.supabase')  # Patch where Flask is actually using supabase
    def test_display_item(self, mock_supabase):  # Pass the mock as an argument
        """Test the /display_mainPage route."""
        # Set up the mock data for Supabase
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
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
    

# class TestListingPageAPI(unittest.TestCase):

#     def setUp(self):
#         """Setup the test client."""
#         self.app = app
#         self.client = self.app.test_client()

#     @patch('listingPage.supabase')  # Patch Supabase in the listingPage module
#     def test_create_listing(self, mock_supabase):
#         """Test the /listing POST route."""
        
#         # Mock Supabase table insert response
#         mock_insert_response = MagicMock()
#         mock_insert_response.execute.return_value.data = [{"id": 123}]
        
#         mock_supabase.table.return_value.insert.return_value.execute = mock_insert_response.execute

#         # Simulate a POST request to create a new listing
#         payload = {
#             "name": "Test Item",
#             "category": "electronics",
#             "description": "A test item for auction",
#             "starting_price": 50,
#             "start_date": "2025-05-01",
#             "start_time": "09:00",
#             "end_date": "2025-05-02",
#             "end_time": "10:00",
#             "image_url": "http://someexample.com"
#         }
#         response = self.client.post('/listing', data=payload, content_type='multipart/form-data')

#         # Assert response
#         self.assertEqual(response.status_code, 201)
#         data = response.get_json()
#         print("Mocked response:", data)
#         self.assertEqual(data["item_id"], 123)  # Should match the mocked ID

if __name__ == '__main__':
    unittest.main()