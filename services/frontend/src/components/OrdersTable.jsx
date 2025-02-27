/* eslint-disable react/prop-types */
import "./../styles/ordersTable.css"

const OrderTable = ({data}) => {  
  let groupNum = -1
  let lastName = null

  const formatter = new Intl.DateTimeFormat("en-GB", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  });

  if (!data) {
    return "No items have been bid"
  }

  return (
    <div className="table-container">
      <table className="order-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Bid Amount</th>
            <th>Time</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          
          {data?.map((order, index) => {
            if (order?.item_name != lastName) {
              groupNum++
              lastName = order?.item_name
            }
            return (
            <tr key={index} className={groupNum % 2 === 0 ? "group-even" : "group-odd"}>
              <td>{order?.item_name}</td>
              <td>{order?.bid_amount}</td>
              <td>{order?.created_at && formatter.format(new Date(order.created_at))}</td>
              <td><span className={`${order?.status == "'active'" ? "bid-status-green" : "bid-status-red"}`}>{order?.status == "'active'" ? "Active" : "Sold"}</span></td>
            </tr>
            );
          })
          
          
          }
        </tbody>
      </table>
    </div>
  );
};

export default OrderTable;
