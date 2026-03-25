import { useState } from "react";
import "./App.css";

const DEFAULT_LOCAL_API_URL = "http://127.0.0.1:8000";
const DEFAULT_PROD_API_URL = "https://smart-activity-tracker.onrender.com";
const isLocalhost =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1";
const API_URL = (
  import.meta.env.VITE_API_URL ||
  (isLocalhost ? DEFAULT_LOCAL_API_URL : DEFAULT_PROD_API_URL)
).replace(/\/$/, "");

const parseResponse = async (res) => {
  const text = await res.text();

  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch {
    return { detail: text };
  }
};

function App() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [loggedIn, setLoggedIn] = useState(false);
  const [isRegister, setIsRegister] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // ---------------- LOGIN ----------------
  const login = async () => {
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await parseResponse(res);

      if (res.ok) {
        localStorage.setItem("token", data.access_token);
        setLoggedIn(true);
      } else {
        alert(data?.detail || `Login failed (${res.status})`);
      }
    } catch {
      alert(`Cannot reach API at ${API_URL}`);
    }

    setLoading(false);
  };

  // ---------------- REGISTER ----------------
  const register = async () => {
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await parseResponse(res);

      if (res.ok) {
        alert("Account created! Please login.");
        setIsRegister(false);
        setForm({ email: "", password: "" });
      } else {
        alert(data?.detail || `Register failed (${res.status})`);
      }
    } catch {
      alert(`Cannot reach API at ${API_URL}`);
    }

    setLoading(false);
  };

  // ---------------- AUTH UI ----------------
  if (!loggedIn) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <h1 className="title">
            {isRegister ? "Create Account" : "Welcome Back"}
          </h1>

          <p className="subtitle">
            {isRegister
              ? "Sign up to start tracking your activities"
              : "Login to continue"}
          </p>

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

          <button
            disabled={loading}
            onClick={isRegister ? register : login}
          >
            {loading
              ? "Processing..."
              : isRegister
              ? "Create Account"
              : "Login"}
          </button>

          <p className="switch">
            {isRegister
              ? "Already have an account?"
              : "Don't have an account?"}
            <span onClick={() => setIsRegister(!isRegister)}>
              {isRegister ? " Login" : " Register"}
            </span>
          </p>
        </div>
      </div>
    );
  }

  // ---------------- DASHBOARD ----------------
  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <button onClick={() => setLoggedIn(false)}>Logout</button>
      <p>You are logged in 🎉</p>
    </div>
  );
}

export default App;
