import { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const sendQuery = async () => {
    const userId = "user_1"; // simulate login
    
    const res = await axios.get("http://localhost:8000/query", {
      params: { q: query, user_id: userId }
    });

    setMessages([
      ...messages,
      { user: query, bot: res.data.response }
    ]);

    setQuery("");
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Agentic AI Platform</h2>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={sendQuery}>Send</button>

      <div>
        {messages.map((m, i) => (
          <div key={i}>
            <p><b>User:</b> {m.user}</p>
            <p><b>AI:</b> {m.bot}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;