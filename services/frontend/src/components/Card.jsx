/* eslint-disable react/prop-types */
import { useState } from "react";
import "../styles/card.css"
import { NavLink } from "react-router-dom";

function Card({data}) {
    const [imageLoaded, setImageLoaded] = useState(false);

    const handleImageLoad = () => {
        setImageLoaded(true);
    };

    return (
      <NavLink to={`/product/${data.id}`} className="card-link">
        <div className="item-card">
          <img 
            src={data.image_url} 
            className={`item-card-img ${!imageLoaded ? 'loading' : ''}`}
            alt={data.name}
            onLoad={handleImageLoad}
          />
          <div className="item-card-description">
            <div className="item-card-title-container">
              <p className="item-card-name">{data.name}</p>
              <p className="item-card-time">
                {data.remaining_days <= 1 ? 'Less than 24 hours' : `${data.remaining_days} Days`}
              </p>
            </div>
            <p className="item-card-price">
              {data.max_bid !== null ? `Current Bid: £${data.max_bid.toLocaleString()}` : `Starting Price: £${data.starting_price.toLocaleString()}`}
            </p>
          </div>
        </div>
      </NavLink>
    );
}

export default Card;