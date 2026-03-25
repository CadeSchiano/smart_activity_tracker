import { useState } from "react";
import "./App.css";

const API_URL = "https://smart-activity-tracker.onrender.com";

function App() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [loggedIn, setLoggedIn] = useState(false);
  const [isRegister, setIsRegister] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const login = async () => {
    setLoading(true);

    const res = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(form),
    });

    const data = await res.json();
    setLoading(false);

    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      setLoggedIn(true);
    } else {
      alert(data.detail || "Login failed");
    }
  };

  const register = async () => {
    setLoading(true);

    const res = await fetch(`${API_URL}/register`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(form),
    });

    const data = await res.json();
    setLoading(false);

    if (res.ok) {
      alert("Account created! Please login.");
      setIsRegister(false);
      setForm({ email: "", password: "" });
    } else {
      alert(data.detail || "Register failed");
    }
  };

  if (!loggedIn) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <h1>{isRegister ? "Create Account" : "Welcome Back"}</h1>

          <input
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
          />

          <input
            name="password"
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
          />

          <button onClick={isRegister ? register : login}>
            {loading ? "Loading..." : isRegister ? "Register" : "Login"}
          </button>

          <p className="switch">
            {isRegister ? "Already have an account?" : "Don't have an account?"}
            <span onClick={() => setIsRegister(!isRegister)}>
              {isRegister ? " Login" : " Register"}
            </span>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <button onClick={() => setLoggedIn(false)}>Logout</button>
    </div>
  );
}

export default App;