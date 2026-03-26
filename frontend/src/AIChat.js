import { useState } from "react";

export default function AIChat() {
  const [query, setQuery] = useState("");
  const [history, setHistory] = useState([]); // initialize as empty array
  const [userId, setUserId] = useState("alice");
  const [newUser, setNewUser] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Send query to backend
  const sendQuery = async () => {
    if (!query) return;
    setLoading(true);
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ q: query, user_id: userId }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      setHistory(data.history || []); // fallback to empty array
      setQuery("");
    } catch (err) {
      console.error(err);
      setError("Failed to send query. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  // Switch to a different user
  const switchUser = () => {
    if (!newUser) return;
    setUserId(newUser);
    setHistory([]); // clear local history; optionally fetch from backend
    setNewUser("");
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
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
          minHeight: "100px",
        }}
      >
        {history && history.length > 0 ? (
          history.map((h, i) => (
            <div key={i} style={{ marginBottom: "8px" }}>
              <b>{h.query}</b> → {h.response}
            </div>
          ))
        ) : (
          <div>No messages yet</div>
        )}
      </div>
    </div>
  );
}