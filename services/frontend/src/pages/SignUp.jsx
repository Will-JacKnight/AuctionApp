import { useState } from "react";
import { useNavigate } from "react-router-dom";
// import "../styles/index.css"; // Import global styles
import "./../styles/authentication.css"
import NavBar from "../components/NavBar";
// import { getApiUrl } from '../config';

  const API_URL =
  import.meta.env.VITE_RUN_MODE === "docker"
    // When running in Docker, we access the frontend via localhost from the browser (external access)
    ? import.meta.env.VITE_API_GATEWAY_LOCAL_URL
    : import.meta.env.VITE_RUN_MODE === "heroku"
    ? import.meta.env.VITE_API_GATEWAY_HEROKU_URL
    : import.meta.env.VITE_API_GATEWAY_LOCAL_URL;

const SignupPage = () => {
    const [formData, setFormData] = useState({
        email: "",
        username: "",
        password: "",
        firstname: "",
        surname: "",
        address: "",
        phone: "",
    });
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const [usernameError, setUsernameError] = useState(null); 

    const handleSignup = async (e) => {
        e.preventDefault();
        setError(null); // Clear previous errors

        try {
            const response = await fetch(`${API_URL}/signup`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            if (response.ok) {
                console.log(data.token)
                alert("Signup successful! Please log in.");
                navigate("/login"); // Redirect to login page
            } else {
                if (data.error === "Username already exists") {
                    setUsernameError(data.error);
                }
                else {
                setError(data.error || "Signup failed");
            }
            }
        } catch (err) {
            console.log(err)
            setError("Network error. Please try again.");
        }
    };

    return (
        <>
            <NavBar />
            <div className="auth-form form">
            <h2>Sign Up</h2>
            {error && <p className="error-message">{error}</p>}
            <form onSubmit={handleSignup}>
                {usernameError && <p className="error-message">{usernameError}</p>} {/* Display Username Error */}
                <input type="email" placeholder="Email" required value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} />
                <input type="text" placeholder="Username" required value={formData.username} onChange={(e) => setFormData({ ...formData, username: e.target.value })} />
                <input type="password" placeholder="Password" required value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} />
                <input type="text" placeholder="First Name" required value={formData.firstname} onChange={(e) => setFormData({ ...formData, firstname: e.target.value })} />
                <input type="text" placeholder="Surname" required value={formData.surname} onChange={(e) => setFormData({ ...formData, surname: e.target.value })} />
                <input type="text" placeholder="Address" required value={formData.address} onChange={(e) => setFormData({ ...formData, address: e.target.value })} />
                <input type="tel" placeholder="Phone Number" required value={formData.phone} onChange={(e) => setFormData({ ...formData, phone: e.target.value })} />
                <button type="submit">Sign Up</button>
            </form>
            <p>Already have an account? <a href="/login">Log in</a></p>
        </div>
        </>
       
    );
};

export default SignupPage;