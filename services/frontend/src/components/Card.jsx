/* eslint-disable react/prop-types */
import "../styles/card.css"
import { NavLink } from "react-router-dom";

function Card({data}) {
    return (
      <NavLink to={`/product/${data.id}`}>
        <div className="popular-items">
          <div className="item-card">
            <img src={data.image_url} className="item-card-img"/>
            <div className="item-card-description">
                
                {/* Flex container for name and time */}
                <div className="item-card-title-container">
                    <p className="item-card-name">{data.name}</p>
                    <p className="item-card-time">2 Days</p>
                </div>

                {/* Display Current Bid if available, otherwise show Starting Price */}
                <p className="item-card-price">
                    {data.max_bid !== null ? `Current Bid: £${data.max_bid}` : `Current Bid: £${data.starting_price}`}
                </p>
                
            </div>
          </div>
        </div>
      </NavLink>
    )
}

export default Card;