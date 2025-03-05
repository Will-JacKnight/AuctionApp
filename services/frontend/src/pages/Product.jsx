import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { io } from "socket.io-client";
import "./../styles/bidding.css";
import NavBar from "../components/NavBar";
import { useNavigate } from "react-router-dom";

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
  const navigate = useNavigate();

  useEffect(() => {
    if (!id) return;

    async function fetchAuctionDetails() {
      try {
        const response = await fetch(`${API_URL}/product/${id}`, { method: "GET"});
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data)

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
    const token = sessionStorage.getItem("token");
      console.log(token);
    if (!token) {
        // sessionStorage.setItem("lastVisited", location.pathname);
        alert("Please log in!");
        navigate("/login");
        return;
      }

    const now = new Date();
    const startTime = new Date(`${auctionData.start_date}T${auctionData.start_time}`);
    if (now < startTime) {
        alert("Bidding has not started yet. Please wait until the auction starts.");
        return;
    }

    if (!bidPrice || isNaN(bidPrice) || bidPrice <= auctionData.starting_price) {
      alert("Invalid bid amount");
      return;
    }
    try {
      const response = await fetch(`${API_URL}/place_bid`, {
        method: "POST",
        headers: { Authorization: `Bearer ${sessionStorage.getItem("token")}`,
                  "Content-Type": "application/json"},
        body: JSON.stringify({ bidPrice: Number(bidPrice), auctionId: id}),
      });

      if (!response.ok) {
        throw new Error("Failed to place bid");
      }
      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        throw new Error("Received non-JSON response. Check API response.");
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
    <>
      <NavBar />
      <div className="bidding-container">
        <div className="auction-info">

          <img src={auctionData[0].image_url} alt={auctionData[0].name} className="auction-image" />
        </div>

        <div className="bidding-section">
          <div className="product-details">
            <h2 className="product-name">{auctionData[0].name}</h2>
            <p className="product-description">{auctionData[0].description}</p>
          </div>

          <div className="price-date-container">
            <span className="price-date-info-text">Starting Price (£)</span>
            <span className="starting-price-placeholder">{auctionData[0].sarting_price}</span>
            <span className="price-date-info-text">Current Price (£)</span>
            <span className="current-price-placeholder">{auctionData[0].ax_bid?.toLocaleString() || auctionData[0].starting_price}</span>
            <span className="price-date-info-text">Bidding Start</span>
            <span className="bidding-date-placeholder">{`${new Date(`${auctionData[0].start_date}T${auctionData[0].start_time}`).toLocaleDateString()} ${new Date(`${auctionData.start_date}T${auctionData.start_time}`).toLocaleTimeString()}`}</span>
            <span className="price-date-info-text">Bidding End</span>
            <span className="bidding-date-placeholder">{`${new Date(`${auctionData[0].end_date}T${auctionData[0].end_time}`).toLocaleDateString()} ${new Date(`${auctionData.end_date}T${auctionData.end_time}`).toLocaleTimeString()}`}</span>
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
    </>
  );
}

export default Product;
