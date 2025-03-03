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
                <p>{data.item_name}</p>
                <div className="item-card-price-time">
                    <p className="smaller-font">Current Bid: £{data.starting_price}</p>
                    <p className="grey-text">2 Days</p>
                </div>
                
            </div>
          </div>
        </div>
      </NavLink>
        
        
    )
}

export default Card;