import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../index.css"; // Import global styles

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

    const handleSignup = async (e) => {
        e.preventDefault();
        setError(null); // Clear previous errors

        try {
            const response = await fetch("http://localhost:5000/api/signup", {
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
                setError(data.error || "Signup failed");
            }
        } catch (err) {
            console.log(err)
            setError("Network error. Please try again.");
        }
    };

    return (
        <div className="auth-form">
            <h2>Sign Up</h2>
            {error && <p className="error-message">{error}</p>}
            <form onSubmit={handleSignup}>
                <input type="email" placeholder="Email" required value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} />
                <input type="text" placeholder="Username" required value={formData.username} onChange={(e) => setFormData({ ...formData, username: e.target.value })} />
                <input type="password" placeholder="Password" required value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} />
                <input type="text" placeholder="First Name" required value={formData.firstname} onChange={(e) => setFormData({ ...formData, firstname: e.target.value })} />
                <input type="text" placeholder="Surname" required value={formData.surname} onChange={(e) => setFormData({ ...formData, surname: e.target.value })} />
                <input type="text" placeholder="Address" required value={formData.address} onChange={(e) => setFormData({ ...formData, address: e.target.value })} />
                <input type="tel" placeholder="Phone Number" required value={formData.phone} onChange={(e) => setFormData({ ...formData, phone: e.target.value })} />
                <button type="submit">Sign Up</button>
            </form>
            <p>Already have an account? <a href="/frontend/public">Log in</a></p>
        </div>
    );
};

export default SignupPage;