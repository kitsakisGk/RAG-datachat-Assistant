# 🚀 Deployment Guide - Get Your App Live in 30 Minutes!

## Quick Deploy to Railway (Recommended - FREE!)

### Step 1: Create Railway Account (2 mins)
1. Go to https://railway.app
2. Click "Login with GitHub"
3. Authorize Railway

### Step 2: Create New Project (3 mins)
1. Click "New Project"
2. Choose "Deploy from GitHub repo"
3. Select your `RAG-datachat-Assistant` repository
4. Railway will auto-detect the Dockerfile!

### Step 3: Add PostgreSQL Database (2 mins)
1. Click "New" → "Database" → "PostgreSQL"
2. Railway creates a database automatically
3. Copy the `DATABASE_URL` (looks like: `postgresql://postgres:...@...railway.app:5432/railway`)

### Step 4: Set Environment Variables (5 mins)

In your Railway project, go to "Variables" and add:

```
ENVIRONMENT=production
DATABASE_TYPE=postgresql
DATABASE_URL=<paste-your-database-url-here>
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=tinyllama
JWT_SECRET=<generate-random-secret>
CORS_ORIGINS=*
```

**Generate JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 5: Deploy! (5 mins)
1. Railway automatically builds and deploys
2. Wait for build to complete (3-5 minutes)
3. Click on your app → "Settings" → Copy your URL
4. Your app is LIVE! 🎉

### Step 6: Test Your Live App (5 mins)
1. Go to: `https://your-app.railway.app/docs`
2. You should see the API documentation!
3. Test the endpoints:
   - POST `/api/auth/register` - Create an account
   - POST `/api/chat` - Ask a question!

---

## Alternative: Deploy to Render (Also FREE!)

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign in with GitHub

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name:** rag-datachat-assistant
   - **Environment:** Docker
   - **Plan:** Free

### Step 3: Add PostgreSQL
1. Click "New +" → "PostgreSQL"
2. Name it `rag-db`
3. Copy the "Internal Database URL"

### Step 4: Environment Variables
Add in Render dashboard:
```
ENVIRONMENT=production
DATABASE_TYPE=postgresql
DATABASE_URL=<your-render-postgres-url>
OLLAMA_BASE_URL=http://localhost:11434
JWT_SECRET=<random-secret>
```

### Step 5: Deploy!
Click "Create Web Service" - Render builds and deploys automatically!

---

## Running Locally with Docker

### Build and Run:
```bash
# Build
docker build -t rag-assistant .

# Run
docker run -p 8000:8000 --env-file .env rag-assistant
```

### Access:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## Important Notes for Production

### 1. Ollama in Production
**Problem:** Railway/Render don't run Ollama by default.

**Solutions:**
- **Option A (Best):** Use OpenAI API instead (add API key to env vars)
- **Option B:** Use a separate Ollama service (Modal.com or Replicate)
- **Option C:** Deploy Ollama separately and point to its URL

For now, you can test everything except chat (since chat needs Ollama).

### 2. Database Migrations
Your app auto-creates tables on startup! No manual setup needed.

### 3. File Uploads
Store uploaded documents in:
- Development: Local `data/` folder
- Production: Use cloud storage (S3, Cloudinary) - coming soon!

### 4. Monitoring
Check logs in Railway/Render dashboard to see what's happening.

---

## Troubleshooting

### Build fails?
- Check Dockerfile syntax
- Ensure all dependencies are listed
- Check Railway/Render build logs

### Database connection fails?
- Verify DATABASE_URL is correct
- Check database is running
- Ensure DATABASE_TYPE=postgresql

### App crashes on startup?
- Check environment variables
- View logs in Railway/Render
- Test locally first with Docker

---

## Cost Breakdown

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **Railway** | $5 credit/month | $0.000231/GB-hour |
| **Render** | 750 hours/month | $7/month |
| **Database** | Included | Included |

**Recommendation:** Start with Railway free tier, upgrade when you start making money!

---

## Next Steps After Deployment

1. ✅ Share your live URL!
2. ✅ Test all endpoints
3. ✅ Add your domain (optional)
4. ✅ Set up monitoring
5. ✅ You're live! 🎉

---

## Need Help?

Check logs:
- Railway: Click on service → "View Logs"
- Render: Click on service → "Logs" tab
- Local: Check `logs/` folder

Your app is ready for production! 🚀
