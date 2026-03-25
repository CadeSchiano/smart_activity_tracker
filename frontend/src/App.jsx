import { useState, useEffect } from "react";
import "./App.css";

const API_URL = "https://smart-activity-tracker.onrender.com";

function App() {
  const [activities, setActivities] = useState([]);
  const [form, setForm] = useState({});
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

  const token = localStorage.getItem("token");

  useEffect(() => {
    if (token) {
      setLoggedIn(true);
      loadActivities();
    }
  }, []);

  // ---------------- LOGIN ----------------
  const login = async () => {
    const res = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(form)
    });

    const data = await res.json();

    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      setLoggedIn(true);
      loadActivities();
    } else {
      alert("Login failed");
    }
  };

  // ---------------- LOAD ----------------
  const loadActivities = async () => {
    try {
      const res = await fetch(`${API_URL}/activities`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`
        }
      });

      if (res.status === 401) {
        localStorage.clear();
        setLoggedIn(false);
        return;
      }

      const data = await res.json();
      setActivities(data.activities || []);
    } catch (err) {
      console.error(err);
      setActivities([]);
    }
  };

  // ---------------- CREATE ----------------
  const addActivity = async () => {
    await fetch(`${API_URL}/activities`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify(form)
    });
    loadActivities();
  };

  // ---------------- DELETE ----------------
  const deleteActivity = async (id) => {
    await fetch(`${API_URL}/activities/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    });
    loadActivities();
  };

  // ---------------- AI ----------------
  const askAI = async () => {
    const res = await fetch(`${API_URL}/ai/ask?q=${encodeURIComponent(question)}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    });

    if (res.status === 401) {
      alert("Session expired. Please login again.");
      localStorage.clear();
      setLoggedIn(false);
      return;
    }

    const data = await res.json();
    setAnswer(data.answer);
  };

  // ---------------- LOGIN SCREEN ----------------
  if (!loggedIn) {
  return (
    <div className="login">
      <h1>Welcome</h1>

      <input
        placeholder="username"
        onChange={(e)=>setForm({...form, username:e.target.value})}
      />

      <input
        placeholder="password"
        type="password"
        onChange={(e)=>setForm({...form, password:e.target.value})}
      />

      <button onClick={login}>Login</button>

      <button onClick={register} className="secondary">
        Register
      </button>
    </div>
  );
}

const register = async () => {
  const res = await fetch(`${API_URL}/register`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(form)
  });

  const data = await res.json();

  if (res.ok) {
    alert("Account created! You can now log in.");
  } else {
    alert(data.detail || "Error creating account");
  }
};

  // ---------------- APP ----------------
  return (
    <div className="app">
      <h1>Dashboard</h1>

      <div className="card">
        <h2>Add Activity</h2>
        <input placeholder="Title" onChange={(e)=>setForm({...form,title:e.target.value})}/>
        <input placeholder="Category" onChange={(e)=>setForm({...form,category:e.target.value})}/>
        <input placeholder="Location" onChange={(e)=>setForm({...form,location:e.target.value})}/>
        <input placeholder="Date" onChange={(e)=>setForm({...form,date:e.target.value})}/>
        <input placeholder="Time" onChange={(e)=>setForm({...form,time:e.target.value})}/>
        <button onClick={addActivity}>Add</button>
      </div>

      <div className="card">
        <h2>Activities</h2>
        {Array.isArray(activities) && activities.map(a => (
          <div key={a.id} className="activity">
            <b>{a.title}</b>
            <button onClick={()=>deleteActivity(a.id)}>Delete</button>
          </div>
        ))}
      </div>

      <div className="card">
  <h2>AI Assistant</h2>

  <input
    placeholder="Ask something about your activities..."
    value={question}
    onChange={(e)=>setQuestion(e.target.value)}
  />

  <button onClick={askAI}>Ask AI</button>

  <div className="ai-box">
    {answer ? answer : "Ask something to get insights..."}
  </div>
</div>
    </div>
  );
}


export default App;