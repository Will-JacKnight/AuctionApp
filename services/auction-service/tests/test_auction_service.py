import sys
import os
from unittest.mock import patch, MagicMock
import unittest
from flask import Flask
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))
from app import app  # Import the Flask app instance
import io


class TestMainPageAPI(unittest.TestCase):

    def setUp(self):
        """Setup the test client."""
        self.app = app
        self.client = self.app.test_client()

    @patch('mainPage.supabase')  # Patch where Flask is actually using supabase
    def test_search_item(self, mock_supabase):  # Pass the mock as an argument
        """Test the /search route."""
        
        mock_supabase.table.return_value.select.return_value.ilike.return_value.execute.return_value.data = [
            {"id": 1, "item_name": "Item 1", "price": 100, "end_date": "2025-03-10", "end_time": "12:00:00"},
            {"id": 2, "item_name": "Item 2", "price": 200, "end_date": "2025-03-11", "end_time": "15:30:00"},
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
            {"id": 1, "item_name": "Item 1", "price": 100, "end_date": "2025-03-10", "end_time": "12:00:00"},
            {"id": 2, "item_name": "Item 2", "price": 200, "end_date": "2025-03-11", "end_time": "15:30:00"},
            {"id": 3, "item_name": "Item 3", "price": 300, "end_date": "2025-03-12", "end_time": "18:45:00"},
        ]

        # Simulate a GET request to the display API
        response = self.client.get('/display_mainPage')
        
        # Assert that the status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Assert that the response data is a list (shuffled items)
        data = response.get_json()
        self.assertTrue(len(data) > 0)  # Check if items are returned
    

class TestListingPageAPI(unittest.TestCase):

    def setUp(self):
        """Setup the test client."""
        self.app = app
        self.client = self.app.test_client()

    @patch('listingPage.supabase')  # Patch Supabase in the listingPage module
    def test_create_listing(self, mock_supabase):
        """Test the /listing POST route."""
        
        # Mock Supabase table insert response
        mock_insert_response = MagicMock()
        mock_insert_response.execute.return_value.data = [{"id": 123}]
        
        mock_supabase.table.return_value.insert.return_value.execute = mock_insert_response.execute

        # Simulate a POST request to create a new listing
        payload = {
            "name": "Test Item",
            "category": "electronics",
            "description": "A test item for auction",
            "starting_price": 50,
            "start_date": "2025-05-01",
            "start_time": "09:00",
            "end_date": "2025-05-02",
            "end_time": "10:00",
            "image_url": "http://someexample.com"
        }
        response = self.client.post('/listing', data=payload, content_type='multipart/form-data')

        # Assert response
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        print("Mocked response:", data)
        self.assertEqual(data["item_id"], 123)  # Should match the mocked ID

    @patch('listingPage.supabase')  # Mock Supabase
    def test_create_listing_with_image(self, mock_supabase):
        """ Testing listing POST request with jpg file"""

        # Mock Supabase Storage upload
        mock_supabase.storage.from_.return_value.upload.return_value = True
        
        # Mock Supabase table insert
        mock_insert_response = MagicMock()
        mock_insert_response.execute.return_value.data = [{"id": 456}]
        mock_supabase.table.return_value.insert.return_value.execute = mock_insert_response.execute

        payload = {
            "name": "Test Item with Image",
            "category": "electronics",
            "description": "A test item for auction with image",
            "starting_price": "100",
            "start_date": "2025-06-01",
            "start_time": "12:00",
            "end_date": "2025-06-02",
            "end_time": "13:00"
        }

        # Simulate image upload
        image = (io.BytesIO(b"fake image data"), "test-image.jpg")

        # Send request
        response = self.client.post('/listing', data={**payload, "productImage": image}, content_type='multipart/form-data')

        # Validate respond
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        print("Mocked response with image:", data)
        self.assertEqual(data["item_id"], 456)
        self.assertIn("image_url", data) 

class TestDashboardPageAPI(unittest.TestCase):

    def setUp(self):
        """Setup the test client."""
        self.app = app
        self.client = self.app.test_client()

    @patch('dashboard.supabase')  # Patch Supabase in the listingPage module
    def test_dashboard_sell(self, mock_supabase):
        """Test the /dashboard_sell POST route."""
        

        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
             {
                "username": "test_user",
                "items": [
                    {
                        "description": "This is a test item for debugging",
                        "id": "abc-123",
                        "image_url": "http://example.com",
                        "max_bid": 10,
                        "name": "test_item1"
                    },
                    {
                        "description": "This is collegedropout bear",
                        "id": "def-456",
                        "image_url": "http://graduation.com",
                        "max_bid": 100,
                        "name": "collegedropout bear"
                    }
                ]
            }
        ]

         # Simulate a GET request to the display API
        response = self.client.get('/dashboard_sell')
        
        # Assert that the status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Assert that the response data is a list (shuffled items)
        data = response.get_json()
        self.assertIn("username", data)  # Ensure username key exists
        self.assertIn("items", data)  # Ensure items key exists
        self.assertIsInstance(data["items"], list)  # Ensure items is a list
        self.assertTrue(len(data) > 0)  # Check if items are returned
    



    # @patch('dashboard.supabase')  # Patch Supabase in the listingPage module
    # def test_dashboard_bid(self, mock_supabase):
    #     """Test the /dashboard_bid POST route."""
        

    #     mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
    #          {
    #             "username": "test_user",
    #             "items": [
    #                 {
    #                     "description": "This is a test item for debugging",
    #                     "id": "abc-123",
    #                     "image_url": "http://example.com",
    #                     "max_bid": 10,
    #                     "name": "test_item1"
    #                 },
    #                 {
    #                     "description": "This is collegedropout bear",
    #                     "id": "def-456",
    #                     "image_url": "http://graduation.com",
    #                     "max_bid": 100,
    #                     "name": "collegedropout bear"
    #                 }
    #             ]
    #         }
    #     ]

    #      # Simulate a GET request to the display API
    #     response = self.client.get('/dashboard_bid')
        
    #     # Assert that the status code is 200
    #     self.assertEqual(response.status_code, 200)
        
    #     # Assert that the response data is a list (shuffled items)
    #     data = response.get_json()
    #     self.assertIn("username", data)  # Ensure username key exists
    #     self.assertIn("items", data)  # Ensure items key exists
    #     self.assertIsInstance(data["items"], list)  # Ensure items is a list
    #     self.assertTrue(len(data) > 0)  # Check if items are returned

if __name__ == '__main__':
    unittest.main()