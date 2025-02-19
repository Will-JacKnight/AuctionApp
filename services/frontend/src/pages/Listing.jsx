import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./../styles/listing.css";

function AuctionUpload() {
    const [formData, setFormData] = useState({
      productName: "",
      productImage: null,
      tag: "electronics",
      description: "",
      startingPrice: "",
      auctionStartDate: "",
      auctionStartTime: "",
      auctionEndTime: "",
    });
  
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
  
    const tags = [
      "electronics", "furniture", "stationery", "clothing", "jewelry", "art", "books", "toys", "vehicles",
      "sports", "musical instruments", "antiques", "collectibles", "home decor", "kitchenware", "tools",
      "outdoor", "pet supplies", "gaming", "office supplies"
    ];
  
    const handleChange = (e) => {
      const { name, value } = e.target;
      setFormData((prev) => ({ ...prev, [name]: value }));
    };
  
    const handleFileChange = (e) => {
      setFormData((prev) => ({ ...prev, productImage: e.target.files[0] }));
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
      
      try {
        const formDataToSend = new FormData();
        Object.keys(formData).forEach((key) => {
          formDataToSend.append(key, formData[key]);
        });
        
        const response = await fetch("/api-gateway/upload-auction", {
          method: "POST",
          body: formDataToSend,
        });
        
        const data = await response.json();
        if (response.ok) {
          alert("Auction created successfully!");
          navigate("/");
        } else {
          setError(data.error || "Upload failed");
        }
      } catch (err) {
        setError("Network error. Please try again.");
      }
      setLoading(false);
    };
  
    return (
      <div className="auction-form-container">
        <h2>Create Auction</h2>
        {error && <p className="error-message">{error}</p>}
        <form onSubmit={handleSubmit}>
          <label>Product Name</label>
          <input
            type="text"
            name="name"
            placeholder="Product Name"
            value={formData.productName}
            onChange={handleChange}
            required
          />
          
          <label>Product Image</label>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            required
          />
          
          <label>Tag</label>
          <select name="catagory" value={formData.tag} onChange={handleChange} required>
            {tags.map((tag) => (
              <option key={tag} value={tag}>{tag}</option>
            ))}
          </select>
          
          <label>Product Description</label>
          <textarea
            name="description"
            placeholder="Product Description"
            value={formData.description}
            onChange={handleChange}
            required
          />
          
          <label>Starting Price (￡)</label>
          <input
            type="number"
            name="starting_price"
            placeholder="Starting Price (￡)"
            value={formData.startingPrice}
            onChange={handleChange}
            required
          />
          
          <label>Auction Start Date</label>
          <input
            type="date"
            name="start_date"
            value={formData.auctionStartDate}
            onChange={handleChange}
            required
          />
          
          <label>Auction Start Time</label>
          <input
            type="time"
            name="start_time"
            value={formData.auctionStartTime}
            onChange={handleChange}
            required
          />
          
          <label>Auction End Time</label>
          <input
            type="time"
            name="end_time"
            value={formData.auctionEndTime}
            onChange={handleChange}
            required
          />
          
          <button type="submit" disabled={loading}>
            {loading ? "Uploading..." : "Create Auction"}
          </button>
        </form>
      </div>
    );
  }
  
  export default AuctionUpload;
  