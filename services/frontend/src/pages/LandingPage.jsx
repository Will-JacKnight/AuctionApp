import { useEffect, useState } from 'react'
import "./../styles/landingPage.css"
import Card from "./../components/Card"
import NavBar from "./../components/NavBar"

const API_URL = import.meta.env.VITE_API_RUN_MODE === "docker"
  ? import.meta.env.VITE_API_DOCKER_API_URL
  : import.meta.env.VITE_API_LOCAL_API_URL;

 
function LandingPage()  {
  const [searchQuery, setSearchQuery] = useState("")
  const [data, setData] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function getData() {
        try {
          // const response = await fetch(("/api-gateway/display_mainPage", {
          const response = await fetch(`${API_URL}/display_mainPage`, {
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
            console.log(response)
            const data = await response.json()
            setData(data)
            console.log(data)

        }
        catch (err) {
            console.log(`Following error occured when fetching data: ${err}`)
            setError(err)
        }
    }
    getData()

  }, [])

  const  handleKeyDown = async (event) => {
    console.log(searchQuery)
    if (event.key === "Enter") {
      event.preventDefault(); // Prevents form submission reloading the page
      try {
        const response = await fetch(`${API_URL}/search`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({"query": searchQuery})
          })

          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          
          const contentType = response.headers.get("content-type");
          if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Received non-JSON response. Check API response.");
          }
          const data = await response.json()
          setData(data)

      }
      catch (err) {
          console.log(`Following error occured when fetching data: ${err}`)
          setError(err)
      }

      
    }
  };

  return (
    <div>
      {/* Navbar */}
      <NavBar />

      {/* Search Bar */}
      <div className="search-container">
        <input
          type="text"
          placeholder="Search for an item..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        {/* <button>Search</button> */}
      </div>

      {/* Popular Items Grid */}
      <div className="popular-items">
        {data && data.map((item, i) => (
          <Card data={item} key={i}/>
        ))}

      </div>
    </div>
  );
};

export default LandingPage;
