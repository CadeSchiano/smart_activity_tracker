import { useState } from "react";
import "./App.css";

const API_URL = "https://smart-activity-tracker.onrender.com";

function App() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [loggedIn, setLoggedIn] = useState(false);
  const [isRegister, setIsRegister] = useState(false);

  // ---------------- LOGIN ----------------
  const login = async () => {
    const res = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      setLoggedIn(true);
    } else {
      alert(data.detail || "Login failed");
    }
  };

  // ---------------- REGISTER ----------------
  const register = async () => {
    const res = await fetch(`${API_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    const data = await res.json();

    if (res.ok) {
      alert("Account created! Please login.");
      setIsRegister(false); // switch to login screen
    } else {
      alert(data.detail || "Register failed");
    }
  };

  // ---------------- LOGOUT ----------------
  const logout = () => {
    localStorage.removeItem("token");
    setLoggedIn(false);
  };

  // ---------------- AUTH SCREENS ----------------
  if (!loggedIn) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <h1>{isRegister ? "Create Account" : "Welcome Back"}</h1>

          <input
            placeholder="Username"
            value={form.username}
            onChange={(e) =>
              setForm({ ...form, username: e.target.value })
            }
          />

          <input
            placeholder="Password"
            type="password"
            value={form.password}
            onChange={(e) =>
              setForm({ ...form, password: e.target.value })
            }
          />

          <button onClick={isRegister ? register : login}>
            {isRegister ? "Register" : "Login"}
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

  // ---------------- DASHBOARD ----------------
  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <button onClick={logout}>Logout</button>
      <p>You are logged in 🎉</p>
    </div>
  );
}

export default App;