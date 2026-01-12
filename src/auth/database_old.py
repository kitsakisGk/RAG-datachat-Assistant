"""
Database setup and models for authentication
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Database path
DB_PATH = Path("data/users.db")


def init_database():
    """Initialize the user database with required tables"""
    # Ensure data directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            tier TEXT DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    """)

    # Usage tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # API keys table (for programmatic access)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            key_hash TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")


def get_db_connection():
    """Get database connection"""
    return sqlite3.connect(str(DB_PATH))


class UserDB:
    """User database operations"""

    @staticmethod
    def create_user(username: str, email: str, hashed_password: str, tier: str = "free") -> Optional[int]:
        """Create a new user"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, hashed_password, tier) VALUES (?, ?, ?, ?)",
                (username, email, hashed_password, tier)
            )
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            logger.info(f"User created: {username} (ID: {user_id})")
            return user_id
        except sqlite3.IntegrityError as e:
            logger.error(f"User creation failed: {e}")
            return None

    @staticmethod
    def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    @staticmethod
    def update_user_tier(user_id: int, tier: str) -> bool:
        """Update user tier (free, pro, enterprise)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET tier = ? WHERE id = ?", (tier, user_id))
            conn.commit()
            conn.close()
            logger.info(f"User {user_id} tier updated to {tier}")
            return True
        except Exception as e:
            logger.error(f"Failed to update user tier: {e}")
            return False


class UsageDB:
    """Usage tracking operations"""

    @staticmethod
    def log_action(user_id: int, action: str, metadata: str = None):
        """Log user action"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usage (user_id, action, metadata) VALUES (?, ?, ?)",
                (user_id, action, metadata)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to log action: {e}")

    @staticmethod
    def get_user_usage_count(user_id: int, action: str = None, days: int = 1) -> int:
        """Get usage count for user"""
        conn = get_db_connection()
        cursor = conn.cursor()

        if action:
            cursor.execute(
                """
                SELECT COUNT(*) FROM usage
                WHERE user_id = ? AND action = ?
                AND timestamp > datetime('now', '-' || ? || ' days')
                """,
                (user_id, action, days)
            )
        else:
            cursor.execute(
                """
                SELECT COUNT(*) FROM usage
                WHERE user_id = ?
                AND timestamp > datetime('now', '-' || ? || ' days')
                """,
                (user_id, days)
            )

        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def get_total_usage(user_id: int) -> Dict[str, int]:
        """Get total usage stats for user"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT action, COUNT(*) as count
            FROM usage
            WHERE user_id = ?
            GROUP BY action
            """,
            (user_id,)
        )

        stats = {}
        for row in cursor.fetchall():
            stats[row[0]] = row[1]

        conn.close()
        return stats


# Initialize database on module import
init_database()
