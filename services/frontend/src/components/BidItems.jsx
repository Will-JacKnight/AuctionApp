import "../styles/navBar.css"
import { useEffect, useState } from "react";
import OrderTable from "./OrdersTable";

const API_URL =
  import.meta.env.VITE_RUN_MODE === "docker"
    // When running in Docker, we access the frontend via localhost from the browser (external access)
    ? import.meta.env.VITE_API_GATEWAY_LOCAL_URL
    : import.meta.env.VITE_RUN_MODE === "heroku"
    ? import.meta.env.VITE_API_GATEWAY_HEROKU_URL
    : import.meta.env.VITE_API_GATEWAY_LOCAL_URL;
  
const Biddings = () => {
  const [biddings, setBiddings] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function getData() {
        try {
            setLoading(true)
          const response = await fetch(`${API_URL}/dashboard_bid`, {
            method: "GET",
            headers: { Authorization: `Bearer ${sessionStorage.getItem("token")}`, },
            })

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
          throw new Error("Received non-JSON response. Check API response.");
        }

        const data = await response.json();
        if(data.message  != "No bids found for this user") {
          const extracted_data = data.flatMap(obj => Object.values(obj).flat());
          setBiddings(extracted_data);
        }
        
      } catch (err) {
        console.log(`Following error occurred when fetching data: ${err}`)
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    getData();
  }, []);

  if (loading) {
    return (
      <div className="loading-state">
        <p>Loading your biddings...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-state">
        <p>Error: {error}</p>
      </div>
    );
  }

  return (
    <div>
      {biddings && <OrderTable data={biddings}/>}
    </div>
  );
};

export default Biddings;
