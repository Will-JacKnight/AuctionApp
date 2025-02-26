import { useEffect, useState } from "react";
  
const getSalesData = () => [
    { id: 1, item: "Bike", price: 100, img: "/images/bike1.jpg", description: "ndustry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum" },
    { id: 2, item: "Headphones", price: 50, img: "/images/shoe1.jpg", description: "ndustry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum" },
  ];

const Sales = () => {
  const [sales, setSales] = useState([]);

  useEffect(() => {
    setSales(getSalesData());
  }, []);

  return (
    <div>
      <h3 className="text-lg font-semibold mb-2">Your Sales</h3>
      <ul>
        {sales.map((sale) => (
            <div className="listing" key={sale.id}>
                <img
                  src={sale.img}
                />
                <div className="information">
                  <h3 className="item-name">
                    {sale.item}
                  </h3>
                  <h5 className="highest-bid">Highest Bid: £{sale.price}</h5>
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
