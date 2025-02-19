/* eslint-disable react/prop-types */
import { useState } from "react";
import "../styles/card.css"

function Card({data}) {
    return (
        <div className="popular-items">
          <div className="item-card">
            <img src={data.img} className="item-card-img"/>
            <div className="item-card-description">
                <p>{data.name}</p>
                <div className="item-card-price-time">
                    <p className="smaller-font">Current Bid: {data.currentBid}</p>
                    <p className="grey-text">2 Days</p>
                </div>
                
            </div>
          </div>
      </div>
        
    )
}

export default Card;