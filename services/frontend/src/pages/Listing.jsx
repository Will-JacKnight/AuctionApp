import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./../styles/listing.css";
import NavBar from "../components/NavBar";
// import { getApiUrl } from '../config';

function AuctionUpload() {
  const [formData, setFormData] = useState({
    name: "",
    category: "electronics",
    description: "",
    starting_price: "",
    start_date: "",
    start_time: "",
    end_date: "",
    end_time: "",
  });

  const [image, setImage] = useState(null);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const API_URL =
    import.meta.env.VITE_RUN_MODE === "docker"
      ? import.meta.env.VITE_API_GATEWAY_LOCAL_URL
      : import.meta.env.VITE_RUN_MODE === "heroku"
      ? import.meta.env.VITE_API_GATEWAY_HEROKU_URL
      : import.meta.env.VITE_API_GATEWAY_LOCAL_URL;

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
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        setError("Image size should be less than 5MB");
        return;
      }
      if (!file.type.startsWith('image/')) {
        setError("Please upload an image file");
        return;
      }
      setImage(file);
      setError("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const formDataToSend = new FormData();
      Object.keys(formData).forEach((key) => {
        formDataToSend.append(key, formData[key]);
      });
      if (image) {
        formDataToSend.append("productImage", image);
      }

      const response = await fetch(`${API_URL}/listing`, {
        method: "POST",
        body: formDataToSend
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
    <>
      <NavBar />
      <div className="auction-form-container">
        <h2>Create New Auction</h2>
        {error && <p className="error-message">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-section">
            <label>Product Name</label>
            <input
              type="text"
              name="name"
              placeholder="Enter product name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-section">
            <label>Product Image</label>
            <input
              type="file"
              name="productImage"
              accept="image/*"
              onChange={handleFileChange}
              required
            />
            <small className="help-text">Upload a clear image of your product (max 5MB)</small>
          </div>

          <div className="form-section">
            <label>Category</label>
            <select
              name="category"
              value={formData.category}
              onChange={handleChange}
              required
            >
              {tags.map((tag) => (
                <option key={tag} value={tag}>{tag.charAt(0).toUpperCase() + tag.slice(1)}</option>
              ))}
            </select>
          </div>

          <div className="form-section">
            <label>Product Description</label>
            <textarea
              name="description"
              placeholder="Describe your product in detail..."
              value={formData.description}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-section">
            <label>Starting Price (£)</label>
            <input
              type="number"
              name="starting_price"
              placeholder="Enter starting price"
              value={formData.starting_price}
              onChange={handleChange}
              min="0"
              step="0.01"
              required
            />
          </div>

          <div className="form-section">
            <label>Auction Start</label>
            <div className="date-time-inputs">
              <input
                type="date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                required
              />
              <input
                type="time"
                name="start_time"
                value={formData.start_time}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-section">
            <label>Auction End</label>
            <div className="date-time-inputs">
              <input
                type="date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
                required
              />
              <input
                type="time"
                name="end_time"
                value={formData.end_time}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? "Creating Auction..." : "Create Auction"}
          </button>
        </form>
      </div>
    </>
  );
}

export default AuctionUpload;
