import { useEffect, useState } from "react";
import "./App.css";

const DEFAULT_LOCAL_API_URL = "http://127.0.0.1:8000";
const DEFAULT_PROD_API_URL = "https://smart-activity-tracker.onrender.com";
const isLocalhost =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1";

const getApiUrl = () => {
  const configuredUrl = import.meta.env.VITE_API_URL?.trim();
  const fallbackUrl = isLocalhost ? DEFAULT_LOCAL_API_URL : DEFAULT_PROD_API_URL;

  if (!configuredUrl) {
    return { apiUrl: fallbackUrl, configError: "" };
  }

  try {
    const normalizedUrl = new URL(configuredUrl).toString().replace(/\/$/, "");
    return { apiUrl: normalizedUrl, configError: "" };
  } catch {
    return {
      apiUrl: fallbackUrl,
      configError: `Invalid VITE_API_URL "${configuredUrl}". Using ${fallbackUrl} instead.`,
    };
  }
};

const { apiUrl: API_URL, configError: API_CONFIG_ERROR } = getApiUrl();

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
  const [loggedIn, setLoggedIn] = useState(() => Boolean(localStorage.getItem("token")));
  const [isRegister, setIsRegister] = useState(false);
  const [loading, setLoading] = useState(false);
  const [activities, setActivities] = useState([]);
  const [dashboardLoading, setDashboardLoading] = useState(false);
  const [dashboardError, setDashboardError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const loadActivities = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      setActivities([]);
      setDashboardError("");
      return;
    }

    setDashboardLoading(true);
    setDashboardError("");

    try {
      const res = await fetch(`${API_URL}/activities`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await parseResponse(res);

      if (res.ok) {
        setActivities(data?.activities || []);
      } else if (res.status === 401) {
        localStorage.removeItem("token");
        setLoggedIn(false);
        setActivities([]);
        setDashboardError("Your session expired. Please log in again.");
      } else {
        setActivities([]);
        setDashboardError(data?.detail || `Failed to load dashboard (${res.status})`);
      }
    } catch {
      setActivities([]);
      setDashboardError(`Cannot reach API at ${API_URL}`);
    }

    setDashboardLoading(false);
  };

  useEffect(() => {
    if (loggedIn) {
      loadActivities();
    }
  }, [loggedIn]);

  // ---------------- LOGIN ----------------
  const login = async () => {
    setLoading(true);

    try {
      if (API_CONFIG_ERROR) {
        alert(API_CONFIG_ERROR);
      }

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
      if (API_CONFIG_ERROR) {
        alert(API_CONFIG_ERROR);
      }

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

          {API_CONFIG_ERROR && (
            <p className="subtitle">
              Config issue detected. Requests are using {API_URL}
            </p>
          )}

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
      <div className="dashboard-header">
        <div>
          <p className="eyebrow">Smart Activity Tracker</p>
          <h1>Dashboard</h1>
        </div>

        <button
          className="logout-button"
          onClick={() => {
            localStorage.removeItem("token");
            setActivities([]);
            setDashboardError("");
            setLoggedIn(false);
          }}
        >
          Logout
        </button>
      </div>

      {dashboardLoading ? (
        <div className="dashboard-card">
          <p>Loading your activities...</p>
        </div>
      ) : dashboardError ? (
        <div className="dashboard-card">
          <p>{dashboardError}</p>
        </div>
      ) : activities.length === 0 ? (
        <div className="dashboard-card">
          <h2>No activities yet</h2>
          <p>Your account is working. Add your first activity to populate the dashboard.</p>
        </div>
      ) : (
        <div className="activity-grid">
          {activities.map((activity) => (
            <article key={activity.id} className="activity-card">
              <div className="activity-card-top">
                <span className="activity-category">{activity.category || "Uncategorized"}</span>
                <span className="activity-time">{activity.time || "No time set"}</span>
              </div>
              <h2>{activity.title || "Untitled activity"}</h2>
              <p>{activity.location || "No location provided"}</p>
              <p>{activity.date || "No date provided"}</p>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
