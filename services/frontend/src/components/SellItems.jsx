import { useEffect, useState } from "react";
  
const API_URL = import.meta.env.VITE_API_RUN_MODE === "docker"
  ? import.meta.env.VITE_API_DOCKER_API_URL
  : import.meta.env.VITE_API_LOCAL_API_URL;

const getSalesData = () => [
    { id: 1, item: "Bike", price: 100, img: "/images/bike1.jpg", description: "ndustry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum" },
    { id: 2, item: "Headphones", price: 50, img: "/images/shoe1.jpg", description: "ndustry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum" },
  ];

const Sales = () => {
  const [sales, setSales] = useState([])
  const [error, setError] = useState()

  useEffect(() => {
    async function getData() {
        try {
          // const response = await fetch(("/api-gateway/display_mainPage", {
          const response = await fetch(`${API_URL}/dashboard_sell`, {
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
            console.log(data)
            const extracted_data = data["items"];
            console.log(extracted_data)

            setSales(extracted_data)

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
      <h3 className="text-lg font-semibold mb-2">Your Sales</h3>
      <ul>
        {sales.map((sale) => (
            <div className="listing" key={sale.id}>
                <img
                  src={sale.image_url}
                />
                <div className="information">
                  <h3 className="item-name">
                    {sale.name}
                  </h3>
                  <h5 className="highest-bid">Highest Bid: £{sale.max_bid}</h5>
                  <h6 className="time-left">Time Left: 12 hrs</h6>
                  <p className="item-description">{sale.description.slice(0, 150)}</p>
                </div>
            </div>
        ))}
      </ul>
    </div>
  );
};

export default Sales;
