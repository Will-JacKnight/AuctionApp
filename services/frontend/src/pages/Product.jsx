import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./../styles/bidding.css";

const API_URL = import.meta.env.VITE_API_RUN_MODE === "docker"
  ? import.meta.env.VITE_API_DOCKER_API_URL
  : import.meta.env.VITE_API_LOCAL_API_URL;

function Product() {
  const { auctionId } = useParams();
  const defaultAuctionId = "test-auction";
  const finalAuctionId = auctionId || defaultAuctionId;

  const [auctionData, setAuctionData] = useState(null);
  const [bidPrice, setBidPrice] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchAuctionDetails() {
      try {
        if (!finalAuctionId || finalAuctionId === "test-auction") {
          setAuctionData({
            name: "Midnight Classic Tee",
            description: "The Midnight Classic Tee is made from high-quality cotton, offering a soft, breathable, and comfortable fit. Its sleek black design makes it a versatile staple for any wardrobe. Perfect for casual outings or layering, this timeless tee ensures effortless style and all-day comfort.",
            image_url: "https://fyzhnlztyjbwdujmzwys.supabase.co/storage/v1/object/public/product_images/e9f13f02-a3a7-4144-89f0-32fb53fd129b.jpg",
            starting_price: 100000,
            current_price: 150000,
            start_time: "2025-02-25T12:00:00Z",
            end_time: "2025-02-28T12:00:00Z"
          });
          return;
        }

        const response = await fetch(`${API_URL}/auction/${finalAuctionId}`);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setAuctionData(data);
      } catch (err) {
        console.error("Error fetching auction details:", err);
        setError(err);
      }
    }
    fetchAuctionDetails();
  }, [finalAuctionId]);

  const handleBidSubmit = async () => {
    if (!bidPrice || isNaN(bidPrice) || bidPrice <= auctionData.current_price) {
      alert("Invalid bid amount");
      return;
    }
    try {
      const response = await fetch(`${API_URL}/place_bid`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ auctionId: finalAuctionId, bidPrice }),
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

  if (error) return <p>Error loading auction details</p>;
  if (!auctionData) return <p>Loading...</p>;

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
  
        {/* Wrap price and date section inside a container */}
        <div className="price-date-container">
          <h3>Starting Price: ${auctionData.starting_price.toLocaleString()}</h3>
          <h3 className="bid-price">Current Price: ${auctionData.current_price.toLocaleString()}</h3>
          <p>Bidding Start: {new Date(auctionData.start_time).toLocaleString()}</p>
          <p>Bidding End: {new Date(auctionData.end_time).toLocaleString()}</p>
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
