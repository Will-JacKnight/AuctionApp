import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { io } from "socket.io-client";
import "./../styles/bidding.css"; 

const API_URL = 
  import.meta.env.VITE_RUN_MODE === "docker"
    ? import.meta.env.VITE_API_GATEWAY_LOCAL_URL
    : import.meta.env.VITE_RUN_MODE === "heroku"
    ? import.meta.env.VITE_API_GATEWAY_HEROKU_URL
    : import.meta.env.VITE_API_GATEWAY_LOCAL_URL;

function Product() {
  const { id } = useParams();
  const [auctionData, setAuctionData] = useState(null);
  const [bidPrice, setBidPrice] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    async function fetchAuctionDetails() {
      try {
        const response = await fetch(`${API_URL}/product/${id}`, { method: "GET" });
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setAuctionData(data);
      } catch (err) {
        console.error("Error fetching auction details:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchAuctionDetails();
  }, [id]);

  useEffect(() => {
    const socket = io(API_URL, {
      transports: ["websocket"],
      reconnection: true,
      reconnectionAttempts: 5,
      timeout: 20000,
    });

    socket.on("connect", () => console.log("✅ Connected to WebSocket server"));
    socket.on("disconnect", (reason) => console.warn("WebSocket disconnected:", reason));
    socket.on("connect_error", (error) => console.error("❌ WebSocket connection error:", error));

    socket.on("bid_update", (updatedBid) => {
      console.log("🔔 Received bid update:", updatedBid);
      setAuctionData((prevData) => ({
        ...prevData,
        max_bid: updatedBid.max_bid,
      }));
    });

    return () => {
      socket.off("bid_update");
      socket.disconnect();
    };
  }, []);

  const handleBidSubmit = async () => {
    if (!bidPrice || isNaN(bidPrice) || bidPrice <= auctionData.max_bid) {
      alert("Invalid bid amount");
      return;
    }
    try {
      const response = await fetch(`${API_URL}/place_bid`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bidPrice: Number(bidPrice), auctionId: id}),
      });

      if (!response.ok) {
        throw new Error("Failed to place bid");
      }

      alert("Bid placed successfully!");
      setBidPrice("");
    } catch (err) {
      console.error("Error placing bid:", err);
      alert("Failed to place bid");
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error loading auction details: {error}</p>;
  if (!auctionData) return <p>No auction data found</p>;

  return (
    <div className="bidding-container">
      <div className="auction-info">
        <img src={auctionData.image_url} alt={auctionData.name} className="auction-image" />
      </div>

      <div className="bidding-section">
        <div className="product-details">
          <h2 className="product-name">{auctionData.name}</h2>
          <p>{auctionData.description}</p>
        </div>

        <div className="price-date-container">
          <h3>Starting Price: ${auctionData.starting_price.toLocaleString()}</h3>
          <h3 className="bid-price">Current Price: ${auctionData.max_bid?.toLocaleString() || "N/A"}</h3>
          <p>Bidding Start: {new Date(auctionData.start_date).toLocaleString()}</p>
          <p>Bidding End: {new Date(auctionData.end_date).toLocaleString()}</p>
        </div>

        <div className="bid-input">
          <input
            type="number"
            value={bidPrice}
            onChange={(e) => setBidPrice(e.target.value)}
            placeholder="Enter your bid..."
          />
          <button onClick={handleBidSubmit}>Place Bid</button>
        </div>
      </div>
    </div>
  );
}

export default Product;
