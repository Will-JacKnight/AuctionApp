import { useEffect, useState } from 'react'
import "./../styles/landingPage.css"
import Card from "./../components/Card"
import NavBar from "./../components/NavBar"
import { NavLink } from 'react-router-dom'

const API_URL =
  import.meta.env.VITE_RUN_MODE === "docker"
    // When running in Docker, we access the frontend via localhost from the browser (external access)
    ? import.meta.env.VITE_API_GATEWAY_LOCAL_URL
    : import.meta.env.VITE_RUN_MODE === "heroku"
    ? import.meta.env.VITE_API_GATEWAY_HEROKU_URL
    : import.meta.env.VITE_API_GATEWAY_LOCAL_URL;

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

  const handleSearchClick =  async (e) => {
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

  console.log(data)
  return (
    <div>
      {/* Navbar */}
      <NavBar />

      {/* Search Bar */}
      <div className="search-container">
        <div className='relative'>
          <img src="/images/search2.png" className='search-icon' onClick={handleSearchClick}></img>
          <input
          type="text"
          placeholder="Search for an item..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={handleKeyDown}>
          </input>
        </div>
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
