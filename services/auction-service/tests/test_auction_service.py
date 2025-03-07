import sys
import os
import io
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import app  # Import the Flask app instance
from flask_jwt_extended import create_access_token, JWTManager

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))

# Configure JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Change this to a strong secret
jwt = JWTManager(app)

###############################
#       Test Main Page       #
###############################

class TestMainPageAPI(unittest.TestCase):

    def setUp(self):
        """Setup the test client."""
        self.app = app
        self.client = self.app.test_client()

    @patch('mainPage.supabase')  # Patch where Flask is actually using supabase
    def test_search_item(self, mock_supabase):  # Pass the mock as an argument
        """Test the /search route."""
        
        mock_supabase.table.return_value.select.return_value.ilike.return_value.execute.return_value.data = [
            {"id": 1, "name": "Item 1", "price": 100, "end_date": "2025-03-10", "end_time": "12:00:00"},
            {"id": 2, "name": "Item 2", "price": 200, "end_date": "2025-03-11", "end_time": "15:30:00"},
        ]

        # Simulate a POST request
        payload = {"keyword": "bear"}
        response = self.client.post('/search', json=payload)

        # Assert response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        print("Mocked data:", data)
        self.assertEqual(len(data), 2)  # Should return only mocked data
        self.assertEqual(data[0]["name"], "Item 1")  # Check if the name matches the mocked data

    @patch('mainPage.supabase')  # Patch where Flask is actually using supabase
    def test_display_item(self, mock_supabase):  # Pass the mock as an argument
        """Test the /display_mainPage route."""
        # Set up the mock data for Supabase
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"id": 1, "name": "Item 1", "starting_price": 100, "end_date": "2025-03-10", "end_time": "12:00", "max_bid": 150, "remaining_days": 1, "image_url": "http://someexample1.com"},
            {"id": 2, "name": "Item 2", "starting_price": 200, "end_date": "2025-03-11", "end_time": "15:30", "max_bid": 250, "remaining_days": 2, "image_url": "http://someexample2.com"},
            {"id": 3, "name": "Item 3", "starting_price": 300, "end_date": "2025-03-12", "end_time": "18:45", "max_bid": 350, "remaining_days": 0, "image_url": "http://someexample3.com"}
        ]

        # Simulate a GET request to the display API
        response = self.client.get('/display_mainPage')
        
        # Assert that the status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Assert that the response data is a list (shuffled items)
        data = response.get_json()
        self.assertTrue(len(data) > 0)  # Check if items are returned
    
###############################
#     Test Listing Page      #
###############################

class TestListingPageAPI(unittest.TestCase):

    def setUp(self):
        """Setup the test client."""
        self.app = app
        self.app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()  # Create an application context
        self.app_context.push()  # Push the context

    def tearDown(self):
        """Remove the Flask app context after each test."""
        self.app_context.pop()  # Pop the context to clean up

    @patch('listingPage.supabase')  # Patch Supabase in the listingPage module
    def test_create_listing(self, mock_supabase):
        """Test the /listing POST route."""
        with self.app.app_context():
            test_token = create_access_token(identity="test_seller_id")  # Mock a seller ID
        auth_header = {
        "Authorization": f"Bearer {test_token}",
        "Content-Type": "application/json",  # Explicitly set Content-Type
        }
        
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
        response = self.client.post('/listing', data=payload, content_type='multipart/form-data', headers=auth_header)

        # Assert response
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        print("Mocked response:", data)
        self.assertEqual(data["item_id"], 123)  # Should match the mocked ID

    @patch('listingPage.supabase')  # Mock Supabase
    def test_create_listing_with_image(self, mock_supabase):
        """ Testing listing POST request with jpg file"""
        with self.app.app_context():
            test_token = create_access_token(identity="test_seller_id")  # Mock a seller ID
        auth_header = {
        "Authorization": f"Bearer {test_token}",
        "Content-Type": "application/json",  # Explicitly set Content-Type
        }

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
        response = self.client.post('/listing', data={**payload, "productImage": image}, content_type='multipart/form-data', headers=auth_header)

        # Validate respond
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        print("Mocked response with image:", data)
        self.assertEqual(data["item_id"], 456)
        self.assertIn("image_url", data) 

###############################
#     Test Dashboard Page    #
###############################

class TestDashboardPageAPI(unittest.TestCase):

    def setUp(self):
        """Setup the test client."""
        self.app = app
        self.app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()  # Create an application context
        self.app_context.push()  # Push the context

    def tearDown(self):
        """Remove the Flask app context after each test."""
        self.app_context.pop()  # Pop the context to clean up

    @patch('dashboard.supabase')  # Patch where supabase is actually imported
    def test_dashboard_bid(self, mock_supabase):
        """Test the /dashboard_bid GET API with mock Supabase RPC."""

        with self.app.app_context():
            test_token = create_access_token(identity="test_user_id")  # Mock user ID

        auth_header = {
            "Authorization": f"Bearer {test_token}",
            "Content-Type": "application/json", 
        }

        mock_rpc_response = MagicMock()
        mock_rpc_response.execute.return_value.data = [
            {
                "auction_name": "Test Item",
                "bid_amount": 5000,
                "created_at": "2025-03-04T10:30:00Z",
                "status": "active",
                "max_bid": 7000,
                "product_id" : 123
            },
            {
                "auction_name": "Test Item",
                "bid_amount": 6000,
                "created_at": "2025-03-04T11:00:00Z",
                "status": "active",
                "max_bid": 7000,
                "product_id" : 456
            },
            {
                "auction_name": "Danny",
                "bid_amount": 15000,
                "created_at": "2025-03-04T13:40:00Z",
                "status": "active",
                "max_bid": 16700,
                "product_id" : 321
            },
            {
                "auction_name": "Danny",
                "bid_amount": 16000,
                "created_at": "2025-03-04T13:50:00Z",
                "status": "active",
                "max_bid": 16700,
                "product_id" : 455
            }
        ]

        mock_supabase.rpc.return_value = mock_rpc_response

        response = self.client.get('/dashboard_bid', headers=auth_header)

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, list)

        self.assertIn("Test Item", data[0])
        self.assertIn("Danny", data[1])
        
    @patch('dashboard.supabase')  # Patch Supabase
    def test_dashboard_sell(self, mock_supabase):
        """Test the /dashboard_sell GET route with SQL RPC and JWT authentication."""

        with self.app.app_context():
            test_token = create_access_token(identity="test_seller_id")  # Mock seller ID

        auth_header = {
            "Authorization": f"Bearer {test_token}",
            "Content-Type": "application/json",  # Explicitly set Content-Type
        }

        # Mock Supabase response for username retrieval
        # mock_username_response = MagicMock()
        # mock_username_response.execute.return_value.data = [{"username": "test_seller"}]
        # mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_username_response

        # Mock Supabase RPC response for seller's auctions
        mock_rpc_response = MagicMock()
        mock_rpc_response.execute.return_value.data = [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "name": "Vintage Watch",
                "description": "A classic timepiece from the 80s.",
                "image_url": "http://example.com/vintage_watch.jpg",
                "status": "active",
                "max_bid": 1200
            },
            {
                "id": "22222222-2222-2222-2222-222222222222",
                "name": "Signed Football",
                "description": "Football signed by a legendary player.",
                "image_url": "http://example.com/signed_football.jpg",
                "status": "active",
                "max_bid": None  # Ensure None works correctly
            },
            {
                "id": "33333333-3333-3333-3333-333333333333",
                "name": "Antique Painting",
                "description": "A rare 19th-century painting.",
                "image_url": "http://example.com/antique_painting.jpg",
                "status": "expired",
                "max_bid": 5000
            }
        ]
        mock_supabase.rpc.return_value = mock_rpc_response

        # Send request
        response = self.client.get('/dashboard_sell', headers=auth_header)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Validate JSON response
        data = response.get_json()
        self.assertIsInstance(data, list)

        # # Ensure username is correctly returned
        # self.assertEqual(data["username"], [{"username": "test_seller"}])


        self.assertEqual(len(data), 3)  # Ensure 3 items are returned

        # Validate first auction item (Vintage Watch)
        self.assertEqual(data[0]["id"], "11111111-1111-1111-1111-111111111111")
        self.assertEqual(data[0]["name"], "Vintage Watch")
        self.assertEqual(data[0]["max_bid"], 1200)

        # Validate second auction item (Signed Football)
        self.assertEqual(data[1]["id"], "22222222-2222-2222-2222-222222222222")
        self.assertEqual(data[1]["name"], "Signed Football")
        self.assertIsNone(data[1]["max_bid"])  # Ensure max_bid is None when no bids exist

        # Validate third auction item (Antique Painting)
        self.assertEqual(data[2]["id"], "33333333-3333-3333-3333-333333333333")
        self.assertEqual(data[2]["name"], "Antique Painting")
        self.assertEqual(data[2]["max_bid"], 5000.00)
