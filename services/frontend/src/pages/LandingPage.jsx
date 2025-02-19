import { useState } from 'react';
import "./../styles/landingPage.css";
 
const LandingPage = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const popularItems = [
    { id: 1, name: "Vintage Watch", currentBid: "$120" },
    { id: 2, name: "Classic Painting", currentBid: "$450" },
    { id: 3, name: "Antique Vase", currentBid: "$200" },
    { id: 4, name: "Limited Edition Sneakers", currentBid: "$300" },
  ];

  return (
    <div>
      {/* Navbar */}
      <nav className="navbar">
        <h1>BiddingHub</h1>
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#auctions">Auctions</a></li>
          <li><a href="#categories">Categories</a></li>
          <li><a href="#profile">Profile</a></li>
        </ul>
      </nav>

      {/* Search Bar */}
      <div className="search-container">
        <input
          type="text"
          placeholder="Search for an item..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button>Search</button>
      </div>

      {/* Popular Items Grid */}
      <div className="popular-items">
        {popularItems.map((item) => (
          <div key={item.id} className="item-card">
            <h3>{item.name}</h3>
            <p>Current Bid: {item.currentBid}</p>
            <button>Bid Now</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LandingPage;
