import { useState } from "react";
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
  const [activityForm, setActivityForm] = useState({
    title: "",
    category: "",
    location: "",
    date: "",
    time: "",
  });
  const [token, setToken] = useState(null);
  const [loggedIn, setLoggedIn] = useState(false);
  const [isRegister, setIsRegister] = useState(false);
  const [loading, setLoading] = useState(false);
  const [activities, setActivities] = useState([]);
  const [dashboardLoading, setDashboardLoading] = useState(false);
  const [dashboardError, setDashboardError] = useState("");
  const [submittingActivity, setSubmittingActivity] = useState(false);
  const [aiQuestion, setAiQuestion] = useState("");
  const [aiAnswer, setAiAnswer] = useState("");
  const [aiSummary, setAiSummary] = useState("");
  const [aiLoading, setAiLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleActivityChange = (e) => {
    setActivityForm({ ...activityForm, [e.target.name]: e.target.value });
  };

  const loadActivities = async (accessToken = token) => {
    if (!accessToken) {
      setActivities([]);
      setDashboardError("");
      return;
    }

    setDashboardLoading(true);
    setDashboardError("");

    try {
      const res = await fetch(`${API_URL}/activities`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      const data = await parseResponse(res);

      if (res.ok) {
        setActivities(data?.activities || []);
      } else if (res.status === 401) {
        setToken(null);
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

  const fetchAiSummary = async () => {
    if (!token) {
      setLoggedIn(false);
      return;
    }

    setAiLoading(true);
    setDashboardError("");

    try {
      const res = await fetch(`${API_URL}/ai/summary`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await parseResponse(res);

      if (res.ok) {
        setAiSummary(data?.summary || "No summary available.");
      } else if (res.status === 401) {
        setToken(null);
        setLoggedIn(false);
        setActivities([]);
        setDashboardError("Your session expired. Please log in again.");
      } else {
        setDashboardError(data?.detail || `Failed to load AI summary (${res.status})`);
      }
    } catch {
      setDashboardError(`Cannot reach API at ${API_URL}`);
    }

    setAiLoading(false);
  };

  const askAiQuestion = async () => {
    if (!token) {
      setLoggedIn(false);
      return;
    }

    setAiLoading(true);
    setDashboardError("");

    try {
      const res = await fetch(`${API_URL}/ai/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ q: aiQuestion }),
      });

      const data = await parseResponse(res);

      if (res.ok) {
        setAiAnswer(data?.answer || "No answer available.");
      } else if (res.status === 401) {
        setToken(null);
        setLoggedIn(false);
        setActivities([]);
        setDashboardError("Your session expired. Please log in again.");
      } else {
        setDashboardError(data?.detail || `Failed to ask AI (${res.status})`);
      }
    } catch {
      setDashboardError(`Cannot reach API at ${API_URL}`);
    }

    setAiLoading(false);
  };

  const createActivity = async () => {
    if (!token) {
      setLoggedIn(false);
      return;
    }

    setSubmittingActivity(true);
    setDashboardError("");

    try {
      const res = await fetch(`${API_URL}/activities`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(activityForm),
      });

      const data = await parseResponse(res);

      if (res.ok) {
        setActivityForm({
          title: "",
          category: "",
          location: "",
          date: "",
          time: "",
        });
        setActivities((current) => [data, ...current]);
      } else if (res.status === 401) {
        setToken(null);
        setLoggedIn(false);
        setActivities([]);
        setDashboardError("Your session expired. Please log in again.");
      } else {
        setDashboardError(data?.detail || `Failed to create activity (${res.status})`);
      }
    } catch {
      setDashboardError(`Cannot reach API at ${API_URL}`);
    }

    setSubmittingActivity(false);
  };

  const deleteActivity = async (id) => {
    if (!token) {
      setLoggedIn(false);
      return;
    }

    setDashboardError("");

    try {
      const res = await fetch(`${API_URL}/activities/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await parseResponse(res);

      if (res.ok) {
        setActivities((current) => current.filter((activity) => activity.id !== id));
      } else if (res.status === 401) {
        setToken(null);
        setLoggedIn(false);
        setActivities([]);
        setDashboardError("Your session expired. Please log in again.");
      } else {
        setDashboardError(data?.detail || `Failed to delete activity (${res.status})`);
      }
    } catch {
      setDashboardError(`Cannot reach API at ${API_URL}`);
    }
  };

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
        setToken(data.access_token);
        setLoggedIn(true);
        await loadActivities(data.access_token);
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
        <main className="auth-card">
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

          <form
            onSubmit={(event) => {
              event.preventDefault();
              isRegister ? register() : login();
            }}
          >
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={form.email}
              onChange={handleChange}
            />

            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete={isRegister ? "new-password" : "current-password"}
              minLength="8"
              maxLength="128"
              required
              value={form.password}
              onChange={handleChange}
            />

            <button disabled={loading} type="submit">
              {loading ? "Processing..." : isRegister ? "Create Account" : "Login"}
            </button>
          </form>

          <p className="switch">
            {isRegister
              ? "Already have an account?"
              : "Don't have an account?"}
            <button type="button" className="link-button" onClick={() => setIsRegister(!isRegister)}>
              {isRegister ? " Login" : " Register"}
            </button>
          </p>
        </main>
      </div>
    );
  }

  // ---------------- DASHBOARD ----------------
  return (
    <main className="dashboard">
      <div className="dashboard-header">
        <div>
          <p className="eyebrow">Smart Activity Tracker</p>
          <h1>Dashboard</h1>
        </div>

        <button
          className="logout-button"
          onClick={() => {
            setToken(null);
            setActivities([]);
            setDashboardError("");
            setLoggedIn(false);
          }}
        >
          Logout
        </button>
      </div>

      <section className="dashboard-card activity-form-card">
        <h2>Add Activity</h2>
        <form className="activity-form-grid" onSubmit={(event) => { event.preventDefault(); createActivity(); }}>
          <label htmlFor="activity-title">Activity title
            <input id="activity-title" name="title" maxLength="200" required value={activityForm.title} onChange={handleActivityChange} />
          </label>
          <label htmlFor="activity-category">Category
            <input id="activity-category" name="category" maxLength="200" required value={activityForm.category} onChange={handleActivityChange} />
          </label>
          <label htmlFor="activity-location">Location
            <input id="activity-location" name="location" maxLength="300" required value={activityForm.location} onChange={handleActivityChange} />
          </label>
          <label htmlFor="activity-date">Date
            <input id="activity-date" name="date" type="date" required value={activityForm.date} onChange={handleActivityChange} />
          </label>
          <label htmlFor="activity-time">Time
            <input id="activity-time" name="time" type="time" required value={activityForm.time} onChange={handleActivityChange} />
          </label>
          <button
            className="primary-action"
            type="submit"
            disabled={
              submittingActivity ||
              !activityForm.title ||
              !activityForm.category ||
              !activityForm.location ||
              !activityForm.date ||
              !activityForm.time
            }
            onClick={createActivity}
          >
            {submittingActivity ? "Saving..." : "Add activity"}
          </button>
        </form>
      </section>

      <section className="dashboard-card ai-card">
        <div className="ai-header">
          <div>
            <h2>AI Assistant</h2>
            <p>Generate a summary or ask a question about this account's activities.</p>
          </div>
          <button
            className="secondary-action"
            disabled={aiLoading || activities.length === 0}
            onClick={fetchAiSummary}
          >
            {aiLoading ? "Working..." : "Generate summary"}
          </button>
        </div>

        <form className="ai-question-row" onSubmit={(event) => { event.preventDefault(); askAiQuestion(); }}>
          <label htmlFor="ai-question">Ask a question about your activities
            <input
              id="ai-question"
              name="aiQuestion"
              maxLength="1000"
              required
              value={aiQuestion}
              onChange={(e) => setAiQuestion(e.target.value)}
            />
          </label>
          <button
            className="primary-action"
            type="submit"
            disabled={aiLoading || !aiQuestion.trim() || activities.length === 0}
            onClick={askAiQuestion}
          >
            {aiLoading ? "Working..." : "Ask AI"}
          </button>
        </form>

        {aiSummary && (
          <div className="ai-output" aria-live="polite">
            <h3>Summary</h3>
            <p>{aiSummary}</p>
          </div>
        )}

        {aiAnswer && (
          <div className="ai-output" aria-live="polite">
            <h3>Answer</h3>
            <p>{aiAnswer}</p>
          </div>
        )}
      </section>

      {dashboardLoading ? (
          <div className="dashboard-card" aria-live="polite">
          <p>Loading your activities...</p>
        </div>
      ) : dashboardError ? (
          <div className="dashboard-card" role="alert">
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
              <button
                className="delete-activity-button"
                onClick={() => deleteActivity(activity.id)}
              >
                Delete
              </button>
            </article>
          ))}
        </div>
      )}
    </main>
  );
}

export default App;
