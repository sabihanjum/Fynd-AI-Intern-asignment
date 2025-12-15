# Deployment Guide - Render.com

This guide walks through deploying both the Flask backend and HTML frontends to Render.com.

## Step 1: Prepare Repository

### Modify Flask app to serve frontend

Edit `task-2/backend/app.py` and add this after the CORS configuration:

```python
from flask import send_from_directory

# Serve frontend files
@app.route('/')
@app.route('/user')
def user_dashboard():
    return send_from_directory('../frontend', 'index.html')

@app.route('/admin')
def admin_dashboard():
    return send_from_directory('../frontend', 'admin.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('../frontend', filename)
```

### Update requirements.txt

Ensure `task-2/backend/requirements.txt` includes:

```
Flask==3.0.0
flask-cors==4.0.0
python-dotenv==1.0.0
google-generativeai==0.3.0
requests==2.31.0
gunicorn==21.2.0
```

### Create render.yaml

Create `render.yaml` in project root:

```yaml
services:
  - type: web
    name: fynd-ai-backend
    runtime: python
    rootDir: task-2/backend
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn app:app"
    envVars:
      - key: GEMINI_API_KEY
        scope: build,runtime
      - key: PYTHON_VERSION
        value: 3.9
```

## Step 2: Push to GitHub

```bash
cd c:\Users\Sabiha Anjum\Documents\Fynd AI Intern asignment

# Initialize git repo
git init
git add .
git commit -m "Initial commit: Complete Fynd AI Assessment solution"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/fynd-ai-assessment.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Render

### Option A: Using render.yaml (Recommended)

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Select the repository
6. Render will auto-detect `render.yaml`
7. Click "Deploy"
8. Wait for build to complete (~2-3 minutes)

### Option B: Manual Setup

1. **Deploy Backend**:
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect GitHub account
   - Select `fynd-ai-assessment` repository
   - Settings:
     - Name: `fynd-ai-backend`
     - Environment: `Python`
     - Root directory: `task-2/backend`
     - Build command: `pip install -r requirements.txt`
     - Start command: `gunicorn app:app`
   - Click "Advanced" and add environment variable:
     - Key: `GEMINI_API_KEY`
     - Value: [Your Gemini API Key]
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)

2. **Get your API URL**:
   - Once deployed, copy the URL (e.g., `https://fynd-ai-backend-xyz.onrender.com`)
   - This is your `API_BASE_URL`

3. **Update Frontend API URL**:
   - Edit `task-2/frontend/index.html`:
     ```javascript
     const API_URL = 'https://fynd-ai-backend-xyz.onrender.com/api';
     ```
   - Edit `task-2/frontend/admin.html`:
     ```javascript
     const API_URL = 'https://fynd-ai-backend-xyz.onrender.com/api';
     ```

4. **Push changes to GitHub**:
   ```bash
   git add .
   git commit -m "Update API URLs for Render deployment"
   git push
   ```

5. **Redeploy Flask service**:
   - Go to Render dashboard
   - Select `fynd-ai-backend`
   - Click "Manual Deploy" → "Deploy latest commit"
   - Wait for redeployment

## Step 4: Test Deployment

### Test Backend API
```bash
# Health check
curl https://your-render-url.onrender.com/api/health

# Get all reviews
curl https://your-render-url.onrender.com/api/reviews

# Get stats
curl https://your-render-url.onrender.com/api/stats
```

### Test User Dashboard
Open in browser: `https://your-render-url.onrender.com/user`

### Test Admin Dashboard
Open in browser: `https://your-render-url.onrender.com/admin`

## Step 5: Final Submission

Update your README with actual deployment URLs:

```markdown
## Deployment Links

- **User Dashboard**: https://your-render-url.onrender.com/user
- **Admin Dashboard**: https://your-render-url.onrender.com/admin
- **API Base URL**: https://your-render-url.onrender.com/api
```

## Troubleshooting

### Build Failed
- Check that Python version is 3.9+
- Verify `requirements.txt` is in correct directory
- Check for syntax errors in app.py

### API Not responding
- Check GEMINI_API_KEY is set correctly
- Look at deployment logs in Render dashboard
- Ensure app.py has correct syntax

### CORS errors
- Verify Flask-CORS is in requirements.txt
- Check frontend API_URL matches backend URL
- Ensure trailing slashes are correct

### Auto-refresh not working (Admin Dashboard)
- Check browser console for errors
- Verify API URLs are correct
- Check CORS configuration in Flask

## Alternative Deployment Platforms

### Heroku (Paid, but reliable)
```bash
heroku create fynd-ai-backend
heroku config:set GEMINI_API_KEY=your_key
git subtree push --prefix task-2/backend heroku main
```

### Railway.app
- Similar to Render
- More generous free tier
- Auto-deploying from GitHub

### PythonAnywhere
- Specifically for Python
- Easy Flask deployment
- Limited free tier

### AWS Free Tier
- EC2 instance
- More complex setup
- More powerful

---

## Important Notes

1. **Cold Starts**: Render may have 15-30 second cold starts on free tier
   - This is normal behavior
   - Premium plans have faster starts

2. **Database**: Currently using JSON file
   - For production, migrate to PostgreSQL (Render offers free PostgreSQL)
   - Update connection string in app.py

3. **Auto-refresh**: Admin dashboard auto-refreshes every 10 seconds
   - This may increase server load
   - Adjust interval in `admin.html` if needed

4. **Rate Limiting**: Not implemented yet
   - Add `flask-limiter` for production

5. **Security**: 
   - No authentication currently
   - Add login/API keys for production
   - Use HTTPS (automatically on Render)

## Success Indicators

✅ You'll know it's working when:
- User dashboard loads without errors
- Star rating selector works
- Submitting review returns AI response
- Admin dashboard shows statistics
- Auto-refresh updates the feed
- All API endpoints respond correctly

---

**Estimated Time to Deploy**: 15-20 minutes
**Cost**: Free (Render free tier)
**Uptime**: 97%+ on free tier

For questions, refer to [Render Documentation](https://render.com/docs)
