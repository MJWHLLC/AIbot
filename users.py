"""Simple SQLite-backed user management for the scaffold.

Provides create_user, get_user, list_users, and delete_user. Passwords are
stored as salted hashes using Werkzeug's `generate_password_hash`.
"""
from __future__ import annotations

import os
import sqlite3
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from werkzeug.security import generate_password_hash, check_password_hash


DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_table():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            token_type TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users (username)
        )
        """
    )
    conn.commit()
    conn.close()


def create_user(username: str, password: str, is_admin: bool = False) -> None:
    _ensure_table()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
        (username, generate_password_hash(password), 1 if is_admin else 0),
    )
    conn.commit()
    conn.close()


def get_user(username: str) -> Optional[Dict]:
    _ensure_table()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, is_admin FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {"id": row["id"], "username": row["username"], "password_hash": row["password_hash"], "is_admin": bool(row["is_admin"]) }


def list_users() -> List[Dict]:
    _ensure_table()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, is_admin FROM users ORDER BY username")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r["id"], "username": r["username"], "is_admin": bool(r["is_admin"])} for r in rows]


def delete_user(username: str) -> None:
    _ensure_table()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()


def verify_password(username: str, password: str) -> bool:
    user = get_user(username)
    if not user:
        return False
    return check_password_hash(user["password_hash"], password)


def generate_token(username: str, token_type: str, expires_in_hours: int = 24) -> str:
    """Generate a secure token for password-reset or invite.
    
    token_type: 'password_reset' or 'invite'
    Returns: the token string
    """
    _ensure_table()
    token = secrets.token_urlsafe(32)
    now = datetime.utcnow()
    expires_at = (now + timedelta(hours=expires_in_hours)).isoformat()
    created_at = now.isoformat()
    
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tokens (token, username, token_type, expires_at, created_at) VALUES (?, ?, ?, ?, ?)",
        (token, username, token_type, expires_at, created_at),
    )
    conn.commit()
    conn.close()
    return token


def validate_token(token: str, token_type: str) -> Optional[str]:
    """Validate a token and return the associated username.
    
    Returns None if token is invalid, expired, or of wrong type.
    """
    _ensure_table()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT username, expires_at FROM tokens WHERE token = ? AND token_type = ?",
        (token, token_type),
    )
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return None
    
    expires_at = datetime.fromisoformat(row["expires_at"])
    if datetime.utcnow() > expires_at:
        return None
    
    return row["username"]


def consume_token(token: str) -> None:
    """Delete a token after it has been used."""
    _ensure_table()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM tokens WHERE token = ?", (token,))
    conn.commit()
    conn.close()
