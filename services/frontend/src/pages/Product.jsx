import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./../styles/bidding.css";
import { io } from "socket.io-client"; 

// Define API URL based on environment variables
const API_URL =
  import.meta.env.VITE_RUN_MODE === "docker"
    // When running in Docker, we access the frontend via localhost from the browser (external access)
    ? import.meta.env.VITE_API_GATEWAY_LOCAL_URL
    : import.meta.env.VITE_RUN_MODE === "heroku"
    ? import.meta.env.VITE_API_GATEWAY_HEROKU_URL
    : import.meta.env.VITE_API_GATEWAY_LOCAL_URL;
    
// const SOCKET_URL = "http://127.0.0.1:4000";
// const SOCKET_URL = API_URL; 

function Product() {
//   // Extract auctionId from URL parameters
//   const { auctionId } = useParams();
 
//   // Default auction ID if none is provided
//   const defaultAuctionId = "test-auction";
//   const finalAuctionId = auctionId || defaultAuctionId;
 
  // State variables for auction data, bid price input, and error handling
  const [auctionData, setAuctionData] = useState(null); // Store auction details
  const [bidPrice, setBidPrice] = useState(""); // Store user's bid price
  const [error, setError] = useState(null); // Store any errors during API calls
 
  const { id } = useParams();
  console.log(id)

   // Fetch auction details when the component mounts or when auctionId changes
  useEffect(() => {
    async function fetchAuctionDetails() {
      try {
        // if (!finalAuctionId || finalAuctionId === "test-auction") {
        //   setAuctionData({
        //     name: "Midnight Classic Tee",
        //     description: "The Midnight Classic Tee is made from high-quality cotton, offering a soft, breathable, and comfortable fit. Its sleek black design makes it a versatile staple for any wardrobe. Perfect for casual outings or layering, this timeless tee ensures effortless style and all-day comfort.",
        //     image_url: "https://fyzhnlztyjbwdujmzwys.supabase.co/storage/v1/object/public/product_images/e9f13f02-a3a7-4144-89f0-32fb53fd129b.jpg",
        //     starting_price: 100000,
        //     current_price: 150000,
        //     start_time: "2025-02-25T12:00:00Z",
        //     end_time: "2025-02-28T12:00:00Z"
        //   });
        //   return;
        // }
        
       
        // Fetch auction details from the API
        const response = await fetch(`${API_URL}/search`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({"auction_id": id})
          })
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json(); // Parse response data as JSON
        console.log(data)
        setAuctionData(data); // Update state with fetched auction details
      } catch (err) {
        console.error("Error fetching auction details:", err);
        setError(err);
      }
    }
    fetchAuctionDetails(); // Call function when component is mounted
  }, []); // Re-run effect when auctionId changes
 
  useEffect(() => {
    const socket = io(API_URL, {
      transports: ["websocket"], // Ensure WebSocket is used
      reconnection: true, 
      reconnectionAttempts: 5,   // Retry before giving up
      timeout: 20000,            // Allow more time before failing
    });

    socket.on("connect", () => {
      console.log("✅ Connected to WebSocket server");
    });

    socket.on("disconnect", (reason) => {
      console.warn(" WebSocket disconnected. Reason:", reason);
    });

    socket.on("connect_error", (error) => {
      console.error("❌ WebSocket connection error:", error);
    });

    // Listen for bid updates
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


  
  // Function to handle bid submission
  const handleBidSubmit = async () => {
    // Validate bid amount
    if (!bidPrice || isNaN(bidPrice) || bidPrice <= auctionData.current_price) {
      alert("Invalid bid amount");
      return;
    }
    try {
      // Send bid request to API
      const response = await fetch(`${API_URL}/place_bid`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bidPrice: Number(bidPrice)}),
      });
      // Handle API response errors
      if (!response.ok) {
        console.log(response)
        console.log(bidPrice)
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
          <h3 className="bid-price">Current Price: ${auctionData.max_bid.toLocaleString()}</h3>
          <p>Bidding Start: {`${new Date(`${auctionData.start_date}T${auctionData.start_time}`).toLocaleDateString()} ${new Date(`${auctionData.start_date}T${auctionData.start_time}`).toLocaleTimeString()}`}</p>
          <p>Bidding End: {`${new Date(`${auctionData.end_date}T${auctionData.end_time}`).toLocaleDateString()} ${new Date(`${auctionData.end_date}T${auctionData.end_time}`).toLocaleTimeString()}`}</p>
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
