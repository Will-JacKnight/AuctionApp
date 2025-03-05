import { useState } from "react";
import Biddings from "../components/BidItems";
import Sales from "../components/SellItems";
import "./../styles/dashboard.css"
import NavBar from "../components/NavBar";


const Dashboard = () => {
  const [activeTab, setActiveTab] = useState("biddings");

  return (
    <>
      <NavBar />
      <div className="p-4">
      <h2 className="">Dashboard</h2>

      {/* Toggle Buttons */}
      <div className="flex space-x-4 mb-4">

        <div className="btns-container">
            <button
            className={`p-2 ${activeTab === "biddings" ? "bg-blue-500 text-white btn-active" : "bg-gray-200 btn-inactive"} toggle-btns`}
            onClick={() => setActiveTab("biddings")}
            >
            Biddings
            </button>
            <button
            className={`p-2 ${activeTab === "sales" ? "bg-blue-500 text-white btn-active" : "bg-gray-200 btn-inactive"} toggle-btns`}
            onClick={() => setActiveTab("sales")}
            >
            Sales
        </button>
        </div>

      </div>

      {/* Show the selected tab content */}
      <div className="listing-section">
        {activeTab === "biddings" ? <Biddings /> : <Sales />}
      </div>
      
    </div>
    </>
    
  );
};

export default Dashboard;