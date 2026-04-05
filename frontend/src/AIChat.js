import { useState, useEffect } from "react";

export default function AIChat() {
  const [query, setQuery] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [user, setUser] = useState(null);
  const [loginForm, setLoginForm] = useState({ username: "", password: "" });
  const [registerForm, setRegisterForm] = useState({ username: "", password: "", email: "" });
  const [showRegister, setShowRegister] = useState(false);

  // Check authentication on mount
  useEffect(() => {
    if (token) {
      validateToken();
    }
  }, []);

  // Fetch user history when authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      fetchHistory();
    }
  }, [isAuthenticated, user]);

  const validateToken = async () => {
    try {
      console.debug("validateToken token:", token);
      const headers = { Authorization: `Bearer ${token}` };
      console.debug("validateToken headers:", headers);
      const res = await fetch("http://127.0.0.1:8000/auth/me", {
        headers
      });
      if (res.ok) {
        const userData = await res.json();
        setUser(userData);
        setIsAuthenticated(true);
      } else {
        console.warn("validateToken failed with status", res.status);
        logout();
      }
    } catch (err) {
      console.error("validateToken error", err);
      logout();
    }
  };

  const login = async () => {
    try {
      const formData = new FormData();
      formData.append("username", loginForm.username);
      formData.append("password", loginForm.password);

      const res = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        body: formData
      });

      if (res.ok) {
        const data = await res.json();
        const accessToken = data.access_token;
        
        // Save token first
        localStorage.setItem("token", accessToken);
        setToken(accessToken);
        setLoginForm({ username: "", password: "" });
        
        // Validate token with the actual token value (not state)
        try {
          const headers = { Authorization: `Bearer ${accessToken}` };
          const meRes = await fetch("http://127.0.0.1:8000/auth/me", {
            headers
          });
          if (meRes.ok) {
            const userData = await meRes.json();
            setUser(userData);
            setIsAuthenticated(true);
          } else {
            console.warn("validateToken failed with status", meRes.status);
            setError("Failed to validate token");
            logout();
          }
        } catch (err) {
          console.error("validateToken error", err);
          setError("Failed to validate token");
          logout();
        }
      } else {
        setError("Login failed");
      }
    } catch (err) {
      console.error("Login error:", err);
      setError("Login failed");
    }
  };

  const register = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(registerForm)
      });

      if (res.ok) {
        setError("Registration successful! Please login.");
        setShowRegister(false);
        setRegisterForm({ username: "", password: "", email: "" });
      } else {
        setError("Registration failed");
      }
    } catch (err) {
      setError("Registration failed");
    }
  };

  const logout = () => {
    setToken("");
    setUser(null);
    setIsAuthenticated(false);
    setHistory([]);
    localStorage.removeItem("token");
  };

  // Fetch user history from backend
  const fetchHistory = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/history", {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setHistory(data.history || []);
      }
    } catch (err) {
      console.error("Failed to fetch history:", err);
    }
  };

  // Send query to backend
  const sendQuery = async () => {
    if (!query || !isAuthenticated) return;
    setLoading(true);
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ query: query }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      setHistory([...history, {
        query,
        response: data.response.answer,
        confidence: data.response.confidence,
        created_at: new Date().toISOString()
      }]);
      setQuery("");
    } catch (err) {
      console.error(err);
      setError("Failed to send query. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div style={{ padding: "20px", fontFamily: "Arial", maxWidth: "400px", margin: "0 auto" }}>
        <h2>Enterprise AI Platform</h2>

        {showRegister ? (
          <div>
            <h3>Register</h3>
            <input
              type="text"
              placeholder="Username"
              value={registerForm.username}
              onChange={(e) => setRegisterForm({...registerForm, username: e.target.value})}
              style={{ display: "block", margin: "10px 0", width: "100%" }}
            />
            <input
              type="email"
              placeholder="Email"
              value={registerForm.email}
              onChange={(e) => setRegisterForm({...registerForm, email: e.target.value})}
              style={{ display: "block", margin: "10px 0", width: "100%" }}
            />
            <input
              type="password"
              placeholder="Password"
              value={registerForm.password}
              onChange={(e) => setRegisterForm({...registerForm, password: e.target.value})}
              style={{ display: "block", margin: "10px 0", width: "100%" }}
            />
            <button onClick={register} style={{ marginRight: "10px" }}>Register</button>
            <button onClick={() => setShowRegister(false)}>Back to Login</button>
          </div>
        ) : (
          <div>
            <h3>Login</h3>
            <input
              type="text"
              placeholder="Username"
              value={loginForm.username}
              onChange={(e) => setLoginForm({...loginForm, username: e.target.value})}
              style={{ display: "block", margin: "10px 0", width: "100%" }}
            />
            <input
              type="password"
              placeholder="Password"
              value={loginForm.password}
              onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
              style={{ display: "block", margin: "10px 0", width: "100%" }}
            />
            <button onClick={login} style={{ marginRight: "10px" }}>Login</button>
            <button onClick={() => setShowRegister(true)}>Register</button>
            <p style={{ fontSize: "12px", marginTop: "10px", color: "#666" }}>
              Demo accounts: admin/admin, user1/password
            </p>
          </div>
        )}

        {error && <div style={{ color: "red", marginTop: "10px" }}>{error}</div>}
      </div>
    );
  }

  return (
    <div style={{ padding: "20px", fontFamily: "Arial", display: "flex", gap: "20px" }}>
      <div style={{ flex: 1 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
          <h2>AI Chat - User: {user?.user_id} ({user?.roles?.join(", ")})</h2>
          <button onClick={logout} style={{ padding: "5px 10px" }}>Logout</button>
        </div>

        {/* Query Input */}
        <div style={{ marginBottom: "10px" }}>
          <input
            style={{ width: "300px" }}
            placeholder="Type your query..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button onClick={sendQuery} disabled={loading}>
            {loading ? "Sending..." : "Send"}
          </button>
        </div>

        {/* Error message */}
        {error && <div style={{ color: "red", marginBottom: "10px" }}>{error}</div>}

        {/* Chat History */}
        <div
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            width: "400px",
            minHeight: "300px",
            maxHeight: "500px",
            overflowY: "auto",
          }}
        >
          {history && history.length > 0 ? (
            history.map((h, i) => (
              <div key={i} style={{ marginBottom: "12px", paddingBottom: "8px", borderBottom: "1px solid #eee" }}>
                <b>Q:</b> {h.query} <br />
                <b>A:</b> {typeof h.response === "object" ? JSON.stringify(h.response) : h.response} <br />
                <small>Confidence: {(h.confidence * 100).toFixed(0)}%</small>
              </div>
            ))
          ) : (
            <div>No messages yet</div>
          )}
        </div>
      </div>
    </div>
  );
}
