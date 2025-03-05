import { useEffect, useState } from 'react'
import "./../styles/landingPage.css"
import Card from "./../components/Card"
import NavBar from "./../components/NavBar"

const API_URL =
  import.meta.env.VITE_RUN_MODE === "docker"
    // When running in Docker, we access the frontend via localhost from the browser (external access)
    ? import.meta.env.VITE_API_GATEWAY_LOCAL_URL
    : import.meta.env.VITE_RUN_MODE === "heroku"
    ? import.meta.env.VITE_API_GATEWAY_HEROKU_URL
    : import.meta.env.VITE_API_GATEWAY_LOCAL_URL;

const tagIcons = {
  electronics: "/images/tag_icons/electronics.svg",
  books: "/images/tag_icons/books.svg",
  clothing: "/images/tag_icons/clothing.svg",
  homeDecor: "/images/tag_icons/homeDecor.svg",
  toys: "/images/tag_icons/toys.svg",
  furniture: "/images/tag_icons/furniture.svg",
  jewelry: "/images/tag_icons/jewelry.svg",
  art: "/images/tag_icons/art.svg",
  vehicles: "/images/tag_icons/vehicles.svg",
  sports: "/images/tag_icons/sports.svg",
  musical: "/images/tag_icons/musical.svg",
  antiques: "/images/tag_icons/antiques.svg",
  kitchenware: "/images/tag_icons/kitchenware.svg",
  tools: "/images/tag_icons/tools.svg",
  outdoors: "/images/tag_icons/outdoors.svg",
  petSupplies: "/images/tag_icons/petSupplies.svg",
  gaming: "/images/tag_icons/gaming.svg",
  office: "/images/tag_icons/office.svg"
};

function formatTagName(tag) {
  return tag.replace(/([a-z])([A-Z])/g, '$1 $2').replace(/^\w/, c => c.toUpperCase());
}

function LandingPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [status, setStatus] = useState('original status')
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function getData() {
      try {
        setLoading(true);
        const response = await fetch(`${API_URL}/display_mainPage`, {
          method: "GET",
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
          throw new Error("Received non-JSON response. Check API response.");
        }

        const data = await response.json();
        setData(data);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    getData();
  }, []);

  // Function to reset search query and navigate to homepage
  const resetHomepage = () => {
    setSearchQuery("");  // Reset search query
    navigate("/");  // Navigate to homepage
  };
  

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      setStatus('original status');
      try {
        setLoading(true);
        // Fetch all items from the API when search query is empty
        const response = await fetch(`${API_URL}/display_mainPage`, {
          method: "GET", // Assuming you use a GET request to fetch all items
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        setData(data); // Show all items
      } catch (err) {
        console.error("Error fetching items:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
      return
    }

    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: searchQuery })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setData(data);
    } catch (err) {
      console.error("Error searching:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTagSearch = async (tag) => {
    try {
      console.log(tag);
      setLoading(true);
      const response = await fetch(`${API_URL}/search_byTag`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query_tag: tag })
      });
      
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      console.log(data);

      setData(data);
    } catch (err) {
      console.error("Error searching by tag:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="landing-page">
      <NavBar resetHomepage={resetHomepage} />
      
      <div className="search-section">
        <h1 className="search-title">Find Your Next Great Deal</h1>
        <p className="search-subtitle">Discover unique items at amazing prices</p>
        
        <form onSubmit={handleSearch} className="search-form">
              <input
                type="text"
                placeholder="Search for items..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-input"
              />
              <button type="submit" className="search-button">
                <img src="/images/Search Icon.svg" alt="Search Icon" className="search-icon" />
              </button>
        </form>
      </div>

      <div className="tag-search-container">
        <div className="tag-search">
          {Object.keys(tagIcons).map((tag, index) => (
            <div
              className="tag-item"
              key={index}
              onClick={() => handleTagSearch(tag)}
            >
              <img src={tagIcons[tag]} alt={`${tag} icon`} className="tag-icon" />
              <span className="tag-name">{formatTagName(tag)}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="content-section">
        {loading ? (
          <div className="loading-state">
            <p>Loading items...</p>
          </div>
        ) : error ? (
          <div className="error-state">
            <p>Error: {error}</p>
          </div>
        ) : data.length === 0 ? (
          <div className="empty-state">
            <p>No items found. Try a different search term.</p>
          </div>
        ) : (
          <div className="popular-items">
            {data.map((item, i) => (
              <Card data={item} key={i} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default LandingPage;
