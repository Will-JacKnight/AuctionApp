import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./../styles/listing.css";

function AuctionUpload() {
  const [formData, setFormData] = useState({
    name: "",
    // productImage: null,
    category: "electronics",
    description: "",
    starting_price: "",
    start_date: "",
    start_time: "",
    end_date: "",
    end_time: "",
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

  /*
  const handleFileChange = (e) => {
    setFormData((prev) => ({ ...prev, productImage: e.target.files[0] }));
  };
  */

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
        const response = await fetch("/api-gateway/listing", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
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
        {/* Product Name */}
        <label>Product Name</label>
        <input
          type="text"
          name="name"
          placeholder="Product Name"
          value={formData.name}
          onChange={handleChange}
          required
        />

        {/* 
        <label>Product Image</label>
        <input
          type="file"
          name="image"
          accept="image/*"
          onChange={handleFileChange}
          required
        />
        */}

        {/* Tag (category) */}
        <label>Tag</label>
        <select
          name="category"
          value={formData.category}
          onChange={handleChange}
          required
        >
          {tags.map((tag) => (
            <option key={tag} value={tag}>{tag}</option>
          ))}
        </select>

        {/* Product Description */}
        <label>Product Description</label>
        <textarea
          name="description"
          placeholder="Product Description"
          value={formData.description}
          onChange={handleChange}
          required
        />

        {/* Starting Price */}
        <label>Starting Price (￡)</label>
        <input
          type="number"
          name="starting_price"
          placeholder="Starting Price (￡)"
          value={formData.starting_price}
          onChange={handleChange}
          required
        />

        {/* Auction Start Date */}
        <label>Auction Start Date</label>
        <input
          type="date"
          name="start_date"
          value={formData.start_date}
          onChange={handleChange}
          required
        />

        {/* Auction Start Time */}
        <label>Auction Start Time</label>
        <input
          type="time"
          name="start_time"
          value={formData.start_time}
          onChange={handleChange}
          required
        />

        {/* Auction End Date */}
        <label>Auction End Date</label>
        <input
          type="date"
          name="end_date"
          value={formData.end_date}
          onChange={handleChange}
          required
        />

        {/* Auction End Time */}
        <label>Auction End Time</label>
        <input
          type="time"
          name="end_time"
          value={formData.end_time}
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
