import { useEffect, useState } from "react";
import OrderTable from "./OrdersTable";

const getBiddingsData = () => [
    { id: 1, item: "Laptop", amount: 450, time: "24/02/2025 10:30", status: "Active" },
    { id: 1, item: "Laptop", amount: 500, time: "24/02/2025 12:30", status: "Active"},
    { id: 1, item: "Laptop", amount: 550, time: "25/02/2025 15:37", status: "Sold"},

    { id: 2, item: "Smartphone", amount: 250, time: "23/02/2025 09:20", status: "Active"},
    { id: 2, item: "Smartphone", amount: 250, time: "24/02/2025 11:45", status: "Active"},
    { id: 2, item: "Smartphone", amount: 250, time: "25/02/2025 16:51", status: "Sold"},
  ];
  
const Biddings = () => {
  const [biddings, setBiddings] = useState([null]);

  useEffect(() => {
    setBiddings(getBiddingsData());
  }, []);

  return (
    <div>
      <h3 className="text-lg font-semibold mb-2">Your Biddings</h3>
      {console.log(biddings)}
      {biddings && <OrderTable data={biddings}/>}
        
    </div>
  );
};

export default Biddings;
