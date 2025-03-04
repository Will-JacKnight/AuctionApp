import { Navigate, Outlet } from "react-router-dom";

const ProtectedRoute = () => {
  const token = sessionStorage.getItem("token");
  if (!token) {
    sessionStorage.setItem("lastVisited", location.pathname);
    return <Navigate to="/login" replace />;
  }
  return <Outlet />
};

export default ProtectedRoute;
