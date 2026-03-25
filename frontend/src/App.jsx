import { useState } from "react";
import "./App.css";

const API_URL = "https://smart-activity-tracker.onrender.com";

function App() {
  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const [loggedIn, setLoggedIn] = useState(false);

  // ---------------- LOGIN ----------------
  const login = async () => {
    try {
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
    } catch (err) {
      alert("Server error");
    }
  };

  // ---------------- REGISTER ----------------
  const register = async () => {
    try {
      const res = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (res.ok) {
        alert("Account created! Now log in.");
      } else {
        alert(data.detail || "Registration failed");
      }
    } catch (err) {
      alert("Server error");
    }
  };

  // ---------------- LOGOUT ----------------
  const logout = () => {
    localStorage.removeItem("token");
    setLoggedIn(false);
  };

  // ---------------- LOGIN SCREEN ----------------
  if (!loggedIn) {
    return (
      <div className="login">
        <h1>Login</h1>

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

        <button onClick={login}>Login</button>
        <button onClick={register} className="secondary">
          Register
        </button>
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