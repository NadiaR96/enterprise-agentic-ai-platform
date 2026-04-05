import { useState, useEffect } from "react";

export default function AIChat() {
  const [query, setQuery] = useState("");
  const [history, setHistory] = useState([]);
  const [userId, setUserId] = useState(localStorage.getItem("userId") || "alice");
  const [newUser, setNewUser] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [users, setUsers] = useState([]);

  // Fetch history when user changes
  useEffect(() => {
    fetchHistory(userId);
    fetchUsers();
  }, [userId]);

  // Fetch user history from backend
  const fetchHistory = async (uid) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/history/${uid}`);
      if (res.ok) {
        const data = await res.json();
        setHistory(data.history || []);
      }
    } catch (err) {
      console.error("Failed to fetch history:", err);
    }
  };

  // Fetch all users
  const fetchUsers = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/users");
      if (res.ok) {
        const data = await res.json();
        setUsers(data.users || []);
      }
    } catch (err) {
      console.error("Failed to fetch users:", err);
    }
  };

  // Send query to backend
  const sendQuery = async () => {
    if (!query) return;
    setLoading(true);
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query, user_id: userId }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      setHistory([...history, { query, response: data.answer, confidence: data.confidence, created_at: new Date().toISOString() }]);
      setQuery("");
    } catch (err) {
      console.error(err);
      setError("Failed to send query. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  // Switch to existing user or create new
  const switchUser = () => {
    if (!newUser) return;
    localStorage.setItem("userId", newUser);
    setUserId(newUser);
    setNewUser("");
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial", display: "flex", gap: "20px" }}>
      <div style={{ flex: 1 }}>
        <h2>AI Chat - User: {userId}</h2>

        {/* Switch User */}
        <div style={{ marginBottom: "10px" }}>
          <input
            placeholder="Switch user"
            value={newUser}
            onChange={(e) => setNewUser(e.target.value)}
          />
          <button onClick={switchUser}>Switch</button>
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

      {/* User List Sidebar */}
      <div
        style={{
          width: "150px",
          border: "1px solid #ddd",
          padding: "10px",
          borderRadius: "4px",
          maxHeight: "500px",
          overflowY: "auto",
        }}
      >
        <h3>Users</h3>
        {users.length > 0 ? (
          users.map((u) => (
            <div
              key={u}
              onClick={() => {
                localStorage.setItem("userId", u);
                setUserId(u);
              }}
              style={{
                padding: "8px",
                marginBottom: "4px",
                backgroundColor: u === userId ? "#007bff" : "#f0f0f0",
                color: u === userId ? "white" : "black",
                cursor: "pointer",
                borderRadius: "4px",
              }}
            >
              {u}
            </div>
          ))
        ) : (
          <div>No users yet</div>
        )}
      </div>
    </div>
  );
}
