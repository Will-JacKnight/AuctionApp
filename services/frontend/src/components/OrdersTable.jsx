/* eslint-disable react/prop-types */
import "./../styles/ordersTable.css";
import { NavLink } from "react-router-dom";
const OrderTable = ({ data }) => {  
  let groupNum = -1;
  let lastName = null;

  const formatter = new Intl.DateTimeFormat("en-GB", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  });

  if (!data || !Array.isArray(data) || data.length === 0) {
    return (
      <div className="empty-state">
        <p>No items have been bid.</p>
      </div>
    );
  }
  console.log(data)
  // Filter out any null or invalid items
  const validData = data.filter(item => item && typeof item === 'object');

  // Sort items: first by name (A-Z), then by created_at (latest first)
  const sortedData = [...validData].sort((a, b) => {
    // First, sort alphabetically by item_name
    if (a.item_name < b.item_name) return -1;
    if (a.item_name > b.item_name) return 1;

    // If item_name is the same, sort by created_at (newest first)
    return new Date(b.created_at) - new Date(a.created_at);
  });

  return (
    <>
      <h3 className="text-lg font-semibold mb-2">Your Bids</h3>
      <div className="table-container">
      <table className="order-table">
        <thead>
          <tr>
            <th>Item Name</th>
            <th>Bid Amount</th>
            <th>Time</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {sortedData.map((order, index) => {
            if (!order?.item_name) return null;
            
            if (order.item_name !== lastName) {
              groupNum++;
              lastName = order.item_name;
            }

            // Determine row highlight condition: If expired and the bid is the highest
            const isWinningExpiredBid = order.status === "expired" && order.bid_amount === order.max_bid;

            return (
             
              <tr key={index} className={`${groupNum % 2 === 0 ? "group-even" : "group-odd"} ${isWinningExpiredBid ? "highlight-row" : ""}`}>
                <td>
                  <div className="item-cell">
                    <NavLink to={`/product/${order.product_id}`}>
                      {order.item_name}
                    </NavLink>
                  </div>
                </td>
                <td>£{order.bid_amount?.toLocaleString() || '0'}</td>
                <td>{order.created_at ? formatter.format(new Date(order.created_at)) : 'N/A'}</td>
                <td>
                  <span className={`${order.status === "active" ? "bid-status-green" : isWinningExpiredBid ? "bid-status-yellow" : "bid-status-red"}`}>
                    {order.status === "active" ? "Active" : isWinningExpiredBid ? "Won" : "Sold"}
                  </span>
                </td>
              </tr>
              
            );
          })}
        </tbody>
      </table>
    </div>
    </>
    
  );
};

export default OrderTable;