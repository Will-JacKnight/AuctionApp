import { useState } from 'react';
import "./../styles/landingPage.css";
import Card from "./../components/Card"

 
function LandingPage()  {
  const [searchQuery, setSearchQuery] = useState("");
  const popularItems = [
    { id: 1, name: "Vintage Watch", currentBid: "$120", img: "/images/watch1.jpg" },
    { id: 2, name: "Classic Painting", currentBid: "$450", img: "/images/car1.jpg" },
    { id: 3, name: "Antique Vase", currentBid: "$200", img: "/images/watch1.jpg" },
    { id: 4, name: "Limited Edition Sneakers", currentBid: "$300", img: "/images/shoe1.jpg" },
    { id: 1, name: "Vintage Watch", currentBid: "$120", img: "/images/hat1.jpg" },
    { id: 2, name: "Classic Painting", currentBid: "$450", img: "/images/watch2.jpg" },
    { id: 3, name: "Antique Vase", currentBid: "$200", img: "/images/bike1.jpg" },
    { id: 4, name: "Limited Edition Sneakers", currentBid: "$300", img: "/images/watch1.jpg" }
  ];

  return (
    <div>
      {/* Navbar */}
      <nav className="navbar">
        <h1>BiddingHub</h1>
        {/* <img src="/images/navbar-logo.png" id='navbar-logo'/> */}
        <ul>
          <li><a href="#home">Sell</a></li>
          <li><a href="#auctions">Dashboard</a></li>
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
        {/* <button>Search</button> */}
      </div>

      {/* Popular Items Grid */}
      <div className="popular-items">
        {popularItems.map((item, i) => (
          <Card data={item} key={i}/>
        ))}

      </div>
    </div>
  );
};

export default LandingPage;
