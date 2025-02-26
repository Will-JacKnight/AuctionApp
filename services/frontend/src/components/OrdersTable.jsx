/* eslint-disable react/prop-types */
import "./../styles/ordersTable.css"

const OrderTable = ({data}) => {  
  let groupNum = -1
  let lastName = null

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
            if (order?.item != lastName) {
              groupNum++
              lastName = order?.item
            }
            console.log(order)
            return (
            <tr key={index} className={groupNum % 2 === 0 ? "group-even" : "group-odd"}>
              <td>{order?.item}</td>
              <td>{order?.amount}</td>
              <td>{order?.time}</td>
              <td><span className={`${order?.status == "Active" ? "bid-status-green" : "bid-status-red"}`}>{order?.status}</span></td>
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
