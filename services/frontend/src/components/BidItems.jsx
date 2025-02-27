import { useEffect, useState } from "react";
import OrderTable from "./OrdersTable";

const API_URL = import.meta.env.VITE_API_RUN_MODE === "docker"
  ? import.meta.env.VITE_API_DOCKER_API_URL
  : import.meta.env.VITE_API_LOCAL_API_URL;

// const getBiddingsData = () => [
//     { id: 1, item: "Laptop", amount: 450, time: "24/02/2025 10:30", status: "Active" },
//     { id: 1, item: "Laptop", amount: 500, time: "24/02/2025 12:30", status: "Active"},
//     { id: 1, item: "Laptop", amount: 550, time: "25/02/2025 15:37", status: "Sold"},

//     { id: 2, item: "Smartphone", amount: 250, time: "23/02/2025 09:20", status: "Active"},
//     { id: 2, item: "Smartphone", amount: 250, time: "24/02/2025 11:45", status: "Active"},
//     { id: 2, item: "Smartphone", amount: 250, time: "25/02/2025 16:51", status: "Sold"},
//   ];
  
const Biddings = () => {
  const [biddings, setBiddings] = useState([null]);
  const [error, setError] = useState()

  useEffect(() => {
    async function getData() {
        try {
          // const response = await fetch(("/api-gateway/display_mainPage", {
          const response = await fetch(`${API_URL}/dashboard_bid`, {
            method: "GET",
            // headers: { "Content-Type": "application/json" },
            })

            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }


            const contentType = response.headers.get("content-type");
            if (!contentType || !contentType.includes("application/json")) {
              throw new Error("Received non-JSON response. Check API response.");
            }
            const data = await response.json()
            const extracted_data = data.flatMap(obj => Object.values(obj).flat());

            setBiddings(extracted_data)

        }
        catch (err) {
            console.log(`Following error occured when fetching data: ${err}`)
            setError(err)
        }
    }
    getData()

  }, [])

  return (
    <div>
      <h3 className="text-lg font-semibold mb-2">Your Biddings</h3>
      {biddings && <OrderTable data={biddings}/>}
        
    </div>
  );
};

export default Biddings;
