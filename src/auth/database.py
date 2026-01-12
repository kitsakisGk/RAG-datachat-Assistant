"""
Modern database layer using SQLAlchemy
Supports both SQLite (dev) and PostgreSQL (production)
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from pathlib import Path

from src.auth.models import Base, User, Usage, APIKey
from src.config import get_database_url, DATABASE_TYPE, SQLITE_PATH
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Create engine
if DATABASE_TYPE == "sqlite":
    # SQLite specific settings
    Path(SQLITE_PATH).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(
        get_database_url(),
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
else:
    # PostgreSQL settings
    engine = create_engine(
        get_database_url(),
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_database():
    """Initialize database - create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info(f"Database initialized successfully ({DATABASE_TYPE})")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserDB:
    """User database operations"""

    @staticmethod
    def create_user(username: str, email: str, hashed_password: str, tier: str = "free") -> Optional[int]:
        """Create a new user"""
        db = SessionLocal()
        try:
            user = User(
                username=username,
                email=email,
                hashed_password=hashed_password,
                tier=tier
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"User created: {username} (ID: {user.id})")
            return user.id
        except Exception as e:
            db.rollback()
            logger.error(f"User creation failed: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if user:
                return {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "hashed_password": user.hashed_password,
                    "tier": user.tier,
                    "created_at": user.created_at.isoformat(),
                    "is_active": user.is_active
                }
            return None
        finally:
            db.close()

    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if user:
                return {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "hashed_password": user.hashed_password,
                    "tier": user.tier,
                    "created_at": user.created_at.isoformat(),
                    "is_active": user.is_active
                }
            return None
        finally:
            db.close()

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                return {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "hashed_password": user.hashed_password,
                    "tier": user.tier,
                    "created_at": user.created_at.isoformat(),
                    "is_active": user.is_active
                }
            return None
        finally:
            db.close()

    @staticmethod
    def update_user_tier(user_id: int, tier: str) -> bool:
        """Update user tier (free, pro, enterprise)"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.tier = tier
                db.commit()
                logger.info(f"User {user_id} tier updated to {tier}")
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update user tier: {e}")
            return False
        finally:
            db.close()

    @staticmethod
    def get_all_users(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all users (for admin)"""
        db = SessionLocal()
        try:
            users = db.query(User).offset(skip).limit(limit).all()
            return [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "tier": user.tier,
                    "created_at": user.created_at.isoformat(),
                    "is_active": user.is_active
                }
                for user in users
            ]
        finally:
            db.close()


class UsageDB:
    """Usage tracking operations"""

    @staticmethod
    def log_action(user_id: int, action: str, metadata: str = None):
        """Log user action"""
        db = SessionLocal()
        try:
            usage = Usage(
                user_id=user_id,
                action=action,
                metadata=metadata
            )
            db.add(usage)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to log action: {e}")
        finally:
            db.close()

    @staticmethod
    def get_user_usage_count(user_id: int, action: str = None, days: int = 1) -> int:
        """Get usage count for user"""
        db = SessionLocal()
        try:
            cutoff_time = datetime.utcnow() - timedelta(days=days)
            query = db.query(Usage).filter(
                Usage.user_id == user_id,
                Usage.timestamp > cutoff_time
            )

            if action:
                query = query.filter(Usage.action == action)

            count = query.count()
            return count
        finally:
            db.close()

    @staticmethod
    def get_total_usage(user_id: int) -> Dict[str, int]:
        """Get total usage stats for user"""
        db = SessionLocal()
        try:
            results = db.query(
                Usage.action,
                func.count(Usage.id).label('count')
            ).filter(
                Usage.user_id == user_id
            ).group_by(Usage.action).all()

            stats = {action: count for action, count in results}
            return stats
        finally:
            db.close()

    @staticmethod
    def get_recent_activity(user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activity for user"""
        db = SessionLocal()
        try:
            activities = db.query(Usage).filter(
                Usage.user_id == user_id
            ).order_by(Usage.timestamp.desc()).limit(limit).all()

            return [
                {
                    "action": activity.action,
                    "timestamp": activity.timestamp.isoformat(),
                    "metadata": activity.metadata
                }
                for activity in activities
            ]
        finally:
            db.close()


# Initialize database on module import
init_database()
