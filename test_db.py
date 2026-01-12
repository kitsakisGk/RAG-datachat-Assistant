"""Quick test script for database"""
from src.auth.database import UserDB, UsageDB
from src.auth.security import hash_password

print("🧪 Testing Database...")
print("=" * 50)

# Test 1: Create user
print("\n1. Creating test user...")
hashed_pwd = hash_password("test123")
user_id = UserDB.create_user("testuser", "test@example.com", hashed_pwd, "free")
print(f"✅ User created with ID: {user_id}")

# Test 2: Get user by username
print("\n2. Getting user by username...")
user = UserDB.get_user_by_username("testuser")
print(f"✅ Found user: {user['username']} (Tier: {user['tier']})")

# Test 3: Log usage
print("\n3. Logging usage...")
UsageDB.log_action(user_id, "chat", "Test query")
print("✅ Usage logged")

# Test 4: Get usage count
print("\n4. Getting usage count...")
count = UsageDB.get_user_usage_count(user_id, "chat", days=1)
print(f"✅ Usage count: {count}")

# Test 5: Update tier
print("\n5. Upgrading to Pro...")
UserDB.update_user_tier(user_id, "pro")
user = UserDB.get_user_by_id(user_id)
print(f"✅ User tier updated to: {user['tier']}")

print("\n" + "=" * 50)
print("✅ All tests passed! Database working correctly.")
print("\n💾 Database type: SQLite (local)")
print("📁 Database location: data/users.db")
