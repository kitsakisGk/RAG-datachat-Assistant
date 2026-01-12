# 🔐 Authentication System Testing Guide

## Setup

1. **Install PyJWT** (required for JWT tokens):
```bash
pip install pyjwt
```

2. **Restart the API** (if it's running):
- Press `CTRL+C` in your terminal
- Run: `python -m uvicorn src.api.main:app --reload --port 8000`

## Test the Authentication

### 1. Register a New User

Open http://localhost:8000/docs and try:

**POST /api/auth/register**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

You'll get back a **JWT token**! Copy it.

### 2. Test Protected Chat Endpoint

**POST /api/chat** (with authentication)

1. Click "Authorize" button in Swagger UI (top right)
2. Paste your token
3. Try asking a question!

Now you'll see:
- ✅ Usage tracking
- ✅ Rate limits (10 queries/day for free tier)
- ✅ User profile with stats

### 3. Check Your Profile

**GET /api/auth/me**
- Click "Authorize" and paste your token
- See your stats!

## What's Different Now?

### Before Auth:
- Anyone could use the API unlimited
- No tracking
- Can't charge money

### After Auth:
- ✅ User accounts
- ✅ **Rate limits per tier** (FREE: 10/day, PRO: 1000/day, ENTERPRISE: unlimited)
- ✅ Usage tracking
- ✅ Ready for payments!

## Rate Limits

| Tier | Daily Limit | Price |
|------|-------------|-------|
| Free | 10 queries | $0 |
| Pro | 1,000 queries | $9.99/month |
| Enterprise | Unlimited | Contact us |

## Upgrade a User (Manual for now)

You can manually upgrade users in the database:

```python
from src.auth.database import UserDB
UserDB.update_user_tier(user_id=1, tier="pro")
```

Later we'll add Stripe payment integration!

## Next Steps for Monetization

1. ✅ Auth system (DONE!)
2. Add Stripe payment integration
3. Add pricing page in UI
4. Deploy to production
5. Start making money! 💰
