import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";

const API_URL =
  import.meta.env.VITE_RUN_MODE === "docker"
    // When running in Docker, we access the frontend via localhost from the browser (external access)
    ? import.meta.env.VITE_API_GATEWAY_LOCAL_URL
    : import.meta.env.VITE_RUN_MODE === "heroku"
    ? import.meta.env.VITE_API_GATEWAY_HEROKU_URL
    : import.meta.env.VITE_API_GATEWAY_LOCAL_URL;


const Sales = () => {
  const [sales, setSales] = useState([])
  const [error, setError] = useState()


  useEffect(() => {
    async function getData() {
        try {
          console.log(sessionStorage.getItem("token"))
          const response = await fetch(`${API_URL}/dashboard_sell`, {
            method: "GET",
            headers: {
              Authorization: `Bearer ${sessionStorage.getItem("token")}`,
            },
          });

            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }


            const contentType = response.headers.get("content-type");
            if (!contentType || !contentType.includes("application/json")) {
              throw new Error("Received non-JSON response. Check API response.");
            }
            const data = await response.json()
            console.log(data)
            if(data != "No items found for this seller") {
              const extracted_data = data;
              console.log(extracted_data);
              setSales(extracted_data)

            }
            console.log(data)
        }
        catch (err) {
            console.log(`Following error occured when fetching data: ${err}`)
            setError(err)
        }
    }
    getData()

  }, [])

  if (!sales || !Array.isArray(sales) || sales.length === 0) {
    return (
      <div className="empty-state">
        <p>No items have been added for sale.</p>
      </div>
    );
  }


  return (
    <div>
      <h3 className="text-lg font-semibold mb-2">Your Sales</h3>
      <ul>
        {sales.map((sale) => (
          <NavLink to={`/product/${sale.id}`} key={sale.id}>
            <div className="listing" >
                <img
                  src={sale.image_url}
                />
                <div className="information">
                  <h3 className="item-name">
                    {sale.name}
                  </h3>
                  <h5 className="highest-bid">Highest Bid: £
                    {/* {sale.max_bid} */}
                    500
                    </h5>
                  <h6 className="time-left">Time Left: 12 hrs</h6>
                  <p className="item-description">{sale.description.slice(0, 150)}</p>
                </div>
            </div>
          </NavLink>
        ))}
      </ul>
    </div>
  );
};

export default Sales;
