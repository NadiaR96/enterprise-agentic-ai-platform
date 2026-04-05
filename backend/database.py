import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "app.db"

def init_db():
    """Initialize SQLite database with users and conversations tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        confidence REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )''')
    
    conn.commit()
    conn.close()

def get_or_create_user(user_id: str):
    """Create user if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if not c.fetchone():
        c.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
    
    conn.close()

def save_conversation(user_id: str, query: str, response: dict):
    """Save a query-response pair to the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    get_or_create_user(user_id)
    
    c.execute(
        "INSERT INTO conversations (user_id, query, response, confidence) VALUES (?, ?, ?, ?)",
        (user_id, query, json.dumps(response), response.get("confidence", 0.0))
    )
    conn.commit()
    conn.close()

def get_user_history(user_id: str):
    """Retrieve all conversations for a user."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute(
        "SELECT query, response, confidence, created_at FROM conversations WHERE user_id = ? ORDER BY created_at",
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()
    
    return [
        {
            "query": row[0],
            "response": json.loads(row[1]),
            "confidence": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]

def get_all_users():
    """Get list of all users."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users ORDER BY created_at DESC")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

# Initialize database on module import
init_db()
